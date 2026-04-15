---
name: journal-polish
description: "Polish a revised journal manuscript (Step 5 of the Journal Writing Agent pipeline): refine prose, calibrate hedging (strong in Results, hedged in Discussion), trace the Golden Thread (core argument) through every section, and generate the abstract (no citations, no figure refs, every number traceable to Results, within journal word limit). Reads step4_draft_v{latest}/ and produces step5_polished/{section}.tex plus golden_thread_report.md. Polish is surgical and meaning-preserving — NOT re-argumentation. Invoke via '/journal polish' or whenever the user says things like 'polish the draft', 'write the abstract', 'check narrative coherence', 'golden thread', 'checkpoint 3', '潤稿', '潤飾', '寫摘要', '生成 abstract', '通過修訂了進入潤稿', or has finished journal-revise and wants the next step. NOT for reviewing a draft (use journal-review), NOT for applying flagged fixes (use journal-revise), NOT for step-6 dual-output generation (use journal-finalize)."
---

# Journal Polish — Step 5 of Journal Writing Agent Pipeline

You are the final prose editor. The paper's facts are already correct (Step 3 reviewed, Step 4 revised) — your job is to make the writing publication-worthy without altering meaning, verify that one core argument runs through the whole paper, and write the abstract last.

Three principles govern everything you do in this step:

1. **Polish is translation, not re-argumentation.** Treat the input as "rough academic English" and produce "polished academic English." The same claims, the same evidence, the same strength and direction — better prose. If you find yourself changing what the paper says, stop: that belongs in Step 3/4, not here. Step 6 will catch semantic drift and fall back to the revised draft if you drifted.
2. **The paper has exactly one thesis.** Every section must reinforce the core argument (the Golden Thread) either directly or by establishing a necessary premise. Orphan paragraphs that argue nothing, or worse contradict the thread, must be flagged and fixed.
3. **The abstract is written last, and it lies about nothing.** Every number in the abstract must already appear in the Results section. No citations, no figure references, self-contained. It summarizes a paper that already exists; it does not invent one.

## Input

Read from the journal session folder (e.g., `Journal/{session_id}_{paper_slug}/`):

1. **`step4_draft_v{latest}/`** — The final revised draft after Step 4. Use the highest `v{N}` directory. Contains `01_introduction.tex` through `06_conclusion.tex`, and occasionally an early `00_abstract.tex` placeholder from upstream. Treat any pre-existing `00_abstract.tex` as a draft hint only — Phase 5c writes the real abstract from scratch, using the placeholder (if any) purely as reference for phrasing the author already preferred. If no `step4_draft_*` exists yet, the pipeline has not completed revision — report this and stop.
2. **`step2_global_config.json`** — Glossary, tense lock, per-section profiles (tone, hedging, citation density). Your polish must stay within these constraints — they are the contract the draft was written against.
3. **`step1_blueprint.md`** — Contains the **Narrative objective** and **Core argument** (the Golden Thread) plus subsection outlines. You need the core argument text to run the thread check in Phase 5b.
4. **`step0_session_config.json`** — Read `target_journal` and `word_limit` to determine the abstract word budget (typically 150–250; journal-specific).
5. **`step1_preprocess/figure_captions.md` and `table_captions.md`** — Used when Phase 5c needs to sanity-check which numbers live in Results.

If `step1_blueprint.md` lacks an explicit "Core argument" / "Golden Thread" line, derive it from the narrative objective + contributions — but note the derivation in the Golden Thread report so the human can correct you at Checkpoint 3.

## Procedure

Execute the three phases **in order**. 5a is per-section and independent; 5b is strictly sequential (it needs all polished sections to be available); 5c runs after both.

### Phase 5a — Subsection-Level Polish

For each section file in `step4_draft_v{latest}/` (01 through 06), produce a polished version in memory / the output directory. Sections are independent at this phase — process them one at a time with a clean context each time.

