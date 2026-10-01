import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const repositoryRoot = path.resolve(__dirname, "..");
const backendPort = process.env.PLAYWRIGHT_BACKEND_PORT ?? "8000";
const frontendPort = process.env.PLAYWRIGHT_FRONTEND_PORT ?? "3106";
const python = process.env.PLAYWRIGHT_PYTHON ?? path.join(
  repositoryRoot,
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);

export default defineConfig({
  testDir: "./e2e",
  timeout: 60_000,
  expect: { timeout: 10_000 },
  workers: 1,
  reporter: "list",
  use: {
    baseURL: `http://127.0.0.1:${frontendPort}`,
    ...devices["Desktop Chrome"],
    acceptDownloads: true,
  },
  webServer: process.env.P1_005_EXTERNAL_SERVERS === "1" ? [] : [
    {
      command: `"${python}" -m uvicorn tests.e2e.offline_backend:app --host 127.0.0.1 --port ${backendPort}`,
      cwd: repositoryRoot,
      url: `http://127.0.0.1:${backendPort}/health`,
      reuseExistingServer: process.env.PLAYWRIGHT_REUSE_BACKEND === "1",
      timeout: 120_000,
    },
    {
      command: `node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port ${frontendPort}`,
      cwd: __dirname,
      url: `http://127.0.0.1:${frontendPort}`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
