---
name: research-init
description: "Initialize a research session: parse a topic into PICO framework, generate strategic search queries, and create the session folder. This is Step 1 of the Research Agent pipeline. Use this skill when the user wants to start a new research project, set up a literature review session, define a research question with PICO, generate academic search queries, or says things like 'I want to research X', 'help me set up a study on X', 'research-init', or '/research-init'. Also trigger when the user asks for research topic recommendations based on recent breakthroughs."
---

# Research Init — Step 1 of Research Agent Pipeline

You are initializing a structured research session. Your job is to take a research topic (user-provided or recommended), decompose it into a PICO framework, generate 5 strategic search queries, and save everything as the session config that all downstream pipeline steps will consume.

This step matters because a well-framed PICO and a diverse set of search queries determine the quality of everything downstream — the papers found, the screening accuracy, and ultimately the literature review itself. Garbage in, garbage out.

## Input Modes

The user will enter in one of two ways:

### Mode A: User provides a topic

The user gives you a topic directly, e.g.:
- `research-init EEG-based cognitive training for elderly`
- `我想研究 brain-computer interface 在憂鬱症治療的應用`

If the topic is too broad or ambiguous, ask one clarifying question before proceeding. Don't over-interview — one question is usually enough. Examples of useful clarifications:
- Time range focus (recent 5 years vs. historical)
- Subfield (theoretical vs. applied, specific population)
- Geographic or clinical context

### Mode B: User asks for a recommendation

The user says something like "recommend a topic" or "最近有什麼值得研究的？". In this case:

1. Use WebSearch to find 3-5 recent scientific breakthroughs, policy changes, or major publications (within the last 6 months)
2. Frame each as an academic research question — not just "X happened" but "What is the mechanism / clinical landscape / efficacy of X?"
3. Present 2-3 of the best options with a one-line rationale for why each is timely
4. **Include the source URL** for each recommendation so the user can verify the news is real
5. Let the user pick, then proceed as Mode A

