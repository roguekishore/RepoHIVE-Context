---
date: 2026-08-22
slug: skills-hold-procedure-hooks-only-trigger
title: "Skills hold procedure; hooks only trigger, and one hook survives"
status: current
superseded_by: null
supersedes: null
summary: "Anything an agent can be asked to do is a skill; a hook exists only for what must fire unasked."
corrected: false
---

## What was decided

A dividing line was set between skills and hooks. Anything an agent can be *asked* to do is a skill. A hook
exists only for what must fire without being asked.

One stop hook survives. Four others were deleted as redundant, broken, or verbatim duplicates of a skill. A
hook may no longer contain a procedure: it judges whether to act and then delegates to the protocol held in
steering. That took the surviving hook from roughly four kilobytes to under one.

## Why

The reasoning is about duplication, not tidiness. The surviving hook had carried a large prompt restating rules
that already lived in always-on steering. Duplicated instructions drift, and the copy buried in configuration
is the one nobody reviews while still being the one that actually executes. So it drifts unseen and keeps
running.

## What this constrains

- New agent capability goes in a skill, not a hook.
- A new hook needs a reason it cannot simply be invoked. Convenience is not that reason.
- Hook prompts stay thin and point at steering. Procedure never gets copied into a hook.

This creates a real coupling to preserve: the surviving hook's correctness now depends on the steering protocol
staying complete, because the hook no longer carries the procedure itself.

## Provenance

Archive: `DECISIONS.md` L647-L677, `BRAIN.md` L719-L758 (RepoHIVE-Archive, frozen)
