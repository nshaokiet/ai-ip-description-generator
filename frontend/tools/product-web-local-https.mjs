// Opt-in Next custom-server transport. The released Next routes are not mounted.
import https from "node:https";
import http from "node:http";
import { readFileSync } from "node:fs";
import { X509Certificate, createPrivateKey, randomBytes } from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const frontend = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const origin = "https://localhost:3443";
const prefix = "/api/product-web/v1";
const safeHeaders = {
  "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
};

function requireSecurity(value) {
  if (!value) throw new Error("Local security prerequisite unavailable");
}

function privateFiles(paths) {
  const result = spawnSync(process.env.AIIP_S1_PYTHON, [
    "-m", "backend.app.services.product_web_host_control", "check-private", ...paths,
  ], { cwd: path.dirname(frontend), stdio: "ignore", windowsHide: true });
  requireSecurity(result.status === 0);
}

function tlsMaterial() {
  const certificate = process.env.AIIP_S1_CERT;
  const privateKey = process.env.AIIP_S1_KEY;
  requireSecurity(certificate && privateKey && process.env.AIIP_S1_PYTHON);
  privateFiles([certificate, privateKey]);
  const cert = readFileSync(certificate);
  const key = readFileSync(privateKey);
  const parsed = new X509Certificate(cert);
  const now = Date.now();
  requireSecurity(parsed.subjectAltName?.split(", ").includes("DNS:localhost"));
  requireSecurity(parsed.checkHost("localhost", { subject: "never", wildcards: false }) === "localhost");
  requireSecurity(now >= Date.parse(parsed.validFrom) && now < Date.parse(parsed.validTo));
  requireSecurity(parsed.checkPrivateKey(createPrivateKey(key)));
  return { cert, key, minVersion: "TLSv1.2" };
}

function guard(request, mutation = false, sourceUpload = false) {
  const seen = new Set();
  requireSecurity(request.rawHeaders.length <= 128);
  for (let index = 0; index < request.rawHeaders.length; index += 2) {
    const name = request.rawHeaders[index].toLowerCase();
    requireSecurity(!seen.has(name));
    seen.add(name);
    requireSecurity(name !== "forwarded" && name !== "authorization" &&
      !name.startsWith("x-forwarded-") && !name.startsWith("x-internal-") &&
      name !== "x-aiip-proxy");
  }
  requireSecurity(request.headers.host === "localhost:3443");
  requireSecurity(["127.0.0.1", "::ffff:127.0.0.1"].includes(request.socket.remoteAddress));
  const suppliedOrigin = request.headers.origin;
  requireSecurity(suppliedOrigin === undefined || suppliedOrigin === origin);
  if (mutation) {
    requireSecurity(suppliedOrigin === origin && request.headers["sec-fetch-site"] === "same-origin");
    if (!sourceUpload) requireSecurity(request.headers["content-type"] === "application/json");
  }
}

function respond(response, status, value) {
  response.writeHead(status, { ...safeHeaders, "Content-Type": "application/json" });
  response.end(JSON.stringify(value));
}

