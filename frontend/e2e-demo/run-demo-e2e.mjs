import { spawn } from "node:child_process";
import { join, resolve } from "node:path";

const frontendRoot = resolve(import.meta.dirname, "..");
const repositoryRoot = resolve(frontendRoot, "..");
const backendPort = process.env.PLAYWRIGHT_DEMO_BACKEND_PORT ?? "8001";
const frontendPort = process.env.PLAYWRIGHT_DEMO_FRONTEND_PORT ?? "3107";
const python = process.env.PLAYWRIGHT_PYTHON ?? join(
  repositoryRoot,
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);

const children = [];

function start(command, args, cwd, env = process.env) {
  const child = spawn(command, args, {
    cwd,
    env,
    stdio: "inherit",
    windowsHide: true,
  });
  children.push(child);
  return child;
}

async function waitFor(url, child) {
  const deadline = Date.now() + 120_000;
  while (Date.now() < deadline) {
    if (child.exitCode !== null) {
      throw new Error(`Server exited before becoming ready: ${url}`);
    }
    try {
      const response = await fetch(url);
      if (response.ok) return;
    } catch {
      // The server is still starting.
    }
    await new Promise((resolveDelay) => setTimeout(resolveDelay, 250));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

async function stop(child) {
  if (child.exitCode !== null) return;
  child.kill("SIGTERM");
  await Promise.race([
    new Promise((resolveExit) => child.once("exit", resolveExit)),
    new Promise((resolveTimeout) => setTimeout(resolveTimeout, 3_000)),
  ]);
  if (child.exitCode === null) child.kill("SIGKILL");
}

let exitCode = 1;
try {
  const backend = start(
    python,
    [
      "-m",
      "uvicorn",
      "backend.app.demo_staging:app",
      "--host",
      "127.0.0.1",
      "--port",
      backendPort,
    ],
    repositoryRoot,
  );
  const frontend = start(
    process.execPath,
    [join("e2e-demo", "static-proxy-server.mjs"), frontendPort, backendPort],
    frontendRoot,
  );

  await Promise.all([
    waitFor(`http://127.0.0.1:${backendPort}/health`, backend),
    waitFor(`http://127.0.0.1:${frontendPort}`, frontend),
  ]);

  const playwright = start(
    process.execPath,
    [
      join("node_modules", "@playwright", "test", "cli.js"),
      "test",
      "--config=playwright.demo.config.ts",
    ],
    frontendRoot,
    { ...process.env, DEPLOY_001_EXTERNAL_SERVERS: "1" },
  );
  exitCode = await new Promise((resolveExit) => {
    playwright.once("exit", (code) => resolveExit(code ?? 1));
  });
} finally {
  await Promise.all(children.reverse().map(stop));
}

process.exitCode = exitCode;
