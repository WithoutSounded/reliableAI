---
name: research-gaps
description: "Use this skill when the user wants to find what's missing or unexplored in their reviewed literature. This is specifically for gap analysis — identifying blind spots, unaddressed questions, and research opportunities from a set of already-reviewed papers or a completed SOTA review. Invoke whenever someone says 'gap analysis', 'find gaps', 'what's missing', 'what hasn't been studied', 'blind spots', 'research opportunities', '研究缺口', '研究空白', '找缺口', '還缺什麼', '沒被研究過', or references a Research/ session folder wanting to know what remains unexplored. Also trigger on 'next step' after research-sota (Step 6). Do NOT use for paper searching, full-text fetching, reading individual papers, knowledge graph building, or hypothesis generation from an already-selected gap."
---

# Research Gaps — Step 7 of Research Agent Pipeline

You are analyzing a completed state-of-the-art review to identify what the field has NOT yet addressed. This is the transition point from "what do we know?" to "what should we do next?" — everything downstream (hypothesis, manuscript) depends on the gaps you surface here.

The difference between a useful gap analysis and a generic "more research is needed" is evidence. Every gap you identify must be grounded in specific papers from the SOTA review — you're not speculating about what might be missing, you're demonstrating what IS missing by pointing to the edges of existing work. A gap exists in the space between papers: where one study's limitations meet another study's assumptions, where a method proven in one domain hasn't been tried in another, where multiple papers call for the same future work that nobody has done yet.

You produce one output: a bilingual gap analysis document with evidence-linked gap descriptions, 3-axis priority scoring, and a ranking that feeds directly into Checkpoint 3 — where the user decides which gap to pursue.

## Input

Read these files from the session folder:

1. **`step6_sota_review.md`** — The thematic SOTA review. This is your primary source: themes, consensus, debates, cross-theme patterns, and the paper-theme mapping table.
2. **`step6_knowledge_graph.canvas`** — The Obsidian Canvas knowledge graph. Use this to identify structural patterns: isolated nodes (papers with few connections), sparse regions between theme clusters, and methodology gaps visible in the color distribution.
3. **`step0_session_config.json`** — PICO framework and session metadata. The PICO anchors your gap analysis — gaps should be relevant to the original research question, not just interesting absences in the literature.

If `step6_sota_review.md` is missing, tell the user to run `/research-sota` first. If `step0_session_config.json` is missing, you can still proceed but warn that gap analysis won't be anchored to a specific PICO — the results will be more generic.

### Topic Consistency Check

After reading both `step0_session_config.json` and `step6_sota_review.md`, verify that the `topic` field in the session config matches the topic in the SOTA review's frontmatter. If they differ (e.g., the SOTA review covers a different topic than what the session config says), warn the user before proceeding — this may indicate a file mismatch or corrupted session state. Use the topic from the SOTA review for your gap analysis since that's the content you're actually analyzing, but flag the inconsistency.

### Handling Abstract-Only Sessions

Check the SOTA review's YAML frontmatter for `abstract_only: true` or `full_text_papers: 0`. Only if one of these conditions is met, add the abstract-only caveat. The presence of some abstract-only papers alongside full-text papers does NOT trigger the caveat — what matters is whether any full texts were available at all. When the caveat is needed, place it immediately after the YAML frontmatter, before the main title:

```
---
(frontmatter)
---

> [!warning] Abstract-Based Gap Analysis / 僅摘要缺口分析
> ...

# Gap Analysis / 研究缺口分析
```

### Reading the SOTA Review

Read the entire SOTA review carefully. For gap identification, pay special attention to:

- **Debates sections**: Unresolved disagreements often point to gaps — if two camps disagree, there may be a study design or population that would resolve the dispute
- **Dominant Methods sections**: Methodological monoculture is itself a gap — if every paper uses the same approach, alternative methods are underexplored
- **Cross-Theme Analysis**: Theme interactions and diverging findings reveal integration gaps — where two strands of work haven't been combined yet
- **Key Results tables**: Look for missing cells, missing populations, missing outcome measures across studies
- **"Future work" mentions**: If multiple papers independently call for the same thing, that's strong evidence of a recognized but unaddressed gap

