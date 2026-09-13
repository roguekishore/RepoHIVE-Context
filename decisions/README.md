# Decisions

One file per decision. This index is **generated** by `gen-index.py` from each file's
frontmatter. Do not hand-edit it; regenerate it instead, so it cannot drift from the files.

38 decisions across 16 dates: **37 current**, **1 superseded**. **19 carry later corrections.**

## How to read this

A `current` status does **not** mean nothing in the file was corrected. This project's
norm is partial supersession: a later decision retracts one named constraint while the rest
of the decision stands. Files marked **(corrected)** below carry a `Corrections since`
section, and you must read it before acting on them.

Load only the decisions that bear on your task. Open them by path: this directory sits
inside a git-ignored mount, so it is invisible to ripgrep-backed search tools.

## 2026-06-22

- [Foundational stack, algorithm and positioning choices](2026-06-22-foundational-stack-and-algorithm-choices.md) **(corrected)**  
  TypeScript/Node, Tree-Sitter, JSON files; structural adaptive per-region grouping, never embeddings.

## 2026-07-07

- [Git milestone operations are owner-driven, not agent-driven](2026-07-07-git-milestones-are-owner-driven.md)  
  Merges to main, tags, and branch creation or deletion are the owner's to run, never done unprompted.
- [Memory, commit and logging conventions established](2026-07-07-memory-and-logging-conventions.md) **(corrected)**  
  Commit type convention, 24-hour real-clock timestamps, user-triggered commit-assist, vault rebinding.

## 2026-07-11

- [Determinism primitives are built first, always](2026-07-11-determinism-primitives-built-first.md) **(corrected)**  
  Canonical ordering and content-addressed stable ids were built before any algorithm stage.

## 2026-07-23

- [Phase 2 grouping engine merged to main](2026-07-23-phase-2-merged-to-main.md) **(corrected)**  
  The grouping engine landed one commit per spec task, with 79 core tests covering 33 properties.

## 2026-08-05

