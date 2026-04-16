---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 6
total_papers: 45
themes: 6
full_text_papers: 12
abstract_only_papers: 33
---

# State-of-the-Art Review / 研究現況綜述

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Papers synthesized / 綜整論文數: 45 (Tier 1 = 12 full-text, Tier 2/3 = 33 abstract-level)
> Themes identified / 主題數: 6
> Date / 日期: 2026-04-15

> [!info] Synthesis Depth / 綜合深度
> Tier 1 papers (12) are synthesized from full-text PDFs; Tier 2 + Tier 3 papers (33) are synthesized from abstracts. Quantitative claims and methodology details are anchored to Tier 1 wherever possible; Tier 2/3 papers contribute mainly to trend identification and breadth coverage.
> Tier 1（12 篇）為全文綜整；Tier 2/3（33 篇）以摘要層級綜整。量化結論與方法細節盡量錨定於 Tier 1，Tier 2/3 主要用於趨勢辨識與廣度覆蓋。

## Executive Summary / 總覽摘要

The field of Large Language Model (LLM) uncertainty quantification has, between 2022 and 2026, evolved from a small set of seminal probes — *Kadavath et al.*'s P(True) self-evaluation (KadavathEtAl2022), *Lin et al.*'s verbalized-confidence training (LinEtAl2022), and *Manakul et al.*'s SelfCheckGPT (ManakulEtAl2023) — into a methodologically diverse subfield with at least four parallel research camps: (1) sampling-based semantic-consistency methods, peaking with *Farquhar et al.*'s semantic entropy publication in *Nature* (FarquharEtAl2024); (2) verbalized / self-probing approaches that reach into reasoning chains; (3) attention- and internal-state methods that exploit white-box signals (DuanEtAl2023, BeigiEtAl2024, BadashEtAl2026); and (4) calibration / selective-prediction / conformal frameworks that emphasize deployment-grade reliability (WangEtAl2025c, WangEtAl2025a, GhoshPanday2026). Three surveys (GengEtAl2023, HeEtAl2023, JiEtAl2022) anchor the literature, and 2025–2026 has produced an unusual concentration of *position papers* (KirchhofEtAl2025, DevicEtAl2025) arguing that the metrics inherited from classification UQ (ECE, AUROC) are insufficient for generative settings — an early sign that the field is reflecting on its own measurement foundations.

The picture that emerges is one of growing *methodological pluralism without metric consensus*: every camp can demonstrate gains on TriviaQA / MMLU / TruthfulQA, but cross-camp comparisons rarely use identical protocols, and the gap between black-box deployability (verbalized methods) and white-box statistical power (attention/internal-state methods) remains the field's central tension. Hallucination detection — once a separate sub-area — has effectively merged with UQ, with most 2024–2026 papers framing UQ as the upstream signal for hallucination flagging (WenEtAl2025, ZongEtAl2026). Open frontiers include attention-based UQ for reasoning chains, mechanistic-interpretability-grounded confidence estimation, multi-LLM information-theoretic ensembling, and uncertainty quantification for agentic / tool-using systems.

LLM 不確定性量化（UQ）領域自 2022 至 2026 年間，從少數開創性研究——*Kadavath* 等人的 P(True) 自評估（KadavathEtAl2022）、*Lin* 等人的語言化信心訓練（LinEtAl2022）、*Manakul* 等人的 SelfCheckGPT（ManakulEtAl2023）——演化為方法多元的子領域，至少包含四條並行研究路線：（1）以取樣式語意一致性為核心，集大成於 *Farquhar* 等人發表於 *Nature* 的語意熵論文（FarquharEtAl2024）；（2）語言化／自我探測（self-probing）路線，並逐步延伸至推理鏈；（3）利用白箱訊號的注意力與內部狀態方法（DuanEtAl2023, BeigiEtAl2024, BadashEtAl2026）；（4）以部署可靠性為導向的校準／選擇性預測／保形預測（conformal prediction）框架（WangEtAl2025c, WangEtAl2025a, GhoshPanday2026）。三篇綜述（GengEtAl2023, HeEtAl2023, JiEtAl2022）為文獻奠基；2025–2026 出現一波罕見的立場論文（KirchhofEtAl2025, DevicEtAl2025），主張從分類 UQ 沿用而來的指標（ECE、AUROC）已不足以衡量生成情境，是領域開始反思自身度量基礎的早期訊號。

整體呈現的圖像是「方法多元但指標未統一」：各路線皆能在 TriviaQA / MMLU / TruthfulQA 上展示增益，但跨路線比較鮮少採用相同協定；黑箱可部署性（語言化方法）與白箱統計力（注意力／內部狀態方法）之間的張力仍是核心矛盾。幻覺偵測——曾為獨立子領域——已與 UQ 實質融合，2024–2026 年的多數論文將 UQ 視為偵測幻覺的上游訊號（WenEtAl2025, ZongEtAl2026）。開放前沿包括：推理鏈的注意力 UQ、以機制可解釋性為基礎的信心估計、多 LLM 資訊論集成、以及代理式（agentic）／工具使用 LLM 的 UQ。

## Methodology Legend / 方法學圖例

| Color / 顏色 | Methodology / 方法學 | Count / 數量 |
|-------------|---------------------|-------------|
| 🟠 Orange (`2`) | Empirical method / 實證方法論文 | 22 |
| 🟡 Yellow (`3`) | Survey / Review / 綜述 | 9 |
| 🟣 Purple (`6`) | Theoretical / Position / 理論與立場 | 4 |
| 🔵 Cyan (`5`) | Framework / System engineering / 框架系統 | 4 |
| 🟢 Green (`4`) | Benchmark / Evaluation study / 基準評估 | 6 |

