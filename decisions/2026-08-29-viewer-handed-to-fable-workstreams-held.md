---
date: 2026-08-29
slug: viewer-handed-to-fable-workstreams-held
title: Viewer handed to Fable; all other workstreams on hold; new components are in scope
status: current
superseded_by: null
supersedes: null
summary: The viewer is handed over with a written brief as its authority; every other workstream pauses, not cancels.
corrected: true
---

## What was decided

The viewer was handed to a design agent, with a written brief as the authoritative document for that work. Every
other workstream, the CLI, the seams, MCP and the hosted path, was paused mid-planning.

**Those workstreams are paused, not cancelled, and all of their recorded decisions still stand.** They resume only
on an explicit owner call. When they do, the first two items are confirming the versioning policy and defining the
orchestration signature.

The handover also cleared the design agent to build genuinely new components rather than only adapt vendored ones.

## Why

The trigger was schedule: the work is under a fixed external delivery date, and concentrating effort on the viewer
was the owner's call about what to deliver first.

The engineering reason is independent of that and is the stronger one. The reuse-only framing was too narrow. The
vendored components were built for a different product, and none of them was designed to surface a
preserve-versus-reconstruct decision, because no other tool makes one. So the surfaces that demonstrate this
project best simply do not exist in the vendored set, and restricting the work to adaptation would have ruled out
exactly the views that show what the engine does.

## What this constrains

- The handoff brief is authoritative for viewer work, wherever that brief ends up living.
- New components go in a separate namespace. Never inside vendored folders.
- **Components must not derive metrics the engine did not record.** This is a correctness constraint, not a matter
  of taste.
- One honest UI limit binds: a boundary slider may show which regions would flip, but never a recomputed
  hierarchy.

The four constraints attached to this handoff guard correctness rather than taste.

## Two open items carried forward

**The versioning policy is unconfirmed.** `cli-requirements-spec-unblocked` recorded a 0.x release as decided, but
single-number lockstep across all four packages was *inferred* from a recommendation being agreed to rather than
stated, and was flagged back for explicit confirmation. That confirmation never arrived, and it is still listed as
owed here. Do not treat lockstep versioning as decided.

**The brief's placement is unresolved, and this decision flags it rather than solving it.** The brief was written
into the repository that `development-moves-to-public-repo` froze as the archive, it is untracked there, and the
destination repository has no matching directory. No cross-repo copy was made.

## Corrections since

**The latitude granted here was materially broadened the same day by `fable-has-total-design-authority`.** This
decision granted new-*component* latitude. That later decision covers the existing canvas, node and edge design,
layout, typography, motion, information architecture and the three existing real surfaces, and explicitly permits
rewriting the canvas from scratch. Do not read this entry as confining the design agent to adding new components
alongside untouched vendored ones, and do not re-narrow the authority: that later entry contains an explicit
anti-re-narrowing clause.

This entry itself **explicitly supersedes constraint 2 of `all-workstreams-run-in-parallel`**, the
instruction not to start the viewer-component brainstorm. That instruction is lifted, though the question is now
delegated to the design agent rather than reopened for general discussion.

## Provenance

Archive: `DECISIONS.md` L45-L87, `BRAIN.md` L1641-L1687 (RepoHIVE-Archive, frozen)
