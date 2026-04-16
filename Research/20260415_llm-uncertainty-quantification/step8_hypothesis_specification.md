---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 8
selected_gap: "GAP_002"
dropped_gaps: ["GAP_001", "GAP_003"]
research_questions: 4
hypotheses: 3
---

# Hypothesis Specification / 假說規格書

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Selected Gap / 選定缺口: GAP_002 — UQ for Multi-Step Reasoning (CoT) and Agentic/Tool-Use LLMs
> Dropped Gaps / 放棄缺口: GAP_001 (Cross-Paradigm Benchmark), GAP_003 (Generative-Native Metrics)
> Date / 日期: 2026-04-15

## Executive Summary / 總覽摘要

All existing LLM uncertainty quantification methods — semantic entropy, verbalized confidence, attention-based signals, conformal prediction — have been developed and validated exclusively on single-turn, short-form QA tasks (TriviaQA, MMLU, NaturalQuestions). Yet the dominant deployment paradigm for LLMs in 2025–2026 is multi-step reasoning (chain-of-thought prompting, where intermediate steps compound uncertainty into the final answer) and agentic pipelines (where the model plans, invokes external tools, and integrates results across turns). No paper in a 45-paper SOTA review addresses how uncertainty propagates through these sequential decision processes, or whether existing single-turn UQ methods transfer to multi-step settings.

This research proposes to formalize **step-level uncertainty propagation** in chain-of-thought LLM reasoning, define an aggregation framework from step-uncertainty to chain-uncertainty, and empirically evaluate whether existing UQ methods (semantic entropy, SAR attention-weighting, verbalized confidence) retain their discriminative power when applied step-wise to reasoning chains. The study will use GSM8K (math reasoning), StrategyQA (multi-hop factual), and a tool-use benchmark (ToolBench or API-Bank) as evaluation testbeds. If successful, this work establishes the first principled UQ framework for the reasoning and agentic settings where LLMs are actually deployed — bridging the gap between controlled QA evaluation and real-world reliability.

現有所有 LLM 不確定性量化方法——語意熵、語言化信心、注意力訊號、保形預測——均僅在單輪、短格式 QA 任務（TriviaQA、MMLU、NaturalQuestions）上開發與驗證。然而 2025–2026 年 LLM 的主流部署範式為多步推理（chain-of-thought 提示，中間步驟將不確定性複合至最終答案）與代理式管線（模型規劃、調用外部工具、跨輪次整合結果）。45 篇 SOTA 綜述中無任何論文探討不確定性如何在這些連續決策過程中傳播，或現有單輪 UQ 方法能否移轉至多步場景。

本研究提議形式化鏈式思考（CoT）LLM 推理中的**步驟級不確定性傳播**，定義從步驟不確定性到鏈不確定性的聚合框架，並實證評估現有 UQ 方法（語意熵、SAR 注意力加權、語言化信心）在逐步應用於推理鏈時是否保持區辨力。研究將以 GSM8K（數學推理）、StrategyQA（多跳事實）與工具使用基準（ToolBench 或 API-Bank）為評估平台。若成功，此研究將建立推理與代理式場景中首個有原則的 UQ 框架——彌合受控 QA 評估與真實部署可靠性之間的落差。

---

## Gap Selection Rationale / 缺口選擇理由

**Locked**: GAP_002 (composite 4.00) — chosen over GAP_001 (4.60) because: (1) the user's longer-term research trajectory targets agentic systems, not just benchmark comparisons; (2) the novelty ceiling is higher (essentially uncharted territory vs. a well-specified benchmark study); (3) even a partial result (CoT-only, without full agentic evaluation) would be publishable and impactful. GAP_001 remains a natural follow-up study.

**Dropped**: GAP_001 (Cross-Paradigm Benchmark, 4.60) — highest-ranked but more incremental; can be pursued as a second publication. GAP_003 (Generative Metrics, 3.80) — important but requires community adoption beyond one paper; better addressed as part of a larger initiative.

---

