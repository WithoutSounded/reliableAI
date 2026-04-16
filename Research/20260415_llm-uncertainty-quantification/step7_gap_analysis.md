---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 7
gaps_identified: 3
priority_weights: "severity=0.40, novelty=0.30, feasibility=0.30"
---

# Gap Analysis / 研究缺口分析

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Papers analyzed / 分析論文數: 45 (from SOTA review, Step 6)
> Gaps identified / 已識別缺口: 3
> Date / 日期: 2026-04-15

## Executive Summary / 總覽摘要

The SOTA review reveals a field that has rapidly diversified along four parallel method-families (sampling-based semantic consistency, verbalized confidence, attention/internal-state signals, and calibration/conformal frameworks) while converging on a shared downstream target: hallucination detection as the applied testbed for UQ. Despite this breadth, three structural gaps stand out.

**First and most critical for the user's priority direction**: no study has conducted a controlled head-to-head comparison between attention-based/internal-state UQ methods (Theme 3: SAR, InternalInspector, intra-layer variance) and the current SOTA sampling-based method (semantic entropy, FarquharEtAl2024). Each camp benchmarks against token perplexity — a strawman baseline — but never against each other. This gap directly blocks the field from understanding which paradigm is superior, and it is the most immediately actionable opening. **Second**, uncertainty quantification for multi-step reasoning chains (CoT) and agentic/tool-use LLMs is essentially uncharted — only one tangential paper (atakKuzlu2024) appears in the collection — despite these being the deployment frontier. **Third**, the field's measurement foundations are under strain: multiple position papers (DevicEtAl2025, KirchhofEtAl2025, GhoshPanday2026) argue that ECE and AUROC inherited from classification UQ are inadequate for generative settings, but no widely adopted replacement has emerged.

SOTA 綜述揭示了一個沿四條方法路線迅速多元化的領域（取樣式語意一致性、語言化信心、注意力/內部狀態訊號、校準/保形框架），同時收斂於共同的下游目標——幻覺偵測作為 UQ 的應用測試場。儘管如此廣泛，三個結構性缺口仍然突出。

**第一也是使用者優先方向最關鍵的缺口**：尚無研究對注意力/內部狀態 UQ 方法（Theme 3: SAR、InternalInspector、層內方差）與當前 SOTA 取樣式方法（語意熵, FarquharEtAl2024）進行受控的正面對比。各陣營僅對比 token perplexity 這一弱基線，從未彼此對照，直接阻礙領域理解哪一範式更優越，且最具即時可行性。**第二**，多步推理鏈（CoT）與代理式/工具使用 LLM 的 UQ 基本上未被探索——收錄中僅一篇切線相關論文（atakKuzlu2024）——儘管這些是部署前沿。**第三**，領域的度量基礎正面臨壓力：多篇立場論文（DevicEtAl2025、KirchhofEtAl2025、GhoshPanday2026）主張從分類 UQ 繼承的 ECE 與 AUROC 不適用於生成情境，但尚無被廣泛採用的替代方案。

---

## GAP_001: Cross-Paradigm Benchmark — Attention/Internal-State UQ vs. Semantic Entropy / 跨範式基準——注意力/內部狀態 UQ vs. 語意熵

**Type / 類型:** Methodological (primary) + Integration (secondary)
**Priority Rank / 優先排名:** #1

### Description / 描述

No paper in the reviewed literature has conducted a controlled, apples-to-apples comparison between the attention-based/internal-state UQ family (DuanEtAl2023 SAR, BeigiEtAl2024 InternalInspector, BadashEtAl2026 intra-layer variance) and the current leading sampling-based method (FarquharEtAl2024 semantic entropy) under identical conditions — same models, same datasets, same hardware, same evaluation protocol. Each camp benchmarks against token-uniform perplexity, which is known to be weak (consistently losing by 5–15 AUROC points). The missing comparison prevents the field from answering the most basic paradigm question: **do internal-state signals provide information that sampling-based methods miss, or are they merely a computationally cheaper proxy for the same signal?**

