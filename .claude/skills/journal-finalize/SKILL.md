---
name: journal-finalize
description: "Finalize a polished journal manuscript into a submission-ready bundle — Step 6 (the last step) of the Journal Writing Agent pipeline. Make sure to use this skill whenever the user has finished polishing and wants the manuscript packaged, even if they don't say the word 'finalize' — phrases like 'I'm done polishing', 'what's next', 'ready to submit', or 'checkpoint 3 passed' are all valid triggers. The skill runs three passes back-to-back: (1) zero-tolerance hard-constraint checks — numbers in abstract/conclusion match the results tables, every \\cite{} has a bib entry, every \\ref{}/\\eqref{} resolves, math symbols appear in the notation glossary, word count stays within the journal limit, equations are numbered; (2) semantic drift detection comparing step5_polished/ against step4_draft_v{latest}/ — if polishing silently changed numbers, added claims, strengthened hedges, or introduced unsupported citations, the skill falls back to the step4 text for that section and annotates why; (3) dual output — a clean LaTeX package (main.tex + per-section .tex + pruned references.bib, using the journal's preamble like IEEEtran or elsarticle) ready for Overleaf, plus bilingual Markdown for Obsidian (EN / 繁中 parallel callouts with per-subsection Revision Zones). Writes step6_final/latex/, step6_final/bilingual/, hard_constraints.json, semantic_drift.json, and final_check_report.md with a READY / REVIEW NEEDED / BLOCKED verdict. Trigger on any of: '/journal finalize', 'finalize the manuscript', 'final check', 'generate the final output', 'produce the submission bundle', 'submission-ready', 'camera ready', 'ready to submit', 'export to Overleaf', 'build the LaTeX package', 'package for submission', 'generate bilingual markdown', 'done polishing', 'checkpoint 3 passed', '終稿', '生成投稿版', '輸出雙語版', '通過潤稿進入 finalize', '潤稿完成', '投稿準備', '打包投稿'. NOT for polishing prose (use journal-polish), NOT for generating review flags from referee comments (use journal-review), NOT for revising based on flags (use journal-revise)."
---

# Journal Finalize — Step 6 of Journal Writing Agent Pipeline

You are the last gate before the paper leaves the pipeline. The prose is already polished (Step 5) and the facts are already verified (Steps 3–4). Your job is to (a) prove, mechanically and conservatively, that nothing mechanical is broken, (b) guarantee that polishing didn't change the paper's meaning, and (c) package the result into two formats the author uses downstream — LaTeX for Overleaf and bilingual Markdown for Obsidian review.

Three principles govern everything in this step:

1. **Zero tolerance on hard constraints.** A manuscript with a broken `\ref{}`, a phantom `\cite{}`, or an abstract number that doesn't appear in Results is not "almost ready" — it's not ready. Hard checks are binary pass/fail. When a check fails, the correct action is to surface the exact failure with location info, not to paper over it.
2. **Polish is translation; translation has a direction.** Step 5 was supposed to improve English without changing meaning. If Step 5 silently dropped a claim, strengthened a hedged statement, or changed a number, the reviewer in the real journal will see it — so we see it first. When semantic drift is detected, fall back to the `step4_draft_v{latest}` text for the affected section, annotate the fallback in the final report, and let the human decide.
3. **The dual output is the contract.** The LaTeX package is what gets uploaded to Overleaf and then to the journal submission system — it has to compile cleanly and contain only what's needed. The bilingual Markdown is what the author reads in Obsidian to catch the last few things a machine can't — it has to show EN and 繁中 side-by-side with a Revision Zone per subsection. Both outputs must come from the same source of truth.

## Input

Read from the journal session folder (e.g., `Journal/{session_id}_{paper_slug}/`):

