---
name: research-write
description: "Step 9 of the Research Agent pipeline: write a publication-ready LaTeX introduction and related work section from the pipeline's accumulated outputs (SOTA review, gap analysis, hypothesis, references). Every citation is validated against the existing BibTeX — zero hallucinated references. Use this skill whenever the user wants to write a manuscript introduction, generate LaTeX from their research pipeline, draft an intro section, create a related work section, or says 'next step' after research-hypothesis (Step 8). Trigger on: 'write introduction', 'write intro', 'draft manuscript', 'generate LaTeX', 'write related work', 'start writing', '寫引言', '寫論文', '撰寫引言', '撰寫相關工作', '產生 LaTeX', or any request to turn the research pipeline outputs into manuscript sections — even casual phrasing like 'ok let's write this up' or '開始寫吧'. Do NOT use for SOTA review synthesis (use research-sota), gap identification (use research-gaps), or hypothesis generation (use research-hypothesis)."
---

# Research Write — Step 9 of Research Agent Pipeline

You are writing the introduction and related work sections of an academic manuscript. This is where the entire pipeline converges: the PICO question, the literature search, the screening, the thematic synthesis, the gap analysis, and the hypothesis all flow into a single, coherent narrative designed to persuade a reviewer that this research is necessary, well-motivated, and methodologically sound.

The difference between a good introduction and a mediocre one is not vocabulary or length — it's narrative architecture. A good introduction builds an argument: the world has problem X, researchers have tried approaches A/B/C (with these specific results), but gap Y remains, so we propose Z. Each sentence advances this argument. A mediocre introduction lists facts and papers without a throughline. Your job is to construct the argument from the evidence the pipeline has gathered, with zero fabrication.

The single most important constraint in this skill is **anti-hallucination**: every `\cite{}` command must correspond to a real entry in `step4_references.bib`, every statistic must come from a paper in the shortlist, and every claim must be traceable to evidence. An introduction with phantom citations is worse than no introduction at all — it undermines the entire pipeline's credibility.

You produce three outputs: a LaTeX introduction, a LaTeX related work section, and a pruned BibTeX file containing only the references actually cited.

## Input

Read these files from the session folder:

1. **`step4_references.bib`** — The complete BibTeX file from Step 4. This is your **citation authority**: the set of all valid citation keys. Any `\cite{}` you write MUST match an entry here. Read this file first and build a citation inventory before writing anything.
2. **`step6_sota_review.md`** — The thematic SOTA review. This provides the narrative structure for the related work and the background sections of the introduction. The themes, consensus, debates, and cross-theme patterns become your raw material.
3. **`step7_gap_analysis.md`** — The gap analysis. The selected gap (locked by the user at Checkpoint 3) becomes the core motivation for the research. The supporting evidence and counter-evidence translate directly into the gaps section of the introduction.
4. **`step8_hypothesis_specification.md`** — The hypothesis, research questions, and IN/OUT scope. This defines what the paper proposes to do. The executive summary, RQs, and H1 feed into the hypothesis and contributions sections.
5. **`step8_journal_recommendations.md`** — Target journal information. The top-recommended journal (or user-specified override) determines writing style, section structure, citation density, and word budget.
6. **`step3_shortlist.json`** — Paper metadata and screening scores. Use this for author names, years, and quantitative results when the SOTA review references them.

### Prerequisite Check

If any of these files are missing:
- Missing `step8_hypothesis_specification.md` or `step8_journal_recommendations.md` → tell the user to run `/research-hypothesis` first
- Missing `step6_sota_review.md` → tell the user to run `/research-sota` first
- Missing `step7_gap_analysis.md` → tell the user to run `/research-gaps` first
- Missing `step4_references.bib` → tell the user to run `/research-export` first

All four must exist before you can proceed. Do not attempt partial writing.

### Topic Consistency Check

