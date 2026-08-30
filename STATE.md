# Project State

> **Read first, every session.** A snapshot of what is true now, not a log. Rewrite in place; delete
> superseded text rather than annotating it. Budget: **150 lines**. Why things are this way: `decisions/`.
> Every measured number: `registers/measurements.md`. Durable rules: `docs/engineering/`.

Last updated: 2026-08-29 22:36

## Current position

The engine is **complete and audited**. All 22 hardening gaps are closed across four waves, and the viewer
finish landed with wave D.

The remaining gap is **reach, not capability**: the pipeline can only be driven by `npm run` scripts from
inside a workspace. Four forward paths are scoped (component reuse, packaged CLI, MCP server, hosted
deployment), with scope, blockers and open decisions in `registers/workstreams.md`.

**Execution shape (owner, 2026-08-23): all workstreams run in parallel, in separate worktrees.** The
"which path first" question is closed; do not re-propose an ordering.

**Current focus (owner, 2026-08-29): the viewer is delegated; everything else is on hold.** The CLI, seams,
MCP and hosted tracks are paused mid-planning, not cancelled, and their decisions all stand. The
viewer-component question that was parked is now open, with the delegate cleared to build new components
rather than only reuse vendored ones.

**Development happens in the public `RepoHIVE` repository.** Its replay is **complete**: 135 commits, `main`
at `dbcdc14`, all eight feature branches pushed (verified 2026-08-29 22:36). The older archive repo is
frozen; do not commit engine work there.

## Verified state

Measured 2026-08-22 on Node v20.19.0 / npm 10.8.2, in the archive checkout. `npm run build` **clean**.
Determinism **holds**: `group` digest `f30c7b3d…` identical across 3 runs, matching the recorded value.
Engine tests **core 153/153**, **parser 180/181**. Root `npm test` **exits 1, unusable as a gate**.
Verify the engine by listing its test files explicitly: `docs/engineering/verification.md` has the command,
the known failures, and which gates run from which checkout. All figures: `registers/measurements.md`.

## Measured reality, headlines only

Every figure, its date, and what it does not license you to claim: **`registers/measurements.md`**. Only the
traps an agent can fall into without opening it are repeated here.

**Pipeline is ~57 s cold and ~14 s warm. Always quote both.** Cold is the first read of just-written files,
which is what a user hits after cloning, so no warm figure belongs in a README unlabelled. **The parser is
not slow and needs no optimization**; a warm parse is already ~85% CPU. Nothing is implemented.

**Group provenance is emitted in `nodes.json`, not `hierarchy.json`** (verified 2026-08-29), which holds only
the tree. The `Hierarchy` object from `parseIndex()` is an **assembled** view across all five files, so
`leafAttributes`, `leafEdges` and `crossGroupEdges` are properties of that object, not keys in any file on
disk. A consumer told "groups carry `regionId`" will look in the wrong file.

**`sample-java-project` has 0/8 provenance coverage: its `index/` is stale and predates Gap 12.** Re-index
before demoing it. **`broadleaf`** (29,190 nodes, 502 regions) is the load-bearing evidence: real, large,
multi-module Java where the adaptive preserve branch actually fires.

**The viewer has 3 real surfaces out of 51 pages**, deliberately gated in the nav. **The vendored IA is not a
backlog**, and **no fabricated or fixture data reaches the running app**.

## Done

- **Phase 1, parser** (`shared`, `parser`): Tree-Sitter Java to `graph.json` plus determinism harness.
- **Phase 2, grouping** (`core`): adaptive preserve-vs-reconstruct to the five-file `index/` plus blast
  radius, covering all 33 spec correctness properties.
- **Phase 3, viewer** (`web`, `ui`, `types`, `api-client`): three real surfaces, gated in the nav.
- **Engine hardening waves A-D**: 22 gaps closed. See `decisions/`.
- **Group naming Tier 1**: engine provenance plus `zoom-labels.ts` label composition. Tier 2 remains.
- **Public repo replay** (2026-08-29): complete, 135 commits.
- **Documentation drift audit** (2026-08-29): 62 claims checked, **39 verified, 15 wrong, 8 unverifiable**.
  Corrections are folded into `docs/engineering/`; the record is `registers/drift-report.md`.

## In progress

- **Viewer work delegated** (2026-08-29). The brief covers running it, the verified shape of all five
  `index/` files, 12 zero-change surfaces, the one additive field, what not to attempt, and total design
  authority over everything visual. **Nothing in it is implemented.**
- **Everything else is on hold** mid-planning, by owner instruction. All recorded decisions stand.
- **Forward-path documents are not yet ported.** The CLI plan, seams design, performance analysis and viewer
  brief live only in the frozen archive, and are needed before the CLI or seams work resumes. **One is
  knowingly contested:** the CLI plan says `index` skips parse when `graph.json` is current, while the seams
  design argues v1 should always parse, since a wrong skip silently serves a stale index. Resolve on porting,
  and drop `parseSkipped` from the result shape if always-parse wins.

