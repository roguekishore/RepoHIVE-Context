# Drift Report

Fact-check of the four engineering convention documents against the repository they will ship inside.

**Primary target:** the public checkout. A claim must be true *there*.
**Cross-checked:** the archive checkout. Divergences noted.
**Sources:** the archive's four steering documents, read-only.
**Method:** file reads and read-only greps only. No installs, no builds, no test runs. That limit is the
single largest constraint on this report and the reason the measured-number rows below come back
unverifiable rather than confirmed.

## Totals

| Verdict | Count |
|---------|-------|
| Verified | 39 |
| Wrong or misleading | 15 |
| Unverifiable | 8 |
| **Total claims checked** | **62** |

Claim granularity is a judgment call. I counted a dependency-table row as one claim and a prose sentence
asserting one checkable fact as one claim, so treat the totals as close approximations rather than exact
scores. The verdicts themselves are exact.

Nothing below was inferred from a filename or from another document's description. Every verdict names
what was read.

## Verified

| # | Claim | Source | Evidence |
|---|-------|--------|----------|
| 1 | 8 packages exist: shared, types, parser, core, cli, api-client, ui, web | architecture.md 50-60 | `ls packages/` in both repos. Identical sets |
| 2 | `packages/cli` is EMPTY, `.gitkeep` only, packaged CLI not built | architecture.md 56 | `ls -aR packages/cli` in both repos returns only `.gitkeep`. The known past error of this exact kind is already corrected in the source doc |
| 3 | `index/` holds repository, hierarchy, nodes, edges, metadata `.json` | architecture.md 26 | `core/src/index-serializer.ts:34-38`, the enforced filename array |
| 4 | `GraphNode` fields: id, kind, packagePath?, directoryPath, definedInFile? | architecture.md 37 | `shared/src/contract.ts:38-55`. All five present with those optionality markers |
| 5 | `DependencyEdge` fields: source, target, importFrequency, methodCallFrequency, sharedTypeCount, strength? | architecture.md 38 | `shared/src/contract.ts:71-84`. All six present |
| 6 | Group nodes carry `regionId` and `ordinal`; decisions carry `groupIds` | architecture.md 41 | `core/src/hierarchy-builder.ts:108-115` (groupIdsOfRegion), `hierarchy-builder.test.ts:319` asserts ordinals start at 0 per preserved region |
| 7 | Node ids carry a `<sourceRoot>\|` prefix, omitted when scope empty | architecture.md 45-46 | `parser/src/ast-extractor.ts:463,474,534` thread `sourceRoot` through `buildClassId` |
| 8 | `parser` and `core` depend only on `shared` | architecture.md 62 | `grep -rho "@repohive/[a-z-]*"` over engine src: 51 hits on `shared`, plus 2 self-naming doc comments |
| 9 | Engine must not and does not import from web/ui/api-client/cli | architecture.md 63, 96, conventions.md 30 | `grep -rn "@repohive/\(web\|ui\|api-client\|cli\|types\)" packages/{parser,core,shared}/src` exits 1, no matches. **Boundary rule currently holds** |
| 10 | `parseProject` in parser, `groupGraphToIndex` in core, neither imports the other | architecture.md 65-67 | `parser/src/index.ts:11` exports parseProject from orchestrator; `core/src/index.ts:35` exports groupGraphToIndex; cross-grep for the other package exits 1 |
| 11 | parse→group exists only as two root npm scripts | architecture.md 67 | Root `package.json:12-13`, `parse` and `group` delegate to workspaces. No orchestration package |
| 12 | The 7 listed API routes exist, and are the only ones | architecture.md 74-82 | `find packages/web/src -path '*api*' -name route.ts` returns exactly 7, matching the list one for one |
| 13 | Routes are unauthenticated | architecture.md 84-86 | `grep -rn -i "auth\|session\|token\|apikey"` across all 7 route files: zero matches. Warning preserved and kept prominent |
| 14 | A flat baseline view exists alongside semantic zoom | architecture.md 88 | `packages/web/src/app/repos/[id]/flat-baseline/page.tsx` |
| 15 | `graph.json` and `index/` are git-ignored generated artifacts | architecture.md 28 | `.gitignore`: `graph.json`, `**/graph.json`, `index/`, `**/index/` |
| 16 | TypeScript 5.9.3 | stack.md 7 | Root `package.json:22`, exact pin |
| 17 | npm workspaces monorepo, glob `packages/*` | stack.md 8 | Root `package.json:6-8` |
| 18 | Licence AGPL-3.0-or-later, upstream attribution in NOTICE | stack.md 9-10 | Root `package.json:18`, engine manifests, `LICENSE`, `NOTICE` attributing types/ui/api-client/web to repowise upstream |
| 19 | All 6 engine dependency versions | stack.md 16-21 | `parser/package.json`: web-tree-sitter 0.26.10, tree-sitter-java 0.23.5, graphology 0.26.0. `core/package.json`: graphology 0.26.0, communities-louvain 2.0.2, metrics 2.4.0, fast-check 4.8.0 dev. All exact, all match |
| 20 | Louvain sits behind a `CommunityDetector` interface, swappable | stack.md 19, 23 | `core/src/community.ts:40` declares `detect(subgraph, seed)`, `:56` implements it as LouvainCommunityDetector |
| 21 | Native `tree-sitter` is not installed | stack.md 25 | `grep -rn '"tree-sitter"' --include=package.json`: no match. Only `tree-sitter-java` |
| 22 | WASM paths resolved from node_modules; bundled deployment must pass `GrammarOptions` | stack.md 27-30 | `parser/src/ast-extractor.ts:129-142` `resolveGrammarPaths` uses `require.resolve`; `:97` `GrammarOptions`, `:103` coreWasmPath, `:109` javaWasmPath |
| 23 | MySQL removed, not present | stack.md 38 | `grep -rn -i mysql --include=package.json`: no match |
| 24 | Viewer dependency list, all 13 named packages | stack.md 33-34 | `web/package.json`: next ~15.5.21, react/react-dom ^19.0.0, @tailwindcss/postcss ^4.0.0, swr ^2.2.5, nuqs ^2.2.0, framer-motion ^11.11.0, recharts, shiki, cmdk ^1.0.0, lucide-react, sonner ^2.0.7, next-themes ^0.4.6, geist ^1.3.0. All present |
| 25 | Tests use Vitest | stack.md 36 | `vitest ^4.1.5` in api-client, types, ui, web devDeps; `test: vitest run` in each |
| 26 | `npm run build` is `tsc -b packages/parser packages/core` | stack.md 59 | Root `package.json:10`, verbatim |
| 27 | `npm test` is `npm run test --workspaces --if-present` | stack.md 61 | Root `package.json:16`, verbatim |
| 28 | parse, group, demo:group-determinism, demo:baselines scripts | stack.md 62-65 | Root `package.json:12-15`, all four present as described |
| 29 | `dev --workspace @repohive/web` serves port 3000 | stack.md 66 | `web/package.json:8`, `next dev --port 3000` |
| 30 | Engine test script is `node --test dist/*.test.js` | stack.md 68, verification.md 32 | Verbatim in `core/package.json` and `parser/package.json` |
| 31 | `npm run parse` resolves relative paths against `INIT_CWD` | stack.md 87 | `parser/src/parse-cli.ts:59` `process.env.INIT_CWD ?? process.cwd()`, comment at `:57` explains the `--workspace` indirection |
| 32 | Read path has no seam: index-parser and orchestrator import node:fs directly | stack.md 98-99 | `core/src/index-parser.ts:10` `import { existsSync, readFileSync } from "node:fs"`; `core/src/orchestrator.ts:7` `import { readFileSync } from "node:fs"`. **Both line numbers exact** |
| 33 | `IndexSerializerDeps` injects mkdir/write/rename/rm/exists/assertWritable with an fs default | stack.md 95-97 | `core/src/index-serializer.ts:107` interface, `:111-116` the six members, `:117` `defaultDeps`, `:140` default parameter |
| 34 | `ParseOptions.projectDirectory` is a required string | stack.md 104 | `parser/src/orchestrator.ts:71-73` |
| 35 | No Math.random, timestamps, or wall-clock reads in engine output paths | conventions.md 9 | `grep -rn "Math.random\|Date.now()\|new Date("` over `{parser,core,shared}/src` excluding tests: zero matches |
| 36 | Community detection runs seeded over canonically-sorted input | conventions.md 12 | `core/src/community.ts:44` `seededRng` mulberry32, `:110` `rng: seededRng(seed)`, header comment at `:10` describes canonical sort then relabel. `core/src/canonical-order.ts` exists in shared |
| 37 | Property tests use fast-check | verification.md 88 | `fast-check 4.8.0` in core and parser devDeps; imported by at least 10 core test files including assessor, blast-radius, canonical-order, hierarchy-builder, orchestrator |
| 38 | `source-collector.test.ts` exists (known failure 1) | verification.md 49 | `packages/parser/src/source-collector.test.ts` |
| 39 | `types/__tests__/node-ids.test.ts` imports a fixture that does not exist | verification.md 52-53 | Import at `packages/types/__tests__/node-ids.test.ts:15` is `../../../tests/fixtures/node_ids.json`; `find . -name node_ids.json -not -path '*/node_modules/*'` returns nothing. **Confirmed defect** |