## Research Questions / 研究問題

### RQ1: Do existing single-turn UQ methods retain discriminative power when applied step-wise to chain-of-thought reasoning? / 現有單輪 UQ 方法在逐步應用於鏈式思考推理時是否保持區辨力？

This is the feasibility question. If existing UQ methods (semantic entropy, SAR, verbalized confidence) applied independently to each reasoning step can already distinguish correct from incorrect steps, then the problem reduces to aggregation. If they fail at the step level — because individual CoT steps are shorter, less self-contained, and more context-dependent than single-turn QA — then fundamentally new step-level methods are needed. This RQ establishes the baseline.

此為可行性問題。若現有 UQ 方法（語意熵、SAR、語言化信心）獨立應用於各推理步驟時即可區辨正確與錯誤步驟，則問題化約為聚合問題。若在步驟層級失敗——因個別 CoT 步驟較短、自洽性較低且更依賴上下文——則需根本性的新步驟級方法。此 RQ 建立基線。

### RQ2: What aggregation function best propagates step-level uncertainty into chain-level uncertainty for predicting final-answer correctness? / 何種聚合函數最能將步驟級不確定性傳播為鏈級不確定性以預測最終答案正確性？

This is the primary methodological question. Candidate aggregation functions include: (a) product rule (independent step uncertainties multiply), (b) max-step (chain uncertainty = highest step uncertainty), (c) weighted aggregation by attention flow between steps, and (d) learned aggregation via a small neural head. The question is which aggregation most faithfully tracks the empirical probability that the chain produces a correct final answer.

此為核心方法論問題。候選聚合函數包括：(a) 乘積法則（獨立步驟不確定性相乘），(b) 最大步驟法（鏈不確定性 = 最高步驟不確定性），(c) 步驟間注意力流加權聚合，(d) 經小型神經頭學習的聚合。問題在於何種聚合最忠實地追蹤鏈產出正確最終答案的經驗機率。

### RQ3: Does chain-level UQ transfer from mathematical reasoning (GSM8K) to multi-hop factual reasoning (StrategyQA) and tool-use settings? / 鏈級 UQ 能否從數學推理（GSM8K）移轉至多跳事實推理（StrategyQA）與工具使用場景？

This tests the generalizability of the aggregation framework across task types. Mathematical reasoning has the advantage of verifiable intermediate steps (each arithmetic step has a ground-truth check); multi-hop factual reasoning and tool-use introduce qualitative steps where step-correctness is harder to define. If the framework transfers, it provides evidence of domain-general applicability; if not, domain-specific adaptation may be needed.

此測試聚合框架跨任務類型的泛化性。數學推理具有可驗證中間步驟的優勢（各算術步驟有標準答案）；多跳事實推理與工具使用引入定性步驟，步驟正確性難以定義。若框架可移轉，提供領域通用適用性的證據；否則可能需領域特定調適。

### RQ4: At which reasoning step does uncertainty first diverge between chains that ultimately produce correct vs. incorrect answers? / 最終產出正確與不正確答案的鏈之間，不確定性在哪一步驟首次分歧？

This is the mechanism/explanation question. If uncertainty diverges early (e.g., at step 1–2 of a 5-step chain), early stopping or re-sampling is practical; if it diverges late, the model commits to a wrong path before uncertainty signals appear. This has direct implications for deployment: early-divergence supports cheap "reject-and-retry" strategies; late-divergence requires more expensive multi-chain sampling.

此為機制/解釋性問題。若不確定性在早期分歧（如 5 步鏈的第 1–2 步），提前停止或重新取樣具實用性；若在後期分歧，模型在不確定性訊號出現前已鎖定錯誤路徑。此對部署有直接蘊含：早期分歧支持低成本「拒絕並重試」策略；後期分歧需更昂貴的多鏈取樣。

---

## Hypotheses / 假說

### Primary Hypothesis H1 / 主要假說

**H0 (Null / 虛無假說):**

