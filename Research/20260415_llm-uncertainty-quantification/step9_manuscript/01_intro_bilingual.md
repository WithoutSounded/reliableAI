---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
target_journal: "NeurIPS 2026"
note: "Bilingual companion — NOT for submission. The authoritative version is 01_intro.tex."
---

# Introduction / 引言

## Context & Motivation / 背景與動機

Large language models (LLMs) are increasingly deployed not as single-turn question-answering systems but as multi-step reasoning engines---chain-of-thought (CoT) prompting decomposes complex problems into sequential intermediate steps (Kadavath et al., 2022; Xiong et al., 2023), while agentic pipelines extend this further by interleaving reasoning with external tool invocations across multiple turns. In these settings, each intermediate step depends on the correctness of its predecessors, creating a sequential decision process where errors compound: a single miscalculated arithmetic step or an incorrect fact retrieval can propagate through the entire chain and corrupt the final answer. Despite this fundamental shift in how LLMs are used, the field's methods for quantifying *how confident* a model is in its own outputs---uncertainty quantification (UQ)---have been developed and validated almost exclusively on single-turn, short-form tasks such as closed-book question answering and multiple-choice classification (Farquhar et al., 2024; Kuhn et al., 2023; Tian et al., 2023; Duan et al., 2023).

大型語言模型（LLMs）日益不再僅作為單輪問答系統，而是被部署為多步推理引擎——鏈式思考（chain-of-thought, CoT）提示將複雜問題分解為連續的中間步驟（Kadavath et al., 2022; Xiong et al., 2023），而代理式（agentic）管線則進一步將推理與跨多輪的外部工具調用交織在一起。在這些場景中，每個中間步驟都依賴於前一步驟的正確性，形成一個誤差會累積的連續決策過程：單一的算術計算錯誤或不正確的事實檢索就可能在整條鏈中傳播並破壞最終答案。儘管 LLM 的使用方式已發生根本性轉變，該領域用於量化模型對自身輸出*有多大把握*的方法——不確定性量化（uncertainty quantification, UQ）——幾乎完全是在單輪、短格式任務（如封閉式問答和多選分類）上開發和驗證的（Farquhar et al., 2024; Kuhn et al., 2023; Tian et al., 2023; Duan et al., 2023）。

---

This mismatch between how UQ is studied and how LLMs are deployed creates a critical reliability gap. When a language model performs multi-step mathematical reasoning on GSM8K or multi-hop factual reasoning on StrategyQA, there is currently no principled way to determine whether the model's uncertainty about its final answer reflects genuine epistemic uncertainty about the problem or merely reflects accumulated noise from intermediate steps. Surveys of the field have flagged this disconnect: Geng et al. (2023) identify reasoning-chain UQ as a top open problem, Kirchhof et al. (2025) argue that existing UQ metrics need fundamental reassessment for agentic LLM settings, and Xia et al. (2025) note the absence of step-level uncertainty decomposition in the current literature. Yet no empirical study has addressed the problem directly.

UQ 的研究方式與 LLM 的實際部署之間的落差造成了關鍵的可靠性缺口。當語言模型在 GSM8K 上進行多步數學推理或在 StrategyQA 上進行多跳事實推理時，目前沒有原則性的方法來判斷模型對最終答案的不確定性究竟反映了對問題的真實認知性不確定性（epistemic uncertainty），還是僅僅反映了中間步驟累積的雜訊。該領域的綜述已標記了這一斷裂：Geng et al. (2023) 將推理鏈 UQ 列為最重要的開放問題之一，Kirchhof et al. (2025) 主張現有 UQ 指標需要為代理式 LLM 場景進行根本性的重新評估，Xia et al. (2025) 指出當前文獻中缺乏步驟級不確定性分解。然而，尚無實證研究直接解決這一問題。

---

## Background / 背景知識

Uncertainty quantification in LLMs builds on the classical distinction between *epistemic uncertainty* (reducible uncertainty due to limited knowledge) and *aleatoric uncertainty* (irreducible uncertainty inherent in the task) (He et al., 2023). For autoregressive language models, UQ operates at the intersection of token-level probabilities and sequence-level semantics: the model produces a probability distribution over next tokens at each position, but users care about the correctness of the *entire generated sequence*. This token-to-sequence gap is a defining challenge (Geng et al., 2024; Liu et al., 2025c). Calibration---the degree to which a model's expressed confidence matches its empirical accuracy---is typically measured via Expected Calibration Error (ECE) or reliability diagrams, while the ability to detect incorrect outputs is measured via AUROC for misclassification detection and risk-coverage curves (AURC) for selective prediction (Huang et al., 2024; Wen et al., 2025). Empirical decomposition studies show that the epistemic component dominates on factual QA (~70% of total uncertainty) but inverts on open-ended generation (~40%), suggesting that "uncertainty" in LLMs is task-dependent rather than a single scalar quantity (Wang et al., 2025b; Kirchhof et al., 2025).

