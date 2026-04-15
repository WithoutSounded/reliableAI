---
name: research-fulltext
description: "Step 5 of the Research Agent pipeline: fetch full-text academic papers from multiple open-access sources (arXiv HTML/PDF, PubMed Central, OA journals, preprint servers), convert to structured markdown, produce bilingual English–Chinese reading notes with Obsidian callout blocks, and log all access results. Automatically detects when WebFetch summarizes long papers and falls back to PDF extraction for complete content. Use this skill whenever the user wants to get paper full text, download PDFs, convert papers to markdown, create bilingual paper notes, or says 'next step' after research-export (Step 4). Trigger on: 'get full text', 'download papers', 'fetch PDFs', '取得全文', '下載論文', '抓全文', '翻譯論文', 'read the papers', 'get the actual papers', or any mention of obtaining paper content beyond abstracts — even if the user just says 'I need to read these papers' or '我要看論文內容'."
---

# Research Fulltext — Step 5 of Research Agent Pipeline

You are acquiring the full text of shortlisted academic papers and converting them to markdown. This step bridges the gap between metadata-level screening (Steps 1–4, which work from titles and abstracts) and deep synthesis (Steps 6–9, which need the actual paper content). Every full text you successfully retrieve improves the quality of the downstream SOTA review, gap analysis, and manuscript.

Papers behind paywalls are a reality. Your job is to exhaust all legitimate open-access routes before marking a paper as abstract-only. The access hierarchy below is ordered by reliability and likelihood of success — follow it top-down for each paper.

## Input

Read these files from the session folder:

1. **`step3_shortlist.json`** — Included papers with full metadata (DOI, arXiv ID, PMC ID, URLs, screening scores). This is the master list of papers to process.
2. **`step4_citation_keys.md`** — The citation key lookup table mapping each paper to its `AuthorYear` key. You need this to name the output files correctly.

If either file is missing, tell the user to run the earlier pipeline steps first (`/research-screen` then `/research-export`).

## Procedure

### 1. Build the Work Queue

Create the output directory if it doesn't exist: `step5_full_text/` inside the session folder.

Read `step3_shortlist.json` and sort papers by composite score descending — highest-scored papers are processed first. This way, if the user stops the process partway through (or you hit rate limits), the most important papers are already done.

For each paper, look up its citation key from `step4_citation_keys.md`. Build a work queue:

```
[
  { paper_id, citation_key, doi, arxiv_id, pmc_id, url, composite_score }
]
```

Before starting, check if `step5_full_text/` already has files from a previous partial run. Skip papers that already have a `{citation_key}.md` file with `access_level` other than `abstract-only` — don't re-download what you already have. Tell the user how many are already done and how many remain.

**Pacing**: Process papers one at a time, in score order. After every 5 papers, give the user a brief progress update (e.g., "5/20 done — 3 full-text, 2 abstract-only"). This keeps them informed and gives them a chance to pause if needed.

### 2. Access Each Paper (Five-Level Hierarchy)

For each paper in the queue, try these sources in order. Stop at the first success.

#### Level 1: arXiv (most reliable)

If the paper has an `arxiv_id`, try the **HTML version first** (better extraction), then fall back to PDF:

**Step A — arXiv HTML** (preferred):
1. Fetch `https://arxiv.org/html/{arxiv_id}` via WebFetch with a prompt that explicitly asks for the **complete, verbatim** paper text — all sections, tables, equations, and figure captions. (See "WebFetch extraction quality" below for prompt guidance.)
2. If WebFetch returns a 404, the paper has no HTML version — go to Step B.
3. If WebFetch succeeds, check extraction quality before saving (see quality check below).
- Access level: `full-text-html`

**Step B — arXiv PDF** (fallback):
1. Download: `curl -L -o /tmp/{citation_key}.pdf "https://arxiv.org/pdf/{arxiv_id}"`
2. Convert to text: `/opt/homebrew/bin/pdftotext -layout /tmp/{citation_key}.pdf /tmp/{citation_key}.txt` (on macOS with Homebrew poppler). If `pdftotext` is unavailable, try the Read tool on the PDF directly.
3. Read the resulting text file and reformat into clean markdown with section headings, tables, etc.
4. This takes more manual effort but works when HTML is not available.
- Access level: `full-text-pdf`

arXiv is always free and has no rate limits for individual downloads, so this is the most reliable source. Many CS, physics, and quantitative biology papers are here.

**Exception**: If the paper also has a DOI from a known open-access publisher (Level 3 list), try the published version first — it's the peer-reviewed final form. Use arXiv only as fallback if the published version fetch fails.

