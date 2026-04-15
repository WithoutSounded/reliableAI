---
name: journal-draft
description: "Produces the complete first draft (step2_draft_v1/) of a journal manuscript — one .tex file per section — via a disciplined sliding-window pass over the blueprint + preprocess artifacts, locking style/glossary/tense in step2_global_config.json and tracking per-section summaries and citations in _sliding_window_state.json. Fire this skill whenever the user asks to draft, write, or generate the first version of a paper — e.g. '/journal draft', '寫第一版草稿', '產生初稿', '開始寫論文', '藍圖通過了開始寫', 'checkpoint 1 passed', 'proceed to step 2', 'draft the manuscript', 'write draft v1', 'run the sliding window', or right after journal-blueprint finishes and Checkpoint 1 is green-lit. Use this skill even when the user only says 'start writing' or 'begin the paper' without naming a step — drafting a manuscript from a completed blueprint is exactly what this is for. Step 2 of the Journal Writing Agent pipeline; enforces per-section Brick Layer rules (Methods = no interpretation, Results = figure-anchored + no causal language, Introduction = every claim cited, Discussion = hedged, Conclusion = no new information) and cross-validates the Introduction against the Research Agent's step9_manuscript/. NOT for blueprint design (journal-blueprint), NOT for reviewing a finished draft (journal-review), NOT for applying review fixes (journal-revise), NOT for abstract/prose polish (journal-polish)."
---

# Journal Draft — Step 2 of Journal Writing Agent Pipeline

You are the **drafter**. Your job is to turn the blueprint (the plan) and the preprocessed materials (the ground truth) into a complete first draft, section by section, subsection by subsection, via a disciplined sliding-window mechanism that keeps the paper internally coherent as it grows.

This is the longest step in the pipeline and the one with the widest failure surface. The blueprint has already committed to what story the paper tells and where each piece of evidence lives; your job is disciplined execution — no reinterpretation, no novel claims, no improvisation. Every number, every citation, every figure reference must be traceable back to the preprocess files or upstream artifacts. Novel claims introduced at this stage propagate silently through Steps 3, 4, 5, and 6 before a human catches them — if they ever do.

Three principles govern everything here:

1. **Blueprint is law. Source material is truth. Draft is execution.** If the blueprint says Results §4.2 claims "F1 drops by 0.08 when gating is removed" and names `analysis_summary.md §3.2 row 2` as the source, your job is to express that claim in polished academic English with the correct citation/figure reference — not to reinterpret it, expand it, soften it, or add "additional context" the blueprint didn't plan. Inventing beyond the blueprint is the #1 source of downstream hallucinations.

2. **The sliding window exists to prevent both amnesia and repetition.** Before drafting any subsection, you need to know: the section-level plan (from blueprint), the last paragraph of the reading-order predecessor (so your opening transitions in), and — if it's already been drafted in an earlier writing-order step — the first paragraph of the reading-order successor (so your closing transitions out). After drafting, emit a 2–3 sentence summary so later windows can read-back without reloading your full text.

3. **Brick Layer rules are section-specific hard constraints, not stylistic suggestions.** A causal claim in Results is a bug even if it sounds natural. A Discussion paragraph without hedging is a bug even if the evidence feels strong. A Methods paragraph interpreting why a design choice matters is a bug even if the reasoning is correct (interpretation belongs in Discussion). These rules exist because Step 3 (review) checks them mechanically — if you violate them here, you produce review flags that cascade into Step 4 rework.

## Input

Read from the journal session folder (e.g., `Journal/{session_id}_{paper_slug}/`):

1. **`step0_session_config.json`** — target journal, word limit, `section_structure`, `writing_order`, upstream session paths. Read first to locate everything else.
2. **`step1_blueprint.md`** — the contract. Contains Narrative Objective, Core Argument (Golden Thread), Section Profiles (tone/tense/hedging/word-budget per section), Evidence Mapping (which figures/tables/citations/claims go where), Subsection Outline (thesis + evidence + transition per subsection), Writing Order, Cross-Agent Validation Plan.
3. **`step1_preprocess/`** — ground-truth reference files:
    - `figure_captions.md` — every figure with caption, key numbers, trend direction
    - `table_captions.md` — every table with columns, best/worst values, significance
    - `pseudocode.md` — algorithm blocks ready to drop into Methods
    - `notation_glossary.md` — canonical math symbol definitions
    - `equation_plan.md` — equation numbers and cross-reference plan