After reading the files, verify that the `topic` field is consistent across `step6_sota_review.md`, `step7_gap_analysis.md`, and `step8_hypothesis_specification.md`. If any differ, warn the user — this may indicate a file mismatch. Use the topic from `step8_hypothesis_specification.md` as the authoritative source since that represents the user's final research direction.

### Identifying the Target Journal

The target journal determines writing conventions:

1. Check if the user specified a journal in their prompt (e.g., "write for IEEE TSE" or "target TOSEM")
2. If not, use the top recommendation (marked with ⭐) from `step8_journal_recommendations.md`
3. Extract: journal name, scope, typical article structure, and any formatting preferences

The journal choice affects:
- **Citation density**: Some journals expect 40+ references in the intro; others prefer focused citation
- **Technical depth**: Systems journals want more implementation context; theory journals want more formal framing
- **Section naming**: Some journals use "Introduction" and "Related Work" as separate sections; others combine them or use "Background"
- **Word budget**: Conference papers have tighter limits than journal articles

## Procedure

### 1. Build the Citation Inventory

Before writing a single sentence, parse `step4_references.bib` and extract every citation key into a lookup set. This inventory is your ground truth for the entire writing process.

For each entry, record:
- Citation key (e.g., `XiaZhang2024b`)
- Author names and year (for in-text references)
- Entry type (`@article`, `@inproceedings`, `@misc`)

Keep this inventory accessible throughout writing. Every time you write `\cite{...}`, check the key against this inventory. If a key is not in the inventory, you cannot use it — period. There are no exceptions.

### 2. Plan the Narrative Arc

Before writing, sketch the argument structure. The introduction tells a story in six acts:

| Section | Purpose | Source material | Word target |
|---------|---------|----------------|-------------|
| 1. Context & Motivation | Why should the reader care? What real-world problem exists? | PICO from session config, SOTA executive summary | ~400 words |
| 2. Background & Key Concepts | What does the reader need to know to follow the argument? | SOTA themes overview, key definitions | ~500 words |
| 3. SOTA Themes Synthesis | What has the field accomplished? What approaches exist? | SOTA review themes (consensus + results) | ~800 words |
| 4. Research Gaps | What remains unsolved? Why do current approaches fall short? | Gap analysis (selected gap + evidence) | ~400 words |
| 5. Hypothesis & Approach | What do we propose? How will we address the gap? | Hypothesis spec (RQs, H1, approach) | ~200 words |
| 6. Contributions & Paper Outline | What are our specific contributions? How is the paper organized? | Hypothesis spec (scope, contributions) | ~200 words |

Total target: ~2500 words. This is a guideline, not a hard limit — adjust ±20% based on the target journal's conventions. Conference papers may need tighter writing (~2000 words); journal articles may afford more space (~3000 words).

The narrative must flow as a logical argument, not a disconnected list of sections. Each section should end by motivating the next:
- Context → "To address this challenge, researchers have explored..." (→ Background)
- Background → "Building on these foundations, recent work has advanced..." (→ SOTA)
- SOTA → "Despite this progress, critical gaps remain..." (→ Gaps)
- Gaps → "To address this gap, we propose..." (→ Hypothesis)
- Hypothesis → "This work makes the following contributions..." (→ Contributions)

### 3. Write `01_intro.tex`

Write the introduction as a self-contained LaTeX file. Use `\section{Introduction}` as the top-level heading, with `\subsection{}` for each of the six parts if the target journal uses subsections in introductions, otherwise use paragraph breaks with topic sentences.

#### Section 1: Context & Motivation (~400 words)

Open with the broad problem domain — why this area matters practically and scientifically. Ground the motivation in concrete stakes: what fails when this problem isn't solved? What are the costs, risks, or missed opportunities?

Then narrow to the specific research context. Cite 2-3 foundational papers that established the field or defined the problem. These should be from your citation inventory — typically survey papers or seminal works from the shortlist.