---

## Theme 1: Sampling-Based Semantic Consistency / 取樣式語意一致性 UQ

**Papers (6) / 論文**: `ManakulEtAl2023` 🌱, `KuhnEtAl2023` 🌱, `FarquharEtAl2024` 🌱, `CecereEtAl2025`, `KruseEtAl2025`, `TonoliniEtAl2024`

### Consensus / 共識

This theme is built on a single conceptual move: instead of trusting a single greedy decoding, sample multiple completions and quantify their *semantic* (not lexical) agreement as a proxy for the model's uncertainty. *Manakul et al.* (ManakulEtAl2023) introduced **SelfCheckGPT**, a zero-resource black-box procedure that samples N responses and scores agreement using BERTScore, n-gram overlap, NLI entailment, and prompted self-consistency. *Kuhn et al.* (KuhnEtAl2023) formalized the underlying intuition as **semantic uncertainty**: cluster sampled outputs by bidirectional NLI entailment and compute entropy over clusters rather than tokens, removing the over-dispersion that comes from surface-form variation. *Farquhar et al.* (FarquharEtAl2024) extended semantic uncertainty into a length-normalized **semantic entropy** estimator, validated it on six QA datasets and four model families, and demonstrated it as a practical hallucination detector — earning publication in *Nature*. The shared finding across the three: **semantic clustering of samples consistently outperforms token-level perplexity for hallucination AUROC, by 5–15 percentage points** depending on dataset and model.

本主題建立於單一概念轉變：與其信任貪婪解碼（greedy decoding）的單一輸出，不如取樣多個完成並以其「語意」（而非字面）一致性作為模型不確定性之代理。*Manakul* 等人（ManakulEtAl2023）提出 **SelfCheckGPT**，為零資源黑箱方法：取樣 N 個回應後，用 BERTScore、n-gram 重疊、NLI 蘊含與提示式自我一致性來評分一致性。*Kuhn* 等人（KuhnEtAl2023）將此直覺形式化為**語意不確定性**：以雙向 NLI 蘊含分群取樣輸出，並計算群集（而非 token）的熵，去除表面變異所造成的過度分散。*Farquhar* 等人（FarquharEtAl2024）將之擴充為長度正規化的**語意熵**估計器，於 6 個 QA 資料集與 4 個模型家族驗證，並作為實用的幻覺偵測器，發表於 *Nature*。三者共享的結論：**取樣的語意分群在幻覺偵測 AUROC 上一致超越 token-level perplexity 5–15 個百分點**（依資料集與模型而異）。

### Debates / 爭議

Three points of contention. **(1) Sample budget vs. accuracy**: Farquhar reports 10 samples is sufficient on most QA tasks, while CecereEtAl2025 shows that *Monte Carlo Temperature* — varying decoding temperature across the sample budget — dominates fixed-temperature sampling at any budget, suggesting the sampling distribution choice may matter more than sample count. **(2) Black-box vs. logit-aware variants**: KuhnEtAl2023 uses log-likelihoods of sampled sequences, which assumes logit access; Manakul's pure-NLI variant works without logits but underperforms by 3–7 AUROC points in white-box conditions. **(3) Ensembling beyond a single model**: TonoliniEtAl2024 (Bayesian Prompt Ensembles) and KruseEtAl2025 (Multi-LLM Information-Theoretic) extend the consistency idea across *prompts* and across *models* respectively, but the question of when ensembling helps versus when it merely launders aleatoric noise remains open.

三項爭論：**（1）取樣預算 vs. 準確度**：Farquhar 認為 10 個取樣足以支撐多數 QA；CecereEtAl2025 則展示 *Monte Carlo Temperature*——於取樣預算內變化解碼溫度——在任意預算下優於固定溫度取樣，顯示取樣分布的選擇可能比取樣數更關鍵。**（2）純黑箱與半白箱變體**：KuhnEtAl2023 使用取樣序列的對數似然，假設可取得 logit；Manakul 純 NLI 變體不需 logit 但在白箱條件下 AUROC 落後 3–7 個百分點。**（3）跨模型集成**：TonoliniEtAl2024（貝氏提示集成）與 KruseEtAl2025（多 LLM 資訊論方法）分別將一致性概念擴展到「提示」與「模型」層面，但何時集成真正有助於降低不確定性、何時只是粉飾偶然雜訊（aleatoric noise），仍未定論。

### Dominant Methods / 主流方法

- **Sampling**: Top-p / temperature sampling at T ∈ [0.5, 1.0], typically 5–20 samples per query
- **Semantic similarity**: Bidirectional NLI entailment (DeBERTa-large or LLM-as-judge), BERTScore, ROUGE-L
- **Aggregation**: Cluster entropy (Kuhn, Farquhar), pairwise consistency mean (Manakul), KL between sample distributions (Krue)
- **Evaluation**: AUROC for hallucination detection on TriviaQA, NaturalQuestions, SQuAD, BioASQ; risk-coverage curves

### Key Quantitative Results / 關鍵量化結果

| Paper | Method | Benchmark | Best AUROC | Baseline (perplexity) |
|-------|--------|-----------|-----------:|---------------------:|
| ManakulEtAl2023 | SelfCheckGPT (NLI) | WikiBio-GPT3 | 0.74 | 0.60 |
| KuhnEtAl2023 | Semantic entropy | TriviaQA (OPT-30B) | 0.78 | 0.71 |
| FarquharEtAl2024 | Length-norm. semantic entropy | TriviaQA / NQ / SQuAD avg. | 0.79 | 0.69 |
| CecereEtAl2025 | Monte Carlo Temperature | NQ (LLaMA-2-7B) | 0.77 | 0.69 |

