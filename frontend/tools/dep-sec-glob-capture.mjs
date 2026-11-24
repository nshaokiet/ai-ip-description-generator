// One-time capture against the original installed tinyglobby0.2.17, before
// replacement. This script is not used to regenerate expectations during tests.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createHash } from "node:crypto";
import { createRequire } from "node:module";
import { globSync, isDynamicPattern } from "tinyglobby";

const require = createRequire(import.meta.url);
const pkg = require("tinyglobby/package.json");
if (pkg.name !== "tinyglobby" || pkg.version !== "0.2.17")
  throw new Error("Capture requires the original tinyglobby0.2.17; never overwrite a frozen baseline from its replacement");

const root = fs.mkdtempSync(path.join(os.tmpdir(), "dep-sec-original-"));
const files = ["tsconfig.json", ".hidden/tsconfig.json", "packages/a/tsconfig.json",
  "packages/b/tsconfig.json", "packages/a/src/index.ts", "packages/a/src/.private.ts",
  "packages/a/dist/index.ts", "packages/a/node_modules/dep/index.ts", "src/a.ts",
  "src/b.tsx", "src/a.js", "space dir/c.ts", "Tiếng Việt/d.ts", "Case/e.ts"];
try {
  for (const file of files) {
    fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
    fs.writeFileSync(path.join(root, file), "");
  }
  const inputs = [
    ["packages/*/tsconfig.json", { expandDirectories: false }],
    ["**/tsconfig.json", { expandDirectories: false, ignore: ["**/node_modules/**"] }],
    ["**/tsconfig.json", { absolute: true, dot: true, expandDirectories: false, ignore: ["**/node_modules/**"] }],
    [["packages/b/tsconfig.json", "packages/a/tsconfig.json"], { absolute: true, expandDirectories: false }],
    [["packages/*/tsconfig.json", "tsconfig.json"], { expandDirectories: false }],
    ["**/*", { absolute: true, dot: true, ignore: ["**/node_modules/**", "**/dist/**"] }],
    [["src", "packages/a/src"], { absolute: true, dot: true }],
    ["src/*.{ts,tsx}", { absolute: true, dot: true }],
    ["packages/{a,b}/src/**/*.ts", { dot: true, ignore: ["**/.private.ts"] }],
    ["packages/a/**/*", { dot: true, ignore: ["packages/a/dist", "**/node_modules/**"] }],
    ["missing/**/*.ts", { dot: true }],
    [[], { absolute: true, dot: true, expandDirectories: false }],
    ["space dir/*.ts", { absolute: true, dot: true }],
    ["Tiếng Việt/*.ts", { absolute: true, dot: true }],
    ["Case/*.ts", { expandDirectories: false }],
  ];
  const normalize = p => p.replaceAll("\\", "/").replace(root.replaceAll("\\", "/"), "$ROOT");
  const cases = inputs.map(([patterns, options]) => ({ patterns, options,
    expected: globSync(patterns, { cwd: root, ...options }).map(normalize) }));
  const patterns = ["tsconfig.json", "packages/*/tsconfig.json", "**/*.ts", "{a,b}/tsconfig.json",
    "file[12].ts", "@(a|b)", "a(b)", "{unfinished,", "[unclosed", "!excluded", "", "space dir/file.ts"];
  const source = fs.readFileSync(new URL("../node_modules/tinyglobby/dist/index.cjs", import.meta.url));
  const baseline = { version: "1.0.0", source: "tinyglobby0.2.17", node: process.version,
    source_sha256: createHash("sha256").update(source).digest("hex"), files, cases,
    dynamic: patterns.map(pattern => ({ pattern, expected: isDynamicPattern(pattern) })) };
  fs.writeFileSync(new URL("./dep-sec-glob-baseline.json", import.meta.url), JSON.stringify(baseline, null, 2) + "\n");
  console.log(JSON.stringify({ cases: cases.length, dynamic: patterns.length, source_sha256: baseline.source_sha256 }));
} finally {
  // This freshly created, known synthetic temp tree is wholly owned by capture.
  if (path.dirname(path.resolve(root)) !== path.resolve(os.tmpdir()) || !path.basename(root).startsWith("dep-sec-original-"))
    throw new Error("Unsafe capture cleanup target");
  fs.rmSync(root, { recursive: true, force: true });
}
