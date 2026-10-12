import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import { test, after } from "node:test";
import { ESLint } from "eslint";
import { globSync } from "./next-root-glob-adapter/index.mjs";

const frontend = path.resolve(import.meta.dirname, "..");
const require = createRequire(path.join(frontend, "package.json"));
const baseline = JSON.parse(fs.readFileSync(new URL("./dep-001-lint-baseline.json", import.meta.url)));
const root = fs.mkdtempSync(path.join(os.tmpdir(), "dep-a2-contract-"));
for (const dir of baseline.tree.dirs.filter(d => d !== "case")) fs.mkdirSync(path.join(root, dir), {recursive:true});
for (const file of baseline.tree.files) fs.writeFileSync(path.join(root,file), "export default function Page(){return null;}");
after(() => fs.rmSync(root, {recursive:true,force:true}));
const onlyDirs = {onlyDirectories:true};
const diagnostics = messages => messages.map(({ruleId,severity,message,line,column})=>({ruleId,severity,message,line,column}));
const configSnapshot = c => ({rules:c.rules,settings:c.settings,plugins:Object.keys(c.plugins),languageOptions:{...c.languageOptions,parser:{meta:c.languageOptions.parser.meta}}});
const eslint = new ESLint({cwd:frontend});
const slash = s => s.replaceAll("\\", "/");
const resolveRoot = v => typeof v === "string" ? v.replace("$ROOT", slash(root)) : Array.isArray(v) ? v.map(resolveRoot) : v;

test("all 25 original configurations preserve rules/options/parser/plugins/globals/settings", async () => {
  for (const group of baseline.groups) for (const file of group.files) assert.deepEqual(configSnapshot(await eslint.calculateConfigForFile(file)), group.config, file);
  for (const entry of baseline.ignores) assert.equal(await eslint.isPathIgnored(entry.file), entry.expected, entry.file);
  for (const file of ["tools/dep-001-lint-security.test.mjs", "tools/next-root-glob-adapter/index.mjs"]) {
    assert.equal(await eslint.isPathIgnored(file),false);
    assert.equal((await eslint.calculateConfigForFile(file)).rules["@next/next/no-html-link-for-pages"][0],2);
  }
});

for (const fixture of baseline.fixtures) test(`negative fixture: ${fixture.name}`, async () => {
  const actual = diagnostics((await eslint.lintText(fixture.source,{filePath:fixture.file}))[0].messages);
  assert(actual.some(d=>d.ruleId===fixture.expected),fixture.expected);
  assert.deepEqual(actual,fixture.before);
});

for (const c of baseline.globCases) test(`relative directory contract: ${c.pattern}`, () => {
  const cwd=process.cwd();
  try {
    process.chdir(root);
    const actual=globSync(c.pattern,onlyDirs);
    const expected=c.pattern==="case" && process.platform!=="win32" ? [] : c.expected;
    assert.deepEqual(actual, [...expected].sort());
    assert.equal(new Set(actual).size,actual.length);
  } finally { process.chdir(cwd); }
});
for (const c of baseline.absoluteCases) test(`absolute directory contract: ${c.pattern}`, () => {
  const expected=c.pattern==="case" && process.platform!=="win32" ? [] : c.expected.map(resolveRoot);
  assert.deepEqual(globSync(slash(path.join(root,c.pattern)),onlyDirs),[...expected].sort());
});

for (const c of baseline.routes) test(`Next actual root/route diagnostics: ${JSON.stringify(c.roots)}`, async () => {
  const settings=c.roots===null ? {} : {next:{rootDir:resolveRoot(c.roots)}};
  const instance=new ESLint({cwd:frontend,overrideConfig:{settings}});
  assert.deepEqual(diagnostics((await instance.lintText(c.source,{filePath:"src/app/a2-route.tsx"}))[0].messages),c.expected);
});

test("Next arrays, duplicate roots, Windows/POSIX separators and default cwd", () => {
  const getRoots=require("@next/eslint-plugin-next/dist/utils/get-root-dirs.js").getRootDirs;
  assert.deepEqual(getRoots({cwd:frontend,settings:{}}),[frontend]);
  const app=slash(path.join(root,"app"));
  assert.deepEqual(getRoots({cwd:frontend,settings:{next:{rootDir:[app,app,17]}}}),[app,app]);
  assert.deepEqual(getRoots({cwd:frontend,settings:{next:{rootDir:app.replaceAll("/","\\")}}}),[app]);
});