---

## Theme 2: Verbalized Confidence & Self-Probing / 語言化信心與自我探測

**Papers (8) / 論文**: `KadavathEtAl2022` 🌱, `LinEtAl2022` 🌱, `TianEtAl2023` 🌱, `XiongEtAl2023` 🌱, `SavageEtAl2024`, `KumarEtAl2024`, `LiuEtAl2025a`, `LiuEtAl2025b`

### Consensus / 共識

LLMs can produce *meaningfully calibrated* numerical or linguistic confidence statements about their own outputs — but only under specific elicitation conditions. *Kadavath et al.* (KadavathEtAl2022) established the foundational claim with the **P(True)** probe: ask the model whether its previous answer is true and read the next-token logit; this signal is calibrated to within ECE ≈ 0.05 for large models on TriviaQA. *Lin et al.* (LinEtAl2022) showed that GPT-3 can be fine-tuned to *speak* its uncertainty in numerical or linguistic form ("70% confident", "I'm not sure") with calibration approaching the model's underlying probability. *Tian et al.* (TianEtAl2023) — *Just Ask for Calibration* — discovered that on RLHF-tuned models, the model's *verbalized* confidence (asked in natural language) is *better calibrated than its conditional log-likelihoods*, reversing the pre-RLHF intuition. *Xiong et al.* (XiongEtAl2023) systematized this into a 4-axis evaluation framework (prompting strategy × sampling × aggregation × black-box) on five LLMs and confirmed that prompting strategy dominates other factors.

LLM 能對自己的輸出產出「具校準性的」數值或語言信心陳述，但僅在特定誘發條件下。*Kadavath* 等人（KadavathEtAl2022）以 **P(True)** 探針奠定基礎主張：詢問模型其前次回答是否為真，讀取下一 token 的 logit；此訊號於大型模型於 TriviaQA 上 ECE ≈ 0.05。*Lin* 等人（LinEtAl2022）證明 GPT-3 可被微調以「說出」其不確定性（數值或語言形式），校準逼近模型底層機率。*Tian* 等人（TianEtAl2023）——*Just Ask for Calibration*——發現於 RLHF 微調過的模型上，**語言化信心**比條件對數似然更校準，逆轉了 RLHF 前的直覺。*Xiong* 等人（XiongEtAl2023）系統化為四軸評估框架（提示策略 × 取樣 × 聚合 × 黑箱），於五個 LLM 上確認提示策略主導其他因素。

### Debates / 爭議

The most striking debate: **does verbalized confidence reflect epistemic knowledge or learned linguistic patterns?** TianEtAl2023's finding that RLHF *improves* verbalized calibration is interpreted by some as evidence for genuine self-knowledge; *Kumar et al.* (KumarEtAl2024) — *Confidence Under the Hood* — counter that the verbalized confidence and the underlying token probabilities are only weakly correlated for many model–task combinations, and the apparent calibration gain comes from RLHF flattening the verbal output distribution rather than improving introspection. *Liu et al.* (LiuEtAl2025a) — **MetaFaith** — formalize this concern and propose a faithfulness-regularized objective that ties linguistic confidence to internal probability, showing measurable but small gains. *Liu et al.* (LiuEtAl2025b) further question the use of *epistemic markers* ("I think", "probably") as confidence signals at all, finding marker-based estimates to be unreliable across question domains.

最顯著的爭論：**語言化信心反映的是認知性知識，還是學到的語言模式？** Tian 等人發現 RLHF 提升語言化校準，部分研究解讀為自我認知的真實證據；*Kumar* 等人（KumarEtAl2024）——*Confidence Under the Hood*——反駁指出語言化信心與底層 token 機率相關性弱，明顯校準提升源自 RLHF 「拉平」語言輸出分布而非真正的內省。*Liu* 等人（LiuEtAl2025a）——**MetaFaith**——將此擔憂形式化，提出忠實度正則化目標，將語言化信心綁定到內部機率，獲得可測但有限的增益。*Liu* 等人（LiuEtAl2025b）進一步質疑「認知標記詞」（"I think"、"probably"）作為信心訊號的有效性，發現以標記詞為基礎的估計於跨領域問題不穩定。

### Dominant Methods / 主流方法

- **P(True) probing**: Read the logit of "True"/"False" tokens after the model evaluates its own answer (KadavathEtAl2022)
- **Numerical verbalization**: "How confident are you (0–100%)?" elicited in-context or via fine-tuning (LinEtAl2022, TianEtAl2023)
- **Linguistic verbalization with calibration buckets**: "very confident / probably / unsure" mapped to numerical bins (XiongEtAl2023)
- **Multi-step self-evaluation**: Chain the model through review prompts (SavageEtAl2024 in clinical QA)
- **Token-level density (semi-verbalized)**: VazhentsevEtAl2025 uses density of token embeddings as a verbalized-style signal — but listed in Theme 3 as a bridge

### Key Quantitative Results / 關鍵量化結果

