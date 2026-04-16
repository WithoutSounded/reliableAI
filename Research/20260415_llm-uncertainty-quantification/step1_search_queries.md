---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
---

# Search Queries / 搜尋策略

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Generated / 產生日期: 2026-04-15

## PICO Framework

| Component | English | 繁體中文 |
|-----------|---------|---------|
| **P** Population | Large Language Models (autoregressive transformer-based); both open-weight (LLaMA, Mistral, Qwen) and API-only/black-box models (GPT-4, Claude, Gemini) | 大型語言模型（自回歸 transformer 架構），含開源權重模型與僅 API 存取的黑盒模型 |
| **I** Intervention | UQ methods: semantic entropy, verbalized confidence（讓模型自陳信心）, P(True)/self-evaluation, consistency-based sampling (SelfCheckGPT), ensemble/MC-dropout, attention-based signals, length-normalized likelihood, token→sequence aggregation | 不確定性量化方法：語意熵、語言化信心、P(True) 自評估、一致性取樣、集成/MC-dropout、基於注意力、長度正規化概似、token 到序列的聚合 |
| **C** Comparison | Baseline likelihood/perplexity; temperature-scaling; white-box（可取得 logits） vs black-box（僅 API）方法族之間比較；hallucination-detection baselines | 基準概似/perplexity；溫度縮放；白盒（可存取 logits）vs 黑盒（僅 API）方法族對照；幻覺偵測基線 |
| **O** Outcome | ECE（Expected Calibration Error 預期校準誤差）, Brier score, AUROC for misclassification detection, risk-coverage curve, selective risk, hallucination detection accuracy, epistemic vs aleatoric decomposition validity | ECE、Brier 分數、誤判偵測 AUROC、風險-覆蓋率曲線、選擇性風險、幻覺偵測準確度、認知/偶然不確定性分解效度 |
| Setting | Short-form QA (TriviaQA, NaturalQuestions, SQuAD, TruthfulQA); multi-choice (MMLU); reasoning (GSM8K, MATH, CoT); long-form (HaluEval, FActScore); emerging: code, multilingual, agentic/tool-use | 短答 QA、多選題、推理鏈、長文本生成；新興：程式碼、多語、代理/工具使用 |
| Timeframe | 2022–2026 (Kadavath 2022 anchor; 2023–2026 SOTA emphasis) | 2022–2026 年（以 Kadavath 2022 為錨點，聚焦 2023–2026 SOTA） |

---

## Queries

### Q1: Core Terms + Population
**Query:** `("large language model" OR LLM) AND ("uncertainty quantification" OR "confidence calibration" OR "selective prediction")`
**Rationale / 策略說明:** Direct hit on the primary topic — captures papers explicitly framing their work as UQ / calibration / selective prediction for LLMs. / 直接命中核心主題，捕捉明確以 UQ / 校準 / 選擇性預測為框架的 LLM 研究。

### Q2: Synonyms + Method-family Terminology
**Query:** `("semantic entropy" OR "semantic uncertainty" OR "verbalized confidence" OR "P(True)" OR "self-evaluation" OR "consistency-based") AND (LLM OR "language model" OR generation)`
**Rationale / 策略說明:** Catches papers using specific method names rather than the umbrella term "UQ" — essential since SOTA papers (Farquhar, Kadavath, Lin) often foreground method names. / 抓取以具體方法名稱（而非 UQ 總稱）發表的論文；SOTA 論文多以方法名為主標題，此策略不可或缺。

### Q3: Mechanism + Theoretical Basis
**Query:** `("epistemic uncertainty" OR "aleatoric uncertainty") AND ("language model" OR autoregressive OR "next-token") AND (logits OR likelihood OR perplexity)`
**Rationale / 策略說明:** Finds the theoretical grounding — epistemic/aleatoric decomposition, likelihood-based signals, token-level probability mechanisms underlying LLM UQ. / 尋找理論基礎論文：認知/偶然不確定性分解、基於概似的訊號、以及支撐 LLM UQ 的 token 層機率機制。

### Q4: Evaluation Metrics + Benchmarks
**Query:** `("Expected Calibration Error" OR ECE OR "risk-coverage" OR AUROC) AND LLM AND (TriviaQA OR MMLU OR TruthfulQA OR GSM8K OR HaluEval OR FActScore)`
**Rationale / 策略說明:** Targets empirical/benchmark papers — finds works with rigorous evaluation on standard UQ benchmarks, useful for baseline comparison and reproducibility. / 鎖定實證/基準論文，尋找在標準 UQ 基準上做嚴謹評估的作品，便於基線比對與結果再現。

### Q5: Cross-Disciplinary + Emerging Angles (aligns with user priority)
**Query:** `("attention-based" OR "attention pattern" OR "chain-of-thought" OR "tool-use" OR agentic OR "long-form generation") AND (uncertainty OR confidence OR hallucination) AND (LLM OR transformer)`
**Rationale / 策略說明:** Targets the user's priority direction (attention-based UQ) plus emerging frontiers (CoT-step UQ, agentic UQ, long-form UQ) where literature is sparse but differentiation potential is high. / 對準使用者優先方向（基於注意力的 UQ）以及新興前沿（CoT 步驟 UQ、代理/工具使用 UQ、長文本 UQ），這些領域文獻稀少但差異化潛力最高。

---

> **Checkpoint 1: 初始定向核准 / Initial Orientation Approval**
>
> Please review the PICO framework and search queries above. / 請檢閱上述 PICO 框架與搜尋策略。
>
> - Are the PICO components accurate? / PICO 各元素是否準確反映你要的研究範圍？
> - Any missing keywords or synonyms? / 有遺漏的關鍵字或同義詞嗎？（例如：`abstention`、`uncertainty estimation`、`trustworthy LLM`、`honest AI`？）
> - Any off-target dimensions to remove? / 有需要移除的偏離維度嗎？
> - Is the timeframe (2022–2026) appropriate? / 時間範圍（2022–2026）是否合適？
> - Should Q5 lean even more heavily toward attention-based UQ (your priority)? / Q5 是否要更偏向「基於注意力的 UQ」（你的優先方向）？
>
> **When ready, reply "approved" / "通過" / "proceed" to advance to Step 2 (`research-search`).**
> **準備好後，回覆「approved / 通過 / proceed」即可進入 Step 2（文獻搜尋）。**
