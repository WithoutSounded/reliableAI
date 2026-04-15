---
name: journal-revise
description: "Fix or revise a journal manuscript draft after review feedback has been generated. Reads structured review flags (HALLUCINATION, NUMBER_MISMATCH, PHANTOM_CITATION, OVERCLAIM, VISUAL_TEXT_MISMATCH, CROSS_SECTION_INCONSISTENCY, etc.) from step3_review_r{N}.json and rewrites flagged sections to resolve every issue while preserving unflagged sections verbatim. Supports full revision, selective fixes ('fix only critical flags'), and user overrides on specific flags. Produces step4_draft_v{N+1}/ with a per-flag revision log. This is Step 4 of the Journal Writing Agent pipeline. Invoke via '/journal revise' or whenever the user wants to apply review feedback, fix flagged issues, or revise a manuscript after review. Triggers on: '修訂草稿', '根據審閱修改', '把 flags fix 掉', 'fix the flagged issues', 'apply review feedback', 'revise the draft', 'checkpoint 2 過了'. NOT for reviewing/checking a draft (use journal-review), NOT for initial drafting (use journal-draft), NOT for polishing (use journal-polish)."
---

# Journal Revise — Step 4 of Journal Writing Agent Pipeline

You are revising a manuscript draft to resolve every issue identified in the review. Your job is surgical: fix what the review says is broken, don't touch what isn't flagged, and document every change you make so the human author can verify.

The revision produces a complete new draft version (`step4_draft_v{N+1}/`) plus a revision log (`_revision_log.md`). Together, these let the author see exactly what changed and why — no hidden edits, no silent rewrites.

## Input

Locate and read these files from the journal session folder (paths relative to the session root, e.g., `Journal/{session_id}_{paper_slug}/`):

1. **`step0_session_config.json`** — Session metadata. Read `review_round` to determine N, and `artifacts` paths for upstream sources.
2. **`step3_review_r{N}.json`** — The review feedback. Contains structured flags with `id`, `type`, `severity`, `location`, `quote`, `evidence_expected`, `instruction`, and `source_file`. This is your primary task specification — every flag is a task to complete.
3. **`step2_draft_v{N}/`** — The latest draft version. Contains `01_introduction.tex` through `06_conclusion.tex`. If this is a second revision round, the input may be `step4_draft_v{N}/` instead (the previous revision output).
4. **`step2_global_config.json`** — Glossary, tense lock, section profiles.
5. **`step1_preprocess/`** — Ground truth files (figure_captions.md, table_captions.md, notation_glossary.md, equation_plan.md) used to verify your rewrites.
6. **Upstream artifacts** (for fact-checking rewrites):
   - Algorithm Agent's `step4_analysis_summary.md` — ground-truth numbers
   - Research Agent's `step4/references.bib` — valid citation keys

If the user provides overrides at Checkpoint 2 (e.g., "Accept all except F003: [custom instruction]"), those overrides replace the original `instruction` field for the specified flags.

## Procedure

### Phase 1: Triage and Plan

Before writing any revised text, analyze the review as a whole.

1. **Read the full review JSON.** Group flags by file (section). Note which sections have flags and which are clean.
2. **Detect systemic issues.** If multiple flags point to the same root cause, address the root cause rather than patching each symptom individually. Common systemic patterns:
   - Multiple `NUMBER_MISMATCH` or `HALLUCINATION` flags with the same wrong number → a single source value was wrong during drafting
   - `SYMBOL_CONFLICT` across sections → the notation glossary needs updating (do this first, then fix all symbol usage)
   - `CROSS_SECTION_INCONSISTENCY` between Introduction and Conclusion → align contribution lists once, not twice
   - Repeated `OVERCLAIM` → the tone calibration for Discussion needs resetting globally, not per-sentence
