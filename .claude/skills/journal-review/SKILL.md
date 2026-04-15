---
name: journal-review
description: "Systematically review a journal manuscript draft: run automated hard checks (citations, figures, numbers, symbols, word count), then perform AI-driven scientific claims review (hallucination detection, logic flow, overclaim detection), adversarial questioning (so-what test, cross-section consistency, visual-text alignment), and produce a structured JSON review with actionable flags. This is Step 3 of the Journal Writing Agent pipeline. Use this skill whenever the user wants to review a paper draft, check a manuscript for errors, audit scientific claims, verify citation integrity, or run quality checks on a LaTeX draft — including requests like 'review my draft', 'check the manuscript', '審閱草稿', '檢查論文'. Also triggers on '/journal review'."
---

# Journal Review — Step 3 of Journal Writing Agent Pipeline

You are reviewing a manuscript draft to catch errors, hallucinations, logical breaks, and overclaims before the human author sees it. Your job is to be a rigorous but fair internal reviewer — the kind of colleague who catches the mistake that would embarrass you at peer review.

The review produces a single structured JSON file (`step3_review_r{N}.json`) containing every issue found, categorized by type and severity. This file drives Step 4 (revision), so every flag must be specific enough for a reviser to act on without guessing what you meant.

## Input

Read these files from the journal session folder:

1. **`step2_draft_v{N}/`** — The latest draft. Contains `01_introduction.tex` through `06_conclusion.tex` and `_sliding_window_state.json`
2. **`step2_global_config.json`** — Glossary, tense lock, section profiles, citation format
3. **`step1_preprocess/`** — Ground truth files:
   - `figure_captions.md` — What each figure actually shows (key numbers, trends)
   - `table_captions.md` — What each table contains (best values, significance)
   - `notation_glossary.md` — Canonical symbol definitions
   - `equation_plan.md` — Equation numbering and cross-ref plan
4. **`step1_blueprint.md`** — Section word budgets, narrative structure
5. **Upstream artifacts** (for fact-checking):
   - Research Agent's `step4_references.bib` — citation pool
   - Algorithm Agent's `step4_analysis_summary.md` — ground-truth numbers
   - Algorithm Agent's `step5_figure_catalog.md` — figure inventory
   - Research Agent's `step5_full_text/*.md` — full text of cited papers (if available, for citation accuracy checks)

Locate these files using `step0_session_config.json` which contains `research_session` and `algorithm_session` paths. If critical files are missing, report what's missing and proceed with available materials — partial review is better than no review.

## Procedure

The review has four phases. Phases 3a and 3b–3c differ in nature: 3a is mechanical checking (deterministic, scriptable), while 3b–3c require judgment. Run 3a first — its results inform the later phases.

### Phase 3a: Automated Hard Checks

Run the `scripts/hard_checks.py` script against the draft. This script performs five machine-verifiable checks that produce binary pass/fail results:

```bash
python <skill_path>/scripts/hard_checks.py \
  --draft-dir <path_to_step2_draft_vN> \
  --bib-file <path_to_references.bib> \
  --preprocess-dir <path_to_step1_preprocess> \
  --blueprint <path_to_step1_blueprint.md> \
  --analysis-summary <path_to_analysis_summary.md> \
  --output <session_path>/hard_checks_output.json
```

The script checks:

| Check | What it does | Flag type |
|-------|-------------|-----------|
| **Citation completeness** | Every `\cite{Key}` has a matching bib entry; factual claims without `\cite{}` are flagged | `MISSING_CITATION`, `ORPHAN_BIB_ENTRY` |
| **Figure/table references** | Every figure in catalog is `\ref{}`'d; every `\ref{fig:X}` has a `\label{fig:X}` | `ORPHAN_FIGURE`, `BROKEN_REF` |
| **Number consistency** | Numbers in text (accuracy, F1, p-value, N) cross-checked against `analysis_summary.md` and `figure_captions.md` | `NUMBER_MISMATCH` |
| **Symbol consistency** | Math symbols match `notation_glossary.md`; same symbol with different meanings flagged | `SYMBOL_CONFLICT` |
| **Word count** | Per-section word count vs. budget from blueprint | `OVER_BUDGET`, `UNDER_BUDGET` |

Read the script output and incorporate flags into the final review, with two important post-processing steps:

1. **Batch structural flags**: If the draft is missing `\begin{figure}` / `\begin{table}` float environments entirely (common in early drafts), BROKEN_REF and ORPHAN_FIGURE flags will be numerous but stem from a single cause. Instead of listing each individually, consolidate into one structural flag: `MISSING_FIGURE_FLOATS` (major) with a note like "Add float environments for all 8 figures and 4 tables — this resolves 19 reference flags." This keeps the review actionable instead of noisy.

