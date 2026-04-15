# Preprocess File Formats

Exact templates and worked examples for the 5 files produced in Phase 1a. Every file is markdown with a leading `# Title`, a short purpose note, and a table. Downstream skills (journal-draft, journal-review, journal-finalize) parse these tables — keep the column order and column names stable.

---

## 1. `figure_captions.md`

**Purpose.** Canonical record of every figure: its caption, the numbers visible in the figure, trend direction, and what the figure demonstrates. Step 3 (review) cross-checks every "as shown in Fig. X" claim against this file. If a number isn't here, Step 2 cannot cite it.

**Source.** `step5_figure_catalog.md` (Algorithm Agent) + actual figure files (caption text in `8_Manuscript/figures/*.png` metadata or adjacent `.md`). Every figure in the catalog must have exactly one row here.

**Format.**

```markdown
# Figure Captions — Preprocessed

Each row is the ground truth for the corresponding figure. All claims in the draft that reference Fig. N must match the values here. Numbers shown are taken from the analysis summary or the figure's embedded annotations — do not round or re-derive.

| Fig N | Caption summary | Key numbers | Trend | Demonstrates |
|-------|-----------------|-------------|-------|--------------|
| Fig 1 | System architecture: EEG branch + gaze branch fused via fuzzy gating layer. | — | — | Model overview |
| Fig 2 | Per-subject decoding accuracy across 3 sessions. | Mean acc: S1=0.74, S2=0.71, S3=0.68 (std ≈ 0.05) | Slight decrease across sessions | Session drift exists |
| Fig 3 | Ablation of gating module: full vs no-gate vs fixed-weight. | F1: full=0.82, no-gate=0.74, fixed=0.77 | Full > fixed > no-gate | Gating gives +0.08 F1 |
| Fig 4 | Attention weight vs. cognitive load (panels a–c). | Peak at moderate load (~0.6), plateau after | Inverted-U, NOT monotonic | Load-dependent gating |
```

**Notes.**

- **Trend column is critical.** It is the single most common source of visual-text mismatches (text says "increasing", figure shows "plateau"). Be precise: `monotonic increase`, `inverted-U`, `saturates at X`, `no significant change`, etc.
- If a figure has multiple panels with different trends, list them: `(a) increase, (b) plateau, (c) decrease`.
- `Key numbers` may be `—` if the figure is a schematic, but then `Demonstrates` must be explicit (e.g., "architecture overview, no quantitative content").

---

## 2. `table_captions.md`

**Purpose.** Canonical record of every table: caption, columns, best/worst values, significance markers.

**Source.** `step5_figure_catalog.md` + `step4_analysis_summary.md`.

**Format.**

```markdown
# Table Captions — Preprocessed

| Table N | Caption summary | Columns | Best result | Worst result | Statistical significance |
|---------|-----------------|---------|-------------|--------------|--------------------------|
| Table 1 | Main comparison: our method vs 4 baselines on 3 datasets (F1 ± std, N=45). | Method, Dataset A F1, Dataset B F1, Dataset C F1 | Ours: 0.87/0.84/0.81 | SVM: 0.62/0.59/0.55 | Ours vs SVM: p<0.001 on all; Ours vs Deep-baseline: p=0.03 on A, p=0.08 on B (n.s.), p=0.12 on C (n.s.) |
| Table 2 | Per-component ablation. | Component removed, F1 drop | Drop 0.14 when gating removed | Drop 0.01 when dropout removed | All drops p<0.05 except dropout (p=0.41, n.s.) |
```

**Notes.**

- **Significance column is critical**. Step 3 catches claims like "significant improvement over baseline X" when the table shows n.s. Be explicit.
- "Best/worst" refers to the numerically extreme values; it doesn't imply significance.
- If a table is huge (20+ rows), summarize ranges and call out the specific rows Methods/Results/Discussion will cite — don't transcribe everything.

---

## 3. `pseudocode.md`

**Purpose.** Core algorithms in LaTeX Algorithm-environment-friendly style so Step 2 (Methods) can drop them in. Numbered for cross-reference.

**Source.** `step1_architecture_spec.md`. Convert prose / code to clean pseudocode.

**Format.**

```markdown
# Pseudocode — Core Algorithms

## Algorithm 1 — Fuzzy-Gated Bimodal Fusion

**Inputs.** EEG feature vector $x_e \in \mathbb{R}^{d_e}$, gaze feature vector $x_g \in \mathbb{R}^{d_g}$, gating network parameters $\theta_g$.

**Output.** Fused representation $z \in \mathbb{R}^{d_z}$.

```
1:  α ← σ(W_g · [x_e; x_g] + b_g)            // gating weight, fuzzy in [0,1]
2:  z_e ← W_e · x_e                            // EEG projection
3:  z_g ← W_g · x_g                            // gaze projection
4:  z ← α · z_e + (1 - α) · z_g                // convex combination
5:  return z
```

**Cross-ref.** Used in Methods §3.3 (model definition), Results §4.2 (ablation on gating), Discussion §5.1 (interpretation of α distribution).

---

## Algorithm 2 — ... (repeat structure)
```