async function proxy(request, response, host) {
  const route = syntheticRoute(request.url, request.method, host.synthetic === true);
  const methods = route ? [request.method] : request.url === `${prefix}/session/bootstrap` ? ["POST"] : ["GET", "POST", "DELETE"];
  requireSecurity(methods.includes(request.method));
  guard(request, request.method !== "GET", route?.upload);
  requireSecurity(request.headers["sec-fetch-site"] === "same-origin");
  requireSecurity(request.headers["transfer-encoding"] === undefined && request.headers["content-encoding"] === undefined);
  const requestLimit = route ? 2048 : 4096;
  const declared = request.headers["content-length"];
  requireSecurity(declared === undefined || (/^(0|[1-9][0-9]*)$/.test(declared) && Number(declared) <= requestLimit));
  if (route && request.method !== "GET") requireSecurity(declared !== undefined);
  if (route?.upload) requireSecurity(["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(request.headers["content-type"]));
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    requireSecurity(size <= requestLimit);
    chunks.push(chunk);
  }
  const headers = { "x-aiip-proxy": host.proxy };
  requireSecurity(declared === undefined || Number(declared) === size);
  if (route && request.method === "GET") requireSecurity(size === 0);
  for (const name of ["cookie", "origin", "content-type", "x-aiip-csrf", "x-aiip-bootstrap", "sec-fetch-site", ...(route?.upload ? ["x-aiip-filename"] : [])]) {
    if (request.headers[name] !== undefined) headers[name] = request.headers[name];
  }
  headers["content-length"] = String(size);
  await new Promise((resolve, reject) => {
    const upstream = http.request({
      hostname: "127.0.0.1", port: host.port, path: request.url, method: request.method,
      headers, timeout: route ? 125000 : 5000, agent: false,
    }, (incoming) => {
      let bytes = 0;
      const parts = [];
      incoming.on("data", (part) => {
        bytes += part.length;
        if (bytes > (route?.responseLimit ?? 8192)) incoming.destroy(new Error("response limit"));
        else parts.push(part);
      });
      incoming.on("error", reject);
      incoming.on("end", () => {
        if (response.destroyed) return resolve();
        const mediaType = incoming.headers["content-type"];
        const success = incoming.statusCode >= 200 && incoming.statusCode < 300;
        const expected = route?.binary && success ? route.mediaType : "application/json";
        if (mediaType !== expected) return reject(new Error("response type"));
        if (incoming.headers["content-length"] !== String(bytes)) return reject(new Error("response framing"));
        const outputHeaders = { ...safeHeaders, "Content-Type": "application/json" };
        outputHeaders["Content-Type"] = expected;
        outputHeaders["Content-Length"] = String(bytes);
        if (route?.binary && success) outputHeaders["Content-Disposition"] = `attachment; filename="${route.filename}"`;
        if (incoming.headers["set-cookie"]) outputHeaders["Set-Cookie"] = incoming.headers["set-cookie"];
        response.writeHead(incoming.statusCode ?? 503, outputHeaders);
        response.end(Buffer.concat(parts));
        resolve();
      });
    });
    upstream.on("timeout", () => upstream.destroy(new Error("deadline")));
    upstream.on("error", reject);
    response.once("close", () => upstream.destroy());
    upstream.end(Buffer.concat(chunks));
  });
}

function syntheticRoute(url, method, enabled) {
  if (!enabled) return null;
  const base = `${prefix}/documents`;
  if (url === base && method === "POST") return { upload: true, responseLimit: 8192 };
  const selector = "[0-9a-f]{32}";
  if (new RegExp(`^${base}/${selector}$`).test(url) && method === "DELETE") return { responseLimit: 8192 };
  if (new RegExp(`^${base}/${selector}/review$`).test(url) && method === "GET") return { responseLimit: 8 * 1024 * 1024 };
  if (new RegExp(`^${base}/${selector}/(ack-content|ack-claims|render)$`).test(url) && method === "POST") return { responseLimit: 8192 };
  const artifact = new RegExp(`^${base}/${selector}/revisions/[1-9][0-9]{0,8}/artifacts/(B2_REFERENCE_PREVIEW|USPTO_APPLICATION_DRAFT)\\.(pdf|docx)$`).exec(url);
  if (artifact && method === "GET") return { binary: true, responseLimit: 8 * 1024 * 1024,
    filename: `${artifact[1]}.${artifact[2]}`, mediaType: artifact[2] === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document" };
  return null;
}

function authenticationPage() {
  const nonce = randomBytes(24).toString("base64");
  const html = `<!doctype html><html lang="en"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Local operator authentication</title><main>
    <h1>Local operator authentication</h1>
    <p>This local session supports authentication only.</p>
    <button id="pair">Request pairing</button>
    <p>Pairing selector: <span id="selector">None</span></p>
    <p>Approve this selector using the protected local operator command.</p>
    <button id="login" disabled>Complete login</button>
    <button id="logout" disabled>Log out</button>
    <p id="status" role="status">Checking session…</p></main>
    <script nonce="${nonce}">
    (() => {
      let csrf;
      const status = document.getElementById('status');
      const selector = document.getElementById('selector');
      const login = document.getElementById('login');
      const logout = document.getElementById('logout');
      const pair = document.getElementById('pair');
      async function request(method, bootstrap = false) {
        const headers = {};
        if (method !== 'GET') headers['Content-Type'] = 'application/json';
        if (bootstrap) headers['X-AIIP-Bootstrap'] = '1';
        else if (csrf && method !== 'GET') headers['X-AIIP-CSRF'] = csrf;
        const result = await fetch('${prefix}/session' + (bootstrap ? '/bootstrap' : ''), {
          method, headers, credentials: 'same-origin', cache: 'no-store',
          ...(method === 'GET' ? {} : {body: '{}'})
        });
        if (!result.ok) throw new Error('request rejected');
        const value = await result.json();
        csrf = value.csrf;
        status.textContent = value.state;
        selector.textContent = value.selector || 'None';
        login.disabled = value.state !== 'pending';
        logout.disabled = value.state !== 'authenticated';
        pair.disabled = value.state === 'authenticated';
      }
      async function perform(method, bootstrap = false) {
        try { await request(method, bootstrap); }
        catch { status.textContent = 'Authentication request rejected. Refresh session or retry.'; }
      }
      pair.onclick = () => perform('POST', true);
      login.onclick = () => perform('POST');
      logout.onclick = () => perform('DELETE');
      perform('GET');
    })();
    </script></html>`;
  return { html, csp: `default-src 'none'; script-src 'nonce-${nonce}'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'` };
}

try {
  const material = tlsMaterial();
  if (process.argv.includes("--check-tls")) {
    process.stdout.write("TLS prerequisites verified.\n");
  } else {
    requireSecurity(process.env.AIIP_S1_HOST_FILE);
    privateFiles([process.env.AIIP_S1_HOST_FILE]);
    const host = JSON.parse(readFileSync(process.env.AIIP_S1_HOST_FILE, "utf8"));
    requireSecurity(/^[0-9a-f]{64}$/.test(host.proxy) && Number.isInteger(host.port) && host.port > 0 && host.port <= 65535);
    // Existing Next dependency/build is reused only by this explicit local host.
    const next = (await import("next")).default;
    const app = next({ dev: false, dir: frontend, hostname: "localhost", port: 3443 });
    await app.prepare();
    const server = https.createServer(material, async (request, response) => {
      try {
        guard(request);
        if (request.url === "/product-web" && request.method === "GET") {
          requireSecurity([undefined, "none", "same-origin"].includes(request.headers["sec-fetch-site"]));
          const { html, csp } = authenticationPage();
          response.writeHead(200, { ...safeHeaders, "Content-Type": "text/html; charset=utf-8", "Content-Security-Policy": csp });
          response.end(html);
        } else if ([`${prefix}/session`, `${prefix}/session/bootstrap`].includes(request.url) || syntheticRoute(request.url, request.method, host.synthetic === true)) {
          await proxy(request, response, host);
        } else respond(response, 404, { error: { code: "not_found" } });
      } catch {
        if (!response.headersSent && !response.destroyed) respond(response, 403, { error: { code: "request_rejected" } });
        else response.destroy();
      }
    });
    server.requestTimeout = 5000;
    server.headersTimeout = 5000;
    server.maxHeadersCount = 64;
    server.on("error", () => {
      process.stderr.write("S1 local transport unavailable.\n");
      app.close().finally(() => process.exit(1));
    });
    const shutdown = () => server.close(() => { app.close().finally(() => process.exit()); });
    process.on("SIGTERM", shutdown);
    process.on("SIGINT", shutdown);
    server.listen(3443, "127.0.0.1");
  }
} catch {
  process.stderr.write("S1 local transport unavailable.\n");
  process.exitCode = 1;
}
