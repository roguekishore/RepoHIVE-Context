---
date: 2026-07-07
slug: memory-and-logging-conventions
title: Memory, commit and logging conventions established
status: current
superseded_by: null
supersedes: null
summary: Commit type convention, 24-hour real-clock timestamps, user-triggered commit-assist, vault rebinding.
corrected: true
---

## What was decided

Four conventions settled across a span of days. Commit subjects distinguish product types
(`feat`/`fix`/`test`/`refactor`/`chore`) from a `kiro(...)` meta type covering specs, hooks and project
memory. Log entries carry 24-hour `YYYY-MM-DD HH:mm` stamps read from the real system clock. A user-triggered
commit assistant was chosen over automatic post-task commits. A memory MCP found misbound to a company vault
was rebound.

## Why

Timestamps moved to the real clock because a single conversation spans several real days, and entries had been
stamped with the conversation's start date instead. The verify-writes rule came from evidence: a prior
session's claimed notes were found never to have persisted, so a claimed write is not trusted until it is
confirmed to have landed.

## What this constrains

Commit subjects separate product types from the meta type. Every log entry is stamped from the real system
clock, not the conversation date. A claimed write must be verified to have landed rather than taken on trust.

## Corrections since

Two clauses were overtaken:

- "Memory and state files belong on main" was set aside on 2026-08-23 by `repo-posture-fable-work-default`.
  The convention document still says so, but the owner overrode it, and branch placement of memory and
  documentation commits must stop being flagged.
- The commit-assist *hook* was deleted on 2026-08-22 by `skills-hold-procedure-hooks-only-trigger`. The
  commit-assist *skill* survives, so the user-triggered assist still exists, as a skill rather than a hook.

The timestamp rule and the verify-writes rule still bind.

## Provenance

Archive: `DECISIONS.md` L940-L951, `BRAIN.md` L173-L204, L244-L261 (RepoHIVE-Archive, frozen)

Recorded at medium confidence. The source heading is a date range covering 2026-07-04 through 2026-07-07;
this entry is dated to the range end, when the last of its four items landed.