2. **Batch word-count flags**: If all sections are uniformly under budget (e.g., the draft is a skeleton), consolidate UNDER_BUDGET flags into one note rather than per-section flags.

The script may miss nuanced issues (e.g., a claim that's technically cited but the citation doesn't actually support it) — that's what Phase 3b is for.

### Phase 3b: Scientific Claims Review (三重比對)

This is the core intellectual work. Read each section of the draft carefully and perform three cross-checks. For each issue found, create a flag with the exact quote, the expected evidence, and a concrete instruction for how to fix it.

#### Check 1: Text vs. Data (防幻覺)

For every quantitative claim in Results and Discussion:
- Find the source number in `analysis_summary.md` or `figure_captions.md`
- Compare: does the text accurately represent the data?
- **`HALLUCINATION`** — the claim has no data support at all (the model invented a number or result)
- **`EXAGGERATION`** — data partially supports the claim but the text overstates it (e.g., "significant improvement" when p=0.08)

This check matters because LLM-drafted text sometimes confabulates specific numbers or invents trends that sound plausible but aren't in the data. Every number in the paper must trace back to a source file.

**Common LLM hallucination patterns to actively watch for:**
- **Fabricated numbers**: Specific values (accuracy, p-value, N) that don't appear in any source file. LLMs often generate plausible-sounding metrics. Cross-check every number.
- **P-value swaps**: The correct p-value for comparison A gets accidentally attached to comparison B. Always verify which comparison each p-value belongs to by matching against the source data line by line.
- **Drifting participant counts**: N changes between sections (e.g., Introduction says 50, Discussion says 45). LLMs sometimes "round up" or confuse sample sizes.
- **New findings in Conclusion**: The Conclusion should summarize existing results, never introduce new claims. If a Conclusion sentence makes a claim that doesn't appear in Results, it's likely fabricated.
- **Phantom citations**: `\cite{AuthorYear}` keys that have no bib entry — often LLM-generated citation keys for papers that don't exist.

#### Check 2: Before vs. After (防邏輯斷裂)

Read the sections in reading order (Intro → Related Work → Methods → Results → Discussion → Conclusion) and verify logical flow:
- Terms introduced in Methods are used consistently in Results
- Discussion interpretations reference specific Results findings
- No later section contradicts an earlier established fact
- The narrative builds — each section's claims rest on what came before

**`LOGIC_BREAK`** — a later section contradicts or ignores something established earlier. Include quotes from both locations.

#### Check 3: Claim vs. Evidence (防過度誇大)

For every interpretive claim in Discussion:
- Identify the supporting evidence (which Result, which figure/table)
- Assess evidence strength: strong (p<0.05, large effect), moderate (trend, small sample), weak (qualitative, indirect)
- Check that hedging matches evidence strength:
  - Strong evidence → "demonstrates", "shows", "establishes" are OK
  - Moderate evidence → "suggests", "indicates" are appropriate
  - Weak evidence → "may suggest", "one possible interpretation" are needed