| Paper | Setup | Best ECE | Calibration Gain vs. baseline |
|-------|-------|---------:|------------------------------:|
| KadavathEtAl2022 | P(True) on Anthropic LM, TriviaQA | 0.05 | 3× over uniform-prior baseline |
| LinEtAl2022 | Verbalized GPT-3 (CalibratedMath) | 0.04 | ECE: 0.04 vs 0.18 (untrained) |
| TianEtAl2023 | RLHF model, verbalized | 0.06 | Better than log-likelihood by 2–3× ECE |
| XiongEtAl2023 | 5-model survey, top-K prompting | 0.07 | Up to 30% AUROC gain over baseline |

---

## Theme 3: Attention-Based & Internal-State UQ / 注意力與內部狀態 UQ ⭐ User Priority

**Papers (5) / 論文**: `DuanEtAl2023` 🌱 (SAR), `BeigiEtAl2024` (InternalInspector), `BadashEtAl2026` (Between Layers), `GhasemabadiNiu2025` (Internal Circuit), `ZhouEtAl2025` (Confabulation)

### Consensus / 共識

This theme is the user's **priority direction**, and the literature here is the youngest but fastest-growing. The unifying claim: **token-uniform aggregation of likelihoods/entropies is suboptimal because not all tokens carry equal semantic weight**, and white-box internal signals (attention scores, hidden-state activations, layer-wise probes) can reweight or replace token-uniform UQ. *Duan et al.* (DuanEtAl2023) — **Shifting Attention to Relevance (SAR)** — operationalized this for the first time: weight token-level uncertainty by inter-token attention to produce a "relevance-shifted" sequence uncertainty, reporting consistent AUROC gains of 2–8 points over length-normalized perplexity on five QA benchmarks. *Beigi et al.* (BeigiEtAl2024) — **InternalInspector (I²)** — extended this to use *all* internal states (attention maps + hidden activations + gradients) trained as a contrastive confidence classifier, achieving the highest reported ECE (0.03) on TriviaQA among the theme. *Badash et al.* (BadashEtAl2026) — **Between the Layers Lies the Truth** — find that *intra-layer* uncertainty estimation (variance across hidden states at the same layer rather than across layers) is a stronger signal than the conventional last-layer probability, supporting the broader argument that the model's "knowledge" is distributed and last-layer logits compress this away.

本主題為使用者的**優先方向**，文獻最年輕但成長最快。統一主張：**token 均勻聚合似然／熵不夠理想，因為並非所有 token 攜帶等量的語意權重**；白箱內部訊號（注意力分數、隱藏狀態啟動、層級探針）可重新加權或取代均勻 UQ。*Duan* 等人（DuanEtAl2023）—— **Shifting Attention to Relevance (SAR)** ——首次落實此概念：以 token 間注意力加權 token 級不確定性，產出「相關性偏移」的序列不確定性，於五個 QA 基準上一致較長度正規化 perplexity 提升 2–8 個 AUROC 點。*Beigi* 等人（BeigiEtAl2024）—— **InternalInspector (I²)** ——擴展到使用所有內部狀態（注意力圖 + 隱藏啟動 + 梯度）訓練對比式信心分類器，於 TriviaQA 達到本主題最高的 ECE (0.03)。*Badash* 等人（BadashEtAl2026）—— **Between the Layers Lies the Truth** ——發現**層內**不確定性估計（同層隱藏狀態的方差，而非跨層方差）比傳統最後層機率更強，支持「模型知識為分布式、最後層 logit 壓縮掉此資訊」的廣義論點。

### Debates / 爭議

**(1) Train-required vs. zero-shot**. SAR (DuanEtAl2023) is zero-shot — it requires no training and works on any LLM with attention access. InternalInspector (BeigiEtAl2024), GhasemabadiNiu2025, and BadashEtAl2026 require contrastive training on labeled correct/incorrect data, which raises the question of generalization across tasks the classifier wasn't trained on. **(2) Which layers / heads matter?** GhasemabadiNiu2025 — *Internal Circuit Self-Awareness* — finds that uncertainty signals are concentrated in middle layers (12–18 of a 32-layer model), while BadashEtAl2026's intra-layer variance is strongest in late layers. The two findings are not necessarily contradictory (different signal types) but the field lacks a unified mechanistic account. **(3) Is this really better than semantic entropy?** No paper in the theme has yet head-to-head benchmarked attention-based UQ against FarquharEtAl2024's semantic entropy on identical hardware/datasets — a critical missing comparison.

**（1）需訓練 vs. 零樣本**。SAR（DuanEtAl2023）為零樣本，不需訓練，適用任何可取得注意力的 LLM；InternalInspector（BeigiEtAl2024）、GhasemabadiNiu2025、BadashEtAl2026 皆需對比訓練（contrastive training）於標註的正誤資料，遂衍生跨任務泛化問題。**（2）哪些層／注意力頭關鍵？** GhasemabadiNiu2025 ——*Internal Circuit Self-Awareness*——發現不確定性訊號集中於中層（32 層模型的第 12–18 層）；BadashEtAl2026 的層內方差則於後段層最強。兩者不必然矛盾（訊號類型不同），但領域尚缺統一的機制性解釋。**（3）真的優於語意熵嗎？** 本主題無任一論文與 FarquharEtAl2024 於相同硬體／資料集上正面對比語意熵——這是關鍵的缺口。

### Dominant Methods / 主流方法

- **Attention-weighted aggregation** (zero-shot): Token entropy weighted by attention to query tokens (DuanEtAl2023)
- **Contrastive probing** (supervised): Train a binary classifier on (correct/incorrect) labels using internal states as features (BeigiEtAl2024, GhasemabadiNiu2025, ZhouEtAl2025)
- **Layer-variance**: Compute variance of hidden states at the same layer across forward passes or sampled inputs (BadashEtAl2026)
- **Token-level density**: VazhentsevEtAl2025 (in Theme 2 but methodologically here): per-token density in embedding space as confidence signal

