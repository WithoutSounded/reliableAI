---
name: aei-checker
description: Check a LaTeX manuscript for compliance with Advanced Engineering Informatics (Elsevier) submission guidelines. Use this skill whenever the user says "check AEI", "AEI compliance", "submission check", mentions Advanced Engineering Informatics, or asks to verify a paper is ready for AEI / Elsevier submission — even if they don't explicitly name this skill. Scans .tex and .bib files and produces an actionable compliance report with file:line evidence, covering structure, references, figures/tables, and formatting.
---

# AEI Compliance Checker

Verify a LaTeX manuscript against Advanced Engineering Informatics (Elsevier) author-guide requirements and produce an actionable compliance report.

Why it exists: AEI submissions get desk-rejected for avoidable reasons — wrong document class, missing CRediT, citation in abstract, unabbreviated journal names, figure defined-but-never-referenced. A one-shot scan catches these before submission.

## Workflow

1. **Locate the main `.tex` file.** Accept either an explicit path from the user, or scan the current directory for the file containing `\documentclass` and `\begin{document}`. If ambiguous, ask. Locate `.bib` files by looking at `\bibliography{}` or scanning sibling `*.bib` files.

2. **Run the audit script.** It does all mechanical parsing — word counts, highlight lengths, figure cross-references, bib entry validation, spelling consistency — and emits a JSON blob:

   ```bash
   python <skill-path>/scripts/audit.py <main.tex> --bib <refs1.bib> [<refs2.bib> ...]
   ```

   If no `--bib` flag is given, the script auto-discovers `*.bib` files in the manuscript's directory. The JSON schema is documented inline in `audit.py`; the fields relevant to each report section are described below.

3. **Narrate the JSON into a Markdown report** using the template below. Don't re-do the mechanical checks by hand — trust the script's numbers. Your job is interpretation and clear communication: grouping issues by severity, citing file:line evidence, and suggesting concrete fixes.

4. **Handle things the script can't verify** (require human judgment) as WARN with a clear note. These are called out in the checklist below.

## What the script checks (and how to narrate it)

### Structure

| Check | JSON field | How to narrate |
|---|---|---|
| Document class is `cas-dc` or `cas-sc` | `document_class` | If `status: fail`, this is a desk-reject-level issue. Lead with it; most downstream checks depend on the template. |
| Title page complete | `title_page` | Report per-field: `has_title`, `author_count`, `affiliation_count`, `affiliations_with_country`, `has_corresponding_author_mark`, `has_corresponding_author_email`. Any missing piece is a FAIL. |
| Abstract ≤250 words, no citations | `abstract.word_count`, `abstract.citation_keys` | `word_count > 250` → FAIL. Non-empty `citation_keys` → FAIL (AEI abstracts must be self-contained). |
| Keywords 1–7 | `keywords.count` | FAIL if 0 or >7. |
| Highlights: 3–5 items, each ≤85 chars | `highlights.count`, `highlights.items[].length` | Report the count, then any item with `over_limit: true` including its character length. |
| Acknowledgements, CRediT, Competing Interest, Data Availability, GenAI declarations | `declarations.*` | Each key is either an object (present) or `null` (missing). Missing CRediT / competing interest / data availability are FAILs. GenAI is WARN — add "required if AI tools were used" to the note. |

### References

| Check | JSON field | Narration |
|---|---|---|
| Numeric bracket citation style | `references.style` | If `status: fail` or `mismatch_numeric_natbib_with_name_bst: true`, explain clearly. The mismatch case (e.g., `natbib[numbers]` with `cas-model2-names`) is a real LaTeX compile-time issue worth flagging. |
| DOI on every entry | `references.bib.missing_doi` | List the keys. If all entries are missing DOI, say so compactly; don't enumerate 50 keys. |
| LTWA-abbreviated journals | `references.bib.journals_likely_need_abbreviation` | This is a heuristic — emit WARN, not FAIL. For each entry, give the current journal name and point the user to verify at the LTWA. |
| Citation ↔ reference mapping | `references.mapping.orphan_citations`, `references.mapping.unused_bib_entries` | Orphan citations (cited but no .bib entry) are FAIL — the document won't compile. Unused .bib entries are WARN. |