Also read the knowledge graph to spot structural signals:
- **Color distribution**: If one methodology color dominates (e.g., all orange/computational, no red/experimental), that's a methodological gap
- **Isolated nodes**: Papers with few edges may represent underexplored directions
- **Missing cross-theme edges**: If two theme clusters have no connections, the integration between those areas is a potential gap

## Procedure

### 1. Systematic Gap Detection

Analyze the SOTA review against five gap type categories. These categories aren't arbitrary — they correspond to the dimensions along which a research field can have blind spots. Not every category will produce a gap for every topic; focus on the ones where the evidence is strongest.

#### Gap Type Taxonomy

| Type | What to look for | Signal in the SOTA review |
|------|-----------------|--------------------------|
| **Methodological** | Methods not yet applied to this domain; over-reliance on one study design; missing validation approaches | Dominant Methods sections show monoculture; knowledge graph has one dominant color; no RCTs, or no computational studies, etc. |
| **Population** | Understudied demographics, conditions, or subgroups; findings that may not generalize | Key Results tables show same population across studies; PICO population is narrow but studies are narrower still |
| **Measurement** | Missing metrics, outcome measures, or evaluation approaches; proxy measures used instead of direct ones | Key Results use different metrics making comparison impossible; outcomes in PICO not actually measured by any paper |
| **Temporal** | No longitudinal data; short follow-up periods; unknown long-term effects | All studies are cross-sectional or short-duration; "future work" sections mention follow-up needs |
| **Integration** | Fields or modalities not yet combined; promising approaches from one theme not applied in another | Cross-Theme Analysis shows no interaction between themes; knowledge graph has disconnected clusters |

Work through each category systematically, but don't force gaps where the evidence doesn't support them. A real gap has multiple papers pointing at it from different angles — a single paper's limitation is not a field-level gap.

### 2. Document 2–3 Critical Gaps

From your systematic analysis, select 2–3 gaps that are most significant. Quality over quantity — three well-evidenced gaps are more useful than six vague ones. Each gap needs to be documented with enough detail and evidence that the user can make an informed decision at Checkpoint 3.

For each gap, document:

#### a) Description (Bilingual)

A clear, specific statement of what is missing. This should be concrete enough to suggest a study — "lack of longitudinal data" is too vague; "no study has tracked neurofeedback effects beyond 3 months in elderly populations" is actionable.

Write the description in English first, then provide the Traditional Chinese translation.

#### b) Gap Type Classification

Assign the primary gap type from the taxonomy above. Some gaps span multiple types (e.g., a methodological gap that also involves a new population) — note the primary type and any secondary types.

#### c) Supporting Evidence — Papers That Reveal the Gap

This is the most important part. Cite specific papers from the SOTA review that demonstrate the gap exists. Evidence comes in several forms:

- **Limitation statements**: Papers that explicitly acknowledge this gap in their discussion/limitations sections
- **Implicit boundaries**: Papers whose methods or populations stop short of the gap area (e.g., every study uses adults 18-40, revealing a gap for elderly populations)
- **Contradictions**: Papers with conflicting results that a new study design could resolve
- **"Future work" calls**: Multiple papers independently requesting the same type of study
- **Methodology absence**: The knowledge graph's color distribution showing a missing methodology type

For each piece of evidence, cite the paper by its citation key and explain how it reveals the gap. Don't just list papers — explain the connection.

#### d) Counter-Evidence — Partial Coverage

Intellectual honesty requires noting any papers that partially address the gap. A gap with zero counter-evidence is either very novel (good) or you may have missed something (check again). A gap with strong counter-evidence may not be as open as it appears.

For each counter-evidence paper, explain:
- What aspect of the gap it addresses
- Why it doesn't fully close the gap (e.g., small sample, different population, preliminary results)

#### e) Why This Gap Matters

Explain the significance in the context of the PICO and the field:
- What questions can't be answered because of this gap?
- What practical or clinical implications does it have?
- How does it limit the field's progress?

This section helps the user at Checkpoint 3 assess which gap is worth investing months of research effort into.

### 3. Prioritize Gaps (Three Axes, Each 1–5)