4. **Upstream artifacts** (paths from session config; read only the portions needed for the current section):
    - Research Agent: `step4_references.bib`, `step4_citation_keys.md`, `step6_sota_review.md`, `step7_gap_analysis.md`, `step8_hypothesis_specification.md`, `step5_full_text/*.md`, `step9_manuscript/01_intro.tex` (for cross-validation only — not starting point)
    - Algorithm Agent: `step1_architecture_spec.md`, `step1_ablation_matrix.md`, `step4_analysis_summary.md`, `step6_experiment_report.md`

If critical upstream artifacts are missing, stop and report rather than filling gaps with plausible-sounding content. A draft built on fabricated evidence is strictly worse than no draft — Step 3 may not catch every fabrication, and the further downstream a hallucination survives, the more expensive it becomes to fix.

## Procedure

Four phases, executed in order. Phase 2a freezes the style constraints; 2b is the main drafting loop; 2c is a narrow cross-validation hook fired once; 2d is self-check before handing back to the user.

### Phase 2a — Global Config Setup

Build `step2_global_config.json`. This file is the frozen style/terminology contract for this draft version. Step 3 (review), Step 4 (revise), and Step 5 (polish) will all read it as ground truth — so inconsistencies here cause downstream violations even if the draft itself is careful.

Run the bootstrap script to assemble a scaffold from the blueprint and preprocess files:

```bash
python <skill_path>/scripts/init_global_config.py \
  --session-path <journal_session_path> \
  --output <journal_session_path>/step2_global_config.json
```

The script copies section profiles from the blueprint, seeds the glossary from `notation_glossary.md`, and derives tense-lock rules from the profiles. After it runs, inspect the output and fill in:

- **Glossary** — Beyond the math symbols already pulled from `notation_glossary.md`, add domain terms you'll reuse across sections (e.g., "fuzzy gating layer", "non-stationary EEG drift", "attention decoding"). Each entry: `{term, definition, first_appears_in: section}`. Flag any term that has alternative spellings the draft should avoid (e.g., prefer "state-of-the-art" not "SOTA" in prose; prefer "electroencephalography (EEG)" on first use, then "EEG").
- **Granularity Level** — One sentence describing the target reader's background (e.g., "expert in BCI, familiar with deep learning, not specialized in fuzzy logic"). This calibrates how much a concept must be explained vs. cited. Derive from `step8_journal_recommendations.md` if available.
- **Citation format** — `\cite{Key}` by default. If target journal requires `\citep/\citet` (natbib) or numeric bracketed style, set accordingly.

See `references/global_config_template.md` for the complete schema and worked examples.