Step-wise application of existing UQ methods (semantic entropy, SAR, verbalized confidence) to chain-of-thought reasoning does not produce chain-level uncertainty estimates that significantly discriminate correct from incorrect final answers (AUROC ≤ 0.55, equivalent to near-random).

將現有 UQ 方法（語意熵、SAR、語言化信心）逐步應用於鏈式思考推理，所產出的鏈級不確定性估計無法顯著區辨正確與不正確的最終答案（AUROC ≤ 0.55，接近隨機）。

**H1 (Alternative / 對立假說):**

At least one combination of step-level UQ method × aggregation function will achieve AUROC ≥ 0.70 for final-answer correctness prediction on GSM8K chain-of-thought outputs, significantly outperforming the single-turn baseline (whole-chain perplexity).

至少一種步驟級 UQ 方法 × 聚合函數的組合，於 GSM8K 鏈式思考輸出上對最終答案正確性預測達 AUROC ≥ 0.70，顯著優於單輪基線（整鏈 perplexity）。

**Expected Direction & Magnitude / 預期方向與幅度:**

Single-turn semantic entropy achieves AUROC ~0.79 on TriviaQA (FarquharEtAl2024). CoT introduces compounding step uncertainty and shorter per-step contexts, so we expect degradation — but a well-designed aggregation should recover significant discriminative power. The 0.70 threshold is calibrated as a meaningful margin above chance (0.50) while acknowledging expected degradation from single-turn performance.

單輪語意熵於 TriviaQA 達 AUROC ≈ 0.79（FarquharEtAl2024）。CoT 引入複合步驟不確定性與較短的每步上下文，預期效能降低——但設計良好的聚合應能恢復顯著區辨力。0.70 門檻校準為高於隨機（0.50）的有意義邊界，同時承認相對單輪效能的預期降低。

**Suggested Statistical Approach / 建議統計方法:**

Bootstrap-resampled AUROC with 95% CI over chains. Paired bootstrap test comparing chain-level UQ AUROC vs. whole-chain-perplexity AUROC. DeLong test for AUROC comparison between UQ methods.

Bootstrap 重抽樣 AUROC（95% CI，以鏈為單位）。配對 bootstrap 檢定比較鏈級 UQ AUROC vs. 整鏈 perplexity AUROC。DeLong 檢定比較 UQ 方法間 AUROC 差異。

### Secondary Hypothesis H2 / 次要假說

**H0:** Aggregation function choice does not significantly affect chain-level AUROC (all aggregation functions perform within ±0.02 AUROC of each other).

聚合函數選擇不顯著影響鏈級 AUROC（所有聚合函數 AUROC 差異在 ±0.02 內）。

**H1:** Attention-flow-weighted aggregation outperforms product-rule and max-step aggregation by ≥ 0.03 AUROC, because inter-step attention captures the information-flow structure that determines where errors compound.

注意力流加權聚合以 ≥ 0.03 AUROC 優於乘積法則與最大步驟聚合，因步驟間注意力捕捉決定錯誤複合位置的資訊流結構。

**Rationale**: DuanEtAl2023 (SAR) demonstrated that intra-sequence attention reweighting yields 2–8 AUROC points on single-turn QA. Extending this to inter-step attention in CoT is a natural generalization; the 0.03 threshold is conservative relative to SAR's single-turn gains.

DuanEtAl2023 (SAR) 展示序列內注意力重加權於單輪 QA 產出 2–8 AUROC 點增益。將此擴展到 CoT 步驟間注意力為自然推廣；0.03 門檻相對 SAR 單輪增益保守。

### Secondary Hypothesis H3 / 次要假說

**H0:** Chain-level UQ performance on GSM8K does not transfer to StrategyQA or tool-use settings (AUROC drops > 0.10 across domains).

鏈級 UQ 於 GSM8K 的效能無法移轉至 StrategyQA 或工具使用場景（跨領域 AUROC 下降 > 0.10）。

**H1:** The best-performing step-level UQ + aggregation combination on GSM8K achieves AUROC ≥ 0.65 on StrategyQA without domain-specific retraining, demonstrating task-transferable chain-level UQ.

