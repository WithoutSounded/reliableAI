---
citation_key: "WatsonEtAl2025"
title: "Is There No Such Thing as a Bad Question? H4R: HalluciBot for Ratiocination, Rewriting, Ranking, and Routing"
authors: "William Watson; Nicole Cho; Nishan Srishankar"
year: 2025
doi: "10.1609/aaai.v39i24.34736"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.55
---
# Is There No Such Thing as a Bad Question? H4R: HalluciBot for Ratiocination, Rewriting, Ranking, and Routing
**Authors**: William Watson, Nicole Cho, Nishan Srishankar
**Year**: 2025
**Venue**: Proceedings of the AAAI Conference on Artificial Intelligence
**DOI**: [10.1609/aaai.v39i24.34736](https://doi.org/10.1609/aaai.v39i24.34736)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.1609/aaai.v39i24.34736

---

## Abstract / 摘要

Hallucination continues to be one of the most critical challenges in the institutional adoption journey of Large Language Models (LLMs). While prior studies have primarily focused on the post-generation analysis and refinement of outputs, this paper centers on the effectiveness of queries in eliciting accurate responses from LLMs. We present HalluciBot, a model that estimates the query's propensity to hallucinate before generation, without invoking any LLMs during inference. HalluciBot can serve as a proxy reward model for query rewriting, offering a general framework to estimate query quality based on accuracy and consensus. In essence, HalluciBot investigates how poorly constructed queries can lead to erroneous outputs - moreover, by employing query rewriting guided by HalluciBot's empirical estimates, we demonstrate that 95.7% output accuracy can be achieved for Multiple Choice questions. The training procedure for HalluciBot consists of perturbing 369,837 queries n times, employing n+1 independent LLM agents, sampling an output from each query, conducting a Multi-Agent Monte Carlo simulation on the sampled outputs, and training an encoder classifier. The idea of perturbation is the outcome of our ablation studies that measures the increase in output diversity (+12.5 agreement spread) by perturbing a query in lexically different but semantically similar ways. Therefore, HalluciBot paves the way to ratiocinate (76.0% test F1 score, 46.6% in saved computation on hallucinatory queries), rewrite (+30.2% positive class transition from hallucinatory to non-hallucinatory), rank (+50.6% positive class transition from hallucinatory to non-hallucinatory), and route queries to effective pipelines.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.55)
- **Relevance**: 3.0 — Tangential — only one UQ or LLM term
- **Quality**: 4.5 — Standard empirical methodology
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: verbalized_self_confidence
