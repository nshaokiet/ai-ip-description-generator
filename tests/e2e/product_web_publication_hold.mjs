// Trusted test-process scheduler. Application code never imports this module.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
const root = new URL(import.meta.url).searchParams.get("root");
const original = http.request;
http.request = function(options, callback) {
  return original.call(this, options, incoming => {
    const arm = path.join(root, "publication-arm.json");
    const target = fs.existsSync(arm) ? JSON.parse(fs.readFileSync(arm, "utf8")).target : null;
    if (options.path === target) {
      fs.unlinkSync(arm);
      let bytes = 0;
      incoming.on("data", chunk => { bytes += chunk.length; });
      const on = incoming.on;
      incoming.on = function(event, listener) {
        if (event !== "end") return on.call(this, event, listener);
        return on.call(this, event, function(...args) {
          fs.writeFileSync(path.join(root, "publication-held.json"), JSON.stringify({
            status: incoming.statusCode, complete: incoming.complete, bytes,
            has_receipt: typeof incoming.headers["x-aiip-publication"] === "string",
          }));
          const timer = setInterval(() => {
            const release = path.join(root, "publication-release");
            if (!fs.existsSync(release)) return;
            clearInterval(timer);
            fs.unlinkSync(release);
            listener.apply(this, args);
          }, 5);
          timer.unref();
          setTimeout(() => { clearInterval(timer); incoming.destroy(); }, 15000).unref();
        });
      };
    }
    callback(incoming);
  });
};
