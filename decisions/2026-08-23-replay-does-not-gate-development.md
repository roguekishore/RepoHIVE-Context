---
date: 2026-08-23
slug: replay-does-not-gate-development
title: "The public-repo replay does not gate development"
status: current
superseded_by: null
supersedes: null
summary: "The replay is an independent packaging exercise and blocks no workstream; new work may be committed freely."
corrected: false
---

## What was decided

The replay of history into the public repo is independent of ongoing development and is not a blocker for
starting any workstream. New work may be committed freely without first draining the replay.

This directly retires constraint 5 of `packaged-cli-next-mcp-deferred`, which had made the unresolved replay
conflict gate where new work could land. Only that constraint is retired; the rest of that entry stands.

## Why

The replay is a packaging exercise running on a separate track from development. Nothing in the engine or the
product depends on its state, so letting it gate new commits was cost with no corresponding safety.

## What this constrains

- New work may land without first draining the replay.
- The mechanical hazard behind the original conflict is unchanged and still real: the replay script asserts an
  expected commit total, and new commits move that number. So whoever next runs the replay must recount the
  expected total rather than trusting the recorded figure, and must not apply on an unexpected count.

The hazard **moved rather than vanished**. The gate shifted from "before development" to "before replaying".
That is not a formality: this is exactly the assertion that later caught three commits that would otherwise
have leaked internal content into the public repo.

## Provenance

Archive: `DECISIONS.md` L482-L499, `BRAIN.md` L1134-L1185 (RepoHIVE-Archive, frozen)
