import { createReadStream, statSync } from "node:fs";
import { createServer, request as httpRequest } from "node:http";
import { extname, join, normalize } from "node:path";

const frontendPort = Number(process.argv[2] ?? "3107");
const backendPort = Number(process.argv[3] ?? "8001");
const staticRoot = join(process.cwd(), "out");
const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".woff2": "font/woff2",
};

function proxyBackend(incoming, outgoing) {
  const targetPath = incoming.url.replace(/^\/backend/, "") || "/";
  const proxied = httpRequest(
    {
      hostname: "127.0.0.1",
      port: backendPort,
      path: targetPath,
      method: incoming.method,
      headers: { ...incoming.headers, host: `127.0.0.1:${backendPort}` },
    },
    (response) => {
      outgoing.writeHead(response.statusCode ?? 502, response.headers);
      response.pipe(outgoing);
    },
  );
  proxied.on("error", () => {
    outgoing.writeHead(502, { "content-type": "application/json" });
    outgoing.end(JSON.stringify({ error: { code: "demo_proxy_unavailable" } }));
  });
  incoming.pipe(proxied);
}

function serveStatic(incoming, outgoing) {
  const urlPath = new URL(incoming.url, "http://127.0.0.1").pathname;
  const relativePath = urlPath === "/" ? "index.html" : decodeURIComponent(urlPath).replace(/^\/+/, "");
  const safePath = normalize(relativePath);
  if (safePath.startsWith("..")) {
    outgoing.writeHead(404).end();
    return;
  }
  const filePath = join(staticRoot, safePath);
  try {
    if (!statSync(filePath).isFile()) throw new Error("not a file");
    outgoing.writeHead(200, {
      "cache-control": "no-store",
      "content-type": contentTypes[extname(filePath)] ?? "application/octet-stream",
    });
    createReadStream(filePath).pipe(outgoing);
  } catch {
    outgoing.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    outgoing.end("Not found");
  }
}

const server = createServer((incoming, outgoing) => {
  if (incoming.url?.startsWith("/backend/")) proxyBackend(incoming, outgoing);
  else serveStatic(incoming, outgoing);
});

server.listen(frontendPort, "127.0.0.1");
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
