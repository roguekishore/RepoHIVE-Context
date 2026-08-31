# Pipeline performance — history, root cause, options

Recorded 2026-08-29. Measurements are from this Windows dev machine, Node v20.19.0.
**Nothing here is implemented.** Full constraints live in `decisions/` (entries dated 2026-08-24 and
2026-08-27); this document is the narrative and the options in one place.

---

## 1. Current numbers

Broadleaf fixture: **2985 `.java` files, 13.4 MB, mean 4.6 KB per file.**

| Stage | Cold | Warm |
|-------|-----:|-----:|
| `parse` broadleaf | **~50 s** | **~6–8 s** |
| `group` broadleaf | — | ~6.5–9 s |
| **full pipeline** | **~57 s** | **~14 s** |
| `parse` vantage (158 files) | — | 1.2–3.5 s |

**Both numbers must always be quoted.** "Cold" means the first read of files that were just written to disk —
which is exactly what a user hits after cloning a repo and running `repohive index`. No warm figure belongs in
a README or a claim without being labelled warm.

Warm parse is **~85% CPU** (reads are 0.87 s of ~6.4 s; the rest is Tree-Sitter, symbol table, stitching,
serialization). **That is the optimization ceiling — ~6 s cannot be removed by touching I/O.**

---

## 2. What went wrong with the original measurement

**2026-08-22.** Wall-clock was measured for the first time and recorded as `parse` broadleaf **68.3 s**,
`group` **11.3 s**, `parse` vantage **4.7 s**. These were single runs. **No `BRAIN` entry recorded how they
were taken**, so the conditions were unrecoverable later.

Those figures then propagated into architectural conclusions: "full pipeline ≈ 80 s", "parse dominates group
6:1", the live-indexing decision's premise, and the argument for keeping `group` separately invokable.

**2026-08-24.** Re-measured, three runs each. Every figure was high — `parse` broadleaf by ~9x. Output was
byte-identical to the recorded values (29,190 nodes, 14,325 edges, 502 regions, preserve 38 / reconstruct
464), so this was a **measurement defect, not a code regression.** The owner's recollection that parse "ran
quick" was accurate; the written-down number was not.

The owner independently reproduced the split the same week: **>40 s cold, <7 s warm.**

### Six conclusions that had to be retracted

| Claim | Status |
|-------|--------|
| "Full pipeline ≈ 80 s" | **void** — ~14 s warm, ~57 s cold |
| "Parse dominates group 6:1" | **false** — roughly equal warm, parse marginally ahead |
| "Parse is where parallelism would pay" | **unsupported** |
| "~1.5 s of npm + WASM startup" | **overstated** — a warm vantage parse is 1.2 s *total* |
| Sweep saving from separate `parse`/`group` = ~21 min | **~2.4 min.** The stages are kept for spec Req 4.4 and debugging, not for speed |
| MCP must be read-only because indexing exceeds tool timeouts | **weakened** — 14 s is borderline, not disqualifying |

One conclusion was *strengthened*: the live-indexing decision's "a full run is watchable, so no queue or
worker fleet is needed" holds better at ~14 s than at ~80 s.

---

## 3. Root cause

**2026-08-27, established by experiment.** Copied the same 2985 files to a fresh path and parsed the copy
three times:

| Run on a fresh copy | Time |
|---------------------|-----:|
| 1st — files never accessed | **51.0 s** |
| 2nd | 6.6 s |
| 3rd | 6.2 s |

Identical output every run. This reproduces the 2026-08-22 anomaly on demand. The residual gap between 51 s
and 68.3 s is plausibly the heavy `git filter-repo` replay work running concurrently that evening.

**The mechanism.** Reading all 2985 files *warm* costs **0.33 s** — 4% of a parse. The extra 44.6 s on first
access is **14.9 ms per file.** An SSD page-cache miss on a 4.6 KB file is well under 1 ms, so cache-miss
alone cannot account for it. Windows Defender real-time **and** on-access protection are enabled here, and
on-access scanning of newly-created files at 10–30 ms each matches the magnitude; Defender caches its verdict
per file, which is why run 2 onward are fast.

**Attribution limit:** the penalty is proven and measured. Defender *specifically* is the leading explanation,
not a demonstrated one — isolating it needs an AV exclusion test, which requires admin rights and modifies a
security setting, so it was not done.

---

## 4. The lever

Probed with three fresh copies, walk timed separately from reads:

| Mode | Walk | Read | Per file |
|------|-----:|-----:|---------:|
| cold, sequential | 0.33 s | **59.06 s** | 19.79 ms |
| cold, concurrent ×16 | 0.32 s | **8.64 s** | 2.90 ms |
| cold, concurrent ×64 | 0.42 s | 8.95 s | 3.00 ms |
| warm, sequential | 0.46 s | 0.87 s | 0.29 ms |
| warm, concurrent ×16 | 0.36 s | 0.15 s | 0.05 ms |

1. **The directory walk is innocent** — 0.33 s cold, same as warm. `source-collector` needs no work.
2. **The whole penalty is per-file read latency**, serialized across 2985 synchronous reads.
3. **Concurrency ×16 gives 6.8x.** The cost is *waiting*, and waiting parallelizes.
4. **×64 saturates.** ~16 is the setting.