Avoid generic openings like "In recent years, X has attracted significant attention." Instead, lead with the problem: "Software bugs cost the global economy an estimated $X billion annually [citation], yet manual debugging remains..." — but only if that statistic comes from a paper in your shortlist. If no such statistic exists, use a qualitative framing grounded in cited evidence.

#### Section 2: Background & Key Concepts (~500 words)

Define the technical concepts the reader needs. For each concept:
- Define it precisely
- Cite the paper(s) that introduced or formalized it
- Explain why it matters for the rest of the introduction

Organize concepts in dependency order: define foundational concepts before those that build on them. The reader should never encounter an undefined term.

This section bridges the general motivation (Section 1) and the specific literature (Section 3). After reading it, the reader should be equipped to understand the SOTA discussion.

#### Section 3: SOTA Themes Synthesis (~800 words)

This is the longest section and draws heavily from `step6_sota_review.md`. Organize by themes, but do NOT simply repeat the SOTA review — reframe it as an argument building toward the gap.

For each theme:
- State the main approach or finding (1-2 sentences)
- Cite key papers with specific results (numbers, metrics, comparisons)
- Note limitations that point toward the gap

The themes should be ordered to build toward your gap. If the gap is about security, for instance, present themes that increasingly approach but don't reach the security dimension — so the gap feels inevitable when you introduce it.

Comparative tables are powerful in this section. If the SOTA review has a Key Results table, adapt it for the introduction — but only include studies that advance the narrative.

**Citation density guideline**: This section typically has the highest citation density. Aim for 1-2 citations per claim. Avoid citation dumps like `\cite{A, B, C, D, E, F}` with no differentiation — each cited work should contribute something specific to the sentence.

#### Section 4: Research Gaps (~400 words)

Transition from what the field has accomplished to what it has missed. Draw directly from `step7_gap_analysis.md`, focusing on the user's selected gap (the locked gap from Checkpoint 3).

Structure:
1. Acknowledge the field's achievements (1-2 sentences — prevents the gaps section from sounding dismissive)
2. State the gap clearly and specifically
3. Provide evidence: cite papers whose limitations reveal the gap
4. Explain why this gap matters — what questions can't be answered, what risks exist

Use the supporting evidence from the gap analysis. Each piece of evidence should be a specific citation with a concrete observation: "While AuthorYear achieved X on benchmark Y, their approach does not address Z" — not "prior work has limitations."

If counter-evidence exists (papers partially addressing the gap), acknowledge it and explain why the gap remains open. This demonstrates scholarly rigor and preempts reviewer objections.

#### Section 5: Hypothesis & Approach (~200 words)

State what this paper proposes to do. Draw from `step8_hypothesis_specification.md`:
- The primary research question (RQ1 or RQ2)
- The hypothesis (H1) — stated in plain language, not formal notation
- A brief description of the approach (from the conceptual framework section)

Keep this focused. The details belong in the Methods section (which this skill does not produce) — the introduction should convey the what and why, not the how.

#### Section 6: Contributions & Paper Outline (~200 words)

List 3-5 specific contributions using an `\begin{itemize}` environment. Each contribution should be:
- Specific: "We propose a security-aware repair pipeline that integrates CodeQL analysis into the agent feedback loop" — not "We improve automated repair"
- Verifiable: The reader should be able to check, after reading the paper, whether each contribution was delivered
- Grounded in the gap: Each contribution should map to an aspect of the identified gap

End with a brief paper outline: "The remainder of this paper is organized as follows. Section~\ref{sec:related} reviews related work. Section~\ref{sec:method}..." Use `\ref{}` for section references.

### 4. Write `02_relatedwork.tex`

The related work section provides deeper coverage than the introduction's SOTA synthesis. While the introduction surveys the field to motivate the gap, the related work situates the proposed approach within the specific bodies of work it builds on or differs from.

#### Structure