- [Adopt repowise's UI under AGPL instead of building a viewer](2026-08-05-adopt-repowise-ui-under-agpl.md) **(corrected)**  
  Four repowise packages vendored whole; repo relicensed MIT to AGPL-3.0-or-later as the accepted cost.
- [Close every engine gap before building the viewer](2026-08-05-close-every-gap-before-viewer.md) **SUPERSEDED** by `wave-b-closed-pivot-to-viewer` **(corrected)**  
  All 22 gaps were to close across four sequential branches before any viewer work began.
- [Commit granularity is a rollback guarantee](2026-08-05-commit-granularity-is-rollback-guarantee.md) **(corrected)**  
  One commit per observable sub-behaviour, each independently building and passing, replacing one-per-gap.
- [Viewer requirements spec written; Gap 12 promoted into it](2026-08-05-viewer-requirements-spec-gap-12.md)  
  The hierarchical-graph-viewer spec was written requirements-only; Gap 12 became Requirement 3.

## 2026-08-06

- [Wave A closed; signal enrichment made the adaptive branch fire on real Java](2026-08-06-wave-a-signal-enrichment-closed.md)  
  Gaps 16, 1a and 1c resolved, taking vantage from preserve 0/20 to 10/10 as edges went 128 to 341.

## 2026-08-08

- [README ships in two stages, and NOTICE is required](2026-08-08-readme-two-stages-notice-required.md)  
  A minimal MIT-era README lands first; the AGPL section and NOTICE land with the vendored packages.
- [Repo split: this repo becomes the private archive, a scrubbed replay builds the public one](2026-08-08-repo-split-archive-plus-scrubbed-replay.md) **(corrected)**  
  Rename this repo private as the archive; populate a new public repo by replaying scrubbed commits.

## 2026-08-09

- [Wave B closed; then pivot to the viewer before the remaining engine gaps](2026-08-09-wave-b-closed-pivot-to-viewer.md)  
  Wave B complete; the viewer is built next for a visible end-to-end result, ahead of waves C and D.

## 2026-08-16

- [Engine waves C and D closed, plus the viewer finish](2026-08-16-engine-waves-c-and-d-closed.md) **(corrected)**  
  All 22 gaps closed; the group-to-region package-prefix heuristic was removed in favour of real provenance.

## 2026-08-22

- [Agent context split from narrative; memory split into three files](2026-08-22-agent-context-split-memory-three-files.md)  
  Steering carries only system facts and protocol; narrative and audience material moved out; memory split.
- [Live indexing of public repos is a product requirement, not an option](2026-08-22-live-indexing-is-a-product-requirement.md) **(corrected)**  
  The hosted surface must demonstrate paste-a-URL live indexing; a pre-indexed-only deployment is insufficient.
- [npm test is not a valid green gate until the engine runner is version-independent](2026-08-22-npm-test-not-a-green-gate.md)  
  Neither test-runner form works on both Node 20 and 21+, so every historical green claim was unreliable.
- [The packaged CLI is the next workstream; MCP is deferred behind it](2026-08-22-packaged-cli-next-mcp-deferred.md) **(corrected)**  
  packages/cli is built next and the MCP server is deferred, as a sequencing choice not a reversal.
- [Public replay: branch topology, and internal vocabulary stripped at the filter](2026-08-22-public-replay-branch-topology-and-scrubbing.md)  
  Later segments replay onto real feature branches; internal vocabulary is stripped from commit messages.
- [Replay classification goes by post-filter paths, never by commit subject](2026-08-22-replay-classification-by-post-filter-paths.md)  
  A commit's replay disposition comes from which paths survive the filter, not from its subject wording.
- [Skills hold procedure; hooks only trigger, and one hook survives](2026-08-22-skills-hold-procedure-hooks-only-trigger.md)  
  Anything an agent can be asked to do is a skill; a hook exists only for what must fire unasked.

## 2026-08-23

- [Delivery is time-constrained; all workstreams run in parallel worktrees](2026-08-23-all-workstreams-run-in-parallel.md) **(corrected)**  
  Viewer polish suffices for the near-term deliverable, and every workstream runs concurrently in its worktree.
- [CLI distribution, output directory and packaging shape locked](2026-08-23-cli-distribution-output-and-packaging.md) **(corrected)**  
  Output goes to a dot-prefixed project directory with an override flag; four packages publish, CLI depends.
- [The CLI requirements spec is unblocked, surface, names, version and bundler locked](2026-08-23-cli-requirements-spec-unblocked.md) **(corrected)**  
  Four commands with one deferred, install guidance, a 0.x release, and a verified single-file bundler.
- [The CLI's shipped viewer is the hierarchical viewer only](2026-08-23-cli-ships-hierarchical-viewer-only.md) **(corrected)**  
  The CLI artifact carries only the semantic-zoom viewer, built as a purpose-made single-page bundle.
- [Everything ships from the public repo; no private deployment](2026-08-23-everything-ships-from-public-repo.md)  
  Engine, viewer and any hosted instance all ship from the public repo; no closed-source deployment exists.
- [The four forward paths get one tracked register](2026-08-23-four-forward-paths-tracked-register.md) **(corrected)**  
  One tracked register is authoritative for the four post-engine paths' scope, blockers and estimates.
- [Internal seams are retrofittable; the published CLI surface is not](2026-08-23-internal-seams-retrofittable-surface-not.md)  
  Only orchestration is a CLI prerequisite; the other three seams retrofit safely behind existing functions.
- [The public-repo replay does not gate development](2026-08-23-replay-does-not-gate-development.md)  
  The replay is an independent packaging exercise and blocks no workstream; new work may be committed freely.
- [Repo posture, fable-work is the default branch, no merge, git plans out of scope](2026-08-23-repo-posture-fable-work-default.md) **(corrected)**  
  The working branch is treated as default with no merge planned; git and replay plans are out of scope.
- [Steering's tool lists are extensible, not boundaries](2026-08-23-steering-tool-lists-are-extensible.md)  
  Tool and dependency lists in steering are not hard boundaries; new tools are admitted when work demands it.

## 2026-08-24

- [The recorded pipeline timings were wrong by up to 9x; every figure derived from them is void](2026-08-24-recorded-pipeline-timings-were-wrong.md) **(corrected)**  
  The 2026-08-22 wall-clock figures are not reproducible; re-measurement put the pipeline at ~14 s warm.
- [Root cause of the bad timings, first-access cost on freshly-written files, ~15 ms/file](2026-08-24-root-cause-first-access-file-latency.md)  
  A reproducible experiment pinned the anomaly to ~15 ms of first-access latency per newly-written file.

## 2026-08-27

- [The cold-start penalty is per-file read latency and parallelizes 6.8x](2026-08-27-cold-start-penalty-parallelizes.md)  
  The directory walk is innocent; the whole penalty is per-file read latency, and concurrency 16 gives 6.8x.

## 2026-08-28

- [Development moves to the public repo; this repo is frozen as the archive](2026-08-28-development-moves-to-public-repo.md)  
  All further coding happens in the public repo; the archive keeps full history and stops receiving work.

## 2026-08-29

- [Fable has total design authority over the viewer; the bar is Awwwards-worthy](2026-08-29-fable-has-total-design-authority.md)  
  Every visual decision belongs to the design agent, including rewriting the existing canvas from scratch.
- [Viewer handed to Fable; all other workstreams on hold; new components are in scope](2026-08-29-viewer-handed-to-fable-workstreams-held.md) **(corrected)**  
  The viewer is handed over with a written brief as its authority; every other workstream pauses, not cancels.

## 2026-09-13

- [Engine tests run through an explicit file-enumerating launcher](2026-09-13-engine-test-launcher.md)  
  Engine test scripts call scripts/run-node-tests.mjs, which enumerates dist/*.test.js, fails on zero files, and spawns node --test with the explicit list
