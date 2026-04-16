# Reliable AI — LLM Uncertainty Quantification Research

本專案是一個以 **LLM 可靠性（Reliable AI）** 為核心的研究工作區，聚焦於大型語言模型的不確定性量化（Uncertainty Quantification）。包含潛在指導教授的論文研讀、系統性文獻調研、以及研究假說的建立。

## 專案結構

```
.
├── paper/                          # Prof. Tianhao Wang 論文集（18 篇 PDF）
├── professor_tianhao_wang_profile.md  # 王天浩教授研究側寫（中英對照）
├── LLM Uncertainty Quantification.md  # UQ 研究指南（關鍵字、必讀論文、可切入方向）
├── Research/
│   └── 20260415_llm-uncertainty-quantification/   # 系統性文獻調研 session
│       ├── step0_session_config.json       # PICO 框架 & 搜尋策略設定
│       ├── step1_search_queries.md         # 5 組策略性搜尋查詢
│       ├── step2_raw_papers.json           # 原始搜尋結果
│       ├── step2_search_summary.md         # 搜尋摘要
│       ├── step3_screening_results.md      # 篩選結果（含納入/排除理由）
│       ├── step3_shortlist.json            # 篩選後候選論文
│       ├── step4_citation_keys.md          # 引用鍵對照表
│       ├── step4_references.bib            # BibTeX 參考文獻
│       ├── step4_references_apa.md         # APA 7 格式參考文獻
│       ├── step5_full_text/                # 全文 PDF 下載（12+ 篇）
│       ├── full_pdf/                       # 額外全文 PDF
│       ├── step6_knowledge_graph.canvas    # 知識圖譜（Obsidian Canvas）
│       ├── step6_sota_review.md            # SOTA 綜述（45 篇，6 大主題）
│       ├── step7_gap_analysis.md           # 研究缺口分析（3 個結構性缺口）
│       ├── step8_hypothesis_specification.md  # 假說規格書
│       ├── step8_journal_recommendations.md   # 投稿期刊建議
│       └── step9_manuscript/               # 論文稿件（撰寫中）
│           └── 01_intro.tex
└── hello.py                        # 測試腳本
```

## 研究主題

### 核心問題：LLM 不確定性量化（UQ）

現有 LLM UQ 方法（語意熵、語言化信心、注意力訊號等）均在單輪短格式 QA 上驗證，但真實部署以**多步推理（CoT）**與**代理式管線（Agentic）**為主。本研究探討不確定性如何在連續推理步驟中傳播。

### 四大方法流派

| # | 流派 | 代表方法 |
|---|------|---------|
| 1 | 取樣式語意一致性 | Semantic Entropy, SelfCheckGPT |
| 2 | 語言化信心 / 自我探測 | P(True), Verbalized Confidence |
| 3 | 注意力 / 內部狀態訊號 | SAR, InternalInspector |
| 4 | 校準 / 保形預測框架 | Conformal Prediction, Selective Prediction |

### 鎖定缺口（GAP_002）

**UQ for Multi-Step Reasoning (CoT) and Agentic/Tool-Use LLMs**
- 形式化 CoT 推理的步驟級不確定性傳播
- 評估現有 UQ 方法在逐步應用時是否保持區辨力
- 測試聚合函數（乘積規則、最大步驟、注意力加權、學習式聚合）
- 評估平台：GSM8K、StrategyQA、ToolBench

### 投稿目標

- **首選**：NeurIPS 2026 / ICLR 2027
- **備選**：AAAI 2027 / AISTATS 2027

## 教授側寫：Tianhao Wang（王天浩）

UC San Diego HDSI 助理教授（2025 秋起），Yale 統計與資料科學博士。三條研究主線：

1. **AMP 普適性理論** — 以 tensor network + moment method 推廣 AMP 到異質方差、重尾、非可分離非線性
2. **Transformer 訓練動力學 & ICL 理論** — 多頭 softmax attention 收斂證明、induction head 機制、隱式正則化
3. **LLM 可靠性 / 對齊** — Reinforced Hesitation（三元獎勵棄權訓練）、SAE 可證特徵恢復、感知瓶頸分析

`paper/` 目錄包含其 17 篇獨立論文 + 博士論文，詳見 [professor_tianhao_wang_profile.md](professor_tianhao_wang_profile.md)。

## 文獻調研進度

| Step | 內容 | 狀態 |
|------|------|------|
| 0 | PICO 框架 & Session 設定 | Done |
| 1 | 搜尋策略 & 查詢生成 | Done |
| 2 | 跨資料庫搜尋（Semantic Scholar, OpenAlex, PubMed, arXiv） | Done |
| 3 | 論文篩選 & 品質評估 | Done |
| 4 | 參考文獻匯出（BibTeX + APA 7） | Done |
| 5 | 全文下載 | Done |
| 6 | SOTA 綜述 & 知識圖譜 | Done |
| 7 | 研究缺口分析 | Done |
| 8 | 假說規格書 & 期刊建議 | Done |
| 9 | 論文撰寫（Introduction） | In Progress |
