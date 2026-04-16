---
session_id: "20260415"
topic: "LLM Uncertainty Quantification"
date: "2026-04-15"
step: 3
threshold: 3.5
weights: "relevance=0.50, quality=0.30, recency_impact=0.20"
---

# Screening Results / 篩選結果

> Topic / 研究主題: LLM Uncertainty Quantification (大型語言模型不確定性量化)
> Papers screened / 篩選論文數: 67
> Date / 篩選日期: 2026-04-15
> Threshold / 門檻: composite >= 3.5

## Screening Criteria / 篩選標準

### Inclusion / 納入條件
- Population (P): Studies LLMs (autoregressive transformer-based, open-weight or API-only) / 研究對象為自迴歸 Transformer 大型語言模型（含開源模型 LLaMA/Mistral/Qwen 與 API 模型 GPT-4/Claude/Gemini）
- Intervention (I): Proposes/evaluates uncertainty quantification, calibration, selective prediction, or hallucination-detection method tied to confidence/probability signals / 提出或評估與信心/機率訊號連結的 UQ、校準、選擇性預測或幻覺偵測方法
- Outcome (O): Reports calibration metrics (ECE/Brier), selective-prediction metrics (AUROC, risk-coverage), hallucination-detection accuracy, or epistemic/aleatoric decomposition / 報告校準指標、選擇性預測指標、幻覺偵測準確率或不確定性分解
- Design: Empirical study, systematic survey, or methodological position paper with concrete proposal / 實證研究、系統性綜述或具體方法論文
- Timeframe: 2022–2026 (post-Kadavath anchor); seminal pre-2022 papers retained as foundational anchors / 2022–2026（含 Kadavath 為錨點），重要前作保留為基礎

### Exclusion / 排除條件
- Off-topic application domain: rotating machinery, nuclear reactor safety, HR management, aerial/drone systems / 領域不相符（旋轉機械、核反應爐、人力資源、無人機）
- General deep-learning UQ without LLM tie-in (industrial RUL, audio ensemble distillation) / 一般深度學習 UQ 但不涉及 LLM
- Position/commentary papers without methodological content (taxonomy-only, generic AI overviews) / 純評論／分類學文章，無方法論貢獻
- Off-topic clinical applications without UQ focus (e.g., LLM medical knowledge benchmarks per se) / 臨床應用論文若不聚焦 UQ

> User-identified seed papers (10 篇使用者奠基論文) are auto-included regardless of score. / 使用者預設 10 篇強制納入。

## Summary / 摘要

| Category / 分類 | Count / 數量 | Percentage / 百分比 |
|-----------------|-------------|-------------------|
| **Included / 納入** | **45** | **67%** |
| Borderline / 邊緣 | 13 | 19% |
| Excluded / 排除 | 9 | 13% |

**Tier breakdown / 分層分布:**
- Tier 1 (>= 4.5): 12 篇
- Tier 2 (4.0–4.4): 13 篇
- Tier 3 (3.5–3.9): 20 篇

**User seeds / 使用者奠基論文**: 10/10 in Included tier

> Legend / 圖例: 🌱 = user-identified seed paper; ⭐ = hub paper (in_degree ≥ 3 in collection)

## Tier 1: Core Direct-Hit Papers / 核心直擊論文 (Composite >= 4.5)


| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| paper_016 | Uncertainty Quantification and Confidence Calibration in Large Langua… | Xiaoou Liu et al. | 2025 | 5.0 | 4.5 | 5.0 | **4.85** | Direct LLM-UQ match across multiple core phrases |
| paper_005 🌱 | SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Gen… | Potsawee Manakul et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_007 🌱 ⭐ | Language Models (Mostly) Know What They Know | Saurav Kadavath et al. | 2022 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_017 🌱 | Teaching Models to Express Their Uncertainty in Words | Stephanie Lin et al. | 2022 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_019 🌱 | Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimati… | Lorenz Kuhn et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_024 🌱 | A Survey on Uncertainty Quantification Methods for Deep Learning | Wenchong He et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_031 🌱 | Shifting Attention to Relevance: Towards the Predictive Uncertainty Q… | Jinhao Duan et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_040 🌱 | Just Ask for Calibration: Strategies for Eliciting Calibrated Confide… | Katherine Tian et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_045 🌱 | A Survey of Confidence Estimation and Calibration in Large Language M… | Jiahui Geng et al. | 2023 | 5.0 | 4.0 | 5.0 | **4.7** | User-identified seminal paper |
| paper_004 🌱 | Detecting hallucinations in large language models using semantic entr… | Sebastian Farquhar et al. | 2024 | 5.0 | 3.5 | 5.0 | **4.55** | User-identified seminal paper |
| paper_018 🌱 | Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confid… | Miao Xiong et al. | 2023 | 5.0 | 3.5 | 5.0 | **4.55** | User-identified seminal paper |
| paper_001 ⭐ | Survey of Hallucination in Natural Language Generation | Ziwei Ji et al. | 2022 | 4.0 | 5.0 | 5.0 | **4.5** | Foundational NLG-hallucination survey (3064 cites, ACM Computing Surveys); struc |

## Tier 2: Strong Supporting Papers / 強力支撐論文 (Composite 4.0–4.4)


| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| paper_009 | 🧜Siren’s Song in the AI Ocean: A Survey on Hallucination in Large Lan… | Yue Zhang et al. | 2025 | 4.0 | 4.5 | 5.0 | **4.35** | Comprehensive LLM hallucination survey in Computational Linguistics |
| paper_008 | Sources of Hallucination by Large Language Models on Inference Tasks | Nick McKenna et al. | 2023 | 4.5 | 3.5 | 5.0 | **4.3** | LLM-specific hallucination source analysis (LLaMA/GPT-3.5/PaLM behavioural studi |
| paper_021 | A Survey of Confidence Estimation and Calibration in Large Language M… | Jiahui Geng et al. | 2024 | 5.0 | 3.0 | 4.5 | **4.3** | Direct LLM-UQ match across multiple core phrases |
| paper_026 | Revisiting Epistemic Markers in Confidence Estimation: Can Markers Ac… | Jiayu Liu et al. | 2025 | 5.0 | 3.0 | 4.5 | **4.3** | Direct LLM-UQ match across multiple core phrases |
| paper_056 | Token-Level Density-Based Uncertainty Quantification Methods for Elic… | Artem Vazhentsev et al. | 2025 | 4.5 | 4.0 | 3.5 | **4.15** | Token-level density-based UQ for LLM (NAACL 2025) |
| paper_030 | Know Your Limits: A Survey of Abstention in Large Language Models | Bingbing Wen et al. | 2025 | 4.0 | 4.0 | 4.5 | **4.1** | Directly addresses LLM uncertainty or calibration |
| paper_038 | A Survey of Uncertainty Estimation Methods on Large Language Models | Zhiqiu Xia et al. | 2025 | 5.0 | 3.0 | 3.5 | **4.1** | Direct LLM-UQ match across multiple core phrases |
| paper_014 | On Hallucination and Predictive Uncertainty in Conditional Language G… | Yijun Xiao et al. | 2021 | 4.5 | 3.5 | 3.5 | **4.0** | Foundational link between predictive uncertainty and hallucination in conditiona |
| paper_020 | Large language model uncertainty proxies: discrimination and calibrat… | Thomas Savage et al. | 2024 | 5.0 | 2.0 | 4.5 | **4.0** | Direct LLM-UQ match across multiple core phrases |
| paper_027 | From Calibration to Collaboration: LLM Uncertainty Quantification Sho… | Siddartha Devic et al. | 2025 | 5.0 | 2.0 | 4.5 | **4.0** | Direct LLM-UQ match across multiple core phrases |
| paper_053 | InternalInspector I2: Robust Confidence Estimation in LLMs through In… | Mohammad Beigi et al. | 2024 | 4.5 | 3.5 | 3.5 | **4.0** | InternalInspector: attention/internal-state UQ (EMNLP Findings 2024) — user prio |
| paper_064 | Between the Layers Lies the Truth: Uncertainty Estimation in LLMs Usi… | Zvi Badash et al. | 2026 | 4.5 | 3.5 | 3.5 | **4.0** | Intra-layer uncertainty estimation in LLMs — user priority direction |
| paper_067 | The Dunning-Kruger Effect in Large Language Models: An Empirical Stud… | Sudipta Ghosh et al. | 2026 | 4.5 | 3.5 | 3.5 | **4.0** | Strong LLM-UQ alignment |

## Tier 3: Contextual / Adjacent Papers / 脈絡與相鄰論文 (Composite 3.5–3.9)


| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale |
|----|-------|---------|------|-----|------|-----|---------------|-----------|
| paper_011 | A Mathematical Investigation of Hallucination and Creativity in GPT M… | Minhyeok Lee | 2023 | 4.0 | 3.5 | 4.5 | **3.95** | Mathematical characterization of GPT hallucination-creativity trade-off (95 cite |
| paper_039 | Monte Carlo Temperature: a robust sampling strategy for LLM's uncerta… | Nicola Cecere et al. | 2025 | 5.0 | 2.5 | 3.5 | **3.95** | Direct LLM-UQ match across multiple core phrases |
| paper_049 | Measuring Aleatoric and Epistemic Uncertainty in LLMs: Empirical Eval… | K. Wang et al. | 2025 | 5.0 | 2.5 | 3.5 | **3.95** | Direct LLM-UQ match across multiple core phrases |
| paper_046 | Benchmarking Large Language Model Uncertainty for Prompt Optimization | Pei-Fu Guo et al. | 2024 | 4.5 | 3.0 | 3.5 | **3.85** | Strong LLM-UQ alignment |
| paper_050 | SConU: Selective Conformal Uncertainty in Large Language Models | Zhiyuan Wang et al. | 2025 | 4.5 | 3.0 | 3.5 | **3.85** | SConU: selective conformal uncertainty for LLMs (direct method) |
| paper_065 | I-CALM: Incentivizing Confidence-Aware Abstention for LLM Hallucinati… | Haotian Zong et al. | 2026 | 4.5 | 3.0 | 3.5 | **3.85** | Strong LLM-UQ alignment |
| paper_057 | Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circ… | Amirhosein Ghasemabadi et al. | 2025 | 4.5 | 3.0 | 3.5 | **3.85** | Internal-circuit self-failure prediction — user priority direction (attention-ba |
| paper_036 | Bayesian Prompt Ensembles: Model Uncertainty Estimation for Black-Box… | Francesco Tonolini et al. | 2024 | 5.0 | 2.0 | 3.5 | **3.8** | Direct LLM-UQ match across multiple core phrases |
| paper_037 | Uncertainty quantification in large language models through convex hu… | Ferhat Özgür Çatak et al. | 2024 | 5.0 | 2.0 | 3.5 | **3.8** | Direct LLM-UQ match across multiple core phrases |
| paper_041 | Simple Yet Effective: An Information-Theoretic Approach to Multi-LLM … | Maya Kruse et al. | 2025 | 5.0 | 2.0 | 3.5 | **3.8** | Direct LLM-UQ match across multiple core phrases |
| paper_051 | UvA-MT at WMT25 Evaluation Task: LLM Uncertainty as a Proxy for Trans… | Di Wu et al. | 2025 | 5.0 | 2.0 | 3.5 | **3.8** | Direct LLM-UQ match across multiple core phrases |
| paper_060 | MetaFaith: Faithful Natural Language Uncertainty Expression in LLMs | G. Liu et al. | 2025 | 5.0 | 2.0 | 3.5 | **3.8** | Direct LLM-UQ match across multiple core phrases |
| paper_025 | Position: Uncertainty Quantification Needs Reassessment for Large-lan… | Michael Kirchhof et al. | 2025 | 4.5 | 2.0 | 4.5 | **3.75** | Strong LLM-UQ alignment |
| paper_034 | Confidence Under the Hood: An Investigation into the Confidence-Proba… | Abhishek Kumar et al. | 2024 | 4.0 | 3.5 | 3.5 | **3.75** | Directly studies LLM confidence-probability alignment (verbalized vs token probs |
| paper_032 | COIN: Uncertainty-Guarding Selective Question Answering for Foundatio… | Zhiyuan Wang et al. | 2025 | 4.0 | 2.5 | 4.5 | **3.65** | Multiple UQ/LLM terms indicate close alignment |
| paper_042 | OpenFactCheck: A Unified Framework for Factuality Evaluation of LLMs | Hasan Iqbal et al. | 2024 | 3.5 | 4.0 | 3.5 | **3.65** | OpenFactCheck LLM factuality framework (EMNLP 2024 demo); adjacent to UQ via fac |
| paper_035 | Uncertainty in Language Models: Assessment through Rank-Calibration | Xinmeng Huang et al. | 2024 | 4.0 | 3.0 | 3.5 | **3.6** | Rank-calibration assessment of LLM uncertainty — direct method paper |
| paper_054 | Can LLMs Detect Their Confabulations? Estimating Reliability in Uncer… | Tianyi Zhou et al. | 2025 | 4.0 | 3.0 | 3.5 | **3.6** | Directly addresses LLM uncertainty or calibration |
| paper_063 | BaseCal: Unsupervised Confidence Calibration via Base Model Signals | Hexiang Tan et al. | 2026 | 4.0 | 3.0 | 3.5 | **3.6** | BaseCal unsupervised LLM confidence calibration |
| paper_058 | Is There No Such Thing as a Bad Question? H4R: HalluciBot for Ratioci… | William Watson et al. | 2025 | 3.0 | 4.5 | 3.5 | **3.55** | H4R HalluciBot: hallucination eval framework; borderline UQ relevance |

---

## Borderline Papers / 邊緣論文 (Composite 3.0–3.4)

> **⛳ Checkpoint 2: 邊緣打撈**

> Review the papers below — these scored close to threshold and may include cross-disciplinary or non-standard-terminology work missed by automatic scoring.
> 請審核以下邊緣論文，這些分數接近門檻，可能包含使用非標準術語或跨領域的相關研究。
>
> Mark any paper you want to include with `include paper_XXX` and I'll add it to the shortlist before proceeding to Step 4.
> 若有想納入的論文，請以 `include paper_XXX` 標記，我會加入精選清單後再進入 Step 4。

| ID | Title | Authors | Year | Rel | Qual | Rec | **Composite** | Rationale | Hub? |
|----|-------|---------|------|-----|------|-----|---------------|-----------|------|
| paper_013 | What large language models know and what people think they know | Mark Steyvers et al. | 2025 | 2.5 | 4.0 | 5.0 | **3.45** | Tangential — only one UQ or LLM term | — |
| paper_028 | Enhancing Vision-Language Model Reliability with Uncertainty-Guided D… | Yi Fang et al. | 2024 | 3.5 | 3.0 | 4.0 | **3.45** | Vision-language model uncertainty-guided dropout; adjacent (multimodal LLM UQ) | — |
| paper_043 | A Systematic Literature Review of Retrieval-Augmented Generation: Tec… | Andrew Brown et al. | 2025 | 3.0 | 4.0 | 3.5 | **3.4** | Systematic review of RAG; RAG quality affects UQ but not core | — |
| paper_055 | From Illusion to Insight: A Taxonomic Survey of Hallucination Mitigat… | Ioannis Kazlaris et al. | 2025 | 3.0 | 4.0 | 3.5 | **3.4** | Hallucination taxonomy survey; overlap with existing surveys | — |
| paper_002 | Large language models encode clinical knowledge | Karan Singhal et al. | 2023 | 2.0 | 4.5 | 5.0 | **3.35** | Clinical knowledge in LLMs (Nature Med); not UQ-focused | — |
| paper_047 | An Information-Theoretic Perspective on Multi-LLM Uncertainty Estimat… | Maya Kruse et al. | 2025 | 3.5 | 3.0 | 3.5 | **3.35** | Multi-LLM information-theoretic UQ (no abstract — scored on title+venue signal) | — |
| paper_059 | Mechanistic Control of Language Models | Li, Kenneth | 2025 | 3.5 | 3.0 | 3.5 | **3.35** | Mechanistic control of LLMs dissertation; relevant but methodology broad | — |
| paper_023 | From Aleatoric to Epistemic: Exploring Uncertainty Quantification Tec… | Tianyang Wang et al. | 2025 | 3.0 | 3.0 | 4.5 | **3.3** | General AI UQ review (aleatoric/epistemic); only partially LLM-focused | — |
| paper_066 | On the Evaluation of Capability Estimation Methods for Large Language… | Qiang Hu et al. | 2026 | 2.5 | 4.0 | 3.5 | **3.15** | LLM capability estimation (AutoEval); adjacent to but not core UQ | — |
| paper_062 | Variational Visual Question Answering for Uncertainty-Aware Selective… | T. J. Wieczorek et al. | 2025 | 3.0 | 3.0 | 3.5 | **3.1** | Variational VQA selective prediction — multimodal adjacent | — |
| paper_012 | AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Cha… | Ranjan Sapkota et al. | 2025 | 2.0 | 3.5 | 5.0 | **3.05** | Agentic-AI taxonomy position paper; not UQ-specific | — |
| paper_022 | DELL: Generating Reactions and Explanations for LLM-Based Misinformat… | Herun Wan et al. | 2024 | 2.5 | 3.0 | 4.5 | **3.05** | DELL misinformation detection using LLMs; not UQ/calibration-focused | — |
| paper_010 | The Era of Artificial Intelligence Deception: Unraveling the Complexi… | S. Williamson et al. | 2024 | 2.5 | 2.5 | 5.0 | **3.0** | AI deception/hallucination overview; low methodological depth for UQ | — |

---

## Excluded Papers / 排除論文 (Composite < 3.0)

| ID | Title | Year | Rel | Qual | Rec | **Composite** | Exclusion Reason / 排除原因 |
|----|-------|------|-----|------|-----|---------------|---------------------------|
| paper_044 | Calibrated Decomposition of Aleatoric and Epistemic Uncertainty in De… | 2025 | 2.5 | 3.0 | 3.5 | **2.85** | General deep-learning aleatoric/epistemic decomposition; not LLM-specific |
| paper_048 | HybridFlow: Quantification of Aleatoric and Epistemic Uncertainty wit… | 2025 | 2.5 | 3.0 | 3.5 | **2.85** | General probabilistic ML UQ (HybridFlow); not LLM-specific |
| paper_052 | Few-shot RUL Prediction with A Hypernetwork Structure Incorporating U… | 2024 | 2.0 | 3.0 | 3.5 | **2.6** | Few-shot RUL prediction with hypernetwork — industrial UQ, not LLM |
| paper_061 | Remaining Useful Life Prediction and Uncertainty Quantification with … | 2025 | 2.0 | 3.0 | 3.5 | **2.6** | Remaining Useful Life UQ — industrial, not LLM |
| paper_006 | Towards trustworthy rotating machinery fault diagnosis via attention … | 2023 | 1.5 | 2.5 | 5.0 | **2.5** | Rotating machinery fault diagnosis — off-topic mechanical domain |
| paper_029 | Evidence, my Dear Watson: Abstractive dialogue summarization on learn… | 2023 | 2.0 | 3.0 | 3.0 | **2.5** | Dialogue summarization evidence — tangential |
| paper_033 | Logit-Based Ensemble Distribution Distillation for Robust Autoregress… | 2023 | 2.0 | 3.0 | 3.0 | **2.5** | Audio/logit ensemble distillation — not LLM |
| paper_015 | Deep learning for safety assessment of nuclear power reactors: Reliab… | 2022 | 1.5 | 3.0 | 4.0 | **2.45** | Nuclear reactor safety deep learning — off-topic engineering domain |
| paper_003 | Human resource management in the age of generative artificial intelli… | 2023 | 1.0 | 3.0 | 5.0 | **2.4** | HR management & generative AI; off-topic |

---

## Hub Paper Summary / 核心引用論文摘要

Papers with in_degree ≥ 3 within the collection — structurally important regardless of pure topical alignment.

| ID | Title | In-Degree | Cluster | Status | Note |
|----|-------|-----------|---------|--------|------|
| paper_001 | Survey of Hallucination in Natural Language Gener… | 4 | survey_position | Included | cited by 4 in-collection papers |
| paper_007 | Language Models (Mostly) Know What They Know | 3 | verbalized_self_confidence | Included | User seed; cited by 3 in-collection papers |

---

Files / 檔案: `step3_screening_results.md`, `step3_shortlist.json`
Next step / 下一步: Resolve Checkpoint 2 → `/research continue` → Step 4 (`research-export`)
