---
name: research-export
description: "Step 4 of the Research Agent pipeline: export screened papers as APA 7 references, citation key lookup table, and BibTeX file. Use this skill whenever the user mentions exporting references, creating a bibliography, generating BibTeX, formatting APA citations, producing citation keys, or says 'next step' after research-screen. Trigger on phrases like 'export references', 'generate .bib', 'APA format', '匯出參考文獻', '產生引用', '建立書目', 'citation key table', or any request to turn shortlisted papers into formatted reference outputs. This skill handles the precise formatting rules (sentence case, author initials, ampersand placement, PascalCase keys, cross-validation) that generic prompting tends to get wrong."
---

# Research Export — Step 4 of Research Agent Pipeline

You are transforming a shortlist of screened papers into three publication-ready reference outputs: an APA 7 reference list, a citation key lookup table, and a BibTeX file. These outputs are consumed by every downstream step — the SOTA review cites papers by key, the manuscript uses the .bib file, and the citation key table is the shared lookup for the entire pipeline.

Getting this right matters because a wrong citation key, a mangled author name, or a missing BibTeX field will propagate errors into the literature review, the LaTeX manuscript, and ultimately the published paper. Treat this as a formatting and validation task — precision over speed.

## Input

Read these files from the session folder:

1. **`step3_shortlist.json`** — Included papers with full metadata (authors, year, title, journal, DOI, URL, arxiv_id, etc.) and screening scores
2. **`step3_screening_results.md`** — For cross-reference if the user manually included borderline papers at Checkpoint 2

If the user manually included borderline papers (marked with `"manually_included": true` in the shortlist, or the user tells you to add specific papers), include those too.

If `step3_shortlist.json` is missing, tell the user to run `/research-screen` first.

## Procedure

### 1. Extract and Validate Citation Metadata

For each paper in the shortlist, extract the fields needed for citation:

- **Authors**: full list from `authors[]` array
- **Year**: from `year` field
- **Title**: from `title` field
- **Journal/Venue**: from `journal` field
- **Volume, Issue, Pages**: extract from the `journal` field or any available metadata. The shortlist from Step 2 may include these in different forms (e.g., embedded in the journal string like "Journal Name, 33(2), 100-115" or as separate fields). Parse what's available; omit only when genuinely absent from the source data
- **DOI**: from `doi` field
- **URL**: from `url` field (fallback if no DOI)
- **arXiv ID**: from `arxiv_id` field (for preprints)

**Validation checks before formatting:**
- If `authors` is empty or missing, flag the paper and skip it with a warning
- If `year` is missing, flag and skip
- If `title` is missing, flag and skip
- If both `doi` and `url` are missing, note it but still include the entry (some papers are identifiable by title alone)
- If any author name appears to have only one token (e.g., just "Charles" with no surname), flag it — this likely indicates incomplete source data. Include the name as-is but add a note: `% TODO: verify author name`

### 2. Generate Citation Keys

Citation keys follow the `AuthorYear` convention used in academic LaTeX workflows:

**Rules:**
- Single author: `LastName` + `Year` → e.g., `Zhang2024`
- Two authors: `LastName1` + `LastName2` + `Year` → e.g., `XiaZhang2024`
- Three or more authors: `FirstAuthorLastName` + `EtAl` + `Year` → e.g., `BouzeniaEtAl2025`

**Disambiguation:** When two or more papers produce the *same* key, append lowercase letters sorted alphabetically by title: `Zhang2024a`, `Zhang2024b`, `Zhang2024c`. Only add suffixes when an actual collision exists — if there's only one paper by Zhang in 2024, the key is simply `Zhang2024` with no suffix. A lone `Zhang2024a` with no corresponding `b` is wrong.

**Last name extraction:**
- For Western names like "Chunqiu Steven Xia", the last name is the final token: "Xia"
- For Chinese/Korean/Japanese names where the family name comes first (e.g., "Zhang Quanjun"), the first token is typically the family name: "Zhang". However, in the `authors[]` array from Step 2, names are usually already in "GivenName FamilyName" order — so default to using the last token unless clearly otherwise
- For hyphenated names like "García-López", keep the full hyphenated form: "Garcia-Lopez2024"

Build a mapping: `paper_id → citation_key` and verify it's a bijection (every paper has exactly one key, no key maps to two papers).

### 3. Format APA 7th Edition References

Apply APA 7th edition formatting rules strictly:

