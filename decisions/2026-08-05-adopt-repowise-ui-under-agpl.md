---
date: 2026-08-05
slug: adopt-repowise-ui-under-agpl
title: Adopt repowise's UI under AGPL instead of building a viewer
status: current
superseded_by: null
supersedes: null
summary: Four repowise packages vendored whole; repo relicensed MIT to AGPL-3.0-or-later as the accepted cost.
corrected: true
---

## What was decided

Four repowise packages were vendored in full rather than a viewer being built from scratch, and the repository
was relicensed from MIT to AGPL-3.0-or-later to permit it. The vendored packages were taken whole, with
visibility gated rather than pruned. A viewer surface goes live only once the project's own engine produces its
data.

## Why

The packages were verified before adoption as nearly standalone, computing layout client-side with no
dependency on their Python backend, and deterministic. The licence cost was accepted knowingly: AGPL
constrains how a closed hosted product could ever be built, so commercial licensing flexibility was given up
deliberately.

## What this constrains

`packages/web` stays on Next.js, because the vendored packages require it. Upstream attribution stays in
NOTICE. The repository stays AGPL-3.0-or-later.

## Corrections since

This entry is explicitly **not** superseded by the 2026-08-23 public-repo decision, which says so in its own
text: `everything-ships-from-public-repo` resolved only the hosting question this entry left open, and this
entry's reasoning and its accepted cost both stand. Two things did move.

- **The AGPL network-use pressure is retired as a design input.**
  `everything-ships-from-public-repo` records that no closed-source or private deployment of any part of the
  project exists. The blocker that serving the app would pull the engine inside the network-use obligation
  therefore stops shaping design and must stop being cited. Do not architect a separate engine-only read
  service for licence reasons; only performance or operational grounds justify one. Attribution obligations and
  the repository's licence are unchanged.
- **"Vendored packages stay whole" no longer binds as an aesthetic constraint.**
  `fable-has-total-design-authority` (2026-08-29) grants the design agent authority over everything visual,
  including rewriting the existing canvas from scratch, and
  `viewer-handed-to-fable-workstreams-held` clears the building of genuinely new components. New components go
  in a separate namespace, never inside vendored folders. The ledger records that this latitude does not
  disturb the licence or attribution obligations set here: attribution must stay accurate for whatever vendored
  code remains.

The Next.js constraint was clarified rather than changed. `steering-tool-lists-are-extensible` (2026-08-23)
records that a blanket "do not reintroduce" line in steering had the narrower real purpose of keeping the web
package on the framework its vendored packages require, not of forbidding new dependencies. Licence
compatibility remains a hard rule that ruling does not relax.

## Provenance

Archive: `DECISIONS.md` L885-L903, `BRAIN.md` L429-L466 (RepoHIVE-Archive, frozen)

Same indirect history provenance as the other 2026-08-05 entries: those decisions were written to the history
file twice and lost twice, then re-recorded on 2026-08-08.
