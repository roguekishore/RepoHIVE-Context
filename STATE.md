# Project State

> **Read first, every session.** A snapshot of what is true now, not a log. Rewrite in place; delete
> superseded text rather than annotating it. **Budget: 200 lines**, and see "Keeping this file short" at the
> foot. Why things are this way: `decisions/`. Every measured number: `registers/measurements.md`.
> Durable rules: `docs/engineering/`.

Last updated: 2026-09-13 13:03

## Current position

The engine is **complete and audited**, and as of 2026-09-13 the **reach gap is being closed in parallel**:
five `wip/*` branches in separate worktrees off `main` at `9b69a62`. Three have landed, two are in flight.

**Everything from 2026-09-13 is LOCAL and UNMERGED.** `git push` fails with 403 on this machine (the local
GitHub identity has no write access to `roguekishore/RepoHIVE`), so nothing has reached the remote. Pushing
and merging are owner operations; the branches are sitting in the worktrees.

The **viewer remains delegated** and the hosted track remains on hold. Development happens in the public
`RepoHIVE` repository; the older archive repo is frozen.

## Verified state

Measured **2026-09-13 on Node v26.4.0 / npm 11.17.0, Linux, in the public checkout** (the AGENTS.md-
prescribed Node 20 was not available; nothing misbehaved and both recorded digests reproduced exactly).
`npm run build` **clean**. Determinism **holds**: `group` digest `f30c7b3d…` and `parse` digest `a603b667…`
both reproduced, byte-identical across repeated runs, matching the recorded baselines.

Engine tests **core 153/153**, **parser 181/181** on `main` (the recorded 180/181 counts one Windows-only
POSIX-filename failure, which passes on Linux) and **190/190** on `wip/engine` after run 2 added prefetch
and handoff tests. Engine package **29/29 unit plus 4/4 integration**. MCP **27/27**. Viewer **web 51/51
across 8 files**, up from the recorded 20/20 across 5 as the phase-3 surfaces landed. Root `npm test`
**remains unusable as a gate** while the vendored `types` and `ui` failures stand. On `wip/cli`, core
reads **141/141** after 12 group-cli tests moved into the CLI's **39**; parser stays 181 because
`parse-cli.ts` had no tests at all. Net coverage rose by 27.

Historical figures and their dates: `registers/measurements.md`.

## Measured reality, headlines only

Every figure, its date, and what it does not license you to claim: **`registers/measurements.md`**. Only the
traps an agent can fall into without opening it are repeated here.

**Pipeline is ~57 s cold and ~14 s warm on broadleaf. Always quote both.** Cold is the first read of
just-written files, which is what a user hits after cloning. **The parser is not slow**; a warm parse is
already ~85% CPU. Fixture-scale timings (the 5-file sample indexes in ~30 ms) are **not extrapolatable**.

**Group provenance is emitted in `nodes.json`, not `hierarchy.json`**, which holds only the tree. The
`Hierarchy` object from `parseIndex()` is an **assembled** view across all five files, so `leafAttributes`,
`leafEdges` and `crossGroupEdges` are properties of that object, not keys in any file on disk.

**`sample-java-project` is freshly indexed** (2026-09-13): **8 of 8 group nodes carry `regionId` and
`ordinal`**, each joining to exactly one decision, and both digests match the recorded baselines. The old
"0/8, stale, predates Gap 12" warning is retired. Artifacts sit at
`fixtures/sample-java-project/{graph.json,index/}` (git-ignored) in the public checkout.
**`broadleaf`** (29,190 nodes, 502 regions) remains the load-bearing evidence and is **not present in these
worktrees**, so nothing here exercises the preserve branch or scale.

**The viewer has 7 reachable surfaces**, all gated through `nav-items.ts`. Our components live in
`ui/src/repohive/`, outside the vendored folders per the NOTICE rule. **The 26 dead vendored pages are still
unreachable and are not a backlog**, and **no fabricated or fixture data reaches the running app** (the
landing page reads real index stats and renders an explicit "index not on this machine" state instead of
zeros; re-verified 2026-09-13).

## Done

- **Engine phases 1-3 plus hardening waves A-D**, the **public repo replay** (135 commits), and the
  **documentation drift audit** (62 claims, 15 wrong; `registers/drift-report.md`). All 2026-08 or
  earlier; `decisions/` and git history carry the detail.
- **Engine test runner fixed** (2026-09-13, `wip/test-fix`): the glob script is replaced by
  `scripts/run-node-tests.mjs`, which enumerates `dist/*.test.js` and **exits 1 on zero test files**, so a
  vacuous green is impossible. The old false green was reproduced on v26 before the fix. Root `engines`
  (`>=20`) and `.nvmrc` added, advisory only. `decisions/2026-09-13-engine-test-launcher.md`.
