---
date: 2026-08-23
slug: all-workstreams-run-in-parallel
title: Delivery is time-constrained; all workstreams run in parallel worktrees
status: current
superseded_by: null
supersedes: null
summary: Viewer polish suffices for the near-term deliverable, and every workstream runs concurrently in its worktree.
corrected: true
---

## What was decided

Two owner calls landed together.

First, the work is under a fixed external delivery date. Because the viewer is already implemented, polishing it
with a few more relevant components was judged sufficient for that deliverable, with the choice of components
deliberately deferred at the time.

Second, every workstream now runs concurrently, each in its own worktree. That closed the sequencing question
which had been open for a day: it is no longer a matter of which path goes first, it is all of them at once.

## Why

The scope call on the viewer was driven by the delivery date rather than by engineering need, so it should be
read as a time-constrained judgment about what is presentable, not as a technical finding about the viewer.

The parallelism call stands on its own footing and is the part that survives independently of any delivery
pressure: with the sequencing question closed, no path waits on another.

## What this constrains

- The sequencing question is closed. Do not re-propose an ordering of the forward paths.
- Orchestration is contested between worktrees. Both the CLI path and the hosted path need a parse-then-group
  layer, so if each worktree writes its own the result is two incompatible implementations and an unresolvable
  merge. The recorded mitigation binds: define the orchestration interface before either worktree writes
  orchestration code.
- Memory files serialize across worktrees.

This entry also made `packaged-cli-next-mcp-deferred` non-exclusive: the CLI is still being built, but it is no
longer the only thing being built. That entry is not otherwise reversed.

## Corrections since

**Constraint 2, "do not start the viewer-component brainstorm", was explicitly superseded by
`viewer-handed-to-fable-workstreams-held`.** That later decision lifted the instruction and reopened the
question of which components to build, though it delegated the question to a design agent rather than reopening
it for general discussion. Do not enforce the original prohibition.

The parallel-worktrees decision, the closing of the sequencing question, and the orchestration contention risk
with its mitigation are all uncorrected and still bind. Note separately that the other workstreams were later
paused by that same entry, paused rather than cancelled, so the parallelism is dormant rather than retracted.

## Provenance

Archive: `DECISIONS.md` L374-L401, `BRAIN.md` L1265-L1314 (RepoHIVE-Archive, frozen)
