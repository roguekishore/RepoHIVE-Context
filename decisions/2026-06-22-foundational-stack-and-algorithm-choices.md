---
date: 2026-06-22
slug: foundational-stack-and-algorithm-choices
title: Foundational stack, algorithm and positioning choices
status: current
superseded_by: null
supersedes: null
summary: TypeScript/Node, Tree-Sitter, JSON files; structural adaptive per-region grouping, never embeddings.
corrected: true
---

## What was decided

Nine numbered choices were recorded together as the project's foundation, and they are kept together here.
The stack is TypeScript/Node rather than a JVM stack. Parsing is Tree-Sitter with Java first, the parser
stitching per-file ASTs into a cross-file graph. Storage is plain JSON files, with no database. The central
technical claim is adaptive per-region preserve-vs-reconstruct grouping, decided from structure alone.
Embeddings are admissible for search and naming, but never for group membership. Command names given in this
entry were explicit placeholders.

## Why

TypeScript/Node was chosen because npx, CLI, MCP and editor distribution is the goal, and a Spring Boot
service cannot be packaged as an easy CLI. Java was chosen as the first language because its explicit imports
make static cross-file resolution tractable. JSON files are sufficient because the data is small and the
pipeline is a stateless file handoff. Embeddings are excluded from membership because embedding-based grouping
is irreproducible, and because using them would make the central claim circular.

## What this constrains

This binds the whole engine. Packaging drives the language choice. Group membership is never
embedding-derived. The JSON contract is the seam that keeps the CLI, MCP, editor and hosted surfaces open with
no engine rework.

## Corrections since

Nothing central was reversed. Three clauses were refined:

- The five-package layout recorded in early history became eight packages. The ledger does not attribute this
  to a named decision. As late as 2026-08-22, `agent-context-split-memory-three-files` records that always-on
  steering was still describing the five-package layout with libraries the repo no longer used.
- React Flow was dropped by `adopt-repowise-ui-under-agpl` (2026-08-05), which vendored four repowise packages
  instead of building a viewer.
- The placeholder command names were finalized on 2026-08-23 by `cli-requirements-spec-unblocked`, and are now
  part of the published CLI contract.

The language choice, Tree-Sitter, the JSON-files storage decision, and the structure-only membership rule all
stand as recorded.

## Provenance

Archive: `DECISIONS.md` L952-L984, `BRAIN.md` L59-L100 (RepoHIVE-Archive, frozen)
