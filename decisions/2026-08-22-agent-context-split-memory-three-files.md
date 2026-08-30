---
date: 2026-08-22
slug: agent-context-split-memory-three-files
title: "Agent context split from narrative; memory split into three files"
status: current
superseded_by: null
supersedes: null
summary: "Steering carries only system facts and protocol; narrative and audience material moved out; memory split."
corrected: false
---

## What was decided

Steering was rebuilt to carry only system facts and protocol. All audience-facing narrative and all
presentation material was moved into separate folders explicitly marked as not agent context.

Memory was split into three files with three distinct write modes: a short snapshot that is rewritten in
place, an append-only decisions log, and an append-only history.

## Why

The always-on context was organised around positioning and external milestones rather than around the system,
and that had two concrete costs.

It was actively suppressing engineering work. The context told agents not to build CLI packaging, MCP or
multi-language support "early", and presentation-honesty rules were being read as engineering ceilings rather
than as reporting standards.

It was also factually stale. It described a five-package layout, with libraries the repo no longer used.

## What this constrains

- Steering is for facts that hold regardless of the task, and every such fact must be verifiable against the
  code.
- Vision, competitive comparisons and claim wording live outside steering.
- Neither of those folders may be loaded to decide what to build.

The three write modes are load-bearing: the snapshot is rewritten, the decisions log and the history are
append-only. The project's whole decision record depends on that structure holding.

## Provenance

Archive: `DECISIONS.md` L745-L770, `BRAIN.md` L658-L716 (RepoHIVE-Archive, frozen)

Wording note: the archive entry names its destination folder after external-audience deliverables, using
framing this project is removing from its engineering record. The destination is described here by its function
instead, not by its original folder name. The rule itself is unchanged.
