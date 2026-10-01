"""Deterministic, synthetic-only offline performance baseline for P1-005."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import io
import json
import math
import os
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from backend.app.core.config import Settings
from backend.app.services.document_parsing import DocumentPreparationService
from backend.app.services.document_registry import DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import (
    DOCX_MEDIA_TYPE,
    PDF_MEDIA_TYPE,
    DocumentValidator,
)
from backend.app.services.draft_validation import validate_canonical_draft
from backend.app.services.patent_docx_renderer import PatentDocxRenderer


REPORT_SCHEMA_VERSION = "1.0.0"
TASK_ID = "P1-005"
AUTHORIZATION = "HUMAN-P1-005-OFFLINE-PERFORMANCE-BASELINE-2026-10-01"
CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
INTERNAL_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="officeDocument" Target="word/document.xml"/>
</Relationships>"""


@dataclass(frozen=True, slots=True)
class BenchmarkConfig:
    warmups: int = 1
    samples: int = 5
    profile: str = "baseline"
    include_browser: bool = True

    def __post_init__(self) -> None:
        if self.warmups < 0:
            raise ValueError("warmups must be zero or greater")
        if self.samples < 1:
            raise ValueError("samples must be one or greater")
        if self.profile not in {"ci", "baseline"}:
            raise ValueError("profile must be 'ci' or 'baseline'")


class _SyntheticUpload:
    def __init__(self, payload: bytes) -> None:
        self._source = io.BytesIO(payload)

    async def read(self, size: int) -> bytes:
        return self._source.read(size)


def calculate_statistics(samples_ms: list[float]) -> dict[str, Any]:
    """Return stable nearest-rank p95 and median statistics."""

    if not samples_ms:
        raise ValueError("at least one timing sample is required")
    ordered = sorted(float(value) for value in samples_ms)
    p95_index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return {
        "sample_count": len(ordered),
        "median_ms": round(statistics.median(ordered), 3),
        "p95_ms": round(ordered[p95_index], 3),
        "min_ms": round(ordered[0], 3),
        "max_ms": round(ordered[-1], 3),
        "samples_ms": [round(value, 3) for value in samples_ms],
    }


def measure(
    name: str,
    operation: Callable[[], Mapping[str, Any] | None],
    *,
    warmups: int,
    samples: int,
    workload: Mapping[str, Any],
) -> dict[str, Any]:
    """Measure an operation with a monotonic, high-resolution clock."""

    for _ in range(warmups):
        operation()
    timings: list[float] = []
    observed: Mapping[str, Any] = {}
    for _ in range(samples):
        started = time.perf_counter_ns()
        observed = operation() or {}
        timings.append((time.perf_counter_ns() - started) / 1_000_000)
    return {
        "name": name,
        "status": "MEASURED",
        "workload": dict(workload),
        "observed": dict(observed),
        "timing": calculate_statistics(timings),
    }


def _pdf_literal(text: str) -> bytes:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("latin-1")


def synthetic_pdf(page_count: int, *, words_per_page: int = 80, padding_bytes: int = 0) -> bytes:
    """Build a deterministic text-layer PDF without external data."""

    if page_count < 1 or words_per_page < 1 or padding_bytes < 0:
        raise ValueError("PDF fixture dimensions must be positive")
    writer = PdfWriter()
    for page_index in range(page_count):
        token = f"sensor-{page_index:02d}"
        text = " ".join(["Synthetic", token, "calibration", "evidence"] * max(1, words_per_page // 4))
        page = writer.add_blank_page(width=612, height=792)
        font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            }
        )
        font_ref = writer._add_object(font)  # pypdf has no public API for this fixture wiring.
        page[NameObject("/Resources")] = DictionaryObject(
            {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref})}
        )
        stream = DecodedStreamObject()
        stream.set_data(b"BT /F1 10 Tf 50 740 Td (" + _pdf_literal(text) + b") Tj ET")
        page[NameObject("/Contents")] = writer._add_object(stream)
    if padding_bytes:
        padding = DecodedStreamObject()
        padding.set_data(b"P" * padding_bytes)
        writer._add_object(padding)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def _stable_text(index: int, character_count: int) -> str:
    pieces: list[str] = []
    counter = 0
    while sum(map(len, pieces)) < character_count:
        pieces.append(hashlib.sha256(f"p1-005:{index}:{counter}".encode()).hexdigest())
        counter += 1
    return "".join(pieces)[:character_count]