**If `step2_global_config.json` already exists** (e.g., a prior run bootstrapped it, or a meta-skill ran `init_global_config.py` for you, or the user hand-filled parts of it), **do not re-run the bootstrap script** and **do not use `Write` to rewrite the whole file** — both will overwrite or drop user-entered glossary, granularity, and tense-lock content. The failure mode we have repeatedly seen: the agent reads the existing config, mentally reconstructs what a "complete" config looks like, and writes that reconstruction — silently losing any field the agent forgot to carry over (most commonly `granularity`, because it's a single string nested among large objects and easy to miss).

Instead, follow this mechanical recipe so no field can be lost:

1. **Record the original key set first.** Before doing anything else, list the top-level keys of the existing file — e.g., run `python -c "import json; print(list(json.load(open('step2_global_config.json')).keys()))"` — and write them down in your working notes. This is the key set you must still see after you are done.
2. **Use the `Edit` tool, one TODO at a time.** For each field whose value is literally the string `"TODO"` (or a placeholder like `"fill from section profiles"`), call `Edit` with `old_string` = the exact JSON line/fragment containing the placeholder (enough surrounding context to make it unique) and `new_string` = the same line with the real value. Never call `Write` on this file. Never pass a reconstructed full-config object.
3. **Verify after.** Re-list the top-level keys. The set must equal the set you recorded in step 1 — no additions, no deletions. If any key is missing, you have silently overwritten user content; stop, re-read the original from git or the iteration-1 snapshot, and restore the field.
4. **Report what you preserved, not what you produced.** Your user-facing summary must name the preserved fields by value, not just by key — e.g., "preserved 3 glossary entries (fuzzy gating layer, non-stationary EEG drift, dyadic social interaction) and the granularity paragraph starting 'Target reader is an expert in BCI…'". Naming values forces you to actually read them; naming only keys is too easy to fake.

Regenerating unprompted is the single most destructive failure mode of this phase — it silently destroys careful user work and the user has no way to notice until a downstream section drifts.

### Phase 2b — Sliding Window Execution

Iterate over sections in the **writing order** from the blueprint (default: Methods → Results → Introduction → Related Work → Discussion → Conclusion). **The Abstract is written in Step 5 (polish), not here** — skip it at this stage. Within each section, iterate over its subsections in reading order. For every subsection, build the context window, draft, then emit a summary.

A few terms that are easy to confuse — pin them down now:

- **Reading order** = the order sections appear in the final PDF (Intro → RW → Methods → Results → Discussion → Conclusion).
- **Writing order** = the order you draft them in (default: Methods first, Intro third, etc.).
- **Reading-order predecessor** of the current subsection = the subsection that appears _just before_ it in the final paper. It may or may not already be drafted — depends on whether its section came earlier in writing order.
- **Reading-order successor** = the subsection _just after_ it in the final paper. Same conditional availability.

Worked example: you are drafting Results §4.1. Reading-order predecessor is Methods §3 (last subsection) — already drafted. Reading-order successor is Discussion §5.1 — not drafted yet, so no successor context. When you later draft Discussion §5.1, the successor is Conclusion §6 — also not drafted yet (Conclusion comes later in writing order). When you draft Introduction §1 (third in writing order), the predecessor is empty (Intro is the first section in reading order) and the successor is Related Work §2.1 — not drafted yet.

See `references/sliding_window_protocol.md` for the exact context-window construction rules and how to handle the "predecessor/successor not yet drafted" cases.

#### The Context Window (per subsection)

| Slot | Content | Source |
|------|---------|--------|
| Global Config | Glossary + tense lock + section profile for the current section + granularity | `step2_global_config.json` |
| Blueprint excerpt | Current subsection's thesis, evidence list, transition plan, word budget | `step1_blueprint.md` |
| Reading-order predecessor | Last paragraph + summary of the previous subsection (if drafted) | Prior window output |
| Reading-order successor | First paragraph + summary of the next subsection (if drafted) | Prior window output |
| Source materials | Only the specific rows/figures/captions/citations named in the blueprint's evidence mapping for this subsection | `step1_preprocess/*`, upstream artifacts |
| Brick Layer rules | The rules for this section type (Methods/Results/Intro/RW/Discussion/Conclusion) | `references/brick_layer_rules.md` |

**Do not pull in material that isn't mapped.** If the blueprint's evidence mapping for Results §4.2 names Fig 4 and Table 2, don't also cite Fig 6 because it "seems related". That's the blueprint's job to allocate, not yours to re-allocate. If you spot a genuine missing allocation while drafting, stop and flag it in `_sliding_window_state.json` under `blueprint_gaps` — the user decides at a later checkpoint whether to patch the blueprint or ignore.

#### Brick Layer Rules (per section type)

Six section types, six rule sets. Before drafting each section, reread the relevant rule set from `references/brick_layer_rules.md`. Summary:

- **Methods** — past tense for what was done, present tense for what the model is; every mathematical expression must match `notation_glossary.md`; every dimension must be traceable through the forward pass; every hyperparameter has either a value or `(see Section 4 for ablation)`; no interpretation of why a design is "better" — that belongs in Discussion.
- **Results** — past tense for experiments ("we measured"), present tense for what figures show ("Fig. 3 shows"); every number comes from `analysis_summary.md` or `figure_captions.md` verbatim; every subsection references at least one figure or table; no causal language ("because", "due to", "demonstrates that X causes Y") — state what was observed, not why.
- **Introduction** — every factual claim has a `\cite{}`; the funnel narrows from broad context to specific gap in ≤4 paragraphs; the final paragraph states the contribution explicitly and previews section structure; no figures; moderate hedging. **If `step4_references.bib` is not reachable**, do not drop citations entirely — that silently reshapes the Introduction into a citation-free essay and costs the user a follow-up pass. Instead, emit `\cite{TODO_short_slug}` placeholders (e.g., `\cite{TODO_ADHD_prevalence}`, `\cite{TODO_EEG_BCI_review}`) wherever a cite would go in the final draft, and record the full list of placeholder keys in `_sliding_window_state.json.blueprint_gaps` so the user can resolve each one in a single subsequent pass. A `\cite{TODO_*}` key is a visible scaffold, not a fabricated citation.
- **Related Work** — every paragraph cites ≥2 papers; thematic grouping, not chronological; ends with a **positioning paragraph** ("In contrast to prior work, we …") that ties directly to the Introduction's contribution claim; no interpretation of the present paper's results.
- **Discussion** — every interpretive claim hedged ("may suggest", "one possible interpretation", "these findings indicate"); every comparison with prior work cites the specific paper and metric ("our F1 of 0.87 exceeds the 0.81 reported by Chen2023 on the same benchmark"); acknowledge limitations explicitly; mirrors the Results structure (discuss what was reported, in the order it was reported).
- **Conclusion** — no new information, no new citations; numbered contribution list (≤4 items); ≥1 acknowledged limitation; forward-looking final sentence (future work).

The full text — worked examples, prohibited phrasings, tense checklists — is in `references/brick_layer_rules.md`.

#### Per-Window Output

For each subsection you draft, emit three artifacts:

1. **LaTeX content** — appended to the section's `.tex` file. Include `\label{sec:...}` on the subsection heading; use `\cite{Key}` (or the configured format) for citations; use `\ref{fig:...}` / `\ref{tab:...}` / `\ref{eq:...}` for cross-references. **Introduction and Conclusion are typically single-flow prose** — it is acceptable (and often preferred) to write them without explicit `\subsection{}` headings, as long as their internal argumentative arc is still visible in the subsection summaries you emit. Methods, Results, and Discussion should use `\subsection{}` headings because their subsections map directly to blueprint evidence groupings that Step 3 verifies. Related Work typically uses `\subsection{}` for thematic groups. When in doubt, match the blueprint's subsection outline.
2. **Subsection summary** (2–3 sentences, English) — captures what this subsection established or argued, and how it transitions forward. Written so later windows can read it without reloading your full text. Store in `_sliding_window_state.json` under `subsections[{section}.{subsection_id}].summary`.
3. **Citation / figure / equation tracking** — list all `\cite{}` keys, `\ref{fig:*}`, `\ref{tab:*}`, `\ref{eq:*}` used. Stored in `_sliding_window_state.json` so Step 3 can cross-check against the blueprint's planned evidence mapping.

After every subsection is drafted, also emit a **section-level summary** (3–5 sentences) covering the section's overall argumentative arc. These section summaries are what the sliding window feeds into later sections' predecessor/successor slots. Store under `_sliding_window_state.json.sections[{section}].summary` and `.last_paragraph` / `.first_paragraph`.

#### The Section-Boundary Handoff

When closing one section and opening the next (in writing order), pause to ask: **does the section that will appear after this one in reading order exist yet?** If yes, read its first paragraph and section summary, and adjust the final paragraph of the section you just drafted so the transition reads naturally. This is where the draft earns the "sliding" in sliding window — the window slides both forward (what comes next in reading) and backward (what came before in reading), not forward in writing order.

Concrete example: After drafting Methods (first in writing order), there is no Results to transition into yet. Just draft Methods as is. After drafting Results (second in writing order), Methods exists — check the last paragraph of Methods, and make sure Results §4.1's opening connects to it. When later drafting Introduction (third in writing order), Related Work doesn't exist yet, but Methods does — so Introduction's final paragraph ("The rest of this paper is organized as follows…") can preview Methods and Results accurately. When later drafting Discussion (fifth), Results exists (predecessor) and Conclusion does not (successor) — so the Discussion opens from Results's last paragraph but closes without successor-shaping.

### Phase 2c — Cross-Agent Validation (fired once, after Introduction)

The moment Introduction is fully drafted, run the cross-agent check: compare your drafted Introduction against the Research Agent's `step9_manuscript/01_intro.tex` on three axes — **gap statement**, **hypothesis framing**, and **foundational citations**. The blueprint's Cross-Agent Validation Plan names the specific things to check.

This is an **alignment check, not a quality comparison**. The Journal Agent's Introduction is expected to be better-calibrated (it has seen the actual Results, figures, and methods). Significant divergence doesn't mean one is wrong — it means the Research Agent's framing diverged from what the paper actually delivers, which is a signal worth recording. Capture findings in `_sliding_window_state.json.cross_validation_flags`:

```json
"cross_validation_flags": [
  {
    "axis": "gap_statement",
    "journal_version": "Current EEG-ADHD classifiers fail under session-length drift, which prior work has not addressed.",
    "research_version": "Prior work has not evaluated EEG-ADHD classifiers on children.",
    "assessment": "Journal version is narrower and better-supported by our ablation results; Research version overgeneralized to a population claim.",
    "severity": "notable_divergence"
  }
]
```

No action is taken here — the flags are surfaced for the user at end-of-step review. Do not rewrite either version based on the comparison.

### Phase 2d — Self-Check

Before presenting to the user, run the draft validator:

```bash
python <skill_path>/scripts/validate_draft.py \
  --session-path <journal_session_path>
```

The script (see `scripts/validate_draft.py` for full rules) checks:

- Every section in `section_structure` (except Abstract) has a non-empty `.tex` file
- Every subsection from the blueprint's outline appears in the matching `.tex` (by `\label` or heading match)
- Every figure in `figure_captions.md` is `\ref{}`'d at least once across the draft
- Every `\cite{Key}` resolves to an entry in `step4_references.bib`
- Per-section word count is within ±15% of the blueprint's section word budget
- `_sliding_window_state.json` contains a summary for every drafted section
- `step2_global_config.json` is well-formed JSON with all required fields

Resolve any failures by editing the relevant `.tex` or `_sliding_window_state.json`. If word count is over budget, trim the subsection that drifted widest; if under, check whether any subsection was truncated and backfill. The validator is strict on purpose — it's cheaper to fix here than to reopen after Step 3 flags the same issues as `OVER_BUDGET` or `MISSING_CITATION`.

**If the validator can't be executed** (sandbox / Bash permission / missing Python): don't let that block the handoff. Walk the same rule list manually and record each result under `_sliding_window_state.json.self_check` as `{rule, status, evidence}`. Note in the user-facing summary that the automated validator did not run and the checks were performed by hand. Do not claim the validator passed when it didn't run.

**Under-budget is acceptable when upstream is missing.** If you had to surface `blueprint_gaps` for missing `references.bib`, missing analysis artifacts, or a blueprint with no evidence mapping, sections will naturally land under budget because padding them would require inventing citations or numbers — which is strictly forbidden. In that case: trim the budget expectation in the validator's eyes (annotate the section in `_sliding_window_state.json.sections[name].budget_adjusted_reason`), and do **not** pad with filler prose to hit the ±15% target. The Golden Thread requires every sentence be load-bearing; a short, defensible section beats a padded one.

## Output

Write these files into the journal session folder:

1. **`step2_draft_v1/01_introduction.tex`** through **`06_conclusion.tex`** — one self-contained section file per entry in `section_structure`, excluding `00_abstract.tex` (generated in Step 5). Files are ordered by reading order for clean `\input{}` sequencing later, not by writing order.

    **Filename convention**: `NN_lowercase_with_underscores.tex`. The NN is a fixed 2-digit reading-order index that you do **not** compute from `section_structure.index(...)` — use this exact table (assuming the default IMRaD+ layout):

    | Reading-order index | Section       | Filename                |
    |---------------------|---------------|-------------------------|
    | `00`                | Abstract      | (deferred to Step 5)    |
    | `01`                | Introduction  | `01_introduction.tex`   |
    | `02`                | Related Work  | `02_related_work.tex`   |
    | `03`                | Methods       | `03_methods.tex`        |
    | `04`                | Results       | `04_results.tex`        |
    | `05`                | Discussion    | `05_discussion.tex`     |
    | `06`                | Conclusion    | `06_conclusion.tex`     |

    Abstract occupies index `00` even though you are not producing it in this step. The first drafted file is **always** `01_introduction.tex`, the last **always** `06_conclusion.tex`. Do not index from 1 through 7 (which would push Methods to `04` and Conclusion to `07` — a common off-by-one that breaks the validator and Step 3/4 file lookups). If the blueprint defines a non-default `section_structure` (e.g., combined Results+Discussion for a Nature-family venue), preserve this gap-free `01`…`NN` convention and record the mapping in `step2_global_config.json.section_file_map`. Lowercase with underscores (`Related Work` → `related_work`, not `relatedwork` or `RelatedWork`).
2. **`step2_draft_v1/_sliding_window_state.json`** — per-section and per-subsection summaries, citation/figure/equation tracking, cross-validation flags, any blueprint gaps surfaced during drafting.
3. **`step2_global_config.json`** — frozen glossary, tense lock, section profiles, granularity, citation format. Lives at the session root (not inside `step2_draft_v1/`) because it spans versions — Step 4 revisions read the same config.

Then update `step0_session_config.json`:
- `current_step`: set to 2
- `artifacts.step2_draft_v1`: list of the section `.tex` file paths + `_sliding_window_state.json`
- `artifacts.step2_global_config`: path to `step2_global_config.json`

## Present to the User

After self-check passes, hand back a short summary:

1. **Sections drafted** (list with subsection count and word count per section)
2. **Total word count** vs. journal limit (with budget utilization %)
3. **Blueprint adherence**: # subsections drafted / # planned, any `blueprint_gaps` surfaced during drafting
4. **Evidence coverage**: # figures placed as planned, # citations used (of # planned in blueprint)
5. **Cross-agent validation**: count and severity of divergence flags from Phase 2c, with brief description of the most significant
6. **Self-check result**: pass/fail per item

Do **not** proceed to Step 3 automatically. The next step (`journal-review`) is user-triggered — the user may want to skim the draft, make manual edits, or adjust the blueprint and re-draft before invoking review. Say so explicitly: "Draft v1 complete. Next step is `journal-review` when you're ready — or edit `step2_draft_v1/*.tex` directly first if you want to make manual changes before review."

## References

The inline section-type summaries above are usually sufficient. Consult the full reference files when:

- A section's Brick Layer rule feels ambiguous in a specific case, or you're about to draft a section type the blueprint handles unusually (e.g., combined Results+Discussion for a Nature-family venue) → `references/brick_layer_rules.md`
- You hit a confusing predecessor/successor case (e.g., a section with no reading-order predecessor because it's first in the paper, or a section whose successor has already been drafted in an earlier writing-order step) → `references/sliding_window_protocol.md`
- Bootstrapping or extending `step2_global_config.json` (glossary format, granularity paragraph examples by journal family, tense_lock conventions) → `references/global_config_template.md`

Files:
- `references/brick_layer_rules.md` — per-section hard rules (Methods / Results / Intro / RW / Discussion / Conclusion), with prohibited phrasings and tense checklists
- `references/sliding_window_protocol.md` — exact context-window construction, predecessor/successor resolution, summary extraction templates
- `references/global_config_template.md` — `step2_global_config.json` schema, glossary conventions, granularity examples
- `scripts/init_global_config.py` — bootstrap `step2_global_config.json` from blueprint + preprocess
- `scripts/validate_draft.py` — self-check script (run in Phase 2d)
