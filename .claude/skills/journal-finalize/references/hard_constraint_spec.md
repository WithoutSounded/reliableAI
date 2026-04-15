# Hard Constraint Spec — Journal Finalize

Exact definitions, thresholds, and edge cases for the six Phase 6a checks and the Phase 6b drift heuristics. Consult this when a flag's severity or semantics is unclear.

## Severity ladder

- **`critical`** — blocks submission. Hard checks whose failure means the paper is internally inconsistent (phantom citation, broken `\ref`, abstract number not in Results, word count off limit by >5%). Phase 6b considers fallback for any section that triggers a `critical` flag.
- **`major`** — should be fixed but the author may override with context (orphan figure, symbol not in glossary).
- **`minor`** — hygiene (orphan bib entry, unreferenced label, unreferenced equation). Reported but not gating.

## 6a.1 Number consistency

Two subset relations must hold:

1. **Abstract ⊆ Results** — every number in `00_abstract.tex` must appear as a token in `04_results.tex`. Flag `ABSTRACT_NUMBER_NOT_IN_RESULTS` (critical) per missing number.
2. **{Abstract, Results, Discussion} ⊆ Source** — every number in those three files must appear in `analysis_summary.md`, `figure_captions.md`, or `table_captions.md`. Flag `NUMBER_NOT_IN_SOURCE` (critical) per missing number.

**Digit-boundary matching.** `20` does not match inside `200` — the token must be delimited by non-digit/non-`.` characters on both sides. Decimals match as whole tokens (`0.87` is one token, not `0` + `87`).

**Filtered out:** single-digit integers (`1`–`9`) and other `<2`-digit numeric tokens. Short integers are usually paragraph counts, list indices, or references to Section N, not metrics. If the paper genuinely reports `N=5` and we want to catch that, the sample-size pattern `N\s*=\s*(\d)` upstream in Results already requires the digit to be in context, and its presence in `analysis_summary.md` also has an `N=5` pattern — both pass. Filtering short ints eliminates false positives from section numbers (`Section 3`) and paragraph labels.

**Skip:** Math-mode content. Numbers inside `$...$` or `\begin{equation}` are algebraic constants, not empirical results; they're replaced with placeholders before extraction.

**Known semantic gap the script can't catch:** If the abstract says "`3` sessions" and Results says "session `3`", both contain the token `3` — the check passes, but the meaning is different. The model always reads both before shipping.

## 6a.2 Citation consistency

Bidirectional:

- **`PHANTOM_CITATION` (critical)** — a `\cite{K}` appears in a `.tex` file but no `@...{K,` entry in the bib file.
- **`ORPHAN_BIB_ENTRY` (minor)** — a `@...{K,` entry in the bib is never `\cite`'d. Phase 6c.1 auto-prunes these, so they're hygiene-only in 6a — we still report them so the author knows what got dropped.

**Cite-command variants** accepted: `\cite{}`, `\citep{}`, `\citet{}`, `\cite*{}`, `\citep*{}`, `\citet*{}`. Comma-separated keys are split.

## 6a.3 Symbol consistency

Every named math symbol used in `$...$` or `\begin{equation}` should have a row in `notation_glossary.md`. Matched by exact symbol string, with a loose fallback: for `\hat{x}` we also accept `\hat` in the glossary.

- **`SYMBOL_NOT_IN_GLOSSARY` (major)** — symbol appears in math but isn't listed in glossary.

**Caveat.** The math-symbol extractor only catches named LaTeX macros (Greek letters, `\mathbf`, `\hat`, `\tilde`, etc.). Plain-letter variables like `x` or `y` are not extracted — the glossary convention in this pipeline is to list only named symbols, not every single variable letter.

## 6a.4 Cross-reference integrity