- **Fixture credibility** (2026-09-13, `wip/credibility`, **zero commits, correctly**): the fixture was
  re-indexed and placed; the landing-page zeros and the two dead Knowledge Graph controls were confirmed
  already fixed on `main` (`b08812f`, `8091939`) with no residue, so nothing needed changing.
- **MCP server, read-only v1** (2026-09-13, `wip/mcp`): `packages/mcp`, six tools over one launch-fixed
  index, stdio. Decisions: `2026-09-13-mcp-v1-tool-surface.md`, `2026-09-13-mcp-sdk-zod-dependency.md`.
- **Engine orchestration package** (2026-09-13, `wip/engine`): `@repohive/engine`, API-frozen at
  `5f0e602`, then run 2 made the in-memory graph handoff and the read prefetch **live** (HEAD `d64bf1b`)
  without moving a public signature. `decisions/2026-09-13-engine-orchestration-package.md`, which carries
  a `Corrections since` section for run 2. The handoff is taken from the **serializer**, not the
  orchestrator, because only the serializer holds the canonical document.
- **Packaged CLI, Stage 1** (2026-09-13, `wip/cli`, forked from `5f0e602`): `packages/cli` with a real
  `bin`, `index` over the engine package, `group` extracted from core and `parse` extracted from the
  parser **and hardened** (its `fixtures/sample-java-project` default, resolved relative to `dist/`, is
  gone). `INIT_CWD` and the self-execution guard are both fixed. `--json` is the primary output.
  `decisions/2026-09-13-cli-published-contract.md`.

## In progress

- **All five streams have landed.** Nothing is in flight.
- **Phase 3 of the viewer is built but unshipped.** It exists only in the archive checkout on
  `fable-work-new`. Deciding how that work reaches the public repo is open.
- **Nothing from this session is pushed or merged.** Five local branches. Merge map, from read-only
  `git merge-tree` probes: **`wip/test-fix` against `wip/cli` conflicts in `packages/core/package.json`
  and `packages/parser/package.json`** (both edit the scripts block: test-fix rewrites the `test` line
  while the CLI removes the `parse`/`group` lines, so keep both edits). **`package-lock.json` conflicts
  among `wip/mcp`, `wip/engine` and `wip/cli`**, resolved by re-running `npm install`. Every other pair
  merges clean, including `docs/engineering/stack.md`, which two branches edit in different sections.
  `wip/cli` is forked from the engine's run-1 `5f0e602` and does **not** contain run 2, but merges clean
  against it.

## Next up

- [ ] **Owner: push and merge the five `wip/*` branches.** Merge follow-ups owed, all small: wire
      `packages/engine`, `packages/mcp` and `packages/cli` into the root `build`/`typecheck` scripts (root
      still reads `tsc -b packages/parser packages/core`); harmonize every new package's test script onto
      the launcher; correct the two now-stale doc lines (`AGENTS.md` Environment, `conventions.md`'s
      false-green example) that describe the pre-fix test script; **rename the root manifest** off
      `repohive` so it stops colliding with the CLI package of the same name.
- [ ] **Real-repo validation on broadleaf.** Now the highest-value unrun check: it is the only fixture where
      the preserve branch fires, and it validates the engine package, the MCP tools and the CLI at scale.
      Collides with nothing.
- [ ] **Hosted deployment**: needs all four foundation seams. Orchestration is now built, so three remain.
- [ ] **Viewer Stage 2** for the CLI: the single-file hierarchical viewer, ~300-500 KB.

**Open owner decisions live in `registers/workstreams.md`**, grouped by what each blocks: the authoritative
list. This file keeps no second copy, because the duplicate drifted incomplete on 2026-08-23.

## Open questions and known risks

- **43% of broadleaf's regions were never assessed, and they look maximally confident.** 216 of 502 score 0
  by rule, and **all 216 carry `decisionConfidence: 0.5`, the dataset maximum**, so any chart keyed on
  confidence presents unassessed regions as the most confident decisions in the run. There is no explicit
  flag; the rule is `score === 0 && cohesion === 0`. **Never quote a raw preserve/reconstruct split**: use
  assessed-only. `packages/mcp` now enforces this structurally (the split is unrepresentable except under an
  `assessed` key), which is a workaround for an **engine emission gap**: a future index version should carry
  the flag explicitly and supersede every consumer-side derivation.
- **The preserve/reconstruct split moves with parser signal, not only with repository quality.** Enriching
  the parser pushes regions toward preserve with no repository changing. Never quote a split without naming
  the signal level it was taken at.
- **Per-package no-emit scripts are named inconsistently**: `typecheck` in `shared`/`parser`/`core`,
  `type-check` in `api-client`/`types`/`ui`/`web`, and **no root script runs the second group**.
