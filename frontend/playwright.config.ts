import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const repositoryRoot = path.resolve(__dirname, "..");
const python = path.join(
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
    baseURL: "http://127.0.0.1:3106",
    ...devices["Desktop Chrome"],
    acceptDownloads: true,
  },
  webServer: [
    {
      command: `"${python}" -m uvicorn tests.e2e.offline_backend:app --host 127.0.0.1 --port 8000`,
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: "node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port 3106",
      cwd: __dirname,
      url: "http://127.0.0.1:3106",
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
