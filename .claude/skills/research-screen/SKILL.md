---
name: research-screen
description: "Use this skill to turn a raw paper collection into a quality-filtered shortlist. Invoke when the user wants to screen papers, score them on relevance and methodological rigor, apply PICO-based inclusion/exclusion criteria, or decide which papers to keep from search results. Also use when the user has finished collecting papers and wants to evaluate, rank, or filter them — including requests like 'screen my papers', 'which papers should I keep', or 'filter by quality'. This is Step 3 of the Research Agent pipeline — run after research-search. Supports Chinese-language screening requests (篩選論文、評分論文、篩選文獻)."
---

# Research Screen — Step 3 of Research Agent Pipeline

You are screening a collection of academic papers gathered in Step 2. Your job is to read every paper's metadata and abstract, score it on three dimensions anchored to the PICO framework, apply a composite threshold, and produce two outputs: a detailed screening results document and a shortlist JSON that downstream steps consume.

This step is a quality gate. Downstream synthesis (SOTA review, gap analysis, hypothesis) inherits whatever you include here. Let through a weak paper and it dilutes the review; cut a relevant one and the review has a blind spot. The scoring needs to be principled and transparent — every score should have a reason the user can audit.

## Input

Read these files from the session folder:

1. **`step2_raw_papers.json`** — The paper collection from research-search: titles, authors, abstracts, citation counts, citation network data (in_degree, is_hub, cluster), and source provenance
2. **`step0_session_config.json`** — PICO framework, topic, timeframe, and session metadata

If either file is missing, tell the user to run the earlier pipeline steps first.

## Procedure

### 1. Define Screening Criteria from PICO

Before scoring, translate the PICO into concrete inclusion/exclusion criteria. This anchors the screening to the research question and prevents drift.

**Inclusion criteria** (derive from PICO):
- Population: Does the paper study the target population (or a closely related one)?
- Intervention: Does it address the intervention/technology of interest?
- Outcome: Does it measure relevant outcomes?
- Design: Is it an empirical study, systematic review, or meta-analysis?

**Exclusion criteria** (common patterns — adapt to the topic):
- Wrong population (e.g., animal studies when PICO specifies humans)
- Wrong intervention (e.g., pharmacological when PICO specifies behavioral)
- No original data (editorials, commentaries, opinion pieces without data)
- Inaccessible content (no abstract available AND title is ambiguous)

Present the criteria to the user before scoring. They should be specific enough that someone else could apply them consistently.

### 2. Score Each Paper (Three Axes, Each 1–5)

For every paper in `step2_raw_papers.json`, assign scores on three dimensions. Score based on the abstract and metadata — you don't have full text yet, and that's fine. Abstracts contain enough signal for screening-level decisions.

#### Axis 1: Relevance to PICO (weight: 0.50)

How directly does this paper address the research question?

| Score | Meaning |
|-------|---------|
| 5 | Directly addresses the exact PICO — same population, intervention, and outcome |
| 4 | Addresses most PICO components; minor mismatch in one dimension (e.g., slightly different population age range) |
| 3 | Partially relevant — shares the intervention or population but not both, or addresses a closely related question |
| 2 | Tangentially related — same broad field but different focus (e.g., a general BCI review when PICO is about neurofeedback for ADHD) |
| 1 | Minimal relevance — only shares keywords, different research question entirely |

#### Axis 2: Methodological Quality (weight: 0.30)

How rigorous is the study design? Judge from what the abstract reveals about methods.

| Score | Meaning |
|-------|---------|
| Score | Meaning |
|-------|---------|
| 5 | Gold standard for the field — adapt to domain: in biomedicine, this means large-N RCT or well-powered meta-analysis; in CS/engineering, it means rigorous evaluation on established benchmarks with strong baselines and ablation studies |
| 4 | Strong design: controlled study with adequate sample OR comprehensive benchmark evaluation across multiple datasets with clear methodology |
| 3 | Acceptable: pilot study, moderate sample, standard methods but some limitations; in CS: evaluation on a single benchmark or limited comparison baselines |
| 2 | Weak: case study, very small sample, unclear methods, no statistical analysis or inadequate evaluation |
| 1 | Minimal: anecdotal, no methods described, or abstract too vague to assess |

