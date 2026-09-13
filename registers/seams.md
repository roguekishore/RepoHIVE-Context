# Foundation seams — what they are, what they block

Recorded 2026-08-29. **Nothing is implemented.** Authoritative decisions are in `decisions/`
(2026-08-22 live-indexing entry, 2026-08-23 retrofit entry).

Status: **on hold.** Needs its own design spec — the owner asked for a storage- and source-agnostic analysis,
which is a spec deliverable rather than something to improvise.

---

## 1. The four seams

| Seam | State today |
|------|-------------|
| **Orchestration** — `parse` → `group` in one call | **Absent.** `parseProject` is in `parser`, `groupGraphToIndex` in `core`, and neither imports the other. The two stages are joined only by two root npm scripts |
| **Source provider** — parse from something other than a local directory | Injectable, but across **three** separate points, none wired together |
| **Storage** — `get` / `put` / `has` instead of direct fs | **Asymmetric.** The write path has `IndexSerializerDeps` (`core/src/index-serializer.ts:108`); the read path calls `node:fs` directly at `core/src/index-parser.ts:10` and `core/src/orchestrator.ts:7` |
| **Snapshot ids** — content-addressed over `(repoUrl, commitSha, engineVersion, configDigest)` | Absent |

---

## 2. What blocks what

| Seam | CLI needs it? | Why |
|------|---------------|-----|
| Orchestration | **Yes** | `repohive index` *is* this layer |
| Source provider | No | the CLI always has a real directory on a real disk |
| Storage | No | the CLI writes to disk |
| Snapshot ids | Partly | enables `index` skipping an unchanged parse; essential only for hosting |

**The hosted path needs all four.** MCP's read-only v1 needs none — `parseIndex` and `analyzeBlastRadius` are
already exported from `core`.

---

## 3. Why retrofitting is safe

**Adding an interface behind an existing function is backwards-compatible when the default is preserved**, and
that is already the house pattern:

```ts
parseProject(options, deps = defaultDeps())        // parser/src/orchestrator.ts
```

`IndexSerializerDeps` does the same for the write path — injects the fs calls with an fs default, added so
write failures were testable. The source provider and storage interface can be added the same way, later,
without breaking the CLI.

**What is *not* retrofittable is the published CLI surface** — the `.repohive/` layout, command and flag names,
the `--json` shape, exit codes. Once a stranger writes CI against those, changing them is a major version.
See `docs/cli.md` § 8.

**So seam work does not block the CLI. Nail the CLI contract instead.**

---

## 4. Source provider — three injection points, not one

`decisions/`'s 2026-08-22 entry says "`ParseDeps.collector` is the existing injection point." Verified
2026-08-23: **necessary but not sufficient.** The parser reaches the filesystem in three injectable but
unwired places:

1. `deps.validator.validate(options.projectDirectory)` — runs first, short-circuits on a bad path.
2. `deps.collector.collect(validated, …)` — the directory walk (`source-collector.ts:137`).
3. `ast-extractor.ts` `defaultDeps.readFile = nodeFs.readFileSync(absolutePath, "utf8")`.

Plus **`ParseOptions.projectDirectory` is a required `string`** (`orchestrator.ts:71`), and `ParseDeps` has six
fields with no partial-override helper.

**Consequence:** swapping the collector alone will not admit tarballs, uploads or in-memory sources. The work
is a first-class source-provider abstraction plus `projectDirectory` becoming optional. The 2026-08-22 decision
itself stands unchanged; only its cost estimate for this item moves up.

Useful detail: `createAstExtractor(deps: AstExtractorDeps = defaultDeps, grammar: GrammarOptions = {})`
already accepts injectable deps, so point 3 needs no change to `ast-extractor.ts` — only a caller that supplies
a different `readFile`.

### A design choice the spec must make

**Extract-then-walk, or stream from the archive?** The performance work (`docs/performance.md`) surfaced this:
a hosted indexer that reads tar entries straight from memory writes no new files, which **eliminates** the
~15 ms/file first-access penalty rather than mitigating it, and replaces 2985 file opens with one sequential
read. Caveat: tar entries arrive in archive order and need canonical sorting first.