1. **`step5_polished/`** — all seven polished section files (`00_abstract.tex` through `06_conclusion.tex`) plus `golden_thread_report.md` and (optionally) `polish_notes.md`. This is the primary source of the final prose. If `step5_polished/` is missing or incomplete, the pipeline has not finished Step 5 — report which section files are missing and stop.
2. **`step4_draft_v{latest}/`** — the last revised draft (highest `v{N}`). Used as the **fallback** text when Phase 6b detects semantic drift, and as the **baseline** against which drift is measured. If no `step4_draft_*` exists, a direct drift comparison isn't possible — note the gap in the final check report and proceed without a fallback source (but treat this as a yellow flag for the human).
3. **`step2_global_config.json`** — glossary and per-section profiles. Used to confirm terminology after polish and to retrieve the tense/hedging contract the paper was written against.
4. **`step1_preprocess/`** — `figure_captions.md`, `table_captions.md`, `notation_glossary.md`, and `equation_plan.md`. Ground truth for number consistency, symbol consistency, and equation numbering checks.
5. **Upstream references pool** — the `.bib` file from the Research Agent (`Research/{session}/step4_references.bib`). The pipeline preserves all cited-adjacent entries here; Phase 6c prunes it down to only the entries actually `\cite`'d in the polished text. The exact path comes from `step0_session_config.json → artifacts.research_session → step4_references.bib`. If the bib file isn't at that path, scan `step0_session_config.json → artifacts` for a `references_bib` key; if still missing, ask the user before fabricating a path.
6. **`step0_session_config.json`** — `target_journal`, `word_limit`, `section_structure`. Used to pick the LaTeX preamble template and to set the word-count tolerance.
7. **Analysis summary** — `{algorithm_session}/step4_analysis_summary.md` (path from `step0_session_config.json`). Ground truth for numerical claims. If missing, number consistency falls back to figure/table captions only and the final report notes the reduced coverage.

If any of (1), (3), (4), (6) is missing, stop and report which file is absent — finalize cannot run meaningfully without the polished text, config, preprocess data, and session metadata.

## Procedure

Execute the phases **in order**. Phase 6.0 is a hard precondition gate — do not start Phase 6a until it passes. Do not generate outputs in 6c until 6a and 6b have both produced their reports — the Phase 6c file writer needs to know which sections fall back to the revised draft. Phase 6d runs the journal-specific format checker on the assembled LaTeX package.

### Phase 6.0 — Format-Checker Precondition Gate

Before any other work, confirm that the journal's designated format-checker skill exists on disk. Without it there is no way to verify submission-guideline compliance, and a paper that desk-rejects on a trivially detectable format issue (wrong documentclass, missing CRediT, citation in abstract, unabbreviated journal names) wastes weeks of turnaround — so we refuse to produce a "final" bundle in that state.

1. Read `format_checker_skill` and `format_checker_status` from `step0_session_config.json`. These were populated by `journal-init`.
2. **Re-probe the filesystem** — do not trust the cached status. The user may have created the checker since init ran, or deleted it. Use `Glob` to check:
   - `.claude/skills/{format_checker_skill}/SKILL.md`
   - `~/.claude/skills/{format_checker_skill}/SKILL.md`
3. Update `format_checker_status` in the config to reflect the current reality (`ready` or `missing`), and refresh `format_checker_checked_at`.

**If status is `missing`, BLOCK:** do not run Phase 6a. Do not write any files under `step6_final/`. Do not update `current_step`. Print this message and stop:

```
🛑 Cannot finalize — format checker missing.

The target journal '{target_journal}' requires the '{format_checker_skill}' skill
to verify submission-guideline compliance, but it does not exist on disk.

Probed:
  .claude/skills/{format_checker_skill}/SKILL.md   — not found
  ~/.claude/skills/{format_checker_skill}/SKILL.md — not found

Required action:
  Run /skill-creator and author a skill named '{format_checker_skill}'. Use
  .claude/skills/aei-checker/ as a reference implementation — it shows the
  expected shape (scripts/audit.py + SKILL.md report template).

Once the skill exists, re-run /journal-finalize. The pipeline will pick up
where it stopped. Nothing you've done so far (step5_polished/, step4_draft_v*/, etc.)
will be touched.
```

This is the only place in the pipeline that hard-blocks on a skill dependency. The rationale: format compliance is the one thing this skill *cannot* verify by itself — it's journal-specific and lives outside `journal-finalize`'s scope. If we silently skipped the check, the `final_check_report.md` verdict would be a lie.

**If status is `ready`:** log to the final report that the checker was resolved to `{format_checker_skill}` and proceed to Phase 6a.

### Phase 6a — Hard Constraint Check

Binary pass/fail. Zero tolerance. Run the hard-constraints script:

```bash
python <skill_path>/scripts/hard_constraints.py \
  --polished-dir <path_to_step5_polished> \
  --preprocess-dir <path_to_step1_preprocess> \
  --bib-file <path_to_references.bib> \
  --analysis-summary <path_to_analysis_summary.md> \
  --session-config <path_to_step0_session_config.json> \
  --output <path_to_step6_final/hard_constraints.json>
```

