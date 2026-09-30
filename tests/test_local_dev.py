from __future__ import annotations

import signal
import subprocess
from pathlib import Path

import pytest

from tools import local_dev


class FakeProcess:
    _next_pid = 4100

    def __init__(self, return_code: int | None = None, *, timeout_on_wait: bool = False):
        self.return_code = return_code
        self.timeout_on_wait = timeout_on_wait
        self.signals: list[int] = []
        self.pid = FakeProcess._next_pid
        FakeProcess._next_pid += 1

    def poll(self) -> int | None:
        return self.return_code

    def wait(self, timeout: float | None = None) -> int:
        if self.timeout_on_wait and self.return_code is None:
            raise subprocess.TimeoutExpired("fake", timeout)
        self.return_code = 0 if self.return_code is None else self.return_code
        return self.return_code

    def send_signal(self, value: int) -> None:
        self.signals.append(value)


def plan(tmp_path: Path, environment: dict[str, str] | None = None) -> local_dev.LaunchPlan:
    return local_dev.LaunchPlan(
        repository_root=tmp_path,
        npm_executable="npm.cmd",
        child_environment=environment or {},
    )


def test_occupied_backend_port_refuses_without_process_cleanup(monkeypatch, tmp_path):
    launcher = local_dev.LocalDevLauncher(plan(tmp_path))
    checked: list[int] = []

    def check(port: int) -> None:
        checked.append(port)
        if port == local_dev.BACKEND_PORT:
            raise local_dev.LauncherError("occupied")

    monkeypatch.setattr(local_dev, "ensure_port_available", check)
    with pytest.raises(local_dev.LauncherError, match="occupied"):
        launcher.check()
    assert checked == [local_dev.BACKEND_PORT]
    assert launcher.owned == []


def test_occupied_frontend_port_refuses_without_spawning(monkeypatch, tmp_path):
    launcher = local_dev.LocalDevLauncher(plan(tmp_path))
    checked: list[int] = []

    def check(port: int) -> None:
        checked.append(port)
        if port == local_dev.FRONTEND_PORT:
            raise local_dev.LauncherError("frontend occupied")

    monkeypatch.setattr(local_dev, "ensure_port_available", check)
    with pytest.raises(local_dev.LauncherError, match="frontend occupied"):
        launcher.check()
    assert checked == [local_dev.BACKEND_PORT, local_dev.FRONTEND_PORT]
    assert launcher.owned == []


def test_backend_child_exit_before_readiness_is_actionable(tmp_path):
    child = FakeProcess(return_code=7)
    launcher = local_dev.LocalDevLauncher(
        plan(tmp_path), process_factory=lambda *args, **kwargs: child
    )
    owner = launcher._spawn("backend", ["python"], tmp_path)
    with pytest.raises(local_dev.LauncherError, match="exit 7"):
        launcher._wait_ready("backend", "http://test", owner, require_health_body=True)


def test_backend_timeout_cleans_up_owned_process(tmp_path):
    child = FakeProcess(timeout_on_wait=False)
    times = iter([0.0, 0.0, 2.0])
    launcher = local_dev.LocalDevLauncher(
        plan(tmp_path),
        startup_timeout=1.0,
        process_factory=lambda *args, **kwargs: child,
        http_probe=lambda url: (_ for _ in ()).throw(OSError("not ready")),
        clock=lambda: next(times, 2.0),
        sleeper=lambda seconds: None,
        platform_name="nt",
    )
    with pytest.raises(local_dev.LauncherError, match="timed out"):
        launcher.start()
    launcher.shutdown()
    assert child.signals == [local_dev.CTRL_BREAK_EVENT]