LLM 的不確定性量化建立在*認知性不確定性*（epistemic uncertainty，因知識有限而可縮減的不確定性）與*偶然性不確定性*（aleatoric uncertainty，任務固有的不可縮減不確定性）之間的經典區分上（He et al., 2023）。對自迴歸語言模型而言，UQ 運作於 token 級機率與序列級語意的交匯處：模型在每個位置產生下一個 token 的機率分布，但使用者關心的是*整個生成序列*的正確性。這種 token 到序列的落差是一個根本性挑戰（Geng et al., 2024; Liu et al., 2025c）。校準（calibration）——模型表達的信心與其實際準確度的一致程度——通常透過期望校準誤差（Expected Calibration Error, ECE）或可靠性圖來衡量；而偵測錯誤輸出的能力則以 AUROC（錯誤分類偵測）和風險-覆蓋曲線（AURC，用於選擇性預測）來衡量（Huang et al., 2024; Wen et al., 2025）。實證分解研究顯示，認知性成分在事實性 QA 中占主導（約 70% 的總不確定性），但在開放式生成中反轉（約 40%），表明 LLM 中的「不確定性」是任務相依的，而非單一的純量（Wang et al., 2025b; Kirchhof et al., 2025）。

---

## Sampling-Based Semantic Consistency / 取樣式語意一致性

The most successful family of methods addresses the token-to-sequence gap by sampling multiple completions and measuring their *semantic* agreement. Manakul et al. (2023) introduced SelfCheckGPT, a zero-resource black-box method that scores inter-sample consistency using BERTScore and NLI entailment, achieving AUROC 0.74 on WikiBio hallucination detection. Kuhn et al. (2023) formalized this intuition as *semantic uncertainty*: cluster sampled outputs by bidirectional NLI entailment and compute entropy over semantic clusters rather than tokens, removing surface-form variation. Farquhar et al. (2024) extended this into length-normalized *semantic entropy*, validated across six QA datasets and four model families, achieving AUROC 0.79 on TriviaQA---a 10-point improvement over token perplexity---and demonstrated its effectiveness as a hallucination detector in a landmark *Nature* publication. More recently, Cecere et al. (2025) showed that varying decoding temperature across the sample budget (Monte Carlo Temperature) further improves sampling efficiency. The core limitation of this family is computational cost: semantic entropy requires 10--20 forward passes per query, and its application to multi-step settings would multiply this by the number of reasoning steps.

最成功的方法家族透過取樣多個完成（completions）並衡量其*語意*一致性來解決 token 到序列的落差。Manakul et al. (2023) 提出 SelfCheckGPT，一種零資源黑箱方法，以 BERTScore 和 NLI 蘊含關係評分樣本間一致性，在 WikiBio 幻覺偵測上達到 AUROC 0.74。Kuhn et al. (2023) 將此直覺形式化為*語意不確定性*（semantic uncertainty）：以雙向 NLI 蘊含對取樣輸出進行語意分群，計算語意群集（而非 token）的熵，從而移除表面形式的變異。Farquhar et al. (2024) 將其擴展為長度正規化的*語意熵*（semantic entropy），在六個 QA 資料集和四個模型族上驗證，於 TriviaQA 達到 AUROC 0.79——較 token perplexity 提升 10 個百分點——並在具里程碑意義的 *Nature* 論文中展示其作為幻覺偵測器的有效性。近期，Cecere et al. (2025) 表明在取樣預算內變化解碼溫度（Monte Carlo Temperature）可進一步改善取樣效率。此方法家族的核心限制是計算成本：語意熵每次查詢需要 10–20 次前向傳播（forward pass），若應用於多步場景則需乘以推理步驟數。

---

## Verbalized Confidence & Self-Probing / 語言化信心與自我探測