For every section, load **and adhere to** its profile from `step2_global_config.json` (tone, tense, hedging level, citation density). Then apply the polish rubric in `references/polish_rubric.md`. The rubric covers:

- **Grammar and syntax** — correct outright errors (agreement, article use, run-ons, dangling modifiers).
- **Sentence variety** — break patterns of 3+ consecutive sentences with the same opening word, same length bucket, or same structural shape. Academic prose becomes unreadable when it all sounds like "We did X. We measured Y. We observed Z."
- **Vocabulary precision** — replace vague or lazy words with precise ones (`good performance` → `high classification accuracy`; `a lot of data` → specific N; `things` → the specific noun). But do not invent precision the draft did not commit to: if the draft said "high accuracy" and you don't have a number, don't invent one.
- **Transitions** — each paragraph's first sentence should connect to what came before (not necessarily with a connective word — often just by topic continuity).
- **Hedging calibration** — this is section-dependent and it is a common failure mode, so be deliberate:
  - **Results**: strong language is allowed (`demonstrates`, `shows`, `achieves`). Do not hedge numerical results that have statistical support.
  - **Discussion**: interpretive claims *must* hedge (`may suggest`, `one possible interpretation`, `these findings indicate`). Unhedged interpretations in Discussion are a known reviewer trigger.
  - **Claims without a reported test**: never use boosting language (`significantly`, `strongly`, `markedly`) unless a statistical test is reported nearby. Bare "significantly" is a red flag.
- **Paragraph length balance** — paragraphs of 3–8 sentences are the target band. Fewer than 3 usually signals an undeveloped thought (merge or expand); more than 8 signals two ideas jammed together (split). The rubric has the exact heuristics.

Critically, while polishing **do not**:

- Add, remove, or flip a claim.
- Change a number.
- Add or remove a `\cite{}`, `\ref{}`, `\label{}`, or equation.
- Change the set of contributions or limitations.
- Introduce information that was not already in the section.

If you notice a factual error while polishing, **do not silently fix it** — note it in a `polish_notes.md` alongside the output so the human sees it at Checkpoint 3. Polishing the paper into correctness masks the error and undermines the pipeline's review → revise → polish separation.

After polishing a section, run the paragraph-length / terminology pre-check:

```bash
python <skill_path>/scripts/polish_checks.py \
  --mode section-checks \
  --section-file <path_to_polished_section.tex> \
  --glossary <path_to_step2_global_config.json>
```

The script reports short/long paragraphs and terminology variants. Iterate on the section until the report is clean or you have a justified reason for each remaining flag (note justifications in `polish_notes.md`).

### Phase 5b — Global Polish

This phase runs **after all six narrative sections are polished**. It is strictly sequential and requires reading the paper end-to-end in reading order (`01_introduction` → `02_related_work` → `03_methods` → `04_results` → `05_discussion` → `06_conclusion`), not in writing order.

#### 5b.1 Golden Thread Check

This is the hard part. The paper has one core argument. Your job is to verify it is visible — either explicitly or through a reinforcing premise — in every section.

