---
date: 2026-08-23
slug: everything-ships-from-public-repo
title: "Everything ships from the public repo; no private deployment"
status: current
superseded_by: null
supersedes: null
summary: "Engine, viewer and any hosted instance all ship from the public repo; no closed-source deployment exists."
corrected: false
---

## What was decided

The engine, the viewer and any hosted instance all ship from the public repo. There is no closed-source or
private deployment of any part of the project.

## Why

The immediate effect is to dissolve a blocker that both the project snapshot and the forward-path register had
been carrying. Because the web package imports the engine in several modules, serving the app would pull the
engine inside the AGPL network-use obligation. That had ruled out the option of open-sourcing the viewer while
keeping the engine closed.

That option is now explicitly not wanted. So the licence pressure stops being a design input, rather than
being worked around.

## What this constrains

- The AGPL network-use pressure is gone as a design constraint and must stop being cited.
- Do not architect a separate engine-only read service for licence reasons. Only performance or operational
  grounds justify one.
- Attribution obligations and the repo's licence are unchanged.

`adopt-repowise-ui-under-agpl` is **not** superseded by this entry, which says so in its own text. Its
reasoning and its knowingly accepted cost both stand. This entry only resolves the hosting choice that entry
left open. What is retired is a recorded *blocker*, not that decision.

## Provenance

Archive: `DECISIONS.md` L461-L481, `BRAIN.md` L1134-L1185 (RepoHIVE-Archive, frozen)
