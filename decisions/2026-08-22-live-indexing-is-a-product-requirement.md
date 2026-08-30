---
date: 2026-08-22
slug: live-indexing-is-a-product-requirement
title: "Live indexing of public repos is a product requirement, not an option"
status: current
superseded_by: null
supersedes: null
summary: "The hosted surface must demonstrate paste-a-URL live indexing; a pre-indexed-only deployment is insufficient."
corrected: true
---

## What was decided

The hosted surface must demonstrate live indexing: paste a public repo URL, watch it index, browse the result,
with no signup required for public repos. A deployment that can only show pre-indexed repositories is not
sufficient.

## Why

The decision rested on wall-clock measurement suggesting that a full pipeline run is a watchable operation
rather than a batch job. If a user can watch a run finish, the queue, broker and worker-fleet architecture
sketched earlier is unnecessary.

That premise was measured wrong, but the conclusion survived re-measurement and is in fact stronger now. See
"Corrections since".

## What this constrains

Several engine consequences follow from making live indexing a requirement:

- A source-provider seam, so the parser no longer requires a local directory.
- Storage behind an interface.
- Content-addressed snapshot ids, so a given repo is indexed once ever.
- Grouping must not run on the request thread, because it is synchronous and CPU-bound.
- Progress is a first-class engine output, because the recorded per-region decision is the demonstration
  itself.
- The public endpoint needs guard rails before it ships.

## Corrections since

**The pipeline timing premise is void.** This entry justified itself with a pipeline figure of roughly 80
seconds. `recorded-pipeline-timings-were-wrong` disproved that figure as about 5.7x high. Never repeat the ~80 s
premise. The corrected figures are approximately **14 s warm** and approximately **57 s cold**; every timing in
this project must carry a cold or warm label, since the two differ by roughly 8x.

That correcting entry states explicitly that this decision is *strengthened* rather than weakened: "a full run
is watchable, so no queue is needed" holds better at ~14 s warm than it ever did at ~80 s.

**The source-provider cost estimate was also corrected.**
`four-forward-paths-tracked-register` found that the parser reaches the filesystem in three
injectable-but-unwired places plus a required directory string, not at a single injection point. Swapping the
dependency collector alone will not admit tarballs. The source is explicit that this is a cost correction and
not a supersession: the seam decision stands, only its estimated effort moves.

## Provenance

Archive: `DECISIONS.md` L539-L579 (RepoHIVE-Archive, frozen)

No history-file provenance exists for this entry, and that absence is itself a recorded finding rather than a
gap in the reconstruction: the session that produced these measurements wrote no history entry at all, so its
method was unrecoverable and had to be reconstructed experimentally days later.

Confidence on this entry is **medium**. The date comes from the decisions file; its position within 2026-08-22
is inferred from file order rather than from a timestamp, because there is no history counterpart to date it
against.
