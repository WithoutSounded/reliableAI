---
citation_key: "McKennaEtAl2023"
title: "Sources of Hallucination by Large Language Models on Inference Tasks"
authors: "Nick McKenna; Tianyi Li; Liang Cheng; Mohammad Javad Hosseini; Mark Johnson; Mark Steedman"
year: 2023
doi: "10.18653/v1/2023.findings-emnlp.182"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 2
composite_score: 4.3
---
# Sources of Hallucination by Large Language Models on Inference Tasks
**Authors**: Nick McKenna, Tianyi Li, Liang Cheng, Mohammad Javad Hosseini, Mark Johnson, Mark Steedman
**Year**: 2023
**Venue**: —
**DOI**: [10.18653/v1/2023.findings-emnlp.182](https://doi.org/10.18653/v1/2023.findings-emnlp.182)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.18653/v1/2023.findings-emnlp.182

---

## Abstract / 摘要

Large Language Models (LLMs) are claimed to be capable of Natural Language Inference (NLI), necessary for applied tasks like question answering and summarization. We present a series of behavioral studies on several LLM families (LLaMA, GPT-3.5, and PaLM) which probe their behavior using controlled experiments. We establish two biases originating from pretraining which predict much of their behavior, and show that these are major sources of hallucination in generative LLMs. First, memorization at the level of sentences: we show that, regardless of the premise, models falsely label NLI test samples as entailing when the hypothesis is attested in training data, and that entities are used as “indices’ to access the memorized data. Second, statistical patterns of usage learned at the level of corpora: we further show a similar effect when the premise predicate is less frequent than that of the hypothesis in the training data, a bias following from previous studies. We demonstrate that LLMs perform significantly worse on NLI test samples which do not conform to these biases than those which do, and we offer these as valuable controls for future LLM evaluation.


## Screening Notes / 篩選備註

- **Tier**: 2 (composite 4.3)
- **Relevance**: 4.5 — Partial alignment (UQ or LLM but not tightly linked)
- **Quality**: 3.5 — Weak methodological signal
- **Recency/Impact**: 5.0 — Seminal (2023, 115 cites)
- **Cluster**: hallucination_detection
