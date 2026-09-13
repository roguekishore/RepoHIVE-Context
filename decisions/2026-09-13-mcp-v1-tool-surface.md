---
date: 2026-09-13
slug: mcp-v1-tool-surface
title: MCP v1 tool surface, six read-only tools over one launch-fixed index
status: current
superseded_by: null
supersedes: null
summary: v1 ships six read-only tools (overview, level, find, details, blast radius, region decisions) over one index fixed at launch, with an assessed-framed decision surface
corrected: false
---

# MCP v1 tool surface, six read-only tools over one launch-fixed index

Decided and implemented 2026-09-13 on `wip/mcp` (commits `53b5fe2`, `22c9edc`, `d31a5a2`, `f5d37e0`;
local, unmerged, owner pushes).

## What was decided

`@repohive/mcp` is an ecosystem package that imports `@repohive/core` directly, per the recorded ruling
that the MCP server must not shell out to a CLI. It exposes an already-produced `index/` over stdio MCP.
No new engine exports were required.

**One index per server process, fixed at launch** (`--index <dir>`, positional, or `REPOHIVE_INDEX`;
argv wins over env). Agent hosts configure MCP servers per project, so the index is launch
configuration. Per-call index paths were rejected: they re-litigate a path on every call, cost tokens,
and turn the server into an arbitrary-filesystem-read oracle. Fixing the location at launch means a tool
call can never steer the process to a new filesystem location. Multi-index means multiple config
entries; a registry is hosted-path territory. A missing or invalid index at launch is a stderr warning
rather than a crash, and every tool call then returns the specific error together with the pipeline
commands that would produce an index, so the flow where an agent generates the index mid-session through
its own shell works. Loads are cached against a size and mtime signature of the five files, so a
long-lived server never serves a stale index after a re-group.

## The six tools, ordered by the recorded differentiation

1. **`region_decisions`** - the differentiator. Recorded decisions verbatim (cohesion, coupling,
   modularity, score, action, automaticAction, userOverridden, decisionConfidence, groupIds) plus
   `assessed`, `displayName`, `memberFileCount`, and the boundary/weights/seed context. Filters on
   action, assessed, regionId, groupId, with paging. `groupId` resolves through the node's
   engine-recorded `regionId` only, and fails with a specific message on non-groups and
   provenance-less wrappers rather than guessing. Serves trust calibration (a preserved high-score
   region is an authored boundary that held) and grouping audit.
2. **`blast_radius`** - core's `analyzeBlastRadius` verbatim: impacted set, kind breakdown, containing
   groups with region ids, counts and deterministic truncation. Pre-edit impact scoping.
3. **`hierarchy_at_level`** - every node at one level in canonical order, paged, each with parent,
   childCount, descendantFileCount, leaf attributes, region provenance and the joined decision brief.
   The level-at-a-time idea: an agent reads the architecture one slice at a time instead of 29k nodes,
   and level 1 is the architecture summary.
4. **`find_node`** - case-insensitive substring over id, packagePath, directoryPath, group
   packagePrefix and regionId, with deterministic ranking (exact id, then id substring, then attribute,
   ties by ascending id) and a `matchedOn` field. Agents know paths and class names, not `g_<hash>` ids,
   and every other tool takes ids, so this is the bridge.
5. **`repository_overview`** - counts, depth, perLevel, kind counts, run parameters, resolved
   configuration, and the assessed-only decision summary. The orientation call: gives the agent real
   level numbers before it drills anywhere.
6. **`node_details`** - one node's full record plus direct one-hop edges in both directions. Without it
   the surface could not answer "what does X depend on" at all, because blast radius is transitive and
   dependents-only.

## Rejected for v1

An `index`/`parse`/`group` tool (the recorded scope call restated, not re-argued: fire-and-forget drags
in the hosted job model, and ~14 s warm / ~57 s cold is borderline-to-hostile for interactive tool
timeouts). Per-call index paths and a multi-index registry. A source-text tool: the index records
structure, not code, and agents have their own file tools. Path-finding, centrality, or any derived
graph metric: computation beyond what the engine recorded, which the adapter convention forbids. A
zoom-map projection tool: a viewer display contract, not agent-useful. MCP `outputSchema` /
`structuredContent`: it doubles every schema, and SDK-side output validation turns a shape edge case
into a runtime tool failure; revisit only if a client demonstrably uses it. Composed English labels:
the viewer composes for humans, agents get structured fields.

## The honesty contract

The adapter convention applies to tools exactly as it applies to viewer adapters: read, never compute;
explicit nulls for fields the engine does not emit, never invented values; joins only through
`regionId` / `ordinal` / `groupIds`, with the web route's legacy package-prefix fallback for
pre-Gap-12 indexes deliberately not ported (an old index shows `groupIds: null` instead of a
heuristic); canonical ordering everywhere via core's `compareIds`; deterministic truncation with
explicit flags.

The unassessed-region trap is handled as a labelled derivation. `assessed = !(score === 0 && cohesion
=== 0)` is the recorded rule, applied in one place and emitted adjacent to every score and confidence.
Crucially, **a raw preserve/reconstruct split is unrepresentable in the schema**: the summary type
splits actions only under an `assessed` key, alongside `totalRegions`, `assessedRegions`,
`unassessedRegions` and an always-present note stating the rule and that unassessed confidence is a
formula artifact. `assessed` is also a first-class filter. Documented caveat: the rule is exact only
under the default `degenerateScore` of 0; a run configured otherwise makes unassessed regions
undetectable from emitted fields. That is an engine emission gap, recorded rather than papered over,
and a future index version carrying an explicit flag would supersede this derivation.

## Verified at decision time

Node v26.4.0, Linux: package build exit 0 including a from-scratch rebuild; 27/27 package tests over a
real fixture index generated by the actual pipeline, using an explicit-file-list test script that
cannot go vacuously green; core 153/153 and parser 181/181 unaffected. A live stdio JSON-RPC session
(initialize, tools/list, tools/call success and error paths) was exercised manually. Independently
re-verified by the orchestrator: from-scratch build exit 0, 27/27 tests. The fixture exercises the
unassessed rule (3 of its 4 regions are unassessed) but not the preserve branch or scale: a broadleaf
smoke run is owed before any external demo.