For **review papers**, score based on comprehensiveness and systematic rigor (systematic review > narrative review > opinion piece). For **CS/engineering**, don't look for clinical trial designs — look for reproducibility, benchmark coverage, statistical significance testing, and ablation studies.

#### Axis 3: Recency & Impact (weight: 0.20)

A combined measure of how current the work is and how much influence it has had.

| Score | Meaning |
|-------|---------|
| 5 | Recent (last 2-3 years) AND high impact (top-quartile citations for its age, or published in a leading journal) |
| 4 | Recent with moderate impact, OR older but seminal (very high citation count, foundational to the field) |
| 3 | Moderate recency and moderate impact — neither cutting-edge nor dated |
| 2 | Older work (5+ years) with low citation impact, or very recent but in a low-impact venue |
| 1 | Outdated findings or negligible impact |

**Important:** Don't penalize highly-cited older papers. A 2013 meta-analysis with 500+ citations is foundational — score it 4 or higher on this axis. The "recency" component is about whether the findings are still current, not just the publication year.

### 3. Compute Composite Score

For every paper, compute the composite score arithmetically — do not estimate or round intuitively. Use this exact formula and write out the arithmetic:

```
composite = (relevance × 0.50) + (quality × 0.30) + (recency_impact × 0.20)
```

For example, if a paper scores Rel=5, Qual=4, Rec=3:
- 5 × 0.50 = 2.50
- 4 × 0.30 = 1.20
- 3 × 0.20 = 0.60
- composite = 2.50 + 1.20 + 0.60 = **4.30**

LLMs are prone to arithmetic drift when scoring many papers in sequence. To prevent this, compute each paper's composite independently from the formula — don't interpolate from nearby scores or adjust based on "feel." If two papers have identical axis scores, they must have identical composites.

The user can adjust weights if they specify different priorities (e.g., "I care more about methodology than recency"). Use the default weights unless told otherwise.

### 4. Apply Threshold and Classify

Classify every paper into one of three categories:

| Category | Composite Score | Action |
|----------|----------------|--------|
| **Included** | >= 3.50 | Goes to shortlist |
| **Borderline** | 3.00 – 3.49 | Flagged for human review (Checkpoint 2) |
| **Excluded** | < 3.00 | Out, with exclusion reason |

Classify strictly by the computed composite — a paper scoring 2.90 is excluded, not borderline; a paper scoring 3.50 is included, not borderline. If your composite computation and your classification disagree, recheck the arithmetic.

For each **excluded** paper, write a one-line exclusion reason. Be specific:
- "Population mismatch: studies rats, not humans"
- "No original data: narrative commentary"
- "Methodology not applicable: hardware-only sensor paper"

Vague reasons like "not relevant" aren't helpful — the user needs to understand why at a glance.

### 5. Citation Network Bonus Notes

Hub papers (high in_degree from the citation network in Step 2) deserve special attention because they are structurally important to the field, even if their PICO alignment isn't perfect.

For any paper where `citation_network.is_hub == true`:
- Add a note in the screening results: "Hub paper: cited by {in_degree} papers in this collection"
- If a hub paper lands in the **borderline** zone, explicitly flag it: "Hub paper in borderline range — recommend human review for potential inclusion"
- If a hub paper is **excluded**, note why despite its structural importance

This doesn't override the score — it provides context for the human reviewer at Checkpoint 2.

### 6. Organize into Tiers

Group included papers into thematic tiers based on score ranges and content. Tiers help the user quickly understand the collection's structure. Derive tier names from what the papers are actually about — don't use generic labels.

Example tiers (adapt to the actual content):
- **Tier 1: Core Papers** (composite >= 4.5) — Direct hits on the PICO
- **Tier 2: Strong Supporting** (composite 4.0–4.4) — Closely related with strong methods
- **Tier 3: Contextual** (composite 3.5–3.9) — Broader context, adjacent methods, or review papers

The number and naming of tiers should reflect the actual distribution. Three tiers is typical; use more if the collection is large and diverse.

## Output

### `step3_screening_results.md`

A bilingual document with the complete screening record. This is the primary artifact for Checkpoint 2 — it needs to be thorough enough for the user to audit decisions.

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 3
threshold: 3.5
weights: "relevance=0.50, quality=0.30, recency_impact=0.20"
---