Use `\section{Related Work}` with `\subsection{}` for each theme. The themes should correspond to (but may not be identical to) the SOTA review's themes. Common adaptations:

- **Merge** small themes that don't warrant separate subsections
- **Split** large themes if the target journal expects fine-grained related work
- **Add** a subsection for the specific technique your approach uses, even if it wasn't a standalone SOTA theme
- **Reorder** themes to build toward your contribution

#### Writing Each Subsection

For each theme subsection:

1. **Opening statement**: What is this strand of work about? (1-2 sentences)
2. **Chronological or methodological progression**: Walk through the key papers, showing how the field evolved. For each paper, state what it did, what results it achieved (with specific numbers from the SOTA review), and what it didn't address.
3. **Synthesis**: What does this body of work collectively tell us? Where does it leave off?
4. **Bridge to your work**: How does your proposed approach relate to this theme? Does it extend it, combine it with another theme, or take a different direction?

The final paragraph of the entire related work section should explicitly contrast your approach with the closest prior work. What makes your approach different? This sets up the Methods section.

#### Citation Coverage

The related work should cite more broadly than the introduction. Aim to reference most papers from the shortlist — this is where the long tail of the literature gets covered. Papers that were too tangential for the introduction's focused narrative belong here.

### 5. Generate Pruned `references.bib`

After writing both .tex files:

1. Scan `01_intro.tex` and `02_relatedwork.tex` for every `\cite{...}` command
2. Extract all unique citation keys (handle `\cite{A, B}` multi-cite syntax)
3. For each key, copy the full BibTeX entry from `step4_references.bib`
4. Write the pruned file with only the cited entries, preserving the original formatting
5. Add a header comment noting the session, topic, and count

The pruned `references.bib` should be a strict subset of `step4_references.bib`. No entries should be added, modified, or invented.

### 6. Anti-Hallucination Validation

This is the final and most critical step. Run these checks before saving:

#### Check 1: Citation Key Validation
Extract every `\cite{...}` from both .tex files. For each key:
- Verify it exists in `step4_references.bib`
- Verify it exists in the pruned `references.bib`
- If a key fails: **remove the citation** and replace with `% TODO: citation needed — no matching entry in references.bib`

Zero phantom citations is a hard requirement. One fabricated `\cite{}` can destroy a submission.

#### Check 2: Statistic Source Verification
Scan both .tex files for quantitative claims (numbers, percentages, p-values, effect sizes). For each:
- Trace it to a specific paper in the SOTA review or shortlist
- If you cannot trace it: replace with `% TODO: verify statistic — source unclear`

#### Check 3: Claim-Source Linking
Review every factual assertion (not general knowledge, but specific research claims). Each should have at least one `\cite{}`. If a claim has no citation and isn't common knowledge in the field:
- Add `% TODO: needs citation` as a LaTeX comment after the sentence

#### Check 4: BibTeX Completeness
For each entry in the pruned `references.bib`, verify required fields are present:
- `@article`: author, title, journal, year
- `@inproceedings`: author, title, booktitle, year
- `@misc`: author, title, year

Flag incomplete entries with `% TODO: missing field` comments.

#### Check 5: Cross-Reference Integrity
- Every `\ref{}` must have a corresponding `\label{}`
- Every `\label{}` must be referenced at least once (or is in a section the user will write later — section labels like `\label{sec:method}` are OK even without a `\ref{}` in these files)

## Output

### `step9_manuscript/01_intro.tex`

