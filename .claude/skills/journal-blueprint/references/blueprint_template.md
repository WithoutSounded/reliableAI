# Blueprint Template — `step1_blueprint.md`

Canonical structure for the paper blueprint. Produce a markdown file with exactly these seven top-level sections, in this order. Downstream skills (journal-draft, journal-polish) parse section headings; do not rename them.

Bilingual convention: narrative text (Narrative Objective, Core Argument, subsection titles, subsection theses, transition plans) is bilingual EN + 繁中. Structured fields (JSON profiles, evidence tables, equation maps) remain in English.

---

## Template — paste this structure and fill in

````markdown
# Paper Blueprint — {paper_slug}

**Session:** {session_id}
**Target journal:** {target_journal} (word limit: {word_limit})
**Created:** {YYYY-MM-DD}

---

## 1. Narrative Objective

**EN.** One directional sentence: we show that X solves Y that prior work Z could not, by doing W.

**繁中.** 一句話方向性陳述：我們證明 X 解決了先前 Z 方法無法處理的 Y 問題，透過 W 的方式。

---

## 2. Core Argument — Golden Thread

**EN.** One falsifiable, specific, traceable claim that runs through every section.

**繁中.** 一句可被反駁、具體、可追溯的核心論點，將貫穿全文每個章節。

**Primary evidence anchor.** The figure or table that most directly supports the core argument (e.g., "Fig 3 (ablation of gating)"). Step 5 (polish) traces the thread from this anchor.

---

## 3. Section Profiles

Profiles below are the contract Step 2 (drafting) writes against. Fields follow `references/section_profile_defaults.md`.

```json
{
  "introduction": {
    "tone": "...",
    "tense": "...",
    "citation_density": "...",
    "hedging_level": "...",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "...",
    "word_budget": 800
  },
  "related_work": { ... },
  "methods": { ... },
  "results": { ... },
  "discussion": { ... },
  "conclusion": { ... },
  "abstract": { ... }
}
```

**Include only sections that appear in `step0_session_config.json.section_structure`.** Journals that fold Related Work into Introduction (JAACAP, many Nature-family venues) should **omit** the `related_work` key entirely — not include it with `word_budget: 0`. Step 2 iterates this JSON's keys and will create a file for every key present, so empty-budget keys produce empty section files.

**Budget check.** Sum of section word_budgets: {X} / journal limit {Y} ({Z}%). Target ~90% to leave room for headings, captions, references.

**Profile adaptations.** If any profile deviates from the default family for the target journal, note the reason here (e.g., "Discussion budget cut to 1200 because Nature-family prefers brief discussion").

---

## 4. Evidence Mapping

For every section, name the source artifacts, the figures/tables placed, the citation keys expected, and the key claims with their evidence sources.

### 4.1 Introduction
- **Source artifacts.** `sota_review.md §{X}`, `gap_analysis.md §{Y}`, `hypothesis_specification.md`, (research-write) `01_intro.tex` for framing reference only
- **Figures/tables placed.** none (unless target journal allows)
- **Citation keys expected.** [CitationKey1, CitationKey2, ...] (typically 10–20 for Introduction)
- **Key claims + evidence.**
    - Claim 1 → `sota_review.md §2.1`
    - Claim 2 (the gap statement) → `gap_analysis.md §3`
    - Claim 3 (the hypothesis) → `hypothesis_specification.md §1`

### 4.2 Related Work
- (same structure)

### 4.3 Methods
- **Source artifacts.** `architecture_spec.md`, `pseudocode.md` (Phase 1a output)
- **Figures/tables placed.** Fig 1 (architecture diagram)
- **Citation keys expected.** method-origin citations only, typically 5–10
- **Key claims + evidence.**
    - Model definition → `architecture_spec.md §{X}` + `pseudocode.md Alg 1`
    - Training procedure → `architecture_spec.md §{Y}`

### 4.4 Results
- **Source artifacts.** `analysis_summary.md`, `figure_captions.md`, `table_captions.md`
- **Figures/tables placed.** Fig 2, Fig 3, Fig 4, Table 1, Table 2
- **Citation keys expected.** none (own work)
- **Key claims + evidence.**
    - Main result → `analysis_summary.md §{X}` / Table 1
    - Ablation → `analysis_summary.md §{Y}` / Fig 3

