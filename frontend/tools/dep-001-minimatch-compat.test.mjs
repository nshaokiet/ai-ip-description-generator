import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

const require = createRequire(import.meta.url);
const configRequire = createRequire(require.resolve("eslint-config-next"));
const tsRequire = createRequire(configRequire.resolve("typescript-eslint"));
const estreeRequire = createRequire(tsRequire.resolve("@typescript-eslint/typescript-estree"));
const { minimatch } = estreeRequire("minimatch");

test("the actual estree consumer retains dot-aware default-project allowlist semantics", () => {
  const cases = [
    ["config.ts", "*.ts", true],
    [".config.ts", "*.ts", true],
    ["config.js", "*.ts", false],
    ["nested/config.ts", "*.ts", false],
    ["nested/config.ts", "nested/*.ts", true],
    ["nested/deep/config.ts", "nested/*.ts", false],
    ["nested/deep/config.ts", "nested/**/*.ts", true],
    ["nested/.config.ts", "nested/*.ts", true],
    ["nested/config.tsx", "nested/*.{ts,tsx}", true],
    ["nested/config.js", "nested/*.{ts,tsx}", false],
    ["tool.ts", "@(tool|config).ts", true],
    ["other.ts", "@(tool|config).ts", false],
  ];
  for (const [file, pattern, expected] of cases) {
    assert.equal(minimatch(file, pattern, { dot: true }), expected, `${file}: ${pattern}`);
  }
  const allowed = ["*.ts", "scripts/*.js"];
  for (const [file, expected] of [[".config.ts", true], ["scripts/task.js", true], ["private/task.js", false]]) {
    assert.equal(allowed.some(pattern => minimatch(file, pattern, { dot: true })), expected, file);
  }
});

test("deep glob preprocessing at optimization level two completes in a bounded child", () => {
  const modulePath = estreeRequire.resolve("minimatch");
  const script = `const {minimatch}=require(${JSON.stringify(modulePath)}); for (const n of [8,16,32]) { const pattern='**/../'.repeat(n)+'file.ts'; const result=minimatch('file.ts',pattern,{optimizationLevel:2,dot:true}); if (typeof result!=='boolean') throw Error('invalid result'); }`;
  const result = spawnSync(process.execPath, ["--max-old-space-size=128", "-e", script], {
    timeout: 3000,
    encoding: "utf8",
    windowsHide: true,
  });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 0, result.stderr);
});