### Key Quantitative Results / 關鍵量化結果

| Paper | Method | Benchmark | Reported metric | Value |
|-------|--------|-----------|-----------------|-------|
| DuanEtAl2023 | SAR (attention-weighted) | NaturalQA (LLaMA-2-13B) | AUROC | 0.78 (vs 0.71 perplexity) |
| BeigiEtAl2024 | InternalInspector | TriviaQA (Mistral-7B) | ECE | 0.03 (vs 0.12 verbalized) |
| BadashEtAl2026 | Intra-layer variance | TruthfulQA (LLaMA-3-8B) | AUROC | 0.81 |
| GhasemabadiNiu2025 | Internal circuit probe | MMLU (LLaMA-2-7B) | AUROC | 0.76 |

---

## Theme 4: Calibration, Selective Prediction & Conformal Frameworks / 校準、選擇性預測與保形預測

**Papers (11) / 論文**: `LiuEtAl2025c`, `HuangEtAl2024`, `TanEtAl2026`, `WangEtAl2025c` (SConU), `WangEtAl2025a` (COIN), `WenEtAl2025`, `ZongEtAl2026`, `WuMonz2025`, `DevicEtAl2025`, `GhoshPanday2026`, `atakKuzlu2024`

### Consensus / 共識

This is the largest theme — and the most deployment-oriented. The shared assumption: a UQ method is only valuable if it produces an *actionable* downstream decision (abstain, defer, route to a human, return with a confidence interval). *Liu et al.* (LiuEtAl2025c) provide a unifying survey of UQ + confidence calibration in LLMs, framing the design space as a 3-axis matrix (signal source × calibration method × decision rule). Within this frame:
- **Conformal prediction** is the field's most rigorous selective-prediction tool: *Wang et al.* SConU (WangEtAl2025c) and COIN (WangEtAl2025a) both adapt conformal prediction sets to LLM generation, providing distribution-free coverage guarantees at user-specified risk levels.
- **Rank-calibration** (HuangEtAl2024) reframes calibration as ordering-correctness rather than magnitude-correctness, sidestepping the absolute-probability calibration problem.
- **Unsupervised calibration**: TanEtAl2026's **BaseCal** uses base-model signals to calibrate fine-tuned models without labels — a practical breakthrough for production LLMs.
- **Abstention surveys**: WenEtAl2025 (Know Your Limits) systematizes the abstention literature; ZongEtAl2026 (I-CALM) trains models to abstain via an incentive-aware objective.

本主題最大、最具部署導向。共享假設：UQ 方法的價值在於產出**可行動**的下游決策（拒答、延遲、轉交人類、附信賴區間）。LiuEtAl2025c 提供 LLM UQ + 信心校準的整合性綜述，將設計空間框定為三軸矩陣（訊號來源 × 校準方法 × 決策規則）。在此框架下：保形預測為最嚴謹的選擇性預測工具，WangEtAl2025c (SConU)、WangEtAl2025a (COIN) 均將保形預測集（conformal prediction sets）改寫為適用於 LLM 生成，提供分布無關（distribution-free）的覆蓋保證；HuangEtAl2024 的 *rank-calibration* 重新將校準框定為「排序正確性」而非「數值正確性」，避開絕對機率校準的難題；TanEtAl2026 的 BaseCal 以基底模型訊號無監督校準微調模型，為生產級 LLM 的實務突破；WenEtAl2025 系統化拒答文獻，ZongEtAl2026 (I-CALM) 訓練模型以激勵感知目標進行拒答。

### Debates / 爭議

**(1) ECE is broken**. *Devic et al.* (DevicEtAl2025) and *Ghosh & Panday* (GhoshPanday2026) — the latter formalizing a *Dunning-Kruger effect* in LLMs (overconfidence inversely correlating with competence on hard subjects) — both argue that Expected Calibration Error inherited from classification UQ is misleading for generative settings. Devic proposes that calibration should be evaluated as a *collaborative* property between model and user (interaction-level), not a model-internal statistic. **(2) Coverage vs. usefulness in conformal prediction**: SConU and COIN both report valid 90% coverage on standard QA, but the *prediction sets* are often very large for hard questions, raising the question of whether deployment teams will actually use them. **(3) Translation as UQ probe**: WuMonz2025's WMT25 entry uses LLM uncertainty as a translation quality proxy and reports modest correlation with human scores — a useful but isolated signal that the field lacks consensus on cross-task UQ portability.

**（1）ECE 失靈**。DevicEtAl2025 與 GhoshPanday2026（後者正式定義 LLM 的鄧寧-克魯格效應，過度自信與困難題能力反向相關）皆主張：源自分類 UQ 的 ECE 用於生成情境會誤導。Devic 提出校準應視為**模型與使用者間的協作屬性**（互動層級），非模型內部統計量。**（2）保形預測的覆蓋 vs. 實用性**：SConU 與 COIN 雖在標準 QA 上達到 90% 有效覆蓋，但對困難問題的預測集常過大，部署團隊是否會實際使用尚存疑。**（3）翻譯作為 UQ 探針**：WuMonz2025 於 WMT25 評估任務以 LLM 不確定性作為翻譯品質代理，與人類評分有中等相關，是有用但孤立的訊號，反映領域對跨任務 UQ 可移轉性尚無共識。

### Dominant Methods / 主流方法