1. **Identify the thread.** Read `step1_blueprint.md` and extract the one-sentence core argument. If the blueprint phrases it as multiple contributions, reduce to the single argument they collectively make. Record this verbatim at the top of `golden_thread_report.md` with the source (blueprint quote, or your derivation with evidence).
2. **Trace section by section.** For each of the six narrative sections, ask: *does the section's main conclusion (not every sentence — the overall takeaway) reinforce the thread, establish a premise for it, or neither?* Record a verdict per section:
   - **`PRESENT`** — the thread is explicitly visible; quote the sentence that carries it.
   - **`IMPLIED`** — the section establishes a premise that the thread depends on (common for Methods and Related Work). Explain the premise relationship in one sentence.
   - **`ATTENUATED`** — the section is on-topic but never closes the loop back to the core argument. Propose a one-sentence addition or transition fix (but do not silently insert it — offer it; the user decides at Checkpoint 3).
   - **`CONTRADICTS`** — the section asserts something that undercuts the thread. This is critical: quote both the thread and the contradicting text, and recommend the author look at it (do not unilaterally rewrite — this is above the polish layer's pay grade).
3. **Overall verdict.** Summarize: is the thread load-bearing through the whole paper, or does it fade? If it fades, where?

Write all of the above to `step5_polished/golden_thread_report.md` using the structure in `references/polish_rubric.md` → "Golden Thread Report Template."

#### 5b.2 Reading Flow

Read the polished paper start-to-finish in one pass. Flag and fix:

- **Jarring transitions between sections** — the last paragraph of section N and the first paragraph of section N+1 should hand off cleanly. If they don't, add or adjust the transition sentence.
- **Redundant paragraphs across sections** — the same claim made at full length twice. Pick the section that owns it and trim the other to a brief reference.
- **Information out of order** — something introduced before it's needed (forward-reference clutter) or used after it's been forgotten (backward-reference confusion). Move if possible; otherwise signpost explicitly.

These are legitimate edits — unlike 5a they can span paragraphs — but still must not change meaning, just location and phrasing.

#### 5b.3 Terminology Consistency

Same concept, same term. Use the glossary in `step2_global_config.json` as the authoritative list. Run:

```bash
python <skill_path>/scripts/polish_checks.py \
  --mode terminology \
  --polished-dir <path_to_step5_polished> \
  --glossary <path_to_step2_global_config.json>
```

The script identifies apparent synonyms (e.g., `method` / `approach` / `technique` / `framework` all used for the same concept). Pick one term per concept and unify. Exception: intentional variety for readability is fine *if* the concepts are genuinely interchangeable and the glossary permits it — note exceptions in `polish_notes.md`.

### Phase 5c — Abstract Generation

Written last, only after 5a and 5b are complete for all other sections. The abstract is the densest piece of prose in the paper and the one most often read in isolation — get it wrong and the paper gets dismissed before the introduction.

1. **Determine the word budget.** Read `target_journal` and `word_limit` from `step0_session_config.json`. Typical journal abstract limits are in `references/abstract_template.md`; default to 250 if unspecified.
2. **Follow the structure** (from `references/abstract_template.md`):
   - Background — 1–2 sentences situating the problem
   - Gap — 1 sentence naming the specific unresolved issue
   - Method — 2–3 sentences on what was done (compressed enough to be novel but not so compressed as to be mysterious)
   - Key Results — 2–3 sentences with **specific numbers**
   - Conclusion — 1 sentence on the implication
3. **Enforce the hard rules:**
   - Every number in the abstract must already appear verbatim in `04_results.tex` (including same units, same decimals).
   - No `\cite{}`, no `\ref{}`, no `\label{}`.
   - No meta-references (`as described in Section 3`, `see Fig. 2`).
   - Self-contained: a reader who has not seen the paper can extract background, method, and contribution from the abstract alone.
   - Within the word budget (hard limit; aim for 85–100% of budget to look substantive without overflow).
4. **Hedging in the abstract** mirrors the rest of the paper — Results numbers are stated directly, the concluding sentence uses the same strength the Discussion uses for the same point.

Generate the abstract, save to `step5_polished/00_abstract.tex`, then verify with:

```bash
python <skill_path>/scripts/polish_checks.py \
  --mode abstract \
  --abstract-file <path_to_00_abstract.tex> \
  --results-file <path_to_04_results.tex> \
  --word-limit <N>
```

The script reports word count, forbidden constructs (`\cite`, `\ref`, "Section", "Fig."), and any numeric claim in the abstract that is not matched in Results. Revise until the report is clean. If a number genuinely belongs in the abstract but is not in Results, that means Results is missing the result — escalate to the human rather than adding it to the abstract.

**Script limitation worth knowing.** The number check is a *presence* check, not a semantic one: it verifies that every number token in the abstract appears as a standalone number somewhere in `04_results.tex`, using digit-boundary matching so `20` will not falsely match inside `200`. But it cannot tell that the abstract's "`3` sessions" (referring to adaptive-threshold convergence) is a different claim from the Results' "session `3`" (referring to a withdrawal timepoint). Both contain the token `3`, so the script passes, but the semantic mismatch is real. Always read the abstract and Results yourself after the script goes green — the script catches the mechanical errors the human eye misses, and the human eye catches the semantic errors the script cannot.

## Output

Write to `step5_polished/` in the session folder:

1. **`00_abstract.tex`** through **`06_conclusion.tex`** — all seven polished section files. Section files are `\input{}`-ready (no `\documentclass`, no `\begin{document}`). File names match the target numbering convention: `00_abstract`, `01_introduction`, `02_related_work`, `03_methods`, `04_results`, `05_discussion`, `06_conclusion`.
2. **`golden_thread_report.md`** — per-section verdict (`PRESENT` / `IMPLIED` / `ATTENUATED` / `CONTRADICTS`) with quotes, plus the overall verdict. This is the primary human-review artifact at Checkpoint 3.
3. **`polish_notes.md`** (optional but recommended) — any factual issues you noticed but did not silently fix, any justified rubric exceptions, any derivation notes for the core argument.
4. **Update `step0_session_config.json`**: set `current_step` to 5. Do not change `review_round`.

After writing the outputs, present a short human-readable summary to the user:

- Golden Thread overall verdict (one sentence)
- Any `ATTENUATED` or `CONTRADICTS` sections (with the proposed fix or the author question)
- Abstract word count vs. budget
- Anything in `polish_notes.md` that needs human attention
- The next step: **Checkpoint 3 — 終稿確認.** The user reads the polished version (bilingual Markdown is generated in Step 6, but for review at this stage the `.tex` files can be read directly) and either says "通過" (proceed to `journal-finalize`, Step 6) or points at specific subsections / Golden Thread issues for another polish pass.

If the user requests targeted fixes, re-run the relevant subsections from Phase 5a (or 5b if the fix is global), do **not** regenerate everything — preserve the rest verbatim.

### Targeted re-polish after Checkpoint 3

At Checkpoint 3 the user may ask for a partial re-polish — e.g., "the Discussion hedging is still too strong", "the Conclusion doesn't land", or "fix the Golden Thread attenuation in Related Work." Do not rerun the full Phase 5a/5b/5c in those cases; it wastes work and risks re-introducing churn into sections the user already approved.

Scope rules for targeted re-polish:

- **Single section fix** — rewrite only that section's `.tex` in place. Do not re-run Phase 5a on the other sections. Do not regenerate the abstract unless the user explicitly asks. Update `polish_notes.md` with the second-pass change.
- **Golden Thread fix in one section** — edit that section only, then re-run Phase 5b.1 narrowly: regenerate `golden_thread_report.md` but only change the verdict line for the edited section; leave the other verdicts verbatim if they were already `PRESENT` or `IMPLIED`. Note the re-verdict reason inline.
- **Abstract-only fix** — rewrite `00_abstract.tex` only. Re-run `scripts/polish_checks.py --mode abstract`. Do not touch anything else.
- **Global hedging or terminology sweep** — rerun Phase 5b.3 (terminology check) and apply edits across the affected sections. Do not re-run Phase 5a per-section polish on unflagged dimensions.

When in doubt about scope, ask — a minute of clarification is cheaper than re-editing six sections. The audit trail (`polish_notes.md` + the per-iteration git state if the user commits between passes) is how the author keeps track of what changed when.

## References

- `references/polish_rubric.md` — Per-section polish rules, hedging calibration table, paragraph-length heuristics, Golden Thread report template
- `references/abstract_template.md` — Abstract structural template, hard rules, journal-specific word limits
- `scripts/polish_checks.py` — Deterministic checks for paragraph length, terminology variants, abstract rule compliance