A complementary approach elicits uncertainty estimates *from the model itself* in natural language. Kadavath et al. (2022) established the foundational P(True) probe---asking the model whether its own answer is correct and reading the next-token logit---achieving ECE ~0.05 on large models. Lin et al. (2022) demonstrated that LLMs can be fine-tuned to express calibrated numerical confidence ("70% confident"), while Tian et al. (2023) discovered that RLHF-tuned models produce *better* calibration through verbalized confidence than through their own conditional log-likelihoods, reversing the pre-RLHF intuition. Xiong et al. (2023) systematized these findings into a four-axis evaluation framework across five LLMs, confirming that prompting strategy dominates other factors. However, the faithfulness of verbalized confidence remains contested: Kumar et al. (2024) found only weak correlation between verbal confidence and internal token probabilities, suggesting apparent calibration may arise from distributional flattening rather than genuine self-knowledge, and Liu et al. (2025a) proposed faithfulness regularization (MetaFaith) to address this gap.

一種互補的方法從模型自身以自然語言誘發不確定性估計。Kadavath et al. (2022) 建立了奠基性的 P(True) 探針——詢問模型其自身答案是否正確並讀取下一個 token 的 logit——在大型模型上達到 ECE ≈ 0.05。Lin et al. (2022) 展示 LLM 可被微調以表達校準過的數值信心（"70% confident"），而 Tian et al. (2023) 發現經 RLHF 微調的模型透過語言化信心產出的校準*優於*其自身的條件對數似然（conditional log-likelihoods），逆轉了 RLHF 之前的直覺。Xiong et al. (2023) 將這些發現系統化為四軸評估框架，跨五個 LLM 確認提示策略（prompting strategy）主導其他因素。然而，語言化信心的忠實度（faithfulness）仍具爭議：Kumar et al. (2024) 發現語言化信心與內部 token 機率之間僅有弱相關，表明表面上的校準可能源自分布平坦化（distributional flattening）而非真正的自我認知，Liu et al. (2025a) 則提出忠實度正則化（MetaFaith）來解決此問題。

---

## Attention-Based & Internal-State Methods / 注意力與內部狀態方法

A third emerging paradigm exploits white-box access to model internals. Duan et al. (2023) introduced Shifting Attention to Relevance (SAR), which weights token-level entropy by inter-token attention scores to produce relevance-shifted uncertainty estimates, reporting consistent AUROC gains of 2--8 points over length-normalized perplexity on five QA benchmarks. Beigi et al. (2024) extended this to InternalInspector (I^2), a contrastive confidence classifier trained on attention maps, hidden activations, and gradients, achieving ECE 0.03 on TriviaQA. Badash et al. (2026) found that intra-layer hidden-state variance outperforms last-layer probability as an uncertainty signal, achieving AUROC 0.81 on TruthfulQA, while Ghasemabadi & Niu (2025) localized uncertainty signals to specific internal circuits in middle transformer layers. These methods require only a single forward pass---an order of magnitude cheaper than sampling-based approaches---but critically, no paper in this theme has benchmarked against semantic entropy under identical conditions (Geng et al., 2023).

第三個新興範式利用白箱存取（white-box access）來獲取模型內部資訊。Duan et al. (2023) 提出 Shifting Attention to Relevance (SAR)，以 token 間注意力分數加權 token 級熵來產出相關性偏移的不確定性估計，在五個 QA 基準上報告了較長度正規化 perplexity 穩定提升 2–8 個 AUROC 百分點。Beigi et al. (2024) 將其擴展為 InternalInspector (I²)，一種在注意力圖、隱藏層啟動和梯度上訓練的對比式信心分類器，於 TriviaQA 達到 ECE 0.03。Badash et al. (2026) 發現層內隱藏狀態方差（intra-layer hidden-state variance）作為不確定性訊號優於最後層機率，在 TruthfulQA 達到 AUROC 0.81；而 Ghasemabadi & Niu (2025) 將不確定性訊號定位到 transformer 中間層的特定內部電路。這些方法僅需一次前向傳播——比取樣式方法便宜一個數量級——但關鍵的是，本主題中尚無論文在相同條件下與語意熵進行對比（Geng et al., 2023）。

---

## Calibration & Deployment Frameworks / 校準與部署框架

Deployment-oriented work has focused on transforming raw UQ signals into actionable decisions. Conformal prediction methods (Wang et al., 2025c; Wang et al., 2025a) provide distribution-free coverage guarantees at user-specified risk levels, while Tan et al. (2026) introduced unsupervised calibration using base-model signals (BaseCal). Rank-calibration (Huang et al., 2024) reframes calibration as ordering-correctness rather than magnitude-correctness. The abstention literature has matured rapidly (Wen et al., 2025; Zong et al., 2026), and position papers have begun questioning whether metrics inherited from classification UQ---particularly ECE---are appropriate for generative settings at all (Devic et al., 2025; Ghosh & Panday, 2026).