Score each gap on three dimensions. These scores feed directly into the user's decision at Checkpoint 3 — they need to be well-calibrated and honestly assessed, not inflated to make every gap look critical.

#### Axis 1: Severity — How much does this gap limit the field?

| Score | Meaning |
|-------|---------|
| 5 | Fundamental blocker: the field cannot advance meaningfully without addressing this. Multiple papers identify it as a critical limitation. |
| 4 | Significant limitation: important questions remain unanswered, affecting the reliability or applicability of existing findings. |
| 3 | Moderate limitation: the field functions but this gap creates uncertainty in a specific area. |
| 2 | Minor limitation: affects a narrow aspect of the field, most work can proceed without it. |
| 1 | Negligible: interesting but not limiting the field's progress. |

#### Axis 2: Novelty — How unexplored is this direction?

| Score | Meaning |
|-------|---------|
| 5 | Completely uncharted: no paper in the collection (or known to you) has attempted this. |
| 4 | Barely explored: 1-2 papers touch on it tangentially or in preliminary form. |
| 3 | Partially explored: some work exists but significant aspects remain unaddressed. |
| 2 | Moderately explored: several papers have addressed parts of this, but with limitations. |
| 1 | Well-covered: multiple papers have substantially addressed this — may not be a real gap. |

A score of 1 on novelty should make you reconsider whether this is actually a gap. If the direction is well-explored, the "gap" may be a misreading of the literature.

#### Axis 3: Feasibility — Can this realistically be addressed?

| Score | Meaning |
|-------|---------|
| 5 | Highly feasible: standard methods, available data/populations, reasonable timeline and budget. |
| 4 | Feasible with effort: requires some specialized resources but achievable for a well-equipped lab. |
| 3 | Moderately feasible: requires significant resources, specialized equipment, or hard-to-recruit populations. |
| 2 | Challenging: requires rare resources, very large samples, multi-site coordination, or novel technology. |
| 1 | Currently impractical: requires technology that doesn't exist, populations that can't be recruited, or unrealistic timescales. |

Feasibility scoring is inherently uncertain since you don't know the user's specific lab resources. Score based on general academic feasibility — the user will adjust at Checkpoint 3 based on their actual capabilities. When in doubt, score conservatively (lower) and note your assumptions.

### 4. Compute Composite Priority and Rank

Calculate a composite priority score for each gap:

```
composite = (severity × 0.40) + (novelty × 0.30) + (feasibility × 0.30)
```

The weighting reflects that severity matters most (a gap that doesn't limit the field isn't worth pursuing regardless of novelty), while novelty and feasibility share equal importance (a novel but infeasible gap is as impractical as a feasible but well-explored one).

Write out the arithmetic explicitly for each gap, the same way research-screen does for paper scoring. Always use the `×` symbol (not `x`) for multiplication to maintain visual consistency:

```
5 × 0.40 + 4 × 0.30 + 3 × 0.30 = 2.00 + 1.20 + 0.90 = **4.10**
```

Rank gaps by composite score, highest first. If two gaps score identically, rank the one with higher severity first — a more impactful gap is a better research investment.

## Output

### `step7_gap_analysis.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 7
gaps_identified: {N}
priority_weights: "severity=0.40, novelty=0.30, feasibility=0.30"
---

# Gap Analysis / 研究缺口分析

> Topic / 研究主題: {topic}
> Papers analyzed / 分析論文數: {N} (from SOTA review)
> Gaps identified / 已識別缺口: {N}
> Date / 日期: {date}

## Executive Summary / 總覽摘要

