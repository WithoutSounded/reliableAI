---
citation_key: "BadashEtAl2026"
title: "Between the Layers Lies the Truth: Uncertainty Estimation in LLMs Using Intra-Layer Local Information Scores"
authors: "Zvi Badash; Yonatan Belinkov; Moti Freiman"
year: 2026
doi: ""
source: "abstract-only (shortlist metadata)"
access_level: "abstract-only"
retrieved_date: "2026-04-15"
tier: 2
composite_score: 4.0
---
# Between the Layers Lies the Truth: Uncertainty Estimation in LLMs Using Intra-Layer Local Information Scores
**Authors**: Zvi Badash, Yonatan Belinkov, Moti Freiman
**Year**: 2026
**Venue**: ArXiv.org
**DOI**: —

> **Note / 備註**: Full text not retrieved in this pipeline run (Tier 2/3 paper). Abstract included below from screening metadata. For deep analysis, retrieve via DOI.
> 此論文未取得全文（Tier 2/3）。以下為篩選階段保留的摘要；如需深入分析請透過 DOI 取得。

---

## Abstract / 摘要

Large language models (LLMs) are often confidently wrong, making reliable uncertainty estimation (UE) essential. Output-based heuristics are cheap but brittle, while probing internal representations is effective yet high-dimensional and hard to transfer. We propose a compact, per-instance UE method that scores cross-layer agreement patterns in internal representations using a single forward pass. Across three models, our method matches probing in-distribution, with mean diagonal differences of at most $-1.8$ AUPRC percentage points and $+4.9$ Brier score points. Under cross-dataset transfer, it consistently outperforms probing, achieving off-diagonal gains up to $+2.86$ AUPRC and $+21.02$ Brier points. Under 4-bit weight-only quantization, it remains robust, improving over probing by $+1.94$ AUPRC points and $+5.33$ Brier points on average. Beyond performance, examining specific layer--layer interactions reveals differences in how disparate models encode uncertainty. Altogether, our UE method offers a lightweight, compact means to capture transferable uncertainty in LLMs.


## Screening Notes / 篩選備註

- **Tier**: 2 (composite 4.0)
- **Relevance**: 4.5 — Direct LLM-UQ match across multiple core phrases
- **Quality**: 3.5 — Standard empirical methodology
- **Recency/Impact**: 3.5 — Very recent (2026), cites still accruing
- **Cluster**: attention_internal_signals