The script performs six deterministic checks; exact definitions and thresholds are in `references/hard_constraint_spec.md`:

1. **Number consistency** — every numeric claim in `00_abstract.tex` must appear as a token in `04_results.tex`; every numeric claim in Results/Discussion/Abstract must appear in `analysis_summary.md` or `figure_captions.md` or `table_captions.md`. The check is a digit-boundary presence check (`20` won't match inside `200`); it catches mechanical mismatch, not semantic mismatch. The abstract ⊆ results ⊆ source data subset relation is the invariant.
2. **Citation consistency** — every `\cite{Key}` in the polished `.tex` files has a matching `@...{Key,` entry in the bib file; every bib entry is `\cite`'d at least once (orphans are flagged as minor, phantoms as critical).
3. **Symbol consistency** — every math symbol appearing in `$...$` or display math must appear in `notation_glossary.md`. A symbol redefined with a conflicting meaning across sections (same symbol, different glossary entries — which shouldn't exist but we check) is a critical failure.
4. **Cross-reference integrity** — every `\ref{X}`/`\autoref{X}`/`\eqref{X}` has a matching `\label{X}` somewhere in the seven section files; every `\label{}` is `\ref`'d at least once (unreferenced label is a minor flag). Figures in `figure_captions.md` that are never `\ref`'d are flagged as `ORPHAN_FIGURE`.
5. **Word count** — total word count across the seven polished files must be within the `word_limit` from `step0_session_config.json` with a ±5% tolerance by default (tighter journals may set stricter tolerances — see the preamble templates for journal-specific limits). Per-section numbers are also reported against the blueprint budget, but the gate is the total.
6. **Equation numbering** — equations counted in order across the reading-order files must form a gap-free 1..N sequence; every `\eqref{eq:X}` has a `\label{eq:X}`; every labelled equation is referenced at least once (unreferenced equations are a minor flag, not a hard fail, because sometimes an equation is defined for exposition only — but they are reported so the author confirms).

Each failure becomes a flag in the JSON with `id`, `type`, `severity`, `location`, `quote`, `evidence_expected`, `instruction`, and `source_file` — same shape as `journal-review` output. The severity ladder matters because Phase 6b decides fallback on `critical` failures:

- **`critical`**: hard checks that must not fail for the paper to be submission-ready (phantom citation, broken `\ref`, abstract number not in results, word count off by >5% of the limit).
- **`major`**: checks that should not fail but the author may override (orphan figure, symbol missing from glossary).
- **`minor`**: hygiene (orphan bib entry, unreferenced label).

Read the JSON back after the script runs. If `critical` > 0, note the affected section files — Phase 6b will consider fallback for those.

### Phase 6b — Semantic Drift Check

Step 5 polish is a meaning-preserving translation: same claims, same evidence, same direction, better prose. This phase verifies that — and when it fails, it falls back to the `step4` revised text for the affected section.

Run the drift script:

```bash
python <skill_path>/scripts/semantic_drift.py \
  --polished-dir <path_to_step5_polished> \
  --revised-dir <path_to_step4_draft_v{latest}> \
  --output <path_to_step6_final/semantic_drift.json>
```

The script compares polished vs revised **per section**, producing per-section signals (full spec in `references/hard_constraint_spec.md`):

- **Number delta** — numbers present in one version but not the other, treated as tokens (ignores pure punctuation and formatting changes).
- **Citation delta** — `\cite` keys present in one version but not the other.
- **Claim delta** — paragraph-level sentence alignment: polished paragraphs that have no close analogue in the revised version (likely added content) or revised paragraphs that disappeared (likely removed content), detected via a simple word-overlap similarity on content words. Threshold configurable; default 0.35 Jaccard after stopword removal.
- **Hedge delta** — counts of boosting words (`demonstrates`, `significantly`, `strongly`, `markedly`, `clearly`) and hedge words (`may`, `suggests`, `indicates`, `one possible`, `could`); a swing from hedged-to-boosted (or vice-versa) in a section is a drift signal that correlates with overclaim/underclaim.

The script does not decide — it reports deltas with locations. You, the model, decide whether each signal is true drift or just rewording:

- **No drift**: section numbers are equal, citation set is equal, hedge counts changed by ≤ 2 or in a justified direction (Discussion section adding hedges during polish is expected), claim-delta paragraphs are short reorderings.
- **Drift — fall back**: any number changed, any citation added or removed, a claim paragraph appeared or disappeared in full, or a boosting-word count increased by ≥ 3 in a Discussion-style section.

For each section that drifts, mark it for fallback in Phase 6c: the output `.tex` for that section will be the `step4_draft_v{latest}` content, not the `step5_polished` content, and the final report will record `FALLBACK: section_name (reason)`. For all other sections, the polished text is used.

**Edge case:** the abstract only exists in `step5_polished/00_abstract.tex` (it is written for the first time during polish). Skip the drift check for `00_abstract` — there is no revised baseline.

Write the per-section decisions to `step6_final/semantic_drift.json` alongside the script's raw output:

```json
{
  "section_decisions": {
    "01_introduction": {"drift": false, "use": "polished", "reason": "..."},
    "05_discussion":  {"drift": true,  "use": "revised",  "reason": "added 2 new hedge words; boosting-word count unchanged; numbers equal; 1 new paragraph in 5.2 — content addition, likely overreach"}
  }
}
```

### Phase 6c — Generate Dual Output

Only run this after 6a and 6b have reports. Three outputs, produced in this order so each subsequent step can verify the previous.

#### 6c.1 LaTeX Package

Run the package builder:

```bash
python <skill_path>/scripts/build_latex_package.py \
  --polished-dir <path_to_step5_polished> \
  --revised-dir <path_to_step4_draft_v{latest}> \
  --drift-decisions <path_to_step6_final/semantic_drift.json> \
  --bib-file <path_to_references.bib> \
  --target-journal "<target_journal>" \
  --output-dir <path_to_step6_final/latex>
```

The script:

1. Copies each section `.tex` into `step6_final/latex/` — from `step5_polished/` by default, or from `step4_draft_v{latest}/` for sections marked `use: revised` in the drift decisions. Adds a commented header line to any fallback section: `% [FINALIZE] This section uses step4 text — see final_check_report.md (semantic drift).`
2. Writes `main.tex` with the preamble template for `target_journal` from `references/journal_preambles.md` (IEEEtran for IEEE journals, elsarticle for Elsevier, sn-jnl for Springer Nature, standard article as fallback). The body consists solely of `\input{00_abstract}` through `\input{06_conclusion}` in reading order, followed by `\bibliographystyle` and `\bibliography{references}`.
3. Prunes the bib: parses all `\cite` keys from the final `.tex` set, reads the upstream bib, and writes `references.bib` containing only cited entries in the order they first appear in reading order. Emits a warning to stderr for any entry whose cite key is used but not found in the upstream bib (this will also have been flagged in Phase 6a as `PHANTOM_CITATION`; we don't fail here because Phase 6a already decided).
4. Runs a structural sanity pass on `main.tex`: brace balance, `\begin`/`\end` pair balance, no forbidden content inside section files (section files must not contain `\documentclass`, `\begin{document}`, `\end{document}`, or a full `\bibliography`), `\input{}` paths resolve to files on disk.

If the structural sanity pass fails, stop and print the failures — do not write partial output.

#### 6c.2 Bilingual Markdown

The bilingual output is what the author reads in Obsidian. One `.md` file per section, each file structured as a sequence of subsections, each subsection a pair of Obsidian callouts (`> [!quote] EN` and `> [!quote] 繁中`) followed by a `> [!edit] ✏️ Revision Zone`. Format spec and translation rules in `references/bilingual_format.md`.

First, run the scaffold script to materialize the EN side and the empty 繁中 / Revision Zone slots:

```bash
python <skill_path>/scripts/build_bilingual_scaffold.py \
  --latex-dir <path_to_step6_final/latex> \
  --output-dir <path_to_step6_final/bilingual>
```

The scaffold script:

1. Parses each `.tex` section into subsections using `\section`/`\subsection`/`\subsubsection` heading boundaries and paragraph-level text between them. It keeps math expressions (`$...$`, `\begin{equation}...\end{equation}`) verbatim — Markdown renders inline math with `$...$` by default in Obsidian with MathJax enabled.
2. Converts LaTeX-specific commands to readable Markdown equivalents for the EN callout body: `\cite{K}` → `[K]`, `\ref{fig:X}` → `Fig. X` (or whatever label convention the `\label` uses), `\textbf{...}` → `**...**`, `\emph{...}` → `*...*`. Keeps equation environments verbatim (Obsidian renders them).
3. Writes one `.md` per section with the EN callouts filled in and the 繁中 callouts and Revision Zones empty (placeholder comments inside them).

Then **you (the model) fill in the 繁中 translation** for each subsection. Do this section by section, not all at once — quality matters more than batch efficiency. The translation must:

- Be professional academic Traditional Chinese, not machine-translation-flavored (no "的 的" chains, no "被" overuse, no literal English word order).
- Preserve all mathematical notation verbatim inside `$...$`.
- Preserve citation brackets: `[Smith2024]` stays `[Smith2024]` in 繁中 too.
- Use the terminology conventions the user already set — check `step2_global_config.json → glossary` for preferred Chinese terms when they exist; otherwise use the standard academic translation (e.g., `attention weights` → `注意力權重`, `cross-validation` → `交叉驗證`). Flag any term you're unsure about in `final_check_report.md`.
- Match the EN sentence-by-sentence but not word-by-word; academic Chinese is naturally more compact than English, so a three-sentence English paragraph may become two Chinese sentences — that's fine as long as no claim is lost.

If you're unfamiliar with the preferred terminology for a specific domain term, invoke the `bilingual-translation` skill's conventions or ask the user before guessing.

Leave the `> [!edit] ✏️ Revision Zone` callouts with a placeholder comment `<!-- 修改意見或直接修改英文段落 -->` — these are for the human to fill at review time.

After you finish translating, verify the scaffold is still intact (same number of subsections, math and citations preserved) by re-running:

```bash
python <skill_path>/scripts/build_bilingual_scaffold.py \
  --verify \
  --latex-dir <path_to_step6_final/latex> \
  --bilingual-dir <path_to_step6_final/bilingual>
```

### Phase 6d — Journal-Specific Format Check

After 6c.1 has built `step6_final/latex/` and before 6c.3 writes the final report, run the journal's format-checker skill against the assembled package. This catches publisher-specific rules that the generic hard-constraint script in 6a cannot encode — highlight lengths, CRediT wording, LTWA-abbreviated journal names, documentclass, country on affiliations, etc.

1. Read `format_checker_skill` from `step0_session_config.json` (guaranteed `ready` by Phase 6.0).
2. **Invoke the skill** via the Skill tool (`skill: "{format_checker_skill}"`) with an instruction along the lines of:

   ```
   Run a compliance check on step6_final/latex/main.tex against the journal's
   submission guidelines. Include step6_final/latex/references.bib. Save the
   Markdown report to step6_final/format_check_report.md.
   ```

   If the Skill tool cannot invoke the skill, fall back to reading its `SKILL.md` from disk and executing its procedure inline — the path is the one that resolved in Phase 6.0.

3. **Capture the verdict.** Parse the resulting report (or its JSON sidecar, if the checker produces one — `aei-checker` emits `audit.py`'s JSON) to count:
   - `format_check_critical` — desk-reject-level issues (wrong documentclass, missing CRediT, citation in abstract, phantom citations, unreferenced figures)
   - `format_check_major` — issues the author may override but that a reviewer will see
   - `format_check_minor` — hygiene (orphan bib entries, unreferenced labels)

4. **Set the pipeline verdict:**
   - `critical == 0` → `READY`
   - `critical == 0 && major > 0` → `REVIEW NEEDED` — finalize completes, but the report flags items requiring human sign-off
   - `critical > 0` → `BLOCKED` — do not tell the user the package is submission-ready. The `.tex` and `.bib` files have already been written (useful for the user to inspect), but `final_check_report.md` must lead with the critical block and recommend the specific fixes. The user decides whether to fix in-place and re-run Phase 6d, or step back to Phase 6a/6b.

5. Store the checker's output path and the counts in memory for Phase 6c.3 to cite. Do not re-run the checker in 6c.3 — read the already-written `format_check_report.md`.

**Why this isn't in Phase 6a:** Phase 6a is a generic script over the section `.tex` files as they are in `step5_polished/`, before the main.tex preamble is assembled and before bib pruning. The format checker operates on the *assembled* LaTeX package (after 6c.1) because many of its checks (documentclass, preamble packages, pruned bib) only become meaningful once `main.tex` exists.

#### 6c.3 Final Check Report

Synthesize the four JSON/Markdown artifacts (hard constraints, drift decisions, bib prune log, format check report) plus your own qualitative notes into `step6_final/final_check_report.md` using `references/final_check_report_template.md`. The report includes:

- **Format check verdict** (Phase 6d) — lead with this: READY / REVIEW NEEDED / BLOCKED, checker skill name, counts of critical/major/minor findings, link to `format_check_report.md`. If BLOCKED, the body of the file must list every critical item with file:line evidence before any other section — this is the single most important thing the user needs to see.
- **Hard check results** — one line per check (pass/fail), with the flag count for each type; failures listed with file and line.
- **Semantic drift results** — per-section decision (polished vs fallback) and reason.
- **Warnings and fallbacks** — any section using `step4` text, any upstream file that was missing, any translation term you flagged as uncertain.
- **Word count breakdown** — per-section count and total vs journal limit, with percent of budget.
- **Citation statistics** — total unique keys, count of cited entries in the pruned bib, orphan bib entries removed.
- **Next step for the user** — depends on verdict:
  - `READY`: "Upload `step6_final/latex/` to Overleaf and read `step6_final/bilingual/` in Obsidian; fill Revision Zones for anything that needs a last-pass edit."
  - `REVIEW NEEDED`: list the major items and ask the user to confirm each before submission.
  - `BLOCKED`: list the critical items and explicit fixes; instruct the user to resolve and re-run `/journal finalize` (Phase 6.0 and 6d will re-run; 6a/6b/6c.1 outputs will be regenerated from the current `step5_polished/` + `step4_draft_v*/`).

Finally, update `step0_session_config.json`: set `current_step` to 6, add `artifacts.step6_final` pointing at the output directory.

## Output

Write to `step6_final/` in the session folder:

1. **`latex/`** — the LaTeX package ready for Overleaf:
   - `main.tex` — with target-journal preamble and `\input{}` chain
   - `00_abstract.tex` through `06_conclusion.tex` — section files (`\input{}`-ready; no `\documentclass`)
   - `references.bib` — pruned to only cited entries
2. **`bilingual/`** — Obsidian bilingual review bundle:
   - `00_abstract.md` through `06_conclusion.md` — per-section EN / 繁中 / Revision Zone callouts
3. **`final_check_report.md`** — comprehensive report (format check verdict, hard checks, drift decisions, warnings, word count, citation stats)
4. **`format_check_report.md`** — journal-specific compliance report produced by the format checker skill in Phase 6d
5. **`hard_constraints.json`**, **`semantic_drift.json`** — raw script output (kept for audit; not primary human-facing artifacts but referenced from the report)
6. **Update `step0_session_config.json`** — set `current_step` to 6; add `artifacts.step6_final`; refresh `format_checker_status` and `format_checker_checked_at`.

After writing outputs, present a short summary to the user:

- **Overall verdict**: READY / REVIEW NEEDED / BLOCKED (driven primarily by Phase 6d critical count, secondarily by Phase 6a)
- Format check: `{format_checker_skill}` — X critical, Y major, Z minor
- Hard check: passed / N critical failures
- Semantic drift: M sections polished, K sections fell back to revised text
- Total word count vs journal limit
- Next:
  - READY → upload `step6_final/latex/` to Overleaf; open `step6_final/bilingual/` in Obsidian to fill the Revision Zones for any last edits.
  - REVIEW NEEDED → review the major items in `format_check_report.md` and confirm each before uploading.
  - BLOCKED → see the critical items at the top of `final_check_report.md`; fix in `step5_polished/` (prose) or upstream (evidence/structure), then re-run `/journal finalize`.

## References

- `references/hard_constraint_spec.md` — exact definitions, thresholds, and subset relations for each of the six hard checks; drift-signal thresholds for Phase 6b
- `references/journal_preambles.md` — preamble templates for IEEE, Elsevier, Springer Nature, and generic `article`; per-journal word-limit conventions
- `references/bilingual_format.md` — Obsidian callout format spec, 繁中 academic translation rules and common-term glossary
- `references/final_check_report_template.md` — template for `final_check_report.md`
- `scripts/hard_constraints.py` — Phase 6a runner (six binary checks)
- `scripts/semantic_drift.py` — Phase 6b runner (polished vs revised deltas)
- `scripts/build_latex_package.py` — Phase 6c.1 (main.tex assembly, bib pruning, structural sanity)
- `scripts/build_bilingual_scaffold.py` — Phase 6c.2 (subsection parsing, EN callout fill, scaffold verification)