**Example recommendation framing:**
- News: "FDA approves new Alzheimer's drug lecanemab" ([source](https://www.nature.com/articles/...))
- Research question: "Anti-amyloid immunotherapy for Alzheimer's disease: clinical efficacy, biomarker outcomes, and long-term safety profile"

## Procedure

### 1. Create the session folder

Generate a session ID and create the folder structure:

```
Research/{session_id}_{topic_slug}/
```

- **session_id**: 8-character timestamp, format `YYYYMMDD` (e.g., `20260410`)
- **topic_slug**: lowercase, hyphens, max 40 chars, derived from the topic (e.g., `eeg-cognitive-training-elderly`)

Example: `Research/20260410_eeg-cognitive-training-elderly/`

### 2. Build the PICO framework

Parse the research topic and extract these components. PICO is a standard framework in evidence-based research — it forces you to be precise about what you're studying, which prevents scope drift later.

- **P (Population)**: Who is being studied? Be specific about demographics, conditions, age ranges. E.g., "Community-dwelling older adults aged 60+ with mild cognitive impairment"
- **I (Intervention)**: What is being done or studied? The treatment, exposure, or technology. E.g., "EEG-based neurofeedback cognitive training protocols"
- **C (Comparison)**: What is the control or alternative? E.g., "Sham neurofeedback, standard cognitive rehabilitation, or no intervention"
- **O (Outcome)**: What are the primary outcomes to measure? E.g., "Cognitive function (attention, working memory, executive function), EEG spectral changes, quality of life"

Additionally, note:
- **Setting**: Where does this research take place? (clinical, community, home-based, laboratory)
- **Timeframe focus**: What publication years are most relevant?

Think carefully about each component. The Population should be specific enough to be searchable but not so narrow that it excludes relevant work. The Comparison is often overlooked but critical — it shapes how you evaluate the intervention's effectiveness.

### 3. Generate 5 search queries

Each query targets a different angle of the topic. The goal is to cast a wide but strategic net — you want to find papers that a single obvious query would miss.

**Query strategy matrix:**

| Query # | Strategy | What it targets |
|---------|----------|----------------|
| Q1 | Core terms + Population | The most direct papers on this exact topic |
| Q2 | Synonyms + Alternative terminology | Papers using different terms for the same concept (include MeSH terms for biomedical topics) |
| Q3 | Mechanism + Theoretical basis | Papers explaining the "why" and "how" — underlying science |
| Q4 | Methodology + Study design | Papers with specific designs (RCT, meta-analysis) that demonstrate rigor |
| Q5 | Cross-disciplinary + Adjacent fields | Papers from neighboring fields that may have relevant methods or findings |

For each query, provide:
- The search string itself (optimized for academic databases — use Boolean operators, quotes for exact phrases)
- A one-line rationale explaining what this query is designed to catch

**Tips for good queries:**
- Use MeSH terms for biomedical topics (e.g., "Neurofeedback"[MeSH] OR "EEG biofeedback")
- Include both the technical term and the common term (e.g., "brain-computer interface" OR "BCI")
- One query should be deliberately broad to catch unexpected angles
- One query should be narrow and specific to find the most directly relevant work

### 4. Present for Checkpoint Review

After generating PICO and queries, present them clearly to the user in a bilingual format. This is **Checkpoint 1: 初始定向核准** — the user needs to:
- Verify the PICO components are accurate
- **Check technical term translations** — medical/scientific terms are easy to mistranslate (e.g., drug names, protocol names, disorder classifications). When in doubt, keep the English term and add a Chinese explanation in parentheses rather than risk a wrong translation.
- Add missing keywords or synonyms you missed
- Remove off-target dimensions
- Greenlight before proceeding to search

Present the output in conversation first, then save the files. The user may want to adjust before you write to disk.

## Output Files

Save two files to the session folder:

### `step0_session_config.json`

```json
{
  "session_id": "20260410",
  "topic": "EEG-based cognitive training for elderly",
  "topic_original": "EEG-based cognitive training for elderly",
  "topic_slug": "eeg-cognitive-training-elderly",
  "timestamp": "2026-04-10T14:30:00+08:00",
  "current_step": 1,
  "pico": {
    "population": "Community-dwelling older adults aged 60+ with mild cognitive impairment",
    "intervention": "EEG-based neurofeedback cognitive training protocols",
    "comparison": "Sham neurofeedback, standard cognitive rehabilitation, or no intervention",
    "outcome": "Cognitive function (attention, working memory, executive function), EEG spectral changes, quality of life",
    "setting": "Clinical or home-based",
    "timeframe": "2019-2026"
  },
  "source_urls": [],
  "queries": [
    {
      "id": "Q1",
      "strategy": "Core terms + Population",
      "query": "EEG neurofeedback cognitive training older adults mild cognitive impairment",
      "rationale": "Direct hit on the primary topic — finds papers studying exactly this intervention in this population"
    },
    {
      "id": "Q2",
      "strategy": "Synonyms + MeSH",
      "query": "\"Neurofeedback\"[MeSH] OR \"EEG biofeedback\" AND (elderly OR aged OR \"older adults\") AND cognition",
      "rationale": "Catches papers using alternative terminology — 'EEG biofeedback' is commonly used in clinical literature"
    },
    {
      "id": "Q3",
      "strategy": "Mechanism + Theory",
      "query": "brain plasticity neurofeedback aging EEG oscillations theta alpha",
      "rationale": "Finds the mechanistic basis — how neurofeedback modulates brain rhythms related to cognitive decline"
    },
    {
      "id": "Q4",
      "strategy": "Methodology + Design",
      "query": "randomized controlled trial neurofeedback cognitive elderly meta-analysis systematic review",
      "rationale": "Targets high-quality evidence — RCTs and meta-analyses that assess intervention efficacy"
    },
    {
      "id": "Q5",
      "strategy": "Cross-disciplinary",
      "query": "brain-computer interface cognitive rehabilitation aging non-invasive neuromodulation",
      "rationale": "Broadens to adjacent fields — BCI and neuromodulation research may have transferable methods"
    }
  ]
}
```

**Field notes:**
- `topic_original`: Preserve the user's exact input (important when the user types in Chinese — `topic` should be the English version for downstream processing, `topic_original` keeps what they actually typed)
- `source_urls`: Empty array for Mode A (user-provided topic). For Mode B (recommendation), populate with the WebSearch source URLs that informed the topic selection — this makes the provenance verifiable

### `step1_search_queries.md`

A human-readable version of the queries with rationale, formatted for easy review:

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
---

# Search Queries / 搜尋策略

> Topic / 研究主題: {topic}
> Generated / 產生日期: {date}

## PICO Framework

| Component | English | 繁體中文 |
|-----------|---------|---------|
| **P** Population | {population} | {population_zh} |
| **I** Intervention | {intervention} | {intervention_zh} |
| **C** Comparison | {comparison} | {comparison_zh} |
| **O** Outcome | {outcome} | {outcome_zh} |
| Setting | {setting} | {setting_zh} |
| Timeframe | {timeframe} | {timeframe} |

## Queries

### Q1: Core Terms + Population
**Query:** `{query}`
**Rationale / 策略說明:** {rationale} / {rationale_zh}

### Q2: Synonyms + MeSH Terms
**Query:** `{query}`
**Rationale / 策略說明:** {rationale} / {rationale_zh}

### Q3: Mechanism + Theoretical Basis
**Query:** `{query}`
**Rationale / 策略說明:** {rationale} / {rationale_zh}

### Q4: Methodology + Study Design
**Query:** `{query}`
**Rationale / 策略說明:** {rationale} / {rationale_zh}

### Q5: Cross-Disciplinary
**Query:** `{query}`
**Rationale / 策略說明:** {rationale} / {rationale_zh}

---

> **Checkpoint 1: 初始定向核准**
> Please review the PICO framework and search queries above.
> - Are the PICO components accurate? / PICO 各元素是否正確？
> - Any missing keywords or synonyms? / 有遺漏的關鍵字或同義詞嗎？
> - Any off-target dimensions to remove? / 有需要移除的偏離維度嗎？
> 
> When ready, greenlight to proceed to `/research-search`.
```

## After Saving

Tell the user:
1. The session folder has been created
2. Show the PICO table and queries inline for quick review
3. Explicitly ask them to review and greenlight (Checkpoint 1)
4. Suggest next step: `/research-search` (or the equivalent next pipeline step)

## Edge Cases

- **Non-biomedical topics**: PICO still works but relax the clinical framing. For engineering or CS topics, Population might be "systems" or "datasets", Intervention might be "proposed method", etc. Adapt the language naturally.
- **Very broad topics**: If the user says something like "AI in healthcare", ask which angle — diagnostic, therapeutic, operational, ethical? One clarifying question, not an interrogation.
- **Non-English topics**: The user may provide the topic in Chinese. Process it the same way — the PICO and queries should still be bilingual, with query strings in English (since academic databases primarily index English). Preserve the user's original input in `topic_original`.

## Bilingual Translation Safety

Translating technical and scientific terminology into Traditional Chinese requires extra care. Mistranslating a drug name or clinical term can be seriously misleading (e.g., confusing methylphenidate/哌醋甲酯 with methamphetamine/甲基苯丙胺).

**Rules of thumb:**
- For drug names, use the established Chinese pharmacological name. If unsure, keep the English name and add a brief Chinese description: e.g., "methylphenidate（一種用於治療ADHD的中樞神經興奮劑）"
- For well-known abbreviations (EEG, fMRI, BCI, RCT), keep the English abbreviation and add the Chinese full form on first mention: e.g., "EEG（腦電圖）"
- For methodology terms (e.g., "sham-controlled", "double-blind"), use the established academic Chinese term: "假刺激對照", "雙盲"
- When in doubt, English term + Chinese explanation in parentheses is always safer than a confident but wrong translation