## Wrong or misleading

| # | Claim | Source | True value and where checked | What I changed |
|---|-------|--------|------------------------------|----------------|
| 40 | `npm run typecheck` is "same targets, no emit" | stack.md 60 | **Wrong.** Root `package.json:11` is `tsc -b packages/parser packages/core`, byte-identical to `build` at `:10`. No `--noEmit`. It emits `dist/`. Real no-emit checks are per package and split across two names: `typecheck` in shared/parser/core, `type-check` in api-client/types/ui/web. No root script runs the second group | Corrected the commands table to say "identical to build", added a paragraph documenting the emit behaviour and the two-name split. Repeated in verification.md Gate 1 |
| 41 | React Flow "not used, do not reintroduce" | stack.md 37-38 | **Wrong at repo level.** `@xyflow/react ^12.10.2` is a dependency at `packages/ui/package.json:139`, imported by **28 files** under `packages/ui/src/c4/` (`grep -rl` count). Narrow reading survives: **0** imports in `packages/ui/src/graph`, **0** in `packages/web/src`. Reached from web only via the `@repohive/ui/c4` entry point, referenced at `web/src/app/repos/[id]/knowledge-graph/page.tsx:23` | Rewrote to the accurate narrow scope per instruction: live `ui` dependency at that version and file count, unused by `packages/web` and by `ui/src/graph`, with the original protective intent stated as still applying to the graph canvas |
| 42 | Next.js required for `packages/web` because the vendored packages depend on it | stack.md 39 | **Reason is false.** `grep -rn 'from "next/'` over `ui/src`, `types/src`, `api-client/src`: **0 matches in all three**. `ui` peer-depends on `next-themes ^0.4.0`, not on `next`. The conclusion may still be right; the stated justification is not | Kept the decision, replaced the false reason with an explicit note that the justification does not hold and the choice should be revisited deliberately rather than treated as imposed |
| 43 | Blanket ESM, `"type": "module"` | stack.md 7 | **Incomplete.** Absent from the **root** manifest and from `packages/web`. Present in the other 6. Checked by grepping each of the 9 manifests | Enumerated exactly which packages set it and noted Next.js handles format in web |
| 44 | `core/src/index-serializer.ts:108` | stack.md 96 | **Off by one.** `export interface IndexSerializerDeps` is at line **107**. `grep -an` on the file | Corrected to `:107` |
| 45 | Root tree contains `.kiro/`, `docs/`, `repowise/`, `tooling/`, `archive/` | architecture.md 104-110 | **None exist in repohive-public.** `ls -a` shows: `.editorconfig`, `.git`, `.gitignore`, `LICENSE`, `NOTICE`, `README.md`, `components.json`, `fixtures/`, `package.json`, `package-lock.json`, `packages/`, `tsconfig.base.json`. Vendored code is merged into the four packages per `NOTICE`, there is no `repowise/` directory. `tooling/` and `archive/` are git-ignored. GRAPH does have all of these, so this is a real divergence between the two repos | Rewrote the section as "Repository layout" describing the actual public tree, plus an explicit list of deliberately-absent git-ignored paths |
| 46 | `.kiro/` at workspace root, with an absolute local path given as the project root | architecture.md 101 | **Must not ship.** An absolute local path naming a private workspace | Deleted outright. Replaced with the repository-relative layout |
| 47 | fixtures are sample-java-project, vantage, broadleaf | architecture.md 107 | **Only one present.** `ls fixtures/` returns `sample-java-project/` alone. `.gitignore` lists all three as ignored, so none is tracked content | Narrowed to the one that exists, noted the clone target is git-ignored |
| 48 | `docs/`: a claim that two named subfolders are excluded from context | architecture.md 106 | **Must not ship.** The claim named the excluded folders explicitly, and no `docs/` exists in the public repo anyway | Removed. `docs/engineering/` documented as the durable public half |
| 49 | Gate 5 properties in `.kiro/specs/hierarchical-repository-grouping/` | verification.md 87 | **Path does not exist in the public repo.** No `docs/` and no `specs/` anywhere (`find -maxdepth 2 -name specs` returns nothing). Present only in GRAPH, holding design.md, requirements.md, tasks.md | Gate 5 removed entirely (owner, 2026-08-29: specs are not ported). The one durable fact inside it is kept as a note: the property tests run under Gate 2 via `fast-check`, so there is nothing extra to invoke, and a behaviour change is described rather than cited by property number |
| 50 | Gate 4 compares against `PROJECT_STATE.md` | verification.md 81 | Ports to `context/STATE.md`, which is git-ignored (`.gitignore` final entry: `context/`), so it ships absent by design | Repointed, labelled "requires the private mount", added explicit degraded-mode instructions |
| 51 | `.kiro/workstreams.md` cited twice as the pointer for open work | architecture.md 68, stack.md 104 | File exists in GRAPH, **absent from the public repo**, and I could not verify any ported public equivalent | Dropped both pointers. Restated the open question inline in architecture.md so the paragraph stands alone |
| 52 | Contract snippet: `kind: "file"\|"function"\|"class"` | architecture.md 37 | **Understated.** `NodeKind` at `shared/src/contract.ts:28` has **five** members including `group` and `repository`. The parser emits only the three; the other two are produced downstream (`contract.ts:12-16`) | Gave the full union and stated the producer split precisely, rather than a three-member type |
| 53 | Parser reaches the filesystem in "three injectable-but-unwired places" (validator, collector, ast-extractor readFile) | stack.md 102-103 | **Count is low.** `serializer.ts:246` documents the same inject-with-fs-default pattern, making four: `input-validator.ts:21,80`, `source-collector.ts:26`, `serializer.ts:29,246`, `ast-extractor.ts:78-88`. Whether any is genuinely "unwired" from `parseProject` was **not** traced | Corrected to four, named all four, and flagged the wired/unwired question as unverified |
| 54 | Commit type `kiro(scope):` for specs, steering, hooks, agents, skills, memory | conventions.md 45 | Kiro-specific machinery, being dropped | Replaced per instruction: `feat fix test refactor perf chore` for `packages/`, `docs:` for documentation including these files, and in the private context repo `decision:` / `state:` / `register:`. Kept lowercase, imperative, no trailing period, ~70 chars, and the one-commit-per-sub-behaviour rule verbatim |
| 55 | Known failure 3 path `dsm-matrix.test.tsx` | verification.md 54 | Actual path is `packages/ui/__tests__/workspace/dsm-matrix.test.tsx`, one directory deeper than implied. `token-drift.test.ts` is at `packages/ui/__tests__/token-drift.test.ts`. Both confirmed present | Corrected both to full repo-relative paths |

