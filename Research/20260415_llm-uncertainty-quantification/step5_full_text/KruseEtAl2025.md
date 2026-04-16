---
citation_key: "KruseEtAl2025"
title: "Simple Yet Effective: An Information-Theoretic Approach to Multi-LLM Uncertainty Quantification"
authors: "Maya Kruse; Majid Afshar; Saksham Khatwani; A. Mayampurath; Guanhua Chen; Yanjun Gao"
year: 2025
doi: "10.18653/v1/2025.emnlp-main.1551"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
arxiv_id: "2507.07236"
tier: 3
composite_score: 3.8
---
# Simple Yet Effective: An Information-Theoretic Approach to Multi-LLM Uncertainty Quantification
**Authors**: Maya Kruse, Majid Afshar, Saksham Khatwani, A. Mayampurath, Guanhua Chen, Yanjun Gao
**Year**: 2025
**Venue**: Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing
**DOI**: [10.18653/v1/2025.emnlp-main.1551](https://doi.org/10.18653/v1/2025.emnlp-main.1551)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.18653/v1/2025.emnlp-main.1551

---

## Abstract / 摘要

Large language models (LLMs) often behave inconsistently across inputs, indicating uncertainty and motivating the need for its quantification in high-stakes settings. Prior work on calibration and uncertainty quantification often focuses on individual models, overlooking the potential of model diversity. We hypothesize that LLMs make complementary predictions due to differences in training and the Zipfian nature of language, and that aggregating their outputs leads to more reliable uncertainty estimates. To leverage this, we propose MUSE (Multi-LLM Uncertainty via Subset Ensembles), a simple information-theoretic method that uses Jensen-Shannon Divergence to identify and aggregate well-calibrated subsets of LLMs. Experiments on binary prediction tasks demonstrate improved calibration and predictive performance compared to single-model and naïve ensemble baselines. In addition, we explore using MUSE as guided signals with chain-of-thought distillation to fine-tune LLMs for calibration. MUSE is available at:https://github.com/LARK-NLP-Lab/MUSE.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.8)
- **Relevance**: 5.0 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 2.0 — Weak methodological signal
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: calibration_metrics_theory
