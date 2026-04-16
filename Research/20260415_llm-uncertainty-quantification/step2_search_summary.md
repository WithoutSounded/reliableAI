---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 2
---

# Search Summary / 搜尋摘要

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Sources / 資料來源: Semantic Scholar, OpenAlex, arXiv (partial)
> Date / 搜尋日期: 2026-04-15

## Results / 搜尋結果

| Stage | Count |
|-------|------:|
| Raw records fetched / 原始紀錄 | 247 |
| After deduplication / 去重後 | 242 |
| After topical relevance filter / 主題過濾後 | **67** |
| User-identified seed papers recovered / 使用者預設 10 篇全數命中 | **10/10** |

### Contribution by Query / 各查詢貢獻

| Query | Strategy / 策略 | Papers contributed (first-found) |
|-------|----------|-------:|
| Q1 | Core terms + Population / 核心詞 | 60 raw → topical subset |
| Q2 | Synonyms + Method names / 方法名 | 30 raw (OpenAlex only; SS rate-limited) |
| Q3 | Mechanism + Theory / 機制與理論 | 58 raw → topical subset |
| Q4 | Metrics + Benchmarks / 指標與基準 | 23 raw (OpenAlex only; SS rate-limited) |
| Q5 | Attention-based + emerging / 注意力與新興方向 | 28 raw (OpenAlex only; SS rate-limited) |
| Direct seed lookup / 直接查詢 | User-identified 8 seed DOIs | 8 |
| Snowball / 滾雪球 | Top-cited seeds' referenced_works | 35 |

### Coverage / 覆蓋率指標

- **DOI coverage / DOI 覆蓋**: 65/67 (97%)
- **Sources breakdown / 來源分布**: OpenAlex 60 papers, Semantic Scholar 7 papers
- **Overlap / 跨源重疊**: 0% (see note on rate-limiting below)

## Hub Papers / 核心文獻

Papers with in-degree ≥ 3 in the internal citation network. These are papers that multiple other collection members cite — they anchor the literature.

1. **paper_001** — "Survey of Hallucination in Natural Language Generation" (Ji et al. 2022)
   - in_degree = 4 | external citations = 3,064
   - 幻覺研究的經典綜述，多數後續 LLM UQ 文獻皆引用。
2. **paper_007** — "Language Models (Mostly) Know What They Know" (Kadavath et al. 2022) **[USER-SEED]**
   - in_degree = 3 | external citations = 159
   - P(True) 自評估起源；使用者指定奠基論文之一。

> 備註 / Note: 內部 citation 連結稀疏（許多 2024–2026 年 arXiv 預印本 OpenAlex 尚未登錄其 referenced_works）。後續 Step 3 screening + Step 6 SOTA 整合會進一步建立主題連結。

## User-Identified Seed Papers / 使用者指定奠基論文

All 10 present in the final collection / 全部 10 篇均已納入最終集合：

| # | Paper ID | Title | Year | Cites |
|---|----------|-------|------|------:|
| 1 | paper_007 | Language Models (Mostly) Know What They Know (Kadavath) | 2022 | 159 |
| 2 | paper_004 | Detecting hallucinations via semantic entropy (Farquhar, Nature) | 2024 | 514 |
| 3 | paper_017 | Teaching Models to Express Their Uncertainty in Words (Lin) | 2022 | 54 |
| 4 | paper_019 | Semantic Uncertainty: Linguistic Invariances (Kuhn) | 2023 | 49 |
| 5 | paper_018 | Can LLMs Express Their Uncertainty? (Xiong, ICLR 2024) | 2024 | 50 |
| 6 | paper_040 | Just Ask for Calibration (Tian) | 2023 | 5 |
| 7 | paper_031 | Shifting Attention to Relevance / SAR (Duan) | 2024 | 10 |
| 8 | paper_005 | SelfCheckGPT (Manakul) | 2023 | 299 |
| 9 | paper_045 | Survey of Confidence Estimation & Calibration in LLMs (Geng) | 2024 | 2 |
| 10 | paper_024 | Survey on UQ Methods for Deep Learning (Huang) | 2024 | 26 |

