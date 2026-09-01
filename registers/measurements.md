# Measurements

Every measured number this project relies on, with its date, the machine state it was taken under, and what
it does and does not license you to claim.

`STATE.md` carries only the headlines and points here. This file is the record. **Not bulk context**: open it
when a number matters, not to orient yourself.

Two rules govern everything below.

**Label every timing cold or warm.** They differ by roughly eight times on this codebase. Unlabelled figures
have produced wrong conclusions more than once, including a void set of figures still quoted for a week.

**A number is only as good as its run.** Every figure here names a date. If you cannot reproduce it, say so
rather than repeating it; a stale measurement asserted confidently is worse than an admitted gap.

## Gates, 2026-08-22

Node v20.19.0, npm 10.8.2, in the archive checkout.

| Gate | Result |
|------|--------|
| `npm run build` | clean |
| Determinism | holds: `group` digest `f30c7b3d…` identical across 3 runs, matches the recorded value |
| `core` tests | 153/153 |
| `parser` tests | 180/181. The one failure is `source-collector` test 124 |
| `api-client` tests | 50/50 |
| `web` tests | 20/20 |
| `types` tests | 2 suites fail, pre-existing, vendored |
| `ui` tests | 1 flaky, pre-existing, vendored |
| Root `npm test` | **exits 1.** Not usable as a gate as written |

The determinism digest is the single most load-bearing number here. If it moves, do not recapture it
silently: identify which field changed and why, record a decision, and update the digest in the same change.

## Fixtures

| Fixture | Scale | Nodes / edges | Regions | Split | Depth |
|---------|-------|---------------|---------|-------|------:|
| `sample-java-project` | 6 Java files | 29 / 6 | 4 | 0 preserved of 1 assessed | n/a |
| `jsoup` | single-module library | not recorded | 8 | 3 preserved of 7 assessed | n/a |
| `broadleaf` | mature multi-module | 29,190 / 14,325 | 502 | 38 preserved of 286 assessed | 6 |
| `vantage` | 158-file Spring Boot | 808 / 344 | 20 | 10 preserved of 17 assessed | n/a |

**`vantage` is absent from the machine** and was not re-created, so its figures are inherited from the
2026-08-22 record rather than re-measured. The viewer excludes it and says so. **`broadleaf` was re-cloned
from the public BroadleafCommerce repository and re-indexed 2026-08-30, and it reproduces the recorded numbers
exactly**: 2985 files, 502 regions, 216 degenerate, 38 preserved, depth 6.

The splits above are **assessed-only**, which is not how they were recorded before. The next section is why.

`broadleaf` is the load-bearing evidence: real, large, multi-module Java where the adaptive preserve branch
actually fires. It previously crashed `group` with `duplicate node identifier` until node identity was scoped
by source root.

**Calibration rests on two real fixtures.** That is the argument for more real-repo validation early, and the
reason the preserve/reconstruct split should not be quoted as a property of repository quality alone. See the
signal-sensitivity note below.

## Pipeline wall-clock

| Stage | Cold | Warm |
|-------|-----:|-----:|
| `parse` broadleaf (2985 files) | ~50 s | ~6-8 s |
| `group` broadleaf | not measured | ~6.5-9 s |
| **full pipeline** | **~57 s** | **~14 s** |

**Cold is the first read of just-written files**, which is exactly what a user hits after cloning. No warm
figure belongs in a README unlabelled.

Root cause of the gap is a **~15 ms per file first-access penalty**. Leading explanation is on-access
antivirus scanning; **this was never isolated**, so treat it as the best available account rather than a
finding. Warm I/O for all 2985 files is only 0.33 s.

Reads are latency-bound, so concurrency at x16 would cut cold parse by **6.8x**, to roughly 15 s. **Nothing
is implemented.** That figure is a projection from the latency measurement, not a measured result.

**A warm parse is about 85% CPU**, which sets the optimization ceiling. **The parser is not slow and needs no
optimization.**

**Void figures, never repeat them.** An earlier 2026-08-22 set was wrong by up to 9x: parse broadleaf 68.3 s,
group 11.3 s, parse vantage 4.7 s, pipeline ~80 s. The claim "parse dominates group 6:1" was an artifact of
timing a cold parse against a warm group. If you find these anywhere, they are stale.

## Index-file reality, verified 2026-08-29 on `vantage`

**Group provenance is emitted in `nodes.json`, not `hierarchy.json`.**

- **0 of 55** group nodes in `hierarchy.json` carry `regionId` or `ordinal`.
- **All 55** group entries in `nodes.json` do.

`hierarchy.json` holds only the tree: `id`, `kind`, `level`, `parentId`, `childIds`.

