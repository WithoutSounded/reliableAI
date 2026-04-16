---
citation_key: "TonoliniEtAl2024"
title: "Bayesian Prompt Ensembles: Model Uncertainty Estimation for Black-Box Large Language Models"
authors: "Francesco Tonolini; Νικόλαος Αλέτρας; Jordan Massiah; Gabriella Kazai"
year: 2024
doi: "10.18653/v1/2024.findings-acl.728"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.8
---
# Bayesian Prompt Ensembles: Model Uncertainty Estimation for Black-Box Large Language Models
**Authors**: Francesco Tonolini, Νικόλαος Αλέτρας, Jordan Massiah, Gabriella Kazai
**Year**: 2024
**Venue**: —
**DOI**: [10.18653/v1/2024.findings-acl.728](https://doi.org/10.18653/v1/2024.findings-acl.728)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.18653/v1/2024.findings-acl.728

---

## Abstract / 摘要

An important requirement for the reliable deployment of pre-trained large language models (LLMs) is the well-calibrated quantification of the uncertainty in their outputs.While the likelihood of predicting the next token is a practical surrogate of the data uncertainty learned during training, model uncertainty is challenging to estimate, i.e., due to lack of knowledge acquired during training.Prior efforts to quantify uncertainty of neural networks require specific architectures or (re-)training strategies, which are impractical to apply to LLMs with several billion parameters, or for black-box models where the architecture and parameters are not available.In this paper, we propose Bayesian Prompts Ensembles (BayesPE), a novel approach to effectively obtain wellcalibrated uncertainty for the output of pretrained LLMs.BayesPE computes output probabilities through a weighted ensemble of different, but semantically equivalent, task instruction prompts.The relative weights of the different prompts in the ensemble are estimated through approximate Bayesian variational inference over a small labeled validation set.We demonstrate that BayesPE approximates a Bayesian input layer for the LLM, providing a lower bound on the expected model error.In our extensive experiments, we show that BayesPE achieves significantly superior uncertainty calibration compared to several baselines over a range of natural language classification tasks, both in zero-and few-shot settings.Validation Samples


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.8)
- **Relevance**: 5.0 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 2.0 — Weak methodological signal
- **Recency/Impact**: 3.5 — Recent (2024), moderate visibility
- **Cluster**: calibration_metrics_theory