3. **Check for cascading dependencies.** Some fixes depend on others:
   - If F001 changes a number in Results, check whether Discussion or Conclusion references that same number (even if those sections don't have their own flag for it)
   - If F011 (`MISSING_FIGURE_FLOATS`) asks to add float environments, you'll need the figure/table captions from `step1_preprocess/figure_captions.md` and `table_captions.md`
   - If a `PHANTOM_CITATION` is removed, check whether the sentence still makes sense without it
4. **Update Global Config if needed.** If the review revealed systemic terminology or tense issues:
   - Add missing terms to the glossary
   - Tighten tense rules if tense violations were flagged
   - Note these updates in the revision log

### Phase 2: Revise Flagged Sections

Process each flagged section. For each section file that has one or more flags:

#### 2a. Build Revision Context

Before rewriting, assemble what you need:

| Slot | Content | Purpose |
|------|---------|---------|
| Original draft | The current `.tex` file for this section | What you're editing |
| Flags for this section | All flags from `step3_review_r{N}.json` where `location.file` matches | Your task list |
| User overrides | Custom instructions from Checkpoint 2 (if any) | Override the flag's default `instruction` |
| Section profile | From `step2_global_config.json` — tone, tense, hedging, citation density | Constraints for the rewrite |
| Source materials | Relevant upstream files cited in the flags' `source_file` fields | Ground truth for fact-checking your rewrite |

#### 2b. Rewrite

For each flag in the section, apply the fix specified in the `instruction` field (or the user's override). Follow these principles:

**Minimal edit radius.** Change only what the flag requires. If a flag targets one sentence, rewrite that sentence — don't rewrite the whole paragraph unless the fix structurally requires it (e.g., removing a sentence that was the paragraph's topic sentence). Preserving the author's voice and structure is important; the review catches errors, not style preferences.

**Fact-check every rewrite.** After writing a revised sentence that contains a number, citation, or factual claim, immediately verify it against the source files (`analysis_summary.md`, `figure_captions.md`, `references.bib`). A revision that introduces a new error is worse than the original.

**Respect the section profile.** Your rewrite must comply with the section's tense lock, tone, hedging level, and citation density from `step2_global_config.json`. For example:
- Results: past tense for experiments, present for what figures show. No interpretation. Minimal hedging.
- Discussion: present for implications, past for literature comparisons. High hedging ("may suggest", "indicates").
- Conclusion: no new information. Past tense for summary.

**Handle each flag type appropriately:**

| Flag Type | How to Fix |
|-----------|-----------|
| `HALLUCINATION` | Delete the fabricated claim, or replace with the correct information from the source file. Never try to "soften" a hallucination — if the data doesn't support it, remove it. |
| `NUMBER_MISMATCH` | Replace the wrong number with the correct one from `analysis_summary.md` or `figure_captions.md`. Check whether the surrounding sentence still makes sense with the corrected number. |
| `PHANTOM_CITATION` | Remove the fake citation key. If the sentence needs a citation, find a real one from `references.bib`. If no appropriate citation exists, rewrite the sentence to not require one. |
| `EXAGGERATION` | Dial down the language to match the evidence strength. Replace "significantly outperforms" with "outperforms" if p is marginal; replace "all datasets" with the actual scope. |
| `OVERCLAIM` | Add hedging language appropriate to the evidence. "demonstrates" → "suggests" for moderate evidence. "confirms" → "supports" for marginally significant results. |
| `UNDERCLAIM` | Strengthen the language since the evidence warrants it. "may suggest" → "demonstrates" when p<0.01. This is about impact — don't undersell strong results. |
| `LOGIC_BREAK` | Trace the contradicting statements across sections. Fix the incorrect one (verify against source data which statement is right). If both are partially correct, reconcile. |
| `CROSS_SECTION_INCONSISTENCY` | Pick the correct version (verify against source data), then update all locations to be consistent. Common: aligning contribution lists between Introduction and Conclusion, matching participant counts across all sections. |
| `VISUAL_TEXT_MISMATCH` | Rewrite the text to accurately describe what the figure/table shows (per `figure_captions.md` / `table_captions.md`). Match trend direction, magnitudes, and significance markers exactly. |
| `MISATTRIBUTION` | Either find the correct citation for the claim, rewrite the claim to match what the cited paper actually says, or remove the attribution if no source supports it. |
| `MISSING_CITATION` | Add an appropriate `\cite{Key}` from `references.bib`, or soften the claim if no citation is available (e.g., "It has been observed that..." instead of stating as established fact). |
| `ORPHAN_BIB_ENTRY` | Note for the finalize step — no tex edit needed here. Log in revision log that the entry should be pruned from references.bib. |
| `ORPHAN_FIGURE` / `BROKEN_REF` | Add `\ref{}` to appropriate location in text, or add `\label{}` / float environments as instructed. |
| `MISSING_FIGURE_FLOATS` | Add `\begin{figure}` / `\begin{table}` float environments with proper `\label{}` and `\caption{}` at the first `\ref{}` location in each section. Use captions from `figure_captions.md` and `table_captions.md`. |
| `SYMBOL_CONFLICT` | Use the canonical symbol from `notation_glossary.md`. If the glossary itself needs updating (as the flag may suggest), note the glossary update in the revision log. |
| `EXPENDABLE` | Either delete the paragraph, merge its essential content into an adjacent paragraph, or convert to a forward/backward reference as the flag suggests. |
| `OVER_BUDGET` / `UNDER_BUDGET` | For over-budget: tighten prose, remove redundancy. For under-budget: this is informational — expansion is usually handled in the next drafting pass, not in revision. Note in the log. |

#### 2c. Self-Check

After revising a section, re-read the revised text and verify:

1. **No new errors introduced.** Every number still matches source data. Every `\cite{}` key exists in `references.bib`. Every `\ref{}` has a `\label{}`.
2. **Brick Layer rules still hold:**
   - Methods: every math expression matches notation_glossary.md, every dimension is traceable
   - Results: every number comes from source data, every subsection references a figure/table, no interpretation
   - Introduction: factual claims have citations, funnel structure preserved
   - Discussion: hedging language on interpretive claims, comparisons cite specific papers
   - Conclusion: no new information, contributions are numbered, at least one limitation acknowledged
3. **Surrounding context still flows.** If you deleted or substantially rewrote a paragraph, check that the transition from the previous paragraph and into the next paragraph still reads smoothly. Add a brief transition sentence if needed.
4. **Cross-section ripple effects.** If you changed a claim, number, or contribution item, check whether the same claim appears in other sections. Fix those too, even if they weren't explicitly flagged. Log these as "cascade fix from F00X" in the revision log.

### Phase 3: Copy Clean Sections

For every section file that has **no flags**, copy it verbatim into the new draft directory. Do not edit, rephrase, or "improve" clean sections — that would introduce unreviewed changes and undermine the trust model of the pipeline.

### Phase 4: Write Revision Log

Create `_revision_log.md` in the output draft directory. This is the author's audit trail — it must be complete enough that someone reading only the log can understand every change without diffing the files.

Format:

```markdown
# Revision Log — Draft v{N} → v{N+1}

Review round: {N}
Date: {ISO 8601}
Flags addressed: {count} / {total flags in review}

## Global Config Updates

{If any glossary, tense, or profile changes were made, list them here. Otherwise: "None."}

## Per-Section Changes

### 01_introduction.tex

#### F001 (PHANTOM_CITATION, critical)
- **Flag**: Removed fabricated citation `\cite{WangNonExistent2025}`
- **Action**: Deleted the citation. Sentence rewritten to be self-referential without external attribution.
- **Verification**: No remaining references to WangNonExistent2025 in any .tex file.

#### F004 (CROSS_SECTION_INCONSISTENCY, critical)
- **Flag**: Participant count mismatch (Introduction says 50, rest of paper says 45)
- **Action**: Changed "50 participants" to "45 participants" in contribution item (3).
- **Verification**: N=45 matches analysis_summary.md. Checked all other sections — consistent.

{... continue for all flags in this section ...}

### 02_related_work.tex

**No flags — copied verbatim from draft v{N}.**

{... continue for all sections ...}

## Cascade Fixes

{List any fixes applied to sections that weren't explicitly flagged, triggered by ripple effects from other flags. E.g., "Fixed participant count in Methods (cascade from F004 in Introduction)."}

## Unresolved Items

{List any flags that could not be fully resolved. E.g., "F018: electrode pair specification requires information not available in source files — flagged for human author to provide." This should be rare.}
```

## Output

1. **`step4_draft_v{N+1}/`** — Complete section set: revised sections + verbatim-copied clean sections. Same file names as the input draft (`01_introduction.tex` through `06_conclusion.tex`).
2. **`step4_draft_v{N+1}/_revision_log.md`** — Per-flag resolution record.
3. **Update `step0_session_config.json`**: set `current_step` to 4. Do not increment `review_round` — that happens when `journal-review` runs again.

After writing the outputs, present a summary to the user:
- How many flags were addressed, by severity
- Key changes made (top 3 most impactful)
- Any cascade fixes applied
- Any unresolved items that need human input
- Recommendation: "可以進行下一輪審閱" (ready for re-review) or "建議直接進入潤稿" (ready for polish) if all issues were minor

This sets up the iterative loop: if the user says "再審一輪", the revised draft goes back to `journal-review` (Step 3). If the user says "通過", it proceeds to `journal-polish` (Step 5).
