import path from "node:path";
import fs from "node:fs";
import { globSync as tinyGlobSync } from "tinyglobby";

// This is the bounded root-directory API of Next's pinned lint helper, not a
// general fast-glob replacement. Validate before entering any glob parser.
function validate(pattern) {
  if (typeof pattern !== "string" || !pattern.length || pattern.includes("\0")) {
    throw new TypeError("Next root glob: expected a non-empty string without NUL");
  }
  if (pattern.length > 4096) throw new RangeError("Next root glob: maximum length is 4096");
  const stack = [];
  let operators = 0;
  let alternatives = 1;
  let extglob = false;
  let characterClass = false;
  for (let i = 0; i < pattern.length; i++) {
    const c = pattern[i];
    if (c === "[") {
      if (characterClass) throw new TypeError("Next root glob: nested character classes are unsupported");
      characterClass = true;
    } else if (c === "]") {
      if (!characterClass) throw new TypeError("Next root glob: unbalanced character class");
      characterClass = false;
    }
    if (c === "{" || c === "(") {
      if (c === "(" && (i === 0 || !"?*+@!".includes(pattern[i - 1]))) {
        throw new TypeError("Next root glob: literal parentheses are unsupported");
      }
      if (c === "(" && extglob) throw new RangeError("Next root glob: nested extglobs are unsupported");
      if (c === "(") extglob = true;
      stack.push({close:c === "{" ? "}" : ")", choices:1});
      if (stack.length > 32) throw new RangeError("Next root glob: maximum nesting depth is 32");
    } else if (c === "}" || c === ")") {
      const frame = stack.pop();
      if (!frame || frame.close !== c) throw new TypeError("Next root glob: unbalanced pattern");
      alternatives *= frame.choices;
      if (alternatives > 256) throw new RangeError("Next root glob: maximum alternatives is 256");
      if (c === ")") extglob = false;
    } else if ((c === "," || c === "|") && stack.length) {
      stack[stack.length - 1].choices++;
    }
    if ("*?{(|".includes(c) && ++operators > 64) throw new RangeError("Next root glob: maximum operators is 64");
  }
  if (stack.length || characterClass) throw new TypeError("Next root glob: unbalanced pattern");
  if (/\{[^{}]*\.\.[^{}]*\}/.test(pattern)) throw new TypeError("Next root glob: brace ranges are unsupported");
  if (pattern.startsWith("!") && !pattern.startsWith("!(")) throw new TypeError("Next root glob: exclusion patterns are unsupported");
}

export function globSync(pattern, options) {
  if (!options || options.onlyDirectories !== true || Object.keys(options).some(k => k !== "onlyDirectories")) {
    throw new TypeError("Next root glob: only { onlyDirectories: true } is supported");
  }
  validate(pattern);
  // get-root-dirs normalizes separators itself; preserve that behavior for direct
  // callers too. Escaped metacharacters are not part of that consumer contract.
  let normalized = pattern.replaceAll("\\", "/");
  if (!/[*?{}[\]()]/.test(normalized)) {
    try { return fs.statSync(normalized).isDirectory() ? [normalized] : []; }
    catch (error) { if (["ENOENT", "ENOTDIR"].includes(error.code)) return []; throw error; }
  }
  // fast-glob treats a final globstar as descendants; tinyglobby also matches
  // the parent. Requiring one terminal entry preserves descendant-only roots.
  if (normalized === "**" || normalized.endsWith("/**")) normalized += "/*";
  const results = tinyGlobSync(normalized, {
    onlyDirectories: true,
    expandDirectories: false,
    absolute: path.isAbsolute(normalized),
    dot: false,
    followSymbolicLinks: true,
  });
  // Ordering is deliberately deterministic. Next accumulates route URLs from
  // every root; differential route tests verify this does not change findings.
  return [...new Set(results.map(p => p.length > 1 ? p.replace(/\/$/, "") : p))].sort();
}
