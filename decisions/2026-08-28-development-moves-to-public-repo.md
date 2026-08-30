---
date: 2026-08-28
slug: development-moves-to-public-repo
title: Development moves to the public repo; this repo is frozen as the archive
status: current
superseded_by: null
supersedes: null
summary: All further coding happens in the public repo; the archive keeps full history and stops receiving work.
corrected: false
---

## What was decided

All further coding moves to the public repository. This repository is frozen as the archive: it keeps the full
working history and all private material, and receives no new work. The tooling moves to a different agent
environment.

Knowledge must be loaded deterministically, through imports declared in a tracked root configuration file, never
by discovery.

## Why

Freezing the archive creates one problem that needed solving: the public repo ignores the knowledge directory, so
a fresh clone on another machine arrives with no memory, no conventions and no decision history. The owner already
works from a second machine, which makes that a real blocker rather than a hypothetical one.

**The load-bearing finding is a silent-failure mode.** The file-read tool takes an explicit path and ignores
gitignore, but search and glob are ripgrep-backed and honour it. So an ignored knowledge directory can be read if
you already know the path, but cannot be *discovered*, and that failure is indistinguishable from an agent simply
choosing not to look. Nothing reports an error. Any design that assumes an agent will find the knowledge is
therefore wrong, which is why loading has to be deterministic and declared.

## What this constrains

- Knowledge is loaded through imports in a tracked root config file. Never rely on discovery.
- The per-session import budget is now a real cost, not a free convenience, since everything needed must be
  imported explicitly rather than found on demand.
- The archive receives no new work.

## Not ratified, and not to be treated as settled

A delivery mechanism was drafted and deliberately left unratified: **mounting a separate private repository at the
knowledge path**, together with the stated rejection of a submodule for that purpose. Owner approval is required
before implementing it, and separately before any steering content is made public. Do not build on either as
though it were decided.

## Relationship to the earlier repo posture

This decision freezes the repository entirely, which makes the 2026-08-23 `repo-posture-fable-work-default`
default-branch posture moot in practice. This entry does not name that one and does not claim to supersede it, so
**no supersession link is asserted**, and the question of whether it should be upgraded to a formal supersession
needs owner confirmation. Do not resolve it unilaterally.

Note also that the viewer handoff brief was subsequently written into this frozen repository and is untracked
there, which `viewer-handed-to-fable-workstreams-held` records as an unresolved placement problem.

## Provenance

Archive: `DECISIONS.md` L88-L122, `BRAIN.md` L1601-L1639 (RepoHIVE-Archive, frozen)
