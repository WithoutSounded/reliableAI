---
name: research-search
description: "Run comprehensive literature search across multiple academic databases (Semantic Scholar, OpenAlex, PubMed, arXiv), deduplicate results, recover DOIs, perform snowball/citation network analysis, and produce a structured paper collection with source-specific IDs. This is Step 2 of the Research Agent pipeline. Use this skill when the user wants to search for papers, run a literature search, collect academic references, find related work, or do a deep search on a research topic. Trigger phrases include: 'search for papers on X', 'find literature about X', 'research-search', '/research-search', 'deep search', 'step 2', 'proceed to search'. Also trigger when the user has just completed research-init and wants to move to the search phase."
---

# Research Search — Step 2 of Research Agent Pipeline

You are executing a comprehensive, multi-source literature search. Your job is to take the PICO framework and search queries from Step 1, systematically query multiple academic databases, deduplicate the results, run a snowball expansion from top-cited seeds, build citation network metadata, and produce a single consolidated JSON file that all downstream pipeline steps will consume.

This step is the foundation of the entire literature review. The papers you find here determine the scope and quality of everything downstream — screening, SOTA synthesis, gap analysis, and the final manuscript. Missing a seminal paper at this stage means every subsequent analysis has a blind spot. That's why you search multiple sources with multiple queries: no single database has everything.

## Input

Read these files from the session folder (created by `research-init`):

1. **`step0_session_config.json`** — Contains PICO, session metadata, and the 5 search queries with rationale
2. **`step1_search_queries.md`** — Human-readable version (use for quick reference; the JSON is authoritative)

If the session folder doesn't exist or these files are missing, tell the user to run `research-init` first.

## Procedure Overview

The search proceeds in 6 phases:

1. **Multi-source search** — Query 3-4 academic APIs with all 5 queries
2. **Deduplication + DOI recovery** — Merge records, then recover missing DOIs
3. **Snowball expansion** — Fetch references of top-cited seed papers
4. **Citation network analysis** — Map internal citations, identify hubs and clusters
5. **Save output** — Write `step2_raw_papers.json` + `step2_search_summary.md`
6. **Report** — Present bilingual summary to user

Target yield: **30-60 unique papers** after deduplication. This is a realistic expectation from 5 queries across 3-4 sources. If yield is much lower, broaden queries; if much higher, that's fine — screening in Step 3 will filter.

---

## Phase 1: Multi-Source Search

For each of the 5 queries from `step0_session_config.json`, search these sources. Not every source is relevant for every topic — adapt based on the field.

### Source Selection by Field

| Source | When to use | Strengths |
|--------|-------------|-----------|
| **Semantic Scholar** | Always | Best metadata, citation data, free API, structured JSON |
| **OpenAlex** | Always | Fully open, excellent for citation network traversal |
| **PubMed** | Biomedical / clinical / neuroscience topics | Gold standard for medical literature, MeSH indexing |
| **arXiv** | CS, physics, math, engineering, AI/ML topics | Preprints, cutting-edge work before peer review |

For biomedical topics, use all 4. For CS/engineering, skip PubMed and focus on Semantic Scholar + OpenAlex + arXiv. Use your judgment based on the PICO.

### How to Search Each Source

Detailed API endpoint documentation is in `references/api_endpoints.md`. Read that file before making your first API call — it contains URL templates, parameter formats, and response parsing guidance for each source.

**General approach for each source:**
1. Construct the API URL using the query string
2. Fetch via WebFetch
3. Parse the JSON/XML response
4. Extract the standard metadata fields (see "Paper Metadata Schema" below)
5. **Populate source-specific IDs** from the response — this is critical. Each API returns its own ID for the paper. Capture it:
   - Semantic Scholar → `semantic_scholar_id` (from `paperId`)
   - OpenAlex → `openalex_id` (from `id`, extract the W-number)
   - PubMed → `pubmed_id` (from `PMID`)
   - arXiv → `arxiv_id` (from entry `id`)
6. Tag each paper with which source it came from

### Search Execution Strategy

You have 5 queries and 3-4 sources, which means 15-20 API calls. To be efficient:

- **Batch by source, not by query.** Do all Semantic Scholar calls together, then all OpenAlex calls, etc. This helps you notice if a source is down or rate-limiting.
- **Apply year filters.** Use the timeframe from `session_config.json` (typically 5-7 years). Each API has its own year filter parameter — see `references/api_endpoints.md`.
- **Request 20-30 results per query per source.** More than that gives diminishing returns at this stage. The snowball phase will catch important missed papers.
- **If an API call fails**, retry once. If it fails again, note it in your search log and move on. Don't let one flaky API block the entire search.

