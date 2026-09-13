---
date: 2026-09-13
slug: engine-orchestration-package
title: The @repohive/engine pipeline orchestration package and its public API
status: current
superseded_by: null
supersedes: null
summary: One package, one call (indexProject) runs parse then group into .repohive/; v1 always parses; stage-discriminated result; progress and concurrency defined now, coarse/inert until the follow-up wiring.
corrected: true
---

# The @repohive/engine pipeline orchestration package and its public API

## Context

Both the packaged CLI and the hosted path need a parse->group layer, and
`registers/seams.md` § 6 required its interface to be defined before either
worktree writes orchestration code. `registers/seams.md` § 9 carried a proposed
signature with five embedded decisions, awaiting an owner call. This decision
records what was actually built on `wip/engine` (API-stable at
`5f0e60207e9d02719b216b0d0ee197394270d67b`), which of § 9's proposals were
adopted, adapted, or rejected, and the owner overrides that bound the design.

## Decided

1. **Package: `packages/engine`, npm `@repohive/engine` (owner override).**
   Overrides § 9's `@repohive/pipeline` proposal, which argued "engine" already
   names parser+core+shared collectively. Terminology is therefore defined and
   used consistently from now on: **"the engine packages"** = `shared`, `parser`,
   `core`, `engine` (the engine side of the boundary); **"the engine orchestration
   package"** = `@repohive/engine` alone. Boundary rule unchanged: engine-side
   packages import nothing from `cli`/`web`/`ui`/`api-client`/`types`; the
   orchestration package may import `shared`, `parser`, `core` and is imported by
   the CLI, the MCP server, and the hosted service.
