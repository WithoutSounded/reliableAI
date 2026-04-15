# Brick Layer Rules

Per-section hard constraints for Phase 2b (sliding-window drafting). These are **not style suggestions** — they are the constraints Step 3 (review) and Step 5 (polish) will check against mechanically. Violating them now creates flags later that cost more to fix than to avoid.

The rules are organized so you can reread the relevant section's block before drafting without scanning the whole file. Each block has: **Purpose**, **Tense**, **Must-have**, **Prohibited**, and **Pre-emit checklist**.

---

## Methods

**Purpose**: describe what was done and the system under study, at a level of detail that allows reproduction. Not why it's novel (that's Introduction), not why it worked (that's Discussion), not what the numbers were (that's Results).

**Tense**
- Past for actions you took ("We trained the model on 80% of the data")
- Present for what the system *is* ("The model consists of three layers", "The gating function operates as follows")
- Do not narrate decisions ("We decided to…", "We chose X because…"). State the design. Rationale in one-liner form is OK sparingly; extended rationale belongs in Introduction or Discussion.

**Must-have**
- Every math expression uses symbols from `notation_glossary.md`. If a symbol doesn't exist there, add it to `step2_global_config.json.glossary` before using.
- Every dimension in a forward pass is traceable: inputs → intermediate tensors → outputs. State shapes explicitly on first appearance ("a tensor of shape [B, T, C]").
- Every hyperparameter either has a value ("learning rate = 1e-4") or the explicit note "(see Section 4 for ablation)".
- Every algorithm block in `pseudocode.md` that the blueprint allocates here is inserted as an `\begin{algorithm}` environment.
- The architecture figure (if allocated here per blueprint) is `\ref{}`'d at the subsection where the architecture is introduced.

**Prohibited**
- Interpretation: "This design choice is superior because…", "We expect this to outperform…", "The benefit of X is…"
- Comparative language: "Unlike prior work…", "In contrast to Chen2023…" — belongs in Related Work or Discussion
- Results-like statements: "We achieve F1 = 0.87" — that's Results
- Citations of the present work's own contribution as if external
- Hedging ("may perform", "could be interpreted as") — Methods describes what is, not what might be

**Pre-emit checklist**
- [ ] Every symbol used appears in `notation_glossary.md` or `step2_global_config.json.glossary`
- [ ] No sentence contains a justification keyword ("because", "since [reason]", "in order to achieve better…")
- [ ] Every figure reference points to the architecture/procedure diagram allocated by blueprint, not to Results figures
- [ ] Every `\cite{}` is either a method-origin citation or a dataset-origin citation (not a performance comparison)

---

## Results

**Purpose**: report what was observed, anchored to figures and tables. Not why it happened, not what it means for the field — just what the measurements showed.

**Tense**
- Past for experiments ("We evaluated on Dataset B", "The model was tested under N=200")
- Present for what figures show ("Fig. 3 shows a monotonic decrease", "Table 2 reports the best F1 on each split")
- Mixed is normal — past for your actions, present for the artifact describing itself.

**Must-have**
- Every number comes verbatim from `step4_analysis_summary.md`, `step1_preprocess/figure_captions.md`, or `step1_preprocess/table_captions.md`. Round only as needed for prose readability, and only to the precision the source uses.
- Every subsection references at least one figure or table via `\ref{fig:*}` or `\ref{tab:*}`. If blueprint didn't allocate a figure/table to a subsection, challenge the blueprint — Results subsections without visual anchors are usually misscoped.
- Statistical results stated with test, statistic, and p-value: "t(48) = 3.21, p = 0.002". If no test was performed, do not imply significance ("Model A was better than Model B" → "Model A achieved higher F1 (0.87 vs 0.81)").