GSM8K 上最佳步驟級 UQ + 聚合組合，於 StrategyQA 上不經領域特定重訓練即達 AUROC ≥ 0.65，展示可跨任務移轉的鏈級 UQ。

---

## Scope Boundaries / 範圍界定

### IN Scope / 範圍內

| Dimension / 維度 | Specification / 規格 |
|-----------------|---------------------|
| **Population / 模型族群** | Open-weight LLMs with attention access: LLaMA-3-8B, LLaMA-3-70B, Mistral-7B (minimum 3 models, 2 scales) / 可取得注意力的開源 LLM：LLaMA-3-8B、LLaMA-3-70B、Mistral-7B（至少 3 模型、2 規模） |
| **Intervention / 方法** | Step-level UQ (semantic entropy, SAR, verbalized confidence applied per-step) + 4 aggregation functions (product, max, attention-weighted, learned) / 步驟級 UQ（語意熵、SAR、語言化信心逐步應用）+ 4 種聚合函數 |
| **Comparison / 對照** | (1) Whole-chain perplexity baseline; (2) Single-turn UQ applied to the full chain as one pass; (3) Self-consistency (majority vote over N chain samples) / 整鏈 perplexity 基線、單輪 UQ 應用於完整鏈、自我一致性（多鏈多數投票） |
| **Primary Outcome / 主要結果** | AUROC for final-answer correctness; AURC (risk-coverage curve) / 最終答案正確性 AUROC；AURC（風險-覆蓋曲線） |
| **Secondary Outcome / 次要結果** | Step-level AUROC; early-divergence-step distribution; computational cost per chain (FLOPs/latency) / 步驟級 AUROC；早期分歧步驟分布；每鏈計算成本 |
| **Setting / 場域** | Controlled benchmark evaluation on academic compute (A100 80GB GPUs) / 學術計算資源上的受控基準評估（A100 80GB GPU） |
| **Design / 設計** | Computational empirical study with ablation across UQ methods × aggregation × tasks × models / 計算實證研究，跨 UQ 方法 × 聚合 × 任務 × 模型消融 |
| **Benchmarks / 基準** | GSM8K (math CoT), StrategyQA (multi-hop), ToolBench subset (tool-use, 1 domain) / GSM8K（數學 CoT）、StrategyQA（多跳）、ToolBench 子集（工具使用，1 領域） |
| **Timeframe / 時間框架** | ~4 months: 1 month framework design + 2 months experiments + 1 month writing / 約 4 個月：1 個月框架設計 + 2 個月實驗 + 1 個月寫作 |

### OUT Scope / 範圍外

| Exclusion / 排除項目 | Rationale / 學術理由 |
|---------------------|---------------------|
| API-only / black-box LLMs (GPT-4, Claude) / API-only 黑箱 LLM | Attention-weighted aggregation (H2) requires white-box access; black-box CoT UQ is a separate study / 注意力加權聚合需白箱存取；黑箱 CoT UQ 為獨立研究 |
| Long-form generation (essays, summaries, code) / 長格式生成 | Step-verification requires ground-truth per step; long-form lacks step-level labels / 步驟驗證需逐步標準答案；長格式缺乏步驟級標籤 |
| Training-time interventions (RLHF, DPO for calibration) / 訓練時介入 | Study targets inference-time UQ methods; training-time methods are a separate research line / 研究聚焦推論時 UQ；訓練時方法為獨立研究線 |
| Multi-agent systems (multi-LLM collaboration) / 多代理系統 | Single-agent multi-step is the tractable sub-problem; multi-agent introduces inter-model uncertainty orthogonal to this study / 單代理多步為可處理的子問題；多代理引入與本研究正交的模型間不確定性 |
| Human evaluation of UQ utility / UQ 實用性的人類評估 | Beyond the scope of a computational methods paper; deferred to a follow-up HCI study / 超出計算方法論文範圍；延後至後續 HCI 研究 |
| Novel step-level UQ methods / 全新步驟級 UQ 方法 | This study evaluates whether existing methods transfer; proposing new methods is a natural follow-up if they don't / 本研究評估現有方法能否移轉；若不能，提出新方法為自然後續 |