The `Hierarchy` object returned by `parseIndex()` is an **assembled** view across all five files.
`leafAttributes`, `leafEdges` and `crossGroupEdges` are properties of that object, **not keys in any file on
disk**. Any consumer told "groups carry `regionId`" will look in the wrong file without this.

Provenance coverage:

| Fixture | Covered | Note |
|---------|---------|------|
| `vantage` | 55/55 | full coverage |
| `broadleaf` | 1670/1698 | The 28 are repository-wrapping levels, which correspond to no region by design |
| `sample-java-project` | **0/8** | Its `index/` is **stale** and predates Gap 12. Re-index before demoing it |

## What `metadata.json` actually carries, read 2026-08-29

More than was recorded for a long time. Each `regionDecisions[]` entry has `regionId`, `action`,
**`automaticAction`**, **`cohesion`**, **`coupling`**, `score`, `decisionConfidence`, `userOverridden`,
`groupIds`.

Top level adds `perLevel[]` (level, groupNodeCount, leafNodeCount, crossGroupEdgeCount, leafEdgeCount),
`configuration` (seed 42, boundary 0.5, maxGroupSize 20, minPartitionThreshold 2, coefficients all 1) and
`metricWeights` (cohesion 0.4, coupling 0.4).

Two consequences worth knowing before proposing engine work:

- **Per-region `cohesion` and `coupling` make a decision scatter plottable with no engine change.**
- **`score` plus the boundary make a client-side sensitivity slider pure arithmetic.**

## Signal sensitivity, the trap in the numbers

**The preserve/reconstruct split moves with parser signal, not only with repository quality.**

Cohesion is raw strength-per-node, squash `k` is 1.0, coefficients are all 1, boundary is 0.5. So enriching
the parser or raising a coefficient pushes regions toward preserve **with no repository changing at all**.

Recorded instance: `vantage` went from **0/20 to 10/10 preserve** when its edge count went from 128 to 341
during wave A. Nothing about `vantage` changed.

Never present a split as a measurement of a codebase without naming the parser signal level it was taken at.

## Viewer surface inventory, 2026-08-22

**Superseded by "Viewer surfaces, 2026-08-30" at the foot of this file.** Kept because it is a dated
measurement of what was true then, not because it describes the viewer now.

All 51 `page.tsx` files against the 7 route handlers.

| Kind | Count | What they are |
|------|------:|---------------|
| Real | **3** | `knowledge-graph` (semantic zoom plus blast-radius highlight), `flat-baseline`, `decision-audit` |
| Redirect | 22 | Shells |
| Dead | 26 | Vendored pages whose endpoints 404 |

The dead pages 404 because `lib/api/client.ts` aims every vendored fetch at the app itself, where only the 7
handlers live.

This is deliberate and honest: `nav-items.ts` gates the sidebar per R9.1, `zoom-map-adapter.ts` emits neutral
zeros rather than inventing metrics, and **no fabricated or fixture data reaches the running app**.

**The vendored IA is not a backlog.** Filling the 26 would need a git-history analyzer, a coverage reader and
a security scanner. Do not read the count as planned work.

**Blast radius has no URL and no nav entry.** It is an interaction inside the Knowledge Graph, so it cannot
be demoed by navigating to it.

## Distribution weight, measured 2026-08-23

| Artifact | Size |
|----------|-----:|
| Engine compiled JS | 1.2 MB |
| Engine runtime deps | 13.5 MB, of which the needed `.wasm` is only 1.2 MB |
| Viewer static client assets | 19.1 MB |
| Viewer `standalone` server output | 90 MB |
| Viewer `node_modules` | 717 MB |
| Viewer `.next` | 1.3 GB |

**The engine is already light; all the weight is the viewer.** An engine-only CLI is roughly 15 MB installed,
about 3 MB bundled.

`repohive` was **available on npm** as of 2026-08-23: registry 404 plus zero search results.

## The viewer is nearly free-standing

`packages/ui/src/zoom` is 20 files / 116 KB and imports only `react` plus two constants from
`@repohive/types/health`. Its chrome is 6 files / 31.5 KB and adds only `lucide-react`, `next/link` and
`sonner`.

**No Next.js, sigma, recharts, d3, elkjs or mermaid.**

So a CLI viewer is a purpose-built single-file artifact of roughly 300-500 KB, **not** a static export of the
vendored app. That distinction decided the CLI's viewer approach.

## Repository state, verified 2026-08-29 22:36

The public repository replay is **complete**: 135 commits, `main` at `dbcdc14`, all eight feature branches
pushed. Earlier records claiming 39 of 57 replayed with `main` at 98 are **stale**, and were corrected on this
date.

## Degenerate regions, the trap in every split, 2026-08-30

**A region that was never assessed still appears in the reconstruct column.** The rule is
`score === 0 && cohesion === 0`, and **there is no explicit flag** in the index. The viewer detects it in one
place, `isDegenerate()` in `ui/src/repohive/decision-model.ts`.

