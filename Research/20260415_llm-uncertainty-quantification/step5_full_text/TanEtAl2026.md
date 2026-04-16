---
citation_key: "TanEtAl2026"
title: "BaseCal: Unsupervised Confidence Calibration via Base Model Signals"
authors: "Hexiang Tan; Wanli Yang; Junwei Zhang; Xin Chen; Rui Tang; Du Su; Jingang Wang; Yuanzhuo Wang; Fei Sun; Xueqi Cheng"
year: 2026
doi: ""
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.6
---
# BaseCal: Unsupervised Confidence Calibration via Base Model Signals
**Authors**: Hexiang Tan, Wanli Yang, Junwei Zhang, Xin Chen, Rui Tang, Du Su, Jingang Wang, Yuanzhuo Wang, Fei Sun, Xueqi Cheng
**Year**: 2026
**Venue**: arXiv (Cornell University)
**DOI**: —

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

---

## Abstract / 摘要

Reliable confidence is essential for trusting the outputs of LLMs, yet widely deployed post-trained LLMs (PoLLMs) typically compromise this trust with severe overconfidence. In contrast, we observe that their corresponding base LLMs often remain well-calibrated. This naturally motivates us to calibrate PoLLM confidence using the base LLM as a reference. This work proposes two ways to achieve this. A straightforward solution, BaseCal-ReEval, evaluates PoLLM's responses by feeding them into the base LLM to get average probabilities as confidence. While effective, this approach introduces additional inference overhead. To address this, we propose BaseCal-Proj, which trains a lightweight projection to map the final-layer hidden states of PoLLMs back to those of their base LLMs. These projected states are then processed by the base LLM's output layer to derive base-calibrated confidence for PoLLM's responses. Notably, BaseCal is an unsupervised, plug-and-play solution that operates without human labels or LLM modifications. Experiments across five datasets and three LLM families demonstrate the effectiveness of BaseCal, reducing Expected Calibration Error (ECE) by an average of 42.90\% compared to the best unsupervised baselines.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.6)
- **Relevance**: 4.0 — Directly addresses LLM uncertainty or calibration
- **Quality**: 3.0 — Limited methodological detail in abstract
- **Recency/Impact**: 3.5 — Very recent (2026), cites still accruing
- **Cluster**: calibration_metrics_theory