---

## 5. WASM constrains bundled deployment

`parser/src/ast-extractor.ts` `resolveGrammarPaths` locates two prebuilt WASM artifacts via
`createRequire(import.meta.url).resolve("web-tree-sitter")` and
`require.resolve("tree-sitter-java/tree-sitter-java.wasm")`. This works from `node_modules` and **breaks under
any bundler**, which drops `.wasm` files and rewrites module resolution.

`GrammarOptions { coreWasmPath?, javaWasmPath? }` exists to override it, and its docstring names bundled
deployments as the reason — so this is anticipated, but it must be explicitly wired for any Lambda, container
or bundled target.

---

## 6. Orchestration must be de-conflicted first

**This is the one sequencing item inside an otherwise parallel plan.** Both the CLI and the hosted path need a
parse→group layer. If each worktree builds its own, the result is two incompatible implementations and an
unresolvable merge.

**Mitigation: define the orchestration package's interface first** — one file of type signatures, a couple of
hours — so both worktrees code against it while the seam worktree supplies the implementation. Do this before
either writes orchestration code.

Give it **its own package.** If it lands inside `packages/cli`, the MCP server ends up importing a package
called "cli".

---

## 7. What the hosted path additionally requires

From the 2026-08-22 live-indexing decision, restated only as a checklist:

- `groupGraph` off the request thread in `worker_threads` — it is synchronous and CPU-bound
- progress as a first-class engine output, carried over SSE
- fetch by codeload tarball, not `git clone`
- `visibility` on the snapshot from day one, so private-repo auth stays additive
- guard rails shipped **with** the endpoint, not after: `github.com/owner/repo` validation only (arbitrary
  remotes are an SSRF hole), size and file-count caps checked via the GitHub API *before* download, per-job
  timeout, global concurrency cap, per-IP rate limit, and extraction hardened against path traversal and
  decompression bombs

Mitigating factor already on record: the engine parses source and never executes it, and persists no source
text.

---

## 8. Estimate

~2–3 days for all four seams. Ships no visible feature. Three of the four forward paths queue behind it, but
**the CLI does not** — see § 3.

Per the 2026-08-28 decision, this work belongs in **the public repository**, not this archive repo.

---

## 9. Orchestration signature — proposal, not decided

Added 2026-08-29 as a proposal. **DECIDED AND BUILT 2026-09-13** as `@repohive/engine` — see
`decisions/2026-09-13-engine-orchestration-package.md` for what was adopted, adapted, and rejected, and read
the per-item notes below before citing anything here. The three findings that follow are still accurate; the
proposed signature is superseded by the implemented one, which the decision file carries verbatim.

### Three findings that shape it

Verified 2026-08-29 by reading the signatures:

**1. `ParseSuccess` does not return the graph.** It carries `outputPath`, `nodeCount`, `edgeCount`, and
optional `crossScopeAmbiguities` / `excludedDirectoryCount` (`parser/src/errors.ts:61`). But `groupGraph` and
`groupGraphToIndex` both accept a `RawDependencyGraph` **in memory**.

So orchestration as things stand must: parse → write `graph.json` → `readGraphFile()` → read it back.
Broadleaf's `graph.json` is **18.6 MB**, so that is **~37 MB of avoidable I/O per `index` run**, purely to move
data between two functions in the same process.

*Proposed fix, additive and non-breaking:* `ParseSuccess` gains an optional `graph?: RawDependencyGraph`.
`index` hands it straight to `groupGraph`. **Keep writing `graph.json`** — it is in the committed `.repohive/`
layout and it is what lets `group` be re-run for sweeps without re-parsing — just stop reading it back.

**2. There are two incompatible `Result` types.** Core's is not generic over the error:

```ts
// core/src/errors.ts
export type Result<T> = { ok: true; value: T } | { ok: false; error: GroupingError };
```

The parser's own `Result` carries `ParseError[]`. Unifying them would be a breaking change to both packages for
no gain, so **orchestration needs a third result type that discriminates by stage.**