#### WebFetch Extraction Quality

WebFetch uses a small model internally to process fetched content. For long papers (especially survey/SLR papers with 30+ pages), this model may **summarize or condense** the content instead of returning it verbatim. This is the single biggest quality risk in the pipeline.

**Prompt strategy**: Always instruct WebFetch to extract complete, verbatim text. Include specifics:
> "Extract the COMPLETE full text of this academic paper. Return ALL sections verbatim: Abstract, Introduction, every section and subsection, Results, Discussion, Conclusion, and References. Do NOT summarize or condense. Preserve all section headings, tables, figure captions, equations, and detailed content."

**Quality check after extraction**: Before saving, verify:
1. **Section count**: A typical research paper has 5–8 major sections. If you only see 2–3 (e.g., just Abstract + Key Findings + Conclusion), the content was likely summarized.
2. **Line count heuristic**: A full paper typically yields 150–500 lines of markdown. If the extraction is under 100 lines for a non-short paper, it's suspicious.
3. **Abrupt endings**: Check if the text ends mid-section or lacks a proper Conclusion/References section.

**If you detect summarization — automatic fallback (hybrid strategy)**:

WebFetch summarization is the single biggest quality risk in the pipeline. Don't just flag it — actively recover the full content using this fallback chain:

**Fallback A — PDF → pdftotext (preferred, deterministic)**:
1. Download the PDF: `curl -L -o /tmp/{citation_key}.pdf "{pdf_url}"`
2. Convert: `/opt/homebrew/bin/pdftotext -layout /tmp/{citation_key}.pdf /tmp/{citation_key}.txt`
   - On Linux: `pdftotext -layout /tmp/{citation_key}.pdf /tmp/{citation_key}.txt`
3. Read the `.txt` file and reformat into clean markdown:
   - Identify section headings (lines matching patterns like `1 Introduction`, `2.1 Background`, `## Methods`)
   - Reconstruct tables (pdftotext preserves column alignment via spaces)
   - Strip page headers/footers, author blocks, and page numbers
   - This is labor-intensive but the content is 100% complete — pdftotext never summarizes
4. Access level: `full-text-pdf`

This approach works because pdftotext is a deterministic text extraction tool — it outputs every character from the PDF without any AI processing, so content length is never a problem.

**Fallback B — Chunked WebFetch (when PDF is unavailable)**:
If the paper has no downloadable PDF (rare, but possible for some PMC-only or publisher HTML-only papers):
1. First, do a quick WebFetch to get the table of contents / section structure:
   `"List only the section headings of this paper (e.g., Abstract, 1. Introduction, 2. Methods...). Just the headings, nothing else."`
2. Then fetch each major section separately with targeted prompts:
   `"Extract ONLY section 3 (Methods) from this paper. Return the complete, verbatim text of this section including all subsections."`
3. Concatenate the sections into the final markdown file
4. This typically needs 3-5 WebFetch calls for a standard paper, or 6-10 for a very long survey

**When to use which fallback:**
- Paper has a PDF URL (arXiv, publisher, preprint server) → Fallback A
- Paper is HTML-only (some PMC articles, some OA publishers) → Fallback B
- Both available → Fallback A (simpler, more reliable)

**After fallback recovery:**
- Update the frontmatter: change `extraction_quality` from `"summarized"` to `"complete"` (or remove the field)
- Update the access log to note the recovery method
- If both fallbacks fail, keep the summarized version but mark it clearly:
  - `extraction_quality: "summarized"` stays in frontmatter
  - Note in `_access_log.md` with ⚠️ flag
  - The downstream SOTA step can still use it but should weight it lower in synthesis

#### Level 2: PubMed Central (PMC)

Many biomedical papers are freely available in PMC even when the publisher version is paywalled (due to NIH public access policy, funder mandates, etc.). The shortlist may or may not include a `pmc_id` field — often it doesn't, so you need to check.

**How to find the PMC ID:**
1. If the paper already has a `pmc_id` in the shortlist → use it directly
2. If the paper has a `pubmed_id` or `doi` but no `pmc_id` → look up PMC availability via the NCBI ID Converter API:
   ```
   https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pubmed_id_or_doi}&format=json
   ```
   Fetch this URL via WebFetch. The response JSON contains a `pmcid` field if the paper is in PMC.
3. If no PubMed ID or DOI → skip this level

