---
citation_key: "WangEtAl2025b"
title: "Measuring Aleatoric and Epistemic Uncertainty in LLMs: Empirical Evaluation on ID and OOD QA Tasks"
authors: "K. Wang; Subre Abdoul Moktar; Jia Li; Kangshuo Li; Feng Chen"
year: 2025
doi: "10.48550/arxiv.2511.03166"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
arxiv_id: "2511.03166"
tier: 3
composite_score: 3.95
---
# Measuring Aleatoric and Epistemic Uncertainty in LLMs: Empirical Evaluation on ID and OOD QA Tasks
**Authors**: K. Wang, Subre Abdoul Moktar, Jia Li, Kangshuo Li, Feng Chen
**Year**: 2025
**Venue**: ArXiv
**DOI**: [10.48550/arxiv.2511.03166](https://doi.org/10.48550/arxiv.2511.03166)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.48550/arxiv.2511.03166

---

## Abstract / 摘要

Large Language Models (LLMs) have become increasingly pervasive, finding applications across many industries and disciplines. Ensuring the trustworthiness of LLM outputs is paramount, where Uncertainty Estimation (UE) plays a key role. In this work, a comprehensive empirical study is conducted to examine the robustness and effectiveness of diverse UE measures regarding aleatoric and epistemic uncertainty in LLMs. It involves twelve different UE methods and four generation quality metrics including LLMScore from LLM criticizers to evaluate the uncertainty of LLM-generated answers in Question-Answering (QA) tasks on both in-distribution (ID) and out-of-distribution (OOD) datasets. Our analysis reveals that information-based methods, which leverage token and sequence probabilities, perform exceptionally well in ID settings due to their alignment with the model's understanding of the data. Conversely, density-based methods and the P(True) metric exhibit superior performance in OOD contexts, highlighting their effectiveness in capturing the model's epistemic uncertainty. Semantic consistency methods, which assess variability in generated answers, show reliable performance across different datasets and generation metrics. These methods generally perform well but may not be optimal for every situation.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.95)
- **Relevance**: 5.0 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 2.5 — Limited methodological detail in abstract
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: epistemic_aleatoric
