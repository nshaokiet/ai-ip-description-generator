"""Executable synthetic reconstruction cases using a small JSON Patch subset."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


def resolve_pointer(document: Any, pointer: str) -> Any:
    current = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def apply_patches(document: Any, patches: list[dict]) -> None:
    for patch in patches:
        parent_path, _, key = patch["path"].rpartition("/")
        parent = resolve_pointer(document, parent_path) if parent_path else document
        value = copy.deepcopy(resolve_pointer(document, patch["from"])) if patch["op"] == "copy" else copy.deepcopy(patch.get("value"))
        if isinstance(parent, list):
            index = len(parent) if key == "-" else int(key)
            if patch["op"] in {"add", "copy"}:
                parent.insert(index, value)
            elif patch["op"] == "remove":
                parent.pop(index)
            elif patch["op"] == "replace":
                parent[index] = value
            else:
                raise ValueError("Unsupported fixture patch operation")
        elif patch["op"] == "remove":
            del parent[key]
        elif patch["op"] in {"add", "copy", "replace"}:
            parent[key] = value
        else:
            raise ValueError("Unsupported fixture patch operation")


def load_case(path: Path) -> tuple[dict, dict]:
    metadata = json.loads(path.read_text(encoding="utf-8"))
    if "extends" in metadata:
        base_path = path.parent / metadata["extends"]
        if base_path.name != "representative-system.json":
            raise ValueError("Fixture inheritance must use the synthetic representative")
        fixture = json.loads(base_path.read_text(encoding="utf-8"))
    else:
        fixture = copy.deepcopy(metadata)
    apply_patches(fixture, metadata.get("input_patches", []))
    return fixture, metadata
