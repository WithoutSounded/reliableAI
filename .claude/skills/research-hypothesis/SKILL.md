---
name: research-hypothesis
description: "Generate testable research hypotheses with IN/OUT scope boundaries and journal recommendations from a user-selected gap. Step 8 of the Research Agent pipeline — the bridge between gap analysis (Step 7) and manuscript writing (Step 9). Invoke when the user says 'generate hypothesis', 'research hypothesis', 'formulate hypothesis', 'define scope', 'IN/OUT scope', 'target journals', 'journal recommendations', '生成假說', '研究假說', '假設生成', '範圍界定', '目標期刊', or says 'next step' after research-gaps (Step 7). Also trigger when the user has locked a gap (e.g., 'Lock GAP_001') and wants to move forward, or asks 'what should I study?' after completing gap analysis. Do NOT use for gap identification (use research-gaps), paper searching (use research-search), or manuscript writing (use research-write)."
---

# Research Hypothesis — Step 8 of Research Agent Pipeline

You are converting a user-selected research gap into a concrete, testable research plan. This is the pivot point of the entire pipeline: everything before this step was analytical (understanding what exists and what's missing); everything after is generative (writing the actual research). The quality of this step determines whether the downstream manuscript has a coherent, defensible foundation — or a vague, unfocused one.

The difference between a useful hypothesis specification and a generic one is precision. "We hypothesize that X improves Y" is not useful. "We hypothesize that X applied to population P under condition C will improve outcome Y by at least Z%, measured via metric M, compared to baseline B" — that's a specification someone can actually design a study around. Your job is to get as close to the second form as the available evidence supports.

You produce two outputs: a bilingual hypothesis specification with research questions, formal hypotheses, and IN/OUT scope boundaries; and a journal recommendations document with target venues matched to the research profile.

## Input

Read these files from the session folder:

1. **`step7_gap_analysis.md`** — The gap analysis with the user's selected gap. The user should have already been through Checkpoint 3 and locked a specific gap (e.g., "Lock GAP_001, drop GAP_002"). If no gap is explicitly locked, ask the user which gap to target before proceeding.
2. **`step6_sota_review.md`** — The thematic SOTA review. This provides the theoretical foundation for framing research questions and the evidence base for expected effect sizes, methodological choices, and population characteristics.
3. **`step0_session_config.json`** — PICO framework and session metadata. The PICO anchors scope boundaries — your IN/OUT scope should be a refinement of the original PICO, not a departure from it.

If `step7_gap_analysis.md` is missing, tell the user to run `/research-gaps` first. If the gap analysis exists but no gap has been locked by the user, present the priority ranking from the gap analysis and ask them to select one before proceeding.

### Topic Consistency Check

After reading both `step0_session_config.json` and `step7_gap_analysis.md`, verify that the `topic` field in the session config matches the topic in the gap analysis frontmatter. If they differ, warn the user before proceeding — this may indicate a file mismatch or corrupted session state. Use the topic from the gap analysis since that's the content you're actually building on, but flag the inconsistency.

### Identifying the Selected Gap

The user's gap selection may come in several forms:

- Explicit: "Lock GAP_001" or "I want to pursue GAP_002"
- Implicit: "Let's go with the methodological gap" or "the one about elderly populations"
- Absent: No selection made yet

If the selection is implicit, match it to the specific GAP_ID from the gap analysis and confirm with the user: "That sounds like GAP_002 (title). Proceeding with that — correct?"

If no selection has been made, do not guess. Present the gap ranking table and ask.

#### Cross-Check: User Description vs. Actual Gap Content

Sometimes the user describes the gap in their own words rather than using the exact title from the gap analysis. Before proceeding, verify that the user's description actually matches the content of the GAP_ID they referenced. For example, if the user says "Lock GAP_001, the one about long-term effects" but GAP_001 is actually about "methodological gaps in measurement," there's a mismatch. In this case, present the actual GAP_001 title and description and ask the user to confirm which gap they truly intend. This prevents silently proceeding with the wrong gap.

#### Acknowledging Dropped Gaps

If the user explicitly drops other gaps (e.g., "Lock GAP_001, drop GAP_002 and GAP_003"), acknowledge the dropped gaps in the output:
- Add a `dropped_gaps` field in the YAML frontmatter listing the dropped GAP IDs
- Include a brief "Gap Selection Rationale" section after the Selected Gap Summary, explaining why the locked gap was chosen over the dropped ones — use the composite scores and a 1-2 sentence justification per dropped gap. This helps reviewers understand the selection logic.

### Reading the SOTA for Hypothesis Grounding

Once you know which gap to target, re-read the relevant sections of the SOTA review with hypothesis-focused lenses:

- **Methods used by related papers**: These inform your choice of study design. If every paper in the theme uses method A, you can either (a) apply method A to the gap's new context, or (b) propose a novel method B — both are valid, but the justification differs.
- **Quantitative results**: Effect sizes, accuracy metrics, and statistical patterns from related studies provide the basis for expected magnitude in your hypothesis. Don't invent numbers — derive expectations from existing evidence.
- **Population and setting details**: The papers' populations define what has been studied; the gap defines what hasn't. Your hypothesis population should be precisely the unstudied group identified in the gap.
- **Debates and contradictions**: Unresolved debates can become research questions. If two camps disagree about X, a well-designed study that controls for the confound can resolve the debate.

## Procedure

### 1. Extract the Selected Gap's Core Elements

From the locked gap in `step7_gap_analysis.md`, extract:

- **Gap type** (methodological, population, measurement, temporal, integration)
- **Gap description** — the specific absence identified
- **Supporting evidence** — the papers that reveal the gap
- **Counter-evidence** — any partial coverage
- **Severity, novelty, feasibility scores** — these calibrate your ambition

These elements are the raw material for research questions. The gap description becomes the research problem; the supporting evidence becomes the motivation; the counter-evidence defines what has already been attempted; the scores help you calibrate scope.

### 2. Formulate 3–4 Research Questions

Research questions bridge the gap (a negative: what's missing) to the hypothesis (a positive: what we will test). They should progress from broad to specific, creating a logical funnel:

#### RQ Structure

| RQ | Focus | Purpose | Example pattern |
|----|-------|---------|-----------------|
| RQ1 | Feasibility / Existence | Can X even work in this context? Does the phenomenon exist in this population? | "Can [method] be applied to [new context] with acceptable [basic metric]?" |
| RQ2 | Primary Outcome | What is the effect on the main outcome of interest? | "What is the effect of [intervention] on [primary outcome] in [population]?" |
| RQ3 | Transfer / Secondary Outcome | Does the finding generalize? Are there secondary benefits? | "Does the effect of [intervention] transfer to [secondary outcome / different setting]?" |
| RQ4 | Mechanism / Explanation | Why does it work (or not)? What mediates the effect? | "What [factors / mechanisms] mediate the relationship between [intervention] and [outcome]?" |

Not every study needs all four RQs. The gap type and feasibility score should guide how many questions are appropriate:

- **High feasibility (4–5)**: All four RQs are reasonable — the study can be comprehensive
- **Moderate feasibility (3)**: Focus on RQ1 and RQ2 — establish feasibility and primary effect first
- **Low feasibility (1–2)**: RQ1 alone may be ambitious enough — frame it as a pilot or proof-of-concept

Each RQ should be:
- **Specific enough to answer**: Avoid "What is the impact of X?" — specify on whom, measured how
- **Grounded in the gap**: Every RQ should trace back to the gap description
- **Answerable with available methods**: Don't ask questions that require technology or data you can't plausibly obtain

Write each RQ in English, then provide the Traditional Chinese translation.

### 3. Define Hypotheses

For each research question (or at minimum for RQ1 and RQ2), formulate a formal hypothesis pair.

#### Primary Hypothesis (H1) — Derived from RQ2

This is the main claim the research will test. It should be:

- **Directional**: Specify the expected direction of the effect (increase, decrease, outperform, etc.)
- **Quantifiable where possible**: If existing literature suggests an expected magnitude, include it (e.g., "by at least 10%", "with CC > 0.90"). Derive these numbers from the SOTA review's quantitative results — never invent them.
- **Falsifiable**: There must be a conceivable result that would disprove it.

#### Null Hypothesis (H0)

The formal negation of H1. State it explicitly — this clarifies what "failure" looks like and helps design appropriate statistical tests.

#### Secondary Hypotheses (H2, H3)

Derived from RQ3 and RQ4 if applicable. These are subordinate to H1 — they extend the finding rather than establish it. If H1 fails, H2 and H3 typically become moot (unless the study is explicitly designed to test them independently).

For each hypothesis:
1. State H0 and H1 formally
2. Note the expected direction and magnitude (with evidence source)
3. Suggest the statistical approach (e.g., paired t-test, ANOVA, regression) — this isn't a methods section, but the hypothesis should be testable with a nameable test
4. Write in both English and Traditional Chinese

### 4. Define Scope Boundaries (IN/OUT)

This is the most consequential part of this step — and the one most prone to either scope creep (IN scope too broad) or excessive narrowness (OUT scope cuts off interesting directions prematurely). The user will audit these boundaries at Checkpoint 4, so your job is to propose well-reasoned defaults that the user can adjust.

#### IN Scope — What This Research Will Cover

Define each dimension explicitly. These are commitments — everything IN scope must be addressed by the study design.

| Dimension | What to specify |
|-----------|----------------|
| **Population** | Who will be studied? Age, condition, demographics, sample characteristics. Derived from the gap's population gap or PICO population. |
| **Intervention / Method** | What will be applied or tested? The specific technique, algorithm, protocol, or treatment. |
| **Comparison / Control** | What baseline or alternative will the intervention be compared against? |
| **Outcomes** | What will be measured? Primary and secondary outcome variables, metrics. Must map to the RQs. |
| **Setting** | Where will the study be conducted? Lab, clinical, field, simulation, dataset. |
| **Design** | Study type: RCT, quasi-experimental, observational, computational, case study, etc. |
| **Timeframe** | Duration of intervention, follow-up period, data collection window. |

#### OUT Scope — What Is Explicitly Excluded

Every exclusion needs a rationale that would satisfy a peer reviewer. The OUT scope is not a dumping ground for "things we don't feel like doing" — it's a set of defensible boundaries. Common categories:

| Category | Example | Required rationale quality |
|----------|---------|---------------------------|
| **Population exclusion** | "Excludes pediatric populations" | Why: different physiology, ethics complexity, separate study needed |
| **Method exclusion** | "Does not include invasive approaches" | Why: ethics, equipment, or the gap specifically targets non-invasive methods |
| **Outcome exclusion** | "Does not measure long-term outcomes beyond 6 months" | Why: feasibility, timeline, or the gap focuses on acute effects |
| **Setting exclusion** | "Lab setting only, not clinical deployment" | Why: regulatory requirements, pilot-stage research |
| **Comparison exclusion** | "Does not benchmark against commercial products" | Why: reproducibility, access, licensing |

Each OUT item should answer: "If a reviewer asks 'why didn't you also do X?', what's the answer?" If you can't articulate a defensible rationale, the item may not belong in OUT — it may need to be IN scope, or it may be a genuine limitation to acknowledge rather than an exclusion to defend.

Write scope boundaries in both English and Traditional Chinese.

### 5. Conceptual Framework and Risk Assessment

After defining scope, add two practical sections that help the user (and future reviewers) understand the proposed study's architecture and risks.

#### Conceptual Framework / System Architecture

Provide a brief description (and where appropriate, an ASCII diagram) of how the proposed intervention or method works. This isn't a full methods section — it's a high-level sketch that shows the reader the moving parts and how they connect. For computational studies, this might be a system architecture diagram. For clinical studies, a participant flow diagram. For observational studies, a data collection timeline. The goal is to make the study design concrete enough that the reader can spot design flaws or missing components.

#### Risk Assessment

Identify 3–5 key risks to the study's success and propose mitigations. This demonstrates methodological foresight and helps the user plan realistically. Format as a table:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

Common risk categories: insufficient sample/data, tool limitations (false positives/negatives), cost overruns, confounding variables, benchmark saturation, ethical/regulatory delays.

### 6. Recommend 3–5 Target Journals

Journal selection informs writing style, scope calibration, and statistical reporting expectations. Search for and recommend journals based on fit, not just prestige.

For each recommended journal, provide:

| Field | What to include |
|-------|----------------|
| **Journal name** | Full name |
| **Impact Factor** | Most recent IF (use WebSearch to find current data if needed) |
| **Scope fit** | Why this journal matches the hypothesis topic and methodology — be specific, not "good fit" |
| **Typical review timeline** | Average time from submission to first decision (if available) |
| **Open access option** | Whether OA is available and at what cost |
| **Why this journal** | The strategic case: audience reach, methodological alignment, recent interest in this topic |

#### Selection Criteria

Rank journals using these priorities:

1. **Scope match**: Does the journal publish work with this method + population + outcome combination?
2. **Methodology alignment**: Is the journal receptive to the study design (e.g., computational journals for computational studies)?
3. **Recency of similar work**: Has the journal published papers from the SOTA review? If yes, editors and reviewers are primed for this topic.
4. **Impact vs. acceptance tradeoff**: Include a range — one aspirational (high IF, lower acceptance rate), two moderate, one accessible (higher acceptance rate, still reputable).

Use WebSearch to verify current impact factors and scope descriptions. Don't rely solely on memorized journal data — IFs change, journals shift scope, and new venues emerge.

Write journal recommendations in both English and Traditional Chinese.

## Output

### `step8_hypothesis_specification.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 8
selected_gap: "GAP_{N}"
dropped_gaps: ["GAP_{X}", "GAP_{Y}"]  # if user explicitly dropped gaps
design_constraint: "{constraint description}"  # if user specified a constraint, omit otherwise
research_questions: {N}
hypotheses: {N}
---

# Hypothesis Specification / 假說規格書

> Topic / 研究主題: {topic}
> Selected Gap / 選定缺口: GAP_{N} — {gap title}
> Dropped Gaps / 放棄缺口: GAP_{X} ({title}), GAP_{Y} ({title})  — if applicable
> Date / 日期: {date}

## Executive Summary / 總覽摘要

{2-3 paragraph overview: what gap is being addressed, what the proposed research will test, and what the expected contribution to the field is. This should read as a standalone justification for the study — someone reading only this section should understand why this research matters.}

{繁體中文翻譯}

---

## Selected Gap Summary / 選定缺口摘要

**Gap ID:** GAP_{N}
**Type / 類型:** {gap type}
**Priority Score / 優先分數:** {composite score}

{Brief restatement of the gap — 2-3 sentences summarizing the absence identified in Step 7, with key supporting citations.}

{繁體中文翻譯}

---

## Research Questions / 研究問題

### RQ1: {Research question — Feasibility/Existence} / {中文}

{Elaboration: what this question targets, why it's the logical starting point, what a positive answer would look like.}

{繁體中文說明}

### RQ2: {Research question — Primary Outcome} / {中文}

{Elaboration: connection to the gap, what outcome is being measured, expected direction.}

{繁體中文說明}

### RQ3: {Research question — Transfer/Secondary} / {中文}

{Elaboration: what secondary outcome or generalization is being tested.}

{繁體中文說明}

### RQ4: {Research question — Mechanism} / {中文}

{Elaboration: what explanatory question this addresses.}

{繁體中文說明}

---

## Hypotheses / 假說

### Primary Hypothesis / 主要假說

**H0 (Null / 虛無假說):**

{Formal null hypothesis statement}

{繁體中文}

**H1 (Alternative / 對立假說):**

{Formal alternative hypothesis — directional, quantifiable where evidence supports it}

{繁體中文}

**Expected Direction & Magnitude / 預期方向與幅度:**

{What direction is the effect expected in? What magnitude, based on which prior results? Cite the specific papers and their reported metrics.}

{繁體中文}

**Suggested Statistical Approach / 建議統計方法:**

{Name the test(s) and justify briefly — e.g., "Paired t-test (within-subject comparison, continuous outcome, two conditions)"}

{繁體中文}

### Secondary Hypothesis H2 / 次要假說 H2

{Same structure as H1: H0, H1, direction, statistical approach}

### Secondary Hypothesis H3 / 次要假說 H3

{Same structure, if applicable}

---

## Scope Boundaries / 範圍界定

### IN Scope / 範圍內

| Dimension / 維度 | Specification / 規格 |
|-----------------|---------------------|
| **Population / 族群** | {Who will be studied} / {中文} |
| **Intervention / Method / 介入/方法** | {What will be applied} / {中文} |
| **Comparison / Control / 對照/控制** | {What baseline} / {中文} |
| **Primary Outcome / 主要結果** | {What will be measured — primary} / {中文} |
| **Secondary Outcome / 次要結果** | {What will be measured — secondary} / {中文} |
| **Setting / 場域** | {Where} / {中文} |
| **Design / 設計** | {Study type} / {中文} |
| **Timeframe / 時間框架** | {Duration} / {中文} |

### OUT Scope / 範圍外

| Exclusion / 排除項目 | Rationale / 學術理由 |
|---------------------|---------------------|
| {What is excluded} / {中文} | {Why — academically defensible reason} / {中文} |
| {What is excluded} / {中文} | {Why} / {中文} |
| {What is excluded} / {中文} | {Why} / {中文} |
| ... | ... |

### Scope Rationale / 範圍邏輯

{A paragraph explaining the overall scope strategy: why IN scope covers what it does, how OUT scope exclusions create a focused but meaningful study. Address potential reviewer concerns proactively.}

{繁體中文翻譯}

---

## Conceptual Framework / 概念框架

{High-level description of the proposed method/intervention architecture. Include an ASCII diagram for computational/engineering studies, or a participant flow / data collection timeline for clinical/observational studies. The goal is to make the study design concrete.}

{繁體中文說明}

---

## Risk Assessment / 風險評估

| Risk / 風險 | Likelihood / 可能性 | Impact / 影響 | Mitigation / 緩解策略 |
|------------|-------------------|-------------|---------------------|
| {Risk 1} | {Low/Medium/High} | {Low/Medium/High} | {How to mitigate} |
| {Risk 2} | ... | ... | ... |
| {Risk 3} | ... | ... | ... |

---

## Gap-to-Hypothesis Traceability / 缺口到假說追溯

{A mapping showing how each element traces back to evidence:}

| Element / 元素 | Source / 來源 | Evidence / 證據 |
|---------------|-------------|----------------|
| RQ1 | GAP_{N} description | {gap description → RQ1 connection} |
| RQ2 | GAP_{N} + SOTA Theme {X} | {evidence linking} |
| H1 direction | {CitationKey} ({Year}) | {reported metric that suggests expected direction} |
| H1 magnitude | {CitationKey} ({Year}) | {reported effect size or benchmark} |
| IN: Population | GAP_{N} population gap | {specific absence identified} |
| OUT: {exclusion} | Feasibility score = {N} | {practical constraint} |

---

> **Checkpoint 4: 護城河最終確認**
>
> Review the IN/OUT boundaries above. Verify that:
> 1. Every OUT exclusion has an academically defensible rationale
> 2. The scope matches your actual time, budget, and resource constraints
> 3. The hypotheses are testable with your available methods and data
>
> 請審核上述 IN/OUT 邊界。確認：
> 1. 每個 OUT 排除項目都有可在學術上辯護的理由
> 2. 範圍符合您實際的時間、預算和資源限制
> 3. 假說可用您現有的方法和數據進行測試
>
> To proceed, confirm: "Scope approved" — then I'll generate journal recommendations and you can move to manuscript writing.
>
> 請確認：「範圍核准」——然後我將生成期刊推薦，您可以進入論文寫作階段。

---

Files / 檔案: `step8_hypothesis_specification.md`
Next step / 下一步: Review journal recommendations, then `/research-write`
```

### `step8_journal_recommendations.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 8
journals_recommended: {N}
---

# Journal Recommendations / 目標期刊推薦

> Topic / 研究主題: {topic}
> Hypothesis / 假說: {H1 short summary}
> Date / 日期: {date}

## Selection Criteria / 選擇標準

{Brief explanation of how journals were selected: scope match to the hypothesis, methodology alignment, recency of similar publications, and impact/acceptance tradeoff.}

{繁體中文翻譯}

---

## Recommended Journals / 推薦期刊

### 1. {Journal Name} ⭐ Top Recommendation / 首選推薦

| Field / 欄位 | Details / 詳細 |
|-------------|---------------|
| **Impact Factor / 影響因子** | {IF} ({year}) |
| **Scope Fit / 範圍契合** | {Specific explanation} / {中文} |
| **Review Timeline / 審稿時程** | {Typical time to first decision} |
| **Open Access / 開放取用** | {OA availability and cost} |
| **Why This Journal / 推薦原因** | {Strategic case} / {中文} |

**Papers from our collection published here / 我們文獻中發表於此刊的論文:**
- {CitationKey} ({Year}) — indicates topic relevance and reviewer familiarity

---

### 2. {Journal Name}

{Same table structure}

---

### 3. {Journal Name}

{Same table structure}

---

### 4. {Journal Name} (if applicable)

{Same table structure}

---

### 5. {Journal Name} (if applicable)

{Same table structure}

---

## Journal Comparison / 期刊比較

| Rank / 排名 | Journal / 期刊 | IF | Scope Fit / 契合度 | Review Time / 審稿時間 | OA Cost / OA費用 | Strategy / 策略 |
|------------|--------------|-----|-------------------|---------------------|-----------------|----------------|
| 1 | {name} | {IF} | {High/Medium} | {time} | {cost} | ⭐ Best fit / 最佳契合 |
| 2 | {name} | {IF} | {High/Medium} | {time} | {cost} | Aspirational / 挑戰型 |
| 3 | {name} | {IF} | {High/Medium} | {time} | {cost} | Solid match / 穩健型 |
| 4 | {name} | {IF} | {Medium} | {time} | {cost} | Accessible / 易接受型 |

---

## Submission Strategy / 投稿策略

{Recommended submission order and contingency plan: which journal to try first, what to do if rejected, how to adapt the manuscript for each venue.}

{繁體中文翻譯}

---

Files / 檔案: `step8_journal_recommendations.md`
Next step / 下一步: `/research-write`
```

## After Saving

Update `step0_session_config.json`: set `"current_step": 8`.

Then present to the user:

1. **Executive summary** — what gap is being addressed and the proposed research direction (bilingual)
2. **Research questions** — the 3–4 RQs with brief context
3. **Primary hypothesis** — H0 and H1 with expected direction
4. **Scope boundaries** — IN/OUT summary table
5. **Top journal recommendation** — the best-fit venue with rationale
6. **Checkpoint 4 prompt** — explicitly ask the user to audit IN/OUT boundaries

## Edge Cases

### Abstract-Only Sessions

Check the SOTA review's YAML frontmatter for `abstract_only: true` or `full_text_papers: 0`. If the entire pipeline ran on abstracts only, your hypotheses will be less precisely calibrated — effect sizes and methodological details drawn from abstracts are less reliable than from full texts. Add a caveat after the frontmatter:

```
> [!warning] Abstract-Based Hypothesis / 僅摘要假說
> This hypothesis is derived from an abstract-only gap analysis and SOTA review. Expected effect sizes and methodological details may be imprecise. Consider running `/research-fulltext` to access full papers before finalizing the study design.
> 本假說基於僅摘要的缺口分析與文獻綜述。預期效果量和方法學細節可能不夠精確。建議在最終確定研究設計前，先執行 `/research-fulltext` 以取得完整論文。
```

### No Quantitative Benchmarks Available

Some gaps (especially in qualitative, theoretical, or emerging fields) may not have existing quantitative results to derive expected magnitudes from. In this case:

- State H1 directionally without magnitude: "X will improve Y" rather than "X will improve Y by Z%"
- Note explicitly that magnitude is exploratory: "No prior work provides a basis for expected effect size; this study will establish baseline estimates"
- Consider framing the study as exploratory or pilot rather than confirmatory
- Adjust the journal recommendations accordingly — some journals are more receptive to exploratory studies

### Multiple Gaps Locked

If the user locked more than one gap (e.g., "Lock GAP_001 and GAP_002"), you need to decide whether they represent a single study or multiple studies:

- **Single study**: If the two gaps are complementary (e.g., a methodological gap + a population gap), they can be addressed in one hypothesis specification with RQs spanning both gaps. Note this explicitly.
- **Multiple studies**: If the gaps are independent, recommend addressing them as separate studies. Write the hypothesis specification for the higher-priority gap first, and note the second gap as future work.

Ask the user for clarification if the relationship between locked gaps is ambiguous.

### Very Narrow Gap (High Feasibility, Low Novelty)

If the gap's novelty score is low (1–2) but feasibility is high, the resulting hypothesis may feel incremental. This is OK — incremental research is still valuable. But adjust your framing:

- Position the contribution as validation, replication, or extension rather than groundbreaking discovery
- Recommend journals that value systematic replication or applied studies
- Consider whether the gap is better addressed as part of a larger study rather than standalone

### Very Broad Gap (High Novelty, Low Feasibility)

If the gap's feasibility is low (1–2), the hypothesis needs aggressive scoping:

- Frame as a pilot study or proof-of-concept
- Limit to RQ1 (feasibility) and possibly RQ2 (primary effect)
- Set conservative success criteria
- IN scope should be narrow; OUT scope extensive with honest rationale
- Recommend journals with shorter formats (letters, brief communications) or that accept pilot studies

### User Has Specific Methodological Constraints

If the user specifies a particular method, tool, or study design (e.g., "I want to use deep learning" or "we can only do an observational study"), this fundamentally reshapes how the gap can be addressed. Don't just swap in the user's method and leave everything else unchanged — think through the implications:

1. **Add a "Constraint Adaptation" section** right after the Selected Gap Summary, explaining how the user's constraint reshapes the gap. For example, if the gap calls for an RCT but the user can only do observational work, explain how the study addresses a tractable sub-question of the original gap rather than the full gap.
2. **Reframe the RQs** to match the feasible design. An observational study can't answer causal questions — reframe from "Does X cause Y?" to "Is X associated with Y?" or "Does the effect of X persist over time?"
3. **Adjust scope boundaries**: The user's constraint should appear in IN scope (as the chosen design) and the excluded alternative should appear in OUT scope with a rationale that references the user's practical constraint.
4. **Calibrate ambition**: A constrained study often generates pilot data for a future definitive study. Note this positioning in the executive summary — it helps reviewers understand why the study matters even with its limitations.
5. **Note the constraint in the YAML frontmatter**: Add a `design_constraint` field (e.g., `design_constraint: "12-month observational follow-up, no new RCT"`).

## Verification Checklist

Before saving, verify:

1. **Gap traceability**: Every RQ traces back to the selected gap. Every hypothesis traces back to an RQ. The traceability table has no gaps.
2. **Evidence-based magnitudes**: Any quantitative expectations in hypotheses cite specific papers from the SOTA review. No invented numbers.
3. **H0/H1 consistency**: H0 is the logical negation of H1. For each hypothesis pair, both cannot be true simultaneously, and one must be true.
4. **Scope completeness**: Every IN dimension has a specification. Every OUT exclusion has a rationale.
5. **Scope-hypothesis alignment**: Everything needed to test the hypotheses is IN scope. Nothing IN scope is irrelevant to the hypotheses.
6. **Journal verification**: Impact factors and scope descriptions have been verified via WebSearch, not recalled from memory.
7. **PICO consistency**: IN scope is a refinement of the original PICO, not a contradiction. If the hypothesis narrows the PICO (which it should), the narrowing is justified by the gap.
8. **Bilingual completeness**: Every substantive section (RQs, hypotheses, scope items, rationale) has both English and Traditional Chinese content.
9. **Statistical approach named**: Each hypothesis has a suggested statistical test. The test is appropriate for the study design and data type.

## Bilingual Communication

Follow the same conventions as previous pipeline steps:
- Section headings: bilingual (e.g., "Research Questions / 研究問題")
- Table headers: bilingual
- RQ and hypothesis statements: English then Chinese translation
- Scope items: bilingual in each cell
- Evidence citations: keep citation keys, author names, and quantitative data in English in both language versions
- Technical terms in English with Chinese explanation on first mention: e.g., "null hypothesis（虛無假說）", "scope boundary（範圍邊界）", "effect size（效果量）"

## Bilingual Translation Safety

Hypothesis specification involves precise scientific claims. The Chinese translation must preserve logical precision:

- "will improve" → 「將改善」, not 「可能改善」(preserve directional commitment of the hypothesis — hedging belongs in the discussion, not the hypothesis statement)
- "is excluded because" → 「因...而排除」, not 「不研究」(the former implies a reasoned decision, the latter implies indifference)
- "we hypothesize that" → 「我們假設」, not 「我們認為」(hypothesize ≠ believe — hypotheses are tested, beliefs are held)
- "no significant difference" (H0) → 「無顯著差異」, not 「沒有差別」(preserve statistical terminology)
- "expected effect size" → 「預期效果量」, not 「預期效果」(preserve the quantitative nature of "size")
- "feasibility" → 「可行性」, not 「可能性」(feasibility ≠ possibility — feasibility implies practical assessment)