以部署為導向的研究專注於將原始 UQ 訊號轉化為可行動的決策。保形預測（conformal prediction）方法（Wang et al., 2025c; Wang et al., 2025a）在使用者指定的風險水準下提供分布無關的覆蓋保證；Tan et al. (2026) 提出使用基底模型訊號的無監督校準（BaseCal）。Rank-calibration（Huang et al., 2024）將校準重新框定為排序正確性而非數值正確性。拒答（abstention）文獻已快速成熟（Wen et al., 2025; Zong et al., 2026），而立場論文（position papers）開始質疑從分類 UQ 繼承的指標——特別是 ECE——是否根本適用於生成式場景（Devic et al., 2025; Ghosh & Panday, 2026）。

---

## The Multi-Step Reasoning Gap / 多步推理缺口

Despite this methodological diversity, a fundamental blind spot persists: **all existing UQ methods have been developed and evaluated exclusively on single-turn tasks**. The dominant deployment paradigm in 2025--2026---chain-of-thought reasoning and agentic pipelines---introduces a qualitatively different uncertainty structure. In a K-step reasoning chain, the model generates intermediate steps s_1, s_2, ..., s_K before producing a final answer a. Each step s_i carries its own uncertainty u(s_i), and these step-level uncertainties interact through the chain's sequential dependency structure: an error at step s_j can invalidate all subsequent steps regardless of their individual confidence. No existing method addresses how to (a) measure uncertainty at the granularity of individual reasoning steps, (b) aggregate step-level uncertainty into a chain-level confidence estimate, or (c) determine whether the aggregation framework transfers across reasoning domains.

儘管方法論如此多元，一個根本性的盲點仍然存在：**所有現有 UQ 方法都僅在單輪任務上開發和評估**。2025–2026 年的主流部署範式——鏈式思考推理與代理式管線——引入了本質上不同的不確定性結構。在一條 K 步推理鏈中，模型生成中間步驟 s_1, s_2, ..., s_K 後才產出最終答案 a。每個步驟 s_i 攜帶自身的不確定性 u(s_i)，而這些步驟級不確定性透過鏈的順序依賴結構相互作用：步驟 s_j 的錯誤可能使所有後續步驟失效，而不論其個別信心如何。現有方法均未解決如何 (a) 在個別推理步驟的粒度上衡量不確定性、(b) 將步驟級不確定性聚合為鏈級信心估計、或 (c) 判定聚合框架能否跨推理領域移轉。

---

The evidence for this gap is structural, not incidental. SAR (Duan et al., 2023) demonstrated that non-uniform attention-based aggregation improves *within*-sequence UQ but did not extend this to *between*-step aggregation. Semantic entropy (Farquhar et al., 2024) processes the entire generation as a single sequence and has no mechanism for step decomposition. Verbalized confidence (Tian et al., 2023; Xiong et al., 2023) could in principle be applied per-step, but no study has evaluated whether per-step verbal confidence retains its calibration properties on the shorter, more context-dependent text spans typical of individual reasoning steps. The only tangentially related work in the reviewed literature, Catak & Kuzlu (2024), applies convex-hull analysis to LLM outputs but does not address step-level decomposition or chain propagation.

此缺口的證據是結構性的，而非偶然的。SAR（Duan et al., 2023）展示了非均勻注意力聚合改善了序列*內部*的 UQ，但並未將其擴展到步驟*之間*的聚合。語意熵（Farquhar et al., 2024）將整個生成作為單一序列處理，沒有步驟分解的機制。語言化信心（Tian et al., 2023; Xiong et al., 2023）原則上可逐步應用，但尚無研究評估逐步語言化信心在個別推理步驟——通常較短且更依賴上下文的文本片段——上是否保持其校準特性。已審查文獻中唯一切線相關的研究（Catak & Kuzlu, 2024）將凸包分析（convex-hull analysis）應用於 LLM 輸出，但未涉及步驟級分解或鏈式傳播。

---

## Our Approach / 我們的方法

