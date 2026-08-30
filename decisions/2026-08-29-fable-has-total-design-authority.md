---
date: 2026-08-29
slug: fable-has-total-design-authority
title: Fable has total design authority over the viewer; the bar is Awwwards-worthy
status: current
superseded_by: null
supersedes: null
summary: Every visual decision belongs to the design agent, including rewriting the existing canvas from scratch.
corrected: false
---

## What was decided

Design authority over everything visual was granted to the design agent, with a high bar set for the result. The
scope covers the graph viewer, the zoom canvas, node and edge rendering, the layout algorithm, typography, motion,
information architecture and the three existing real surfaces. Rewriting the canvas from scratch is explicitly
permitted.

This is materially broader than the new-component latitude granted in `viewer-handed-to-fable-workstreams-held`,
which it extends. The agent is to work as a senior designer rather than an implementer, is invited to push back on
the brief, and may reject the surfaces it lists in favour of better ones.

## Why

Nothing vendored counts as a design decision. Those components were adopted only to get engine data on screen
quickly, and they carry another product's aesthetic, so treating them as a baseline to preserve would lock the
viewer into choices nobody made for this project.

The anti-re-narrowing clause is itself part of the decision. A future session that finds the brief's suggestions
ignored should read that as intended, not as drift.

## What this constrains

The brief's component inventory is not a work list. Exactly four things survive the full latitude, and all four are
framed as correctness or legal obligations rather than design preferences, so they do not read as interference.
**They must not be softened:**

1. **Never display a number the engine did not record.** The neutral-zero rule still binds. No metric may be
   derived or inferred client-side to fill a gap.
2. **Layout must be deterministic.** Any algorithm is acceptable provided it is seeded and stable, so that the same
   inputs always produce the same visual output. Non-deterministic rendering would undercut the engine's
   determinism claim, which is central to the project, and would make any figure taken from the viewer
   irreproducible.
3. **Accessibility is part of the bar.** In particular, the preserve-versus-reconstruct distinction must not be
   conveyed by colour alone.
4. **Attribution stays accurate** for whatever vendored code remains. Rewriting vendored components aesthetically
   is permitted and does not disturb the licence or attribution obligations recorded in
   `adopt-repowise-ui-under-agpl`.

Do not re-narrow this authority in a future session.

## Provenance

Archive: `DECISIONS.md` L12-L44, `BRAIN.md` L1689-L1728 (RepoHIVE-Archive, frozen)