### Scope Rationale / 範圍邏輯

The scope is deliberately narrow: we apply existing, well-characterized UQ methods to a new setting (multi-step reasoning) and measure what breaks. This "transfer evaluation" design is tractable for a single paper and produces clearly publishable results regardless of outcome — if existing methods transfer, we report the first validated CoT UQ framework; if they fail, we characterize exactly where and why, providing a detailed roadmap for the follow-up study. The exclusion of black-box models is necessary for H2 (attention-based aggregation) but acknowledged as a limitation; a black-box extension using only verbalized confidence and self-consistency is a natural second paper.

範圍刻意收窄：我們將現有、已充分描述的 UQ 方法應用於新場景（多步推理）並測量何處失效。此「移轉評估」設計於單篇論文中可操作，無論結果如何均可發表——若現有方法可移轉，我們報告首個經驗證的 CoT UQ 框架；若失敗，我們精確描述失敗位置與原因，為後續研究提供詳細路線圖。排除黑箱模型為 H2（注意力聚合）所必需，但被承認為限制；僅使用語言化信心與自我一致性的黑箱擴展為自然的第二篇論文。

---

## Conceptual Framework / 概念框架

```
                    Chain-of-Thought LLM Reasoning
                    ┌─────────────────────────────┐
Input Question ──→  │ Step 1 → Step 2 → ... → Step N → Final Answer │
                    └────┬────────┬──────────┬──────────┬───────────┘
                         │        │          │          │
                    ┌────▼────┐  ┌▼────┐   ┌▼────┐   ┌▼────────┐
                    │ Step UQ │  │Step │   │Step │   │Final    │
                    │ Method  │  │UQ   │   │UQ   │   │Answer   │
                    │ (SE/SAR │  │     │   │     │   │Check    │
                    │ /Verb)  │  │     │   │     │   │(ground  │
                    └────┬────┘  └──┬──┘   └──┬──┘   │ truth)  │
                         │         │         │       └────┬────┘
                         ▼         ▼         ▼            │
                    ┌─────────────────────────────┐       │
                    │   Aggregation Function       │       │
                    │   (product/max/attention/    │       │
                    │    learned)                  │       │
                    └──────────────┬───────────────┘       │
                                  ▼                       │
                         Chain-Level Uncertainty           │
                         Score u(chain)                    │
                                  │                       │
                                  ▼                       ▼
                         ┌────────────────────────────────┐
                         │  Evaluation: AUROC, AURC       │
                         │  u(chain) vs. correct/incorrect │
                         └────────────────────────────────┘
```

**Step-level UQ methods applied (3)**:
1. **Semantic entropy (SE)**: Sample K step-continuations, cluster by NLI entailment, compute cluster entropy per step
2. **SAR (attention-weighted)**: Compute token-level entropy at each step, weight by attention to question + previous steps
3. **Verbalized confidence**: Prompt the model to rate its confidence in each step (0–100%)

**Aggregation functions evaluated (4)**:
1. **Product**: u(chain) = Π u(step_i) — assumes independence
2. **Max**: u(chain) = max u(step_i) — chain is as uncertain as its weakest step
3. **Attention-weighted**: u(chain) = Σ α_i · u(step_i), where α_i = attention from final-answer tokens to step_i
4. **Learned**: Small MLP trained on (u(step_1), ..., u(step_N)) → u(chain)

每步應用三種 UQ 方法（語意熵、SAR、語言化信心），再通過四種聚合函數（乘積、最大值、注意力加權、學習式）合成鏈級不確定性，以 AUROC/AURC 對照最終答案正確性評估。

---

## Risk Assessment / 風險評估