# Screening Results / 篩選結果

> Topic / 研究主題: {topic}
> Papers screened / 篩選論文數: {total}
> Date / 篩選日期: {date}
> Threshold / 門檻: composite >= {threshold}

## Screening Criteria / 篩選標準

### Inclusion / 納入條件
- {criterion_1_en} / {criterion_1_zh}
- {criterion_2_en} / {criterion_2_zh}
- ...

### Exclusion / 排除條件
- {criterion_1_en} / {criterion_1_zh}
- ...

## Summary / 摘要

| Category / 分類 | Count / 數量 | Percentage / 百分比 |
|-----------------|-------------|-------------------|
| **Included / 納入** | **{n}** | **{pct}%** |
| Borderline / 邊緣 | {n} | {pct}% |
| Excluded / 排除 | {n} | {pct}% |

## Tier 1: {tier_name_en} / {tier_name_zh} (Score >= 4.5)

| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| {id} | {title} | {first_author} et al. | {year} | {score} | {score} | {score} | **{composite}** | {one_line_rationale} |

## Tier 2: {tier_name_en} / {tier_name_zh} (Score 4.0–4.4)

| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| ... |

## Tier 3: {tier_name_en} / {tier_name_zh} (Score 3.5–3.9)

| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| ... |

---

## Borderline Papers / 邊緣論文 (Score 3.0–3.4)

> **⛳ Checkpoint 2: 邊緣打撈**
> Review the papers below. These scored close to the threshold and may contain relevant work that the scoring missed — especially cross-disciplinary papers using non-standard terminology.
> 請審核以下邊緣論文。這些論文分數接近門檻，可能包含評分遺漏的相關研究——特別是使用非標準術語的跨領域論文。
>
> Mark any paper you want to include with `include` and I'll add it to the shortlist.

| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale | Hub? |
|----|-------|---------|------|-----|------|-----|---------------|-----------|------|
| {id} | {title} | {first_author} et al. | {year} | {score} | {score} | {score} | **{composite}** | {rationale} | {Yes/—} |

---

## Excluded Papers / 排除論文 (Score < 3.0)

| ID | Title | Year | Rel | Qual | Rec | **Composite** | Exclusion Reason / 排除原因 |
|----|-------|------|-----|------|-----|---------------|---------------------------|
| {id} | {title} | {year} | {score} | {score} | {score} | **{composite}** | {specific_reason} |

---

## Hub Paper Summary / 核心引用論文摘要

| ID | Title | In-Degree | Cluster | Status | Note |
|----|-------|-----------|---------|--------|------|
| {id} | {title} | {in_degree} | {cluster} | Included/Borderline/Excluded | {note} |

---