**Journal article:**
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. *Journal Name*, *volume*(issue), pages. https://doi.org/xxxxx
```

**Conference paper:**
```
Author, A. A., & Author, B. B. (Year). Title of paper. In *Proceedings of the Conference Name* (pp. pages). Publisher. https://doi.org/xxxxx
```

**Preprint (arXiv):**
```
Author, A. A., & Author, B. B. (Year). Title of paper. *arXiv preprint*. https://arxiv.org/abs/XXXX.XXXXX
```

**APA 7 formatting details:**

- **Author names**: Last, F. M. (use initials for given names). Up to 20 authors listed; if 21+, list the first 19, then `...`, then the last author.
- **Ampersand**: Use `&` before the last author in *every* multi-author reference (not "and"). This is the most commonly missed APA rule — double-check every entry with 2+ authors has `&` before the final name. For two authors: `Author, A. A., & Author, B. B.` For three+: `Author, A. A., Author, B. B., & Author, C. C.`
- **Title**: Sentence case (capitalize only the first word, first word after a colon, and proper nouns). This is a common mistake — do NOT use title case.
- **Journal name**: Title case, italicized with `*`
- **Volume**: Italicized with `*`
- **DOI**: Always use `https://doi.org/` format (not `doi:` or bare DOI)
- **No period after DOI/URL**: APA 7 does not put a period after a DOI or URL at the end of a reference

**Detecting entry type:**
- If `journal` contains "Proceedings", "Conference", "Symposium", "Workshop", or "ICSE/ISSTA/FSE/ASE/NeurIPS/ICLR/ACL" etc. → conference paper format
- If `arxiv_id` is present and `journal` is null or says "arXiv" → preprint format
- Otherwise → journal article format

**Sort** the final list as a single flat alphabetical list by the first author's last name. Do NOT group by tier or any other category — APA requires one unified list. For same first-author, sort by year (oldest first). For same first-author and year, sort by title.

### 4. Generate BibTeX Entries

For each paper, produce a BibTeX entry with the citation key from Step 2:

**Journal article:**
```bibtex
@article{AuthorYear,
  author    = {LastName1, FirstName1 and LastName2, FirstName2},
  title     = {Full Title in Original Case},
  journal   = {Journal Name},
  year      = {2024},
  volume    = {33},
  number    = {2},
  pages     = {100--115},
  doi       = {10.1145/xxxxx},
  url       = {https://doi.org/10.1145/xxxxx}
}
```

**Conference paper:**
```bibtex
@inproceedings{AuthorYear,
  author    = {LastName1, FirstName1 and LastName2, FirstName2},
  title     = {Full Title in Original Case},
  booktitle = {Proceedings of the Conference Name},
  year      = {2024},
  pages     = {100--115},
  doi       = {10.1145/xxxxx},
  url       = {https://doi.org/10.1145/xxxxx}
}
```

**Preprint:**
```bibtex
@misc{AuthorYear,
  author       = {LastName1, FirstName1 and LastName2, FirstName2},
  title        = {Full Title in Original Case},
  year         = {2024},
  eprint       = {2304.00385},
  archiveprefix = {arXiv},
  primaryclass = {cs.SE},
  url          = {https://arxiv.org/abs/2304.00385}
}
```

**BibTeX-specific rules:**
- **Title**: Keep original case (NOT sentence case — BibTeX handles casing). Protect proper nouns and acronyms with braces: `{ChatGPT}`, `{LLM}`, `{Defects4J}`
- **Author names**: `LastName, FirstName and LastName, FirstName` format (use `and` to separate, not `&`)
- **Special characters**: Escape LaTeX special chars: `&` → `\&`, `%` → `\%`, `_` → `\_`
- Include `doi` and `url` fields when available
- Omit fields that are empty rather than leaving blank values

### 5. Cross-Validation

Before saving, run these checks:

1. **Count match**: Number of entries in APA list = number in BibTeX file = number in citation key table = number of papers in shortlist
2. **Key consistency**: Every citation key in the key table appears exactly once in the APA list and exactly once in the .bib file
3. **No orphans**: Every paper in `step3_shortlist.json` has a corresponding entry in all three outputs
4. **DOI format**: All DOIs use `https://doi.org/` prefix (not bare DOI or `doi:` prefix)
5. **Author formatting**: Spot-check 3-5 entries — initials in APA, full names in BibTeX, correct last-name extraction
6. **Ampersand check**: Scan every multi-author APA entry for `&` before the last author. Every entry with 2+ authors must have exactly one `&`. Missing ampersands are the most common APA error — check every entry, not just a sample.
7. **Disambiguation check**: Verify that every citation key with a letter suffix (a/b/c) has at least one sibling. If `Zhang2024a` exists, `Zhang2024b` must also exist. Lone suffixed keys are errors.
8. **Alphabetical order check**: Verify the APA list is sorted as a single flat list, not grouped by tier. The first author last names should be in strict A-Z order from start to end.

If any check fails, fix the issue before saving.

## Output

### `step4_references_apa.md`

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 4
total_references: {N}
---

# References (APA 7th Edition) / 參考文獻

> Topic / 研究主題: {topic}
> Total references / 參考文獻總數: {N}
> Generated / 產生日期: {date}

---

