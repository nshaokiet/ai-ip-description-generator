import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const repositoryRoot = path.resolve(__dirname, "..");
const backendPort = process.env.PLAYWRIGHT_DEMO_BACKEND_PORT ?? "8001";
const frontendPort = process.env.PLAYWRIGHT_DEMO_FRONTEND_PORT ?? "3107";
const python = process.env.PLAYWRIGHT_PYTHON ?? path.join(
  repositoryRoot,
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);

export default defineConfig({
  testDir: "./e2e-demo",
  timeout: 60_000,
  expect: { timeout: 10_000 },
  workers: 1,
  reporter: "list",
  use: {
    baseURL: `http://127.0.0.1:${frontendPort}`,
    ...devices["Desktop Chrome"],
    acceptDownloads: true,
  },
  webServer: process.env.DEPLOY_001_EXTERNAL_SERVERS === "1" ? [] : [
    {
      command: `"${python}" -m uvicorn backend.app.demo_staging:app --host 127.0.0.1 --port ${backendPort}`,
      cwd: repositoryRoot,
      url: `http://127.0.0.1:${backendPort}/health`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: `node e2e-demo/static-proxy-server.mjs ${frontendPort} ${backendPort}`,
      cwd: __dirname,
      url: `http://127.0.0.1:${frontendPort}`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
