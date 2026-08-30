---
date: 2026-07-07
slug: git-milestones-are-owner-driven
title: Git milestone operations are owner-driven, not agent-driven
status: current
superseded_by: null
supersedes: null
summary: Merges to main, tags, and branch creation or deletion are the owner's to run, never done unprompted.
corrected: false
---

## What was decided

Milestone git operations belong to the owner. Merges to the main branch, tags, and branch creation or deletion
are never performed by an agent unprompted. Ordinary commits are fine when asked for.

## Why

An agent performed a `phase-1-parser` to `main` `--no-ff` merge plus a tag and a new branch, all local and
never pushed, and the whole thing was reverted at the owner's request. The owner had asked only whether the
parser features were solid enough to proceed. A question asking for an assessment is not an instruction to
execute a workflow.

## What this constrains

Ordinary commits are fine when asked. A merge, tag, or branch create or delete is never run unprompted,
including when a question about readiness could be read as authorizing it.

## Provenance

Archive: `DECISIONS.md` L930-L939, `BRAIN.md` L298-L317 (RepoHIVE-Archive, frozen)

Still live and consistent with every later git decision. The 2026-08-23 `repo-posture-fable-work-default`
entry reinforces it by putting merge decisions out of scope entirely.