**Prohibited**
- Causal language: "because", "due to", "caused by", "as a result of [mechanism]". State observed associations; mechanism discussion belongs in Discussion.
- Interpretation: "This suggests that…", "indicating that…", "which demonstrates…". Use only describing-the-figure verbs ("shows", "reports", "presents").
- Citations to external work to compare performance — those comparisons belong in Discussion (with appropriate hedging) or Related Work.
- Editorializing: "impressively", "notably", "surprisingly", "only", "just". Report the number; let the reader judge whether it's impressive.

**Pre-emit checklist**
- [ ] Every numerical claim is traceable to `analysis_summary.md` or a figure/table caption with matching value
- [ ] Every subsection has ≥1 `\ref{fig:*}` or `\ref{tab:*}`
- [ ] No sentence contains "because", "due to", "suggests", "demonstrates" (Results verbs: shows, reports, reaches, yields, presents, indicates-that-measurement-shows-not-interpretation)
- [ ] Statistical claims include the test and statistic, or explicitly note they are descriptive

---

## Introduction

**Purpose**: answer "why should the reader keep reading?" by funneling from broad context into the specific gap this paper fills, the hypothesis, and the contributions.

**Tense**
- Present for general truths and current state of the field ("EEG-based attention decoding remains challenging…")
- Past for citing specific prior studies ("Chen et al. demonstrated that…", "A recent study found that…")
- Future occasionally for contribution preview ("We show that…")

**Must-have**
- Every factual claim has a `\cite{}`. "EEG-based BCI has gained traction in clinical settings" needs a citation; otherwise reword or drop.
- The funnel narrows from broad to specific in **≤4 paragraphs**:
  1. Broad field and why it matters
  2. The current state-of-the-art and what it achieves
  3. The specific limitation or gap (sourced from `step7_gap_analysis.md`)
  4. Our contribution and the hypothesis
- The final paragraph states contributions explicitly (numbered or enumerated) and previews the section structure ("The remainder of the paper is organized as follows: Section 2 reviews related work…"). The preview sentence is optional if journal style discourages it (some venues consider it filler).

**Prohibited**
- Figures: Introduction should not reference figures. (A teaser figure, if allocated, is an exception — place it but don't let its content carry the argument.)
- Causal or experimental specifics: "We used X learning rate" — belongs in Methods.
- Over-hedging: the Introduction states claims confidently. Save hedging for Discussion.
- Referring to "this paper" or "this work" more than twice. Once in the contribution paragraph is enough.

**Pre-emit checklist**
- [ ] Every factual sentence has `\cite{}` or is clearly about the present paper's contribution
- [ ] The funnel is ≤4 paragraphs and ends with an explicit contribution list
- [ ] No `\ref{fig:*}` except the optional teaser figure allocated by blueprint
- [ ] Citations match keys in `step4_references.bib` (no fabricated keys)

---

## Related Work

**Purpose**: contextualize the paper among prior work, grouped by theme, ending with a paragraph that positions the current contribution against the prior work reviewed.

**Tense**
- Present perfect for the field's trajectory ("Prior work has explored…")
- Past for individual studies ("Chen et al. proposed…", "A 2023 study demonstrated…")

**Must-have**
- **Every paragraph cites ≥2 papers**. A paragraph with one citation is a single-source summary — either expand with peers or merge into a neighboring theme.
- **Thematic grouping, not chronological**. Organize by approach/method/assumption, not by year. A section titled "Deep learning approaches to EEG" is better than "2019, 2020, 2021".
- **Ends with a positioning paragraph** that explicitly contrasts prior work with the current paper's contribution: "In contrast to prior work, which [limitation], we [contribution]." The positioning paragraph ties back to the gap statement in Introduction and forward to Methods.

**Prohibited**
- Interpretation of the present paper's results. Related Work is written before readers see Methods; it cannot reference "our findings".
- Exhaustive listing. Cite the most relevant 3–5 papers per theme. If the blueprint's citation allocation is too broad, push back — encyclopedic Related Work sections are one of the most common review complaints.
- Taking sides in a debate without citing both sides. If you critique approach A, cite papers in A and, if relevant, the critique papers.

**Pre-emit checklist**
- [ ] Every paragraph cites ≥2 papers
- [ ] The final paragraph contains an explicit "In contrast…" or "Unlike prior work…" positioning statement
- [ ] Themes align with the blueprint's subsection outline (don't invent new themes mid-draft)
- [ ] All citation keys resolve to `references.bib`

