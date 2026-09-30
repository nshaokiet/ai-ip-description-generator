"""Start the local FastAPI and Next.js development servers as one owned unit.

This launcher is intentionally stdlib-only.  It never calls a provider and it
does not enable the opt-in local orchestration API.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence


HOST = "127.0.0.1"
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
DEFAULT_STARTUP_TIMEOUT_SECONDS = 120.0
DEFAULT_SHUTDOWN_TIMEOUT_SECONDS = 8.0
HEALTH_BODY = {"status": "ok"}
LIVE_FLAGS = ("RUN_OPENAI_LIVE_TESTS", "RUN_OPENAI_DRAFT_LIVE_TESTS")
SIGKILL = getattr(signal, "SIGKILL", 9)
CTRL_BREAK_EVENT = getattr(signal, "CTRL_BREAK_EVENT", 1)
CREATE_NEW_PROCESS_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)


class LauncherError(RuntimeError):
    """A safe, actionable local-launch failure."""


@dataclass(frozen=True, slots=True)
class LaunchPlan:
    repository_root: Path
    npm_executable: str
    child_environment: dict[str, str]

    @property
    def backend_command(self) -> list[str]:
        return [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app.main:app",
            "--host",
            HOST,
            "--port",
            str(BACKEND_PORT),
        ]

    @property
    def frontend_command(self) -> list[str]:
        return [
            self.npm_executable,
            "run",
            "dev",
            "--",
            "--hostname",
            HOST,
            "--port",
            str(FRONTEND_PORT),
        ]


@dataclass(slots=True)
class OwnedProcess:
    name: str
    process: subprocess.Popen[bytes]


def _default_kill_process_group(process_group_id: int, signal_number: int) -> None:
    killpg = getattr(os, "killpg", None)
    if killpg is None:
        raise OSError("POSIX process-group signaling is unavailable")
    killpg(process_group_id, signal_number)


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if not (root / "backend" / "app" / "main.py").is_file() or not (
        root / "frontend" / "package.json"
    ).is_file():
        raise LauncherError(
            "repository layout is incomplete; run the committed tools/local_dev.py file"
        )
    return root


def _validated_flag(environment: Mapping[str, str], name: str, *, default: str) -> str:
    value = environment.get(name, default)
    if value not in {"0", "1"}:
        raise LauncherError(f"{name} must be 0 or 1")
    return value


def child_environment(environment: Mapping[str, str]) -> dict[str, str]:
    result = dict(environment)
    _validated_flag(result, "AI_IP_ENABLE_LOCAL_ORCHESTRATION_API", default="0")
    result.setdefault("AI_IP_ENABLE_LOCAL_ORCHESTRATION_API", "0")
    for name in LIVE_FLAGS:
        value = _validated_flag(result, name, default="0")
        if value != "0":
            raise LauncherError(f"{name} must be 0 for the local launcher")
        result[name] = "0"
    result["BACKEND_URL"] = f"http://{HOST}:{BACKEND_PORT}"
    return result


def _npm_executable() -> str:
    names = ("npm.cmd", "npm") if os.name == "nt" else ("npm",)
    for name in names:
        executable = shutil.which(name)
        if executable:
            return executable
    raise LauncherError("npm is unavailable; install Node.js/npm and ensure npm is on PATH")


def validate_prerequisites(
    root: Path, environment: Mapping[str, str] | None = None
) -> LaunchPlan:
    if sys.version_info[:2] != (3, 12):
        raise LauncherError(
            f"Python 3.12 is required; current interpreter is {sys.version_info.major}."
            f"{sys.version_info.minor} at {sys.executable}"
        )
    for module in ("uvicorn", "fastapi"):
        if importlib.util.find_spec(module) is None:
            raise LauncherError(
                f"backend dependency '{module}' is unavailable; install backend/requirements.txt"
            )
    frontend = root / "frontend"
    if not (frontend / "package.json").is_file():
        raise LauncherError("frontend/package.json is missing")
    if not (frontend / "node_modules" / "next").is_dir():
        raise LauncherError("frontend dependencies are missing; run 'npm ci' in frontend/")
    return LaunchPlan(
        repository_root=root,
        npm_executable=_npm_executable(),
        child_environment=child_environment(environment or os.environ),
    )


def ensure_port_available(port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            listener.bind((HOST, port))
    except OSError as exc:
        raise LauncherError(
            f"required port {HOST}:{port} is unavailable; stop its existing owner or choose another session"
        ) from exc


def probe_http(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "ai-ip-local-dev/1"})
    with urllib.request.urlopen(request, timeout=2.0) as response:
        return response.status, response.read()


class LocalDevLauncher:
    def __init__(
        self,
        plan: LaunchPlan,
        *,
        startup_timeout: float = DEFAULT_STARTUP_TIMEOUT_SECONDS,
        shutdown_timeout: float = DEFAULT_SHUTDOWN_TIMEOUT_SECONDS,
        process_factory: Callable[..., subprocess.Popen[bytes]] = subprocess.Popen,
        command_runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run,
        http_probe: Callable[[str], tuple[int, bytes]] = probe_http,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
        platform_name: str = os.name,
        kill_process_group: Callable[[int, int], None] | None = None,
    ) -> None:
        self.plan = plan
        self.startup_timeout = startup_timeout
        self.shutdown_timeout = shutdown_timeout
        self.process_factory = process_factory
        self.command_runner = command_runner
        self.http_probe = http_probe
        self.clock = clock
        self.sleeper = sleeper
        self.platform_name = platform_name
        self.kill_process_group = kill_process_group or _default_kill_process_group
        self.owned: list[OwnedProcess] = []

    def check(self) -> None:
        ensure_port_available(BACKEND_PORT)
        ensure_port_available(FRONTEND_PORT)

    def _spawn(self, name: str, command: Sequence[str], cwd: Path) -> OwnedProcess:
        options: dict[str, object] = {
            "cwd": cwd,
            "env": self.plan.child_environment,
        }
        if self.platform_name == "nt":
            options["creationflags"] = CREATE_NEW_PROCESS_GROUP
        else:
            options["start_new_session"] = True
        try:
            process = self.process_factory(list(command), **options)
        except OSError as exc:
            raise LauncherError(f"could not start {name}: {exc}") from exc
        owned = OwnedProcess(name=name, process=process)
        self.owned.append(owned)
        return owned

    def _wait_ready(
        self,
        name: str,
        url: str,
        owner: OwnedProcess,
        *,
        require_health_body: bool,
    ) -> None:
        deadline = self.clock() + self.startup_timeout
        last_problem = "no response"
        while self.clock() < deadline:
            return_code = owner.process.poll()
            if return_code is not None:
                raise LauncherError(f"{owner.name} exited before {name} readiness (exit {return_code})")
            try:
                status, body = self.http_probe(url)
                if 200 <= status < 300:
                    if not require_health_body:
                        return
                    try:
                        payload = json.loads(body)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        last_problem = "response was not valid JSON"
                    else:
                        if payload == HEALTH_BODY:
                            return
                        last_problem = "health response did not match {'status': 'ok'}"
                else:
                    last_problem = f"HTTP {status}"
            except (OSError, urllib.error.URLError) as exc:
                last_problem = str(exc)
            self.sleeper(0.2)
        raise LauncherError(f"{name} readiness timed out at {url}: {last_problem}")

    def start(self) -> None:
        print("[start] backend", flush=True)
        backend = self._spawn(
            "backend", self.plan.backend_command, self.plan.repository_root
        )
        backend_url = f"http://{HOST}:{BACKEND_PORT}/health"
        self._wait_ready("backend", backend_url, backend, require_health_body=True)
        print(f"[ready] backend {backend_url}", flush=True)

        print("[start] frontend", flush=True)
        frontend = self._spawn(
            "frontend", self.plan.frontend_command, self.plan.repository_root / "frontend"
        )
        frontend_url = f"http://{HOST}:{FRONTEND_PORT}"
        self._wait_ready("frontend", frontend_url, frontend, require_health_body=False)
        print(f"[ready] frontend {frontend_url}", flush=True)
        proxy_url = f"{frontend_url}/backend/health"
        self._wait_ready("proxy", proxy_url, frontend, require_health_body=True)
        print("[ready] proxy /backend/health", flush=True)
        print("[run] local application ready; press Ctrl+C to stop", flush=True)

    def supervise(self) -> None:
        while True:
            for owned in self.owned:
                return_code = owned.process.poll()
                if return_code is not None:
                    raise LauncherError(
                        f"{owned.name} exited unexpectedly (exit {return_code})"
                    )
            self.sleeper(0.5)

    def _wait_for_exit(self, owned: OwnedProcess, deadline: float) -> bool:
        remaining = max(0.0, deadline - self.clock())
        try:
            owned.process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            return False
        return True

    def shutdown(self) -> None:
        live = [owned for owned in reversed(self.owned) if owned.process.poll() is None]
        if not live:
            return
        print("[stop] shutting down owned processes", flush=True)
        for owned in live:
            try:
                if self.platform_name == "nt":
                    owned.process.send_signal(CTRL_BREAK_EVENT)
                else:
                    self.kill_process_group(owned.process.pid, signal.SIGINT)
            except (OSError, ProcessLookupError):
                pass

        deadline = self.clock() + self.shutdown_timeout
        remaining: list[OwnedProcess] = []
        for owned in live:
            if not self._wait_for_exit(owned, deadline):
                remaining.append(owned)

        if self.platform_name == "nt":
            for owned in remaining:
                if owned.process.poll() is None:
                    self.command_runner(
                        ["taskkill", "/PID", str(owned.process.pid), "/T", "/F"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False,
                    )
        else:
            for owned in remaining:
                if owned.process.poll() is None:
                    try:
                        self.kill_process_group(owned.process.pid, signal.SIGTERM)
                    except (OSError, ProcessLookupError):
                        pass
            final_deadline = self.clock() + 2.0
            for owned in remaining:
                if owned.process.poll() is None and not self._wait_for_exit(
                    owned, final_deadline
                ):
                    try:
                        self.kill_process_group(owned.process.pid, SIGKILL)
                    except (OSError, ProcessLookupError):
                        pass


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local backend and frontend")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate prerequisites and ports without starting servers",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=DEFAULT_STARTUP_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help="bounded readiness timeout for each check (default: 120)",
    )
    return parser


def _interrupt_handler(_signal_number: int, _frame: object) -> None:
    raise KeyboardInterrupt


def _install_termination_handlers() -> None:
    signal.signal(signal.SIGTERM, _interrupt_handler)
    windows_break = getattr(signal, "SIGBREAK", None)
    if windows_break is not None:
        signal.signal(windows_break, _interrupt_handler)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.startup_timeout <= 0:
        print("[error] --startup-timeout must be greater than zero", file=sys.stderr)
        return 2
    launcher: LocalDevLauncher | None = None
    try:
        _install_termination_handlers()
        print("[check] prerequisites", flush=True)
        plan = validate_prerequisites(repository_root())
        launcher = LocalDevLauncher(plan, startup_timeout=arguments.startup_timeout)
        launcher.check()
        if arguments.check:
            print("[check] prerequisites and ports ready", flush=True)
            return 0
        launcher.start()
        launcher.supervise()
    except KeyboardInterrupt:
        return 0
    except LauncherError as exc:
        print(f"[error] {exc}", file=sys.stderr, flush=True)
        return 1
    finally:
        if launcher is not None:
            launcher.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