```latex
% 01_intro.tex — Introduction
% Research Agent Pipeline — Step 9
% Session: {session_id} | Topic: {topic}
% Target journal: {journal_name}
% Generated: {date}
% Citation inventory: {N} keys available, {M} keys used

\section{Introduction}
\label{sec:intro}

{Section 1: Context & Motivation — ~400 words}

{Section 2: Background & Key Concepts — ~500 words}

{Section 3: SOTA Themes Synthesis — ~800 words}

{Section 4: Research Gaps — ~400 words}

{Section 5: Hypothesis & Approach — ~200 words}

The main contributions of this work are as follows:
\begin{itemize}
    \item {Contribution 1 — specific, verifiable, grounded in the gap}
    \item {Contribution 2}
    \item {Contribution 3}
\end{itemize}

The remainder of this paper is organized as follows. Section~\ref{sec:related} discusses related work. Section~\ref{sec:method} describes our proposed approach. Section~\ref{sec:experiment} presents the experimental setup and results. Section~\ref{sec:discussion} discusses implications and limitations. Section~\ref{sec:conclusion} concludes the paper.
```

### `step9_manuscript/02_relatedwork.tex`

```latex
% 02_relatedwork.tex — Related Work
% Research Agent Pipeline — Step 9
% Session: {session_id} | Topic: {topic}
% Target journal: {journal_name}
% Generated: {date}

\section{Related Work}
\label{sec:related}

{Brief introductory paragraph framing the related work structure}

\subsection{{Theme 1 Title}}
\label{sec:related:{theme1_slug}}

{Theme 1 synthesis — chronological or methodological progression with specific citations and results}

\subsection{{Theme 2 Title}}
\label{sec:related:{theme2_slug}}

{Theme 2 synthesis}

\subsection{{Theme N Title}}

{...}

{Final paragraph: explicit contrast with closest prior work, bridge to Methods}
```

### `step9_manuscript/references.bib`

```bibtex
% Pruned BibTeX — Research Agent Pipeline Step 9
% Session: {session_id} | Topic: {topic}
% Generated: {date}
% Entries: {M} (pruned from {N} total in step4_references.bib)
% Only includes entries actually cited in 01_intro.tex and 02_relatedwork.tex

{BibTeX entries — exact copies from step4_references.bib, no modifications}
```

## After Saving

Update `step0_session_config.json`: set `"current_step": 9`.

Create the `step9_manuscript/` directory if it doesn't exist.

Then present to the user:

1. **Target journal** — which journal the writing was calibrated for
2. **Word counts** — per-section and total for both .tex files
3. **Citation stats** — how many unique references cited (out of total available), citation density
4. **Anti-hallucination report** — confirm zero phantom citations, list any `% TODO` flags that need human attention
5. **TODO summary** — if any claims couldn't be sourced, list them so the user knows what to verify
6. **LaTeX compilation hint** — remind the user to compile with `pdflatex` + `bibtex` (or `biber`) to verify the output renders correctly

## Edge Cases

### Abstract-Only Sessions

Check the SOTA review's YAML frontmatter for `abstract_only: true` or `full_text_papers: 0`. If the pipeline ran on abstracts only:

- The introduction will have less quantitative detail to draw from — this is expected
- Add a LaTeX comment at the top of `01_intro.tex`:
  ```latex
  % NOTE: This introduction was generated from an abstract-only pipeline.
  % Quantitative claims may need verification against full-text sources.
  % Run /research-fulltext to improve source material before finalizing.
  ```
- Score lower confidence on statistics — prefer qualitative framing where exact numbers aren't available from the abstracts
- Flag more claims with `% TODO: verify against full text`

### Small Paper Collections (<15 papers)

With few papers, the introduction risks being thin. Adapt:
- Reduce the SOTA synthesis section to ~500 words (cover fewer themes)
- Combine Background and SOTA into a single section if themes are few
- The related work section may have only 2-3 subsections
- Note to the user that the introduction may benefit from additional references found through manual search

### User Specifies a Different Journal

If the user says "write for [journal X]" and journal X is not in `step8_journal_recommendations.md`:
- Use the user's specified journal
- Search for the journal's formatting guidelines (scope, typical article length, section conventions) using WebSearch if needed
- Adapt word budgets and citation density accordingly
- Note in the LaTeX header comment which journal was targeted

### Missing Hypothesis (Abstract-Only Quick Draft)

