---
date: 2026-08-23
slug: cli-distribution-output-and-packaging
title: CLI distribution, output directory and packaging shape locked
status: current
superseded_by: null
supersedes: null
summary: Output goes to a dot-prefixed project directory with an override flag; four packages publish, CLI depends.
corrected: true
---

## What was decided

The CLI's output directory is a dot-prefixed folder inside the project being indexed, with a flag to override
it. Discoverability comes from printing the absolute path on completion.

Packaging is four published packages: the three engine libraries plus the CLI, with the CLI depending on the
three rather than bundling them.

## Why

The dot-prefixed project directory matches existing tooling convention, stays out of the way, and is
gitignore-friendly.

The packaging shape survives independently of the CLI. The three engine packages have to publish as libraries in
any case, because the MCP server and the hosted service import the engine directly and must not shell out to a
command line. Bundling into a smaller install is explicitly a later optimization: it changes nothing a user
types.

## What this constrains

- The WASM grammar files can never be bundled into JavaScript. They must ship as real files, located via the
  existing override.
- The output directory, and everything in it, is a published contract from the first release onward.

## Corrections since

**Constraint 3 of this entry is spent and must not be read as live.** It listed four items as still open and
blocking the CLI requirements spec: the full command shape, the final command names, the version policy, and
the bundler. All four were closed the same evening by `cli-requirements-spec-unblocked`. Do not treat any of
them as an open blocker.

The output-directory choice and the packaging reasoning are uncorrected.

## Provenance

Archive: `DECISIONS.md` L347-L373, `BRAIN.md` L1265-L1314 (RepoHIVE-Archive, frozen)
