#!/usr/bin/env bash
# Wave 4 gate: scan staged knowledge files for coursework/academic leakage.
#
# Usage:  bash gate.sh <dir> [<dir>...]
#
# Exit 0 = clean, exit 1 = hits requiring adjudication.
#
# Why this is not the replay's pattern verbatim:
#   The public-repo replay stripped .kiro/ and docs/ BY PATH and only ever
#   content-grepped source files, so its pattern never met this vocabulary.
#   Run unanchored against these documents and it produces false positives:
#     - "thesis" matches inside "hypothesis" (16 occurrences in the registers)
#     - "review" matches inside "preview" (the replay's one known carve-out)
#   Word boundaries fix both. "\bthesis\b" does not match "hypothesis"
#   because 'o' and 't' are both word characters, so no boundary exists there.
#
# Known benign phrase that WILL still be reported, by design:
#   "now academic" means "moot", not coursework. Adjudicate, do not auto-strip:
#   suppressing it would blind the gate to real uses of "academic".

set -uo pipefail

# Prefix terms: no trailing boundary, they inflect (university/universities).
PREFIX='universit|plagiaris'

# Whole-word terms.
WORDS='review|reviews|reviewer|reviewers|semester|semesters|academic|academics|academically|college|examiner|examiners|viva|rubric|rubrics|coursework|deadline|deadlines|submission|submissions|thesis|theses'

# Literal terms.
LITERAL='23CS701|Project-I|final-year'

hits=0
files=0

for target in "$@"; do
  if [ ! -e "$target" ]; then
    printf 'gate: no such path: %s\n' "$target" >&2
    exit 2
  fi

  while IFS= read -r f; do
    files=$((files + 1))

    # -o prints only matches so the count is per-occurrence, not per-line.
    n=$(grep -oiE "\\b(${WORDS})\\b|\\b(${PREFIX})|(${LITERAL})" "$f" 2>/dev/null | wc -l)
    n=$(printf '%s' "$n" | tr -d '[:space:]')

    if [ "${n:-0}" -gt 0 ]; then
      printf '\n=== %s: %s hit(s)\n' "$f" "$n"
      grep -inE "\\b(${WORDS})\\b|\\b(${PREFIX})|(${LITERAL})" "$f" 2>/dev/null \
        | cut -c1-160
      hits=$((hits + n))
    fi

    # High-confidence milestone-label signal, reported separately: a numbered
    # "Review N" is never engineering vocabulary.
    m=$(grep -oiE '\bReview[- ][0-9]' "$f" 2>/dev/null | wc -l)
    m=$(printf '%s' "$m" | tr -d '[:space:]')
    if [ "${m:-0}" -gt 0 ]; then
      printf '  !! %s numbered milestone label(s) - always a real hit\n' "$m"
    fi
  done < <(find "$target" -type f \( -name '*.md' -o -name '*.json' -o -name '*.txt' \) 2>/dev/null)
done

printf '\n--- scanned %s file(s), %s hit(s)\n' "$files" "$hits"

if [ "$hits" -gt 0 ]; then
  printf -- '--- FAIL: adjudicate each hit above before landing.\n'
  exit 1
fi

printf -- '--- PASS\n'
exit 0
