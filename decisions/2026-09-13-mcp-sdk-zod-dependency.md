---
date: 2026-09-13
slug: mcp-sdk-zod-dependency
title: Add the MCP SDK and zod to packages/mcp, pinned to one zod instance
status: current
superseded_by: null
supersedes: null
summary: exact-pinned MIT deps for the MCP server; zod pinned to the SDK's own resolution so the workspace holds a single instance
corrected: false
---

# Add the MCP SDK and zod to packages/mcp, pinned to one zod instance

Decided and implemented 2026-09-13 on `wip/mcp` (commits `53b5fe2`, `f5d37e0`).

## What was decided

Per the recorded ruling that the steering tool lists are extensible rather than boundaries,
`packages/mcp` adds two dependencies, both exact rather than ranged, matching how the engine packages
pin theirs:

| Package | Version | Licence | Role |
|---------|---------|---------|------|
| `@modelcontextprotocol/sdk` | 1.30.0 | MIT | MCP server framework and stdio transport |
| `zod` | 3.25.76 | MIT | tool input validation at the MCP boundary |

Both licences were verified against the registry and are compatible with AGPL-3.0-or-later.
`docs/engineering/stack.md` gained an MCP dependency subsection in the same change, as the extensible
tool lists ruling requires.

## Why zod is pinned to 3.25.76 rather than 4.x

zod 4.6.4 was tried first and rejected on evidence, not preference. The SDK carries its own zod 3.25.76,
and with a second zod 4 copy in the tree the schema types fail against the SDK's `zod-compat`
`AnySchema` across the two instances: five type errors under a probe compile. Pinning to the exact
version the SDK resolves dedupes the workspace to a single zod instance and restores full type
inference.

**Operational consequence:** when the SDK is bumped, re-check the zod version it resolves and move this
pin with it. A pin that silently drifts out of step with the SDK's own resolution reintroduces the
dual-instance failure.

## Lockfile side effect, intended

`@modelcontextprotocol/sdk` already existed in the lockfile as a transitive development dependency of
the root `shadcn` package at 1.29.0. Taking it as a direct dependency upgraded that shared entry
in-range to 1.30.0 and flipped it from development to production. The `dev: true` deletions visible in
the lockfile diff are that flip, not an unrelated change.
