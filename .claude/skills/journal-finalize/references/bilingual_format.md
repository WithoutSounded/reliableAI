# Bilingual Markdown Format — Obsidian Review Bundle

The `step6_final/bilingual/` output is read by the author in Obsidian with MathJax and callouts enabled. Every section file follows the same structure so the author can predict where the Revision Zones are and leave edits there.

## Per-section file structure

```markdown
## <section title>

### <subsection title>

> [!quote] EN
> <English paragraph(s), converted from LaTeX>
> 
> <Another EN paragraph if the subsection has multiple>

> [!quote] 繁中
> <繁體中文 translation>

> [!edit] ✏️ Revision Zone
> <!-- 修改意見或直接修改英文段落 -->

---

### <next subsection title>
...
```

Rules:

1. **One subsection = one callout triple** (EN / 繁中 / Revision Zone). If the source `.tex` has no `\subsection`, the whole body becomes a single, untitled subsection.
2. **Callout type matters.** `> [!quote] EN` and `> [!quote] 繁中` render the content in a quote-style box; `> [!edit] ✏️ Revision Zone` renders with the edit icon Obsidian reserves for the edit callout. Using `> [!note]` or `> [!info]` would still render, but the author's CSS is keyed to `quote`/`edit`.
3. **Separators.** Use `---` (triple dash) between subsections. Obsidian renders this as a horizontal rule and it helps the author scroll by section.
4. **Every line inside a callout starts with `>`.** An empty line inside a callout is `>` alone (no space). A blank line without `>` closes the callout — don't accidentally split a paragraph that way.

## LaTeX → Markdown conversion (EN side)

Performed by `build_bilingual_scaffold.py`. The mappings are deliberately conservative — we convert only what renders better in Markdown, and preserve math verbatim so Obsidian's MathJax handles it.

| LaTeX | Markdown |
|---|---|
| `\cite{Key}` | `[Key]` |
| `\cite{K1,K2}` | `[K1, K2]` |
| `\ref{fig:X}` | `Fig. X` |
| `\ref{tab:X}` | `Table X` |
| `\ref{eq:X}` or `\eqref{eq:X}` | `Eq. (X)` |
| `\textbf{...}` | `**...**` |
| `\emph{...}`, `\textit{...}` | `*...*` |
| `\underline{...}` | `__...__` |
| `$...$` | `$...$` (unchanged) |
| `\begin{equation}...\end{equation}` | kept verbatim |
| `\label{...}` | dropped (no Markdown equivalent) |
| Unknown `\foo{text}` | `text` (argument kept) |
| Unknown `\foo` | dropped |

## 繁中 translation rules

The script leaves `> [!quote] 繁中` empty with a placeholder comment; the LLM fills it. Follow these principles:

### Style

Professional academic Traditional Chinese (繁體中文). The target reader is a Taiwanese / Hong Kong researcher who also reads the English version — they should feel the Chinese is *publication-quality*, not a rough gloss.

**Yes:**
- 本研究提出一個基於注意力機制的雙流融合架構，結合腦電訊號與注視熱圖以辨識配對社交互動。
- 實驗結果顯示，在 N=45 名受試者的資料集上，本方法的分類準確率達到 0.87。

**No:**
- 這個研究介紹了一個基於注意力的雙流融合的結構（machine-translation feel，多重「的」）
- 我們的方法比基線好 15% （太口語）
- 被提出的架構實現了... （被字句濫用）

### Do

- 使用台灣學界常用術語（e.g. `注意力機制`, `交叉驗證`, `消融實驗`）。
- Preserve math verbatim inside `$...$`. Chinese punctuation outside math; Western punctuation inside.
- Keep citation brackets verbatim: `[Smith2024]` stays `[Smith2024]` — don't translate author names.
- Preserve figure/table references as-is (`Fig. 1`, `Table 2`) — these are cross-references, not prose.
- Compact 2–3 English sentences into 1–2 Chinese sentences when it reads better, as long as no claim is lost.
- Translate field-specific terms consistently — if `attention weight` was translated as `注意力權重` in one subsection, use the same term throughout.