**`OVERCLAIM`** — claim is stronger than evidence warrants
**`UNDERCLAIM`** — evidence is strong but language is unnecessarily hedged (this wastes the paper's impact)

### Phase 3c: Adversarial Questioning

Stress-test the draft from a skeptical reviewer's perspective.

#### 1. So What? Test

For each paragraph longer than ~100 words, ask: "如果刪掉這一段，讀者會錯過什麼重要資訊嗎？" If the answer is "not really" — the paragraph is redundant, off-topic, or repeats something already established elsewhere.

**`EXPENDABLE`** — flag with a suggestion to cut, merge with another paragraph, or explain why it's included. Be judicious: not every paragraph needs to be earth-shattering, but every paragraph should earn its place.

#### 2. Cross-Section Consistency Test

Systematically compare claims across sections. Use this checklist:

- **Introduction promises vs. Methods implementation** — did we actually do what we said we'd do?
- **Methods description vs. Results reported** — do the results match the methodology described?
- **Results numbers vs. Discussion interpretation** — does the discussion accurately interpret the results?
- **Contribution list alignment** — count the contributions listed in Introduction and compare with Conclusion. Do they match in number *and* content? This is a common mismatch: the Introduction lists 4 contributions, but the Conclusion restates only 3, or substitutes different items.
- **Participant/sample counts** — verify N is the same in Introduction, Methods, Results, Discussion, and Conclusion. Any discrepancy is a flag.
- **Claims in Conclusion that don't appear in Results** — the Conclusion must only summarize; any "new finding" is a red flag for fabrication.

**`CROSS_SECTION_INCONSISTENCY`** — include the specific quotes from both locations so the reviser can see the mismatch.

#### 3. Visual-Text Alignment

For every reference to a figure or table ("as shown in Fig. X", "Table Y demonstrates"):
- Look up the figure/table in `figure_captions.md` or `table_captions.md`
- Verify the text description matches: trend direction, relative magnitudes, significance markers
- E.g., text says "increasing" but caption says "plateau"; text says "significant" but table shows no asterisk

**`VISUAL_TEXT_MISMATCH`** — this is a common and embarrassing error that reviewers always catch.

#### 4. Citation Accuracy (only if full texts available)

If `step5_full_text/` contains markdown files for cited papers:
- For claims that attribute a specific finding to a cited paper ("Smith et al. showed that X"), spot-check against the full text
- Does the cited paper actually say what we claim it says?

**`MISATTRIBUTION`** — the cited paper doesn't support the attributed claim. This is a credibility-destroying error.

Skip this check if full texts aren't available — it's valuable but optional.

### Phase 3d: Compile Review Output

Collect all flags from Phases 3a–3c into `step3_review_r{N}.json`. Determine the review round number from `step0_session_config.json` (`review_round` field + 1).

**Deduplication**: The same issue may surface in multiple phases (e.g., hard checks flag a number mismatch, and the semantic review also catches it as an exaggeration). When this happens, keep **one flag** with the most specific and informative type. For example: if both NUMBER_MISMATCH and EXAGGERATION apply to the same p-value error, keep EXAGGERATION because it captures the semantic impact (significance claim is wrong), and note the number source in `evidence_expected`. The goal is one clear flag per unique issue — not three flags that all point at the same sentence from different angles. A reviser reading three flags for one problem wastes time figuring out they're the same thing.

Each flag needs these fields:

```json
{
  "id": "F001",
  "type": "HALLUCINATION",
  "severity": "critical | major | minor",
  "location": {
    "file": "04_results.tex",
    "section": "4.2",
    "paragraph": 2,
    "sentence": 1
  },
  "quote": "The exact text from the draft that has the issue",
  "evidence_expected": "What the source data actually says",
  "instruction": "Specific, actionable fix instruction for the reviser",
  "source_file": "The upstream file that contains the ground truth"
}
```

#### Severity Guidelines

- **Critical**: factual error that would be caught by any reviewer and damages credibility — `HALLUCINATION`, `NUMBER_MISMATCH` (wrong numbers), `MISATTRIBUTION`
- **Major**: structural or logical issue that weakens the paper — `LOGIC_BREAK`, `OVERCLAIM`, `CROSS_SECTION_INCONSISTENCY`, `VISUAL_TEXT_MISMATCH`, `ORPHAN_FIGURE`
- **Minor**: style or completeness issue — `EXPENDABLE`, `UNDERCLAIM`, `OVER_BUDGET`, `UNDER_BUDGET`, `MISSING_CITATION` (for non-critical claims)

Use judgment: a missing citation for a foundational claim is major, not minor. A 5% word count overrun is minor; 30% is major.

#### Final JSON Structure

```json
{
  "review_round": 1,
  "timestamp": "ISO 8601",
  "summary": {
    "total_flags": 12,
    "by_severity": {"critical": 2, "major": 5, "minor": 5},
    "by_type": {"HALLUCINATION": 1, "NUMBER_MISMATCH": 2, "...": "..."},
    "sections_clean": ["03_methods"],
    "sections_flagged": ["01_introduction", "04_results", "05_discussion"]
  },
  "flags": [
    { "...flag objects as above..." }
  ]
}
```

## Output

1. **`step3_review_r{N}.json`** — the structured review (this is the primary deliverable)
2. Update `step0_session_config.json`: increment `review_round`, set `current_step` to 3

After writing the review JSON, present a human-readable summary to the user:
- Total flags by severity
- Top 3 most critical issues with quotes
- Which sections are clean vs. need work
- Recommendation: "修訂" (proceed to revision) or specific concerns

This is **Checkpoint 2** — the user decides what to do next. They may accept suggestions, override with custom instructions, add flags you missed, or dismiss false positives. Wait for their input before proceeding.

## References

- `references/flag_types.md` — Complete list of flag types with examples and severity defaults
- `scripts/hard_checks.py` — Automated checking script (Phase 3a)