test("unsupported multiple/exclusion/options/empty calls fail explicitly", () => {
  for(const pattern of [[],["app","packages"],"!app","",null,17,"app\0bad","{1..100000}","{app", "@(a|@(b))","app[","app]","(app)"]) assert.throws(()=>globSync(pattern,onlyDirs));
  for(const options of [undefined,{}, {onlyDirectories:false},{onlyDirectories:true,ignore:["app"]},{onlyDirectories:true,cwd:root},{onlyDirectories:true,dot:true}]) assert.throws(()=>globSync("app",options),/Next root glob/);
});

test("bounded malicious patterns terminate before parser invocation", () => {
  const adapterModule=path.join(import.meta.dirname,"next-root-glob-adapter/index.mjs");
  const script=`import {globSync} from ${JSON.stringify(pathToFileURL(adapterModule).href)}; for(const p of ['{'.repeat(33)+'a'+'}'.repeat(33),'a'.repeat(4097),'{a,b}'.repeat(12),'*'.repeat(65),'@('.repeat(10)+'a'+')'.repeat(10)]) { let rejected=false; try { globSync(p,{onlyDirectories:true}); } catch { rejected=true; } if(!rejected) throw Error('unsafe pattern accepted'); }`;
  const result=spawnSync(process.execPath,["--input-type=module","-e",script],{timeout:3000,encoding:"utf8"});
  assert.equal(result.error,undefined);
  assert.equal(result.status,0,result.stderr);
});

test("symlink roots follow the existing contract; filesystem failures propagate", t => {
  const link=path.join(root,"linked");
  try { fs.symlinkSync(path.join(root,"app"),link,process.platform==="win32" ? "junction" : "dir"); }
  catch(error) { if(["EPERM","EACCES","ENOTSUP"].includes(error.code)) {t.skip(`symlink unavailable: ${error.code}`);return;} throw error; }
  assert.deepEqual(globSync(slash(link),onlyDirs),[slash(link)]);
  assert.deepEqual(globSync(slash(link)+"/**",onlyDirs),[slash(link)+"/nested"]);
  const stat=fs.statSync;
  try { fs.statSync=()=>{throw Object.assign(new Error("probe access failure"),{code:"EACCES"});}; assert.throws(()=>globSync(slash(link),onlyDirs),/probe access failure/); }
  finally {fs.statSync=stat;}
});

test("pinned sole consumer, actual alias identity, graph and official plugin integrity", () => {
  const lock=JSON.parse(fs.readFileSync(path.join(frontend,"package-lock.json")));
  const consumers=Object.entries(lock.packages).filter(([,v])=>v.dependencies?.["fast-glob"]).map(([k])=>k);
  assert.deepEqual(consumers,["node_modules/@next/eslint-plugin-next"]);
  assert.equal(require("@next/eslint-plugin-next/package.json").version,"16.3.8");
  const pluginRequire=createRequire(require.resolve("@next/eslint-plugin-next/package.json"));
  assert.equal(pluginRequire("fast-glob").globSync instanceof Function,true);
  const adapterPath=pluginRequire.resolve("fast-glob");
  assert.equal(JSON.parse(fs.readFileSync(path.join(path.dirname(adapterPath),"package.json"))).name,"@ai-ip/next-root-glob-adapter");
  assert.deepEqual(fs.readFileSync(adapterPath),fs.readFileSync(path.join(import.meta.dirname,"next-root-glob-adapter/index.mjs")));
  for(const key of Object.keys(lock.packages)) assert(!/(?:^|\/node_modules\/)(braces|micromatch)$/.test(key) && !/^node_modules\/(braces|micromatch)$/.test(key),key);
  const pluginDir=path.dirname(require.resolve("@next/eslint-plugin-next/package.json"));
  for(const [file,hash] of Object.entries(baseline.pluginHashes)) assert.equal(createHash("sha256").update(fs.readFileSync(path.join(pluginDir,file))).digest("hex"),hash);
});

test("additional Next/React/TS rules and positive route cases retain protection", async () => {
  for(const [source,rule] of [
    ['import Document from "next/document"; export default Document;',"@next/next/no-document-import-in-page"],
    ['import Head from "next/head"; export default function Page(){return <Head><script src="/x.js"/></Head>;}',"@next/next/no-sync-scripts"],
    ['export default function Page(){return <div children="x">child</div>;}','react/no-children-prop'],
    ['export const value: String = "x";',"@typescript-eslint/no-wrapper-object-types"],
  ]) assert((await eslint.lintText(source,{filePath:"src/app/a2-extra.tsx"}))[0].messages.some(m=>m.ruleId===rule),rule);
  const source='import Link from "next/link"; export default function Page(){return <><Link href="/">Home</Link><a href="https://example.org">External</a><a download href="/">Download</a></>;}';
  assert.equal((await eslint.lintText(source,{filePath:"src/app/a2-positive.tsx"}))[0].messages.filter(m=>m.ruleId==="@next/next/no-html-link-for-pages").length,0);
});
