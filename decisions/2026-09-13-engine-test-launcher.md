---
date: 2026-09-13
slug: engine-test-launcher
title: Engine tests run through an explicit file-enumerating launcher
status: current
superseded_by: null
supersedes: null
summary: Engine test scripts call scripts/run-node-tests.mjs, which enumerates dist/*.test.js, fails on zero files, and spawns node --test with the explicit list
corrected: false
---

# Engine tests run through an explicit file-enumerating launcher

Decided 2026-09-13, implemented on `wip/test-fix` (commits `73093ee`, `3818b82`, `2fa28ea`; local,
unmerged, owner pushes).

## Decision

Any package whose tests are compiled to `dist/` and run with the node test runner declares:

```
"test": "node ../../scripts/run-node-tests.mjs"
```

`scripts/run-node-tests.mjs` (repo root, plain .mjs, dependency-free, node: builtins only) is the one
test entry mechanism for engine packages, and the default for future packages of the same shape. It:

1. enumerates `<dir>/*.test.js` (default `dir` = `dist`, non-recursive) with `readdirSync` and sorts
   the list, so the file set and run order depend on the filesystem contents, not on shell glob
   expansion or Node version;
2. **exits 1 with a clear stderr message when zero test files are found** (including missing or
   unreadable dir). This guard is load-bearing: it is what makes a vacuous green run impossible;
3. spawns `process.execPath --test <files...>` with stdio inherited and propagates the child's exit
   status (signal death and spawn failure also exit 1);
4. forwards `-`-prefixed args to `node --test` in `--flag=value` form
   (`npm test -- --test-name-pattern=x`).

## Why this mechanism

The previous script `node --test dist/*.test.js` had no correct form across Node versions. Measured
2026-09-13 in the public repo worktree: on Node v26.4.0 the bare-directory alternative
`node --test dist/` reported exactly one passing test named `dist` and exited 0 against 17 real test
files (the directory resolves to `dist/index.js`, and a file with no test registrations counts as one
passing test); on Node v18.19.1 the unexpanded glob failed with `Could not find ... dist/*.test.js`,
exit 1. Node 20 and 21-25 were reasoned from documented behaviour (runner glob support landed in 21),
not measured. Explicit enumeration removes every version- and shell-dependent step.

Spawning `node --test` was chosen over the `node:test` `run()` API deliberately: `run()`'s options and
reporter surface changed across 18-22, while `node --test file1 file2` semantics and output have been
stable since 18, and the spawn preserves the exact CLI output format developers already read. No new
dependencies; AGPL question does not arise.

## Constraints this binds

- Future engine-shaped packages reuse `scripts/run-node-tests.mjs` rather than writing a new test
  script form. If a package needs different enumeration (other dir, recursion, other extension), extend
  the launcher behind its existing argument contract; do not fork per-package variants.
- Do not switch any test script back to `node --test dist/*.test.js` or `node --test dist/`; both are
  recorded traps (`docs/engineering/verification.md` keeps the history and the measured evidence).
- The zero-file guard must survive any future edit to the launcher. A test entry mechanism that can
  pass with zero tests executed is a regression of this decision, not a refactor.
- Root `package.json` `engines` (`>=20`) and `.nvmrc` (`20`) record the supported floor. Advisory, not
  enforcement: npm warns without `engine-strict`. Raising the floor is a decision, not a cleanup.

## Verified / not verified at decision time

Verified on Node v26.4.0 Linux: core 153/153 (17 files), parser 181/181 (11 files, the known
Windows-only source-collector failure passes on Linux), guard exits 1 on missing/empty/test-less dist,
failing tests propagate exit 1. Verified on v18.19.1: core 153/153 via the launcher. Independently
re-verified by the orchestrator: core 153/153 via `npm test`, guard exit 1 on missing and empty dirs.
Not verified: Node 20/21-25 (reasoned, bracketed by the measured 18 and 26), and Windows shells
(reasoned: the launcher hands node an explicit file list, so the cmd.exe/PowerShell glob difference no
longer participates; the historical parser suite ran 180/181 on Windows Node 20 via explicit listing,
recorded 2026-08-22).

## Follow-ups owed at merge time

Two docs outside this change's scope still describe the pre-fix state and stay accurate on `main`
until `wip/test-fix` merges; correct both in the merge or immediately after: the `AGENTS.md`
Environment line saying only `packages/web` declares `engines` and that the engine test scripts
misbehave on Node 21+, and the `docs/engineering/conventions.md` line citing the engine test script as
a live false-green example.