**Notes.**

- Keep each algorithm self-contained: inputs, outputs, body, cross-ref. Step 2 pastes these into Methods with minimal editing.
- Use LaTeX-style math inside the prose lines (`$...$`) and plain text inside the numbered block — Step 2 converts the block to an `algorithm` environment.
- If the architecture has >3 core algorithms, split into distinct numbered blocks; don't merge.

---

## 4. `notation_glossary.md`

**Purpose.** Every math symbol with canonical meaning, first-appearance subsection, and dimensions. Step 3 checks that every symbol in the draft matches a row here; Step 5 checks consistent use throughout.

**Source.** Scan `step1_architecture_spec.md`, `pseudocode.md`, and any equations in upstream materials. Collect every distinct symbol.

**Format.**

```markdown
# Notation Glossary

Canonical symbol definitions. Every symbol used in the draft must appear here exactly once, with one meaning. Symbols with conflicting uses in the source materials are flagged with ⚠️ CONFLICT — the blueprint must pick one meaning and rename the other.

| Symbol | Meaning | First appears in | Dimensions |
|--------|---------|------------------|------------|
| $x_e$ | EEG feature vector (per-window) | Methods §3.2 | $\mathbb{R}^{d_e}$, $d_e=128$ |
| $x_g$ | Gaze feature vector (per-window) | Methods §3.2 | $\mathbb{R}^{d_g}$, $d_g=12$ |
| $\alpha$ | Fuzzy gating weight | Methods §3.3 | scalar $\in [0,1]$ |
| $\theta$ | Model parameters (all learnable) | Methods §3.4 | — |
| ⚠️ $\sigma$ | CONFLICT: (a) sigmoid activation (Methods §3.3), (b) standard deviation (Results §4.1). **Resolution**: keep $\sigma(\cdot)$ for sigmoid; use $s$ for std in Results. | — | — |
```

**Notes.**

- The glossary is the **source of truth**. If the source uses `\sigma` for two things, decide here which wins and which gets renamed, and Step 2 will enforce the rename.
- Include `Greek`, `Latin`, subscripted, and superscripted variants as separate rows — `x_e`, `x_g`, and `\hat{x}` are three distinct entries.
- Dimensions help Step 3 catch type errors (e.g., "we compute $\alpha \cdot x_e$" when $\alpha$ is a vector but text treats it as scalar).

---

## 5. `equation_plan.md`

**Purpose.** Pre-assign equation numbers, place them in subsections, plan which later sections reference which equations. Step 2 uses this to produce correct `\label{eq:N}` / `\eqref{eq:N}` pairs.

**Source.** `step1_architecture_spec.md` + the subsection outline in the blueprint. If the subsection outline doesn't exist yet, do a first-pass plan here and refine after Phase 1b §5.

**Format.**

```markdown
# Equation Plan

| Eq # | Equation (short form) | Subsection where defined | Cross-refs (sections that cite it) |
|------|----------------------|--------------------------|-----------------------------------|
| 1 | $z = \alpha z_e + (1-\alpha) z_g$ | Methods §3.3 | Results §4.2 (ablation), Discussion §5.1 (interpretation) |
| 2 | $\alpha = \sigma(W_g [x_e; x_g] + b_g)$ | Methods §3.3 | Results §4.3 (weight distribution) |
| 3 | $\mathcal{L} = \text{CE}(f(z), y) + \lambda \|\theta\|_2^2$ | Methods §3.4 | Methods §3.5 (training details) |
```

**Notes.**

- Equations that appear only once (defined and never cross-referenced) are fine — leave the Cross-refs cell as `—`.
- If Methods structure is still fluid, assign tentative numbers (`1a`, `1b`) and fix at Phase 1b §5 subsection outlining.
- Long derivation equations (3+ intermediate steps) should either be collapsed to one numbered `(N)` with the derivation in an appendix, or explicitly chained (`(4a)→(4b)→(4c)`) — decide here so Step 2 doesn't improvise.

---

## Quality checks (all 5 files)

Before moving to Phase 1b, verify:

- [ ] Every figure in `step5_figure_catalog.md` has exactly one row in `figure_captions.md`
- [ ] Every table in the catalog has exactly one row in `table_captions.md`
- [ ] Every algorithm in `step1_architecture_spec.md` has a pseudocode block
- [ ] Every symbol used in the architecture has a glossary row; no orphan symbols in pseudocode
- [ ] Every equation in the architecture has an equation-plan row with a subsection assignment
- [ ] No `CONFLICT` flag is left unresolved (each must have a resolution plan)

Failures here compound into Step 2 drafting errors. Resolve now, not later.