@pytest.mark.parametrize(
    ("responses", "expected"),
    [
        ([(200, b'{"status":"ok"}'), (503, b"wait"), (503, b"wait")], "frontend"),
        (
            [(200, b'{"status":"ok"}'), (200, b"page"), (200, b'{"status":"bad"}')],
            "proxy",
        ),
    ],
)
def test_frontend_or_proxy_failure_cleans_up_both_processes(tmp_path, responses, expected):
    backend = FakeProcess()
    frontend = FakeProcess()
    children = iter([backend, frontend])
    replies = iter(responses)
    clock_values = iter([0.0, 0.0, 0.0, 0.0, 2.0, 10.0, 11.0, 12.0, 20.0])
    launcher = local_dev.LocalDevLauncher(
        plan(tmp_path),
        startup_timeout=1.0,
        process_factory=lambda *args, **kwargs: next(children),
        http_probe=lambda url: next(replies),
        clock=lambda: next(clock_values),
        sleeper=lambda seconds: None,
        platform_name="nt",
    )
    with pytest.raises(local_dev.LauncherError, match=expected):
        launcher.start()
    launcher.shutdown()
    assert backend.signals == [local_dev.CTRL_BREAK_EVENT]
    assert frontend.signals == [local_dev.CTRL_BREAK_EVENT]


def test_windows_shutdown_targets_only_owned_pids(tmp_path):
    first = FakeProcess(timeout_on_wait=True)
    second = FakeProcess(timeout_on_wait=True)
    commands: list[list[str]] = []
    launcher = local_dev.LocalDevLauncher(
        plan(tmp_path),
        command_runner=lambda command, **kwargs: commands.append(command),
        clock=lambda: 0.0,
        platform_name="nt",
    )
    launcher.owned = [
        local_dev.OwnedProcess("backend", first),
        local_dev.OwnedProcess("frontend", second),
    ]
    launcher.shutdown()
    assert first.signals == [local_dev.CTRL_BREAK_EVENT]
    assert second.signals == [local_dev.CTRL_BREAK_EVENT]
    assert commands == [
        ["taskkill", "/PID", str(second.pid), "/T", "/F"],
        ["taskkill", "/PID", str(first.pid), "/T", "/F"],
    ]


def test_posix_shutdown_uses_owned_process_groups(tmp_path):
    child = FakeProcess(timeout_on_wait=True)
    signals: list[tuple[int, int]] = []
    launcher = local_dev.LocalDevLauncher(
        plan(tmp_path),
        clock=lambda: 0.0,
        platform_name="posix",
        kill_process_group=lambda pid, sig: signals.append((pid, sig)),
    )
    launcher.owned = [local_dev.OwnedProcess("backend", child)]
    launcher.shutdown()
    assert signals == [
        (child.pid, signal.SIGINT),
        (child.pid, signal.SIGTERM),
        (child.pid, local_dev.SIGKILL),
    ]


def test_environment_is_offline_safe_and_does_not_require_api_key():
    environment = local_dev.child_environment({})
    assert "OPENAI_API_KEY" not in environment
    assert environment["AI_IP_ENABLE_LOCAL_ORCHESTRATION_API"] == "0"
    assert environment["RUN_OPENAI_LIVE_TESTS"] == "0"
    assert environment["RUN_OPENAI_DRAFT_LIVE_TESTS"] == "0"
    with pytest.raises(local_dev.LauncherError, match="must be 0"):
        local_dev.child_environment({"RUN_OPENAI_LIVE_TESTS": "1"})


def test_existing_supported_orchestration_flag_is_preserved():
    environment = local_dev.child_environment({"AI_IP_ENABLE_LOCAL_ORCHESTRATION_API": "1"})
    assert environment["AI_IP_ENABLE_LOCAL_ORCHESTRATION_API"] == "1"
    with pytest.raises(local_dev.LauncherError, match="must be 0 or 1"):
        local_dev.child_environment({"AI_IP_ENABLE_LOCAL_ORCHESTRATION_API": "yes"})


def test_commands_bind_both_servers_to_loopback(tmp_path):
    launch_plan = plan(tmp_path)
    assert launch_plan.backend_command[-4:] == [
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ]
    assert launch_plan.frontend_command[-4:] == [
        "--hostname",
        "127.0.0.1",
        "--port",
        "3000",
    ]


def test_missing_frontend_package_is_actionable(monkeypatch, tmp_path):
    monkeypatch.setattr(local_dev.sys, "version_info", (3, 12, 0))
    with pytest.raises(local_dev.LauncherError, match="frontend/package.json"):
        local_dev.validate_prerequisites(tmp_path, {})
