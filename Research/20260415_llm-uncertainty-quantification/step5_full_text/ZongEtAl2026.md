---
citation_key: "ZongEtAl2026"
title: "I-CALM: Incentivizing Confidence-Aware Abstention for LLM Hallucination Mitigation"
authors: "Haotian Zong; Binze Li; Yufei Long; Sinyin Chang; Jialong Wu; Gillian K. Hadfield"
year: 2026
doi: ""
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.85
---
# I-CALM: Incentivizing Confidence-Aware Abstention for LLM Hallucination Mitigation
**Authors**: Haotian Zong, Binze Li, Yufei Long, Sinyin Chang, Jialong Wu, Gillian K. Hadfield
**Year**: 2026
**Venue**: arXiv (Cornell University)
**DOI**: —

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

---

## Abstract / 摘要

Large language models (LLMs) frequently produce confident but incorrect answers, partly because common binary scoring conventions reward answering over honestly expressing uncertainty. We study whether prompt-only interventions -- explicitly announcing reward schemes for answer-versus-abstain decisions plus humility-oriented normative principles -- can reduce hallucination risk without modifying the model. Our focus is epistemic abstention on factual questions with a verifiable answer, where current LLMs often fail to abstain despite being uncertain about their answers. We first assess self-reported verbal confidence as a usable uncertainty signal, showing stability under prompt paraphrasing and reasonable calibration against a token-probability baseline. We then study I-CALM, a prompt-based framework that (i) elicits verbal confidence, (ii) partially rewards abstention through explicit reward schemes, and (iii) adds lightweight normative principles emphasizing truthfulness, humility, and responsibility. Using GPT-5 mini on PopQA as the main setting, we find that confidence-eliciting, abstention-rewarding prompts, especially with norms, reduce the false-answer rate on answered cases mainly by identifying and shifting error-prone cases to abstention and re-calibrating their confidence. This trades coverage for reliability while leaving forced-answer performance largely unchanged. Varying the abstention reward yields a clear abstention-hallucination frontier. Overall, results show the framework can improve selective answering on factual questions without retraining, with the magnitude of effect varying across models and datasets. Code is available at the following https://github.com/binzeli/hallucinationControl.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.85)
- **Relevance**: 4.5 — Strong LLM-UQ alignment
- **Quality**: 3.0 — Standard empirical methodology
- **Recency/Impact**: 3.5 — Very recent (2026), cites still accruing
- **Cluster**: hallucination_detection