### Don't

- Don't invent precision the English didn't commit to (`high accuracy` → `高準確率`, not `85% 的準確率`).
- Don't translate code identifiers, model names, or library names (`PyTorch` stays `PyTorch`, `ViT` stays `ViT`).
- Don't add Chinese text to the English callout or vice versa — keep the two callouts clean.
- Don't translate `\cite{}` keys — they're citation identifiers, not prose.

## Common-term glossary

Preferred Traditional Chinese terms for recurring concepts in this project's domain. If `step2_global_config.json → glossary` has a Chinese entry for a term, use that instead — the blueprint/polish steps may have established project-specific conventions.

| English | 繁中 |
|---|---|
| attention mechanism | 注意力機制 |
| attention weight | 注意力權重 |
| cross-attention | 交叉注意力 |
| transformer | Transformer（保留英文） |
| encoder / decoder | 編碼器 / 解碼器 |
| embedding | 嵌入 (or 嵌入向量 for vector) |
| feature map | 特徵圖 |
| fusion | 融合 |
| early fusion / late fusion | 早期融合 / 晚期融合 |
| multi-modal | 多模態 |
| dyadic | 二元（互動） |
| EEG | 腦電（訊號）/ EEG |
| gaze heatmap | 注視熱圖 |
| ablation study | 消融實驗 |
| cross-validation | 交叉驗證 |
| confusion matrix | 混淆矩陣 |
| loss function | 損失函數 |
| gradient descent | 梯度下降 |
| hyperparameter | 超參數 |
| spectrogram | 頻譜圖 |
| inter-brain synchrony (IBS) | 腦際同步性 (IBS) |
| fuzzy gating | 模糊閘控 |
| benchmark | 基準（測試） |
| baseline | 基線 |
| state-of-the-art (SOTA) | 最先進 / SOTA |
| classification accuracy | 分類準確率 |
| F1 score | F1 分數 |
| precision / recall | 精確率 / 召回率 |
| AUC / AUROC | AUC / ROC 曲線下面積 |
| statistical significance | 統計顯著性 |
| p-value | p 值 |
| standard deviation | 標準差 |
| subject / participant | 受試者 |
| sampling rate | 取樣率 |
| bandpass filter | 帶通濾波器 |
| feature extraction | 特徵擷取 |

When in doubt, prefer the term used by published Chinese-language papers in the same domain. If no consensus term exists, keep the English term and add the Chinese gloss in parentheses the first time: `模糊閘控融合 (fuzzy gating fusion)`.

## Revision Zone conventions

The human fills these. The scaffold leaves:

```markdown
> [!edit] ✏️ Revision Zone
> <!-- 修改意見或直接修改英文段落 -->
```

What the human writes in it:

- **Plain comment**: "英文第二句太強，改成 may rather than demonstrates"
- **Direct English replacement**: a replacement paragraph the author wants propagated back to the `.tex`
- **Chinese-only feedback**: a note on translation quality

When the author later asks to "propagate the Revision Zone edits back to Overleaf", the expected workflow (out of scope for this skill but useful to know): read the Revision Zones, map each to the subsection, update the corresponding `.tex` in `step6_final/latex/`, rerun `hard_constraints.py` to make sure the edits didn't break anything.

## Verification

After the LLM fills the 繁中 callouts, `build_bilingual_scaffold.py --verify` checks:

- Same number of EN / 繁中 / Revision Zone callouts per file
- Every `\cite` key from the `.tex` appears somewhere in the `.md`
- Inline-math count is not lower than the `.tex` count

If any check fails, the scaffold structure was broken during translation — usually because the LLM accidentally removed a `>` prefix or merged two subsections. Rerun the scaffold build and re-translate, or patch the `.md` file directly.