**3. `readGraphFile` uses `readFileSync` directly** (`core/src/orchestrator.ts:321`), which is the same
read-path storage gap recorded in § 1. Passing the graph in memory sidesteps it for the `index` path but does
not close it.

### Proposed signature

```ts
// packages/pipeline/src/index.ts

export interface IndexOptions {
  projectDirectory: string;
  outputDirectory?: string;           // default: <projectDirectory>/.repohive
  grouping?: PartialGroupingConfig;   // core's type, passed straight through
  excludedSegments?: ReadonlySet<string>;
  readConcurrency?: number;           // the prefetch knob (docs/performance.md)
  force?: boolean;                    // reserved; see decision 5
}

export type IndexStage = "parse" | "group" | "serialize";

export interface IndexProgress {
  stage: IndexStage;
  completed: number;
  total: number;
}

export interface IndexSuccess {
  graphPath: string;
  indexDirectory: string;
  nodeCount: number;
  edgeCount: number;
  regionCount: number;
  preserveCount: number;
  reconstructCount: number;
  hierarchyDepth: number;
  parseSkipped: boolean;
  crossScopeAmbiguities?: number;
  excludedDirectoryCount?: number;
}

export type IndexResult =
  | { ok: true; value: IndexSuccess }
  | { ok: false; stage: "parse"; errors: readonly ParseError[] }
  | { ok: false; stage: "group"; error: GroupingError };

export interface PipelineDeps {
  parse: (o: ParseOptions) => Promise<ParserResult>;
  group: (g: RawDependencyGraph, outDir: string, c?: PartialGroupingConfig) => CoreResult<GroupingOutput>;
}

export async function indexProject(
  options: IndexOptions,
  onProgress?: (p: IndexProgress) => void,
  deps?: Partial<PipelineDeps>,
): Promise<IndexResult>;
```

### The five decisions inside it

1. **Package name: ~~`@repohive/pipeline`~~ → OVERRIDDEN by the owner to `@repohive/engine`, 2026-09-13.**
   The objection recorded here — that "engine" already means parser + core + shared collectively — was
   answered by defining the terminology instead: **"the engine packages"** = `shared`, `parser`, `core`,
   `engine`; **"the engine orchestration package"** = `@repohive/engine` alone. The rest of this item stands
   and was honoured: not inside `packages/cli` (or the MCP server ends up importing a package called "cli"),
   classified **engine-side**, and it must not import from `web`, `ui`, `api-client` or `cli`.
2. **In-memory handoff** — add `graph?` to `ParseSuccess`. Saves ~37 MB of I/O on broadleaf; additive.
3. **Stage-discriminated result** — leave the two existing `Result` types alone.
4. **Define the progress callback now, fire coarse events in v1.** The 2026-08-22 live-indexing decision makes
   progress a first-class engine output for SSE. Defining the shape costs nothing; the parser emits no per-file
   events today, so v1 fires at stage boundaries only, and per-file granularity lands later without a signature
   change.
5. **`force` reserved, and v1 always parses.** **This reverses what `docs/cli.md` § 3 currently says.** That
   document states `index` "skips parse when `graph.json` is already current." Deciding "current" properly is
   the snapshot-id seam; the cheap substitute is mtime comparison, which is fragile — and **a wrong skip
   silently serves a stale index, which is far worse than a redundant ~7 s parse.** Keep the flag for forward
   compatibility, document that v1 ignores currency. **ACCEPTED 2026-09-13**, with one half corrected:
   `parseSkipped` is **kept** in the result shape (present, always `false` in v1), not dropped, because that
   already matches the snapshot-id era. `registers/cli.md` § 3 was corrected in the same change. The `force`
   flag itself was **not** adopted: it existed only to control skipping, so v1 would ship it dead; it arrives
   as a new optional field when skipping lands.

### Still open, both one-liners

- **Lockstep versioning** — do all packages share one version and move together? Adding `@repohive/pipeline`
  makes five, which slightly strengthens the case.
- **Does the first publish ship without a viewer?** Stage 1 is `index` + `--json` only.