**Once you have a PMC ID:**
- Fetch the full HTML from `https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/` via WebFetch
- Extract the article body — PMC pages have structured HTML with clear article sections
- Convert to markdown, preserving section headings (Introduction, Methods, Results, Discussion)
- Access level: `full-text-html`

PMC is the free full-text archive for biomedical literature. This level is especially important because many papers that look paywalled actually have a free PMC copy. Always check before giving up on a biomedical paper.

#### Level 3: Open Access Journals

If the paper's DOI or URL points to a known open-access publisher:
- **PLOS** (`journals.plos.org`) — always open access
- **Frontiers** (`frontiersin.org`) — always open access
- **MDPI** (`mdpi.com`) — always open access
- **Nature Communications** (`nature.com/ncomms`) — open access
- **Scientific Reports** (`nature.com/srep`) — open access
- **BMC journals** (`biomedcentral.com`) — open access
- **eLife** (`elifesciences.org`) — open access
- **PeerJ** (`peerj.com`) — open access

Try fetching the full page via WebFetch using the DOI URL (`https://doi.org/{doi}`). If the page contains full article text (not just abstract + paywall), extract and convert to markdown.

How to tell if you got the full text vs. a paywall stub: full-text pages typically contain sections like "Introduction", "Methods", "Results", "Discussion" with substantial content (multiple paragraphs each). A paywall page usually shows only the abstract, followed by login/purchase prompts.

Access level: `full-text-html` or `full-text-pdf` depending on what you get.

#### Level 4: Preprint Servers

Check if the paper (or a preprint version) is available on:
- **bioRxiv** (`biorxiv.org`) — biology preprints
- **medRxiv** (`medrxiv.org`) — medical preprints
- **SSRN** (`ssrn.com`) — social science / interdisciplinary

If the paper's URL or metadata mentions these, try WebFetch on the URL. bioRxiv and medRxiv provide full-text HTML for all preprints.

If none of the metadata points to a preprint server, try a WebSearch for `"{paper title}" site:biorxiv.org OR site:medrxiv.org OR site:arxiv.org` — authors sometimes post preprints even when the published version is paywalled.

Access level: `full-text-html` or `full-text-pdf`

#### Level 5: Abstract Only (fallback)

If all the above fail, the paper is likely behind a paywall. Don't attempt to bypass paywalls or access unauthorized copies.

Record in the access log:
- The DOI (so the user can try via institutional access)
- The publisher URL
- A suggested action: "Try via institutional proxy: `https://doi.org/{doi}`"

Access level: `abstract-only`

For abstract-only papers, create a minimal `{citation_key}.md` that contains the structured abstract from the shortlist metadata, clearly marked as abstract-only. This way downstream steps always have a file to reference, even if it's limited.

### 3. Convert to Markdown

Regardless of source, each paper's markdown file should follow a consistent structure:

```markdown
---
citation_key: "{citation_key}"
title: "{title}"
authors: "{authors}"
year: {year}
doi: "{doi}"
source: "{arXiv (arxiv_id) / PMC (pmcid) / publisher / preprint}"
access_level: "{full-text-pdf / full-text-html / abstract-only}"
retrieved_date: "{YYYY-MM-DD}"
arxiv_id: "{arxiv_id, if applicable}"
extraction_quality: "{complete / summarized, omit if complete}"
---

# {title}

## Abstract

{abstract}

## {Section headings from the paper, preserved as-is}

{full text content here, with section headings preserved}
```

Note: The `extraction_quality: "summarized"` field should only appear when WebFetch or another tool returned a condensed version of the paper. Most papers won't need this field.

**Conversion guidelines:**
- Preserve the paper's section structure (Abstract, Introduction, Methods, Results, Discussion, Conclusion, References)
- Keep tables as markdown tables where feasible; for complex tables, describe the structure
- For figures, note their captions and descriptions (e.g., `> **Figure 1**: {caption}`) — you can't embed images in markdown, but the caption text is valuable context for synthesis
- Strip navigation elements, ads, sidebar content, and other page chrome — keep only the article body
- For PDF conversions, the `/pdf` skill handles the heavy lifting; you just need to add the frontmatter and clean up any conversion artifacts
- Mathematical equations: preserve in LaTeX notation where possible (`$...$` for inline, `$$...$$` for display)
- Reference lists at the end of papers: include them — they're useful for citation network verification in later steps

### 4. Bilingual Translation (雙語翻譯)

After saving the English full-text markdown, create a bilingual reading version for each paper using the `bilingual-translation` skill format. This step transforms the academic paper into an Obsidian-friendly bilingual note with callout blocks.