We propose a *step-level uncertainty propagation* framework for chain-of-thought LLM reasoning. The framework applies existing, well-characterized UQ methods---semantic entropy, SAR attention-weighting, and verbalized confidence---independently to each reasoning step, then aggregates step-level uncertainty into a chain-level confidence estimate via four candidate aggregation functions: product rule (assuming step independence), max-step (chain uncertainty equals its weakest link), attention-flow-weighted aggregation (exploiting inter-step attention patterns), and a learned aggregation head. We evaluate this framework on three reasoning benchmarks spanning mathematical reasoning (GSM8K), multi-hop factual reasoning (StrategyQA), and tool-use (ToolBench), using three open-weight LLMs (LLaMA-3-8B, LLaMA-3-70B, Mistral-7B) that permit full white-box access. Our primary hypothesis is that at least one step-level UQ method combined with an appropriate aggregation function will achieve AUROC >= 0.70 for final-answer correctness prediction, significantly outperforming the single-turn baseline of whole-chain perplexity.

我們提出一個用於鏈式思考 LLM 推理的*步驟級不確定性傳播*框架。該框架將現有的、已充分描述的 UQ 方法——語意熵、SAR 注意力加權、語言化信心——獨立應用於每個推理步驟，然後透過四種候選聚合函數將步驟級不確定性聚合為鏈級信心估計：乘積法則（假設步驟獨立）、最大步驟法（鏈不確定性等於其最弱環節）、注意力流加權聚合（利用步驟間注意力模式）、以及學習式聚合頭（learned aggregation head）。我們在涵蓋數學推理（GSM8K）、多跳事實推理（StrategyQA）和工具使用（ToolBench）的三個推理基準上評估此框架，使用三個允許完整白箱存取的開源 LLM（LLaMA-3-8B、LLaMA-3-70B、Mistral-7B）。我們的主要假說是，至少一種步驟級 UQ 方法與適當聚合函數的組合將在最終答案正確性預測上達到 AUROC ≥ 0.70，顯著優於整鏈 perplexity 的單輪基線。

---

## Contributions / 研究貢獻

The main contributions of this work are as follows:

本研究的主要貢獻如下：

1. **Step-level uncertainty propagation formalization / 步驟級不確定性傳播形式化**: We formalize the *step-level uncertainty propagation* problem for chain-of-thought reasoning, defining the mathematical framework for decomposing chain-level uncertainty into step-level components and aggregating them through four distinct functions. / 我們將鏈式思考推理的步驟級不確定性傳播問題形式化，定義將鏈級不確定性分解為步驟級成分並透過四種不同函數進行聚合的數學框架。

2. **First systematic step-wise UQ evaluation / 首次系統性逐步 UQ 評估**: We provide the first systematic empirical evaluation of whether existing single-turn UQ methods (semantic entropy, SAR, verbalized confidence) retain discriminative power when applied step-wise to individual reasoning steps, establishing baselines for future work in multi-step UQ. / 我們提供首次系統性實證評估，檢驗現有單輪 UQ 方法（語意熵、SAR、語言化信心）在逐步應用於個別推理步驟時是否保持區辨力，為多步 UQ 的未來研究建立基線。

3. **Attention-flow-weighted aggregation / 注意力流加權聚合**: We demonstrate that attention-flow-weighted aggregation---extending SAR's intra-sequence attention reweighting to inter-step attention---outperforms naive aggregation strategies (product rule, max-step) for chain-level correctness prediction. / 我們展示注意力流加權聚合——將 SAR 的序列內注意力重加權擴展到步驟間注意力——在鏈級正確性預測上優於樸素聚合策略（乘積法則、最大步驟法）。

4. **Uncertainty divergence point characterization / 不確定性分歧點特徵化**: We characterize the *uncertainty divergence point*---the reasoning step at which uncertainty first diverges between chains that ultimately produce correct versus incorrect answers---providing actionable guidance for early-stopping and re-sampling deployment strategies. / 我們特徵化*不確定性分歧點*——最終產出正確與不正確答案的鏈之間不確定性首次分歧的推理步驟——為提前停止和重新取樣的部署策略提供可行動的指引。

---

## Paper Outline / 論文結構

The remainder of this paper is organized as follows. Section 2 discusses related work in detail. Section 3 describes the step-level UQ propagation framework and aggregation functions. Section 4 presents the experimental setup, models, benchmarks, and evaluation protocol. Section 5 reports the results. Section 6 discusses implications, limitations, and future directions. Section 7 concludes the paper.

本文其餘部分的結構如下。第 2 節詳細討論相關工作。第 3 節描述步驟級 UQ 傳播框架與聚合函數。第 4 節呈現實驗設置、模型、基準與評估協定。第 5 節報告結果。第 6 節討論蘊含、限制與未來方向。第 7 節為結論。
