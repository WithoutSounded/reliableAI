---
name: research-sota
description: "Step 6 of the Research Agent pipeline: synthesize shortlisted papers into a thematic state-of-the-art review with an Obsidian Canvas knowledge graph. Use this skill whenever the user wants to build a SOTA review, synthesize papers by theme, create a literature synthesis, map research themes, generate a knowledge graph from papers, or says 'next step' after research-fulltext (Step 5). Trigger on: 'build SOTA', 'synthesize papers', 'thematic review', 'literature synthesis', 'knowledge graph', 'SOTA review', '文獻綜述', '主題綜整', '知識圖譜', 'state of the art', or any request to organize collected papers into a structured thematic analysis — even if they just say 'what do these papers tell us' or '幫我整理這些論文'."
---

# Research SOTA — Step 6 of Research Agent Pipeline

You are synthesizing a collection of academic papers into a thematic state-of-the-art review. This is the intellectual core of the pipeline: everything before this step (search, screen, export, fulltext) was gathering and organizing material; everything after (gaps, hypothesis, manuscript) depends on the quality of your synthesis here.

The difference between a good SOTA review and a bad one is the difference between synthesis and summary. A summary tells you what each paper says; a synthesis tells you what the field knows, what it debates, and where it's heading. Your job is synthesis — find the patterns, tensions, and trajectories that emerge when you read the papers as a collective body of work, not as isolated contributions.

You produce two outputs: a bilingual thematic review document and an Obsidian Canvas knowledge graph that visually maps the relationships between papers, themes, and methodologies.

## Input

Read these files from the session folder:

