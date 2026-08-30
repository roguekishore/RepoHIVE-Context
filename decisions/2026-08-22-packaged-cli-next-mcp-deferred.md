---
date: 2026-08-22
slug: packaged-cli-next-mcp-deferred
title: "The packaged CLI is the next workstream; MCP is deferred behind it"
status: current
superseded_by: null
supersedes: null
summary: "packages/cli is built next and the MCP server is deferred, as a sequencing choice not a reversal."
corrected: true
---

## What was decided

`packages/cli` is the next workstream and the MCP server is deferred behind it. Deferred, not dropped. The CLI
starts from a requirements spec rather than from code.

## Why

The choice was the owner's, and it was made against an analysis that had ranked MCP higher on strategic value.
No reason was given beyond "for now", so this is recorded as a sequencing choice and not as a reversal of that
analysis.

The analysis itself stands and should not be re-argued:

- The code-graph MCP space is crowded.
- MCP is distribution, not differentiation.
- MCP does not depend on the CLI, since an ecosystem package may import the engine directly.
- The CLI is largely already written, as an extraction of existing flag surfaces.

## What this constrains

- Do not re-propose MCP-first.
- Do not rest any project claim on having an MCP server. The differentiator is the recorded deterministic
  per-region decision.
- The CLI starts from a requirements spec, not from code.

## Corrections since

Constraint 5 of this entry is retracted. It had said that the unresolved public-repo replay conflict gates
where new work lands. `replay-does-not-gate-development` retires that: new work may be committed freely without
first draining the replay. Constraints 1 through 4 above are unaffected.

This entry is also no longer *exclusive*, though nothing in it was reversed.
`all-workstreams-run-in-parallel` put every workstream into its own worktree running concurrently, so
the CLI is still being built but is no longer the only thing being built.

Wording note: the archive entry's first constraint made re-proposing MCP-first conditional on the owner asking
or on an external milestone schedule changing. That schedule framing is being removed from the project's
engineering record, so the condition is stated here as the owner asking or delivery priorities changing. The
prohibition is unchanged.

## Provenance

Archive: `DECISIONS.md` L580-L609, `BRAIN.md` L972-L1008 (RepoHIVE-Archive, frozen)