**The curve is flat past the knee, so overshooting is cheap and undershooting is not:** overshooting 4x cost
3.6%, undershooting cost 580%. Pick a value past the likely knee and stop tuning. The *penalty size* varies a
lot by machine (AV product and settings, OS, disk); the *benefit of concurrency* is what is consistent.

---

## 5. Options

### 1. Concurrent prefetch, then sequential extraction — the CLI lever

Projected cold `parse` **~51 s → ~15 s**; warm unchanged.

**Shape (this is the part that matters):** read concurrently into a `Map<absolutePath, string>`, then run the
**existing extraction loop unchanged**, pulling from the map. Only *when* bytes are fetched changes; the
processing order does not, so byte-identical output is structurally guaranteed rather than hoped for.
**Any design that lets read-completion order reach the graph is forbidden** — determinism is a hard constraint.

**Change surface is one file.** `createAstExtractor(deps: AstExtractorDeps = defaultDeps, grammar = {})`
already accepts injectable deps, so **`ast-extractor.ts` needs no changes at all**:

- `ParseOptions` gains `readConcurrency?: number` — optional, additive, beside `excludedSegments?`.
- `orchestrator.ts` gains a step after collect, before `deps.createExtractor()`, that fills the map.
- `ParseDeps.createExtractor` widens from `() => Promise<AstExtractor>` to
  `(deps?: AstExtractorDeps) => Promise<AstExtractor>`. **Backwards-compatible** — an existing zero-arg factory
  stays assignable. This is the only non-obvious part of the change.
- The `AstExtractor` interface, `extract()`, and the extraction loop are untouched.

**Keep it deliberately dumb.** A concurrent read into a map, no abstraction, no attempt to pre-guess the
future source-provider interface. A one-file change that the seam work later replaces is cheaper than
designing around a spec that does not exist.

**Settings:** concurrency ~16. Value belongs in `ParseOptions`, **not** a CLI flag initially — every published
flag is a permanent contract and this is a workaround for an environment quirk, not a domain choice.
**Do not derive the default from CPU count**; the bottleneck is I/O latency, so core count is the wrong
predictor. Bound the read-ahead for very large repos (13.4 MB at 2985 files; ~134 MB at 10x).

### 2. Parse from the archive stream without extracting — the cloud lever

**Eliminates** rather than mitigates: a hosted indexer that reads tar entries straight from memory writes no
new files, so there is no first-access cost, and one sequential read replaces 2985 opens.

This is a **live input to the source-provider seam design**, which must choose between extract-then-walk and
stream-from-archive. Caveat: tar entries arrive in archive order and need canonical sorting first.

### 3. Antivirus exclusion — maintainer's machine only

Works, needs admin, machine-specific. Fine for the maintainer's own `fixtures/` while benchmarking.

**Never user-facing guidance.** The CLI's purpose is indexing repositories a user just cloned from the
internet — the one directory that most warrants a scanner. It must not appear in the README.

### 4. Content-hash caching / snapshot ids — does not help

Already planned for the hosted path. Helps *re-indexing*; does nothing for the **first** index, which is the
cold case. Do not treat that work as covering this.

### 5. `worker_threads` for Tree-Sitter — different target

Attacks the ~6 s of real CPU work, not this penalty. Costs a WASM instance per worker. Parked as low priority.

### 6. Do nothing — defensible

On Linux the penalty is likely absent (no on-access scanner), which would make this a Windows-developer
annoyance rather than a product problem. **But that is unmeasured**, and a user's first run genuinely is cold.

**Suggested split: 2 for the cloud, 1 for the CLI, 3 privately, note 4 and 5.** Not decided.

---

## 6. Scope of the benefit — do not oversell

The prefetch fixes **cold local runs**. Since the leading cause is on-access AV scanning, a Linux host — so the
hosted path — probably sees little or none of the penalty. **That assumption is unmeasured and must be checked
on the target instance before any indexing duration is quoted.**

So this is real value for a user's first `repohive index` on Windows or macOS, not a universal 6.8x.

---

## 7. If it gets implemented

It is an engine change, so `docs/engineering/verification.md` applies in full:

- **Gate 1** build clean.
- **Gate 2** engine tests — core 153/153, parser 180/181 with only the known Windows failure.
- **Gate 3 determinism** — the digest must not move. The map-then-sequential-loop shape should guarantee this
  structurally, but it has to be confirmed, not assumed.
- **Gate 4 real-repo smoke** — it touches the parser, so re-run against broadleaf and compare node, edge and
  region counts against `STATE.md`.

Per the 2026-08-28 decision, engine code belongs in **the public repository**, not this archive repo.

---

## 8. Process rules this episode produced

Recorded as constraints in `decisions/`:

1. **Never record a first-ever run as a representative timing.** Measure three; report the range or median.
2. **Quote cold and warm as two labelled figures**, never one.
3. **A measurement with no recorded method is not a measurement.** Any figure reaching `STATE.md` or
   `decisions/` needs its method recorded in `registers/measurements.md`. The 2026-08-22 figures had none, which
   is why the conditions had to be reconstructed experimentally two days later.
4. **Recorded measurements deserve the same scepticism as recorded prose.** A number labelled "measured" was
   treated as authoritative over the owner's direct experience of the tool, twice. The owner was right both
   times.