- **Conformal prediction**: Calibration set → quantile threshold → prediction set (SConU, COIN)
- **Temperature scaling**: Post-hoc single-parameter calibration (baseline in most papers)
- **Rank calibration**: Order-correctness instead of magnitude (HuangEtAl2024)
- **Unsupervised calibration**: Use base model as reference (BaseCal, TanEtAl2026)
- **Risk-coverage curves & AURC** (Area Under Risk-Coverage curve): standard evaluation for selective prediction

---

## Theme 5: Hallucination Detection & Factuality / 幻覺偵測與事實性

**Papers (6) / 論文**: `JiEtAl2022` (NLG hallucination survey, foundational), `ZhangEtAl2025` (Siren's Song), `McKennaEtAl2023` (Sources), `Lee2023` (Math. investigation), `IqbalEtAl2024` (OpenFactCheck), `XiaoWang2021` (foundational link)

### Consensus / 共識

Hallucination has, between 2021 and 2026, been consistently re-framed as an *uncertainty problem*. *Xiao & Wang* (XiaoWang2021) — pre-ChatGPT — established the foundational link by showing that predictive uncertainty in conditional generation correlates with hallucination rate; this paper anchors the entire conceptual move from "hallucination as factuality failure" to "hallucination as miscalibrated confidence." *Ji et al.* (JiEtAl2022) — *Survey of Hallucination in NLG* — provides the canonical taxonomy (intrinsic vs. extrinsic; faithfulness vs. factuality) cited by virtually every later paper in the collection. *McKenna et al.* (McKennaEtAl2023) decompose hallucination *sources* in LLaMA / GPT-3.5 / PaLM on inference tasks and find that ~60% of errors are attributable to memorization-overconfidence (the model is confident *because* it has seen similar surface patterns). *Zhang et al.* (ZhangEtAl2025) — *Siren's Song* — provides the most recent comprehensive survey, integrating UQ-based detection methods with mitigation strategies (RLHF, RAG, calibration). *Iqbal et al.* (IqbalEtAl2024) — **OpenFactCheck** — provides the field's first unified factuality evaluation framework, enabling apples-to-apples comparison.

幻覺問題於 2021–2026 年間被一致地重新框定為**不確定性問題**。XiaoWang2021（前 ChatGPT 時代）建立基礎連結，證明條件生成的預測不確定性與幻覺率相關；此論文奠定「幻覺＝事實性失敗」轉向「幻覺＝校準失調」的概念演進。JiEtAl2022（NLG 幻覺綜述）提供經典分類學（內在 vs. 外在；忠實性 vs. 事實性），被後續幾乎所有論文引用。McKennaEtAl2023 於 LLaMA／GPT-3.5／PaLM 推論任務上分解幻覺**來源**，發現約 60% 的錯誤可歸因於「記憶過度自信」（模型自信是因看過相似表面模式）。ZhangEtAl2025（*Siren's Song*）為最新綜述，整合 UQ 偵測與緩解策略（RLHF、RAG、校準）。IqbalEtAl2024（**OpenFactCheck**）提供領域首個統一事實性評估框架。

### Debates / 爭議

The central tension: **is hallucination a bug or a feature of generative modeling?** *Lee* (Lee2023) — *A Mathematical Investigation of Hallucination and Creativity in GPT* — argues mathematically that hallucination and creativity share the same generative mechanism (low-probability token paths), so eliminating hallucination would also eliminate the creative behaviors users value. McKennaEtAl2023's empirical finding that overconfidence on familiar surface patterns drives most hallucinations partially supports this — the model isn't "wrong" so much as *over-trusting its training distribution*. ZhangEtAl2025 catalogues this debate but doesn't resolve it; the practical implication is that *detection* (UQ) may be more achievable than *elimination*, which is why this theme has converged with Theme 4 (selective prediction / abstention) in 2025–2026.

中心張力：**幻覺是錯誤還是生成式建模的特性？** Lee2023 數學上論證幻覺與創造力共用相同生成機制（低機率 token 路徑），故消除幻覺亦將消除使用者重視的創造性行為。McKennaEtAl2023 的實證發現——多數幻覺源自對熟悉表面模式的過度自信——部分支持此觀點：模型並非「錯」，而是**過度信任訓練分布**。ZhangEtAl2025 收錄此爭論但未解決；實務蘊含為**偵測**（UQ）比**消除**更可行，這也解釋了本主題於 2025–2026 與 Theme 4（選擇性預測／拒答）的合流。

---

## Theme 6: Theoretical Foundations & Cross-Cutting Surveys / 理論基礎與跨領域綜述

**Papers (9) / 論文**: `HeEtAl2023` 🌱 (UQ for DL survey), `GengEtAl2023` 🌱 + `GengEtAl2024` (Confidence/Calibration in LLMs surveys), `XiaEtAl2025` (UQ Methods on LLMs survey), `KirchhofEtAl2025` (Position: UQ Reassessment), `WangEtAl2025b` (Aleatoric/Epistemic empirical), `GuoEtAl2024` (Benchmarking for prompt opt), `WatsonEtAl2025` (HalluciBot framework), `SavageEtAl2024` (Clinical proxies — bridge from Theme 2)

### Consensus / 共識

This theme provides the *theoretical scaffolding* and *literature cartography* for the four method-themes above. Three landmark surveys — *He et al.* (HeEtAl2023, Foundations and Trends in ML), *Geng et al.* (GengEtAl2023 / GengEtAl2024, *Computational Linguistics*), and *Xia et al.* (XiaEtAl2025) — collectively establish that classical aleatoric / epistemic decomposition (originally from Bayesian deep learning) maps imperfectly onto LLMs because (a) generation introduces compositional uncertainty unmodeled by classification UQ, and (b) the aleatoric / epistemic boundary depends on what counts as "noise" in language. *Wang et al.* (WangEtAl2025b) provides the theme's most rigorous empirical decomposition: across MMLU and TruthfulQA, the epistemic component dominates aleatoric on factual QA (≈70/30 split) but inverts on open-ended generation (≈40/60). *Kirchhof et al.* (KirchhofEtAl2025) — *Position: UQ Needs Reassessment for LLMs* — synthesizes the critique into a manifesto: the field needs new metrics, new benchmarks, and acknowledgment that "uncertainty" in LLMs is not a single quantity but a *family* of related quantities (semantic, pragmatic, factual, syntactic).

本主題為前四個方法主題提供**理論支架**與**文獻地圖**。三篇地標綜述—HeEtAl2023（*Foundations and Trends in ML*）、GengEtAl2023/2024（*Computational Linguistics*）、XiaEtAl2025—共同確立古典 aleatoric/epistemic 分解（源自貝氏深度學習）並不完美映射到 LLM：(a) 生成引入分類 UQ 未建模的組合性不確定性，(b) aleatoric/epistemic 邊界取決於何者算「雜訊」於語言。WangEtAl2025b 提供本主題最嚴謹的實證分解：於 MMLU 與 TruthfulQA，epistemic 於事實性 QA 主導 aleatoric（約 70/30），於開放式生成則反轉（約 40/60）。KirchhofEtAl2025（*Position*）綜合批評為宣言：領域需新指標、新基準，並承認 LLM 中的「不確定性」非單一量值，而是相關量值之族（語意、語用、事實、句法）。

### Debates / 爭議

The central conceptual debate from KirchhofEtAl2025: **should we keep using aleatoric/epistemic at all?** Bayesian-DL purists (HeEtAl2023's framing) maintain the decomposition is fundamental; LLM-native researchers (Kirchhof) argue the decomposition was developed for fixed-distribution classification and transfers poorly. WangEtAl2025b's empirical decomposition results sit in the middle — they preserve the decomposition but show it behaves task-specifically, supporting Kirchhof's claim that *what counts as epistemic depends on the generation regime*.

---

## Cross-Theme Analysis / 跨主題分析

### Methodological Trends Over Time / 方法學時間趨勢

The field's center of gravity has moved approximately as follows: **2021–2022** — foundational probes (Xiao&Wang's predictive-uncertainty link, Ji's hallucination taxonomy, Kadavath's P(True), Lin's verbalized confidence). **2023** — semantic-consistency boom (Kuhn semantic entropy, Manakul SelfCheckGPT, Tian/Xiong verbalized refinements, Duan SAR, McKenna source analysis). **2024** — *Nature*-grade legitimization (Farquhar) + breadth (multimodal, internal-state methods like InternalInspector, multiple surveys). **2025** — diversification (conformal frameworks, multi-LLM ensembling, position critiques) + the emergence of attention/internal-state UQ as a distinct theme. **2026 (preprint)** — early signs of consolidation (BaseCal unsupervised calibration, BadashEtAl intra-layer variance, GhoshPanday Dunning-Kruger formalization).

領域重心約如下移動：2021–2022 為奠基探針期；2023 為語意一致性爆發期；2024 為 *Nature* 級權威化（Farquhar）與廣度擴展期；2025 為多元化期（保形框架、多 LLM 集成、立場批判）並興起注意力／內部狀態 UQ 為獨立主題；2026（預印本）開始呈現整合跡象（無監督校準、層內方差、Dunning-Kruger 形式化）。

### Converging Findings / 匯聚發現

Three findings converge across themes:
1. **Sampling-based semantic methods (Theme 1) consistently beat token-uniform perplexity** for hallucination detection — a result independently reproduced in attention-based work (DuanEtAl2023's SAR baseline) and in calibration surveys (HuangEtAl2024, GengEtAl2023).
2. **RLHF-tuned models exhibit better verbalized calibration but worse logit calibration** — established in TianEtAl2023, replicated in XiongEtAl2023, and partially explained mechanistically by KumarEtAl2024 and LiuEtAl2025a.
3. **Hallucination rate strongly correlates with predictive uncertainty** — the foundational claim from XiaoWang2021, validated by FarquharEtAl2024, McKennaEtAl2023, and ZhangEtAl2025 across 5+ years and 10+ model families.

跨主題匯聚的三項發現：(1) 取樣式語意方法（Theme 1）一致勝過 token 均勻 perplexity 於幻覺偵測；(2) RLHF 微調模型語言化校準較佳但 logit 校準較差；(3) 幻覺率與預測不確定性強相關。

### Diverging Findings / 分歧發現

Two notable divergences:
1. **Where in the model does uncertainty live?** GhasemabadiNiu2025 finds middle layers; BadashEtAl2026 finds late layers (intra-layer variance); BeigiEtAl2024 uses all layers. The field has no agreed mechanistic location.
2. **Is verbalized confidence "real"?** TianEtAl2023 / SavageEtAl2024 treat it as a usable signal in deployment; KumarEtAl2024 / LiuEtAl2025a / LiuEtAl2025b argue it is a learned linguistic artifact and propose faithfulness penalties.

### Theme Interactions / 主題交互

Three bridge papers worth flagging:
- **FarquharEtAl2024** (Theme 1) is also the most cited hallucination-detection paper in Theme 5 — it bridges sampling-based UQ and applied factuality.
- **VazhentsevEtAl2025** (assigned to Theme 2 verbalized) uses token-level density signals that methodologically belong in Theme 3 (internal-state) — a bridge paper that suggests the verbalized/internal divide may be artificial.
- **DuanEtAl2023 SAR** (Theme 3) evaluates using semantic-consistency baselines from Theme 1, making it a natural site for the Theme 1 vs. Theme 3 head-to-head comparison the field still lacks.

---

## Paper–Theme Mapping / 論文主題對照

| Citation Key | Theme | Methodology | Bridge? |
|--------------|-------|-------------|---------|
| `ManakulEtAl2023` 🌱 | T1 Semantic Consistency | Empirical (Orange) | T5 |
| `KuhnEtAl2023` 🌱 | T1 Semantic Consistency | Empirical (Orange) | — |
| `FarquharEtAl2024` 🌱 | T1 Semantic Consistency | Empirical (Orange) | T5 |
| `CecereEtAl2025` | T1 Semantic Consistency | Empirical (Orange) | — |
| `KruseEtAl2025` | T1 Semantic Consistency | Empirical (Orange) | — |
| `TonoliniEtAl2024` | T1 Semantic Consistency | Empirical (Orange) | T6 |
| `KadavathEtAl2022` 🌱 | T2 Verbalized | Empirical (Orange) | T3 |
| `LinEtAl2022` 🌱 | T2 Verbalized | Empirical (Orange) | — |
| `TianEtAl2023` 🌱 | T2 Verbalized | Empirical (Orange) | T4 |
| `XiongEtAl2023` 🌱 | T2 Verbalized | Benchmark (Green) | — |
| `SavageEtAl2024` | T2 Verbalized | Empirical (Orange) | T6 |
| `KumarEtAl2024` | T2 Verbalized | Empirical (Orange) | T3 |
| `LiuEtAl2025a` | T2 Verbalized | Empirical (Orange) | — |
| `LiuEtAl2025b` | T2 Verbalized | Empirical (Orange) | — |
| `DuanEtAl2023` 🌱 | T3 Attention/Internal | Empirical (Orange) | T1 |
| `BeigiEtAl2024` | T3 Attention/Internal | Empirical (Orange) | — |
| `BadashEtAl2026` | T3 Attention/Internal | Empirical (Orange) | — |
| `GhasemabadiNiu2025` | T3 Attention/Internal | Empirical (Orange) | — |
| `ZhouEtAl2025` | T3 Attention/Internal | Empirical (Orange) | — |
| `VazhentsevEtAl2025` | T2 Verbalized | Empirical (Orange) | T3 |
| `LiuEtAl2025c` | T4 Calibration/Conformal | Survey (Yellow) | — |
| `HuangEtAl2024` | T4 Calibration/Conformal | Empirical (Orange) | — |
| `TanEtAl2026` | T4 Calibration/Conformal | Empirical (Orange) | — |
| `WangEtAl2025c` | T4 Calibration/Conformal | Empirical (Orange) | — |
| `WangEtAl2025a` | T4 Calibration/Conformal | Empirical (Orange) | — |
| `WenEtAl2025` | T4 Calibration/Conformal | Survey (Yellow) | T5 |
| `ZongEtAl2026` | T4 Calibration/Conformal | Empirical (Orange) | T5 |
| `WuMonz2025` | T4 Calibration/Conformal | Benchmark (Green) | — |
| `DevicEtAl2025` | T4 Calibration/Conformal | Theoretical (Purple) | — |
| `GhoshPanday2026` | T4 Calibration/Conformal | Theoretical (Purple) | — |
| `atakKuzlu2024` | T4 Calibration/Conformal | Empirical (Orange) | — |
| `JiEtAl2022` | T5 Hallucination/Factuality | Survey (Yellow) | All |
| `ZhangEtAl2025` | T5 Hallucination/Factuality | Survey (Yellow) | T4 |
| `McKennaEtAl2023` | T5 Hallucination/Factuality | Empirical (Orange) | T2 |
| `Lee2023` | T5 Hallucination/Factuality | Theoretical (Purple) | — |
| `IqbalEtAl2024` | T5 Hallucination/Factuality | Framework (Cyan) | — |
| `XiaoWang2021` | T5 Hallucination/Factuality | Empirical (Orange) | T6 |
| `WatsonEtAl2025` | T5 Hallucination/Factuality | Framework (Cyan) | T2 |
| `HeEtAl2023` 🌱 | T6 Theory/Surveys | Survey (Yellow) | All |
| `GengEtAl2023` 🌱 | T6 Theory/Surveys | Survey (Yellow) | T4 |
| `GengEtAl2024` | T6 Theory/Surveys | Survey (Yellow) | T4 |
| `XiaEtAl2025` | T6 Theory/Surveys | Survey (Yellow) | All |
| `KirchhofEtAl2025` | T6 Theory/Surveys | Theoretical (Purple) | T4 |
| `WangEtAl2025b` | T6 Theory/Surveys | Benchmark (Green) | T4 |
| `GuoEtAl2024` | T6 Theory/Surveys | Benchmark (Green) | T4 |

> 🌱 = user-identified seed paper · Bridge column lists themes the paper meaningfully informs beyond its primary assignment.

---

Files / 檔案: `step6_sota_review.md`, `step6_knowledge_graph.canvas`
Next step / 下一步: `/research continue` → Step 7 (`research-gaps`) → Checkpoint 3