## Next up

All of these run concurrently in separate worktrees. Scope, blockers and the parallelism map are in
`registers/workstreams.md`; titles only here so the two cannot drift.

- [ ] **Port the forward-path documents** out of the archive. Blocks the CLI and seams tracks.
- [ ] **Packaged CLI**, on hold. Write the requirements spec before any code. Node test-script fix first.
- [ ] **Foundation seams**, on hold. Own worktree, own design spec. **Does not block the CLI.**
- [ ] **MCP server**: read-only v1 needs no new engine exports and does not depend on the CLI.
- [ ] **Hosted deployment**: needs all four foundation seams.
- [ ] **More real-repo validation**: collides with nothing, and the only candidate that could surface a real
      problem. Calibration rests on two real fixtures.
- [ ] **Credibility pass**: re-index the stale fixture, fix the landing-page zeros, drop 2 dead controls.

**De-conflict before anyone writes orchestration code:** both the CLI and the hosted path need a
parse-then-group layer, so define that package's *interface* first (one file of type signatures) and have both
worktrees code against it. Otherwise parallel work produces two incompatible implementations.

**Open owner decisions live in `registers/workstreams.md`**, grouped by what each blocks: the authoritative
list. This file keeps no second copy, because the duplicate drifted incomplete on 2026-08-23.

## Open questions and known risks

- **The engine test script works on neither Node version.** The glob form needs Node 21+; the bare `dist/`
  form is silently vacuous on 21+. **No green-suite claim from `npm test` is trustworthy** until fixed. And
  **nothing enforces a Node version**: only `packages/web` declares `engines`, so the trap is reachable by
  default on a fresh machine. Add a root `engines` plus `.nvmrc`.
- **Per-package no-emit scripts are named inconsistently**: `typecheck` in `shared`/`parser`/`core`,
  `type-check` in `api-client`/`types`/`ui`/`web`, and **no root script runs the second group**, so those
  four are unchecked in any aggregate run.
- **Three pre-existing test failures**, none in engine logic: a Windows-vs-POSIX filename assumption in
  `parser/source-collector.test.ts`; a vendored `types` test importing `tests/fixtures/node_ids.json`, which
  **does not exist**; and flaky render-budget tests in `ui`.
- **Dependency major skew**: `recharts` `^2.13.0` in `web` against `^3.8.1` in `ui`. Nothing depends on it.
- **Index write is not fully atomic**: five same-directory renames, so a mid-promotion failure leaves a
  mixture. Inherent to the design; a directory swap was rejected for its no-index window.
- **Viewer route handlers are unauthenticated**, intended for localhost only; authentication blocks any
  non-local deployment. The AGPL section 13 concern beside it is **resolved**: everything ships from the public
  repo (owner, 2026-08-23), so the engine being served is intended. **Do not cite AGPL as a constraint.**
- **Gap 1b (method-call edges)** is deferred by design, not closed. `methodCallFrequency` is not fully
  populated from real call sites.
- **The preserve/reconstruct split moves with parser signal, not only with repository quality.** Enriching the
  parser pushes regions toward preserve with no repository changing (mechanism and instance:
  `registers/measurements.md`). Never quote a split without naming the signal level it was taken at.
- **The viewer's landing page reads as measured when it is not.** `web/src/app/page.tsx` swallows failed
  fetches via `Promise.allSettled` and renders `Total Pages 0` / `Fresh Pages 0` / `Stale Pages 0` in metric
  cards. Nothing is fabricated, but zeros in a metric card read as a measurement on the first demo screen.
- **The code-graph-MCP space is crowded**, so an MCP server is distribution, not differentiation.
- **Command names** `parse` / `group` / `view` are still placeholders.
- **Documentation drift is systemic, not incidental.** 15 wrong claims out of 62, all the same shape: prose
  asserting facts that live in `package.json` or source, with nothing checking them. These are the files an
  agent reads first, so a stale claim misdirects. **If a doc disagrees with the code, the code wins.**
- **The archive repository is public** and holds the full working registers. Owner-owned and deliberately out
  of scope (2026-08-23), so not a blocker, but a live exposure, recorded rather than dropped.

## Reference registers

Large working documents, not context. Load only when working the item each describes.

| File | Contents |
|------|----------|
| `registers/measurements.md` | **Every measured number**, with its date and what it does not license |
| `registers/drift-report.md` | The 2026-08-29 audit: 62 claims, what was wrong, what is unverifiable |

**Four registers are not ported yet** and exist only in the frozen archive: the workstream register (four
forward paths, blockers, open owner decisions), the 22-gap register, the Fix 3-22 designs, and the edge-case
audit. Every pointer to `registers/workstreams.md` above is dead until that port lands, so treat the open
decisions it holds as unavailable rather than empty.