## Unverifiable

| # | Claim | Source | Why unverifiable | What I did |
|---|-------|--------|------------------|------------|
| 56 | Per-workspace test counts: core 153/153, parser 180/181, api-client 50/50, web 20/20, types 2 suites fail, ui 1041/1042 | verification.md 22-29 | `repohive-public` has **no `node_modules`** (`ls -d node_modules` fails) and **no `dist/`** (`ls -d packages/*/dist` fails). Installs and builds are forbidden for this task, so no count can be reproduced. What I could verify is test **file** counts, identical in both repos: core 17, parser 11, api-client 5, types 3, ui 143, web 5, shared 0. That is consistency of surface, not of results | Kept every number with its "measured 2026-08-22, private workspace, Node v20.19.0 / npm 10.8.2" attribution, retitled the column to say so, and added an explicit line that none has been reproduced in the public repo. Added the verifiable file counts separately |
| 57 | Both SHA-256 digests, group and parse | verification.md 70-72 | Same reason. Recomputing needs a build and a pipeline run | Kept both with their recorded dates, added that neither was recomputed, and split the gate into its self-contained repeatability half (runnable) and its compare-to-table half (assumes the same fixture clone) |
| 58 | "Root `npm test` currently exits 1" | verification.md 19 | Not executed. It is a **sound inference**, not a measurement: the missing `node_ids.json` fixture is confirmed, which guarantees at least one failing workspace | Restated as expected-non-zero with the reasoning shown, and explicitly flagged that the exact code was not measured. Reframed `npm test` as a change detector rather than a gate |
| 59 | Node 20 fails on `dist/*.test.js`; Node 21+ silently resolves `dist/` to one file | verification.md 33-37, stack.md 71-74 | Neither form was executed. The script text is confirmed verbatim in both manifests; the behaviour is reasoned from documented Node semantics | Kept prominently, under a heading naming it a false green, explicitly marked "reasoned, not measured". Added the enforcement gap: only `packages/web` declares `engines` (`>=20.0.0`), root declares none, so the version skew that breaks this is unconstrained |
| 60 | `graph.json` is ~10 to 20 MB at 4k files | stack.md 92 | No 4k-file fixture measurement available offline | Kept, relabelled explicitly as an estimate rather than a measurement |
| 61 | Group ids are content-addressed | conventions.md 13 | **Partly supported only.** No `createHash` or `sha256` call in `core/src/hierarchy-builder.ts`. The `g_<hash>` format appears in test commentary at `hierarchy-builder.test.ts:301`. The derivation was not traced to its implementation | Kept the rule, added an explicit note that this specific claim is only partly confirmed and should be re-verified. Not silently promoted |
| 62 | Semantic zoom is ~20 nodes per level; client-side layout is deterministic, sorted by sibling rank with ties broken by id | architecture.md 88-89 | Not confirmed. No node-budget constant located in the zoom-map route; the client layout code was not inspected | Moved both out of the factual flow into a named paragraph marking them recorded but unconfirmed, to re-derive before relying on them |