| | `broadleaf` | `jsoup` | `sample-java-project` |
|---|---:|---:|---:|
| Total regions | 502 | 8 | 4 |
| **Degenerate**, score 0 by rule | **216 (43%)** | 1 | 3 |
| Genuinely assessed | 286 | 7 | 1 |
| Preserved | 38 | 3 | 0 |
| Reconstructed on measurement | 248 | 4 | 1 |

So the long-recorded "preserve 38 / reconstruct 464" for `broadleaf` is misleading: 216 of those 464 were
never measured. **Quote assessed-only splits.** On that basis the adaptivity evidence is `broadleaf` 38 of 286
(**13%**), `jsoup` 3 of 7 (**43%**), `sample-java-project` 0 of 1 — same algorithm, same seed, same
configuration, verified rather than assumed, and a 43-point spread.

**All 216 degenerate `broadleaf` regions carry `decisionConfidence: 0.5`, the maximum in the dataset.** Any
chart keyed on confidence therefore presents the unassessed regions as the most confident decisions in the
run. The viewer renders that cell as absent rather than as a measurement.

## Viewer surfaces, 2026-08-30

Rebuilt across two phases, 2026-08-29 and 2026-08-30. Seven reachable surfaces, gated through
`repoNavGroups()` / `GLOBAL_NAV` in `nav-items.ts`:

| Surface | Route | Holds |
|---------|-------|-------|
| Landing | `/` | server-rendered repo index read from each `index/`; absent fixtures shown as absent |
| **Adaptivity** | `/adaptivity` | cross-repo, not repo-scoped: assessed-only preserve rate per fixture |
| Structure map | `/repos/[id]/knowledge-graph` | the zoom canvas; decision carried by card frame, wash and badge |
| **Hierarchy** | `/repos/[id]/hierarchy` | radial icicle: radius depth, sweep file count, colour decision |
| Decisions | `/repos/[id]/decision-audit` | boundary strip, normalised scatter, provenance card, morph, table |
| **Architecture** | `/repos/[id]/architecture` | per-level flow, group DSM, fragmentation, determinism panel |
| Flat baseline | `/repos/[id]/flat-baseline` | the unstructured "before" |

Our modules live in `ui/src/repohive/` and adapters in `web/src/lib/repohive/`, outside the vendored folders
per the NOTICE rule. **19 of the 22 redirect shells are deleted** (repo-root, `/c4`, `/zoom` remain, all
landing on the canvas), the two dead Knowledge-Graph controls are gone, every visible upstream brand string is
out of the chrome, and `/api/repos` lists only repositories whose index exists on the machine. The 26 dead
vendored pages remain unreachable and are **not** a backlog.

**Identity is applied at the token layer**: `--color-decision-{preserve,reconstruct,degenerate,boundary}` in
both themes, **dark is the default**, and `reconstruct` no longer resolves to `--color-warning` because
rebuilding a boundary is a success rather than a fault. Amber is the quality boundary alone. Every state
carries colour plus shape plus word, so nothing is colour-only.

**Test counts, 2026-08-30:** `ui` repohive **40**, `web` **51**. The 37 pre-existing vendored `ui` failures
and the two pre-existing `ui gates` hex hits are unchanged and were not touched. `next build` is clean with
every new route present.

### Three briefed items were not built as specified

Recorded because each refusal is itself a finding about the engine.

1. **Group purity is structurally impossible.** A Region *is* an authored package (`pkg:<path>`) and
   reconstruction partitions strictly *within* a region, so a produced group can never mix packages. Measured:
   **0 of 1,182** reconstructed groups draw from more than one package, on either fixture. A packages-to-groups
   mixing flow would assert something the engine cannot produce. **Fragmentation** was built instead, the
   inverse, which is where the evidence actually is: `broadleaf` `common.util` is **65 authored files split
   into 46 clusters**, `jsoup` `internal` is 12 into 10.
2. **The vendored DSM view was not fed.** It renders rule violations and dependency cycles, which this project
   does not compute, and it defaults a null edge kind to an HTTP transport, which would paint every structural
   edge as one. A plain-CSS DSM was built instead, ordered by recorded region and ordinal so blocks are *read*
   from the index rather than produced by a clustering pass.
3. **The coupling ring was not built.** Its own documentation describes its edges as co-change; ours are
   structural strength. The group DSM already covers group coupling. Treemaps remain blocked on a per-leaf
   size field.

**One verification caveat.** Client rendering was verified by component tests in `ui` plus endpoint checks
against real fixtures, not by eye: a hidden browser pane throttles React's Suspense reveal, so every route
rendered its loading fallback while the server HTML was correct. That is an environment artifact, diagnosed by
bisecting, not a bug.
