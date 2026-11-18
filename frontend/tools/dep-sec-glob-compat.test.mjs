import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";
import { test, after } from "node:test";

const require = createRequire(import.meta.url);
const { globSync, isDynamicPattern } = require("tinyglobby");
const frontend = path.resolve(import.meta.dirname, "..");
const baseline = JSON.parse(fs.readFileSync(new URL("./dep-sec-glob-baseline.json", import.meta.url)));
const root = fs.mkdtempSync(path.join(os.tmpdir(), "dep-sec-compat-"));
for (const file of baseline.files) {
  fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
  fs.writeFileSync(path.join(root, file), "");
}
after(() => {
  assert.equal(path.dirname(path.resolve(root)), path.resolve(os.tmpdir()));
  assert(path.basename(root).startsWith("dep-sec-compat-"));
  fs.rmSync(root, { recursive: true, force: true });
});
const slash = p => p.replaceAll("\\", "/");
const normalize = p => slash(p).replace(slash(root), "$ROOT");

test("frozen source expectations came from original tinyglobby0.2.17", () => {
  assert.equal(baseline.source, "tinyglobby0.2.17");
  assert.equal(baseline.source_sha256, "ee408bbc9665cba5800a6b2a0c89dd3df9820baa30d4ff3ba2f2435f16ce9f94");
  assert.equal(require("tinyglobby/package.json").name, "@ai-ip/ts-project-glob-adapter");
});

for (const [index, entry] of baseline.cases.entries()) test(`original project/include/ignore path set ${index}`, () => {
  // Original traversal order is filesystem-dependent, not an API promise.
  // Actual estree pattern precedence is tested separately below.
  const actual = globSync(entry.patterns, { cwd: root, ...entry.options }).map(normalize).sort();
  assert.deepEqual(actual, [...entry.expected].sort());
});
for (const entry of baseline.dynamic) test(`original dynamic classification: ${entry.pattern}`, () => {
  assert.equal(isDynamicPattern(entry.pattern), entry.expected);
});

const configRequire = createRequire(require.resolve("eslint-config-next"));
const tsRequire = createRequire(configRequire.resolve("typescript-eslint"));
const estreeRequire = createRequire(tsRequire.resolve("@typescript-eslint/typescript-estree"));
const resolverRequire = createRequire(configRequire.resolve("eslint-import-resolver-typescript"));

test("both actual TS consumers use the owned adapter and vulnerable packages are absent", () => {
  for (const consumer of [estreeRequire, resolverRequire]) assert.equal(consumer("tinyglobby").globSync, globSync);
  const lock = JSON.parse(fs.readFileSync(path.join(frontend, "package-lock.json")));
  const consumers = Object.entries(lock.packages).filter(([,v]) => v.dependencies?.tinyglobby).map(([k]) => k);
  assert.equal(consumers.length, 2);
  assert(consumers.some(p => p.endsWith("/typescript-estree")));
  assert(consumers.some(p => p.endsWith("/eslint-import-resolver-typescript")));
  for (const key of Object.keys(lock.packages))
    assert(!/(?:^|node_modules\/)(picomatch|fdir|micromatch|braces)$/.test(key), key);
  assert.equal(lock.packages["node_modules/tinyglobby"].resolved, "file:tools/ts-project-glob-adapter");
  assert.deepEqual(fs.readFileSync(require.resolve("tinyglobby")),
    fs.readFileSync(path.join(frontend,"tools/ts-project-glob-adapter/index.mjs")));
});

test("actual estree project selection preserves pattern precedence and node_modules exclusion", () => {
  const entry = path.join(path.dirname(estreeRequire.resolve("@typescript-eslint/typescript-estree/package.json")),
    "dist/parseSettings/resolveProjectList.js");
  const { resolveProjectList, clearGlobResolutionCache } = require(entry);
  clearGlobResolutionCache();
  const projects = [...resolveProjectList({ project: ["packages/b/*.json", "packages/a/*.json"],
    tsconfigRootDir: root, singleRun: true }).values()].map(p => slash(path.relative(root, p)));
  assert.deepEqual(projects, ["packages/b/tsconfig.json", "packages/a/tsconfig.json"]);
  fs.writeFileSync(path.join(root, "packages/a/node_modules/dep/tsconfig.json"), "{}");
  clearGlobResolutionCache();
  const all = [...resolveProjectList({ project: ["**/tsconfig.json"], tsconfigRootDir: root,
    singleRun: true }).values()];
  assert(all.every(p => !slash(p).includes("/node_modules/")));
  assert.equal(all.length, 3); // Non-dot a,b and root, matching original defaults.
});

test("actual typed parser and import resolver retain project programs, aliases and excludes", () => {
  for (const pkg of ["a", "b"]) {
    fs.writeFileSync(path.join(root, `packages/${pkg}/tsconfig.json`), JSON.stringify({
      compilerOptions: { baseUrl: ".", paths: { [`@${pkg}/*`]: ["src/*"] } },
      include: ["src/**/*.ts"], exclude: ["dist", "node_modules"] }));
  }
  const file = path.join(root, "packages/a/src/index.ts");
  const source = "export const value: number = 1;";
  fs.writeFileSync(file, source);
  const parser = tsRequire("@typescript-eslint/parser");
  const parsed = parser.parseForESLint(source, { filePath: file, project: ["packages/*/tsconfig.json"],
    tsconfigRootDir: root });
  assert(parsed.services.program.getSourceFile(file));
  const resolver = configRequire("eslint-import-resolver-typescript");
  const resolved = resolver.resolve("@a/index", file, { project: [slash(root) + "/packages/*/tsconfig.json"] });
  assert.equal(resolved.found, true);
  assert.equal(slash(resolved.path), slash(file));
});

test("unknown options reject rather than silently weakening project filtering", () => {
  for (const options of [17, true, "str", [], null, { dot: "true" }, { onlyDirectories: true }, { fs: {} }, { ignore: 17 }])
    assert.throws(() => globSync("**/*.ts", options), /Project glob/);
});

test("advisory repeated extglobs and pathological brace patterns stay bounded", () => {
  const adapterModule = require.resolve("tinyglobby");
  const script = `const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
    const {globSync}=require(${JSON.stringify(adapterModule)});
    const root=fs.mkdtempSync(path.join(os.tmpdir(),'dep-redos-'));
    try {fs.writeFileSync(path.join(root,'a'.repeat(42)+'!'),'');
      for(const pattern of ['+(*a)','+(*?a)','*(?*a)']) if(globSync(pattern,{cwd:root}).length) throw Error('bad match');
      for(const pattern of ['{a,b}'.repeat(12),'*'.repeat(65),'a'.repeat(4097)]) {
        let denied=false;try{globSync(pattern,{cwd:root})}catch{denied=true}if(!denied)throw Error('unbounded input');}
    } finally {if(path.dirname(path.resolve(root))!==path.resolve(os.tmpdir())||!path.basename(root).startsWith('dep-redos-'))throw Error('unsafe cleanup');fs.rmSync(root,{recursive:true,force:true});}`;
  const result = spawnSync(process.execPath, ["--max-old-space-size=128", "-e", script], {
    timeout: 3000, encoding: "utf8", windowsHide: true });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 0, result.stderr);
});