## Divergences between the two repositories

Both repos share an identical `packages/*` set, identical root `package.json`, and identical test-file
counts per package. The differences are all at the root, and all matter for documents shipping publicly:

- GRAPH has `.kiro/`, `docs/`, `repowise/`, `tooling/`, `archive/`, `ui-ideas/`, `node_modules/`,
  `AGENTS.md`, `FABLE_HANDOFF.md`, and a conversation transcript at the root. `repohive-public` has none
  of these.
- `repohive-public` has no installed dependencies and no build output, so it is a source-only clone.
- `fixtures/`: three clone targets in GRAPH's ignore list, one directory actually present publicly.
- The public `.gitignore` already ignores `context/`, so the private mount layout the docs now reference
  is consistent with the repo as it stands.

## Additional findings not claimed by any document

Found while verifying, worth recording because each is a live inconsistency:

1. **Nothing enforces a Node version.** Only `packages/web` declares `engines` (`>=20.0.0`). The root
   declares none. Yet the engine test script needs Node 21+ to expand its glob, and the Node 20 form has
   a false-green mode. The one constraint that would prevent the trap is absent.
2. **Duplicate majors inside one dependency tree.** `recharts` `^2.13.0` in web versus `^3.8.1` in ui;
   `shiki` `^1.22.0` versus `^4.0.0`; `lucide-react` `^0.460.0` versus `^1.7.0`; `tailwind-merge`
   `^2.5.4` versus `^3.5.0`; `@types/node` `20.19.9` root, `^22` web, `^26.1.0` api-client. Nothing
   reconciles these, and a component moved between packages may not behave identically.
