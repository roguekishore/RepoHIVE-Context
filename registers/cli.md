# Packaged CLI — decisions, blockers, plan

Recorded 2026-08-29. **Nothing is implemented; `packages/cli` holds one `.gitkeep`.** Authoritative source for
the decisions is `decisions/` (entries 2026-08-22 and 2026-08-23); this document collects them in one
place with the supporting measurements.

Status: **requirements spec unblocked, on hold** pending an owner call. Write the spec before any code.

---

## 1. Decided

| Area | Decision |
|------|----------|
| **Sequencing** | The CLI is a workstream; MCP is deferred behind it. All workstreams run in parallel worktrees, so "which first" is closed |
| **Commands** | `index` · `parse` · `group` · `view`. **Names are final.** `describe` deferred to a later release |
| **Install** | README recommends `npm i -g repohive` → `repohive index .`; `npx repohive index .` is the no-install path |
| **Output** | `.repohive/` by default, `--out` to override |
| **Packaging** | Publish **four**: `@repohive/shared`, `@repohive/parser`, `@repohive/core` as libraries, plus `repohive` as the CLI. The CLI **depends on** the three rather than bundling them |
| **Version** | Release at **`0.x`** |
| **Bundler** | **Vite + `vite-plugin-singlefile`** for the viewer artifact; `tsup`/esbuild for the CLI if it is ever bundled |
| **Shipped viewer** | The **hierarchical viewer only.** Others are bonus if weightless |
| **Seam dependency** | Only **orchestration** blocks the CLI. Source provider, storage and snapshot ids are all safely retrofittable |
| **Steering** | `docs/engineering/stack.md`'s tool lists are **extensible, not boundaries** — new tools admitted when the work demands, recorded in the same change |

**`repohive` is available on npm** — registry returns 404 and a search returns zero results, checked
2026-08-23. So the unscoped name and `npx repohive` are achievable.

---

## 2. Open

1. **Confirm lockstep versioning.** `0.x` is decided; whether all four packages share one number and move
   together was *assumed* from the recommendation being agreed to, not stated. Cheap now, expensive after the
   first publish.
2. **Is a first publish with no viewer acceptable?** Stage 1 is `index` + `--json`, no viewer, ships in days.
   Recommended yes, with the viewer following as a minor version. Blocks nothing.

---

## 3. Command surface

```
repohive index <dir> [--out <dir>] [--json] [<group flags>]
    -> .repohive/graph.json + .repohive/index/ + .repohive/view/
    parse, then group, then write the viewer artifact.
    Skips parse when graph.json is already current for the input.   <-- CONTESTED

repohive parse <dir> [--out <dir>] [--include-generated] [--exclude a,b] [--json]
    -> .repohive/graph.json                                    (stage 1 alone)

repohive group <graph.json | dir> [--out <dir>] [--boundary <n>] [--seed <n>]
              [--weight-cohesion <n>] [--weight-coupling <n>] [--weight-modularity <n>]
              [--squash-k <n>] [--degenerate-score <n>] [--compute-modularity]
              [--preserve <regionId>] [--reconstruct <regionId>] [--json]
    -> .repohive/index/                                        (stage 2 alone)

repohive view [dir] [--port <n>] [--no-open]
repohive --version | --help
```

Artifact layout:

```
.repohive/
  graph.json    # stage-1 output
  index/        # the 5-file engine contract - stable, documented, what tools read
  view/         # the hierarchical viewer artifact
```

`index/` stays separate and untouched because it is the published contract that MCP, the hosted service and
third-party tooling read. `view/` is a rendering of it and may churn.

> **CONTESTED — "skips parse when `graph.json` is already current".** Recommendation as of 2026-08-29 is that
> **v1 should always parse.** Deciding "current" properly is the snapshot-id seam; the cheap substitute is mtime
> comparison, which is fragile, and a wrong skip silently serves a stale index — far worse than a redundant
> ~7 s parse. Reasoning and the proposed signature are in `docs/seams.md` § 9, decision 5. **Not yet decided;**
> if accepted, correct this line and drop `parseSkipped` from the result shape.

### Why the stages stay separately invokable

Not for speed. Corrected 2026-08-24 after the timings it originally rested on were found wrong:

| Scenario | Cost (broadleaf, warm) |
|----------|-----------------------:|
| A user indexing once | **~14 s.** Users never sweep |
| Sweep of 20 boundary values, stages separate | 7.6 + (20 × 6.7) ≈ **2.4 min** |
| Same sweep with `index` as the only command | 20 × 14.3 ≈ **4.8 min** |

