---
date: 2026-08-23
slug: steering-tool-lists-are-extensible
title: Steering's tool lists are extensible, not boundaries
status: current
superseded_by: null
supersedes: null
summary: Tool and dependency lists in steering are not hard boundaries; new tools are admitted when work demands it.
corrected: false
---

## What was decided

The tool and dependency lists in the project's steering documents are not hard boundaries. New tools may be added
when the work genuinely demands it. A "not used, do not reintroduce" line is to be read as "do not swap out a
working choice without a decision", not as "never introduce anything new".

## Why

This is a meta-ruling that corrects a *reading* rather than a decision. It came while a bundler was being approved
for the CLI artifact, and an agent had read a do-not-reintroduce line as a blanket prohibition on new
dependencies. The line's real purpose was narrower: keeping the web package on the framework its vendored packages
require.

The steering document was amended in the same change, so a rule contradicting an approved decision was not left
standing. That is the pattern the project follows generally.

## What this constrains

- Read a do-not-reintroduce line narrowly, as protection for a specific working choice, not as a ban on additions.
- Any tool or dependency addition still gets a decision entry plus the steering update in one change.
- Licence compatibility remains a hard rule. This ruling explicitly does not relax it.

## Provenance

Archive: `DECISIONS.md` L279-L297, `BRAIN.md` L1331-L1369 (RepoHIVE-Archive, frozen)