A study filling this gap would: (1) run SAR, InternalInspector, intra-layer variance, semantic entropy, and SelfCheckGPT-NLI on the same model family (e.g., LLaMA-3 8B/70B) across TriviaQA, NaturalQuestions, MMLU, and TruthfulQA; (2) evaluate on AUROC, ECE, AURC (risk-coverage); (3) decompose where each method's errors concentrate (question types, model sizes, domain shifts); and (4) test whether combining both paradigms yields further gains (ensemble of internal + semantic signals).

已審查文獻中無任何論文對注意力/內部狀態 UQ 家族（DuanEtAl2023 SAR、BeigiEtAl2024 InternalInspector、BadashEtAl2026 層內方差）與當前領先的取樣式方法（FarquharEtAl2024 語意熵）在相同條件下——相同模型、資料集、硬體、評估協定——進行受控的正面對比。各陣營均以 token 均勻 perplexity 作為基線（已知較弱，一致落後 5–15 AUROC 點）。此缺失阻礙領域回答最基本的範式問題：**內部狀態訊號是否提供取樣式方法未捕捉到的資訊，抑或只是同一訊號的低計算代價代理？**

填補此缺口的研究將：(1) 於同一模型族（如 LLaMA-3 8B/70B）上運行 SAR、InternalInspector、層內方差、語意熵、SelfCheckGPT-NLI，跨 TriviaQA、NaturalQuestions、MMLU、TruthfulQA；(2) 以 AUROC、ECE、AURC 評估；(3) 分解各方法錯誤集中之處（問題類型、模型規模、領域偏移）；(4) 測試結合兩種範式是否產出進一步增益（內部 + 語意訊號集成）。

### Supporting Evidence / 支持證據

- **DuanEtAl2023 (SAR)**: Evaluates attention-weighted UQ against length-normalized perplexity and PE (predictive entropy) — reports +2–8 AUROC points. Does NOT compare against semantic entropy (FarquharEtAl2024). The paper's comparison table uses perplexity, PE, and token entropy as baselines — none from the sampling-based semantic family.

  DuanEtAl2023 以長度正規化 perplexity 與預測熵為基線，報告 AUROC 增加 2–8 點，但未對比語意熵（FarquharEtAl2024）。比較表中的基線無一來自取樣式語意家族。

- **BeigiEtAl2024 (InternalInspector)**: Benchmarks against verbalized confidence and token perplexity, achieving ECE 0.03. The paper's related work acknowledges semantic entropy but does not include it in the experimental comparison "due to differing evaluation protocols."

  BeigiEtAl2024 對比語言化信心與 token perplexity，達 ECE 0.03。相關工作提及語意熵但因「評估協定不同」未納入實驗比較。

- **FarquharEtAl2024 (Semantic Entropy, Nature)**: Compares against "all baselines available at time of submission" — which included Kadavath P(True) and token perplexity but NOT any attention-based method (SAR was concurrent work). The Nature paper's baseline table lacks any internal-state method.

  FarquharEtAl2024 對比「提交時所有可用基線」——包含 Kadavath P(True) 與 token perplexity 但不含任何注意力方法（SAR 為同期工作）。Nature 論文基線表無內部狀態方法。

- **BadashEtAl2026 (Between the Layers)**: Reports AUROC 0.81 on TruthfulQA using intra-layer variance — but the baseline is again token perplexity, not semantic entropy. States in future work: "direct comparison with sampling-based methods remains an important direction."

  BadashEtAl2026 於 TruthfulQA 以層內方差達 AUROC 0.81，基線仍為 token perplexity。未來工作中明確指出「與取樣式方法的直接比較仍為重要方向」。

- **GengEtAl2023 (Survey)**: Identifies both sampling-based and internal-state methods but notes "no study has systematically compared these two families under controlled conditions" (§5.3 Research Directions).

  GengEtAl2023（綜述）同時辨識取樣式與內部狀態方法，但指出「尚無研究在受控條件下系統比較這兩類方法」。