The saving is ~2.4 minutes, not the ~21 previously claimed. **Do not cite a large time saving.** The durable
reasons are that algorithm spec **Req 4.4** requires boundary sweeps without code changes, and running `parse`
alone is the natural move when a graph looks wrong. The stages are the research and debugging interface;
`index` is the product interface.

### Why the names were kept

| Considered | Rejected because |
|------------|------------------|
| `parse` → `scan`, `extract` | no clearer; `parse` is precise |
| `group` → `cluster` | actively wrong — asserts clustering always happens, when the contribution is *deciding* between preserve and reconstruct |
| `group` → `organize`, `structure` | vaguer, and they do not name the output |
| `view` → `open`, `serve` | `view` covers both serving and opening; each alternative covers one |

Decisive argument was cost: those four words appear across the specs and steering in 30-plus places and
renaming buys a user nothing.

---

## 4. How the command gets created

A `bin` entry is what makes it a command:

```json
"bin": { "repohive": "./dist/cli.js" }
```

| User runs | Effect | Then invoked as |
|-----------|--------|-----------------|
| `npm i -g repohive` | global install, shim on PATH | `repohive index .` anywhere |
| `npm i repohive` | local; shim only in `node_modules/.bin` | `npx repohive index .` |
| `npx repohive index .` | fetch to cache, run, no install | that one line |

**`npm repohive index` is not valid** — npm's subcommands are its own and cannot be extended. The valid long
form is `npm exec repohive index .`, which `npx` abbreviates. **This must not appear wrongly in any docs.**

Subcommands need no special mechanism: they are the first argument to the same binary, dispatched on, as
`git commit` and `docker build` work.

---

## 5. Blockers

1. **`packages/cli` contains only `.gitkeep`.** `docs/engineering/architecture.md` described it as wiring the pipeline;
   corrected 2026-08-23.
2. **Nothing is publishable.** Every package is `private: true` at `0.0.0` (`@repohive/web` is `0.3.0`, also
   private). The CLI depends on `parser` and `core`, so those must be published too or bundled in.
3. **No orchestration layer**, so `index <dir>` has nowhere to live. `parseProject` is in `parser`,
   `groupGraphToIndex` in `core`, and neither imports the other — parse→group exists only as two root npm
   scripts. **Give orchestration its own package**; if it lands inside `packages/cli`, the MCP server ends up
   importing a package called "cli".
4. **`INIT_CWD` is an npm-script artifact.** Both wrappers resolve relative paths against it
   (`group-cli.ts` `resolveAgainstInvocationDir`, `parse-cli.ts` `invocationCwd`). A real `bin` must use
   `process.cwd()`.
5. **The self-execution guard will not fire under a `bin` shim.** `group-cli.ts` ends with
   `if (process.argv[1]?.endsWith("group-cli.js"))`. A packaged binary needs a shebang and unconditional
   `main`.
6. **`parse-cli.ts` is materially weaker than `group-cli.ts`.** Ad-hoc `args.indexOf("--exclude")`, a fragile
   positional filter, no unknown-flag rejection, and a default target of `fixtures/sample-java-project`
   resolved relative to `dist/` — demo behaviour that must not ship.
7. **No machine-readable output.** Both print hand-rolled prose. Add `--json` and treat prose as a rendering of
   it, before anyone depends on the sentences.
8. **The engine test script works on neither Node version.** `node --test dist/*.test.js` needs Node 21+ to
   expand the glob; `node --test dist/` runs on 20 but silently resolves to `dist/index.js` on 21+ and reports
   one passing test. **Fix this first** so the CLI inherits a working runner.

### What already exists and is good

`core/src/group-cli.ts` carries the full flag surface, routes every value through `validateConfig`, rejects
unknown flags and extra positionals, and exposes a testable `main(argv, io) → exit code` with 2 for usage and
1 for failure. **That part is done.** The extraction moves it; it does not redesign it.

---

## 6. Packaging and weight

Measured 2026-08-23:

| What | Size | In the CLI? |
|------|------|-------------|
| Engine compiled JS (`shared` + `parser` + `core` dist) | **1.2 MB** | yes |
| Engine runtime deps (graphology family + both Tree-Sitter packages) | **13.5 MB** | yes |
| — of which the `.wasm` actually needed | **1.2 MB** | yes |
| Viewer `standalone` server output | 90 MB | **no** |
| `node_modules` (dev tree) | 717 MB | no |
| `packages/web/.next` | 1.3 GB | no |

