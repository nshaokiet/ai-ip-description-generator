// S2-local private shared-state IPC. No browser-supplied publication authority.
import fs from "node:fs";
import path from "node:path";
import { createHash, timingSafeEqual } from "node:crypto";
import { setTimeout as delay } from "node:timers/promises";

const digest = value => createHash("sha256").update(value).digest("hex");
const hex = value => typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
const same = (a, b) => hex(a) && hex(b) && timingSafeEqual(Buffer.from(a, "hex"), Buffer.from(b, "hex"));
function requireGate(value) { if (!value) throw new Error("publication_unavailable"); }

export async function publish(host, receipt, request, response, payload, status, headers, started,
  { clock = () => performance.now() } = {}) {
  requireGate(host.publication && hex(receipt) && hex(host.publication.instance));
  const root = host.publication.root;
  const statePath = path.join(root, "state.json");
  const gate = path.join(root, "gate");
  const failed = path.join(root, "failed");
  const end = performance.now() + 1000;
  let acquired = false;
  try {
    requireGate(!fs.existsSync(failed));
    while (!acquired) {
      try { fs.mkdirSync(gate, { mode: 0o700 }); acquired = true; }
      catch (error) {
        if (error.code !== "EEXIST" || performance.now() >= end) {
          try { fs.writeFileSync(failed, "", { flag: "wx", mode: 0o600 }); } catch { /* Fail closed below. */ }
          throw new Error("publication_unavailable");
        }
        await delay(5);
      }
    }
    // Everything below is synchronous: no check--await--send gap. The parent
    // cannot acknowledge revocation until this same gate has been released.
    const stat = fs.lstatSync(statePath);
    requireGate(stat.isFile() && !stat.isSymbolicLink() && stat.size <= 8192);
    const state = JSON.parse(fs.readFileSync(statePath, "utf8"));
    requireGate(!fs.existsSync(failed) && same(state.instance, host.publication.instance) && state.open === true);
    const grant = state.receipts[receipt];
    if (!grant) {
      const error = new Error("authority_revoked");
      error.status = 401;
      throw error;
    }
    requireGate(same(grant.instance, state.instance));
    const tokens = (request.headers.cookie ?? "").split(";").map(p => p.trim().split("="))
      .filter(p => p[0] === "__Host-aiip_web");
    requireGate(tokens.length === 1 && same(grant.session, digest(tokens[0][1])));
    const base = "/api/product-web/v1/documents";
    const action = request.method === "POST" && request.url === base ? "intake"
      : request.url.includes("/artifacts/") ? "download" : request.url.split("/").at(-1);
    requireGate(hex(grant.principal) && /^[0-9a-f]{32}$/.test(grant.document)
      && Number.isInteger(grant.revision) && grant.revision > 0
      && Number.isInteger(grant.epoch) && grant.epoch >= 0
      && Number.isInteger(grant.operation) && grant.operation > 0
      && grant.action === action && grant.path === request.url
      && (action === "intake" || request.url.startsWith(`${base}/${grant.document}/`))
      && (!request.url.includes("/revisions/") || request.url.includes(`/revisions/${grant.revision}/`))
      && grant.status === status && grant.media_type === headers["Content-Type"]
      && grant.bytes === payload.length && same(grant.digest, digest(payload))
      && Number.isInteger(grant.budget_ms) && grant.budget_ms > 0 && grant.budget_ms <= 120000
      && clock() < started + grant.budget_ms);
    requireGate(!response.destroyed && !response.headersSent && response.socket?.writable
      && !response.socket.destroyed);
    delete state.receipts[receipt]; // Consume before transport handoff; replay fails.
    const fd = fs.openSync(statePath, "r+");
    try {
      fs.ftruncateSync(fd, 0);
      fs.writeFileSync(fd, JSON.stringify(state));
    } finally { fs.closeSync(fd); }
    response.writeHead(status, headers);
    response.end(payload);
    // HTTP end() may cork its connected TLS socket. Flush that transport's
    // cork synchronously before releasing the publication gate.
    const socket = response.socket;
    if (socket && socket.writableCorked) {
      requireGate(socket.writableCorked <= 4);
      while (socket.writableCorked) socket.uncork();
    }
    // A connected response must transfer its body to TLS/socket output during
    // end(), not retain a private HTTP outputData buffer for a later callback.
    if (response.outputSize !== 0) {
      response.destroy();
      throw new Error("publication_unavailable");
    }
  } finally {
    if (acquired) fs.rmdirSync(gate);
  }
}