- **Three pre-existing test failures**, none in engine logic: a Windows-vs-POSIX filename assumption in
  `parser/source-collector.test.ts` (passes on Linux); a vendored `types` test importing
  `tests/fixtures/node_ids.json`, which **does not exist**; and flaky render-budget tests in `ui`.
- **One parser test failed once on `wip/engine` and never again.** Observed 2026-09-13 during
  orchestrator verification: a single run reported 189/190. It did not reproduce in **34 subsequent runs**,
  including repeated build-then-test cycles and runs under `ulimit -n` 128 and 64 (a file-descriptor
  hypothesis, since the new prefetch opens up to 16 concurrent reads; the system limit is ~1M, so
  exhaustion was never plausible). **The failing test was not identified** because that run's output was
  not captured. This is recorded rather than dismissed because an intermittent failure in freshly
  concurrent code is exactly the thing not to wave through. **Before this branch merges, run the parser
  suite in a loop with output captured** and either reproduce it or record that it did not recur.
- **The root manifest and the CLI package are both named `repohive`.** npm resolves
  `--workspace repohive` to the workspace rather than the root, verified by running it, so it works
  today, but it is ambiguous to a reader and rests on npm's resolution order. The root is private and
  unpublished, so renaming it is free; do it before the first publish.
- **The prefetch's cold-path win is unmeasured.** The 5-file fixture cannot show it and no cold
  multi-thousand-file corpus is present. It remains a projection from the recorded 2026-08-27 figures.
- **Node 20 and Windows are now unmeasured.** The 2026-09-13 runs were all Node v26.4.0 on Linux, bracketed
  by one v18.19.1 run. The test launcher removes the version- and shell-sensitive step by construction, but
  no Windows or Node 20 execution has happened since. Measure when such a machine is available.
- **A live dead control survives on the Flat baseline surface.** It renders an "Open file page" action
  linking to a vendored, nav-ungated route: the same disease as the two removed Knowledge Graph controls,
  but a different, pre-existing control. Established from source, not from a running browser.
- **Index write is not fully atomic**: five same-directory renames, so a mid-promotion failure leaves a
  mixture. Inherent to the design; a directory swap was rejected for its no-index window.
- **Viewer route handlers are unauthenticated**, intended for localhost only; authentication blocks any
  non-local deployment. **Do not cite AGPL as a constraint** — everything ships from the public repo.
- **Gap 1b (method-call edges)** is deferred by design, not closed. `methodCallFrequency` is not fully
  populated from real call sites.
- **Dependency major skew**: `recharts` `^2.13.0` in `web` against `^3.8.1` in `ui`. Nothing depends on it.
- **The code-graph-MCP space is crowded**, so an MCP server is distribution, not differentiation.
- **Documentation drift is systemic, not incidental.** 15 wrong claims out of 62, all the same shape: prose
  asserting facts that live in `package.json` or source, with nothing checking them. **If a doc disagrees
  with the code, the code wins.**
- **The archive repository is public** and holds the full working registers. Owner-owned and deliberately
  out of scope, so not a blocker, but a live exposure, recorded rather than dropped.

## Reference registers

Large working documents, not context. Load only when working the item each describes.

| File | Contents |
|------|----------|
| `registers/measurements.md` | **Every measured number**, with its date and what it does not license |
| `registers/workstreams.md` | The four forward paths: scope, blockers, dependency map, **open owner decisions** |
| `registers/cli.md` | Every CLI decision, command bodies, blockers, weight, versioning, plan |
| `registers/seams.md` | The four seams, what each blocks, why retrofitting is safe, the orchestration record |
| `registers/performance.md` | Pipeline performance: measurement history, root cause, the six options |
| `registers/viewer-handoff.md` | The viewer brief: index-file shapes, 12 zero-change surfaces, constraints |
| `registers/drift-report.md` | The 2026-08-29 audit: 62 claims, what was wrong, what is unverifiable |

**Three registers are still in the frozen archive**: the 22-gap register, the Fix 3-22 designs, and the
edge-case audit. They need a substantive rewrite rather than a scrub, so they are a later pass.

## Keeping this file short

The budget exists because this is the one file read unconditionally every session, so its length is a running
cost. Two sections grow on their own and are where the pressure always appears:

- **Done** gains an entry per completed phase and never loses one. Once something is finished and no longer
  shapes current work, cut it to a single line or drop it: `decisions/` and git history already hold it.
- **Open questions and known risks** accumulates. A risk that is recorded but no longer influences any
  decision belongs in a register, or should become a decision and leave.

**Detail belongs in a register, not here.** When a section starts carrying numbers, file lists, or
reproduction steps, that is the signal to move it and leave a pointer.