Bouzenia, I., Devanbu, P., & Pradel, M. (2025). RepairAgent: An autonomous, LLM-based agent for program repair. In *Proceedings of the IEEE/ACM 47th International Conference on Software Engineering*. https://doi.org/10.1109/ICSE55347.2025.00157

Xia, C. S., & Zhang, L. (2024). Keep the conversation going: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT. In *Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis*. https://doi.org/10.1145/3650212.3680323

Zhang, Q., Fang, C., Zhang, Y., Zhang, T., & Chen, Z. (2024). A systematic literature review on large language models for automated program repair. *ACM Transactions on Software Engineering and Methodology*. https://doi.org/10.1145/3799693

---

Files / 檔案: `step4_references_apa.md`, `step4_citation_keys.md`, `step4_references.bib`
Next step / 下一步: `/research-fulltext`
```

### `step4_citation_keys.md`

A quick-lookup table that maps citation keys to papers. This is the shared reference for the entire pipeline — the SOTA review, gap analysis, and manuscript all use these keys.

```markdown
---
session_id: "{session_id}"
topic: "{topic}"
date: "{YYYY-MM-DD}"
step: 4
---

# Citation Keys / 引用鍵值對照表

> Topic / 研究主題: {topic}
> Total / 總數: {N} papers

| Citation Key / 引用鍵 | Citation / 引用 | Short Title / 簡稱 | Year / 年份 | Tier |
|----------------------|----------------|-------------------|------------|------|
| `XiaZhang2024` | (Xia & Zhang, 2024) | Keep the conversation going... | 2024 | 1 |
| `ZhangEtAl2024` | (Zhang et al., 2024) | Systematic literature review on LLM-APR | 2024 | 1 |
| `BouzeniaEtAl2025` | (Bouzenia et al., 2025) | RepairAgent | 2025 | 1 |

---

## Usage / 使用方式

In downstream steps, cite papers using the citation key:
- In SOTA review: `(Xia & Zhang, 2024)` or `Xia and Zhang (2024)`
- In LaTeX: `\cite{XiaZhang2024}`

---

Files / 檔案: `step4_references_apa.md`, `step4_citation_keys.md`, `step4_references.bib`
Next step / 下一步: `/research-fulltext`
```

### `step4_references.bib`

A standard BibTeX file with all entries, ready for LaTeX compilation. No markdown — pure `.bib` format.

```bibtex
% Auto-generated BibTeX — Research Agent Pipeline Step 4
% Session: {session_id} | Topic: {topic}
% Generated: {date}
% Total entries: {N}

@inproceedings{XiaZhang2024,
  author    = {Xia, Chunqiu Steven and Zhang, Lingming},
  title     = {Keep the Conversation Going: Fixing 162 out of 337 Bugs for \$0.42 Each Using {ChatGPT}},
  booktitle = {Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis},
  year      = {2024},
  doi       = {10.1145/3650212.3680323},
  url       = {https://doi.org/10.1145/3650212.3680323}
}
```

## After Saving

Update `step0_session_config.json`: set `"current_step": 4`.

Then present to the user:

1. **Summary** — total references exported, format breakdown (journal / conference / preprint)
2. **Citation key table** — show the full table inline for quick review
3. **Spot-check highlight** — show 2-3 formatted APA entries so the user can verify formatting
4. **Suggest next step:** `/research-fulltext`

## Edge Cases

- **Missing metadata**: If a paper has no DOI, no URL, and no arXiv ID, include it with whatever identifying info exists (title, authors, year). Add a comment: `% TODO: missing DOI/URL — verify manually`
- **Non-English titles**: Keep the original title. If the paper has both an English and non-English title, use the English one for the APA entry.
- **Very long author lists (21+)**: APA 7 rule: list first 19 authors, then `...`, then last author. In BibTeX, list all authors.
- **Papers with organization authors**: e.g., "OpenAI" as author. Use the organization name directly: `OpenAI. (2024). Title...` and BibTeX: `author = {{OpenAI}}` (double braces to prevent parsing).
- **Preprints later published**: If a paper has both an `arxiv_id` and a journal `doi`, prefer the published version format. Note the arXiv ID in the BibTeX entry as a supplementary field.
- **Dollar signs and special chars in titles**: Escape for both LaTeX (`\$`) and markdown (`$` is fine in markdown but watch for accidental math mode).
- **Duplicate papers after manual inclusion**: If the user included borderline papers that somehow overlap with the existing shortlist, deduplicate by DOI or title before generating references.

## Bilingual Communication

Follow the same conventions as previous pipeline steps:
- Section headers: bilingual (e.g., "References / 參考文獻")
- Table headers: bilingual
- Usage instructions: bilingual
- Technical formatting (APA entries, BibTeX entries): English only — these are standardized formats
- Keep technical terms in English with Chinese explanation on first mention: e.g., "citation key（引用鍵）", "BibTeX（LaTeX 參考書目格式）"
