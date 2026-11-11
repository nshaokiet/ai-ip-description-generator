import { test, expect, type BrowserContext, type Browser } from "@playwright/test";
import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import https from "node:https";
import http from "node:http";

const repo = path.resolve(__dirname, "../..");
const python = process.env.PLAYWRIGHT_PYTHON ?? path.join(repo, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
const origin = "https://localhost:3443";
const endpoint = "/api/product-web/v1/session";
let root: string;
let host: ChildProcess;
let configPath: string;
let config: { proxy: string; port: number; control_key: string };
let unexpectedBrowserEgress = 0;
let hostLogs = "";
let hostLogOverflow = false;

function control(action: string, selector?: string) {
  return spawnSync(python, ["-m", "backend.app.services.product_web_host_control", action,
    configPath, ...(selector ? [selector] : [])], {
    cwd: repo, encoding: "utf8", windowsHide: true,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
}

function wire(tls: boolean, requestPath: string, headers: string[] | Record<string, string> = {}, method = "GET") {
  return new Promise<{ status: number; body: string }>((resolve, reject) => {
    const options = { hostname: "127.0.0.1", port: tls ? 3443 : config.port,
      path: requestPath, headers, method, rejectUnauthorized: false, servername: "localhost" };
    const request = (tls ? https : http).request(options, (response) => {
      let body = "";
      response.on("data", (chunk) => { body += chunk; });
      response.on("end", () => resolve({ status: response.statusCode ?? 0, body }));
    });
    request.setTimeout(2000, () => request.destroy(new Error("local deadline")));
    request.on("error", reject);
    request.end(method === "GET" ? undefined : "{}");
  });
}

async function context(browser: Browser) {
  const value = await browser.newContext({ baseURL: origin, ignoreHTTPSErrors: true });
  // Certificate exception and network allowance belong only to this pinned test origin.
  await value.route("**/*", (route) => {
    if (new URL(route.request().url()).origin === origin) return route.continue();
    unexpectedBrowserEgress += 1;
    return route.abort();
  });
  return value;
}

async function pair(value: BrowserContext) {
  const page = await value.newPage();
  await page.goto("/product-web");
  await expect(page.getByRole("status")).toHaveText("anonymous");
  await page.getByRole("button", { name: "Request pairing" }).click();
  await expect(page.getByRole("status")).toHaveText("pending");
  const selector = await page.locator("#selector").innerText();
  expect(control("approve", selector).status).toBe(0);
  await expect(page.getByRole("status")).toHaveText("pending");
  await page.getByRole("button", { name: "Complete login" }).click();
  await expect(page.getByRole("status")).toHaveText("authenticated");
  expect(control("approve", selector).status).toBe(1);
  return page;
}

async function startHost(reuse = false) {
  host = spawn(python, ["tests/e2e/product_web_host.py", "--root", root, ...(reuse ? ["--reuse"] : [])], {
    cwd: repo, windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1", PYTHONUNBUFFERED: "1" },
  });
  for (const output of [host.stdout, host.stderr]) {
    output?.on("data", (part) => {
      hostLogs += part.toString();
      if (hostLogs.length > 65536) { hostLogOverflow = true; hostLogs = hostLogs.slice(-65536); }
    });
  }
  const deadline = Date.now() + 90_000;
  let ready = false;
  while (Date.now() < deadline && host.exitCode === null) {
    try {
      ready = (await wire(true, "/product-web", { Host: "localhost:3443" })).status === 200;
      if (ready) break;
    } catch { /* Start-up is bounded; no raw exceptions or private paths printed. */ }
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  expect(ready, "real local TLS host must become available").toBe(true);
  const state = path.join(root, "state");
  const directory = fs.readdirSync(state).filter((name) => name.startsWith("s1-"));
  expect(directory).toHaveLength(1);
  configPath = path.join(state, directory[0], "host.json");
  config = { ...JSON.parse(fs.readFileSync(configPath, "utf8")),
    ...JSON.parse(fs.readFileSync(path.join(state, directory[0], "proxy.json"), "utf8")) };
}

test.beforeAll(async () => {
  test.setTimeout(120_000);
  root = fs.mkdtempSync(path.join(os.tmpdir(), "aiip-s1-browser-"));
  await startHost();
});

test.afterAll(async () => {
  if (configPath && host?.exitCode === null) expect(control("shutdown").status).toBe(0);
  if (host) {
    await expect.poll(() => host.exitCode, { timeout: 15_000 }).not.toBeNull();
    expect(host.exitCode).toBe(0);
  }
  expect(unexpectedBrowserEgress).toBe(0);
  expect(hostLogOverflow).toBe(false);
  if (config) expect(hostLogs.includes(config.proxy) || hostLogs.includes(config.control_key)).toBe(false);
  if (root) {
    expect(fs.existsSync(path.join(root, "provider.json"))).toBe(true);
    const counts = JSON.parse(fs.readFileSync(path.join(root, "provider.json"), "utf8"));
    expect(counts.unexpected_provider_client_attempts).toBe(0);
    expect(counts.provider_api_requests).toBe(0);
    expect(counts.unexpected_egress_attempts).toBe(0);
    expect(fs.readdirSync(path.join(root, "state"))).toEqual([]);
    const evidence = { platform: process.platform, ...counts, unexpected_browser_egress: unexpectedBrowserEgress,
      owned_state_cleanup: true, private_values_absent_from_logs: true };
    const output = path.join(repo, "frontend/test-results");
    fs.mkdirSync(output, { recursive: true });
    fs.writeFileSync(path.join(output, "product-web-security.json"), JSON.stringify(evidence));
    console.log("S1_SECURITY_EVIDENCE", JSON.stringify(evidence));
    const resolved = path.resolve(root);
    expect(path.dirname(resolved)).toBe(path.resolve(os.tmpdir()));
    expect(path.basename(resolved).startsWith("aiip-s1-browser-")).toBe(true);
    fs.rmSync(resolved, { recursive: true });
  }
});

test("real HTTPS and OS pairing establish independent browser sessions and logout", async ({ browser }) => {
  test.setTimeout(90_000);
  const first = await context(browser);
  const second = await context(browser);
  try {
    const a = await pair(first);
    const b = await pair(second);
    const firstCookie = (await first.cookies()).find((cookie) => cookie.name === "__Host-aiip_web");
    const secondCookie = (await second.cookies()).find((cookie) => cookie.name === "__Host-aiip_web");
    expect(firstCookie?.value).not.toBe(secondCookie?.value);
    expect(firstCookie).toMatchObject({ secure: true, httpOnly: true, sameSite: "Strict", path: "/" });
    const headers = { Origin: origin, "Sec-Fetch-Site": "same-origin" };
    const secondStatus = await second.request.get(endpoint, { headers });
    const secondCsrf = (await secondStatus.json()).csrf;
    for (const csrf of [undefined, secondCsrf]) {
      const denied = await first.request.delete(endpoint, { data: {}, headers: {
        ...headers, ...(csrf ? { "X-AIIP-CSRF": csrf } : {}),
      } });
      expect(denied.status()).toBe(403);
    }
    for (const page of [a, b]) {
      expect(await page.evaluate(() => localStorage.length + sessionStorage.length)).toBe(0);
      const text = await page.content();
      expect(text.includes(config.proxy) || text.includes(config.control_key)).toBe(false);
    }
    const bundled = path.join(repo, "frontend/.next/static");
    for (const entry of fs.readdirSync(bundled, { recursive: true, withFileTypes: true })) {
      if (!entry.isFile()) continue;
      const contents = fs.readFileSync(path.join(entry.parentPath, entry.name));
      expect(contents.includes(Buffer.from(config.proxy)) || contents.includes(Buffer.from(config.control_key))).toBe(false);
    }
    await a.getByRole("button", { name: "Log out" }).click();
    await expect(a.getByRole("status")).toHaveText("anonymous");
    await b.reload();
    await expect(b.getByRole("status")).toHaveText("authenticated");
    expect(control("revoke-all").status).toBe(0);
    await b.reload();
    await expect(b.getByRole("status")).toHaveText("anonymous");
  } finally {
    await first.close();
    await second.close();
  }
});

test("private proxy rejects origins, spoofing and direct backend access", async () => {
  const valid = { Host: "localhost:3443", Origin: origin, "Sec-Fetch-Site": "same-origin", "Content-Type": "application/json", "X-AIIP-Bootstrap": "1" };
  for (const headers of [
    { ...valid, Origin: "null" }, { ...valid, Origin: "https://foreign.invalid" },
    { ...valid, Origin: "" }, { ...valid, Host: "foreign.invalid:3443" },
    { ...valid, "Sec-Fetch-Site": "cross-site" }, { ...valid, Forwarded: "host=localhost" },
    { ...valid, "X-Forwarded-Host": "localhost" }, { ...valid, "X-AIIP-Proxy": "forged" },
    { ...valid, "X-Internal-Control": "approve" },
  ]) expect((await wire(true, endpoint + "/bootstrap", headers, "POST")).status).toBe(403);
  const missing = { ...valid } as Partial<typeof valid>;
  delete missing.Origin;
  expect((await wire(true, endpoint + "/bootstrap", missing as Record<string, string>, "POST")).status).toBe(403);
  const duplicate = Object.entries(valid).flat();
  duplicate.push("Origin", origin);
  expect((await wire(true, endpoint + "/bootstrap", duplicate, "POST")).status).toBe(403);
  expect((await wire(false, endpoint, { Host: `127.0.0.1:${config.port}`, "Sec-Fetch-Site": "same-origin" })).status).toBe(403);
  for (const suffix of ["/documents", "/process", "/review", "/render", "/download"]) {
    expect((await wire(true, suffix, { Host: "localhost:3443" })).status).toBe(404);
  }
});

test("a real host restart invalidates the previous browser credential", async ({ browser }) => {
  test.setTimeout(120_000);
  const value = await context(browser);
  try {
    const page = await pair(value);
    const cookie = (await value.cookies()).find((item) => item.name === "__Host-aiip_web")?.value;
    const previousProxy = config.proxy;
    expect(control("shutdown").status).toBe(0);
    await expect.poll(() => host.exitCode, { timeout: 15_000 }).toBe(0);
    expect(fs.readdirSync(path.join(root, "state"))).toEqual([]);
    const previousCounts = JSON.parse(fs.readFileSync(path.join(root, "provider.json"), "utf8"));
    expect(previousCounts.unexpected_provider_client_attempts + previousCounts.provider_api_requests + previousCounts.unexpected_egress_attempts).toBe(0);
    expect(hostLogs.includes(config.proxy) || hostLogs.includes(config.control_key)).toBe(false);
    await startHost(true);
    expect(config.proxy).not.toBe(previousProxy);
    await page.reload();
    await expect(page.getByRole("status")).toHaveText("anonymous");
    expect((await value.cookies()).find((item) => item.name === "__Host-aiip_web")?.value).toBe(cookie);
  } finally {
    await value.close();
  }
});
