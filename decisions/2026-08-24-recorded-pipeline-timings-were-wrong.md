---
date: 2026-08-24
slug: recorded-pipeline-timings-were-wrong
title: The recorded pipeline timings were wrong by up to 9x; every figure derived from them is void
status: current
superseded_by: null
supersedes: null
summary: The 2026-08-22 wall-clock figures are not reproducible; re-measurement put the pipeline at ~14 s warm.
corrected: true
---

## What was decided

The wall-clock figures recorded on 2026-08-22 were found not reproducible, and were superseded by re-measurement
on the same machine and the same fixtures, three runs each. Errors ran from roughly 1.7x to 9x high, with the full
pipeline landing near a quarter of the recorded figure. Every figure derived from that set is void.

Two claims built on the bad numbers are declared FALSE and must not be repeated: that parse dominates group 6:1,
and that parse is where parallelism would pay. Six downstream conclusions were corrected in the same pass.

## Why

The output was byte-for-byte identical to the recorded values in every respect. Node, edge, region and decision
counts all matched, and were stable across runs. That identity is what proves this a measurement defect rather
than a code regression: the code was doing the same work, and only the timing of it was misreported.

The leading explanation at the time was cold filesystem cache on first-ever runs, since run one was slowest in
every set measured and the error scaled with file count. It could not be proven retroactively from the original
data, and was recorded as a hypothesis rather than a finding.

## What this constrains

- These figures are void and must never be quoted as live: parse broadleaf 68.3 s, group broadleaf 11.3 s, parse
  vantage 4.7 s, and the roughly 80 s pipeline.
- Never record a first-ever run as a representative timing. Measure three runs and report the range or median.
- This decision **explicitly supersedes constraint 4 of `cli-requirements-spec-unblocked`**, which had instructed
  readers not to quote roughly 20 s and had asserted roughly 80 s. The owner's roughly 20 s estimate was right and
  the agent's correction of it was wrong.
- `live-indexing-is-a-product-requirement` is declared **strengthened**, not weakened. Its argument that a full run
  is watchable, so no queue, broker or worker fleet is needed, holds better at the corrected figure than at the
  void one.
- The sweep-time argument for keeping pipeline stages separately callable is now weak, but **the decision to keep
  them separately callable stands** on durable grounds: a spec requirement for boundary sweeps without code
  changes.

## Corrections since

**The quoting rule recorded here was warm-only and has since been tightened.** This entry said to quote the
corrected warm figures. `root-cause-first-access-file-latency`, later the same day, made the rule stricter:
always quote two numbers, cold and warm, never one. A user's first run is cold, so no warm figure may reach a
README or any user-facing claim unlabelled.

The corrected figures, both labelled: **roughly 14 s warm and roughly 57 s cold.** Quoting roughly 14 s on its own
is not sufficient.

**The cold-cache explanation recorded here was an unproven hypothesis and has since been closed.** That same later
entry reproduced the anomaly on demand and pinned it to roughly 15 ms of first-access latency per newly-written
file, which is a narrower and better-evidenced mechanism than cold page cache on small files.

The measurement-defect conclusion, the list of void figures, the two FALSE claims, the three-run rule and the
supersession of the CLI spec's constraint 4 are all uncorrected and still bind.

## Provenance

Archive: `DECISIONS.md` L225-L278, `BRAIN.md` L1402-L1458 (RepoHIVE-Archive, frozen)