- **`BROKEN_REF` (critical)** — `\ref{X}`/`\autoref{X}`/`\eqref{X}` has no matching `\label{X}` anywhere in the seven section files.
- **`UNREFERENCED_LABEL` (minor)** — `\label{X}` exists but `X` is never `\ref`'d. Author may legitimately add a label for future use, but we report it.
- **`ORPHAN_FIGURE` (major)** — a figure ID listed in `figure_captions.md` is never `\ref{fig:<id>}`'d in text. Either add the reference or remove the figure from the catalog.

Figure IDs are recognised as numeric (`Fig 1`) or as label-style (`fig:architecture`) in `figure_captions.md`.

## 6a.5 Word count

Total word count across the seven polished files must fall within `[limit × (1-t), limit × (1+t)]` where:

- `limit` = `word_limit` from `step0_session_config.json`
- `t` = tolerance (default 0.05; session config can override with `word_limit_tolerance`)

**`WORD_COUNT_OUT_OF_RANGE` (critical)** if outside the band.

Word-counting strips comments, math environments, LaTeX commands, and braces, then splits on whitespace. Numbers in prose count as words (they appear in the rendered PDF).

**Journal-specific defaults** (see `journal_preambles.md` for authoritative sources, but this is the common range):

| Journal family | Word limit (main body) | Typical abstract limit |
|---|---|---|
| IEEE TNSRE / TBME | 7,000–8,000 | 200 |
| NeuroImage | ~7,000 | 250 |
| Nature Methods | 3,000–4,000 (full article) | 150 |
| Scientific Reports | no hard limit | 200 |
| Advanced Engineering Informatics | 7,000 | 250 |
| Frontiers | 12,000 (soft) | 350 |

The per-section budget from the blueprint is reported but not gated — only the total matters at submission time.

## 6a.6 Equation numbering

Equations are walked in reading order (01→06). For each numbered equation environment (`equation`, `align`, `gather` — unstarred), the `\label{eq:...}` is recorded in order of appearance.

- **`BROKEN_EQREF` (critical)** — an `\eqref{eq:X}` or `\ref{eq:X}` targets an equation label that was never defined.
- **`UNREFERENCED_EQUATION` (minor)** — an equation has a `\label{}` but is never `\eqref`'d. Exposition-only equations are legitimate; the flag just surfaces them for author confirmation.

The check doesn't verify the sequence numbers (LaTeX does that at compile time), but it does verify that the label set referenced and the label set defined are consistent.

## Phase 6b drift heuristics

Signals produced by `semantic_drift.py`, per section:

- **`number_delta`** — numbers present in polished XOR revised. Pure rewording shouldn't change number tokens; any change is drift-suspect. After filtering out single-digit integers.
- **`citation_delta`** — `\cite` key set symmetric difference. Polishing should never add or drop a citation; that's a Step 3/4 activity. Any non-empty delta here is drift.
- **`claim_delta`** — paragraph alignment via greedy best-match Jaccard on content words (stopwords removed, 3+ char tokens). Default threshold 0.35. Unmatched paragraphs are the signal:
  - Unmatched in polished = likely added content during polish (red flag).
  - Unmatched in revised = likely removed content during polish (red flag).
- **`hedge_delta`** — counts of boosting words vs hedge words:
  - **Boosting words**: `demonstrates`, `proves`, `significantly`, `strongly`, `markedly`, `clearly`, `definitely`, `establishes`, `robustly`, `conclusively`.
  - **Hedge words**: `may`, `might`, `could`, `suggests`, `indicates`, `appears`, `seem`, `possibly`, `potentially`, `likely`, `tends`, `one possible`.
  - Rule: boost-count growth ≥ 3 in a Discussion-style section is overclaim-suspect; hedge-count swing of ≥ 4 in any other section is tone-drift suspect. Discussion gaining hedges during polish is expected and not flagged.

The script produces per-section `drift: true/false` verdicts based on these rules. The model may override — e.g., if the abstract-only drift reason is "abstract doesn't exist in revised" that's not true drift. But the default is: trust the heuristic, fall back to `step4` text when drift is flagged.