**Output file**: `step5_full_text/{citation_key}_zh.md` (separate from the English-only `{citation_key}.md`)

**Why two files**: The English-only version is consumed by downstream pipeline steps (SOTA review, gap analysis, manuscript writing) which need clean text for synthesis. The bilingual version is for the researcher's reading and comprehension.

**Format**: Follow the `bilingual-translation` skill's callout structure:

```markdown
# {title} | {中文標題}

> [!abstract] 重點摘要
> - 重點一
> - 重點二
> - ...

---

## Abstract | 摘要

> [!quote] Original
> {English abstract paragraph}

> [!note] 翻譯
> {Traditional Chinese translation}

---

## Introduction | 引言

> [!quote] Original
> {English paragraph}

> [!note] 翻譯
> {Chinese translation}

---
...
```

**Translation guidelines:**
- Translate paragraph by paragraph — nothing omitted, nothing summarized
- Section headings are bilingual: `## Methods | 方法`
- Technical terms: first occurrence includes English in parentheses, e.g., 自動程式修復（Automated Program Repair）
- Tables: reproduce in both the Original and 翻譯 callouts
- Citations like `[1]`, `(Smith et al., 2023)` stay in English in both callouts
- LaTeX equations stay as-is in both callouts
- Maintain academic register in Chinese — formal, precise, but natural

**For abstract-only papers**: Still create a bilingual version of whatever content is available (abstract + metadata).

**For summarized papers** (`extraction_quality: "summarized"`): Translate what you have, but note in the summary that this is a condensed version.

**Pacing**: Translation is token-intensive. Process one paper at a time. For very long papers (400+ lines), work section by section, appending to the output file.

### 5. Handle Errors Gracefully

Things will go wrong. Some common issues:

- **WebFetch timeout or failure**: Note it in the access log and try the next level. Don't retry the same URL more than once.
- **PDF too large or corrupted**: Note the DOI and file size in the access log. Suggest the user download manually.
- **Rate limiting**: If you get HTTP 429 or similar from a source, stop hitting that source for remaining papers. Note which papers were affected and which source was rate-limited.
- **Unexpected format**: If a page returns something neither PDF-like nor HTML-article-like (e.g., a login redirect, a CAPTCHA page), skip it and move to the next level.

The goal is resilience — get as many papers as possible, log everything, and make it easy for the user to manually fill in the gaps.

### 6. Generate the Access Log

After processing all papers, create `_access_log.md` summarizing the results. This is the user's action item list for papers that need manual retrieval.

## Output

### `step5_full_text/{citation_key}.md`

One file per paper, using the citation key as the filename. Contains the converted full text with YAML frontmatter (see format in Section 3 above).

For abstract-only papers, the file is shorter but still exists:

```markdown
---
citation_key: "{citation_key}"
title: "{title}"
authors: "{authors}"
year: {year}
doi: "{doi}"
source: "abstract-only"
access_level: "abstract-only"
retrieved_date: "{YYYY-MM-DD}"
---

# {title}

**Authors**: {authors}
**Year**: {year}
**DOI**: {doi}

> **Note / 備註**: Full text not available through open access. Abstract included below from screening metadata. Try institutional access: `https://doi.org/{doi}`
> 全文無法透過開放取用管道取得。以下為篩選階段的摘要。請嘗試機構存取：`https://doi.org/{doi}`

---

## Abstract

{abstract from shortlist metadata}
```

### `step5_full_text/{citation_key}_zh.md`

Bilingual reading version of each paper, using Obsidian callout blocks. Created for every paper that has content beyond abstract-only. Format follows the `bilingual-translation` skill conventions (see Step 4 above).

### `step5_full_text/_access_log.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 5
---

# Full Text Access Log / 全文取得紀錄

> Topic / 研究主題: {topic}
> Total papers / 論文總數: {N}
> Date / 處理日期: {date}

## Summary / 摘要

| Access Level / 取得層級 | Count / 數量 | Percentage / 百分比 |
|------------------------|-------------|-------------------|
| full-text-pdf | {n} | {pct}% |
| full-text-html | {n} | {pct}% |
| abstract-only | {n} | {pct}% |

Full-text retrieval rate / 全文取得率: **{pct}%** ({n}/{N} papers)

## Successfully Retrieved / 成功取得

| # | Citation Key / 引用鍵 | Title / 標題 | Source / 來源 | Access Level / 層級 |
|---|---------------------|-------------|--------------|-------------------|
| 1 | `{citation_key}` | {short_title} | {source} | {access_level} |
| ... |