If `step8_hypothesis_specification.md` exists but lacks formal hypotheses (e.g., the user skipped Checkpoint 4 or the field doesn't suit formal hypothesis testing):
- Write Sections 1-4 normally
- For Section 5, frame the approach as research objectives rather than formal hypotheses
- For Section 6, frame contributions as anticipated outcomes rather than hypothesis-derived claims
- Add `% TODO: formalize hypothesis before submission` comment

### Non-English Manuscript

The default output is English-only LaTeX — academic manuscripts are typically written in English. If the user explicitly requests Chinese or another language, adapt the writing language but keep:
- Citation keys in English (they reference the .bib file)
- BibTeX entries in English (standard format)
- LaTeX commands in English (they're code)

### Conflicting Information Between Pipeline Steps

If the SOTA review and gap analysis present different information about the same paper (e.g., different reported metrics), prefer the SOTA review as the primary source — it was synthesized from fuller reading. Flag the discrepancy with a `% TODO: conflicting data` comment.

## LaTeX Quality Guidelines

The .tex files must be compilable. Follow these rules:

- **Special characters**: Escape `%`, `&`, `$`, `#`, `_` in running text. Use `\%`, `\&`, `\$`, `\#`, `\_`
- **Quotes**: Use `` ` `` and `'` for single quotes, ``` `` ``` and `''` for double quotes — not Unicode quotes
- **Dashes**: Use `--` for number ranges (pp. 10--15), `---` for em-dashes
- **Citations**: Use `\cite{key}` for parenthetical, `\citet{key}` for textual if the document class supports natbib. Default to `\cite{key}` unless the journal template specifies otherwise
- **Multi-cite**: `\cite{key1, key2}` with a space after the comma
- **Tables**: Use `\begin{table}` with `\centering`, `\caption`, and `\label`
- **No package declarations**: The .tex files are meant to be `\input{}`'d into a main document. Do not include `\documentclass`, `\usepackage`, `\begin{document}`, etc.
- **Cross-references**: Use `\label{sec:intro}`, `\label{sec:related}`, etc. Reference with `Section~\ref{sec:...}` (with a non-breaking space `~`)

## Verification Checklist

Before saving, verify:

1. **Zero phantom citations**: Every `\cite{key}` matches an entry in `step4_references.bib` and in the pruned `references.bib`
2. **Citation inventory coverage**: The pruned `references.bib` is a strict subset of `step4_references.bib` — no entries added or modified
3. **Statistic traceability**: Every number in the .tex files traces to a specific paper in the SOTA review or shortlist
4. **Narrative coherence**: Read the introduction start-to-finish — does each section flow logically into the next? Does the gap feel inevitable after the SOTA synthesis?
5. **Word budget compliance**: Total word count is within ±20% of 2500 (for intro) and appropriate for the target journal
6. **LaTeX compilability**: No unescaped special characters, all environments properly closed, no orphaned `\ref{}` or `\label{}`
7. **Gap-hypothesis alignment**: The gap described in Section 4 matches the selected gap from `step7_gap_analysis.md`, and the hypothesis in Section 5 matches `step8_hypothesis_specification.md`
8. **Contribution specificity**: Each contribution in the `\itemize` is specific and verifiable, not generic
9. **Related work completeness**: The related work covers all major themes from the SOTA review and cites a substantial portion of the shortlist
10. **No self-citations or invented references**: Every citation key was generated by Step 4. You did not invent, modify, or guess any key.

## Communication with User

This skill produces English-only LaTeX output (the manuscript language), but communicate with the user bilingually:

- **Progress updates**: Bilingual (English + Traditional Chinese)
- **Anti-hallucination report**: Bilingual
- **TODO flags explanation**: Bilingual
- **LaTeX content**: English only

When presenting the results, show a brief excerpt from the introduction (the opening paragraph and the contributions list) so the user can quickly assess tone and scope without opening the file.
