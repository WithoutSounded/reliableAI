---
citation_key: "GhasemabadiNiu2025"
title: "Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits"
authors: "Amirhosein Ghasemabadi; Di Niu"
year: 2025
doi: ""
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 3
composite_score: 3.85
---
# Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits
**Authors**: Amirhosein Ghasemabadi, Di Niu
**Year**: 2025
**Venue**: ArXiv.org
**DOI**: —

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

---

## Abstract / 摘要

Large language models (LLMs) generate fluent and complex outputs but often fail to recognize their own mistakes and hallucinations. Existing approaches typically rely on external judges, multi-sample consistency, or text-based self-critique, which incur additional compute or correlate weakly with true correctness. We ask: can LLMs predict their own failures by inspecting internal states during inference? We introduce Gnosis, a lightweight self-awareness mechanism that enables frozen LLMs to perform intrinsic self-verification by decoding signals from hidden states and attention patterns. Gnosis passively observes internal traces, compresses them into fixed-budget descriptors, and predicts correctness with negligible inference cost, adding only ~5M parameters and operating independently of sequence length. Across math reasoning, open-domain question answering, and academic knowledge benchmarks, and over frozen backbones ranging from 1.7B to 20B parameters, Gnosis consistently outperforms strong internal baselines and large external judges in both accuracy and calibration. Moreover, it generalizes zero-shot to partial generations, enabling early detection of failing trajectories and compute-aware control. These results show that reliable correctness cues are intrinsic to generation process and can be extracted efficiently without external supervision.


## Screening Notes / 篩選備註

- **Tier**: 3 (composite 3.85)
- **Relevance**: 4.5 — User-priority direction: attention/internal-state UQ for LLMs
- **Quality**: 3.0 — Limited methodological detail in abstract
- **Recency/Impact**: 3.5 — Very recent (2025), cites still accruing
- **Cluster**: attention_internal_signals