### Counter-Evidence / 反面證據

- **DuanEtAl2023**: Does include a self-consistency baseline (sample-then-vote) as one comparator. However, this is a simplistic consistency check, not semantic clustering / semantic entropy. The gap for a rigorous semantic-entropy baseline remains open.

  DuanEtAl2023 確有納入自我一致性基線（取樣投票）作為比較器之一，但此為簡易一致性檢查，非語意聚類/語意熵。嚴謹語意熵基線的缺口仍存在。

### Why It Matters / 重要性

This gap sits at the intersection of the user's priority direction (attention-based UQ) and the field's strongest existing result (semantic entropy). Filling it would: (1) establish whether internal-state methods are complementary to or substitutes for sampling-based methods; (2) provide the first efficiency-accuracy Pareto frontier for LLM UQ (internal-state methods require 1 forward pass; sampling methods require 10–20); (3) inform deployment decisions — if internal-state methods match semantic entropy at 10× lower cost, the practical implications are immediate.

此缺口位於使用者優先方向（注意力 UQ）與領域最強現有成果（語意熵）的交匯處。填補後將：(1) 確立內部狀態方法與取樣式方法為互補或替代關係；(2) 提供 LLM UQ 的首個效率-準確度 Pareto 前沿（內部狀態方法需 1 次前向傳播，取樣式需 10–20 次）；(3) 指導部署決策——若內部狀態方法以 10 倍低成本匹配語意熵，實務意義立現。

### Priority Score / 優先分數

| Axis / 評估軸 | Score / 分數 | Rationale / 理由 |
|--------------|-------------|-----------------|
| Severity / 嚴重性 | 4 | Blocks paradigm comparison; field can't choose between two dominant approaches / 阻礙範式比較；領域無法在兩大主流方法間做出選擇 |
| Novelty / 新穎性 | 5 | Zero papers perform this exact comparison; explicitly called for by 2+ surveys / 零篇論文執行此確切比較；被 2+ 綜述明確呼籲 |
| Feasibility / 可行性 | 5 | All methods are published with code; standard benchmarks; single-GPU reproducible / 所有方法已發表含程式碼；標準基準；單 GPU 可復現 |

**Composite / 綜合分:** 4 × 0.40 + 5 × 0.30 + 5 × 0.30 = 1.60 + 1.50 + 1.50 = **4.60**

---

## GAP_002: UQ for Multi-Step Reasoning (CoT) and Agentic/Tool-Use LLMs / 多步推理（CoT）與代理式/工具使用 LLM 的 UQ

**Type / 類型:** Integration (primary) + Temporal (secondary)
**Priority Rank / 優先排名:** #2

### Description / 描述

