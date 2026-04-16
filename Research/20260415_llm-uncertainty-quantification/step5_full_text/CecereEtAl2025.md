---
citation_key: "CecereEtAl2025"
title: "Monte Carlo Temperature: a robust sampling strategy for LLM's uncertainty quantification methods"
authors: "Nicola Cecere; Andrea Bacciu; Ignacio Fernández-Tobías; Amin Mantrach"
year: 2025
doi: "10.48550/arxiv.2502.18389"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
arxiv_id: "2502.18389"
tier: 3
composite_score: 3.95
---
# Monte Carlo Temperature: a robust sampling strategy for LLM's uncertainty quantification methods
**Authors**: Nicola Cecere, Andrea Bacciu, Ignacio Fernández-Tobías, Amin Mantrach
**Year**: 2025
**Venue**: ArXiv
**DOI**: [10.48550/arxiv.2502.18389](https://doi.org/10.48550/arxiv.2502.18389)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.48550/arxiv.2502.18389

---

## Abstract / 摘要

Uncertainty quantification (UQ) in Large Language Models (LLMs) is essential for their safe and reliable deployment, particularly in critical applications where incorrect outputs can have serious consequences. Current UQ methods typically rely on querying the model multiple times using non-zero temperature sampling to generate diverse outputs for uncertainty estimation. However, the impact of selecting a given temperature parameter is understudied, and our analysis reveals that temperature plays a fundamental role in the quality of uncertainty estimates. The conventional approach of identifying optimal temperature values requires expensive hyperparameter optimization (HPO) that must be repeated for each new model-dataset combination. We propose Monte Carlo Temperature (MCT), a robust sampling strategy that eliminates the need for temperature calibration. Our analysis reveals that: 1) MCT provides more robust uncertainty estimates across a wide range of temperatures, 2) MCT improves the performance of UQ methods by replacing fixed-temperature strategies that do not rely on HPO, and 3) MCT achieves statistical parity with oracle temperatures, which represent the ideal outcome of a well-tuned but computationally expensive HPO process. These findings demonstrate that effective UQ can be achieved without the computational burden of temperature parameter calibration.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.95)
- **Relevance**: 5.0 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 2.5 — Limited methodological detail in abstract
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: calibration_metrics_theory
