# context

Project state and decision history for RepoHIVE. This is a **separate private repository** cloned into the
public checkout at `context/`, which the public repository git-ignores.

It is local tooling. Nothing here is required to build, test, or run the project.

## What is here

| Path | Mode | Holds |
|------|------|-------|
| `STATE.md` | rewritten in place | Where the project is right now. Read first, every session |
| `decisions/` | one file per decision, never edited | Why things are the way they are |
| `decisions/README.md` | **generated** | Index of every decision, one line each |
| `registers/` | appended as work proceeds | Large working documents. Never bulk context |
| `gen-index.py` | run after any decision change | Generates `decisions/README.md`, and validates while it does |
| `gate.sh` | run before committing new prose | Scans for vocabulary that must not travel |

Durable engineering rules are **not** here. They are tracked publicly in `docs/engineering/`.

## This directory is invisible to search

The mount is git-ignored, so ripgrep-backed search tools skip it silently. Grep for a string in one of
these files and you get no result and no warning. **Open these files by explicit path.**

That is also why the read order lives in the public `AGENTS.md`: a tracked front door can be found, and it
names these paths literally so nothing depends on discovery.

## Memory protocol

Three roles, three write modes. Keeping them distinct is what stops the record from rotting.

**`STATE.md` answers "what is true now."** A snapshot, not a log. When something finishes, its in-progress
entry is *replaced*. When a plan is superseded, the old text is *deleted*, not struck through. Hold it under
**150 lines** so it can be read every session without crowding out the task. It is the one file here loaded
unconditionally, so its length is a running cost.

**`decisions/` answers "why is it like this."** One file per decision, named `YYYY-MM-DD-<slug>.md`, with
frontmatter carrying `date`, `slug`, `title`, `status`, `superseded_by`, `supersedes`, `summary`, and
`corrected`.

Never edit a decision file's substance and never delete one. A reversal is a **new file** that names the
slug it supersedes, plus a `superseded_by` pointer added to the old one. Because each decision is its own
file, git history proves this rather than merely asking for it.

**Partial supersession is the norm.** Usually a later decision retracts one named constraint while the rest
stands. Record that in the earlier file's `Corrections since` section and set `corrected: true`. Reserve
`status: superseded` for whole-entry replacement. A reader of one file alone must never act on a retracted
constraint.

**`registers/` answers "what was found."** Long-lived working documents, opened only for the item they
describe.

There is no session narrative log. Git history records what happened and when; decisions record what binds
future work. A running log was tried and dropped as low value per byte.

## Adding a decision

1. Get the real date and time: `Get-Date -Format 'yyyy-MM-dd HH:mm'`. Never reuse a conversation's start
   date; sessions span days.
2. Write `decisions/YYYY-MM-DD-<slug>.md` with full frontmatter. Slugs are permanent: the index, the
   filename, and every cross-reference join on them.
3. If it reverses or narrows an earlier decision, update that file (`superseded_by`, or a
   `Corrections since` entry plus `corrected: true`) **in the same change**.
4. Regenerate the index: `python gen-index.py decisions`. It validates as it goes, failing on a missing
   field, a dangling `superseded_by`, or a filename that disagrees with its frontmatter.
5. **Never hand-edit `decisions/README.md`.** It is generated. A hand-maintained index is a second home for
   the same fact, and the two drift.

## When to update

After **meaningful work**: files created, edited, or deleted; a decision made; a verification result
obtained; scope changed.

**Not** after answering a question, reading code, or diagnosing without changing anything. If nothing
meaningful happened, write nothing and say so in one line. An empty update is correct.

## Honesty rules

- Record only what happened. Never fabricate progress, dates, results, or test counts.
- Numbers must come from a run performed in this session or cited from a recorded measurement. Label
  estimates as estimates.
- **Label every timing cold or warm.** They differ by roughly eight times here, and unlabelled figures have
  caused wrong conclusions twice.
- If a gate could not be run, name it and say why. Never imply it passed.
- If a determinism digest moves, do not recapture it silently: identify which field changed and why, record
  a decision, and update the digest table in the same change.

## Before committing new prose

`bash gate.sh .` scans this repository for vocabulary that must not travel. It exits non-zero on a hit and
prints every match with its line, for a human to adjudicate one at a time.

It is deliberately not a silent auto-fix. Two known benign matches recur and must never be "corrected":
**`hypothesis` contains `thesis`**, and the phrase **"now academic" means moot**. Suppressing either would
blind the gate to a real use of the same word, so word boundaries are used instead of a blanket filter.

A numbered milestone label is always a real hit; the gate reports those separately.

**Expected baseline: 3 hits, in 2 known places.** Two are in the paragraph above, which has to name the
benign words in order to explain them. One is in
`decisions/2026-08-22-skills-hold-procedure-hooks-only-trigger.md` at line 25, where the flagged word is
ordinary English about a file going unread.

**Anything outside those two locations is new and unadjudicated.** Compare against this baseline rather than
expecting a clean run: a gate that always fails is a gate nobody reads, and a real leak would hide in the
noise. If you edit this section, re-run the gate and correct the count in the same change.

## Commit before you stop

**Knowledge is never merely saved to disk. It is always at least committed.**

This is not precaution. Decisions written here have been lost twice, both times because they were
uncommitted when a branch operation ran. Two repositories makes that easier, not harder: the public one
will feel finished while this one sits dirty.

Commit locally as part of the work, using `decision:`, `state:`, or `register:`. **Pushing stays
owner-driven** and must not run unprompted.