### Paper Metadata Schema

For every paper found, extract these fields into a normalized structure:

```json
{
  "id": "paper_001",
  "title": "Full paper title",
  "authors": ["First Author", "Second Author"],
  "year": 2024,
  "journal": "Journal or venue name",
  "doi": "10.xxxx/xxxxx",
  "url": "https://...",
  "abstract": "Full abstract text",
  "citation_count": 42,
  "sources_found_in": ["semantic_scholar", "openalex"],
  "semantic_scholar_id": "abc123",
  "openalex_id": "W1234567890",
  "pubmed_id": "12345678",
  "arxiv_id": "2401.12345",
  "references": [],
  "cited_by": [],
  "is_seed_paper": false,
  "found_via": "Q1"
}
```

**Field notes:**
- `id`: Sequential ID you assign (`paper_001`, `paper_002`, ...) — stable identifier within this session
- `sources_found_in`: Track every source that returned this paper (populated during dedup merge)
- `references` and `cited_by`: Populated during citation network phase (Phase 4)
- `is_seed_paper`: Set to `true` for papers used as snowball seeds
- `found_via`: Which query first found this paper (e.g., "Q1", "Q3", "snowball")
- Source-specific IDs: Keep all of them — downstream steps may need them to fetch full text

If a field is unavailable from a source, set it to `null` rather than omitting it.

---

## Phase 2: Deduplication

After collecting papers from all sources, deduplicate aggressively. The same paper will appear in multiple sources — that's expected and even desirable (it confirms the paper is well-indexed).

### Dedup Strategy

1. **Primary key: DOI match.** Normalize DOIs (lowercase, strip `https://doi.org/` prefix). Two records with the same DOI are the same paper — merge them.

2. **Fallback: Fuzzy title match.** For papers without DOIs (preprints, some conference papers):
   - Normalize: lowercase, strip punctuation, collapse whitespace
   - Compare: if two normalized titles share >85% of their words AND have the same first author last name AND are published within ±1 year, treat as duplicates
   - When in doubt, keep both — false negatives (missing a duplicate) are less harmful than false positives (merging different papers)

3. **Merge logic:** When merging duplicate records:
   - Keep the richest metadata (prefer Semantic Scholar for abstracts, OpenAlex for citation counts)
   - Union all `sources_found_in`
   - Keep all source-specific IDs
   - Prefer the version with a DOI

### DOI Recovery Pass

After merging duplicates, many papers (especially arXiv preprints and conference papers) will still lack DOIs. DOIs are critical for downstream steps — full-text retrieval, reference export, and dedup against future searches all depend on them. Run a recovery pass:

1. For each paper missing a DOI, look it up via Semantic Scholar by title or arXiv ID:
   ```
   GET https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=externalIds
   ```
   or search by title if no arXiv ID. The `externalIds.DOI` field often has the DOI even when the original source didn't.

2. For papers found only via arXiv, also check if OpenAlex has the DOI — many arXiv papers get DOIs once published at a venue, and OpenAlex tracks this.

3. Target: **≥70% of papers should have a DOI** after this pass. CS/arXiv-heavy collections may settle around 60%, which is acceptable.

### Abstract Fidelity

Use the actual abstract text returned by the API — copy it verbatim. Do not paraphrase or summarize the abstract in your own words. If a source returns a truncated abstract, prefer the Semantic Scholar version (which usually has the full text). If no source returns the abstract, set it to `null`.

### Post-Dedup Check

After deduplication and DOI recovery, report:
- Total papers found (before dedup)
- Unique papers (after dedup)
- DOI coverage rate (percentage of papers with DOIs)
- Papers per source
- Papers per query
- Overlap rate between sources

If unique count is below 20, consider broadening the weakest-performing queries and running an additional search round.

---

## Phase 3: Snowball Expansion

Snowballing catches important papers that your keyword queries missed — especially foundational work that uses different terminology, or very recent papers not yet well-indexed.

### Identify Seed Papers

From the deduplicated collection, pick the **top 5 papers by citation count** as seeds. These are the most-cited papers in your collection — their reference lists are likely to contain other important work.

Mark these papers with `"is_seed_paper": true`.