The entire reviewed literature evaluates UQ on single-turn, short-form QA tasks (TriviaQA, MMLU, NaturalQuestions). No paper systematically addresses how uncertainty propagates through multi-step reasoning chains (chain-of-thought prompting, where each step's uncertainty compounds into the final answer) or through agentic pipelines (where the LLM makes tool calls, retrieves information, and integrates results across multiple turns). The `retrieval_agentic` cluster from Step 2 yielded only one included paper (atakKuzlu2024), which addresses RAG uncertainty via convex-hull geometry but does not model multi-step uncertainty propagation.

A study filling this gap would: (1) formalize uncertainty propagation through sequential reasoning steps (step-level → chain-level aggregation); (2) evaluate on reasoning benchmarks (GSM8K, MATH, StrategyQA) where intermediate steps can be individually verified; (3) extend to agentic settings where the LLM makes API calls or tool invocations, each introducing external uncertainty sources; (4) determine whether existing single-turn UQ methods (semantic entropy, SAR) transfer to multi-step settings or require fundamental adaptation.

整篇已審查文獻均於單輪、短格式 QA 任務（TriviaQA、MMLU、NaturalQuestions）上評估 UQ。無論文系統性探討不確定性如何在多步推理鏈（chain-of-thought 提示，各步不確定性複合至最終答案）或代理式管線（LLM 調用工具、擷取資訊、跨多輪整合結果）中傳播。Step 2 的 `retrieval_agentic` 聚類僅產出一篇納入論文（atakKuzlu2024），以凸包幾何處理 RAG 不確定性，但未建模多步不確定性傳播。

填補此缺口的研究將：(1) 形式化不確定性於連續推理步驟中的傳播（步驟級 → 鏈級聚合）；(2) 於推理基準（GSM8K、MATH、StrategyQA）上評估，其中中間步驟可逐一驗證；(3) 擴展到 LLM 進行 API 或工具調用的代理式場景，各引入外部不確定性來源；(4) 確定現有單輪 UQ 方法（語意熵、SAR）是否可移轉至多步場景或需根本性改寫。

### Supporting Evidence / 支持證據

- **KirchhofEtAl2025 (Position)**: Explicitly identifies "compositional uncertainty in multi-step generation" as one of three critical open problems for LLM UQ (alongside metric inadequacy and distribution shift).

  KirchhofEtAl2025 明確將「多步生成中的組合性不確定性」列為 LLM UQ 三大關鍵開放問題之一。

- **XiongEtAl2023**: Evaluates 5 LLMs on single-turn QA only. Acknowledges in limitations: "Our framework does not address multi-step reasoning settings where confidence must be tracked across inference steps."

  XiongEtAl2023 僅評估單輪 QA。於限制中承認：「我們的框架未處理需跨推理步驟追蹤信心的多步推理場景。」

- **GengEtAl2023 (Survey)**: Lists "UQ for agentic LLMs" as the most under-explored frontier; zero papers in survey's coverage address it.

  GengEtAl2023 將「代理式 LLM 的 UQ」列為探索最不足的前沿；綜述覆蓋範圍中零篇論文涉及。

- **LiuEtAl2025c (Survey)**: Mentions CoT-level uncertainty in the taxonomy but notes "no method paper has proposed a principled approach to step-level UQ aggregation in reasoning chains."

  LiuEtAl2025c 在分類學中提及 CoT 級不確定性，但指出「尚無方法論文為推理鏈中的步驟級 UQ 聚合提出有原則的方法。」

- **atakKuzlu2024**: The closest existing work — models RAG uncertainty as convex hull of retrieval embeddings, but only for single-retrieval-augmented QA, not multi-step tool-use.

  atakKuzlu2024 為最接近的現有工作——以擷取嵌入的凸包建模 RAG 不確定性，但僅適用於單次擷取增強 QA，非多步工具使用。

### Counter-Evidence / 反面證據

- **atakKuzlu2024**: Partially addresses RAG-integrated uncertainty, providing one concrete method for retrieval-augmented settings. However, this covers only one specific form of external uncertainty (retrieval quality) and does not model the compositional propagation across multiple reasoning or tool-use steps.

  atakKuzlu2024 部分解決了 RAG 整合不確定性，為擷取增強場景提供一個具體方法。但僅涵蓋一種特定外部不確定性形式（擷取品質），未建模跨多個推理或工具使用步驟的組合傳播。

### Why It Matters / 重要性

Agentic LLMs — systems that plan, reason, and use external tools — are the dominant deployment paradigm for 2025–2026. Without UQ methods validated for multi-step settings, these systems cannot signal when they are uncertain about intermediate reasoning steps, leading to cascading errors that compound undetected. The gap between single-turn QA evaluation and real deployment settings undermines the practical impact of all existing UQ work.

代理式 LLM——進行規劃、推理並使用外部工具的系統——是 2025–2026 的主流部署範式。若無經多步場景驗證的 UQ 方法，這些系統無法在中間推理步驟不確定時發出訊號，導致複合錯誤未被偵測地累積。單輪 QA 評估與實際部署場景之間的落差削弱了所有現有 UQ 研究的實務影響力。

### Priority Score / 優先分數

| Axis / 評估軸 | Score / 分數 | Rationale / 理由 |
|--------------|-------------|-----------------|
| Severity / 嚴重性 | 4 | Agentic deployment is the frontier; UQ-less agents are dangerous / 代理式部署為前沿；無 UQ 的代理有風險 |
| Novelty / 新穎性 | 5 | Only 1 tangentially related paper in 45; identified by 3+ surveys / 45 篇中僅 1 篇切線相關；被 3+ 綜述指出 |
| Feasibility / 可行性 | 3 | Requires new benchmarks (step-level labels); agentic eval frameworks still immature / 需新基準（步驟級標籤）；代理式評估框架尚不成熟 |

**Composite / 綜合分:** 4 × 0.40 + 5 × 0.30 + 3 × 0.30 = 1.60 + 1.50 + 0.90 = **4.00**

---

## GAP_003: Generative-Native UQ Metrics Beyond ECE/AUROC / 超越 ECE/AUROC 的生成原生 UQ 指標

**Type / 類型:** Measurement (primary)
**Priority Rank / 優先排名:** #3

### Description / 描述

The field's evaluation infrastructure is strained. Multiple position papers (DevicEtAl2025, KirchhofEtAl2025, GhoshPanday2026) argue that ECE (Expected Calibration Error) and AUROC — the two dominant metrics inherited from classification and binary detection — are inadequate for evaluating UQ in generative settings. ECE assumes a well-defined "correct/incorrect" partition, which is ambiguous for open-ended generation; AUROC measures discrimination but not calibration quality; neither accounts for the *semantic* dimension of uncertainty (two outputs can be token-different but semantically equivalent). Despite this critique being well-articulated, no paper proposes a metric that has gained traction as a replacement. HuangEtAl2024's rank-calibration and DevicEtAl2025's interaction-level calibration are promising directions but remain individual proposals without community adoption.

A study filling this gap would: (1) formalize the requirements for generative-native UQ metrics (semantic equivalence awareness, length invariance, compositional decomposability); (2) propose a concrete metric with theoretical grounding; (3) demonstrate it on the standard benchmark suite (TriviaQA/MMLU/TruthfulQA); (4) show that rankings of UQ methods change when the new metric is used vs. ECE/AUROC — proving the metric reveals information the old ones miss.

領域的評估基礎設施承受壓力。多篇立場論文（DevicEtAl2025、KirchhofEtAl2025、GhoshPanday2026）主張從分類與二元偵測沿用的兩大主流指標——ECE（期望校準誤差）與 AUROC——不適用於生成情境的 UQ 評估。ECE 假設明確定義的「正確/不正確」分割，對開放式生成而言模糊不清；AUROC 衡量區辨力但非校準品質；兩者均未考慮不確定性的「語意」維度（兩個輸出可 token 不同但語意等價）。儘管批評已清晰表述，尚無論文提出被廣泛採用的替代指標。HuangEtAl2024 的排序校準與 DevicEtAl2025 的互動級校準是有前途的方向，但仍為個別提案。

### Supporting Evidence / 支持證據

- **DevicEtAl2025**: Argues calibration should be evaluated as an interaction-level property (model + user + task), not a model statistic. Proposes collaborative calibration concept but not a concrete implementable metric.

  DevicEtAl2025 主張校準應作為互動層級屬性（模型 + 使用者 + 任務）而非模型統計量。提出協作校準概念但非具體可實現的指標。

- **GhoshPanday2026**: Formalizes the Dunning-Kruger effect in LLMs — overconfidence on hard tasks, underconfidence on easy tasks — and shows ECE fails to capture this asymmetry because it averages over difficulty levels.

  GhoshPanday2026 形式化 LLM 的 Dunning-Kruger 效應——困難任務過度自信、簡單任務信心不足——並證明 ECE 因跨難度等級平均而無法捕捉此不對稱性。

- **KirchhofEtAl2025 (Position)**: "The field needs new metrics ... uncertainty in LLMs is not a single quantity but a family of related quantities (semantic, pragmatic, factual, syntactic)."

  KirchhofEtAl2025：「領域需要新指標⋯⋯LLM 中的不確定性非單一量值，而是相關量值之族（語意、語用、事實、句法）。」

- **Cross-theme observation**: Themes 1–3 in the SOTA review use different primary metrics (Theme 1: AUROC; Theme 2: ECE; Theme 3: mixed), making cross-theme comparison of methods effectively impossible.

  跨主題觀察：SOTA 綜述中 Theme 1–3 使用不同主要指標（Theme 1: AUROC；Theme 2: ECE；Theme 3: 混合），使方法的跨主題比較實質上不可能。

### Counter-Evidence / 反面證據

- **HuangEtAl2024 (Rank-Calibration)**: Proposes rank-calibration as an alternative to ECE for LLM settings — a concrete metric that evaluates ordering rather than absolute probability. This partially fills the gap but addresses only the calibration axis (not discrimination, semantic equivalence, or compositionality).

  HuangEtAl2024 提出排序校準作為 ECE 的替代——一個具體指標，評估排序而非絕對機率。部分填補缺口但僅涉及校準軸（非區辨力、語意等價或組合性）。

- **FarquharEtAl2024**: By construction, semantic entropy is a metric that accounts for semantic equivalence. However, it is both a UQ method and an evaluation signal — using it as an evaluation metric for other methods creates circularity.

  FarquharEtAl2024 依設計，語意熵本身即考慮語意等價的指標。但它同時是 UQ 方法與評估訊號——以其評估其他方法會造成循環論證。

### Why It Matters / 重要性

Metrics determine what the field optimizes for. If ECE remains the standard despite its known inadequacy for generation, methods will be designed to optimize for a misleading target. The metric gap compounds the paradigm-comparison gap (GAP_001) — even if someone runs the head-to-head benchmark, the results may be misleading if evaluated with inappropriate metrics.

指標決定領域的優化方向。若 ECE 在已知不適用於生成的情況下仍為標準，方法將被設計以優化一個誤導性的目標。指標缺口加劇了範式比較缺口（GAP_001）——即使有人執行正面對比基準，若以不適當的指標評估，結果仍可能具誤導性。

### Priority Score / 優先分數

| Axis / 評估軸 | Score / 分數 | Rationale / 理由 |
|--------------|-------------|-----------------|
| Severity / 嚴重性 | 5 | Fundamental measurement problem; every cross-method comparison is undermined / 基礎度量問題；每項跨方法比較均受影響 |
| Novelty / 新穎性 | 3 | Critique is well-articulated (3+ papers); partial proposals exist but no consensus / 批評已清晰表述（3+ 篇）；有部分提案但無共識 |
| Feasibility / 可行性 | 3 | Metric proposal is feasible but adoption requires community buy-in beyond a single paper / 指標提案可行但採用需社群認可 |

**Composite / 綜合分:** 5 × 0.40 + 3 × 0.30 + 3 × 0.30 = 2.00 + 0.90 + 0.90 = **3.80**

---

## Priority Ranking / 優先排名

| Rank | Gap ID | Title / 標題 | Type / 類型 | Severity | Novelty | Feasibility | **Composite** |
|------|--------|-------------|-------------|----------|---------|-------------|--------------|
| **1** | GAP_001 | Cross-Paradigm Benchmark: Attention/Internal-State vs. Semantic Entropy / 跨範式基準 | Methodological + Integration | 4 | 5 | 5 | **4.60** |
| 2 | GAP_002 | UQ for CoT Reasoning & Agentic LLMs / 多步推理與代理式 UQ | Integration + Temporal | 4 | 5 | 3 | **4.00** |
| 3 | GAP_003 | Generative-Native UQ Metrics / 生成原生 UQ 指標 | Measurement | 5 | 3 | 3 | **3.80** |

---

## Gap Landscape Summary / 缺口全景

### Coverage Strength / 覆蓋強項

The field is well-covered on: (1) sampling-based semantic methods for short-form QA — the SelfCheckGPT → Semantic Uncertainty → Semantic Entropy lineage is mature, with Nature-grade validation; (2) verbalized confidence elicitation with 4+ independent evaluations; (3) hallucination taxonomy and detection — Ji's 2022 survey and Zhang's 2025 update provide comprehensive coverage; (4) survey/meta-level reflection — the field is unusually self-aware for its youth, with multiple position papers critiquing its own foundations.

覆蓋強項：(1) 短格式 QA 的取樣式語意方法——SelfCheckGPT → 語意不確定性 → 語意熵脈絡成熟，具 Nature 級驗證；(2) 語言化信心誘發有 4+ 獨立評估；(3) 幻覺分類學與偵測——Ji 2022 與 Zhang 2025 提供全面覆蓋；(4) 綜述/元層級反思——該領域以其年齡而言異常自覺，有多篇立場論文批判自身基礎。

### Methodology Distribution / 方法學分布

From the knowledge graph: 22 empirical method papers (Orange, 49%), 9 surveys (Yellow, 20%), 6 benchmark studies (Green, 13%), 4 theoretical/position (Purple, 9%), 4 frameworks (Cyan, 9%). The dominance of empirical method papers is expected for a young CS subfield. The notable absence: **no experimental (Red) papers** — the field lacks controlled human-subject experiments testing whether UQ signals actually improve human trust calibration or decision-making.

從知識圖譜：22 篇實證方法論文（橙, 49%）、9 篇綜述（黃, 20%）、6 篇基準評估（綠, 13%）、4 篇理論/立場（紫, 9%）、4 篇框架（青, 9%）。實證方法論文主導符合年輕 CS 子領域的預期。顯著缺席：**零篇實驗研究（紅）**——領域缺乏受控的人體實驗，測試 UQ 訊號是否實際改善人類信任校準或決策。

### Cross-Gap Patterns / 跨缺口模式

All three gaps share a common root cause: **the field optimized for demonstrating individual method improvements on isolated benchmarks rather than building comparative infrastructure.** GAP_001 is the method-level manifestation (no cross-paradigm comparison), GAP_002 is the task-level manifestation (no multi-step evaluation), and GAP_003 is the metric-level manifestation (no agreed measurement standard). A single ambitious study could address parts of all three — a cross-paradigm benchmark (GAP_001) on reasoning tasks (GAP_002) evaluated with a new generation-aware metric (GAP_003) — but such a study would be very large. The most tractable entry point is GAP_001, which addresses the comparison question on existing benchmarks with existing methods.

三個缺口共享一個根本原因：**領域優先於在孤立基準上展示個別方法改進，而非建立比較性基礎設施。** GAP_001 為方法層面表現（無跨範式比較），GAP_002 為任務層面表現（無多步評估），GAP_003 為指標層面表現（無共識度量標準）。一項雄心勃勃的研究可同時部分解決三者——在推理任務（GAP_002）上進行跨範式基準（GAP_001）並以新的生成感知指標（GAP_003）評估——但規模極大。最可操作的切入點為 GAP_001，於現有基準以現有方法解決比較問題。

---

> **⛳ Checkpoint 3: 戰場選擇與價值裁定**
>
> Review the three gaps above. Select which gap to pursue based on your research interests, lab capabilities, and timeline.
>
> 請審核以上三個研究缺口。根據您的研究興趣、實驗室能力與時間表，選擇要鎖定的缺口。
>
> **Recommended**: GAP_001 is the highest-ranked gap and directly aligns with your priority direction (attention-based UQ). It is also the most immediately feasible — all methods have published code, and standard benchmarks are available.
>
> **建議**: GAP_001 為最高排名缺口，直接對齊您的優先方向（注意力 UQ），且最具即時可行性——所有方法皆已發表程式碼，標準基準亦可用。
>
> To proceed, specify: `Lock GAP_00X, drop GAP_00Y, GAP_00Z`
>
> 請指示：「鎖定 GAP_00X，放棄 GAP_00Y, GAP_00Z」

---

Files / 檔案: `step7_gap_analysis.md`
Next step / 下一步: After Checkpoint 3 resolution → `/research continue` → Step 8 (`research-hypothesis`)