Files / 檔案: `step3_screening_results.md`, `step3_shortlist.json`
Next step / 下一步: `/research-export`
```

### `step3_shortlist.json`

The machine-readable shortlist that downstream steps consume. Contains **only included papers** (composite >= 3.5), preserving all original metadata from `step2_raw_papers.json` plus the screening scores.

```json
{
  "session_id": "{session_id}",
  "topic": "{topic}",
  "screening_timestamp": "{ISO 8601}",
  "screening_config": {
    "threshold": 3.5,
    "weights": {
      "relevance": 0.50,
      "quality": 0.30,
      "recency_impact": 0.20
    }
  },
  "summary": {
    "total_screened": 51,
    "included": 28,
    "borderline": 8,
    "excluded": 15,
    "inclusion_rate": "55%"
  },
  "papers": [
    {
      "...all original fields from step2_raw_papers.json...",
      "screening": {
        "relevance": 5.0,
        "quality": 4.5,
        "recency_impact": 4.0,
        "composite": 4.55,
        "tier": 1,
        "rationale": "One-line rationale for this paper's inclusion"
      }
    }
  ]
}
```

**Field notes:**
- Preserve every field from the original paper record — downstream steps need `doi`, `semantic_scholar_id`, `citation_network`, etc.
- Add the `screening` sub-object with scores, composite, tier, and rationale
- Sort papers by composite score descending (highest first)
- If the user manually includes borderline papers at Checkpoint 2, add them with their original scores and a `"manually_included": true` flag

### After Saving

Update `step0_session_config.json`: set `"current_step": 3`.

Then present to the user:

1. **Summary table** — included / borderline / excluded counts
2. **Top scoring papers** — the 3-5 highest-scoring papers with title and composite
3. **Borderline papers for review** — list with scores and rationale (this is the Checkpoint 2 prompt)
4. **Hub paper status** — which hubs were included vs. borderline vs. excluded
5. **Suggest next step:** `research-export` (but only after Checkpoint 2 is resolved)

## Checkpoint 2: 邊緣打撈

After presenting results, explicitly prompt the user to review borderline papers. This is where the human catches what the algorithm missed. Cross-disciplinary papers are especially vulnerable to false negatives — they may use different terminology than the PICO expects.

Tell the user something like:

> I've flagged {n} borderline papers (score 3.0–3.4). Please review the list above — if any look relevant, tell me which to include (by ID or title) and I'll add them to the shortlist.
>
> 我標記了 {n} 篇邊緣論文（分數 3.0–3.4）。請審核上方清單——如果有任何看起來相關的，告訴我要納入哪些（用 ID 或標題），我會加入精選清單。

Wait for the user's response before suggesting the next step. If the user includes additional papers, update `step3_shortlist.json` accordingly.

## Edge Cases

- **Papers without abstracts**: Score conservatively. If the title clearly aligns with the PICO, give relevance a 3 and quality a 2 (insufficient info). Add a note: "No abstract — scored on title only, lower confidence." These often land in the borderline zone, which is appropriate — let the human decide.
- **Review vs. empirical papers**: Reviews aren't methodologically "weak" — they're a different study type. Score their methodology based on systematic rigor (PRISMA adherence, search comprehensiveness, risk-of-bias assessment), not on experimental design criteria.
- **Very large collections (>80 papers)**: The screening still applies to every paper. Consider adding more tiers to keep the tables readable (4-5 tiers instead of 3).
- **Very small collections (<20 papers)**: Consider lowering the threshold to 3.0 to preserve enough papers for meaningful synthesis. Flag this to the user: "Small collection — I've used a lower threshold (3.0) to preserve enough papers. You can adjust."
- **Non-English papers**: Score based on the English abstract/title if available. If only a non-English title exists, note the language and let the user decide at Checkpoint 2.
- **Preprints**: Don't penalize for lack of peer review — many important recent papers are preprints. Score based on content quality as evident from the abstract.

## Verification Checklist

Before saving the output files, verify these invariants:

1. **Paper count**: Count the distinct paper IDs across included + borderline + excluded sections. The total must equal the number of papers in `step2_raw_papers.json`. If it doesn't, find the missing papers and add them.
2. **No duplicates**: No paper ID should appear in more than one category (included, borderline, excluded). If a paper's status changed during calibration, remove it from its old location.
3. **Composite arithmetic**: Spot-check at least 5 papers by recomputing `relevance × 0.50 + quality × 0.30 + recency_impact × 0.20`. If any are wrong, recompute all composites.
4. **Classification consistency**: Every included paper has composite >= 3.50, every borderline paper has 3.00 <= composite < 3.50, every excluded paper has composite < 3.00.
5. **Shortlist JSON matches markdown**: The papers in `step3_shortlist.json` should be exactly those classified as "included" in the markdown.

## Scoring Calibration

To keep scores consistent across the collection, do a calibration pass before finalizing:

1. Score all papers in a first pass
2. Review the distribution: if everything clusters at 3.5-4.0 or if the range is too compressed, revisit your anchoring — your "5" and "1" should represent genuine extremes in this collection
3. Check that hub papers have scores that reflect their structural importance alongside content relevance
4. Verify that the tier boundaries produce meaningful groupings — if Tier 1 has 20 papers, the bar is too low

## Bilingual Communication

Follow the same conventions as research-init and research-search:
- Table headers: bilingual (e.g., "Title / 標題", "Composite / 綜合分")
- Tier names: English + Chinese (e.g., "Core RCTs / 核心隨機對照試驗")
- Checkpoint instructions: full bilingual
- Exclusion reasons: English only is fine (these are brief technical notes)
- Keep technical terms in English with Chinese explanation on first mention: e.g., "composite score（綜合加權分數）"