**The engine has no weight problem; the viewer does.** Engine-only CLI ≈ **15 MB installed**, ≈ **3 MB** if
bundled to one file plus the two `.wasm` files.

Two publishing mechanics worth stating:

- **`dist/` is what ships, not `src/`.** `tsc` compiles `src/*.ts` → `dist/*.js` plus `dist/*.d.ts`, and
  `"files": ["dist"]` means only `dist` enters the tarball. `dist/` is git-ignored (`.gitignore:8`, zero tracked
  files) and regenerates from `npm run build`.
- **`dependencies` are a shopping list, not luggage.** They are fetched at install time, not bundled. Bundling
  (esbuild/tsup) inlines them instead, trading a smaller install for having to republish on a dependency fix.
- **The `.wasm` files can never be inlined into JavaScript.** Even a fully bundled CLI ships them as real files
  located via `GrammarOptions` — the override that exists in `ast-extractor.ts` for exactly this.

**Start unbundled.** 15 MB is fine and npx caches it; bundling is a later optimization that changes nothing a
user types.

### Versioning

Semver is `MAJOR.MINOR.PATCH` — patch for a fix, minor for a backwards-compatible addition, major for a break.
The promise matters because a consumer writing `"repohive": "^1.4.2"` trusts any `1.x` not to break them, so
renaming a JSON field and shipping it as a minor silently breaks every such consumer. While MAJOR is `0`, that
promise is suspended by convention.

All packages currently read `0.0.0`, which conventionally means never released. **Decided: `0.1.0`**, because
the JSON contract will still grow (per-leaf file size, an engine-version field, snapshot ids) and a rename may
yet be wanted. Go to `1.0.0` when the contract has survived strangers.

**Lockstep is assumed, not confirmed** — see § 2.

---

## 7. Shipped viewer

**The hierarchical viewer only.** Measured 2026-08-23: `packages/ui/src/zoom` is 20 files / 116 KB and its
**only** bare-specifier imports are `react` and two constants from `@repohive/types/health`. Its chrome
(`web/src/components/zoom`, 6 files / 31.5 KB) adds only `lucide-react` (tree-shakes to a few icons),
`next/link` (replaceable with `<a>`) and `sonner` (droppable). **No Next.js, sigma, recharts, d3, elkjs or
mermaid** — the canvas paints itself.

So the artifact is a **purpose-built single-page bundle, ~300–500 KB as one self-contained `.html`**, not a
static export of the vendored Next.js app. That estimate is from the import graph, **not from a built
artifact**.

**Withdrawn:** static-exporting the vendored app (`output: "export"` replacing the current
`output: "standalone"`, deleting the 7 route handlers, pointing `lib/api/client.ts` at relative static paths).
Sound, but unnecessary once only the hierarchical viewer ships. Retained in `registers/workstreams.md` because it
is still the right recipe if a future artifact must carry several vendored surfaces.

Staging:

1. **Stage 1** — no viewer. `index` + `--json`. Ships in days.
2. **Stage 2** — the single-file hierarchical viewer. No server, no Next.js runtime, no dependency on the
   viewer-polish workstream.

---

## 8. What is expensive to change later

Internal seams are retrofittable behind defaults. **These are not** — once anyone writes CI around
`repohive index --json`, changing them is a major version and a broken build for them:

- the on-disk layout of `.repohive/`
- command names and flag names
- the `--json` output shape
- exit codes (the existing 2 = usage, 1 = failure split is already consistent — make it documented contract)

**So the CLI is blocked on nailing its contract, not on seam work.** That is what the requirements spec is for.

---

## 9. Plan

1. **Fix the engine test script** so the CLI inherits a runner that works on Node 20 and 21+.
2. **Define the orchestration signature** — one file of type signatures. Must land before the CLI *or* hosted
   worktree writes orchestration code, or the two produce incompatible implementations.
3. **Write the requirements spec.** Owner-reviewable flag surface before any code.
4. **Build the orchestration package**, then `packages/cli` with both wrappers moved in and `index` added.
5. **`npm pack` dry run**, then publish.

Estimate 3–4 days, above the 2–3 originally recorded because of blockers 2 and 3. Estimate, not measured.

Per the 2026-08-28 decision, this work belongs in **the public repository**, not this archive repo.

---

## 10. Licence note

Publishing an AGPL-3.0-or-later CLI to npm is unproblematic, and end users who merely run it take on no
obligation. The obligation attaches to conveying modified versions or offering it as a network service. Not
legal advice; get a qualified opinion if commercial licensing ever matters.
