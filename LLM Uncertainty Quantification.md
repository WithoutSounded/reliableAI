## LLM Uncertainty Quantification 深入研究指南

### 核心關鍵字（Google Scholar / arXiv 搜尋用）

**基礎術語**

- `LLM uncertainty quantification` / `UQ for LLMs`
- `LLM calibration` / `confidence calibration`
- `selective prediction` / `selective generation`
- `abstention` / `知道何時說不知道`

**方法流派關鍵字**

- `semantic entropy` / `semantic uncertainty`
- `verbalized confidence` / `self-verbalized uncertainty`（讓模型自己說信心）
- `P(True)` / `self-evaluation`
- `length-normalized likelihood`
- `Monte Carlo dropout for LLMs` / `ensemble uncertainty`
- `consistency-based uncertainty`（多次採樣比對）
- `epistemic vs aleatoric uncertainty in LLMs`

**評估指標**

- `Expected Calibration Error (ECE)`
- `AUROC for misclassification detection`
- `Brier score`
- `selective risk` / `risk-coverage curve`

---

### 必讀論文（依影響力排序）

**奠基性 / 必讀**

1. **Kadavath et al. 2022** — "Language Models (Mostly) Know What They Know" (Anthropic) → P(True) 起源，必讀第一篇
2. **Farquhar et al. 2024 (Nature)** — "Detecting hallucinations in LLMs using semantic entropy" → 目前 SOTA 之一，概念優雅
3. **Lin et al. 2022** — "Teaching Models to Express Their Uncertainty in Words" → Verbalized confidence 起源

**方法深化** 4. **Kuhn et al. 2023** — "Semantic Uncertainty: Linguistic Invariances..."（Farquhar 前作） 5. **Xiong et al. 2024 (ICLR)** — "Can LLMs Express Their Uncertainty? An Empirical Evaluation..." 6. **Tian et al. 2023** — "Just Ask for Calibration" 7. **Duan et al. 2024** — "Shifting Attention to Relevance" (SAR) 8. **Manakul et al. 2023** — SelfCheckGPT（雖列在 hallucination，方法可遷移）

**Survey（快速建立全貌）** 9. **Geng et al. 2024** — "A Survey of Confidence Estimation and Calibration in LLMs" 10. **Huang et al. 2024** — "A Survey on Uncertainty Quantification Methods for Deep Learning"

---

### 可切入的研究方向（帶差異化空間）

依新穎度 × 可行性推薦：

|#|方向|說明|難度|
|---|---|---|---|
|1|**Token-level → Sequence-level UQ 聚合**|如何把每個 token 的信心合理加總？目前多用平均/最小，但 open problem|⭐⭐|
|2|**Long-form generation 的 UQ**|現有方法多在 QA 短答案，長文本仍有空間|⭐⭐⭐|
|3|**Reasoning chain 的 UQ**|CoT 每一步的信心如何估？錯誤如何傳遞？|⭐⭐⭐|
|4|**Multilingual / Code / Math 領域的 UQ**|多數研究集中英文 QA，垂直領域少|⭐⭐|
|5|**White-box（logits）vs Black-box（API）方法比較**|只能用 API 時怎麼做？|⭐⭐|
|6|**Attention-based UQ**（呼應你原本想法）|用 attention pattern 作為 epistemic signal，研究較少|⭐⭐⭐|
|7|**UQ for Agentic / Tool-use LLM**|新興場景，幾乎空白|⭐⭐⭐⭐|

---

### 標準 Benchmark（實驗要用）

- **TriviaQA / Natural Questions / SQuAD** — QA calibration 老三樣
- **TruthfulQA** — 對抗性事實
- **MMLU** — 多選題 calibration
- **GSM8K / MATH** — 推理信心
- **HaluEval / FActScore** — 跨領域

---

### 建議起手式

1. 先讀 **Kadavath 2022 + Farquhar 2024 + Geng survey** 這三篇建立全景（約 2 週）
2. 從上面 7 個方向中挑 1–2 個有興趣的，做 literature gap 分析
3. 選一個**小規模可跑**的 benchmark（建議 TriviaQA）先複現 baseline

要我幫你用 `research-init` skill 正式啟動一次文獻調研 session 嗎？可以把 PICO 框架和搜尋策略自動生成。