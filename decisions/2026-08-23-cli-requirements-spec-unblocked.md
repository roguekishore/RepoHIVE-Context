---
date: 2026-08-23
slug: cli-requirements-spec-unblocked
title: The CLI requirements spec is unblocked, surface, names, version and bundler locked
status: current
superseded_by: null
supersedes: null
summary: Four commands with one deferred, install guidance, a 0.x release, and a verified single-file bundler.
corrected: true
---

## What was decided

The four items that had been blocking the CLI requirements spec were closed:

- A four-command surface on one binary, dispatching on its first argument, with a fifth command deferred.
- Those command names, finalized.
- Install guidance recommending a global install, with a no-install alternative.
- A 0.x release, plus a specific single-file bundler plugin, verified for version, licence and stated purpose
  before being adopted.

One sequencing item survives inside the otherwise parallel plan: the orchestration function's signature must be
defined before either the CLI worktree or the hosted worktree writes orchestration code, since two independent
versions would be an unresolvable merge.

## Why

All four items are published surface. Once the first release is out and anyone scripts against the tool, changing
a command name, the dispatch shape, or the version policy is a breaking change for them. Locking these is what
allows the requirements spec to be written at all.

The bundler plugin was checked against the registry before adoption rather than after, which is the standing
pattern for any dependency addition here.

## The version policy carries a disclosed inference

The owner agreed to a 0.x release. **Lockstep single-numbering across all four packages was never stated. It was
inferred from a recommendation being agreed to**, was flagged back for explicit confirmation, and the record notes
that a successor decision is needed if independent versioning was in fact meant.

**That confirmation is still outstanding.** No later decision closes it, and later history entries still list it
as owed. Do not treat lockstep versioning as decided or act as though it binds. Confirming it is one of the first
items due when the held workstreams resume, per `viewer-handed-to-fable-workstreams-held`.

## What this constrains

- The four locked items join the published contract alongside the output directory layout, flag names, JSON output
  shape and exit codes. Changing any of them after the first publish is a major version.
- Define the orchestration signature before any worktree writes orchestration code.

## Corrections since

**Constraint 4 of this entry is void and was explicitly superseded by `recorded-pipeline-timings-were-wrong`.**
That constraint instructed readers not to quote a roughly 20 s figure, and asserted the pipeline ran at roughly
80 s. The later re-measurement found the reverse: the owner's roughly 20 s estimate was right and the agent's
correction of it was wrong. Never repeat constraint 4, and never quote the 80 s figure as live.

The corrected pipeline figures, both labelled as this project requires: **roughly 14 s warm and roughly 57 s
cold.** Never give one without the other, and never let a warm-only figure reach a README or user-facing claim
unlabelled.

The command surface, the finalized names, the install guidance, the 0.x release, the bundler choice and the
orchestration sequencing item are all uncorrected and still bind.

## Provenance

Archive: `DECISIONS.md` L298-L328, `BRAIN.md` L1331-L1369 (RepoHIVE-Archive, frozen)
