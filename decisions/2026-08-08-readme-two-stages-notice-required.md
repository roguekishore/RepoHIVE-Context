---
date: 2026-08-08
slug: readme-two-stages-notice-required
title: README ships in two stages, and NOTICE is required
status: current
superseded_by: null
supersedes: null
summary: A minimal MIT-era README lands first; the AGPL section and NOTICE land with the vendored packages.
corrected: false
---

## What was decided

The public README ships in two stages. A minimal README lands first under MIT, carrying only a general
description, with no commands and no metrics. The AGPL section plus NOTICE land later, with the vendored
packages.

## Why

Chronological honesty. The relicense and the vendoring both happened after the grouping algorithm, so a single
README carrying AGPL from day one would have contradicted the MIT licence file sitting beside it and would have
cited packages that did not yet exist. NOTICE became a licence obligation the moment the vendored AGPL packages
shipped publicly, not a courtesy.

## What this constrains

Injected public-repo content must be chronologically self-consistent: a document may not assert a licence or
cite packages that did not exist at the date it carries. NOTICE is a licence obligation.

The deliberate absence of commands and metrics from the minimal README is what keeps it from going stale, and it
meets a later rule from the 2026-08-24 cold-start work: no warm-only performance figure may appear in a README
or any user-facing claim unlabelled, because a user's first run is cold. Every timing must carry a cold or warm
label.

This was executed. The project history records that README, NOTICE and LICENSE were verified present on the
public default branch before their source templates were deleted.

## Provenance

Archive: `DECISIONS.md` L837-L845, `BRAIN.md` L429-L466 (RepoHIVE-Archive, frozen)