def _zip_write(package: zipfile.ZipFile, name: str, data: str) -> None:
    info = zipfile.ZipInfo(name, date_time=(2026, 10, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o600 << 16
    package.writestr(info, data.encode("utf-8"))


def synthetic_docx(paragraph_count: int, *, chars_per_paragraph: int = 160) -> bytes:
    """Build a byte-reproducible minimal DOCX with deterministic paragraphs."""

    if paragraph_count < 1 or chars_per_paragraph < 1:
        raise ValueError("DOCX fixture dimensions must be positive")
    paragraphs = "".join(
        '<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
        % escape(f"Synthetic paragraph {index:04d} {_stable_text(index, chars_per_paragraph)}")
        for index in range(paragraph_count)
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{paragraphs}</w:body></w:document>"
    )
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as package:
        _zip_write(package, "[Content_Types].xml", CONTENT_TYPES)
        _zip_write(package, "_rels/.rels", INTERNAL_RELS)
        _zip_write(package, "word/document.xml", document_xml)
    return output.getvalue()


def fixture_metadata(payload: bytes, **details: Any) -> dict[str, Any]:
    return {"size_bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), **details}


def validate_report(report: Mapping[str, Any]) -> None:
    """Fail closed on the stable machine-readable report contract."""

    required = {"schema_version", "task_id", "authorization", "generated_at", "environment", "config", "cases"}
    if set(report) != required:
        raise ValueError("benchmark report fields do not match schema v1")
    if report["schema_version"] != REPORT_SCHEMA_VERSION or report["task_id"] != TASK_ID:
        raise ValueError("benchmark report identity is invalid")
    cases = report["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("benchmark report must contain cases")
    for case in cases:
        if case.get("status") != "MEASURED" or case.get("timing", {}).get("sample_count", 0) < 1:
            raise ValueError("benchmark case is incomplete")


def evaluate_thresholds(report: Mapping[str, Any], thresholds: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate optional local ceilings; CI never supplies these thresholds."""

    cases = {case["name"]: case for case in report["cases"]}
    failures: list[dict[str, Any]] = []
    for name, rule in thresholds.items():
        if name not in cases or not isinstance(rule, Mapping):
            raise ValueError(f"unknown or invalid threshold case: {name}")
        for metric in ("median_ms", "p95_ms"):
            ceiling_key = f"{metric}_max"
            if ceiling_key in rule:
                actual = cases[name]["timing"][metric]
                ceiling = float(rule[ceiling_key])
                if actual > ceiling:
                    failures.append({"case": name, "metric": metric, "actual": actual, "ceiling": ceiling})
    return {"status": "PASS" if not failures else "FAIL", "failures": failures}


def _environment() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "processor": platform.processor() or "unknown",
        "logical_cpu_count": os.cpu_count(),
        "clock": "time.perf_counter_ns",
        "live_flags": {"RUN_OPENAI_LIVE_TESTS": "0", "RUN_OPENAI_DRAFT_LIVE_TESTS": "0"},
        "provider_api_calls": "NONE",
    }


def _load_draft_assets() -> tuple[dict[str, Any], dict[str, Any]]:
    schema = json.loads((ROOT / "schemas/patent-draft/v1.0.0/patent-draft.schema.json").read_text(encoding="utf-8"))
    case = json.loads((ROOT / "tests/fixtures/patent-draft/v1.0.0/cases/representative.json").read_text(encoding="utf-8"))
    return schema, case["expected_output"]


def _backend_cases(config: BenchmarkConfig, workspace: Path) -> list[dict[str, Any]]:
    dimensions = ({"small": (1, 10), "medium": (10, 250), "near_limit": (50, 2000)} if config.profile == "baseline" else {"ci": (1, 5)})
    settings = Settings(storage_root=workspace / "uploads", local_export_root=workspace / "exports")
    validator = DocumentValidator(settings)
    storage = DocumentStorage(
        settings.storage_root,
        ttl_seconds=settings.upload_ttl_seconds,
        max_upload_bytes=settings.max_upload_bytes,
        read_chunk_bytes=settings.read_chunk_bytes,
    )
    parser = DocumentPreparationService(storage, DocumentRegistry(), max_source_unit_chars=settings.max_source_unit_chars)
    schema, draft = _load_draft_assets()
    renderer = PatentDocxRenderer(output_root=settings.local_export_root)
    cases: list[dict[str, Any]] = []
    fixtures: dict[str, tuple[Path, Path, bytes, bytes, int, int]] = {}

    for label, (pages, paragraphs) in dimensions.items():
        pdf = synthetic_pdf(pages)
        docx = synthetic_docx(paragraphs)
        pdf_path = workspace / f"{label}.pdf"
        docx_path = workspace / f"{label}.docx"
        pdf_path.write_bytes(pdf)
        docx_path.write_bytes(docx)
        fixtures[label] = (pdf_path, docx_path, pdf, docx, pages, paragraphs)

        cases.append(measure(
            f"upload_document_validation_pdf_{label}",
            lambda payload=pdf, name=pdf_path.name: _upload_validate_observed(storage, validator, payload, name),
            warmups=config.warmups, samples=config.samples,
            workload=fixture_metadata(pdf, format="PDF", page_count=pages),
        ))
        cases.append(measure(
            f"pdf_parsing_{label}",
            lambda path=pdf_path: _parse_observed(parser._parse_pdf(path)),
            warmups=config.warmups, samples=config.samples,
            workload=fixture_metadata(pdf, format="PDF", page_count=pages),
        ))
        cases.append(measure(
            f"docx_parsing_{label}",
            lambda path=docx_path: _parse_observed(parser._parse_docx(path)),
            warmups=config.warmups, samples=config.samples,
            workload=fixture_metadata(docx, format="DOCX", paragraph_count=paragraphs),
        ))

    if config.profile == "baseline":
        near_file_limit = synthetic_pdf(1, padding_bytes=9 * 1024 * 1024)
        near_file_path = workspace / "near-10-mib.pdf"
        near_file_path.write_bytes(near_file_limit)
        cases.append(measure(
            "upload_document_validation_pdf_near_10_mib",
            lambda: _upload_validate_observed(storage, validator, near_file_limit, near_file_path.name),
            warmups=config.warmups, samples=config.samples,
            workload=fixture_metadata(near_file_limit, format="PDF", page_count=1, configured_max_bytes=settings.max_upload_bytes),
        ))

    cases.append(measure(
        "structured_draft_validation",
        lambda: {"top_level_fields": len(validate_canonical_draft(draft, schema))},
        warmups=config.warmups, samples=config.samples,
        workload={"schema_version": draft["schema_version"], "input_size_bytes": len(json.dumps(draft, sort_keys=True).encode())},
    ))

    render_path = settings.local_export_root / "benchmark.docx"
    cases.append(measure(
        "docx_render_export",
        lambda: _render_observed(renderer, draft, render_path),
        warmups=config.warmups, samples=config.samples,
        workload={"template": "patent-template-v1", "draft_sections": len(draft["draft_sections"])},
    ))

    representative = fixtures["medium" if "medium" in fixtures else "ci"]
    cases.append(measure(
        "representative_offline_backend_e2e",
        lambda: _offline_e2e_observed(validator, parser, renderer, schema, draft, representative[0], settings.local_export_root / "e2e.docx"),
        warmups=config.warmups, samples=config.samples,
        workload=fixture_metadata(representative[2], format="PDF", page_count=representative[4], stages=4),
    ))
    return cases


def _parse_observed(units: list[Any]) -> dict[str, Any]:
    return {"source_unit_count": len(units), "parsed_character_count": sum(len(unit.content) for unit in units)}


def _upload_validate_observed(
    storage: DocumentStorage,
    validator: DocumentValidator,
    payload: bytes,
    filename: str,
) -> dict[str, Any]:
    document_id = storage.allocate_id()
    path, size_bytes = asyncio.run(storage.stream_to_disk(_SyntheticUpload(payload), document_id))
    try:
        result = validator.validate(path, filename=filename, declared_mime=PDF_MEDIA_TYPE)
        return {"stored_size_bytes": size_bytes, "page_count": result.page_count}
    finally:
        storage.delete(document_id)


def _render_observed(renderer: PatentDocxRenderer, draft: dict[str, Any], output: Path) -> dict[str, Any]:
    rendered = renderer.render(draft, output)
    return {"output_size_bytes": rendered.stat().st_size}


def _offline_e2e_observed(
    validator: DocumentValidator,
    parser: DocumentPreparationService,
    renderer: PatentDocxRenderer,
    schema: dict[str, Any],
    draft: dict[str, Any],
    pdf_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    validation = validator.validate(pdf_path, filename=pdf_path.name, declared_mime=PDF_MEDIA_TYPE)
    units = parser._parse_pdf(pdf_path)
    validate_canonical_draft(draft, schema)
    rendered = renderer.render(draft, output_path)
    return {
        "page_count": validation.page_count,
        "source_unit_count": len(units),
        "parsed_character_count": sum(len(unit.content) for unit in units),
        "output_size_bytes": rendered.stat().st_size,
    }


def run_browser_benchmark(config: BenchmarkConfig, result_path: Path) -> dict[str, Any]:
    """Run the synthetic local HTTP/browser workflow with outbound access blocked."""

    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm is required for the browser benchmark")
    env = os.environ.copy()
    env.update({
        "RUN_OPENAI_LIVE_TESTS": "0",
        "RUN_OPENAI_DRAFT_LIVE_TESTS": "0",
        "P1_005_BROWSER_RESULT": str(result_path),
        "P1_005_BROWSER_WARMUPS": str(config.warmups),
        "P1_005_BROWSER_SAMPLES": str(config.samples),
        "PLAYWRIGHT_PYTHON": sys.executable,
    })
    env.pop("OPENAI_API_KEY", None)
    env["P1_005_EXTERNAL_SERVERS"] = "1"
    completed = _run_browser_processes(npm, env)
    if completed.returncode:
        raise RuntimeError(f"browser benchmark failed with exit code {completed.returncode}")
    data = json.loads(result_path.read_text(encoding="utf-8"))
    return {
        "name": "local_browser_workflow",
        "status": "MEASURED",
        "workload": data["workload"],
        "observed": data["observed"],
        "timing": calculate_statistics(data["samples_ms"]),
    }


def _run_browser_processes(
    npm: str,
    env: Mapping[str, str],
    script: str = "test:e2e:performance",
) -> subprocess.CompletedProcess[str]:
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("node is required for the browser benchmark")
    creation: dict[str, Any] = {}
    if os.name == "nt":
        creation["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
    else:
        creation["start_new_session"] = True
    processes: list[subprocess.Popen[Any]] = []
    try:
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "tests.e2e.offline_backend:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=ROOT, env=dict(env), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **creation,
        ))
        next_cli = ROOT / "frontend/node_modules/next/dist/bin/next"
        processes.append(subprocess.Popen(
            [node, str(next_cli), "start", "--hostname", "127.0.0.1", "--port", "3106"],
            cwd=ROOT / "frontend", env=dict(env), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **creation,
        ))
        _wait_for_http("http://127.0.0.1:8000/health", processes[0])
        _wait_for_http("http://127.0.0.1:3106", processes[1])
        return subprocess.run(
            [npm, "run", script], cwd=ROOT / "frontend", env=dict(env),
            check=False, text=True, timeout=180,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("browser benchmark exceeded 180 seconds") from exc
    finally:
        for process in reversed(processes):
            _terminate_process_tree(process)


def _wait_for_http(url: str, process: subprocess.Popen[Any], timeout: float = 120.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"benchmark server exited before readiness: {url}")
        try:
            with urllib.request.urlopen(url, timeout=1.0) as response:
                if response.status < 500:
                    return
        except (OSError, urllib.error.URLError):
            time.sleep(0.1)
    raise RuntimeError(f"benchmark server readiness timed out: {url}")


def _terminate_process_tree(process: subprocess.Popen[Any]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    else:
        import signal

        os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_benchmark(config: BenchmarkConfig) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ai-ip-p1-005-") as temporary:
        workspace = Path(temporary)
        cases = _backend_cases(config, workspace)
        if config.include_browser:
            cases.append(run_browser_benchmark(config, workspace / "browser.json"))
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "task_id": TASK_ID,
        "authorization": AUTHORIZATION,
        "generated_at": datetime.now(UTC).isoformat(),
        "environment": _environment(),
        "config": {
            "warmups": config.warmups,
            "samples": config.samples,
            "profile": config.profile,
            "include_browser": config.include_browser,
            "timing_thresholds_enforced": False,
        },
        "cases": cases,
    }
    validate_report(report)
    return report


def human_summary(report: Mapping[str, Any]) -> str:
    lines = ["P1-005 offline performance baseline", "case | median ms | p95 ms | samples"]
    for case in report["cases"]:
        timing = case["timing"]
        lines.append(f"{case['name']} | {timing['median_ms']:.3f} | {timing['p95_ms']:.3f} | {timing['sample_count']}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/p1-005-offline-baseline.json")
    parser.add_argument("--warmups", type=int, default=1)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--profile", choices=("ci", "baseline"), default="baseline")
    parser.add_argument("--skip-browser", action="store_true", help="Run backend stages only; not a complete baseline.")
    parser.add_argument("--thresholds", type=Path, help="Optional local absolute ceilings; never used by CI.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        config = BenchmarkConfig(args.warmups, args.samples, args.profile, not args.skip_browser)
        report = run_benchmark(config)
        if args.thresholds:
            evaluation = evaluate_thresholds(report, json.loads(args.thresholds.read_text(encoding="utf-8")))
            if evaluation["status"] != "PASS":
                print(json.dumps(evaluation, indent=2), file=sys.stderr)
                return 2
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(human_summary(report))
        print(f"JSON: {args.output}")
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"benchmark error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
