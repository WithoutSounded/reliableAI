---
title: Prof. Tianhao Wang (王天浩) — 研究側寫 / Research Profile
source_site: https://tiiao.github.io/
paper_dir: ./paper/
compiled: 2026-04-15
language: 中英對照 / Bilingual ZH–EN
---

# Prof. Tianhao Wang (王天浩) — 研究側寫 / Research Profile

> 本檔是根據 [tiiao.github.io](https://tiiao.github.io/) 的公開資料與 [paper/](paper/) 資料夾中 18 份 PDF 所整理的深度側寫。
> This document is a deep profile compiled from the public website and the 18 PDFs in [paper/](paper/).

---

## 0. TL;DR

**中文**
Tianhao Wang（王天浩）是 UC San Diego Halıcıoğlu 資料科學研究院（HDSI）新任助理教授（2025 秋上任），Yale 統計與資料科學系博士（2024，指導教授 Zhou Fan）。他的研究風格是**「把學習演算法本身當成研究對象」**——用高維機率、隨機矩陣、自由機率、梯度流動力學等工具去刻畫演算法實際會走到哪裡、會學到什麼。目前有三條主線：(1) **Approximate Message Passing (AMP) 普適性理論**（博論核心、與 Zhou Fan 團隊長期合作）；(2) **Transformer 訓練動力學與 in-context learning 理論**（與 Siyu Chen / Heejune Sheen / Zhuoran Yang 合作，COLT / NeurIPS / ICLR）；(3) **新興的 LLM 可靠性 / 對齊方向**（與 TTIC Zhiyuan Li、UMich Qiaozhu Mei 合作，探討 RLVR 訓練下的過度自信、可棄權模型、perception vs reasoning bottleneck）。博士論文題為 *Algorithm Dynamics in Modern Statistical Learning: Asymptotics, Universality, and Implicit Regularization*，等於在宣告這三條線的統一基調。

**English**
Tianhao Wang is a brand-new Assistant Professor at UC San Diego's Halıcıoğlu Data Science Institute (HDSI, starting Fall 2025), with a Yale PhD in Statistics & Data Science (2024, advisor: Zhou Fan). His signature move is to **treat learning algorithms themselves as the object of study** — using high-dimensional probability, random matrix theory, free probability, and gradient-flow dynamics to characterize *where the algorithm actually goes* and *what the model ends up learning*. Three active research threads: (1) **universality theory for Approximate Message Passing (AMP)** (his thesis core, ongoing with Zhou Fan); (2) **training dynamics and in-context learning (ICL) theory for transformers** (with Siyu Chen / Heejune Sheen / Zhuoran Yang; COLT / NeurIPS / ICLR); (3) an **emerging LLM-reliability / alignment line** (with Zhiyuan Li at TTIC and Qiaozhu Mei at Michigan — studying RLVR-induced overconfidence, abstention training, and perception vs reasoning bottlenecks). His dissertation title — *Algorithm Dynamics in Modern Statistical Learning: Asymptotics, Universality, and Implicit Regularization* — essentially announces the unifying frame across all three.

---

## 1. 基本資料 / At a Glance

| | |
|---|---|
| **姓名 / Name** | Tianhao Wang（王天浩） |
| **現職 / Position** | Assistant Professor, Halıcıoğlu Data Science Institute (HDSI), UC San Diego（2025 秋起 / since Fall 2025） |
| **先前職位 / Previous** | Research Assistant Professor, Toyota Technological Institute at Chicago (TTIC), 2024–2025 |
| **博士 / PhD** | Statistics & Data Science, Yale University, 2024（指導教授 / advisor: **Zhou Fan**） |
| **Email** | `tianhaowang@ucsd.edu` |
| **個人網站 / Site** | <https://tiiao.github.io/> |
| **研究大方向 / Broad area** | Machine Learning · Optimization · High-Dimensional Statistics |
| **合作圈 / Key collaborators** | Zhou Fan, Zhiyuan Li, Zhuoran Yang, Jason D. Lee, Harrison H. Zhou, Quanquan Gu, Qiaozhu Mei, Sanjeev Arora；學生 / mentees：Siyu Chen, Heejune Sheen, Shuo Xie, Xinyi Zhong |

---

## 2. 研究三大主線 / Three Research Threads

### 2.1 AMP 普適性理論 / Universality of Approximate Message Passing

**中文**
AMP 是高維統計裡一類以「狀態演化 (state evolution)」為核心的迭代演算法——它在每一步的經驗分佈能被一條遞推式精確預測。但傳統證明幾乎只對「entries 獨立同分佈高斯」或「正交不變 ensembles」成立。Wang 的博論第 2、3 章以及三篇期刊論文（[Tianhao2024](paper/Tianhao2024.pdf)、[Xinyi2024](paper/Xinyi2024.pdf)、[Max2025](paper/Max2025.pdf)）把 AMP 普適性推廣到：
- **異質方差、重尾、稀疏**的隨機矩陣（廣義 Wigner 類）；
- **正交不變 ensembles 下的矩陣值（multivariate）迭代**，並提供 spectral initialization 與相對應的 Onsager 修正；
- **non-separable 非線性**（如影像重建、矩陣 sensing、深度生成先驗中常見的），透過提出 **Bounded Composition Property (BCP)** 作為充分條件。

技術工具是「tensor network + moment method + 多項式逼近」，並把 AMP 普適性與 tensor network 的漸進自由性 (asymptotic freeness) 連起來——這是與 Zhou Fan 團隊合作下的長期方案。

**English**
AMP is a family of high-dimensional iterative algorithms whose empirical per-iterate distribution is predicted exactly by a recursion called *state evolution*. Classical proofs only handle i.i.d. Gaussian entries or orthogonally invariant ensembles. Wang's thesis (Chapters 2–3) and three derivative papers — [Tianhao2024](paper/Tianhao2024.pdf), [Xinyi2024](paper/Xinyi2024.pdf), [Max2025](paper/Max2025.pdf) — push AMP universality to:
- random matrices with **heterogeneous variances, heavy tails, and sparsity** (generalized Wigner);
- **matrix-valued AMP on orthogonally invariant ensembles** with a data-independent *spectral* initialization and the matching Onsager correction;
- **non-separable non-linearities** (as used in image reconstruction, matrix sensing, deep generative priors), via a new **Bounded Composition Property (BCP)** as a sufficient condition.

The technical engine is "tensor network + moment method + polynomial approximation", yielding an asymptotic-freeness statement for tensor networks — a long-running program with the Fan group.

**代表作 / Flagship papers**
- [Tianhao2024.pdf](paper/Tianhao2024.pdf) — *Universality of AMP and Tensor Networks*（博論 Ch.2 的期刊版 / journal version of thesis Ch. 2）
- [Xinyi2024.pdf](paper/Xinyi2024.pdf) — *AMP for Orthogonally Invariant Ensembles with Multivariate Non-linearities and Spectral Initialization*（*Information and Inference*, 2024）
- [Max2025.pdf](paper/Max2025.pdf) — *On Universality of Non-separable AMP Algorithms*（近作 / recent）
- [Zhoufan2024.pdf](paper/Zhoufan2024.pdf) — *MLE for High-Noise Group Orbit Estimation & Cryo-EM*（*Annals of Statistics*, 2024；應用於 cryo-EM / applied to cryo-EM）

---

### 2.2 Transformer 訓練動力學 & In-Context Learning 理論 / Transformer Training Dynamics & ICL Theory

**中文**
這是他博士後期開啟、也是未來幾年最活躍的主線。核心問題：**「為什麼訓練好的 transformer 會 in-context learning？每個架構零件（多頭、softmax、FFN、RPE）到底各做了什麼？」** 他不走「用訓練好的 transformer 去擬合 ICL 行為」的行為主義路線，而是直接做**梯度流收斂性證明**：給定合理初始化，GF 會把參數帶到哪個解？每個訓練階段在算什麼？

- [Siyu2024.pdf](paper/Siyu2024.pdf)（COLT 2024）：第一個**多頭 softmax attention** 的收斂證明，刻畫出「warm-up → emergence → convergence」三階段，證明 H 個 head 會**自發分工**處理 I 個 task（每 head 負責一個），loss 比單 head 低 H 倍。
- [Siyuchen2025.pdf](paper/Siyuchen2025.pdf)（NeurIPS 2024）：兩層 transformer 學 n-gram Markov chain，**端到端地把每個架構零件（RPE、FFN、第二層 attention）指派到具體的 ICL 角色**——RPE 當 copier、FFN 當 selector（基於 χ² mutual information）、第二層 attention 當 exponential kernel classifier。把經典 "induction head" 機制推廣到 n-gram。
- [Angeliki2024.pdf](paper/Angeliki2024.pdf)：Transformer 能在 context 裡「模擬二階優化」（Newton's method for logistic regression），給出深度/寬度 vs. 誤差 ε 的明確構造。
- [Heejune2024.pdf](paper/Heejune2024.pdf)：單層 softmax attention 在 K、Q 分別參數化下的 **implicit regularization 是 nuclear norm**（與把 K、Q 合併成 W 時的 Frobenius norm 正則化形成對比）。

**English**
This is the thread he opened late in his PhD and where he is currently most prolific. The driving question: **"Why does a trained transformer do ICL, and what is each architectural piece actually doing?"** He does not take the behaviorist route of fitting trained transformers to ICL behavior — he proves gradient-flow convergence theorems: under reasonable initialization, where does GF take the weights, and what is each phase of training computing?

- [Siyu2024.pdf](paper/Siyu2024.pdf) (COLT 2024): first convergence proof for a **multi-head softmax attention** model, identifying three training phases (warm-up → emergence → convergence) and proving spontaneous **task allocation** (each of H heads converges to handling a distinct task), with loss a factor of H below any single-head model.
- [Siyuchen2025.pdf](paper/Siyuchen2025.pdf) (NeurIPS 2024): two-layer transformer on n-gram Markov data; **end-to-end assignment of ICL roles to architectural components** — RPE → copier, FFN → selector (via χ² mutual information), 2nd attention → exponential-kernel classifier. Generalizes the classical induction-head mechanism.
- [Angeliki2024.pdf](paper/Angeliki2024.pdf): explicit transformer constructions emulate **Newton's method** in-context for logistic regression, with quantified depth/width vs ε trade-offs.
- [Heejune2024.pdf](paper/Heejune2024.pdf): separately-parametrized K and Q in softmax attention yield **nuclear-norm implicit regularization** under gradient flow (vs Frobenius when K, Q are merged).

---

### 2.3 LLM 可靠性、特徵學習與優化 / LLM Reliability, Feature Learning & Optimization

**中文**
2025 年之後在 TTIC/UCSD 與 Zhiyuan Li、Sanjiv Kumar、Qiaozhu Mei 等人合作的「產出加速期」。這條線橫跨三個子主題：

1. **自適應優化器的統一理論 / Adaptive optimizers**
   - [Shuoxie2025.pdf](paper/Shuoxie2025.pdf)（ICML 2025）：提出「well-structured preconditioners」概念，一個框架統一 AdaGrad-Norm / diagonal AdaGrad / full AdaGrad / **one-sided Shampoo**，並給出 one-sided Shampoo 比 Gupta 等人的 two-sided 好 √d 的 regret bound。
   - [Shuoxie2026.pdf](paper/Shuoxie2026.pdf)（ICLR 2026）：區分「adaptive smoothness」與「standard smoothness」兩種幾何，解釋 Adam / Shampoo 與 Lion / Muon 為什麼性質不同；給出 Nesterov 加速的 Õ(T⁻²) 率。
   - [Robin2025.pdf](paper/Robin2025.pdf)（NeurIPS OPT workshop 2025）：**重尾類別不平衡**（Zipf 分佈 tokens）是 Adam 勝過 GD 的可證明原因——架構無關。

2. **LLM 可信度與可解釋性 / LLM trustworthiness and interpretability**
   - [Mohamad2025.pdf](paper/Mohamad2025.pdf)：**Reinforced Hesitation (RH)**——把 RLVR 的二元獎勵 {+1, 0} 改成三元 {+1, 0, −λ}，把 abstention 當訓練信號。單一超參數 λ 可調出一條 Pareto 前緣；級聯（cascading）+ 自級聯（self-cascading）把 77.5%→92.5% 正確率。
   - [Siyuchen2026.pdf](paper/Siyuchen2026.pdf)（ICLR 2026）：**Sparse Autoencoders 的可證特徵恢復**——提出 Group Bias Adaptation (GBA) 訓練法，第一個 SAE 特徵可識別性的理論保證，在 Qwen2.5-1.5B 上實證優於 baseline。
   - [Xingjian2026.pdf](paper/Xingjian2026.pdf)（TMLR 2026）：用 rejection sampling 從「只有標籤」的人類評分資料反推 thinking traces，訓練出更可靠的 LLM-as-judge。
   - [Xinhe2026.pdf](paper/Xinhe2026.pdf)：ARC 等「推理 benchmark」其實多半是 **perception bottleneck**——兩階段 pipeline (VLM 做感知 → 純文字 LLM 做推理) 大幅勝過 end-to-end。

3. **神經網路特徵學習理論 / Feature learning theory**
   - [Siyuchen_2_2025.pdf](paper/Siyuchen_2_2025.pdf)（ICLR 2025）：兩層神經網路學 Gaussian single-index model 達到 optimal computational-statistical tradeoff（配合 SQ lower bound），所有 generative exponent s*≥1 都涵蓋——解決了 s*≥3 的長期 open problem。

**English**
A "post-PhD productivity burst" at TTIC/UCSD with Zhiyuan Li, Sanjiv Kumar, and Qiaozhu Mei, spanning three sub-topics:

1. **Unified theory of adaptive optimizers** — Shuoxie2025 / Shuoxie2026 / Robin2025: a "well-structured preconditioner" framework covering AdaGrad variants and Shampoo with improved regret bounds; separation between *adaptive smoothness* and *standard smoothness* geometry; and a provable link from **heavy-tail class imbalance** (Zipf tokens) to Adam's edge over GD — architecture-agnostic.
2. **LLM trustworthiness & interpretability** — Mohamad2025: ternary-reward **Reinforced Hesitation** for abstention; cascading pushes accuracy 77.5 → 92.5 %. Siyuchen2026 (ICLR '26): provable feature recovery in SAEs via **Group Bias Adaptation**. Xingjian2026 (TMLR '26): inferred thinking traces make LLM raters reliable. Xinhe2026: ARC-style benchmarks mostly probe **perception, not reasoning** — a two-stage pipeline wins.
3. **Feature learning theory** — Siyuchen_2_2025 (ICLR '25): two-layer NN provably matches the SQ lower bound for Gaussian single-index models at *all* generative exponents s* ≥ 1 (prior work left s* ≥ 3 open).

---

## 3. 博士論文導讀 / PhD Thesis Reading Guide

**中文**
- **題目 / Title**：*Algorithm Dynamics in Modern Statistical Learning: Asymptotics, Universality, and Implicit Regularization*
- **學校 / University**：Yale University, GSAS, Dept. of Statistics and Data Science（2024 年 5 月頒授）
- **論文檔 / File**：[Tianhao_phd_2024.pdf](paper/Tianhao_phd_2024.pdf)（320+ 頁）
- **指導教授 / Advisor**：Zhou Fan
- **中心論點 / Thesis statement**：現代統計學習的泛化現象無法用「loss landscape 本身」解釋；得分析**演算法走出來的軌跡**才會出現答案。本論文在兩個家族 (AMP、SGD) 分別貫徹這個方法論。
- **章節結構 / Chapter layout**：
  1. Introduction（動機 + 四大貢獻一覽）
  2. Universality of AMP Algorithms（tensor network 證法，一般化到廣義 Wigner 與 generalized invariant ensembles）
  3. AMP for Orthogonally Invariant Ensembles with Spectral Initialization（multivariate iterates + Bayes-OAMP for Bayesian PCA）
  4. Implicit Regularization of SGD（在最小值流形附近的 Katzenberger 型 SDE，label noise 如何帶來 provable generalization benefit）
  5. Implicit Regularization of GD on Reparametrized Models（commuting parametrization ⇔ mirror flow 的等價性，time-warping 推廣）
- **對外的價值 / Why it's worth reading**：第 1 章是**非常清楚的 research statement**——想理解他的品味與世界觀，讀 §1.1–1.2 即可（約 20 頁）；第 5 章把 GD on reparametrized models 與 mirror flow 畫上等號，對 deep learning theory 有興趣的人格外值得看。
- **致謝中列出的「研究導師 / research mentors」**：Zhou Fan（指導）、Quanquan Gu（大學到研究所的 ML 啟蒙）、Zhiyuan Li（implicit regularization 合作）、Sanjeev Arora（Princeton 訪學期間的 deep-learning theory）。這四個名字幾乎預測了他未來的合作網絡。

**English**
- Title: *Algorithm Dynamics in Modern Statistical Learning: Asymptotics, Universality, and Implicit Regularization*, Yale GSAS, May 2024, advisor Zhou Fan; 320+ pages.
- Thesis statement: modern ML generalization cannot be explained from the loss landscape alone — one must analyze the **trajectory the algorithm produces**. The thesis applies this methodology to two algorithm families (AMP and SGD).
- Five chapters: (1) Introduction — clear research statement in §1.1–1.2; (2) AMP universality via tensor networks; (3) matrix-valued AMP with spectral init, plus Bayes-OAMP for Bayesian PCA; (4) SGD Katzenberger limiting SDE near minima; (5) GD on reparametrized models ⇔ mirror flow, generalized by time-warping.
- Acknowledged research mentors — Zhou Fan, Quanquan Gu, Zhiyuan Li, Sanjeev Arora — essentially predict his current collaborator network.

---

## 4. 論文地圖 / Paper Map (18 files, 17 unique works)

> Angeliki2024.pdf 與 Angeliki2025.pdf 為同一論文（arXiv 2403.03183）。/
> Angeliki2024.pdf and Angeliki2025.pdf are the same work (arXiv 2403.03183).

| # | 檔案 / File | 年份 / Year | 場所 / Venue | 主線 / Thread | 題目（簡） / Short title |
|---|---|---|---|---|---|
| 1 | [Tianhao2024](paper/Tianhao2024.pdf) | 2024 | arXiv (math.PR) | AMP | Universality of AMP & Tensor Networks |
| 2 | [Tianhao_phd_2024](paper/Tianhao_phd_2024.pdf) | 2024 | Yale Thesis | All | **PhD Thesis** |
| 3 | [Xinyi2024](paper/Xinyi2024.pdf) | 2024 | *Information & Inference* | AMP | AMP for Orthogonally Invariant Ensembles |
| 4 | [Zhoufan2024](paper/Zhoufan2024.pdf) | 2024 | *Annals of Statistics* | AMP / cryo-EM | MLE for Group Orbit & Cryo-EM |
| 5 | [Max2025](paper/Max2025.pdf) | 2025 | arXiv (math.ST) | AMP | Non-separable AMP Universality (BCP) |
| 6 | [Siyu2024](paper/Siyu2024.pdf) | 2024 | **COLT 2024** | Transformer theory | Multi-Head Softmax Attention ICL Dynamics |
| 7 | [Siyuchen2025](paper/Siyuchen2025.pdf) | 2024 | **NeurIPS 2024** | Transformer theory | Induction Heads on n-gram Markov |
| 8 | [Heejune2024](paper/Heejune2024.pdf) | 2024 | arXiv | Transformer theory | Implicit Reg. of Softmax Attention (K,Q) |
| 9 | [Angeliki2024](paper/Angeliki2024.pdf) / [Angeliki2025](paper/Angeliki2025.pdf) | 2024 | **AISTATS 2025** | Transformer theory | Transformers Emulate Newton's Method |
| 10 | [Siyuchen_2_2025](paper/Siyuchen_2_2025.pdf) | 2025 | **ICLR 2025** | Feature learning | Optimal Comp.-Stat. Tradeoff, Single-Index |
| 11 | [Shuoxie2025](paper/Shuoxie2025.pdf) | 2025 | **ICML 2025** | Optimization | Structured Preconditioners (Shampoo) |
| 12 | [Shuoxie2026](paper/Shuoxie2026.pdf) | 2025→2026 | **ICLR 2026** | Optimization | Two Geometries (Adam vs Lion/Muon) |
| 13 | [Robin2025](paper/Robin2025.pdf) | 2025 | NeurIPS OPT WS 2025 | Optimization | Sign Descent & Heavy-tail Class Imbalance |
| 14 | [Mohamad2025](paper/Mohamad2025.pdf) | 2025 | arXiv (cs.LG) | LLM reliability | Reinforced Hesitation (abstention) |
| 15 | [Siyuchen2026](paper/Siyuchen2026.pdf) | 2025→2026 | **ICLR 2026** | Interpretability | SAE Provable Feature Recovery (GBA) |
| 16 | [Xingjian2026](paper/Xingjian2026.pdf) | 2026 | **TMLR 2026** | LLM reliability | Inferred Thinking Traces for LLM Raters |
| 17 | [Xinhe2026](paper/Xinhe2026.pdf) | 2026 | arXiv | LLM reliability | Perception Bottleneck in ARC Benchmarks |

---

## 5. 精讀 / Deep Reads

### 5.1 Siyu2024 — Multi-Head Softmax Attention ICL Dynamics（COLT 2024）

**動機 / Motivation**
實證上 transformer 能做 in-context learning，但理論文獻幾乎都在「單頭 + 線性 attention + K=Q 合併」的玩具上做；這樣連「多頭到底做了什麼」這種最基本的問題都回答不了。本文第一次在**真正的多頭 softmax attention** 上做梯度流收斂證明。
Empirically transformers do ICL; theoretically, almost all prior work collapsed to single-head, linear, merged K=Q toys — which cannot even articulate *what multiple heads buy*. This paper gives the first gradient-flow convergence theorem for *genuine* multi-head softmax attention.

**設定 / Setup**
單層 H-head 模型，prompt 是 L 組 (xₗ, yₗ)，其中 yₗ = Gᵀxₗ + 噪音；G 在 (Φ, Ψ) 正交基下是分塊對角的，把特徵空間分成 I 個任務。每個 head 有 K、Q、V、O；作者把它們合併成 W⁽ʰ⁾（attention）與 U⁽ʰ⁾（output）來分析。
One-layer H-head model on prompts of L pairs where the regression matrix G is block-diagonal in basis (Φ, Ψ), splitting features into I tasks; per-head matrices are combined into W⁽ʰ⁾ (attention) and U⁽ʰ⁾ (output) for analysis.

**主定理（白話）/ Main theorem**
在對稱、小尺度的「可分解初始化」下，且 H ≥ I：
Under symmetric small-magnitude "decomposable" initialization with H ≥ I:
1. **三階段**：warm-up → emergence（loss 驟降）→ convergence。
   **Three phases**: warm-up → emergence (abrupt loss drop) → convergence.
2. **Task allocation**：收斂時每個任務被**剛好一個 head** 處理，跨 head 的干擾項趨零。沒有損失函數告訴 head 要分工，是**自發**的。
   **Task allocation**: at convergence each task is handled by exactly one head; cross-head interference decays to zero — spontaneously.
3. **H 倍下界**：最好的單頭 softmax attention 在 I 個任務上的 loss ≥ H × 多頭 loss——多頭**可證明地**好 H 倍。
   **Factor-H separation**: the best single-head model's loss is at least H × multi-head loss — provable H-factor advantage.
4. 收斂後的模型在每個任務上，loss 最多比最優單頭模型差一個常數，且在低 SNR 時達到 Bayesian MMSE 下界。
   Per-task, the limit matches the best single-head model up to a constant, and hits the Bayesian MMSE lower bound at low SNR.

**證法關鍵 / Proof trick**
「可分解權重不變集」：若 W 與 U 在 (Φ, Ψ) 基下同時對角且 X / Y 之間正交，GF 會保持此結構——於是矩陣 ODE 壓縮成譜域上的向量 ODE。Softmax 用 moment analysis 處理，指認出最優行為落在「指數區 (attention budget B = o(log L))」，與先前 Huang 等人「正交字典 (orthogonal dictionary)」區間互補。三階段結構來自 μ 與 ω 的 two-timescale：μ 先動、ω 後動，帶分母 2 + φexp(d ω²)/Lω² + Lω²/(φexp(dω²)) 的生長項產生 S 型曲線。
A "decomposable-weights" invariant: if W, U are simultaneously diagonal in (Φ, Ψ) with X/Y orthogonality, GF preserves it, collapsing matrix dynamics to vector ODEs on spectral coordinates. Softmax is handled by moment analysis, identifying the optimal "exponential regime" (attention budget B = o(log L)). The three phases fall out of a two-timescale analysis of μ (fast) vs ω (slow).

**為什麼非顯然 / Why non-obvious**
Task allocation 是 emergent 的；過往把 K、Q 合成 W 或丟掉 softmax 的做法剛好抹掉本題的旋轉對稱，也就抹掉了難度。另一個 subtle point：softmax 自帶的「像 ridge 的隱式正則化」讓 GF-ICL 不會 double descent。
Task allocation is emergent, not imposed. Merging K, Q or dropping softmax destroys exactly the rotational symmetry that makes this problem hard — so prior analyses could not see the phenomenon. A subtler point: softmax provides *ridge-like implicit regularization* that saves GF-ICL from double descent.

**限制 / Limitations**
單層；無 residual、無 MLP；任務同質；H ≥ I；對稱初始化；Linear regression only。擴展到 nonlinear / Markov 在後續 Siyuchen2025 處理。
One layer, no residual, no MLP; homogeneous tasks; H ≥ I; symmetric initialization; linear regression only. Nonlinear / Markov extension in Siyuchen2025.

**在大計畫中的位置 / Bigger picture**
這是 Zhang et al. / Huang et al. / Ahn et al. / Mahankali et al. 那條「transformer 是某種梯度/核 regression/Bayes」家族的第一個**真正的多頭 softmax** 收斂結果，也解釋了多頭到底好在哪裡。與 Wang 的 reliability 議程相輔：理解 capability 何時 emerge，才能預測對齊介入在哪裡有效。
First truly multi-head, full-softmax convergence result in the Zhang / Huang / Ahn / Mahankali "transformer = GD / kernel / Bayes" lineage, and it isolates *what multi-head buys you*. Pairs with Wang's reliability agenda: understanding when capability emerges predicts where alignment interventions will hold.

---

### 5.2 Mohamad2025 — Reinforced Hesitation: Honesty over Accuracy

**動機 / Motivation**
RLVR（DeepSeek-R1、o1 等的訓練範式）給 +1 / 0：答對得 +1，答錯與「不知道」都拿 0。在醫、法、證明這種「錯很貴」的領域，這是災難性的——模型會寧願瞎猜也不棄權。實證上：11 個前沿模型在 GSM8K / MedQA / GPQA 上**即使被明白地告知「錯了 −100、棄權 0」**，棄權率仍不到 1%。結論：棄權必須是**訓練信號**，不能靠 prompt 挽救。
RLVR (the recipe behind DeepSeek-R1 / o1) gives +1 for right, 0 for wrong *or* "don't know" — catastrophic when errors are expensive. Empirically, 11 frontier models on GSM8K / MedQA / GPQA abstain < 1 % of the time *even when prompted with "wrong = −100, abstain = 0"*. Takeaway: abstention must be a *training-time* signal; prompting cannot undo gradient-driven priors.

**RH 公式 / The RH rule**
獎勵從二元 {+1, 0} 改為**三元** {+1, 0, −λ}（外加 −0.5λ 的格式懲罰）。單一超參數 λ 即**一個可解釋的領域旋鈕**：理性代理人在自信度 p < 1/(1+λ) 時應棄權。λ=1 → 自信低於 50% 時棄權；λ=100 → 低於 99% 才答。
Reward goes from binary {+1, 0} to **ternary** {+1, 0, −λ} (plus a −0.5 λ format penalty). The single hyperparameter λ is **an interpretable domain knob**: a rational agent abstains when confidence falls below 1/(1 + λ). λ=1 ⇒ abstain below 50 %; λ=100 ⇒ answer only above 99 %.

**主要結論 / Main claims**
1. **Prompt 無法替代訓練**：無論懲罰多重，prompt-only 幾乎讓所有前沿模型都照答不誤。
   Prompt-only abstention fails universally across frontier models and penalty magnitudes.
2. **Pareto 前緣**：不同 λ 訓出「各司其職」的模型——沒有一個 λ 在所有評估 λ 下最優，最優解沿對角線聚集。λ=0 → 84% 正確 / 15% 錯；λ=1 → 條件正確率 95–99%（棄權 10%）；λ=10 → 錯率 <2%；λ=20 → 全棄權塌陷。
   A Pareto frontier: no single training-λ dominates; optimal-per-column models cluster near the diagonal. λ=0: 84 % right / 15 % wrong; λ=1: 95–99 % conditional accuracy with 10 % abstention; λ=10: errors < 2 %; λ=20: collapse to total abstention.
3. **棄權是協調信號，不是失敗**：Cascading（λ=10 → 5 → 2 → 1 → 0 依序查）用平均 2.2 次查詢達 88.1% 正確率，打敗 majority voting 的 16–64 次。**Self-cascading**（對同一個 λ=1 模型反覆問到不棄權為止）把 77.5% → 92.5%——利用取樣 nondeterminism 當免費探索。
   Abstention is a coordination signal. *Cascading* λ = 10 → 5 → 2 → 1 → 0 hits 88.1 % accuracy with 2.2 queries on average, beating majority voting at 16–64 queries. *Self-cascading* (re-query same λ=1 model until non-abstain) lifts 77.5 → 92.5 %.
4. **Coverage-risk-compute frontier**：適中 λ 讓回答長度從 3000 壓到 1200 tokens——模型學會「要棄權就別再想了」。
   Moderate λ compresses response length 3000 → 1200 tokens — the model learns not to spend tokens on what it will abstain from.

**機制 / Mechanism**
沒有架構改動，**一行 reward 公式的改動**。背後的最佳決策論：在非對稱損失下，回答的期望效用是 p − λ(1 − p)，在 p = λ/(1 + λ) 過零；RH 把這條規則透過 gradient 寫進權重，這是 prompting 做不到的。Cascade 有效的經驗規律：**conditional accuracy given non-abstention 隨 λ 單調上升**（84 → 95 → 97 → 99 %），所以降序查詢永遠不劣於提前停止。
No architectural change — one line of the reward. The Bayes-optimal decision rule under asymmetric loss crosses zero at p = λ/(1 + λ); RH gradient-encodes that threshold into weights, which prompting cannot. Cascading works because *conditional* accuracy given non-abstention is monotonic in λ (84 → 95 → 97 → 99 %), so descending-λ queries never worsen outcomes.

**為什麼驚人 / Why striking**
（a）11 個前沿系統（含 Gemini 2.5 Pro、DeepSeek-R1）對 −100 懲罰的指令視若無睹——RL post-training 把「必須回答」的先驗焊進權重，instructions 蓋不過。（b）Pareto 前緣是真正的互不支配：人會以為「高 λ 模型只要多棄權就等於低 λ 模型的超集」，但不同 λ 學到**質上不同的分流策略**，cascading 因此對 voting 是 Pareto-dominant。
(a) 11 frontier systems (including Gemini 2.5 Pro, DeepSeek-R1) ignore an explicit −100 instructed penalty — RL post-training bakes a "must answer" prior into weights that instructions cannot override. (b) The Pareto frontier is genuine non-domination: different λ-models learn qualitatively different triage strategies, making cascading Pareto-dominant over majority voting.

**限制 / Limitations**
單一模型規模（Qwen3-1.7B）；單一領域（邏輯謎題，ground truth 乾淨）；只有「答 / 棄權」二選一，未處理連續信心；λ 要人挑。沒有理論保證——純實證。
Single model scale (Qwen3-1.7B); one domain (logic puzzles with clean ground truth); binary abstain/answer (no continuous confidence); λ selection manual. No theoretical guarantees — empirical.

**在大計畫中的位置 / Bigger picture**
對應 Chow (1970) / Geifman & El-Yaniv (2017) 的 selective prediction 譜系，移植到 RLVR 時代，並直接反駁 "RLVR 增加 hallucination" 的新近結論。在 Wang 的議程裡，這是 Siyu2024 的**對齊書擋**：前者證明訓練動力學能造出乾淨結構（task allocation），後者證明用錯獎勵也會造出**有結構的過度自信**——**單一 reward scalar 就能改寫模型的風險畫像**。兩篇一起展示他的哲學：把訓練本身當研究對象，小結構選擇有大下游後果。
Extends the selective-prediction lineage (Chow 1970; Geifman & El-Yaniv 2017) into the RLVR era and challenges recent claims that RLVR increases hallucination. Within Wang's agenda this is the *alignment bookend* to Siyu2024: the former shows training dynamics can produce clean structure (task allocation), the latter shows the wrong reward *also* reliably produces structured over-confidence — and a **single reward scalar rewrites the model's risk profile**. Together they articulate his philosophy: treat training as the object of study; small structural choices have outsized downstream consequences.

---

## 6. 合作網絡 / Collaboration Network

| 合作者 / Collaborator | 機構 / Affiliation | 共同論文 / Joint papers | 主題 / Topic |
|---|---|---|---|
| **Zhou Fan** (thesis advisor) | Yale Statistics | Tianhao2024, Xinyi2024, Zhoufan2024 | AMP universality, cryo-EM |
| **Zhiyuan Li** | TTIC | Shuoxie2025/2026, Robin2025, Mohamad2025 | Adaptive optimization, LLM RL |
| **Zhuoran Yang** | Yale Statistics | Siyu2024, Siyuchen2025, Siyuchen2026, Siyuchen_2_2025 | Transformer theory |
| **Jason D. Lee** | Princeton | Angeliki2024 | In-context Newton |
| **Harrison H. Zhou** | Yale Statistics | Heejune2024 | Attention implicit reg. |
| **Siyu Chen (student)** | Yale | Siyu2024, Siyuchen2025/2026, Siyuchen_2_2025 | 核心學生合作者 / core student collaborator |
| **Heejune Sheen (student)** | Yale | Siyu2024, Siyuchen2025, Siyuchen2026, Heejune2024 | 同上 / same |
| **Shuo Xie (student)** | TTIC | Shuoxie2025/2026, Robin2025 | Optimization |
| **Qiaozhu Mei** | U. Michigan | Xingjian2026, Xinhe2026 | LLM evaluation |
| **Sanjiv Kumar** | Google Research | Shuoxie2025 | Adaptive optimization |
| **Roy R. Lederman / Yi Sun / Sheng Xu** | Yale / U. Chicago | Zhoufan2024 | Cryo-EM |

---

## 7. 研究風格關鍵字 / Style Tags

- **Theory-heavy, proof-first**：所有論文都有定理陳述；即使是 empirical 導向的 Mohamad2025 也建立在 Bayes-optimal decision 的分析上。
  Theory-first: every paper states a theorem; even empirical work (Mohamad2025) rests on a Bayes-optimal decision analysis.
- **演算法軌跡派 / Algorithm-dynamics school**：不分析最終解，分析「到達路徑」。
  Cares about the trajectory to the solution, not the solution itself.
- **高維工具箱 / High-dimensional toolbox**：random matrix theory、free probability、moment method、tensor network、梯度流 ODE、two-timescale 分析。
  RMT, free probability, moments, tensor networks, gradient-flow ODEs, two-timescale analysis.
- **合作者結構穩定 / Stable collaborator structure**：與 Zhou Fan、Zhiyuan Li、Zhuoran Yang 形成三個穩固「三角」，分別對應 AMP、優化、transformer 理論。
  Three stable "triangles" — with Fan / Li / Yang — map onto AMP / optimization / transformer theory.
- **寫作習慣 / Writing habits**：定理陳述簡潔有力；Introduction 做得長而細，常用「our result / compared with prior work」明確定位。
  Clean theorem statements; long, careful introductions with explicit "our result / compared with prior work" positioning.

---

## 8. 若要與他產生對話 / How to Engage

**中文**
- **如果你做理論/ML 基礎**：讀他博論 Ch. 1（研究宣言）+ Siyu2024 + Shuoxie2026。能跟他討論 "what new algorithm dynamics" 會是最直接的切入點。
- **如果你做 LLM 應用 / 可靠性**：Mohamad2025 + Xingjian2026 + Xinhe2026 是最新也最開放的方向。他明顯在把 selective prediction、perception bottleneck、trace reconstruction 當作新 research program 起手——適合帶具體的應用痛點（醫療、教育、評分）來找交集。
- **如果你做 interpretability / SAE**：Siyuchen2026 (GBA) 是他目前**唯一**的純可解釋性工作；可視為他整體「特徵學習理論」進入 mechanistic interpretability 的橋梁。
- **如果你打算申請他**：他剛開 lab（2025 秋），學生名額與題目都在最開放的時期；從 Siyu Chen / Heejune Sheen 的論文可看出他帶 PhD 的風格——問題漂亮、證明紮實、審稿刊在 COLT/NeurIPS/ICLR。三件事準備好：(1) 有紮實的機率/統計基礎，(2) 對某個演算法動力學有自己的 take，(3) 讀過他博論的 Ch. 1。

**English**
- **Theory / ML foundations audience**: read thesis Ch. 1 + Siyu2024 + Shuoxie2026; conversations about "new algorithm dynamics" will land best.
- **LLM applications / reliability audience**: Mohamad2025 + Xingjian2026 + Xinhe2026 are the newest, most open directions. He is visibly opening a program around selective prediction / perception bottleneck / trace reconstruction — bring a concrete application pain point (medicine, education, grading) and look for overlap.
- **Interpretability / SAE audience**: Siyuchen2026 (GBA) is his *only* pure-interpretability paper so far; it is the bridge between his feature-learning theory and mechanistic interpretability.
- **Prospective students**: He just opened a lab (Fall 2025) — student slots and topics are at their most open. Style from his mentees (Siyu Chen, Heejune Sheen): clean problems, rigorous proofs, COLT / NeurIPS / ICLR placements. Prepare: (1) strong probability/statistics, (2) your own take on some algorithm's dynamics, (3) read thesis Ch. 1.

---

## 9. 可能的空白與未來方向 / Open Gaps & Likely Futures

**中文**
- **LLM 可靠性還缺 "scaling"**：Mohamad2025 只在 1.7B 上做；他未來幾篇很可能會 scale 並結合 adaptive λ 或 learned confidence。
- **Transformer theory 走向多層 / MLP**：Siyu2024 → Siyuchen2025 已從 1 層走到 2 層；下一步合理預期是「多層 + residual + 真實 tokenizer」。
- **AMP 與 diffusion / flow matching 的連結**：Max2025 的 BCP 特別提到 deep generative priors，這條路線有機會跨到現代生成模型。
- **Interpretability × dynamics**：GBA (Siyuchen2026) + induction heads (Siyuchen2025) 暗示一個更大的融合題目——「在訓練動力學層面理解並控制 LLM 特徵」。這是他最有可能立旗的方向。

**English**
- LLM reliability lacks *scaling* — Mohamad2025 is only at 1.7B; expect scaled follow-ups with adaptive λ or learned confidence.
- Transformer theory going multi-layer / MLP — Siyu2024 → Siyuchen2025 already pushed 1 → 2 layers; next natural step is multi-layer + residual + real tokenizer.
- AMP ↔ diffusion / flow matching — Max2025's BCP explicitly mentions deep generative priors; a bridge to modern generative models is in reach.
- Interpretability × dynamics — GBA (Siyuchen2026) + induction heads (Siyuchen2025) hint at a larger agenda: understand and control LLM features at the level of *training dynamics*. The most likely flag he will plant.

---

*Compiled 2026-04-15. 如需某一篇論文更深度的精讀、或延伸到特定主題（例如「AMP 普適性細節」、「SAE 特徵恢復證明」），再告訴我就好。*
*If you want a deeper dive on any single paper or a drill-down on a specific sub-topic (e.g. "AMP universality proof in detail", "SAE feature-recovery theorem"), say the word.*