2. **Public API: one async call.**
   `indexProject(options, deps = defaultEngineDeps()): Promise<EngineResult>` -
   the house DI pattern. Artifact layout (decided elsewhere, followed here):
   default output root `<projectDirectory>/.repohive/` containing `graph.json` and
   `index/` (core's five-file contract); `outputDirectory` overrides the root;
   `view/` is not engine scope. The engine composes the two deterministic stages
   without adding ordering or nondeterminism; it writes no artifact of its own.
3. **v1 always parses (resolves the cli.md § 3 CONTESTED line).**
   Skip-when-current is the snapshot-id seam; mtime is fragile; a wrong skip
   silently serves a stale index, which is far worse than a redundant warm ~7 s
   parse. `parseSkipped: boolean` is KEPT in the result (owner-fixed), always
   `false` in v1, so the shape is already correct for the snapshot-id era.
   `registers/cli.md` § 3 (line + blockquote), `registers/workstreams.md`'s
   command-surface copy, and STATE.md's contested-document bullet are corrected in
   the same change as this decision; the earlier "drop `parseSkipped`" clause is
   superseded by "keep it, always false".
4. **In-memory graph handoff: adopted as a designed-in upgrade; parser change
   deferred.** The engine's parse dependency returns
   `EngineParseSuccess = ParseSuccess & { graph?: RawDependencyGraph }`; v1 reads
   `graph.json` back via core's `readGraphFile`, and the read-back disappears
   automatically (no engine signature change, no `defaultEngineDeps` change) once
   the parser's additive `ParseSuccess.graph?` lands in the follow-up run.
   `graph.json` is always written regardless - it is the committed layout and the
   `group`-only sweep input.
5. **Stage-discriminated result: adopted; the two existing `Result` types stay.**
   `EngineResult` = success | `{ stage: "engine"; error: EngineError }` |
   `{ stage: "parse"; errors: readonly ParseError[] }` |
   `{ stage: "group"; error: GroupingError; graphPath: string }`. Adaptations from
   the § 9 sketch: no separate "serialize" stage (core composes group+serialize;
   the owner-fixed `durationMs` names exactly parse/group/total; a serialize
   failure is a group-stage `WRITE_FAILED`); a third `"engine"` arm exists from
   day one (option validation, output-root preparation, internal backstop) and is
   the arm cloud-source validation will reuse, so no future failure arm is needed;
   the group arm names the written `graph.json`.
6. **Progress: shape defined now, coarse events in v1, callback in options.**
   `EngineProgressEvent { stage: "parse" | "group"; kind: "start" | "complete" |
   "progress"; completed?; total? }` with `"progress"` reserved and unemitted in
   v1, so per-file granularity for hosted SSE lands as pure behavior with zero
   type change. The callback is `EngineOptions.onProgress` rather than a third
   parameter: the house signature stays `fn(options, deps)`, and the parser
   already threads callbacks through options objects (collector's
   `onExcludedDirectory` / `onUnsupportedPath`).
7. **`concurrency?: number` defined and validated now, inert until wired.**
   Parse-stage read concurrency; internal knob, not a v1 CLI flag; integer >= 1
   enforced today so nonsense fails before it can become load-bearing; wired to
   the parser prefetch in the follow-up run with no public signature change.
8. **Source seam (hard constraint): additive path to cloud sources.**
   v1 keeps `projectDirectory: string` required (matches `ParseOptions`; zero
   ceremony for the CLI). Cloud lands by relaxing it to optional and adding
   `source?: EngineSource` (a discriminated union designed when its real variants
   are known), with exactly-one-of enforced at run time through the existing
   `INVALID_OPTIONS` arm. This is non-breaking because `EngineOptions` is a
   caller-constructed options bag: relaxing required->optional plus adding
   optional fields keeps every existing call site compiling and behaving
   identically, and touches no other exported type. A one-variant union today was
   rejected as speculative structure that taxes every v1 caller to protect a
   shape we cannot yet design correctly.
9. **Failure/cleanup semantics are the stages' own, documented not redesigned.**
   Parse failure: no partial `graph.json`, prior file intact (parser R10). Group
   failure: `graph.json` kept deliberately; core's serializer stages all five
   files and promotes via five same-directory renames, so an existing `index/`
   survives everything except a failure inside that five-rename window (recorded,
   accepted bound). Engine-specific guard: the output root is created only when
   `projectDirectory` is a real directory, so a bad input cannot fabricate
   directories or flip the parser's `path-not-found` into `no-java-files`.
   Timeouts/cancellation stay hosted-service concerns per the 2026-08-22
   live-indexing decision.
10. **Determinism.** Durations are measured with `performance.now` (injectable
    `now()` dep) and exist only on the returned result; no timing, wall clock, or
    randomness exists anywhere in `packages/engine/src` (grep-verified), and the
    integration suite byte-compares two full runs and matches the recorded
    2026-08-22 group digest `f30c7b3d...` and 2026-08-16 parse digest
    `a603b667...` exactly.
11. **Test-script form (measured this run, Node 26.4.0).** A single `node --test`
    invocation with several listed files silently drops missing ones and exits 0
    when at least one resolves; only all-missing exits 1. The engine unit script
    therefore chains one invocation per file with `&&` (each is loud on its own
    missing file); integration is a separate env-guarded script that skips with a
    message when the git-ignored fixture is absent. The cross-package test-script
    fix on the other branch should account for this partial-silent-drop behavior.

## Not in this change (follow-up run, same branch)

- Parser-side `ParseSuccess.graph?` population (activates the in-memory handoff).
- Parser prefetch wiring for `concurrency` (turns the inert knob live; update its
  doc comment and README in the same change).
- Optional: core exports `validateConfig` so the engine can pre-flight grouping
  config before paying for a parse.
- Root-script wiring for the engine package (owner-merge follow-up; the root
  `build` script deliberately still reads `tsc -b packages/parser packages/core`).

After `5f0e60207e9d02719b216b0d0ee197394270d67b` the public signatures are frozen
for the CLI agent; the follow-up must be additive-optional only, ideally nothing.

## Corrections since

**2026-09-13, run 2 on the same branch (`fba6061`, `e3eedd6`, `d00bf6d`, `d64bf1b`).** The two deferred
items in "Not in this change" are now done, and one characterization there was wrong. The rest of this
decision stands unchanged, and **no public engine signature moved** (verified by diffing the exported
sources: `index.ts` and `errors.ts` changed only in doc comments, and `orchestrator.ts` gained one
implementation line forwarding `concurrency`).

- **Decision 4 is now live, and "parser change deferred" is retracted.** `ParseSuccess` carries an
  additive optional `graph?: RawDependencyGraph`. **It is populated by the serializer, not the
  orchestrator** - this was the run's only real trap. Only the serializer holds the canonical document
  (normalized, endpoint-swept, sorted, and in emitted property order); the orchestrator's `nodes`/`edges`
  are in extraction order with un-normalized fields, so handing those back would have let the in-memory
  and on-disk paths diverge silently. `d00bf6d` closed a residual gap the proof run exposed, where
  `normalizeNode` inserted `directoryPath` before `packagePath` while the stringifier emits the reverse:
  deep-equal but not byte-equal. `readGraph` is no longer called on the default pipeline; the read-back
  branch remains for a `parse` dependency that returns no graph, and `graph.json` is still always written.
- **Decision 7 is now live, and "inert until wired" is retracted.** `ParseOptions` gained an additive
  optional `concurrency`, and a prefetch step between collect and extract reads the collected files into a
  path-keyed map, at most `concurrency` at a time, default a fixed **16** rather than anything derived
  from `os.cpus().length` (the bottleneck is per-file read latency, not compute, and the measured curve is
  flat past the knee). Determinism stays **structural**: the `AstExtractor` interface, `extract()`, the
  extraction loop and the canonical order it walks are all unchanged, so neither the concurrency value nor
  read-completion order can reach an artifact. A prefetch read failure is deliberately swallowed and left
  to surface in the extractor, preserving both the exact `file-unreadable` shape and its canonical
  position.
- **Decision 10 gains a stronger proof.** The fixture digests were re-confirmed after both changes and
  additionally **across read concurrencies**: default 16 and `concurrency: 1` produce byte-identical
  `graph.json` and index files, both matching the recorded `a603b667...` and `f30c7b3d...`. This
  invariance is now asserted by the engine integration suite rather than by a one-off script.
- **One non-additive parser type change, source-compatible.** `ParseDeps.createExtractor` went from
  `() => Promise<AstExtractor>` to taking a `readFile` argument. It is unavoidable given the recorded
  prefetch design, and existing zero-argument stubs still satisfy it because a function of fewer
  parameters is assignable to one of more. No engine export references `ParseDeps`.
- **The `validateConfig` pre-flight was NOT the cheap additive follow-up recorded above.** It was
  attempted and skipped deliberately: the failure has no clean home, because `INVALID_OPTIONS` with field
  `"grouping"` would flatten core's structured field paths into free text, so the same user mistake would
  report a different code and a coarser field depending only on when it was caught. Doing it properly
  needs a dedicated `INVALID_GROUPING_CONFIG` arm, which is a change to the result union and therefore
  belongs in a deliberate version window, not a follow-up run.
- **The prefetch's cold-path win is unmeasured.** The 5-file fixture cannot show it and no cold
  multi-thousand-file corpus was present. The benefit remains a projection from the recorded 2026-08-27
  figures, not a result.

## Verified at decision time

Node v26.4.0, Linux, `wip/engine` worktree: engine workspace build exit 0
(re-verified independently by the orchestrator from a wiped `dist/`); root build
exit 0; engine tests 28/28 unit + 2/2 integration; core 153/153; parser 181/181
(the known Windows-only failure passes on Linux); two full runs byte-identical
with both recorded digests matched exactly (4 regions, 38 hierarchy nodes,
depth 4). Not run: root `npm test` aggregate (recorded as unusable); broadleaf
smoke (fixture absent from the worktree).