{2-3 paragraph overview of the gap landscape — what the field has covered well and where the significant blind spots are. Frame this as a transition from Step 6's synthesis to actionable research opportunities.}

{繁體中文翻譯}

---

## GAP_001: {Gap Title EN} / {缺口標題中文}

**Type / 類型:** {Primary type} ({secondary type if any})
**Priority Rank / 優先排名:** #{rank}

### Description / 描述

{Detailed description of the gap — specific enough to suggest a study design.}

{繁體中文翻譯}

### Supporting Evidence / 支持證據

{For each piece of evidence:}

- **{CitationKey} ({Year})**: {How this paper reveals the gap — quote specific limitations, note methodology boundaries, cite "future work" calls}

  {繁體中文說明}

- **{CitationKey} ({Year})**: {Next piece of evidence}

  {繁體中文說明}

- ...

### Counter-Evidence / 反面證據

{Papers that partially address this gap, with explanation of why the gap remains open:}

- **{CitationKey} ({Year})**: {What aspect it addresses} → {Why it doesn't fully close the gap}

  {繁體中文說明}

{If no counter-evidence exists:}

> No papers in the collection address this gap, even partially. This suggests a highly novel direction but also warrants caution — the absence may indicate practical barriers not captured in the literature.
>
> 文獻中無論文涉及此缺口。這暗示了一個高度新穎的方向，但也需謹慎——此空白可能反映文獻未記錄的實際障礙。

### Why It Matters / 重要性

{Significance in context of PICO and field progress}

{繁體中文翻譯}

### Priority Score / 優先分數

| Axis / 評估軸 | Score / 分數 | Rationale / 理由 |
|--------------|-------------|-----------------|
| Severity / 嚴重性 | {1-5} | {One-line rationale EN} / {中文理由} |
| Novelty / 新穎性 | {1-5} | {One-line rationale EN} / {中文理由} |
| Feasibility / 可行性 | {1-5} | {One-line rationale EN} / {中文理由} |

**Composite / 綜合分:** {severity} × 0.40 + {novelty} × 0.30 + {feasibility} × 0.30 = **{composite}**

---

## GAP_002: ...

{Same structure as GAP_001}

---

## GAP_003: ...

{Same structure, if 3 gaps identified}

---

## Priority Ranking / 優先排名

| Rank / 排名 | Gap ID | Title / 標題 | Type / 類型 | Severity / 嚴重性 | Novelty / 新穎性 | Feasibility / 可行性 | **Composite / 綜合分** |
|------------|--------|-------------|-----------|-----------------|----------------|--------------------|-----------------------|
| 1 | GAP_{N} | {Title} / {中文} | {Type} | {score} | {score} | {score} | **{composite}** |
| 2 | GAP_{N} | {Title} / {中文} | {Type} | {score} | {score} | {score} | **{composite}** |
| 3 | GAP_{N} | {Title} / {中文} | {Type} | {score} | {score} | {score} | **{composite}** |

---

## Gap Landscape Summary / 缺口全景

### Coverage Strength / 覆蓋強項

{What the field does well — areas thoroughly covered by existing literature. This provides context: the gaps exist against a backdrop of strengths.}

{繁體中文翻譯}

### Methodology Distribution / 方法學分布

{Summary of methodology colors from the knowledge graph. Which methodology types are overrepresented? Which are missing? This directly supports methodological gap identification.}

{繁體中文翻譯}

### Cross-Gap Patterns / 跨缺口模式

{Do the gaps share underlying causes? For example, if both GAP_001 and GAP_002 stem from the field's reliance on convenience samples, that's a systemic pattern worth noting.}

{繁體中文翻譯}

---

> **Checkpoint 3: 戰場選擇與價值裁定**
>
> Review the gaps above. Select which gap to pursue based on your lab's capabilities, budget, ethics timeline, and equipment access.
>
> 請審核上述缺口。根據您實驗室的能力、預算、倫理審查時程與設備，選擇要鎖定的缺口。
>
> To proceed, specify: "Lock GAP_{N}, drop GAP_{N}" — then I'll generate a hypothesis from the selected gap.
>
> 請指示：「鎖定 GAP_{N}，放棄 GAP_{N}」——然後我將根據選定缺口生成假說。

---

Files / 檔案: `step7_gap_analysis.md`
Next step / 下一步: `/research-hypothesis`
```

## After Saving

Update `step0_session_config.json`: set `"current_step": 7`.

Then present to the user:

1. **Executive summary** — the gap landscape overview (bilingual)
2. **Gap list** — numbered gaps with type, title, and composite score
3. **Top priority gap** — highlight the highest-ranked gap with its evidence summary
4. **Priority ranking table** — all gaps compared side by side
5. **Checkpoint 3 prompt** — explicitly ask the user to select which gap to lock

## Edge Cases

- **SOTA review based on abstracts only**: See the "Handling Abstract-Only Sessions" section under Input for the exact trigger logic (`abstract_only: true` or `full_text_papers: 0` in the SOTA review frontmatter) and caveat placement. Do NOT add the abstract-only caveat if the SOTA review has some full-text papers — the threshold is zero full texts, not "mostly abstracts." Gap analysis from abstracts alone can still identify structural and topical gaps, but methodological gaps visible only in full-text methods sections may be under-detected. Note this in the caveat and consider scoring Feasibility more conservatively since you have less methodological detail to assess.

- **Small paper collections (<10 papers)**: With few papers, "gaps" may simply reflect insufficient search coverage rather than genuine blind spots in the field. Warn the user: identify gaps as preliminary and recommend broadening the search before committing to a research direction. Reduce to 1-2 gaps rather than 3.

- **Very mature fields**: Some fields have been heavily studied and obvious gaps are already closed. In this case, your gaps may be more nuanced — integration gaps, replication needs, or methodology transfers from adjacent fields. These are still valuable but score lower on novelty; be honest about that rather than inflating scores.

- **Highly interdisciplinary collections**: Gaps at the intersection of fields are often the most valuable but hardest to detect — they appear as missing connections between theme clusters rather than absent topics within a theme. Pay extra attention to the knowledge graph's cross-theme structure.

- **No knowledge graph available**: If `step6_knowledge_graph.canvas` is missing, you lose the structural/visual analysis but can still identify gaps from the text of the SOTA review. Note this limitation and proceed.

- **User has domain expertise**: If the user provides additional context about their field (e.g., "everyone knows about X but nobody has tried Y"), incorporate their insight. Domain expertise can reveal gaps that pure literature analysis misses — the user may know about practical barriers, unpublished work, or field conventions not captured in papers.

## Verification Checklist

Before saving, verify:

1. **Evidence grounding**: Every gap cites at least 2 papers from the SOTA review as supporting evidence. If you can't cite specific papers, the gap may be speculative — reconsider.
2. **Citation key consistency**: All citation keys match those in the SOTA review's Paper-Theme Mapping table.
3. **Score arithmetic**: Recompute each gap's composite: `severity × 0.40 + novelty × 0.30 + feasibility × 0.30`. Verify the ranking matches the computed composites.
4. **PICO relevance**: Each gap is relevant to the original PICO framework in `step0_session_config.json`. Interesting gaps that fall outside the PICO scope should be noted as "adjacent opportunities" but not ranked as primary gaps.
5. **No hallucinated gaps**: Every gap description is supported by evidence from the papers you actually read. Don't invent gaps based on general knowledge about the field — if it's not visible in the reviewed literature, it doesn't belong here.
6. **Bilingual completeness**: Every substantive section (descriptions, evidence explanations, significance, rationale) has both English and Traditional Chinese content.
7. **Counter-evidence honesty**: If a gap has strong counter-evidence, don't suppress it. An honest assessment serves the user better at Checkpoint 3 than an inflated gap claim.

## Bilingual Communication

Follow the same conventions as previous pipeline steps:
- Section headings: bilingual (e.g., "Supporting Evidence / 支持證據")
- Table headers: bilingual
- Gap titles: bilingual
- Description and significance paragraphs: English paragraph then Chinese translation
- Evidence citations: keep citation keys, author names, and quantitative data in English in both language versions
- Technical terms in English with Chinese explanation on first mention: e.g., "research gap（研究缺口）", "feasibility（可行性）", "severity（嚴重性）"

## Bilingual Translation Safety

Gap analysis involves nuanced claims about what is and isn't known. The Chinese translation must preserve epistemic precision:

- "has not been studied" → 「尚未被研究」, not 「無法研究」(the latter implies impossibility)
- "limited evidence" → 「證據有限」, not 「沒有證據」(limited ≠ absent)
- "suggests a gap" → 「顯示存在缺口」, not 「證明存在缺口」(suggestion ≠ proof)
- "may be feasible" → 「可能可行」, not 「可行」(preserve hedging)
- "no study has examined" → 「尚無研究探討」, not 「不能研究」

When describing gaps, use language that invites investigation rather than declaring failure. The field hasn't failed — it simply hasn't gotten to everything yet.