1. **`step5_full_text/*.md`** — Full-text papers converted to markdown (excluding `_zh.md` bilingual versions and `_access_log.md`). These are your primary source material.
2. **`step3_shortlist.json`** — Paper metadata, screening scores, and citation network data. Use this for abstract-only papers (where full text wasn't available) and for citation cluster information from Step 2.
3. **`step4_citation_keys.md`** — Citation key lookup table. Use these keys when referencing papers throughout the review.
4. **`step4_references_apa.md`** — APA reference list. Useful for quickly checking author names and years.

### Handling Missing Full Texts

If `step5_full_text/` is missing or empty but `step3_shortlist.json` exists, the user wants to proceed without full texts. This is valid — you can still produce a useful thematic review from abstracts alone. However, you must:

1. **Warn the user in conversation** that synthesis will be based on abstracts only and depth will be limited
2. **Add a prominent caveat in the review file itself**, right after the frontmatter, using an Obsidian callout block:
   ```
   > [!warning] Abstract-Only Synthesis / 僅摘要綜整
   > This review is based on abstracts only — full texts were not available (`step5_full_text/` not found). Synthesis depth is limited: claims cannot be verified against full methodology sections, and quantitative results may be incomplete. Run `/research-fulltext` first for a deeper review.
   > 本綜述僅基於摘要——全文不可用（`step5_full_text/` 未找到）。綜整深度有限：無法根據完整方法學章節驗證論點，定量結果可能不完整。建議先執行 `/research-fulltext` 以獲得更深入的綜述。
   ```
3. **Note in the YAML frontmatter**: `abstract_only: true` and `full_text_papers: 0`

Do not refuse to proceed or insist the user run fulltext first — they may have good reasons to skip it. Just make the limitation visible.

### Reading the Papers

Start by reading every paper in `step5_full_text/`. Read the English-only versions (`{citation_key}.md`), not the bilingual `_zh.md` files. For each paper, focus on:

- **Introduction**: What problem does the paper address? How does it frame the research question?
- **Methods**: What approach, dataset, or experimental design was used?
- **Results**: What were the key quantitative findings? (effect sizes, accuracy metrics, statistical significance)
- **Discussion/Conclusion**: What do the authors claim? What limitations do they acknowledge?

For abstract-only papers (those with `access_level: "abstract-only"` in frontmatter), you're limited to title, abstract, and metadata from the shortlist. These papers can still contribute to theme identification and cross-referencing, but you should weight their contributions lower in synthesis — you can't verify claims you haven't read in detail.

Take notes as you read. You're looking for:
- Recurring methods or frameworks across papers
- Conflicting results between studies
- Evolving trends (older papers use method X, newer papers shift to method Y)
- Gaps that multiple papers mention in their "future work" sections
- Papers that cite each other and build on each other's work

## Procedure

### 1. Identify 4–6 Themes

Themes are the organizing structure of your review. A good theme groups papers that address a common question, use a shared methodology, or contribute to the same strand of knowledge — not just papers that happen to share a keyword.

**How to find themes:**

Start with the citation clusters from `step3_shortlist.json` (the `citation_network.cluster` field). These clusters — detected in Step 2 based on which papers cite each other — are strong signals of intellectual groupings. Papers that cite each other are usually working on related questions.

Then refine by reading the actual content. Citation clusters sometimes group papers that are related but address different aspects. You may need to:
- **Split** a large citation cluster into two themes if it contains distinct sub-topics
- **Merge** small clusters that address the same theme from different angles
- **Create** a new theme for papers that don't cluster together by citation but share a methodological or conceptual thread

**What makes a good theme:**
- It has a clear intellectual identity — you can explain what this theme is "about" in one sentence
- It contains at least 2–3 papers (a theme with one paper is probably too narrow)
- It's distinct from other themes — if you can't explain how Theme A differs from Theme B, they should probably be merged
- It reflects genuine intellectual structure, not surface-level keyword grouping

**Theme naming:** Each theme gets a short English title and a Chinese translation. The title should capture the theme's intellectual focus, not just list keywords. For example:
- Good: "Transformer Architectures for EEG Decoding" / "Transformer 架構於腦電訊號解碼之應用"
- Bad: "Deep Learning Papers" / "深度學習論文"

**Assign every shortlisted paper to exactly one primary theme.** Some papers span multiple themes — note these as bridge papers in the cross-theme analysis (Section 3), but assign them to the theme they contribute to most directly.

### 2. Synthesize Each Theme

For each theme, write a structured synthesis section. The goal is to tell the story of this research strand — what do we know, how do we know it, and what remains uncertain?

Structure each theme section around these four dimensions:

#### a) Consensus — What does the field agree on?

Identify findings that multiple papers in this theme support. Cite specific papers and, where possible, quote specific numbers:
- "Three independent RCTs (Author1Year, Author2Year, Author3Year) consistently found 15–20% improvement in working memory after 8 weeks of intervention"
- Not: "Several studies found improvements"

Consensus claims need at least 2 supporting papers. A single study's finding is a result, not a consensus.

#### b) Debates — What is contested or unresolved?

Identify areas where papers disagree or where evidence is mixed. This is where the review becomes most valuable — it helps the reader understand not just "what's known" but "what's still being argued about."

For each debate, present both sides with citations:
- "While Author1Year reports significant effects using protocol X, Author2Year found no significant difference using a similar protocol but with a different population, suggesting that population characteristics may moderate the effect"

#### c) Dominant Methods — What approaches does this theme rely on?

Describe the methodological landscape:
- What experimental designs are most common? (RCT, case-control, cross-sectional)
- What tools, frameworks, or datasets are standard?
- What analytical methods dominate? (specific statistical tests, ML architectures)
- Are there methodological trends over time? (shift from method A to method B)

This dimension directly feeds the knowledge graph's color-coding and the gap analysis in Step 7.

#### d) Key Quantitative Results

Compile the most important numbers from papers in this theme into a comparison. Use a table when comparing across studies:

| Study | N | Method | Primary Outcome | Result |
|-------|---|--------|----------------|--------|
| Author1Year | 45 | Protocol X | Working memory | +18% (p<0.01) |
| Author2Year | 30 | Protocol Y | Working memory | +12% (p<0.05) |

Not every theme will have cleanly comparable quantitative results — some themes are more conceptual or methodological. Adapt the structure to what the papers actually contain. Don't force a quantitative table where the data doesn't support it.

### 3. Analyze Cross-Theme Patterns

After synthesizing individual themes, step back and look at the collection as a whole. This section identifies patterns that span themes — the meta-level insights that emerge only when you consider all the work together.

Cover three dimensions:

#### a) Methodological Trends Over Time

How has the field's approach evolved? Look at the publication years within and across themes:
- Are newer papers using different methods than older ones?
- Is there a convergence toward a particular approach?
- Are certain methods emerging or declining?

#### b) Converging and Diverging Findings

Which findings hold up across themes, and which are theme-specific?
- **Converging**: "Across all themes, studies consistently find that X outperforms Y" — these are the strongest claims the field can make
- **Diverging**: "Theme A studies report positive effects of X, while Theme C studies focused on a different population find no effect" — these point toward moderating variables or boundary conditions

#### c) Theme Interactions

Identify papers or findings that bridge themes. Some papers may appear in one theme but have methods from another, or their findings inform a different theme's debates:
- "Author1Year (Theme 2) developed a framework that was later adopted by three papers in Theme 4, suggesting a methodological transfer from basic science to applied clinical work"
- Note bridge papers here — papers you assigned to one theme but that contribute meaningfully to another

### 4. Build the Knowledge Graph

The knowledge graph is an Obsidian Canvas file (`.canvas`) that visually represents the relationships between papers, themes, and methodologies. It serves as a navigational map of the literature — the user can open it in Obsidian and click through to individual papers.

#### Node Types

**Group nodes** — One per theme. The group spatially contains all papers belonging to that theme.
```json
{
  "id": "theme-{N}",
  "type": "group",
  "x": ..., "y": ..., "width": ..., "height": ...,
  "label": "{Theme Title EN} / {Theme Title ZH}",
  "color": "0"
}
```
Group color should be neutral (`"0"` or omitted) since individual paper nodes carry the methodology color.

**Paper nodes** — One per paper. Color-code by the paper's primary methodology category.

- If the paper has a full-text file in `step5_full_text/`, use `type: "file"` to link to it — this makes the node clickable in Obsidian:
```json
{
  "id": "{citation_key}",
  "type": "file",
  "file": "{session_folder}/step5_full_text/{citation_key}.md",
  "x": ..., "y": ..., "width": 320, "height": 70,
  "color": "{color_code}"
}
```

- If no full-text files exist (abstract-only session), use `type: "text"` with the citation key and short title:
```json
{
  "id": "{citation_key}",
  "type": "text",
  "text": "**{citation_key}**\n{short_title} ({year})",
  "x": ..., "y": ..., "width": 320, "height": 70,
  "color": "{color_code}"
}
```

**Overview node** — A single node linking to the SOTA review document itself, placed prominently at the top of the canvas.
```json
{
  "id": "overview",
  "type": "file",
  "file": "{session_folder}/step6_sota_review.md",
  "x": ..., "y": ..., "width": 450, "height": 100,
  "color": "6"
}
```

#### Methodology Color Codes

Assign each paper a methodology color based on its primary research approach:

| Methodology | Color Code | Obsidian Color |
|-------------|-----------|----------------|
| Experimental (RCT, controlled study) | `"1"` | Red |
| Computational (ML, simulation, algorithm) | `"2"` | Orange |
| Review (systematic review, meta-analysis) | `"3"` | Yellow |
| Observational (cohort, cross-sectional, case study) | `"4"` | Green |
| Engineering (system design, framework, BCI hardware) | `"5"` | Cyan |
| Theoretical (model, theory, conceptual framework) | `"6"` | Purple |

Most papers have a clear primary methodology. If a paper genuinely straddles two categories (e.g., an RCT that also proposes a computational model), choose the methodology that the paper's main contribution belongs to.

#### Edges

Edges represent meaningful relationships between papers. Don't connect every pair — focus on connections that convey intellectual structure.

**Types of edges to draw:**
- **Shared methodology with specific label**: "shared: transformer-based EEG decoding"
- **Build-on relationship**: "extends protocol to elderly population"
- **Contradicts**: "conflicting results on alpha-band training"
- **Review includes primary study**: "primary study included in meta-analysis"
- **Methodological transfer**: "framework concept → practical implementation"

```json
{
  "id": "edge-{from}-{to}",
  "fromNode": "{citation_key_1}",
  "fromSide": "right",
  "toNode": "{citation_key_2}",
  "toSide": "left",
  "label": "{relationship description}"
}
```

**Edge guidelines:**
- Prefer specific labels over generic ones. "shared: theta-band neurofeedback protocol" is better than "related"
- Use `fromSide`/`toSide` to avoid visual clutter — edges between papers in the same group should use `"top"`/`"bottom"`, edges between groups should use `"left"`/`"right"`
- Aim for 1–3 edges per paper. A paper with zero edges is suspicious (is it truly connected to the collection?). A paper with 6+ edges probably has some redundant connections.
- Citation relationships from `step3_shortlist.json` are a good starting point, but add conceptual edges the citation network misses (e.g., two papers using the same method but not citing each other)

#### Layout Strategy

Arrange themes as spatial clusters with enough spacing that the canvas is readable:
- Place the overview node at the top center
- Arrange theme groups in a roughly circular or grid layout around the overview
- Leave ~200px gaps between groups
- Within each group, stack paper nodes vertically with ~30px spacing
- Size groups to fit their contents with ~50px padding

A canvas with 15 papers in 5 themes needs roughly 2500×1500px of total space. Scale accordingly.

### 5. Bilingual Content

All substantive content in the SOTA review must be bilingual (English + Traditional Chinese). This applies to:
- Theme titles and descriptions
- Synthesis text (each paragraph in English followed by Chinese translation)
- Cross-theme analysis
- Table headers
- Section headings

Follow the same conventions as previous pipeline steps:
- Section headings: `## Theme 1: {English Title} / {中文標題}`
- Paragraph structure: English paragraph first, then Chinese translation
- Technical terms: keep English with Chinese explanation on first mention, e.g., "systematic review（系統性文獻回顧）"
- Citation keys and author names stay in English in both languages
- Quantitative data (numbers, p-values, effect sizes) stay as-is in both languages
- LaTeX equations stay as-is in both languages

For the knowledge graph, use bilingual labels on group nodes: `"Theme Title EN / 中文標題"`. Edge labels stay in English (they're short relational descriptions).

## Output

### `step6_sota_review.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 6
total_papers: {N}
themes: {N_themes}
full_text_papers: {N_fulltext}
abstract_only_papers: {N_abstract}
---

# State-of-the-Art Review / 研究現況綜述

> Topic / 研究主題: {topic}
> Papers synthesized / 綜整論文數: {N}
> Themes identified / 主題數: {N_themes}
> Date / 日期: {date}

## Executive Summary / 總覽摘要

{2-3 paragraph overview of what this body of literature tells us — the big picture. What is the field doing, where is it heading, and what are the major open questions?}

{同上的繁體中文翻譯}

## Methodology Legend / 方法學圖例

| Color / 顏色 | Methodology / 方法學 | Count / 數量 |
|-------------|---------------------|-------------|
| 🔴 Red | Experimental / 實驗研究 | {n} |
| 🟠 Orange | Computational / 計算方法 | {n} |
| 🟡 Yellow | Review / 文獻回顧 | {n} |
| 🟢 Green | Observational / 觀察研究 | {n} |
| 🔵 Cyan | Engineering / 工程設計 | {n} |
| 🟣 Purple | Theoretical / 理論研究 | {n} |

---

## Theme 1: {Title EN} / {標題中文}

**Papers / 論文:** {citation_key_1}, {citation_key_2}, {citation_key_3}

### Consensus / 共識

{English synthesis paragraph with inline citations like (AuthorYear)}

{繁體中文翻譯}

### Debates / 爭議

{English synthesis paragraph}

{繁體中文翻譯}

### Dominant Methods / 主流方法

{English description of methodological landscape}

{繁體中文翻譯}

### Key Results / 關鍵發現

{Quantitative comparison table or narrative, depending on what the papers contain}

{繁體中文翻譯或標註}

---

## Theme 2: ...

...

---

## Cross-Theme Analysis / 跨主題分析

### Methodological Trends Over Time / 方法學時間趨勢

{English analysis}

{繁體中文翻譯}

### Converging Findings / 匯聚發現

{English analysis with citations}

{繁體中文翻譯}

### Diverging Findings / 分歧發現

{English analysis with citations}

{繁體中文翻譯}

### Theme Interactions / 主題交互

{English analysis — bridge papers, methodological transfers}

{繁體中文翻譯}

---

## Paper–Theme Mapping / 論文主題對照

| Citation Key / 引用鍵 | Theme / 主題 | Methodology / 方法學 | Bridge? / 跨主題? |
|----------------------|-------------|---------------------|------------------|
| `{key}` | {theme_N} | {methodology} | {Yes/—} |
| ... |

---

Files / 檔案: `step6_sota_review.md`, `step6_knowledge_graph.canvas`
Next step / 下一步: `/research-gaps`
```

### `step6_knowledge_graph.canvas`

A valid Obsidian Canvas JSON file. Structure:

```json
{
  "nodes": [
    {"id": "overview", "type": "file", "file": "...", "x": ..., "y": ..., "width": 450, "height": 100, "color": "6"},
    {"id": "theme-1", "type": "group", "x": ..., "y": ..., "width": ..., "height": ..., "label": "Theme Title / 中文標題"},
    {"id": "AuthorYear", "type": "file", "file": "...", "x": ..., "y": ..., "width": 320, "height": 70, "color": "1"},
    ...
  ],
  "edges": [
    {"id": "edge-a-b", "fromNode": "AuthorYear1", "fromSide": "bottom", "toNode": "AuthorYear2", "toSide": "top", "label": "shared: specific methodology"},
    ...
  ]
}
```

**Validation before saving:**
1. Every `file` path in a node must point to an actual file in the session folder
2. Every `fromNode` and `toNode` in an edge must match an existing node `id`
3. Every paper from `step3_shortlist.json` must appear as a node in the canvas
4. Every paper node must be spatially inside its assigned theme group
5. The JSON must be valid — test by checking that `nodes` and `edges` are both arrays

## After Saving

Update `step0_session_config.json`: set `"current_step": 6`.

Then present to the user:

1. **Executive summary** — the 2-3 paragraph overview (bilingual)
2. **Theme list** — numbered themes with paper counts and one-line descriptions
3. **Methodology distribution** — the color legend table with counts
4. **Cross-theme highlights** — 2-3 most interesting cross-theme patterns
5. **Knowledge graph** — tell the user to open `step6_knowledge_graph.canvas` in Obsidian to explore the visual map
6. **Suggest next step:** `/research-gaps`

## Edge Cases

- **Small collections (<10 papers)**: Reduce to 2-3 themes. With very few papers, having 5-6 themes means most themes have only 1 paper, which defeats the purpose of thematic grouping. Note to the user that the synthesis is limited by collection size.
- **Large collections (>30 papers)**: You may find more than 6 natural themes. It's OK to go up to 7-8, but beyond that, look for opportunities to merge related themes under broader headings with sub-themes. The review becomes unwieldy if there are too many top-level themes.
- **Mostly abstract-only papers**: If >50% of papers are abstract-only, warn the user prominently. Your synthesis will be shallower — you're working from abstracts rather than full arguments and data. Recommend the user retrieve more full texts before relying on this review for gap analysis.
- **Highly interdisciplinary collections**: Papers from different fields may use incompatible methodology categories. A neuroscience paper's "experimental" is very different from a CS paper's "experimental." Adapt the methodology legend to the specific collection — you can rename categories if the defaults don't fit. The color codes (1-6) stay the same; the labels can change.
- **Papers that don't fit any theme**: If 1-2 papers are genuine outliers, create a "Peripheral / Related Work" theme rather than forcing them into an ill-fitting group. But if many papers don't fit, your themes may need rethinking.
- **No citation network data**: If `step3_shortlist.json` lacks `citation_network` fields (e.g., user ran an older version of the pipeline), identify themes purely from content analysis. The procedure still works — citation clusters are a helpful starting signal, not a requirement.
- **Non-standard session folder structure**: If the user has organized files differently (e.g., different folder names), adapt. The filenames and content matter more than the exact folder path.

## Verification Checklist

Before saving, verify:

1. **Paper coverage**: Every paper in `step3_shortlist.json` is mentioned in the review and appears in the knowledge graph canvas
2. **Theme assignment**: Every paper is assigned to exactly one theme in the Paper–Theme Mapping table
3. **Citation key consistency**: All citation keys used in the review match those in `step4_citation_keys.md`
4. **Canvas validity**: The `.canvas` file is valid JSON with `nodes` and `edges` arrays. All node IDs referenced in edges exist in the nodes array.
5. **File paths**: All `file` fields in canvas nodes point to existing files relative to the vault root
6. **Bilingual completeness**: Every substantive section has both English and Chinese content
7. **No unsupported claims**: Every factual statement in the synthesis is traceable to at least one cited paper. If you find yourself writing something without a citation, either find the source or remove the claim.

## Bilingual Communication

Follow the same conventions as previous pipeline steps:
- Section headings: bilingual (e.g., "Cross-Theme Analysis / 跨主題分析")
- Table headers: bilingual
- Theme names: bilingual
- Synthesis paragraphs: English paragraph then Chinese translation
- Technical terms in English with Chinese explanation on first mention: e.g., "state-of-the-art review（研究現況綜述）", "knowledge graph（知識圖譜）", "citation cluster（引用聚類）"
- Keep citation keys, author names, journal names, and quantitative data in English in both language versions

## Bilingual Translation Safety

Scientific synthesis adds a translation challenge beyond term-level accuracy: you need to preserve the epistemic nuance. Phrases like "suggests," "demonstrates," "is associated with," and "causes" have very different strength — make sure the Chinese translation preserves the same level of certainty.

- "suggests" → 「顯示」 or 「暗示」, not 「證明」
- "is associated with" → 「與⋯有關聯」, not 「導致」
- "demonstrates" → 「展示」 or 「證實」
- "may contribute to" → 「可能有助於」, not 「有助於」

When in doubt, use the weaker/more hedged Chinese phrasing. Overclaiming in a literature review is a serious academic issue.
