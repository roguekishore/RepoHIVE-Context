---
date: 2026-09-13
slug: cli-published-contract
title: The repohive CLI published contract as implemented
status: current
superseded_by: null
supersedes: null
summary: Four commands over the engine package, .repohive/ layout, a schemaVersioned --json document as primary output, and a three-code exit contract that turns on whether anything was attempted
corrected: false
---

# The repohive CLI published contract as implemented

Built 2026-09-13 on `wip/cli` (commits `928e745`, `3f1ffcd`, `df9a169`, `b6def3c`, `513f8a4`,
`390fa13`; local, unmerged, owner pushes). The branch is forked from the engine's API-frozen
`5f0e602`.

This decision exists because `registers/cli.md` § 8 is right: the on-disk layout, the command and flag
names, the `--json` shape and the exit codes are the parts that **cannot** be retrofitted once anyone
writes automation against them. Everything below is now implemented, so this is the record of what a
future version is bound by.

## What was built

`packages/cli`, npm name `repohive`, `bin: { repohive: ./dist/cli.js }`, depending on
`@repohive/shared`, `@repohive/parser`, `@repohive/core` and `@repohive/engine` rather than bundling
them. Still `private: true` at `0.0.0`; publishing is a separate owner-driven change. `index` is
implemented over the engine package's `indexProject`, which is why orchestration lives in
`@repohive/engine` and not here: the MCP server must never import a package called "cli".

Both recorded blockers are fixed. Relative paths resolve against `process.cwd()`, never `INIT_CWD`,
which was an npm-script artifact. The bin entry has a shebang and calls `main` unconditionally; the old
`if (process.argv[1]?.endsWith("group-cli.js"))` self-execution guard would never fire under a bin
shim. `main(argv, io)` stays exported so every command is testable without spawning a process.

`group` moved out of `packages/core` and `parse` moved out of `packages/parser`, which is what removes
the CLI surface from the engine packages. `group` was an extraction and kept its behaviour: the full
flag surface, every value through core's `validateConfig`, unknown-flag and extra-positional
rejection. `parse` was **hardened** to that same standard, since it was materially weaker: it had
ad-hoc argument scanning, no unknown-flag rejection, and a default target of
`fixtures/sample-java-project` resolved relative to `dist/`. That default is gone. Its absence is the
point: demo behaviour must not ship, and a missing directory is now a usage error.

## The contract

**Commands: `index` / `parse` / `group` / `view`.** Names were already final. `describe` stays
deferred.

**`index` always parses.** There is no skip-when-current in v1, per the decision recorded in
`2026-09-13-engine-orchestration-package.md`, and the result reports `parseSkipped: false` so the
field is already the right shape for when skipping lands.

**`view` is recognized and exits 2 with "ships in a later release"**, rather than being omitted from
dispatch. Answering `unknown command: view` would imply the name is undecided and send someone hunting
for a different spelling of a command that simply is not here yet. The name is final; only the viewer
is Stage 2.

**Layout `.repohive/` containing `graph.json` and `index/`.** `--out <dir>` always names *the
directory this command writes into*, which is the one reading that stays coherent across three
commands with different outputs. `index` and `parse` default to `<dir>/.repohive`. `group` defaults to
a sibling `index/` of the graph file it read, so grouping `.repohive/graph.json` writes
`.repohive/index/` untold, and a directory argument resolves to `<dir>/.repohive/graph.json` when that
exists and `<dir>/graph.json` otherwise, so `repohive parse X && repohive group X` composes. `index/`
stays separate and untouched because it is the published contract that MCP, the hosted service and
third-party tooling read.

**Exit codes, and the test that decides them.** `0` success, `1` the request ran and a stage reported
a structured error, `2` the command line could not be turned into a request. **The test is whether
anything was attempted.** So a path that exists but cannot be parsed is `1` and carries the parser's
own error, while a path that does not exist at all is `2` in every command, and nothing is written or
created. `2` also covers an unknown command, an unknown option, a missing option value, an extra
positional, and a command not in this release.

**Streams.** stdout carries the result, stderr carries diagnostics and human error prose and never any
part of the result. Under `--json` a command writes exactly one JSON document to stdout and nothing to
stderr, **on success and on failure alike**, so the failure document is the result and
`repohive index . --json | jq .ok` is always well formed. `--version` and `--help` are the deliberate
exception: they print prose even under `--json`, because they answer a question about the tool rather
than producing a result.

**`--json` is the primary output and prose is a rendering of it**, never the reverse. Every document
carries `schemaVersion`, `command`, and an `ok` discriminant; failures add `stage` plus the stage's
structured errors. `schemaVersion` is bumped only when a field is renamed, removed, or changes
meaning, so **consumers must ignore fields they do not know**. Optional fields are **omitted** when the
underlying stage omits them rather than defaulted to zero, matching the JSON contract's existing
field-omission semantics. The document is explicitly **not byte-reproducible**: it carries measured
durations, so two runs over identical input differ. The artifacts under `.repohive/` are the
deterministic output; the document describes a run.

Honesty carried into the surface: `preserveCount` and `reconstructCount` are documented as raw
decision counts that include degenerate regions, pointing at `index/metadata.json` for per-region
detail, so the CLI does not become a new way to quote a raw preserve/reconstruct split.

## Verified by the orchestrator, not by agent report

Node v26.4.0, Linux, after a clean rebuild. Root, engine and CLI builds exit 0. CLI tests 39 across
four chained per-file invocations (the chaining is deliberate: a single `node --test` call with
several files silently drops missing ones on Node 26). Core **141/141** and parser **181/181** after
the moves, with no stale compiled artifacts left behind; the arithmetic is core 153 - 12 moved = 141,
and parser is unchanged at 181 because `parse-cli.ts` had **no tests at all**, which is the same
weakness that made hardening necessary. Net test coverage rose by 27.

End to end on the built binary: `index --json` exits 0 and writes `.repohive/graph.json` plus a
five-file `index/`; two consecutive runs produce a **byte-identical** `index/`; `graph.json` hashes
`a603b667...`, matching the recorded 2026-08-16 baseline. `npm run demo:group-determinism` still runs
from the root and reports DETERMINISTIC with digest `f30c7b3d...`, matching the recorded 2026-08-22
baseline: the extraction did not disturb the demo gate, and core's demo scripts never imported
`group-cli`. Exit codes confirmed live: unknown flag 2, missing directory argument 2, unknown command
2, nonexistent path 2, `view` 2, `--help` 0, and a real runtime failure (a directory containing no
Java files) 1 with a structured `stage: "parse"` failure document on stdout.

## Known wart

**The root manifest and the CLI package are both named `repohive`.** npm resolves
`--workspace repohive` to the workspace rather than the root, verified by running it, so this works
today. It is still ambiguous to a reader and depends on npm's resolution order. Renaming the root to
something like `repohive-monorepo` costs nothing (it is private and unpublished) and should happen
before the first publish.
