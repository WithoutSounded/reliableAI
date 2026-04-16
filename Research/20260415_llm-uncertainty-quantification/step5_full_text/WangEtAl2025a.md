---
citation_key: "WangEtAl2025a"
title: "COIN: Uncertainty-Guarding Selective Question Answering for Foundation Models with Provable Risk Guarantees"
authors: "Zhiyuan Wang; Jinhao Duan; Qingni Wang; Xiaofeng Zhu; Tianlong Chen; Xiaoshuang Shi; Kaidi Xu"
year: 2025
doi: "10.48550/arxiv.2506.20178"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
arxiv_id: "2506.20178"
tier: 3
composite_score: 3.65
---
# COIN: Uncertainty-Guarding Selective Question Answering for Foundation Models with Provable Risk Guarantees
**Authors**: Zhiyuan Wang, Jinhao Duan, Qingni Wang, Xiaofeng Zhu, Tianlong Chen, Xiaoshuang Shi, Kaidi Xu
**Year**: 2025
**Venue**: ArXiv
**DOI**: [10.48550/arxiv.2506.20178](https://doi.org/10.48550/arxiv.2506.20178)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.48550/arxiv.2506.20178

---

## Abstract / 摘要

Uncertainty quantification (UQ) for foundation models is essential to identify and mitigate potential hallucinations in automatically generated text. However, heuristic UQ approaches lack formal guarantees for key metrics such as the false discovery rate (FDR) in selective prediction. Previous work adopts the split conformal prediction (SCP) framework to ensure desired coverage of admissible answers by constructing prediction sets, but these sets often contain incorrect candidates, limiting their practical utility. To address this, we propose COIN, an uncertainty-guarding selection framework that calibrates statistically valid thresholds to filter a single generated answer per question under user-specified FDR constraints. COIN estimates the empirical error rate on a calibration set and applies confidence interval methods such as Clopper-Pearson to establish a high-probability upper bound on the true error rate (i.e., FDR). This enables the selection of the largest uncertainty threshold that ensures FDR control on test data while significantly increasing sample retention. We demonstrate COIN's robustness in risk control, strong test-time power in retaining admissible answers, and predictive efficiency under limited calibration data across both general and multimodal text generation tasks. Furthermore, we show that employing alternative upper bound constructions and UQ strategies can further boost COIN's power performance, which underscores its extensibility and adaptability to diverse application scenarios.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.65)
- **Relevance**: 4.0 — Multiple UQ/LLM terms indicate close alignment
- **Quality**: 2.5 — Limited methodological detail in abstract
- **Recency/Impact**: 4.5 — Recent (2025) + moderate impact (10 cites)
- **Cluster**: calibration_metrics_theory
