# Next root glob security adapter 1.0.0

Private, development-only package `@ai-ip/next-root-glob-adapter`, approved by the
Human DEP-001-A2 implementation instruction on 2026-10-11. It implements only
`globSync(string, { onlyDirectories: true })`, consumed by the unchanged
`@next/eslint-plugin-next@16.3.8/dist/utils/get-root-dirs.js`. The consumer already
normalizes Windows separators and expands arrays one string at a time. Application
paper input does not feed this setting; repository/configuration input can.

The frontend devDependency uses the **fast-glob module key**, with this explicit
local package identity, and a version-scoped `$fast-glob` override. `.npmrc` sets
npm's documented `install-links=true`: pack the local file dependency instead of
linking it. This avoids npm 11.16's broken plugin-relative file-link resolution.
The actual lock entry names the adapter and its portable local path. Normal
`npm ci` must pass in a fresh checkout; no postinstall patch, registry publication,
audit filtering, forged patched version, vulnerable parser or vendor fork exists.

Dependency: exact tinyglobby 0.2.17 (MIT), using the existing fdir 6.5.0 and
picomatch 4.0.7 (MIT) graph. No upstream source is copied. Node >=24 is required
for the pinned CommonJS consumer to require synchronous ESM; no top-level await.
CI pins Node 24.18.0. Render's actual Node/service settings remain unverified.

Literal directories retain their input spelling (including ./, ../ and a final
slash) and never expand into descendants. Files return no directory match. Dynamic
patterns disable tinyglobby's directory expansion, select absolute output for
absolute input, strip directory-only output slashes, and translate a final **
segment to **/* so its parent is excluded as in fast-glob. Dot directories are
excluded unless explicitly named; symlink directories are followed.

Dynamic results are deduplicated and sorted by JavaScript string ordering.
This intentionally differs from fast-glob's filesystem/group traversal order.
Committed baseline values retain the old order; tests compare every path and the
new deterministic order, and separately require **identical ordered diagnostics**
from the actual Next rule over literal, wildcard, recursive, brace and array roots.
The application has no explicit next.rootDir setting. This ordering difference
requires the fresh independent review; this adapter is not a general substitute.

Unsupported calls throw clear errors: pattern arrays (Next handles root arrays),
negative include/exclude patterns, ignore/cwd/dot/fs/async/stream/object options,
brace ranges, nested extglobs, literal parentheses, malformed balanced syntax,
empty/non-string/NUL inputs. Escaped glob syntax is not supported: the pinned
Next helper converts every backslash to a separator. It cannot encode escaped
metacharacters either. Broad fast-glob file matching is outside this contract.

Before parser entry, iterative validation limits length to 4096, brace nesting to
32, glob operators to 64 and conservative alternative product to 256. Nested
extglobs are rejected. Child-process tests bound malicious inputs to three seconds.
These are explicit tooling restrictions, not a claim of universal regex or
filesystem resource safety; valid broad globs can still traverse many directories.
Filesystem errors other than missing/non-directory literal paths propagate.

Maintenance: built-in node:test checks the sole locked consumer, pinned version,
official helper/rule hashes, actual installed identity and source bytes. Any Next
upgrade/new fast-glob consumer requires fresh compatibility/security review. Remove
the adapter and override together only after a compatible upstream fix and all
audit/equivalence/regression gates pass. ESLint 9's existing EOL remains a separate
maintenance limitation; this task does not migrate or downgrade ESLint.

Rollback by an ordinary revert of the A2 implementation commits; retain the earlier
Next/sharp/source-map-js patches and history. Revalidate installation and tests.
Rollback restores five HIGH entries, so remains BLOCKED, never security accepted.
No merge/deployment or risk exception is authorized by this implementation.
