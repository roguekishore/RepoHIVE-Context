---
date: 2026-08-24
slug: root-cause-first-access-file-latency
title: Root cause of the bad timings, first-access cost on freshly-written files, ~15 ms/file
status: current
superseded_by: null
supersedes: null
summary: A reproducible experiment pinned the anomaly to ~15 ms of first-access latency per newly-written file.
corrected: false
---

## What was decided

Copying the same source files to a fresh path and parsing the copy three times reproduced the timing anomaly on
demand: the first run took roughly eight times the second and third. That closes the open question the earlier
correction the same day had left as a hypothesis.

Reading all the files warm costs a fraction of a second, so input/output is a few percent of a normal parse. The
extra time on a first run works out to roughly 15 ms per file on first access.

The parser itself needs no optimization. Its real work is roughly 2 ms per file.

## Why

15 ms per file is far too much for a page-cache miss on small files, but it matches the magnitude of on-access
malware scanning of newly created files.

**The attribution limit is explicit and must be preserved.** The first-access penalty is proven and measured.
Antivirus specifically is the *leading* explanation, not a demonstrated one, because isolating it would need an
exclusion test requiring administrator rights and a change to a security setting, which was deliberately not
done. Do not state the cause as established.

## What this constrains

- Always quote two numbers, cold and warm, never one. For the pipeline those are roughly 57 s cold and roughly
  14 s warm.
- A user's first run is cold, so a cold-sized first index is the honest number. No warm figure may reach a README
  or any user-facing claim unlabelled.
- Any figure reaching durable memory needs a history entry stating how it was obtained.
- The assumption that a Linux host escapes this penalty must be measured, not relied upon.

A later measurement session localized the penalty further, finding the directory walk innocent and the whole cost
in per-file reads. See `cold-start-penalty-parallelizes`.

## Provenance

Archive: `DECISIONS.md` L177-L224, `BRAIN.md` L1460-L1505 (RepoHIVE-Archive, frozen)