| Risk / 風險 | Likelihood / 可能性 | Impact / 影響 | Mitigation / 緩解策略 |
|------------|-------------------|-------------|---------------------|
| Step-level UQ methods fail entirely on short CoT steps (AUROC < 0.55 per step) | Medium | High — H1 fails | Design study so negative result is still publishable (characterize failure modes); include verbalized confidence which may work on short contexts | 
| Step-level ground truth labels are noisy (hard to determine if step 3 of 5 is "correct") | High | Medium — reduces AUROC ceiling | Use GSM8K where each arithmetic step is verifiable; for StrategyQA, use GPT-4-as-judge for step verification with inter-annotator agreement | 
| Semantic entropy per-step sampling is too expensive (K=10 samples × N steps = 50+ forward passes per chain) | Medium | Medium — limits practical value | Report Pareto frontier of sample count vs. AUROC; test K={3, 5, 10}; highlight that SAR/verbalized require only 1 pass per step |
| ToolBench step labels are unavailable or ambiguous | Medium | Low — affects only H3 | Drop to 2 benchmarks (GSM8K + StrategyQA) and note tool-use as future work if labels are insufficient |
| Compute budget insufficient for 70B model experiments | Low | Medium — reduces generalizability across scales | Prioritize 8B experiments; run 70B on the best-performing configuration only (not full ablation) |

---

## Gap-to-Hypothesis Traceability / 缺口到假說追溯

| Element / 元素 | Source / 來源 | Evidence / 證據 |
|---------------|-------------|----------------|
| RQ1 (step-level UQ transfer) | GAP_002 description | "No paper systematically addresses how uncertainty propagates through multi-step reasoning" — direct gap |
| RQ2 (aggregation function) | GAP_002 + SOTA Theme 1/3 | FarquharEtAl2024 uses sequence-level aggregation; DuanEtAl2023 uses attention-weighted aggregation; neither applies to inter-step structure |
| RQ3 (cross-task transfer) | GAP_002 supporting evidence | XiongEtAl2023 acknowledges "Our framework does not address multi-step reasoning settings"; GengEtAl2023 lists agentic UQ as most under-explored |
| RQ4 (divergence point) | SOTA Theme 3 debates | BadashEtAl2026 finds layer-level divergence; analogous question at step-level is unasked |
| H1 direction (AUROC ≥ 0.70) | FarquharEtAl2024 | Single-turn AUROC = 0.79 on TriviaQA; degradation expected from step-level application |
| H2 direction (attention-weighted > others) | DuanEtAl2023 (SAR) | SAR's attention reweighting yields +2–8 AUROC on single-turn; generalization to inter-step attention is the proposed mechanism |
| IN: Population (LLaMA-3, Mistral) | SOTA review | Most reviewed papers use LLaMA-2/3 and Mistral as primary evaluation models |
| OUT: Black-box exclusion | H2 design requirement | Attention-weighted aggregation requires attention-map access; verbalized-only variant is acknowledged as future work |

---

> **⛳ Checkpoint 4: 護城河最終確認**
>
> Review the IN/OUT boundaries above. Verify that:
> 1. Every OUT exclusion has an academically defensible rationale
> 2. The scope matches your actual time, budget, and resource constraints (especially: do you have A100 GPU access? Can you run LLaMA-3-70B?)
> 3. The hypotheses are testable with your available methods and data
> 4. The 4-month timeline is realistic for your situation
>
> 請審核上述 IN/OUT 邊界。確認：
> 1. 每個 OUT 排除項目都有可在學術上辯護的理由
> 2. 範圍符合您實際的時間、預算和資源限制（特別是：您是否有 A100 GPU？能否運行 LLaMA-3-70B？）
> 3. 假說可用您現有的方法和數據進行測試
> 4. 四個月的時間表對您的情況是否合理
>
> To proceed, confirm: **"Scope approved"** / **「範圍核准」**

---

Files / 檔案: `step8_hypothesis_specification.md`, `step8_journal_recommendations.md`
Next step / 下一步: After Checkpoint 4 → `/research continue` → Step 9 (`research-write`)