## Abstract Only — Action Required / 僅有摘要 — 需人工處理

> These papers could not be accessed through open channels. If you have institutional access, you can retrieve them via the DOI links below.
> 以下論文無法透過開放管道取得。如有機構存取權限，可透過下方 DOI 連結取得。

| # | Citation Key / 引用鍵 | Title / 標題 | DOI | Suggested Action / 建議動作 |
|---|---------------------|-------------|-----|--------------------------|
| 1 | `{citation_key}` | {short_title} | [{doi}](https://doi.org/{doi}) | Try institutional proxy / 嘗試機構代理 |
| ... |

## Access Attempts Detail / 取得嘗試詳情

For each paper, what was tried and what happened:

### {citation_key}: {short_title}
- **arXiv**: {tried? result}
- **PMC**: {tried? result}
- **OA Journal**: {tried? result}
- **Preprint**: {tried? result}
- **Final status**: {access_level}

---

Files / 檔案: `step5_full_text/` directory with {N} paper files + this access log
Next step / 下一步: `/research-sota`
```

## After Saving

Update `step0_session_config.json`: set `"current_step": 5`.

Then present to the user:

1. **Summary** — total papers processed, retrieval rate by access level (full-text-pdf / full-text-html / abstract-only)
2. **Top retrievals** — show 2-3 successfully retrieved papers with their source
3. **Action items** — list the abstract-only papers with DOI links for manual retrieval
4. **Suggest next step:** `/research-sota` (but note which papers are abstract-only, as this affects synthesis depth)

## Edge Cases

- **Papers with both arXiv ID and published DOI**: Handled by the Level 1 exception — try the published OA version first, arXiv as fallback. Note in the access log which version was retrieved.
- **Multiple versions on arXiv**: Use the latest version (arXiv URLs without version suffix default to the latest, which is the right behavior).
- **Supplementary materials**: Focus on the main paper text. Don't attempt to retrieve supplementary files, appendices hosted separately, or supporting data. Note their existence if mentioned.
- **Very long papers (>50 pages)**: These are usually reviews, textbooks, or theses. Convert the full text but add a note in the frontmatter: `long_paper: true`. Downstream synthesis steps can decide how to handle them.
- **Non-English papers**: If the full text is in a non-English language, still retrieve and convert it. Note the language in the frontmatter: `language: "{language}"`. Downstream steps can use translation if needed.
- **Retracted papers**: If you encounter a retraction notice during retrieval, flag it prominently in both the paper's markdown and the access log. The user should decide whether to keep it in the analysis.
- **Partial HTML extraction**: Sometimes WebFetch captures only part of an article (e.g., the introduction loads but later sections are lazy-loaded). If the extracted text seems truncated (ends abruptly mid-section or only has 1-2 sections), note it as `access_level: "partial-text-html"` and flag it in the access log for human verification.
- **WebFetch summarization of long papers**: Survey papers, SLRs, and other very long papers (30+ pages) are especially vulnerable to being condensed by WebFetch's internal model. Add `extraction_quality: "summarized"` to the frontmatter. If the paper is high-priority, re-try via the PDF fallback path.
- **arXiv HTML 404**: Not all arXiv papers have HTML versions (older papers, certain formats). This is expected — fall back to the PDF path described in Level 1 Step B.
- **Duplicate files from previous runs**: Check before writing — if a `{citation_key}.md` already exists and was from a successful full-text retrieval, don't overwrite it. Only overwrite if the existing file is abstract-only and you now have full text.

## Verification Checklist

Before finalizing, verify:

1. **File count**: Number of `.md` files in `step5_full_text/` (excluding `_access_log.md`) equals the number of papers in `step3_shortlist.json`
2. **Naming consistency**: Every filename matches a citation key from `step4_citation_keys.md` exactly
3. **Frontmatter completeness**: Every file has `citation_key`, `title`, `access_level`, and `retrieved_date` in the YAML frontmatter
4. **Access log completeness**: Every paper from the shortlist appears in the access log, either under "Successfully Retrieved" or "Abstract Only"
5. **No empty files**: Every file has content beyond just the frontmatter — at minimum, an abstract for abstract-only papers

## Bilingual Communication

Follow the same conventions as previous pipeline steps:
- Section headers in output files: bilingual (e.g., "Access Log / 取得紀錄")
- Table headers: bilingual
- Action items and instructions to the user: bilingual
- Paper content itself: keep in the original language (usually English)
- Technical terms in English with Chinese explanation on first mention: e.g., "access hierarchy（存取層級）", "open access（開放取用）"