### 4.5 Discussion
- **Source artifacts.** `analysis_summary.md` (interpretations), `sota_review.md` (comparisons), `experiment_report.md §interpretation`
- **Figures/tables placed.** refer back to Results figures (no new figures)
- **Citation keys expected.** moderate-high, typically 15–25 for comparisons
- **Key claims + evidence.**
    - Interpretation of main result → `experiment_report.md §{X}`, compared against `sota_review.md §{Y}`
    - Limitation → `experiment_report.md §{Z}` or analysis_summary.md

### 4.6 Conclusion
- **Source artifacts.** all prior sections (summary)
- **Figures/tables placed.** none
- **Citation keys expected.** none
- **Key claims + evidence.** list of concrete contributions (should match the Introduction's contribution list exactly); at least 1 limitation; future work direction

### 4.7 Abstract
- **Source artifacts.** written last; draws only from the polished full paper
- **Figures/tables placed.** none
- **Citation keys expected.** none
- **Key claims + evidence.** every number in Abstract must trace to a Results subsection

### Orphan check
- [ ] Every figure in `figure_captions.md` is placed in exactly one section above.
- [ ] Every table in `table_captions.md` is placed in exactly one section above.
- [ ] Any figure/table NOT placed: list here and decide (add to a section, or remove from catalog).

### Unsupported-claim check
- [ ] Every key claim above names a specific source file + location.
- [ ] Any claim without a named source: list here and flag to user at Checkpoint 1.

---

## 5. Subsection Outline

Per section, define subsections with title, thesis, evidence, and transition. This is the **contract** Step 2's sliding window executes against.

### 5.1 Introduction

#### §1.1 (title)
- **EN thesis:** One-sentence statement of what this subsection establishes.
- **繁中 thesis:** 一句話說明本小節要建立什麼論點。
- **Evidence:** [citation keys, equations, figures]
- **Transition EN:** How §1.1 hands off to §1.2.
- **Transition 繁中:** §1.1 如何承接到 §1.2。

#### §1.2 (title)
- ...

(Repeat for each section's subsections. Methods and Results typically have 3–6 subsections; Introduction 3–4; Discussion 2–4; Related Work 2–4 thematic clusters; Conclusion 1–3; Abstract no subsections.)

---

## 6. Writing Order

**Order:** Methods → Results → Introduction → Related Work → Discussion → Conclusion → Abstract

**Rationale (if default):** Most concrete material first; Introduction calibrates to what the paper actually delivers; Abstract summarizes a finished paper.

**Override (if non-default):** Explain why — e.g., target journal requires combined Results+Discussion; Introduction must be drafted first because the gap is still evolving.

---

## 7. Cross-Agent Validation Plan

Plan for Step 2 to compare its Introduction against Research Agent's `step9_manuscript/01_intro.tex`.

- **Gap statement expected in both:** {one sentence}
- **Hypothesis framing expected in both:** {one sentence}
- **Foundational citation keys expected in both:** [Key1, Key2, Key3]
- **Divergence threshold:** significant = either version cites a different foundational paper, or frames the gap categorically differently (e.g., "data scarcity" vs "modeling limitation"). Minor wording differences are expected and not flagged.

---

## Appendix A — Known Gaps / Deferred Decisions

Any open questions the blueprint couldn't resolve yet. These become the first Checkpoint 1 discussion topics. Examples:

- "Methods §3.5 training details assume learning rate 1e-4 but analysis_summary notes 5e-5 for the final run — need confirmation before Step 2."
- "Discussion §5.2 limitation on sample size: unclear whether to frame as external validity threat or as power concern."

---
````

## Notes on filling the template

- **Do not leave placeholder `{X}` markers in the output.** If a value is genuinely unknown (e.g., Algorithm Agent hasn't run), write `[AWAITING_ALGORITHM]` or `[AWAITING_USER_DECISION]` — explicit markers are safer than empty braces.
- **Subsection numbering follows the section profile's narrative_pattern.** Figure-driven sections (Results) should have one subsection per figure or per tightly-related figure group. Thematic sections (Related Work) should have one subsection per theme from the SOTA review.
- **Every `Evidence` entry should use real citation keys or file references** — not TODOs. If a citation is still uncertain, list the candidate keys and note the uncertainty.
- **Keep the bilingual parts bilingual.** Skipping Chinese in the thesis statements defeats the purpose of Checkpoint 1 review.
