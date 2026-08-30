---
date: 2026-08-22
slug: replay-classification-by-post-filter-paths
title: "Replay classification goes by post-filter paths, never by commit subject"
status: current
superseded_by: null
supersedes: null
summary: "A commit's replay disposition comes from which paths survive the filter, not from its subject wording."
corrected: false
---

## What was decided

A commit's replay disposition follows the paths it still touches *after* the path filter runs, never its
subject wording. Any commit assumed to self-empty must be confirmed empty in a dry run before that assumption
is acted on.

## Why

Classifying by subject produced three wrong calls, caught only because a script asserts an expected commit
total and the dry run disagreed with it.

One documentation-titled commit wrote a file at the repository root, outside the filtered directory, so 360
lines of internal brief survived the filter and would have been published. Another documentation-titled commit
was not purely documentation: real changes remained once the filter ran, so it was kept with a rewritten
subject rather than dropped.

The sharpest case is the detection gap itself. A commit whose subject literally named one of the internal terms
being removed passed both acceptance checks, because that term was missing from the acceptance pattern for
commit messages, and the commit edited the archive's own `README.md` rather than anything published. A subject
is not evidence about content in either direction.

## What this constrains

- Root-level internal files must be named individually in the path filter. A directory filter does not reach
  them.
- Archive `README.md` commits never replay.
- A commit whose subject must be scrubbed but whose surviving content is real gets retitled, not dropped.
- Scrub patterns are deliberately phrases, not bare words. The vendored UI calls one of its surfaces a "paper
  wash", so a bare word-boundary match on `paper` would fail the build on legitimate code.
- Recorded commit totals in this area are volatile and have been restated more than once. Recount rather than
  trusting a recorded number, and do not apply on an unexpected count.

## Provenance

Archive: `DECISIONS.md` L612-L646, `BRAIN.md` L844-L876 (RepoHIVE-Archive, frozen)

Wording note: the archive entry quotes the internal term at issue verbatim, including inside a commit subject.
The term is one this project is removing from its records, so it is described here by its role rather than
reproduced. The mechanism, that the acceptance pattern did not contain the word it was meant to catch, is the
part that matters and is preserved intact.