## Citation Clusters / 引用聚類

Thematic clusters assigned from title + abstract content. Aligns well with user's research direction map in `LLM Uncertainty Quantification.md`.

| Cluster | Size | Theme / 主題 |
|---------|-----:|----------|
| `calibration_metrics_theory` | 15 | Calibration metrics (ECE/Brier) & selective prediction / 校準指標與選擇性預測 |
| `epistemic_aleatoric` | 13 | Epistemic vs aleatoric decomposition / 認知/偶然不確定性分解 |
| `hallucination_detection` | 9 | Hallucination detection & factuality / 幻覺偵測與事實性 |
| `verbalized_self_confidence` | 8 | Verbalized confidence & P(True) self-evaluation / 語言化信心 |
| `attention_internal_signals` | 7 | **Attention-based & internal-state UQ** (user priority) / 基於注意力/內部狀態 |
| `retrieval_agentic` | 5 | RAG & agentic/tool-use UQ / 檢索與代理式不確定性 |
| `general_uq` | 4 | General UQ methods / 一般方法 |
| `survey_position` | 2 | Surveys / 綜述 |
| `consistency_sampling` | 2 | Consistency-based sampling / 一致性取樣 |
| `semantic_entropy_family` | 1 | Semantic entropy family / 語意熵族 |
| `domain_application` | 1 | Domain applications (medical/code) / 領域應用 |

> The `attention_internal_signals` cluster (7 papers) directly supports your priority direction. The `retrieval_agentic` cluster (5 papers) covers the agentic/tool-use frontier.
> 「基於注意力／內部狀態訊號」7 篇對應你的優先方向；「RAG/代理」5 篇覆蓋代理式 LLM UQ 新興前沿。

## Yield Assessment / 產量評估

**English**: The target range was 30–60 papers after deduplication; we settled on **67 topically-filtered papers** with all 10 user-identified seeds recovered and 11 thematic clusters covering every research direction listed in your scoping document. DOI coverage is excellent at 97%. Two sources were partially degraded: Semantic Scholar rate-limited Q2/Q4/Q5, and arXiv's public API returned "Rate exceeded" for every attempt in this session. This is compensated by (a) OpenAlex returning all 5 queries successfully, (b) direct DOI lookup of 8 user-specified seeds, and (c) snowball expansion from top-cited seeds contributing 35 additional relevant papers. The collection is strong enough to proceed to screening without re-running the search.

**繁體中文**: 目標為去重後 30–60 篇，最終取得 **67 篇主題相關論文**。使用者預設的 10 篇奠基論文 100% 命中，11 個主題聚類涵蓋你規劃文件中每一條研究方向；DOI 覆蓋率 97%。兩個資料源部分受限：Semantic Scholar 的 Q2/Q4/Q5 查詢被限流，arXiv API 全程回傳「Rate exceeded」。我們以以下三點補償：(1) OpenAlex 五條查詢皆成功；(2) 直接以 DOI 查詢 8 篇使用者指定奠基論文；(3) 由高引用 seed 論文滾雪球抓出 35 篇新引用。文獻集合足以進入 Step 3 篩選，不需重跑搜尋。

### Known Gaps / 已知缺口

- Semantic Scholar contribution is limited to Q1/Q3 (cached from earlier calls). Step 5 (full-text retrieval) will fill in SS metadata as needed.
- arXiv did not contribute directly; however, most arXiv papers on this topic are mirrored in OpenAlex via their arXiv DOIs (`10.48550/arXiv.*`), so coverage is largely preserved.
- A second-round search could be triggered later (`/research step 2`) once rate limits reset if user wants broader coverage of very recent 2025–2026 arXiv papers.

---

Files / 檔案: `step2_raw_papers.json`, `step2_search_summary.md`
Next step / 下一步: `/research continue` → Step 3 (`research-screen`) for quality-filtered shortlist.