3. **TypeScript is pinned 5.9.3 at the root but ranged** `^5.6.0` / `^5.7` in the workspaces, so the pin
   does not govern what compiles them.
4. **Undocumented root tooling:** `shadcn ^4.12.0` in root devDependencies plus a root
   `components.json`, unmentioned by stack.md.
5. **Script-name split:** `typecheck` in engine packages, `type-check` in the four vendored ones, with no
   root script covering the second group.

Items 1 through 4 are now recorded in the refactored docs. Item 5 is documented in stack.md and
verification.md.

## What a human should check

Ordered by consequence. Each needs either a command run or a judgment call I could not make from files
alone.

1. **Re-measure every number in verification.md Gate 2 and Gate 3, in the public repo, after an install
   and build.** All six test counts and both SHA-256 digests currently rest on a single 2026-08-22 run in
   a different working tree. They are labelled as such, but labelling is a stopgap. Until someone runs
   `npm install; npm run build` in a public clone and records the result, the file that defines "done"
   has no verified numbers in it. This is the largest open gap in the report.
2. **Execute the Node 20 versus 21+ glob trap and confirm both failure modes.** The false green is the
   most dangerous single item in these documents, and it is reasoned rather than measured. Confirm
   `node --test dist/` on Node 21+ really does report one passing test, then fix both engine `test`
   scripts. The explicit-file-list workaround is documented as an interim measure, not a fix.
