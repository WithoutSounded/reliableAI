---
citation_key: "ZhouEtAl2025"
title: "Can LLMs Detect Their Confabulations? Estimating Reliability in Uncertainty-Aware Language Models"
authors: "Tianyi Zhou; Johanne Medina; S. Chawla"
year: 2025
doi: "10.48550/arxiv.2508.08139"
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
arxiv_id: "2508.08139"
tier: 3
composite_score: 3.6
---
# Can LLMs Detect Their Confabulations? Estimating Reliability in Uncertainty-Aware Language Models
**Authors**: Tianyi Zhou, Johanne Medina, S. Chawla
**Year**: 2025
**Venue**: —
**DOI**: [10.48550/arxiv.2508.08139](https://doi.org/10.48550/arxiv.2508.08139)

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

**DOI link / 連結**: https://doi.org/10.48550/arxiv.2508.08139

---

## Abstract / 摘要

Large Language Models (LLMs) are prone to generating fluent but incorrect content, known as confabulation, which poses increasing risks in multi-turn or agentic applications where outputs may be reused as context. In this work, we investigate how in-context information influences model behavior and whether LLMs can identify their unreliable responses. We propose a reliability estimation that leverages token-level uncertainty to guide the aggregation of internal model representations. Specifically, we compute aleatoric and epistemic uncertainty from output logits to identify salient tokens and aggregate their hidden states into compact representations for response-level reliability prediction. Through controlled experiments on open QA benchmarks, we find that correct in-context information improves both answer accuracy and model confidence, while misleading context often induces confidently incorrect responses, revealing a misalignment between uncertainty and correctness. Our probing-based method captures these shifts in model behavior and improves the detection of unreliable outputs across multiple open-source LLMs. These results underscore the limitations of direct uncertainty signals and highlight the potential of uncertainty-guided probing for reliability-aware generation.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.6)
- **Relevance**: 4.0 — Directly addresses LLM uncertainty or calibration
- **Quality**: 3.0 — Standard empirical methodology
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: attention_internal_signals
