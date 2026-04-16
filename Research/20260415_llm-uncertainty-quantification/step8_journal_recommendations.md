---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 8
gap: "GAP_002 — UQ for Multi-Step Reasoning (CoT) and Agentic/Tool-Use LLMs"
---

# Journal & Venue Recommendations / 投稿期刊與會議建議

> Topic / 研究主題: LLM Uncertainty Quantification — Step-Level UQ Propagation in Chain-of-Thought Reasoning
> Gap / 鎖定缺口: GAP_002
> Date / 日期: 2026-04-15

## Recommended Venues / 建議投稿目標

### Tier A: Top ML Conferences / 頂級機器學習會議

| Venue | Acceptance Rate | Page Limit | Deadline (approx.) | Fit / 契合度 |
|-------|----------------|------------|-------------------|-------------|
| **NeurIPS 2026** | ~24.5% | 9 pages + refs | May 2026 | ★★★★★ |
| **ICLR 2027** | ~28-32% | 9 pages + refs | Sep 2026 | ★★★★★ |
| **ICML 2026** | ~25-28% | 8 pages + refs | Jan 2026 (passed) | ★★★★☆ |

**NeurIPS** is the primary target. The uncertainty/reliability track at NeurIPS has grown significantly since 2023; Farquhar et al. 2024, Kuhn et al. 2023, and Xiong et al. 2024 all appeared at top ML venues. A May 2026 deadline aligns well with the 4-month project timeline (start now → experiments done by July → write in August → submit NeurIPS 2026 late track or ICLR 2027).

NeurIPS 為首選目標。自 2023 年起 NeurIPS 的不確定性/可靠性方向論文顯著增加；Farquhar、Kuhn、Xiong 等重要論文均發表於頂級 ML 會議。五月截止日期與四個月計畫時程吻合。

**ICLR 2027** is the fallback if NeurIPS timing doesn't work. Xiong et al. 2024's "Can LLMs Express Their Uncertainty?" was an ICLR oral — demonstrating the venue's receptiveness to this exact topic.

ICLR 2027 為備選，Xiong et al. 2024 於 ICLR 獲口頭報告——顯示此會議對此主題的接受度。

### Tier B: Top NLP Venues / 頂級自然語言處理會議與期刊

| Venue | Type | IF / Acceptance | Page Limit | Fit / 契合度 |
|-------|------|-----------------|------------|-------------|
| **ACL 2026** | Conference | ~23% acceptance | 8 pages + refs | ★★★★☆ |
| **EMNLP 2026** | Conference | ~25% acceptance | 8 pages + refs | ★★★★☆ |
| **TACL** | Journal (rolling) | IF 6.9 | ~15 pages | ★★★★★ |

**TACL (Transactions of the ACL)** is an excellent option for this work. Rolling submission means no deadline pressure. The journal format (15 pages) allows the full ablation study across 3 UQ methods × 4 aggregation functions × 3 tasks × 3 models to be presented comprehensively. Papers accepted at TACL also get an oral presentation slot at ACL/EMNLP/NAACL.

TACL（ACL 彙刊）為此研究的絕佳選擇。滾動投稿無截止壓力。期刊格式（15 頁）允許完整展示 3 種 UQ 方法 × 4 種聚合函數 × 3 項任務 × 3 個模型的消融研究。TACL 接受的論文同時獲得 ACL/EMNLP/NAACL 口頭報告機會。

**ACL/EMNLP** are strong alternatives if the paper is framed more toward NLP evaluation methodology. The CoT reasoning angle is highly relevant to the NLP community.

### Tier C: High-Impact Journals / 高影響力期刊

| Venue | Type | IF | Review Time | Fit / 契合度 |
|-------|------|-----|------------|-------------|
| **Nature Machine Intelligence** | Journal | 23.9 | 3-6 months | ★★★☆☆ |
| **JMLR** | Journal (rolling) | 6.0 | 3-9 months | ★★★★☆ |

**Nature Machine Intelligence** is aspirational. The work would need to demonstrate a surprising finding (e.g., "all existing UQ methods catastrophically fail on CoT reasoning" or "attention-weighted aggregation universally solves CoT UQ") to clear the novelty bar. Farquhar et al. 2024 (semantic entropy) was published in Nature — so there is precedent for UQ work at this venue, but that paper introduced a fundamentally new method rather than evaluating existing ones.

Nature Machine Intelligence 為挑戰性目標。需展示驚人發現才能通過新穎性門檻。Farquhar et al. 2024 於 Nature 發表語意熵——顯示 UQ 研究有此層級的先例，但該論文提出了全新方法而非評估現有方法。

**JMLR** is a solid journal option if the paper develops into a longer, more methodological piece with formal analysis of the aggregation functions.

---

## Recommended Strategy / 投稿策略

### Primary Path / 主要路徑

```
1. NeurIPS 2026 (deadline ~May 2026)
   ├── If accepted → done
   └── If rejected ↓
2. ICLR 2027 (deadline ~Sep 2026)
   ├── If accepted → done
   └── If rejected ↓
3. TACL (rolling, no deadline)
```

### Alternative Path / 替代路徑

If you prefer journal publication or need the longer format for the full ablation:

```
1. TACL (rolling)  ← start here
   └── Also get ACL/EMNLP presentation slot if accepted
```

### Timeline Alignment / 時程對齊

| Milestone / 里程碑 | Date / 日期 | Venue Window / 投稿窗口 |
|-------------------|-----------|----------------------|
| Framework design complete / 框架設計完成 | May 2026 | — |
| Core experiments done (GSM8K + StrategyQA) / 核心實驗完成 | Jul 2026 | NeurIPS 2026 late if available |
| Full experiments + writing / 全部實驗 + 撰寫 | Aug 2026 | ICLR 2027 prep |
| Paper submission / 論文投稿 | Sep 2026 | ICLR 2027 or TACL |
| Revised submission / 修訂投稿 | Nov 2026 | TACL or EMNLP 2027 |

---

## Open Access Considerations / 開放取用考量

- **NeurIPS/ICLR/ACL/EMNLP**: All proceedings are freely available on the conference websites and OpenReview. De facto open access.
- **TACL**: Published by MIT Press, open access.
- **Nature Machine Intelligence**: Requires APC (~$11,590 USD) for gold OA; otherwise 6-month embargo. Check institutional funding.
- **JMLR**: Fully open access, no APC.
- **arXiv preprint**: Regardless of venue choice, post an arXiv preprint at submission time to establish priority. This is standard practice in ML/NLP.

所有推薦的 ML/NLP 會議論文集均免費公開。TACL 為開放取用。Nature Machine Intelligence 需文章處理費（~$11,590 USD）。無論選擇哪個場所，投稿時同步上傳 arXiv 預印本以確立優先權。

---

## Venue-Specific Framing Advice / 場所特定定位建議

| Venue | Emphasis / 強調重點 | De-emphasize / 淡化 |
|-------|-------------------|-------------------|
| **NeurIPS/ICLR** | Novel framework; aggregation function analysis; multi-task generalization | Survey/review aspects |
| **ACL/EMNLP** | NLP reasoning evaluation; CoT reliability; practical implications for LLM deployment | Formal mathematical framework |
| **TACL** | Comprehensive empirical study; ablation depth; formal analysis of aggregation properties | Breadth claims beyond CoT |
| **Nature MI** | Surprising finding; broad impact narrative ("LLMs deployed in reasoning are unreliable and here's why") | Technical depth of aggregation variants |

---

Files / 檔案: `step8_hypothesis_specification.md`, `step8_journal_recommendations.md`
Next step / 下一步: Checkpoint 4 approval → Step 9 (`research-write`)
