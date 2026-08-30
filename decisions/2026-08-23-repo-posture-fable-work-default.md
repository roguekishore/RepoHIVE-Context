---
date: 2026-08-23
slug: repo-posture-fable-work-default
title: Repo posture, fable-work is the default branch, no merge, git plans out of scope
status: current
superseded_by: null
supersedes: null
summary: The working branch is treated as default with no merge planned; git and replay plans are out of scope.
corrected: true
---

## What was decided

The working branch is treated as the default branch, and no merge to the main branch will happen. Branch
placement of memory and documentation commits is set aside as a non-concern. The git plans and the public-repo
replay plans are placed outside workstream planning entirely.

Two items are explicitly deferred pending an owner call rather than resolved: a systematic steering-drift audit,
and which copy of some duplicated registers wins. Neither is settled.

## Why

Three flags kept recurring and were consuming attention without changing any outcome: that memory changes belong
on the main branch, that a merge decision was pending, and that the replay or the archive repo's visibility were
workstream blockers. Ruling the branch posture settled and the git plans out of scope stops all three at once.

## What this constrains

- Stop flagging that memory and documentation changes belong on the main branch.
- Stop surfacing the replay or the archive repo's visibility as workstream blockers.
- Nothing may be deleted in the duplicate-register case. The duplication stands until the owner picks a winner.
- The archive repo's public exposure stays on the record. This decision is explicit that the fact must not be
  deleted, even though it is deliberately out of scope for path planning.

This entry sets aside the "memory and state files belong on main" clause of `memory-and-logging-conventions`. The
conventions document still says so, but the owner has overridden it.

## Corrections since

**`development-moves-to-public-repo` (2026-08-28) freezes this repository entirely, which makes this
default-branch posture moot in practice.** That later decision does not name this entry and does not claim to
supersede it, so no supersession link is asserted here. The relationship is recorded on both entries and needs
owner confirmation before it is upgraded to a formal supersession. Treat the practical effect as real, and leave
the link question open.

The two deferred items above are unaffected by that freeze and remain owed.

## Provenance

Archive: `DECISIONS.md` L329-L346, `BRAIN.md` L1265-L1314 (RepoHIVE-Archive, frozen)
