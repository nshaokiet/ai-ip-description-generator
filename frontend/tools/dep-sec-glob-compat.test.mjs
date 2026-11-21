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
      if(globSync(Array.from({length:256},(_,i)=>'missing-'+i),{cwd:root}).length) throw Error('bad expanded match');
      for(const pattern of ['{a,b}'.repeat(12),'*'.repeat(65),'a'.repeat(4097)]) {
        let denied=false;try{globSync(pattern,{cwd:root})}catch{denied=true}if(!denied)throw Error('unbounded input');}
    } finally {if(path.dirname(path.resolve(root))!==path.resolve(os.tmpdir())||!path.basename(root).startsWith('dep-redos-'))throw Error('unsafe cleanup');fs.rmSync(root,{recursive:true,force:true});}`;
  const result = spawnSync(process.execPath, ["--max-old-space-size=128", "-e", script], {
    timeout: 3000, encoding: "utf8", windowsHide: true });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 0, result.stderr);
});


// Independent synthetic cases for DEP-RECON-QUAL-001. The original frozen
// tinyglobby baseline above stays unchanged; these exercise its missing contract.
const expansionRoot = fs.mkdtempSync(path.join(os.tmpdir(), "dep-sec-expansion-"));
const aFiles = ["packages/a/src/index.ts", "packages/a/src/nested/deep.ts", "packages/a/src/target.ts"];
const aDots = ["packages/a/src/.hidden/deep.ts", "packages/a/src/.private.ts"];
const bFiles = ["packages/b/src/index.ts", "packages/b/src/target.ts"];
const srcFiles = ["src/a.js", "src/a.ts", "src/b.tsx"];
for (const file of [...aFiles, ...aDots, ...bFiles, ...srcFiles]) {
  fs.mkdirSync(path.dirname(path.join(expansionRoot, file)), { recursive: true });
  fs.writeFileSync(path.join(expansionRoot, file), "");
}
after(() => {
  assert.equal(path.dirname(path.resolve(expansionRoot)), path.resolve(os.tmpdir()));
  assert(path.basename(expansionRoot).startsWith("dep-sec-expansion-"));
  fs.rmSync(expansionRoot, { recursive: true, force: true });
});
const expansionCases = [
  ["default wildcard directory", "packages/*/src", {}, [...aFiles, ...bFiles]],
  ["explicit expansion", "packages/*/src", { expandDirectories: true }, [...aFiles, ...bFiles]],
  ["trailing slash", "packages/*/src/", {}, [...aFiles, ...bFiles]],
  ["leading dot slash", "./packages/*/src", {}, [...aFiles, ...bFiles]],
  ["brace directories", "{src,packages/a/src}", {}, [...srcFiles, ...aFiles]],
  ["character class directories", "packages/[ab]/src", {}, [...aFiles, ...bFiles]],
  ["extglob directories", "packages/@(a|b)/src", {}, [...aFiles, ...bFiles]],
  ["globstar directories", "**/src", {}, [...srcFiles, ...aFiles, ...bFiles]],
  ["nested files and dotfiles", "packages/*/src", { dot: true }, [...aFiles, ...aDots, ...bFiles]],
  ["negative directory", ["packages/*/src", "!packages/a/src/nested"], {}, [...aFiles.filter(p => !p.includes("/nested/")), ...bFiles]],
  ["negative dotfile", ["packages/*/src", "!packages/a/src/.private.ts"], { dot: true }, [...aFiles, ...aDots.filter(p => !p.endsWith("/.private.ts")), ...bFiles]],
  ["ignore directory", "packages/*/src", { ignore: "packages/a/src/nested" }, [...aFiles.filter(p => !p.includes("/nested/")), ...bFiles]],
  ["ignore leading dot slash", "packages/*/src", { ignore: ["./packages/a/src/nested"] }, [...aFiles.filter(p => !p.includes("/nested/")), ...bFiles]],
  ["negative leading dot slash", ["packages/*/src", "!./packages/b/src"], {}, aFiles],
  ["ignore glob subtree", "packages/*/src", { ignore: ["**/nested/**"] }, [...aFiles.filter(p => !p.includes("/nested/")), ...bFiles]],
  ["disabled wildcard expansion", "packages/*/src", { expandDirectories: false }, []],
  ["disabled static expansion", "packages/a/src", { expandDirectories: false }, []],
  ["disabled file matching", "packages/*/src/*.ts", { expandDirectories: false }, [...aFiles.filter(p => !p.includes("/nested/")), ...bFiles]],
  ["direct brace file glob", "src/*.{ts,tsx}", {}, ["src/a.ts", "src/b.tsx"]],
  ["direct literal file", "src/a.ts", {}, ["src/a.ts"]],
  ["mixed file and directory brace", "{src/*,packages/a/src}", {}, [...srcFiles, ...aFiles]],
  ["terminal wildcard remains direct", "packages/*", {}, []],
  ["terminal wildcard with slash", "packages/*/", {}, []],
  ["static directory", "packages/a/src/", {}, aFiles],
];
for (const [name, patterns, options, expected] of expansionCases) test(`directory expansion: ${name}`, () => {
  const actual = globSync(patterns, { cwd: expansionRoot, ...options }).map(slash).sort();
  assert.deepEqual(actual, [...expected].sort());
  const absolute = globSync(patterns, { cwd: expansionRoot, ...options, absolute: true });
  assert.deepEqual(absolute.map(p => slash(path.relative(expansionRoot, p))).sort(), [...expected].sort());
});

for (const include of ["packages/*/src", "packages/[ab]/src"]) test(`actual resolver selects owning tsconfig for ${include}`, t => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), "dep-sec-resolver-"));
  t.after(() => {
    assert.equal(path.dirname(path.resolve(fixture)), path.resolve(os.tmpdir()));
    assert(path.basename(fixture).startsWith("dep-sec-resolver-"));
    fs.rmSync(fixture, { recursive: true, force: true });
  });
  for (const file of ["packages/a/src/index.ts", "packages/a/src/target.ts", "packages/legacy/src/target.ts"]) {
    fs.mkdirSync(path.dirname(path.join(fixture, file)), { recursive: true });
    fs.writeFileSync(path.join(fixture, file), "export const synthetic = 1;");
  }
  const configs = ["legacy", "packages"].map(name => path.join(fixture, `tsconfig.${name}.json`));
  for (const [index, config] of configs.entries()) fs.writeFileSync(config, JSON.stringify({
    compilerOptions: { baseUrl: ".", paths: { "@shared/*": [index ? "packages/a/src/*" : "packages/legacy/src/*"] } },
    include: index ? [include] : ["packages/legacy/src"],
  }));
  const resolverEntry = configRequire.resolve("eslint-import-resolver-typescript");
  assert.equal(JSON.parse(fs.readFileSync(path.join(path.dirname(resolverEntry), "../package.json"))).version, "3.10.1");
  const resolved = configRequire("eslint-import-resolver-typescript").resolve("@shared/target",
    path.join(fixture, "packages/a/src/index.ts"), { project: configs });
  assert.equal(resolved.found, true);
  assert.equal(slash(resolved.path), slash(path.join(fixture, "packages/a/src/target.ts")));
  assert.notEqual(slash(resolved.path), slash(path.join(fixture, "packages/legacy/src/target.ts")));
});

test("directory expansion preserves bounded pattern and ignore arrays", () => {
  assert.deepEqual(globSync(Array(256).fill("missing-directory"), { cwd: expansionRoot }), []);
  assert.throws(() => globSync(Array(257).fill("missing-directory")), /bounded pattern array/);
  assert.throws(() => globSync("packages/*/src", { ignore: Array(257).fill("missing") }), /invalid ignore array/);
});