### Fetch References

For each seed paper, use the Semantic Scholar API to fetch its reference list:
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,authors,year,abstract,externalIds,citationCount&limit=50
```

(See `references/api_endpoints.md` for details.)

### Filter and Add

From the snowball results, add papers that:
1. Fall within the session's timeframe
2. Have an abstract that appears relevant to the PICO (use your judgment — read the title and abstract)
3. Are not already in the collection (check DOI/title dedup)

Mark snowball additions with `"found_via": "snowball"`.

Realistically, snowballing adds 5-15 papers. Don't chase every reference — focus on the ones that look directly relevant.

---

## Phase 4: Citation Network Analysis

This phase adds relationship data that makes the paper collection much more useful for downstream synthesis (SOTA review, gap analysis).

### 4a. Map Internal Citations

For each paper in the final collection, check which other papers in the collection it cites or is cited by. You already have reference data from Semantic Scholar — cross-reference against your paper IDs.

Populate the `references` and `cited_by` fields with internal paper IDs:
```json
{
  "id": "paper_003",
  "references": ["paper_001", "paper_012"],
  "cited_by": ["paper_007", "paper_015"]
}
```

Only include references/citations that are **within the collection** — we don't need external citation data.

### 4b. Identify Hub Papers

A hub paper is one that many other papers in the collection cite. Calculate `in_degree` (number of papers in the collection that cite this paper) for each paper. Papers with in_degree >= 3 are hubs.

Add a `citation_network` field to each paper:
```json
{
  "citation_network": {
    "in_degree": 5,
    "out_degree": 2,
    "is_hub": true,
    "cluster": "cluster_A"
  }
}
```

### 4c. Detect Citation Clusters

Group papers by citation connectivity — papers that heavily cite each other likely represent the same research camp or school of thought. A simple approach:

1. Build an adjacency list from the internal citations
2. Identify connected components or tightly-connected subgroups
3. Label clusters descriptively based on common themes (e.g., "transformer_denoising", "traditional_signal_processing")

You don't need a formal graph algorithm — use your understanding of the papers' topics and their citation relationships to identify 2-4 clusters. Label them with short descriptive names.

---

## Phase 5: Save Output

### `step2_raw_papers.json`

Save the final deduplicated, snowball-expanded, citation-network-annotated collection:

```json
{
  "session_id": "20260410",
  "topic": "EEG-based cognitive training for elderly",
  "search_timestamp": "2026-04-10T15:30:00+08:00",
  "search_summary": {
    "total_raw_results": 142,
    "after_dedup": 58,
    "snowball_additions": 12,
    "final_count": 70,
    "sources": {
      "semantic_scholar": 45,
      "openalex": 52,
      "pubmed": 38,
      "arxiv": 7
    },
    "queries": {
      "Q1": 18,
      "Q2": 15,
      "Q3": 12,
      "Q4": 14,
      "Q5": 11,
      "snowball": 12
    },
    "doi_coverage": "45/70 (64%)",
    "hub_papers": ["paper_003", "paper_017"],
    "clusters": [
      {"name": "cluster_name", "paper_ids": ["paper_001", "paper_002"], "theme": "Brief description"}
    ]
  },
  "papers": [
    {
      "id": "paper_001",
      "title": "...",
      "authors": ["..."],
      "year": 2024,
      "journal": "...",
      "doi": "...",
      "url": "...",
      "abstract": "...",
      "citation_count": 42,
      "sources_found_in": ["semantic_scholar", "openalex"],
      "semantic_scholar_id": "...",
      "openalex_id": "...",
      "pubmed_id": null,
      "arxiv_id": null,
      "references": ["paper_003", "paper_012"],
      "cited_by": ["paper_007"],
      "is_seed_paper": true,
      "found_via": "Q1",
      "citation_network": {
        "in_degree": 5,
        "out_degree": 2,
        "is_hub": true,
        "cluster": "cluster_A"
      }
    }
  ]
}
```

### `step2_search_summary.md`

Also save a human-readable bilingual summary file. This file serves two purposes: it's a quick reference for the user, and it's a checkpoint artifact that documents exactly what was searched and found.

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 2
---

# Search Summary / 搜尋摘要

> Topic / 研究主題: {topic}
> Sources / 資料來源: {list of sources used}
> Date / 搜尋日期: {date}

## Results / 搜尋結果

| Query | Strategy / 策略 | Raw | Unique / 唯一 |
|-------|----------|-----|--------|
| Q1 | {strategy} / {strategy_zh} | {raw} | {unique} |
| ... | ... | ... | ... |
| Snowball | Top-cited references / 高引用文獻延伸 | — | {n} |
| **Total / 總計** | | **{total_raw}** | **{final_count}** |

DOI coverage / DOI 覆蓋率: {n}/{total} ({pct}%)
Source overlap rate / 來源重疊率: {pct}%

## Hub Papers / 核心文獻

1. "{title}" ({first_author}, {year}) — in_degree: {n} — {one_line_zh}
2. ...

## Citation Clusters / 引用聚類

- **{cluster_slug}** ({n} papers) — {description_en} / {description_zh}
- ...

## Yield Assessment / 產量評估

{assessment_en}
{assessment_zh}

---

Files / 檔案: `step2_raw_papers.json`
Next step / 下一步: `/research-screen`
```

