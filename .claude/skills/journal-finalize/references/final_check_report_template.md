# Final Check Report — Template

This is the template the `journal-finalize` skill uses to synthesize `step6_final/final_check_report.md`. Copy the structure verbatim and fill in the `<...>` placeholders from the three raw JSON artifacts (`hard_constraints.json`, `semantic_drift.json`, `latex/_build_log.json`). Remove bracketed commentary. Keep the headings and order so the human can scan quickly.

---

```markdown
# Final Check Report — <paper_slug>

**Session:** <session_id>
**Target journal:** <target_journal>
**Timestamp:** <ISO timestamp>
**Verdict:** <READY | REVIEW NEEDED | BLOCKED>

> **Verdict key**
> - **READY** — all hard checks passed, no critical drift, zero fallbacks. Safe to upload `latex/` to Overleaf.
> - **REVIEW NEEDED** — hard checks passed, but one or more sections fell back to step4 text (drift), or there are major/minor flags the author should confirm.
> - **BLOCKED** — at least one critical hard-check failure. Do not submit until addressed; the script has already written the package but it won't compile cleanly or the data is inconsistent.

## 1. Hard constraint checks (Phase 6a)

| # | Check | Passed | Flags |
|---|---|---|---|
| 1 | Number consistency (abstract ⊆ results ⊆ source) | <✓/✗> | <N critical / M major / K minor> |
| 2 | Citation consistency (\\cite ↔ .bib) | <✓/✗> | <counts> |
| 3 | Symbol consistency (notation glossary) | <✓/✗> | <counts> |
| 4 | Cross-reference integrity (\\ref ↔ \\label) | <✓/✗> | <counts> |
| 5 | Word count (total vs limit ±<tolerance>%) | <✓/✗> | <counts> |
| 6 | Equation numbering | <✓/✗> | <counts> |

**Critical failures** (if any — otherwise write "None"):

- `<flag.id>` — `<type>` in `<file:line>`: <quote>
  - Fix: <instruction>

**Major / minor flags** (grouped; show only if > 0 per severity):

[List by type, e.g.:]
- ORPHAN_BIB_ENTRY ×3: `Smith2020`, `Jones2018`, `Lee2022` (auto-pruned from `references.bib` in Phase 6c.1)
- SYMBOL_NOT_IN_GLOSSARY ×1: `\kappa` in `04_results.tex:27` — add to `notation_glossary.md`

## 2. Semantic drift check (Phase 6b)

| Section | Decision | Reason |
|---|---|---|
| 00_abstract | polished | abstract written in Phase 5c — no revised baseline |
| 01_introduction | <polished/FALLBACK> | <reason> |
| 02_related_work | <polished/FALLBACK> | <reason> |
| 03_methods | <polished/FALLBACK> | <reason> |
| 04_results | <polished/FALLBACK> | <reason> |
| 05_discussion | <polished/FALLBACK> | <reason> |
| 06_conclusion | <polished/FALLBACK> | <reason> |

**Fallbacks applied:** <N>. Each fallback uses the `step4_draft_v{latest}` text for that section in `step6_final/latex/<nn>_<name>.tex`, with a header comment pointing back to this report.

## 3. Word count

| Section | Words | Blueprint budget | % of budget |
|---|---|---|---|
| 00_abstract | <W> | <B> | <P>% |
| 01_introduction | <W> | <B> | <P>% |
| ... | | | |
| **Total** | **<T>** | **<journal limit>** | **<P>%** |

Within tolerance band `[<lower>, <upper>]`: <✓/✗>.

## 4. Citation statistics

- Unique cite keys in manuscript: <N>
- Entries in pruned `references.bib`: <M>
- Orphan bib entries removed: <K>
- Missing cite keys (referenced but not in upstream bib): <list, or "None">

## 5. LaTeX package

- Preamble: <preamble_note>
- Bibstyle: <bibstyle>
- Structural sanity: <passed / FAILED>
  - [If failed, list errors from `latex/_build_log.json → structural_errors`]

## 6. Bilingual Markdown

- Section files written: <N of 7>
- Subsections total: <M>
- Scaffold verification: <passed / FAILED>
- Translation terminology flags (terms the translator was unsure about): <list, or "None">

## 7. Warnings and notes

[Anything not covered above — e.g. missing upstream files, translation exceptions the LLM called out, symbols that appeared exactly once and couldn't be disambiguated.]

## 8. Next steps for the author

1. Upload `step6_final/latex/` to Overleaf. The package is `\input{}`-wired; `main.tex` compiles against `references.bib`.
2. Open `step6_final/bilingual/` in Obsidian. Read each section's EN / 繁中 side-by-side. Fill any Revision Zones with edit instructions or direct English replacements.
3. [If verdict is REVIEW NEEDED] Address the fallback sections — either accept the step4 text or re-polish the specific paragraphs that drifted.
4. [If verdict is BLOCKED] Fix the critical failures listed in §1 before uploading.
```

---

## Notes on synthesizing this report

- **`<✓/✗>`** — use literal check/cross marks so the human can scan quickly.
- **Don't invent flags.** Only list what's in `hard_constraints.json → flags` and `semantic_drift.json → section_decisions`.
- **Verdict decision tree:**
  - Any `critical` flag remaining after pruning (orphan bib entries are auto-pruned in 6c.1 so they don't count) → BLOCKED
  - Any fallback section, or any major-severity flag → REVIEW NEEDED
  - Otherwise → READY
- **Word count table** comes from `hard_constraints.json → meta.word_count.per_section`; blueprint budgets may or may not be present in that artifact — when missing, just omit that column rather than fake numbers.
- **Missing cite keys** are the `missing_bib_keys` field in `latex/_build_log.json`. Even if Phase 6a's `PHANTOM_CITATION` flags caught them, re-listing here is useful because this is the section the author reads when deciding what bib entries to chase down.
- **Next steps** are almost always the same three items; add special instructions only when the verdict is BLOCKED (then #4 gets specific guidance).

## Length

Keep the report under 150 lines of Markdown including tables. It's a check report, not a narrative — the human scans it for 30 seconds and moves on unless something is wrong.
