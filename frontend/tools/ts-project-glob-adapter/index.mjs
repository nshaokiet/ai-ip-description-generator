// Narrow synchronous contract used by pinned typescript-estree project discovery
// and eslint-import-resolver-typescript. This contains no picomatch/fdir code and
// is not a general tinyglobby replacement. Unrecognized APIs/options fail closed.
import path from "node:path";
import { fileURLToPath } from "node:url";
import { globSync as officialGlobSync, hasMagic } from "glob";

function validate(pattern, empty = false) {
  if (typeof pattern !== "string" || pattern.includes("\0") || (!empty && !pattern.length))
    throw new TypeError("Project glob: invalid pattern");
  if (pattern.length > 4096) throw new RangeError("Project glob: pattern too long");
  let operators = 0, alternatives = 1;
  const stack = [];
  for (let index = 0; index < pattern.length; index++) {
    if (pattern[index] === "\\") { index++; continue; }
    const c = pattern[index];
    if ("*?{(|".includes(c) && ++operators > 64) throw new RangeError("Project glob: too many operators");
    if (c === "{") { stack.push(1); if (stack.length > 32) throw new RangeError("Project glob: nesting limit"); }
    else if (c === "," && stack.length) stack[stack.length - 1]++;
    else if (c === "}" && stack.length) {
      alternatives *= stack.pop();
      if (alternatives > 256) throw new RangeError("Project glob: expansion limit");
    }
  }
}
export function isDynamicPattern(pattern, options) {
  validate(pattern, true);
  if (options?.caseSensitiveMatch === false) return true;
  return pattern.startsWith("!") || /(?<!\\)[()]/.test(pattern)
    || /(?<!\\)\{[^}]*,/.test(pattern) || hasMagic(pattern, { magicalBraces: true });
}

export function globSync(patterns, options = {}) {
  if (!options || typeof options !== "object" || Array.isArray(options)
      || Object.keys(options).some(k => !["cwd", "absolute", "dot", "expandDirectories", "ignore"].includes(k)))
    throw new TypeError("Project glob: unsupported options");
  for (const key of ["absolute", "dot", "expandDirectories"])
    if (options[key] !== undefined && typeof options[key] !== "boolean") throw new TypeError("Project glob: invalid option");
  const input = typeof patterns === "string" ? [patterns] : patterns;
  if (!Array.isArray(input) || input.length > 256) throw new TypeError("Project glob: expected bounded pattern array");
  input.forEach(p => validate(p));
  let ignores = options.ignore === undefined ? [] : typeof options.ignore === "string" ? [options.ignore] : options.ignore;
  if (!Array.isArray(ignores) || ignores.length > 256) throw new TypeError("Project glob: invalid ignore array");
  ignores.forEach(p => validate(p));
  let cwd = options.cwd ?? process.cwd();
  if (cwd instanceof URL) cwd = fileURLToPath(cwd);
  if (typeof cwd !== "string") throw new TypeError("Project glob: invalid cwd");
  const include = [], negatives = [];
  for (const pattern of input) {
    if (pattern.startsWith("!") && !pattern.startsWith("!(")) { negatives.push(pattern.slice(1)); continue; }
    if (options.expandDirectories !== false) {
      const normalized = pattern.length > 1 ? pattern.replace(/\/$/, "") : pattern;
      // Keep direct files and directory descendants. At most two derived patterns
      // per validated input (256 inputs); no filesystem-driven pattern expansion.
      include.push(normalized);
      if (!normalized.endsWith("*")) include.push(normalized.endsWith("/") ? `${normalized}**` : `${normalized}/**`);
    } else include.push(pattern);
  }
  if (!include.length) return [];
  ignores = [...ignores, ...negatives].flatMap(p => [p, p.replace(/\/$/, "") + "/**"]);
  const results = officialGlobSync(include, { cwd, absolute: options.absolute ?? false,
    dot: options.dot ?? false, nodir: true, follow: true, nocase: false, ignore: ignores });
  return [...new Set(results.map(p => p.replaceAll("\\", "/").replace(/^\/\/\?\//, "")))].sort();
}