3. **Decide whether to add `engines` to the root manifest.** Finding 1 above. A root `engines` field
   naming the supported range would make the script trap detectable at install time.
4. **Confirm `types` belongs on the ecosystem side of the boundary.** A judgment call I made: the source
   conventions.md listed only `cli`, `web`, `ui`, `api-client` as forbidden imports, and architecture.md
   classified `types` as neither engine nor ecosystem while calling it a leaf dependency. I added `types`
   to the forbidden list in conventions.md, since it is described as serving the viewer and API surface
   and no engine code imports it today (so the rule costs nothing now). If that is wrong, it is a
   one-word revert.
5. **Trace the group-id derivation** and either confirm content-addressing or correct conventions.md.
   Claim 61.
6. **Confirm the semantic-zoom node budget and the client layout's determinism.** Claim 62. Both were
   load-bearing descriptions of the renderer and are now marked unconfirmed.
7. **Decide whether the Vite and `vite-plugin-singlefile` approval is still live.** stack.md records an
   owner ruling dated 2026-08-23, but neither package is in any manifest. Either the work has not started
   or the decision lapsed. The plugin version and its stated Vite compatibility range were not verifiable
   offline.
8. **Determine which parser filesystem seams are actually wired** through `parseProject` versus reachable
   only from tests. Claim 53. It changes how much work "parse from a non-directory source" really is.
9. **Revisit the Next.js justification.** Claim 42. The stated reason is false; the decision may be
   correct for other reasons that should be written down.
10. **Confirm no ported equivalent of `workstreams.md` is expected.** I dropped both pointers rather than
    guess at a `context/` path. If open work now lives at a known location, the two paragraphs in
    architecture.md and stack.md want that pointer restored.
