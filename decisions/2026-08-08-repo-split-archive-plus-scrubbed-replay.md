---
date: 2026-08-08
slug: repo-split-archive-plus-scrubbed-replay
title: "Repo split: this repo becomes the private archive, a scrubbed replay builds the public one"
status: current
superseded_by: null
supersedes: null
summary: Rename this repo private as the archive; populate a new public repo by replaying scrubbed commits.
corrected: true
---

## What was decided

This repository was to be renamed to an archive name and made private, with a new public repository populated by
replaying scrubbed commits at a paced rate. The three large internal registers, the gap, fix and audit
registers, stay deliberately tracked on the private side.

## Why

The decision was forced by a real leak: three large internal registers, 514 KB in total, were found tracked and
already pushed publicly, because the ignore entries only ever covered the `docs/` copies of those files.

A split was chosen over rewriting this repository's history. Rewriting would have destroyed contribution
history, and it still could not un-publish what was already exposed, so it paid a real cost for no complete
remedy.

## What this constrains

The three large gap, fix and audit registers stay tracked here intentionally, because this is the private side.
Replay commit granularity is one commit per observable sub-behaviour, each independently green, reusing the rule
from `commit-granularity-is-rollback-guarantee`.

## Corrections since

The decision stands. Four things around it moved.

- **The commit arithmetic in this entry, 69 of 99 commits surviving, is stale.** It was revised repeatedly as
  new work accumulated. `replay-classification-by-post-filter-paths` (2026-08-22) records totals in this area as
  volatile, 56 then 57, and `replay-does-not-gate-development` (2026-08-23) makes the rule explicit: whoever
  next runs the replay must recount the expected commit total rather than trust the recorded number, and must
  not apply on an unexpected count. Do not treat 69 of 99 as a current figure.
- **The scrubbing approach needed a mechanical correction of the same class as the original leak.**
  `replay-classification-by-post-filter-paths` found that a commit's replay disposition must come from which
  paths survive the filter, never from its subject wording, and that root-level internal files must be named
  individually in the path filter. A documentation-titled commit wrote a file at the repository root, outside
  the filtered directory, so 360 lines of internal brief survived. Any commit assumed to self-empty must be
  confirmed empty in a dry run first. `public-replay-branch-topology-and-scrubbing` (2026-08-22) settled the
  replay's branch topology, its literal-pair vocabulary scrubbing, and its one-segment-per-calendar-day timing.
- **The archive repository stayed public for some time after this decision.** That was tracked as an urgent
  open item, not as a reversal of this decision. `repo-posture-fable-work-default` (2026-08-23) later put the
  archive repository's visibility out of scope for workstream planning, while being explicit that the fact must
  not be deleted from the record. On the deliberately tracked registers, that same entry leaves one item
  deferred rather than resolved: which copy of the duplicated registers wins is an open owner call, and nothing
  may be deleted in the duplicate case.
- **The private side is now frozen, not merely private.** `development-moves-to-public-repo` (2026-08-28) moves
  all further coding to the public repository. The archive keeps the full history and all private material, and
  receives no new work.

One further caveat carries over from `commit-granularity-is-rollback-guarantee`: because the replay reuses that
entry's granularity rule, and because `npm-test-not-a-green-gate` (2026-08-22) found a root `npm test` run was
never a valid green gate, historical claims that a replayed commit was independently green are unreliable even
though the rule itself stands.

## Provenance

Archive: `DECISIONS.md` L823-L836, `BRAIN.md` L429-L466 (RepoHIVE-Archive, frozen)