---

## Discussion

**Purpose**: interpret what the results mean, compare with prior literature, acknowledge limitations, and draw implications. This is where you earn the right to say what your numbers mean.

**Tense**
- Present for implications and interpretations ("Our findings suggest…", "This result indicates…")
- Past for comparing with prior studies ("Chen et al. reported similar trends…", "Unlike Wang (2023), we observed…")

**Must-have**
- **Every interpretive claim uses hedging**: "may suggest", "one possible interpretation is", "these findings indicate that [claim] under [scope condition]". Calibrate the hedge to the evidence: a p<0.001 ablation supports stronger language ("these results demonstrate") than a descriptive observation (use "suggest").
- **Every comparison with prior work cites the specific paper and metric**: "Our F1 of 0.87 exceeds the 0.81 reported by Chen et al. (2023) on the same benchmark." Vague comparisons ("outperforms prior work") are prohibited — Step 3 will flag them as `OVERCLAIM`.
- **Acknowledge ≥1 limitation explicitly**. "Our study did not include …", "The generalization to [population X] remains untested." Limitations belong here (even briefly) so Conclusion doesn't carry the whole burden.
- **Mirrors the Results structure**. Discuss findings in the same order Results reported them. Each Discussion subsection maps to a Results subsection (or cluster of them).

**Prohibited**
- New data or new results. Discussion uses only what Results already reported.
- Unhedged causal claims. "Our method is superior because of X" → "One possible reason our method outperforms is X, though further ablation would be needed to isolate the mechanism."
- Strawmen. If you critique prior work, cite it and represent its claim fairly.

**Pre-emit checklist**
- [ ] Every claim either reports a factual result (cross-check against Results subsection) or is hedged
- [ ] Every comparison with prior work names the paper and the metric
- [ ] ≥1 explicit limitation stated
- [ ] Discussion subsections parallel Results subsections in order

---

## Conclusion

**Purpose**: a tight summary. Contributions enumerated, one limitation carried forward, one forward-looking sentence. Many readers read only Abstract + Conclusion — make both self-contained.

**Tense**
- Past for what was done ("We proposed…", "We evaluated on…")
- Present or future for implications and future work ("These results open the door to…", "Future work will investigate…")

**Must-have**
- **Numbered contribution list** (≤4 items). Each contribution is one sentence, pointing to the evidence ("(1) We show that X improves Y by Z on Benchmark B.").
- **≥1 limitation acknowledged** (may be abbreviated compared to Discussion; one sentence is fine).
- **Forward-looking final sentence** naming a concrete next step, not vague aspiration ("Future work will extend the evaluation to adolescents" not "Future work will explore more scenarios").

**Prohibited**
- **No new information.** Every claim must trace to something already stated in Abstract/Intro/Methods/Results/Discussion. Conclusion condenses, it does not introduce.
- **No citations.** Conclusion is the paper talking about itself; external references belong earlier.
- **No figures or tables.**

**Pre-emit checklist**
- [ ] Contribution list is numbered and ≤4 items
- [ ] Every contribution is traceable to a Results or Methods claim already made
- [ ] ≥1 limitation stated (can refer back to Discussion)
- [ ] Final sentence is forward-looking and concrete
- [ ] No `\cite{}` and no `\ref{fig:*}`/`\ref{tab:*}`

---

## A note on Abstract

**Abstract is drafted in Step 5 (polish), not here.** Skip it entirely during the sliding window. The reason: Abstract is written last because it summarizes the finished paper; drafting it early means rewriting it after every revision. If the user or a meta-skill insists on a placeholder, leave `00_abstract.tex` absent and let Step 5 generate it from the polished sections.
