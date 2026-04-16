---
citation_key: "atakKuzlu2024"
title: "Uncertainty quantification in large language models through convex hull analysis"
authors: "Ferhat Özgür Çatak; Murat Kuzlu"
year: 2024
doi: "10.1007/s44163-024-00200-w"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.8
---
# Uncertainty quantification in large language models through convex hull analysis
**Authors**: Ferhat Özgür Çatak, Murat Kuzlu
**Year**: 2024
**Venue**: Discover Artificial Intelligence
**DOI**: [10.1007/s44163-024-00200-w](https://doi.org/10.1007/s44163-024-00200-w)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.1007/s44163-024-00200-w

---

## Abstract / 摘要

Uncertainty quantification approaches have been more critical in large language models (LLMs), particularly high-risk applications requiring reliable outputs. However, traditional methods for uncertainty quantification, such as probabilistic models and ensemble techniques, face challenges when applied to the complex and high-dimensional nature of LLM-generated outputs. This study proposes a novel geometric approach to uncertainty quantification using convex hull analysis. The proposed method leverages the spatial properties of response embeddings to measure the dispersion and variability of model outputs. The prompts are categorized into three types, i.e., ’easy’, ’moderate’, and ’confusing’, to generate multiple responses using different LLMs at varying temperature settings. The responses are transformed into high-dimensional embeddings via a BERT model and subsequently projected into a two-dimensional space using Principal Component Analysis (PCA), Isomap, Multidimensional Scaling (MDS). The Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm is utilized to cluster the embeddings and compute the convex hull for each selected cluster. The experimental results indicate that the uncertainty of the model for LLMs depends on the prompt complexity, the model, and the temperature setting.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.8)
- **Relevance**: 5.0 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 2.0 — Weak methodological signal
- **Recency/Impact**: 3.5 — Recent (2024), moderate visibility
- **Cluster**: retrieval_agentic