### After Saving

Update `step0_session_config.json`: set `"current_step": 2`.

Then report to the user (this should match the content of `step2_search_summary.md`):

1. **Search summary table** — papers per query, per source, overlap rate
2. **Hub papers** — list the top-cited papers with title and citation count
3. **Citation clusters** — brief description of each cluster detected
4. **Yield assessment** — is the collection large enough? Any gaps?
5. **Suggest next step:** `research-screen` for paper screening

**Example summary output:**

```
Search complete! / 搜尋完成！

## Summary / 搜尋摘要

| Query | Strategy | Raw | Unique |
|-------|----------|-----|--------|
| Q1 | Core terms + Population | 34 | 18 |
| Q2 | Synonyms + MeSH | 28 | 15 |
| Q3 | Mechanism + Theory | 25 | 12 |
| Q4 | Methodology + Design | 30 | 14 |
| Q5 | Cross-disciplinary | 25 | 11 |
| Snowball | Top-cited references | — | 12 |
|---------|----------|-----|--------|
| **Total** | | **142** | **70** (after dedup) |

## Hub Papers / 核心文獻
1. "Paper Title A" (2023) — cited by 5 papers in collection
2. "Paper Title B" (2022) — cited by 4 papers in collection

## Citation Clusters / 引用聚類
- **Cluster A: transformer_denoising** (12 papers) — Deep learning approaches to EEG artifact removal
- **Cluster B: traditional_methods** (8 papers) — Classical signal processing techniques

Files saved to: Research/{session_id}_{topic_slug}/step2_raw_papers.json
Next step: /research-screen
```

---

## Edge Cases

- **Non-biomedical topics**: Skip PubMed. Focus on Semantic Scholar + OpenAlex + arXiv. The PICO adaptation from Step 1 should already frame the topic in searchable terms.
- **Very niche topics (low yield)**: If you get fewer than 15 unique papers after all queries, try:
  1. Broader synonym queries
  2. Extending the timeframe
  3. Searching with just the key concept (dropping population/outcome constraints)
  4. Report the low yield to the user — the topic may genuinely be underexplored (which is useful information for gap analysis)
- **API rate limiting**: Semantic Scholar allows ~100 requests/5 minutes without an API key. OpenAlex is generous with rate limits. PubMed E-utilities allow 3 requests/second without API key. If rate-limited, add brief pauses between calls.
- **Missing abstracts**: Some older papers or conference proceedings lack abstracts in APIs. Set abstract to `null` — the screening step will handle this (lower confidence scoring).
- **Non-English papers**: Keep them in the collection if found. Tag with a `"language"` field if detectable. Downstream steps can filter if needed.

## Output Files Checklist

Before reporting to the user, verify you have saved these files to the session folder:

1. **`step2_raw_papers.json`** — The main output (all papers with metadata, citation network)
2. **`step2_search_summary.md`** — Human-readable bilingual summary (must contain both English and Traditional Chinese)
3. **`step0_session_config.json`** — Updated with `current_step: 2`

## Bilingual Communication

Both `step2_search_summary.md` and your conversation output must be bilingual (English + Traditional Chinese), following the same conventions as `research-init`:
- Keep technical terms in English with Chinese explanations in parentheses on first mention
- Hub papers: list in English with brief Chinese annotation
- Cluster names: English slug + Chinese description
- Table headers: bilingual (e.g., "Strategy / 策略", "Unique / 唯一")
- Yield assessment: one paragraph English, one paragraph Chinese