### Figures, Tables, Equations

| Check | JSON field | Narration |
|---|---|---|
| All figures/tables referenced | `figures_tables.figures.unreferenced`, `...tables.unreferenced` | FAIL per unreferenced label. |
| Captions present | `figures_tables.figures.missing_caption`, same for tables | FAIL per missing caption. |
| Tables editable (not images) | `figures_tables.tables.image_tables` | FAIL per entry. |
| Sequential numbering | `figures_tables.figures.out_of_order` | WARN if out of order. |
| Image-equations | `equations.likely_image_equations` | FAIL if any. |
| Inline `\frac` in running text | `equations.inline_frac_in_text_math` | WARN per occurrence — AEI prefers `a/b` in inline math. |

### Formatting

| Check | JSON field | Narration |
|---|---|---|
| Language consistency (US/UK) | `language.mixed`, `language.conflicting_pairs` | FAIL if both variants of the same root appear. List the conflicting pairs with counts. |

### Things the script cannot verify (handle as WARN)

- **Appendix equation/figure/table numbering** (A.1 form). If the document uses `\appendix`, note this needs manual verification — look for `\renewcommand{\thefigure}{A.\arabic{figure}}` etc. Emit WARN if `\appendix` is present without those renewcommands.
- **Variables should be italic / in math mode.** The heuristic for this is noisy, so skip automated flagging and instead add one line at the end of the report: "Manually verify that all variable names in running text appear inside math mode (`$x$`, not `x`)."
- **Whether the user used AI tools.** If `declarations.genai` is `null`, emit WARN asking the user to confirm. If they used any, the declaration is mandatory.

## Report format

Produce Markdown in this structure so it scans fast:

```
# AEI Compliance Report — <main .tex filename>

## Summary
- ✅ Passed: X
- ❌ Failed: Y
- ⚠️  Warnings: Z

## 1. Structure
- ✅ / ❌ / ⚠️  <check name>: <one-line verdict>
  - Location: <file:line>
  - Fix: <concrete action>
...

## 2. References
...

## 3. Figures, Tables & Equations
...

## 4. Formatting
...

## Recommended fix order
1. <highest-impact item first>
2. ...
```

Lead the fix order with items that would cause a desk reject — wrong template, missing CRediT, citation in abstract, unabbreviated journals, orphan citations — then formatting items.

## Heuristics for good reporting

- **Group identical issues.** If 30 .bib entries are missing DOI, one line ("30 of 32 entries missing DOI: [list]") is better than 30 separate findings.
- **Don't over-report PASSes.** A short "PASS" line per category is enough; don't enumerate every passing sub-check unless the user asked for verbose output.
- **Use WARN when uncertain.** LTWA abbreviation matches, GenAI declaration (conditional on AI use), and variable-italicization are the three areas where the tool cannot be certain. Emit WARN and ask the user to verify.
- **If the document class is wrong** (e.g., `elsarticle`), skip CAS-specific missing-macro findings (`\affiliation`, `\ead`, `highlights` env) — they cascade from the template issue. Instead, add one line: "After switching to cas-dc/cas-sc, re-run this check to see which CAS-specific front matter still needs to be added."

## Example invocation

User: "check my paper for AEI compliance"

1. Ask for the `.tex` path if unclear, otherwise proceed.
2. Run `python <skill-path>/scripts/audit.py <main.tex>`.
3. Parse the JSON and emit the Markdown report following the template above.
4. Offer: "Want me to fix any of these automatically? I can handle the mechanical ones — adding missing declaration sections, swapping journal names to LTWA abbreviations, reconciling US/UK spelling."
