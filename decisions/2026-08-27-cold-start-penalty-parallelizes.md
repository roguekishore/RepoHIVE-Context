---
date: 2026-08-27
slug: cold-start-penalty-parallelizes
title: The cold-start penalty is per-file read latency and parallelizes 6.8x
status: current
superseded_by: null
supersedes: null
summary: The directory walk is innocent; the whole penalty is per-file read latency, and concurrency 16 gives 6.8x.
corrected: false
---

## What was measured

Three fresh copies of the same source files were probed, with the directory walk timed separately from the file
reads. The walk is not implicated at all: it is identical cold and warm, so the source collector needs no
optimization. The entire cold penalty is per-file read latency, serialized across thousands of sequential reads.

Because the cost is waiting rather than computing, it parallelizes. A concurrency of 16 gave a 6.8x improvement on
the cold case, while 64 bought nothing further.

**This entry records a measurement, not a decision.** No workaround has been chosen and none has been
implemented. What binds is the design constraint below, which applies to whatever workaround is eventually
selected.

## Why

Waiting on first access is latency, not CPU work, so overlapping the waits recovers most of the loss. The
diminishing return past 16 is consistent with that: once enough reads are outstanding to keep the device busy,
adding more only adds bookkeeping.

An antivirus exclusion was explicitly refused as user-facing guidance. The tool's purpose is indexing
repositories a user has just cloned from the internet, which is precisely the case where scanning is warranted.

## What this constrains

- Any prefetch must fetch concurrently and then run the existing extraction loop sequentially in canonical order.
  **Any design that lets read-completion order reach the graph is forbidden.** Determinism here is guaranteed by
  structure rather than by testing: only *when* the bytes are fetched changes, while extraction order does not, so
  byte-identical output follows by construction.
- Use a concurrency of roughly 16, and bound the read-ahead.
- Never recommend an antivirus exclusion to users.

## Limits recorded with the measurement

- **A probe defect is disclosed.** A byte counter raced across async workers, so concurrent runs under-report
  character counts. Timing figures are unaffected.
- **Content-hash caching and snapshot ids do not address this.** The cold case is the first index of a repository,
  which is exactly the case no cache can have warmed.
- **A warm parse is roughly 85% CPU**, which caps what any prefetch can achieve on the warm path.
- A later session pinned the injection point for a prefetch, alongside that CPU figure.

## A live input to the source-provider seam

Parsing from an archive stream eliminates this penalty rather than mitigating it, because the files are never
written out and read back. That makes extract-then-walk versus stream-from-archive a real, open choice for the
source-provider seam spec, not a detail to settle later.

## Provenance

Archive: `DECISIONS.md` L123-L176, `BRAIN.md` L1507-L1557, L1559-L1597 (RepoHIVE-Archive, frozen)
