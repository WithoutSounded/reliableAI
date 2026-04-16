---
citation_key: "DuanEtAl2023"
title: "Shifting Attention to Relevance: Towards the Predictive Uncertainty Quantification of Free-Form Large Language Models"
authors: "Jinhao Duan; Hao Cheng; Shiqi Wang; Alex Zavalny; Chenan Wang; Renjing Xu; Bhavya Kailkhura; Kaidi Xu"
year: 2023
doi: "10.48550/arxiv.2307.01379"
source: "local PDF (Jinhao2024.pdf)"
access_level: "full-text-pdf"
retrieved_date: "2026-04-15"
arxiv_id: "2307.01379"
is_user_seed: true
tier: 1
composite_score: 4.7
---
# Shifting Attention to Relevance: Towards the Predictive Uncertainty Quantification of Free-Form Large Language Models
**Authors**: Jinhao Duan, Hao Cheng, Shiqi Wang, Alex Zavalny, Chenan Wang, Renjing Xu, Bhavya Kailkhura, Kaidi Xu
**Year**: 2023
**Venue**: arXiv (Cornell University)
**DOI**: [10.48550/arxiv.2307.01379](https://doi.org/10.48550/arxiv.2307.01379)

## Full Text (extracted via pdftotext) / 全文（pdftotext 抽取）

```text
                                                 Shifting Attention to Relevance: Towards the Predictive Uncertainty
                                                         Quantification of Free-Form Large Language Models
                                                 Jinhao Duan1          Hao Cheng3  Shiqi Wang2   Alex Zavalny1    Chenan Wang1
                                                                      Renjing Xu3 Bhavya Kailkhura4   Kaidi Xu1 *
                                                                               Drexel University 2 AWS AI Lab
                                                                  Hong Kong University of Science and Technology (Guangzhou)
                                                                            Lawrence Livermore National Laboratory

                                                                    Abstract                             Question: What is the ratio of the mass of an object to its volume?
                                                                                                         Ground Truth: density

                                                 Large Language Models (LLMs) show promis-                             . . . LLMs Generation: density of an object          Correctness

arXiv:2307.01379v3 [cs.CL] 28 May 2024
                                                 ing results in language generation and instruc-
                                                 tion following but frequently “hallucinate”,            Predictive Entropy-based Uncertainty Quantification

                                                 making their outputs less reliable. Despite Un-
                                                                                                                        density         of          an         object
                                                 certainty Quantification’s (UQ) potential solu-          Token
                                                                                                         Entropy        ( 0.238    +   6.528   +   0.966   +    0.008 ) / 4
                                                 tions, implementing it accurately within LLMs
                                                                                                         Uncertainty     = 1.949       High uncertainty, refuse to answer
                                                 is challenging. Our research introduces a sim-
                                                 ple heuristic: not all tokens in auto-regressive
                                                 LLM text equally represent the underlying               Shifting Attention to Relevance Uncertainty Quantification

                                                 meaning, as “linguistic redundancy” often al-
                                                                                                                        density         of          an         object
                                                 lows a few keywords to convey the essence
                                                                                                                         0.238         6.528       0.966        0.008
                                                 of long sentences. However, current methods             Token-Level
                                                                                                                                   +           +           +
                                                                                                           Shifting
                                                                                                                         0.757         0.057       0.097        0.088
                                                 underestimate this inequality when assessing
                                                 uncertainty, causing tokens with limited se-            Uncertainty     = 0.650       Low uncertainty, return generation

                                                 mantics to be equally or excessively weighted
                                                 in UQ. To correct this, we propose Shifting          Figure 1: Irrelevant tokens (or sentences) may commit
                                                 Attention to more Relevant (SAR) components          majority uncertainty in free-form generations, such as
                                                 at both token- and sentence-levels for better        the token “of” committing extremely large uncertainty
                                                 UQ. We conduct extensive experiments involv-         misleads the uncertainty quantification of LLMs. We
                                                 ing a range of popular “off-the-shelf” LLMs,         term these observations as generative inequalities and
                                                 such as Vicuna, WizardLM, and LLaMA-2-               tackle them by shifting attention to more relevant com-
                                                 chat, with model sizes extending up to 33B           ponents.
                                                 parameters. We evaluate various free-form
                                                 question-answering tasks, encompassing do-           2022), profoundly shape the range of what AIs
                                                 mains such as reading comprehension, science         could do, and how they communicate with humans.
                                                 Q&A, and medical Q&A. Our experimental                  Despite the surprising progress, LLMs are
                                                 results, coupled with a comprehensive demo-          proven to be vulnerable to widely known relia-
                                                 graphic analysis, demonstrate the superior per-
                                                                                                      bility issues (Yao et al., 2024; Sun et al., 2024;
                                                 formance of SAR. The code is available at
                                                 https://github.com/jinhaoduan/SAR.                   Hong et al., 2024), such as hallucination (Manakul
                                                                                                      et al., 2023a) and factual errors (Bian et al., 2023;
                                         1       Introduction                                         Karpinska and Iyyer, 2023; Gekhman et al., 2023).
                                                                                                      Uncertainty quantification (UQ) is one of the most
                                         Large Language Models (LLMs) have shown re-                  popular approaches to answering when humans
                                         markable capabilities in multi-round conversa-               can trust the generations of LLMs, which is critical
                                         tion (Long, 2023; Chen et al., 2023), logical reason-        for Human-AI interaction applications (e.g., ther-
                                         ing (Creswell et al., 2022; Pan et al., 2023; Duan           apy and mental health (Lin et al., 2023; Sharma
                                         et al., 2024), and also disclose great potential in          et al., 2023)) where humans need to densely com-
                                         scientific discovery (Birhane et al., 2023). For in-         municate with LLMs. In these applications, the
                                         stance, ChatGPT, BARD, GPT-4, pre-trained on                 resulting behaviors will be largely affected by the
                                         large-scale corpora and carefully aligned to human           generations from LLMs.
                                         preferences (Christiano et al., 2017; Ouyang et al.,            Unfortunately, UQ remains challenging due to
                                             *    Corresponding author: Kaidi Xu <kx46@drexel.edu>.   various uncertainty sources (e.g., aleatoric uncer-
tainty and epistemic uncertainty (Kendall and Gal,         Based on these observations, we propose a sim-
2017)). This challenge is particularly pronounced       ple attention-shifting method, by jointly examin-
in the context of free-form LLMs, which are char-       ing the relevance of each component and reassign-
acterized by high complexity and an essentially         ing its attention, from both the token level and
limitless solution space—any output matching the        the sentence level, termed as Shifting Attention
semantic content of the true answer is considered       to Relevance (SAR). SAR is evaluated on mul-
correct. This makes UQ in LLMs markedly distinct        tiple popular instruction-tuned LLMs (e.g., Vi-
from more traditional classification models or mod-     cuna (Zheng et al., 2023), LLaMA-2-chat (Tou-
els with defined labels, where the solution space is    vron et al., 2023b), WizardLM (Xu et al., 2023)),
constrained.                                            with model size up to 33B, and popular pre-
   Prior works in this direction estimate uncertainty   trained LLMs (e.g., OPT (Zhang et al., 2022),
by prompting LLMs to answer confidence (Lin             LLaMA (Touvron et al., 2023a)) with model sizes
et al., 2022a; Kadavath et al., 2022a) or design-       up to 30b, over cross-domain free-form question-
ing logits- or entropy-based measurements (Ma-          answering tasks, such as the conventional NLP
linin and Gales, 2021, 2020; Kuhn et al., 2023).        domain (e.g., CoQA (Reddy et al., 2019), Trivi-
The most recent work proposes Semantic Entropy          aQA (Joshi et al., 2017) and SciQ (Welbl et al.,
(SE) (Kuhn et al., 2023) where generations sharing      2017)) and medical domain (e.g., MedQA (Jin
the same meaning are gathered in a semantic clus-       et al., 2020), MedMCQA (Pal et al., 2022)). Exper-
ter. Then the cluster-wise entropy is calculated as     imental results demonstrate SAR’s superior perfor-
the uncertainty measurement.                            mance. Our contributions can be summarized as
   Our motivation is derived from an intuitive fact:    the following:
tokens are created unequally in presenting seman-           • We disclose that uncertainty quantification is
tics. Namely, some tokens (e.g., nouns, verbs) are            significantly affected by token- and sentence-
more meaningful than other tokens (e.g., definite             level generative inequality, i.e., irrelevant to-
articles). For example, for a given question “What            kens or sentences might be over-valued when
is the ratio of the mass of an object to its volume?”         estimating uncertainty.
and a model generation “density of an object”,
“density” is the most relevant token in presenting          • We mitigate the two inequality biases by
semantics than the rest tokens. We term the former            Shifting Attention to Relevance (SAR), which
as relevant tokens and the rest tokens as irrelevant          jointly examines the relevance of each token
tokens. Prior works treat each token equally when             and sentence, and reassigns attention when
estimating uncertainty, which is counter-intuitive            estimating uncertainty.
( Figure 1). Therefore, we ask:                             • We conduct experiments over “off-the-shelf”
   Are relevant tokens more critical than irrelevant          instruction-tuned LLMs and popular pre-
tokens in uncertainty quantification?                         trained LLMs, across various free-form
   To answer this question, we first investigate              question-answering tasks. Experimental re-
how token-level generative inequality affects un-             sults demonstrate that SAR outperforms previ-
certainty quantification in LLMs. Specifically, we            ous state-of-the-art by a large margin.
first measure the relevance score of each token by
                                                        2    Related Works
comparing the semantic change before and after
removing this token from the sentence. A larger         Uncertainty Quantification in Conventional
semantic change means more relevance for this           NLP Tasks. Uncertainty Quantification of ma-
token and vice versa. Then we quantify the uncer-       chine translation (MT) has been studied for years
tainty proportions, i.e., the uncertainty committed     to evaluate the performance of MT better. (Ott
by this token. At last, we analyze the correlation      et al., 2018) access uncertainty by comparing mul-
between relevance and uncertainty proportion. Our       tiple model outputs to multiple references with
results reveal that large amounts of tokens contain-    inter-sentence BLEU. (Glushkova et al., 2021)
ing very limited semantics are weighted equally         measure uncertainty through techniques of Monte
or even heavily in UQ. Similar observations are         Carlo dropout (Gal and Ghahramani, 2016) and
also observed when generalizing to the sentence-        deep ensembles (Lakshminarayanan et al., 2017).
level inequality by assessing relevant sentences and    (Fomicheva et al., 2020) use uncertainty quantifi-
irrelevant sentences.                                   cation methods to improve probability estimates in
neural networks. (Lahlou et al., 2021) proposed          3     Generative Inequality in Uncertainty
Direct Epistemic Uncertainty Prediction, a model-              Quantification
agnostic framework, for estimating epistemic un-
                                                         Tokens are created unequally in reflecting the mean-
certainty in machine learning models. For regres-
                                                         ing of the generation yet they are treated equally
sion tasks, (Wang et al., 2022) use uncertainty
                                                         when estimating uncertainty. We term these in-
quantification to address both data uncertainty and
                                                         equalities as generative inequalities and investigate
model uncertainty, and (Malinin et al., 2020) pro-
                                                         how they affect uncertainty quantification.
poses a method for uncertainty quantification using
Prior Networks to obtain interpretable measures of       3.1     Preliminaries
uncertainty at a low computational cost. For Natu-
                                                         LLMs normally output generations in a free-form
ral Language Understanding tasks, (Talman et al.,
                                                         and auto-regressive manner, i.e., progressively pre-
2023) use uncertainty quantification by applying
                                                         dicting the probability distribution of the next to-
Bayesian uncertainty modeling using Stochastic
                                                         ken. We denote by x the input (or the prompt)
Weight Averaging-Gaussian.
                                                         and s the sentence consisting of N tokens. Here,
Uncertainty Quantification in LLMs. Although             we take a sentence s as a completion regarding
uncertainty quantification has been thoroughly ex-       prompt x. Then, for a given LLM, the probability
amined in models with distinct labels, such as clas-     of generating zi as the i-th token can be described
sification models (Ulmer et al., 2022; Vazhentsev        as p(zi |s<i , x)(1 ≤ i ≤ N ), where s<i refers to
et al., 2022), it is still under-explored for popular    the previously generated tokens {z1 , ..., zi−1 }.
free-form LLMs, e.g., GPT (Radford et al., 2019),        Baseline. We use the popular Predictive Entropy
OPT (Zhang et al., 2022), LLaMA (Touvron et al.,         (PE), described in (Kadavath et al., 2022b), as the
2023a). These models present a unique challenge          baseline and investigate how it is affected by gen-
in uncertainty quantification as their solution do-      erative inequalities in this section. The Predictive
mains are flexible and effectively infinite, i.e., any   Entropy (PE) is defined as the entropy over the
generation can be deemed correct as long as the          whole sentence s:
semantics align consistently with the real answer.
                                                                                        X
                                                         PE(s, x) = − log p(s|x) =          − log p(zi |s<i , x).
   (Xiao et al., 2022) conducts large-scale empirical                                     i
evaluations on how the configuration (e.g., model                                                      (1)
size, architecture, training loss) of LLMs affect un-    It can be interpreted as the accumulation of the
certainty. (Lin et al., 2022a; Kadavath et al., 2022a)   token-wise entropy.
propose to quantify uncertainty by directly prompt-
                                                         3.2     Token-Level Generative Inequality
ing the language models to answer the uncertainty
with respect to their generations. (Manakul et al.,      Generative inequality refers to an observation: to-
2023b) measures the faithfulness of generations          kens containing limited semantics are equally val-
by quantifying the consistency of generations, i.e.,     ued when estimating the uncertainty of a sentence,
generations should be consistent if the model really     which is counter-intuitive. To outline this, we spec-
captured the concept. (Malinin and Gales, 2021)          ify two quantities for each token: how much se-
examines the uncertainty of free-form LLMs by            mantics the token contains, i.e., the relevance, and
calculating the accumulative predictive entropies        how much uncertainty the token committed, i.e.,
over multiple generations. Recently, Semantic En-        the uncertainty proportion.
tropy (SE) (Kuhn et al., 2023) is presented to tackle       For a given prompt x and the sentence s consist-
the “semantic equivalence” difficulty in uncertainty     ing of N tokens, i.e., s = {z1 , z2 , ..., zN }:
quantification. SE gathers generations sharing the       Relevance. To measure how important zi is in re-
same semantics into clusters and performs cluster-       flecting the semantics of s, we compare the seman-
wise predictive entropy as the uncertainty measure-      tic change before and after removing this token:
ment.
                                                             RT (zi , s, x) = 1 − |g(x ∪ s, x ∪ s \ {zi })|, (2)
   We aim to design metrics from multiple genera-
tions to characterize the uncertainty of LLMs. Our       where g(·, ·), calculating the similarity between
work focuses on the token- and sentence-level gen-       two sentences on a scale of 0 to 1, can be any
erative inequalities, which are not explored by prior    semantic similarity measurement. In our experi-
works in uncertainty quantification.                     ments, we leverage the Cross-Encoder (Reimers
                                                                                                                                   Token-level UP
                                                                                             0.4

                                                               Uncertainty Proportion (UP)
              More Irrelevant           More Relevant
                                                                                             0.2
                                                                                             0.0
                                                                                                         0.2       0.4       0.6         0.8
              More Irrelevant           More Relevant                                        0.3                               Sentence-Level UP

                                                                                             0.2
                                                                                             0.2
                                                                                                               1         2           3
                                                                                                                   Relevance
                                                               Figure 3: Correlations between relevance scores and un-
Figure 2: Distributions of relevance scores in both token-     certainty proportions in both token-level and sentence-
level and sentence-level situations. It is shown that          level situations. Irrelevant tokens and sentences domi-
irrelevant tokens and sentences take considerable pro-         nate the total volume of uncertainty quantification.
portions.

and Gurevych, 2019a)-RoBERTa-large (Liu et al.,                are semantically consistent with other sentences.
2019) as this measurement since it is one of the               Namely, a sentence that is semantically close to
most powerful sentence similarity evaluation mod-              other sentences is considered more representative.
els provided by the popular SentenceTransformers               Besides, the generative probability p(sj , x) pro-
Library (Reimers and Gurevych, 2019b). Gener-                  vides more confidence to sj when measuring rele-
ally, larger RT (zi , s, x) means removing zi will             vance, i.e., higher p(sj , x) makes sj more accept-
lead to significant semantic changing, indicating              able.
that zi is more relevant.                                         Similar to the token-level situation, the sentence-
Uncertainty Proportion. To measure the propor-                 level uncertainty proportion of si is defined as:
tion of uncertainty committed by zi , we simply
derive the ratio from Eq. (1):                                                                                        PE(si , x)
                                                                                                   UPS (si , S, x) = P             ,                (5)
                                                                                                                      k PE(sk , x)
                                − log p(zi |s<i , x)
       UPT (zi , s, x) =                             .   (3)
                                    PE(s, x)                   where 1 ≤ k ≤ K. It is the proportion of uncer-
Larger UPT (zi , s, x) means zi commits more un-               tainty committed by si ,
certainty when estimating the uncertainty of sen-
                                                               3.4                            Analytical Insights
tence s; vice versa.
                                                               We leverage the defined relevance and uncertainty
3.3   Sentence-Level Generative Inequality                     proportion to characterize the generative inequality
It has been widely shown that involving multiple               observations in this section. We utilize CoQA as
sentences benefits estimating uncertainty (Kada-               the dataset and OPT-13b as the model to be exam-
vath et al., 2022b). For instance, PE will usually be          ined. For each prompt in CoQA, we generate 10
the arithmetic                                                 sentences, i.e., K = 10 in Eq. (4) and Eq. (5).
               Pmean of multiple sentences in prac-
tice, i.e., K1 k PE(sk , x) (1 ≤ k ≤ K) where                  More details of generative hyper-parameters can
S = {s1 , s2 , ..., sK } consisting of K sentences re-         be found in Appendix A.
garding x and sk ∈ S is the k-th sentence. Follow-                We first quantify the histograms of token-
ing Section 3.2, for a given sentence si , we define           level relevance scores and sentence-level relevance
the sentence-level relevance of si as the probability-         scores. Results are summarized in Figure 2. For
weighted semantic similarity with other sentences:             token-level relevance, it is clear that most of the to-
                        X                                      kens are irrelevant tokens, i.e., low relevance scores,
    RS (si , S, x) =          g(si , sj )p(sj |x), (4)         indicating that linguistic redundancy exists widely.
                      j=1,j̸=i
                                                               In terms of the sentence-level situation, although
where 1 ≤ i, j ≤ K and p(sj |x) is the generative              the distribution is smoother than the token-level
probability of sj . It is out of an intuitive assump-          situation, the irrelevant sentences still take a con-
tion that sentences are more convincing if they                siderable amount over all the sentences.
   We further investigate the correlations between      relevant tokens by re-weighting token entropy ac-
relevance and uncertainty proportions, i.e., how        cording to their normalized relevance scores:
much uncertainty is committed by tokens and sen-
                                                         ET (zi , sj , x) = − log p(zi |s<i , x)R̃T (zi , sj , x).
tences under various relevance scores. Specifi-
                                                                                                                (7)
cally, we first group tokens and sentences into 10
                                                        The token-level shifted predictive entropy defined
bins with uniform relevance ranges and then aver-
                                                        over sj can be formulated as:
age/sum the uncertainty proportions committed by
tokens or sentences grouped in the same bin. Since                                    Nj
                                                                                      X
irrelevant tokens take majority proportions over all        TOKEN SAR(sj , x) =             ET (zi , sj , x).   (8)
the tokens, averaging the uncertainty proportions                                       i

in each bin may hide the real effect of irrelevant      The reason we normalize relevance score in Eq. (6)
tokens. Therefore, we report the sum of uncertainty     is two-fold: a) to make tokens comparable across
proportions in each bin in the token-level situation.   sentences; b) to mitigate the bias posed by the
Results are summarized in Figure 3.                     length of sentence, such as the length normaliza-
   It is clear that irrelevant tokens/sentences com-    tion in Length-normalized Predictive Entropy (LN-
mit significantly more uncertainty than relevant        PE) (Malinin and Gales, 2020). In this way, the
sentences in both token-level and sentence-level        uncertainty proportions of tokens containing strong
situations. These observations demonstrate the ex-      relevance will be enlarged when estimating uncer-
istence of sentence inequalities and also the un-       tainty.
certainty quantification is highly affected by these    Sentence-Level Shifting. As mentioned in Sec-
inequalities.                                           tion 3.3, sentences that have higher relevance
                                                        scores, i.e., semantically consistent, are more con-
4     Shifting Attention to Relevance                   vincing than others. Therefore, we simply reduce
A natural hypothesis derived from Section 3.4 is        sentence uncertainty by enlarging its generative
that shifting the attention to those relevant com-      probability with a relevance-controlled quantity:
ponents may benefit uncertainty quantification. In                                           1
                                                         ES (sj , S, x) = − log(p(sj |x) + RS (sj , S, x))
this section, we introduce the proposed Shifting                               P              t
Attention to Relevance (SAR) in detail.                                          k̸=j g(s j k )p(sk |x)
                                                                                           , s
                                                         = − log(p(sj |x) +                             ),
                                                                                            t
4.1    Notations                                                               |           {z         }
                                                                                       sentence relevance
We reuse the notations defined in Section 3.1 where                         Q                           (9)
we denote by x the prompt and S the K sentences         where p(sj |x) = i p(zi |s<i , x) is the generative
regarding x. There will be Nj tokens for each           probability of sj and t is the temperature used to
sentence sj ∈ S (1 ≤ j ≤ K).                            control the scale of shifting. Then, the sentence-
                                                        level shifted predictive entropy over K sentences
4.2    Relevance Discovery and Shifting                 can be formulated as:
SAR corrects generative inequalities by reviewing                               1 X
                                                           SENTSAR(S, x) =             ES (sk , S, x). (10)
the relevance of each token and/or sentence and                                 K
                                                                                       k
emphasizing uncertainty quantification attention to
those more relevant components. Here we intro-          Note that Eq. (9) shares a similar form with
duce token-level shifted measurement and sentence-      SE (Kuhn et al., 2023), i.e., reducing the uncer-
level shifted measurements:                             tainty of semantically consistent sentences. Differ-
Token-Level Shifting. For a sentence sj regard-         ently, SE achieves this with bi-directional entail-
ing prompt x, sj = {z1 , z2 , ..., zNj } contains Nj    ment prediction and we achieve this with weighted
tokens. We first calculate the normalized rele-         relevance scores. With manual examination, we
vance score for each token zi (1 ≤ i ≤ Nj ) based       found that around 36.7% of the entailment predic-
on Eq. (2), i.e., RT (zi , sj , x):                     tions are undesirable, over the long sentences that
                                                        have more than 20 tokens on average (120 ques-
                             RT (zi , sj , x)           tions in total). Instead, our SENTSAR leverages
        R̃T (zi , sj , x) = PNj                   (6)   the more “soft” sentence similarity to calculate the
                             n RT (zn , sj , x)
                                                        relevance score, which is more desirable for long
Then we enlarge the uncertainty proportions of          and complex sentences.
        0.76
                                                CoQA                                  0.70
                                                                                                    CoQA                    TriviaQA
                                                                                                                     0.82
                                                                                      0.69
        0.74                                                                                                         0.80
                                                                                      0.68

AUROC
        0.72                                                                                                         0.78
                                                                                      0.67
                                                                                                                     0.76
        0.70                             PE            tokenSAR                       0.66
                                         LN PE         sentSAR                                                       0.74
                                                                                      0.65
        0.68                             SE            SAR                                                           0.72
                                                                                      0.64
                    OPT-2.7b           OPT-6.7b        OPT-13b         OPT-30b               Llama-7b    Llama-13b          Llama-7b
Figure 4: The AUROCs of TOKENSAR, SENTSAR, SAR, and baseline methods, across various “off-the-shelf” LLMs
and datasets (e.g., CoQA, and Trivia QA). Rouge-L with a threshold of 0.5 is used as the correctness metric. The
proposed SAR substantially outperforms existing methods across all the scenarios.

    Models & Datasets           LS         PE      LN-PE          SE    TOKEN SAR (∆SE)         SENTSAR(∆SE)         SAR(∆SE)
    Vicuna-13b w./ 5 generations are generated for each question
    Trivia QA                  0.560      0.690    0.624      0.630         0.692 (+6.2%)       0.745 (+11.5%)   0.749 (+11.9%)
    SciQ                       0.589      0.708    0.668      0.675         0.706 (+3.1%)        0.745 (7.0%)     0.741 (+6.6%)
    Vicuna-33b w./ 5 generations are generated for each question
    Trivia QA                  0.565      0.644    0.639      0.651         0.652 (+0.1%)        0.715 (+6.4%)    0.710 (5.9%)
    SciQ                       0.584      0.665    0.668      0.674         0.665 (-0.9%)        0.717 (+4.3%)   0.710 (+3.6%)
    WizardLM-13b w./ 5 generations are generated for each question
    Trivia QA                  0.519      0.647    0.615      0.634         0.657 (+2.3%)       0.743 (+10.9%)   0.744 (+11.0%)
    SciQ                       0.574      0.677    0.638      0.649         0.681 (+3.2%)        0.719 (+7.0%)   0.707 (+5.8%)
    LLaMA-2-13b-chat w./ 5 generations are generated for each question
    Trivia QA                  0.504      0.647    0.615      0.622         0.654 (+3.2%)        0.698 (+7.6%)   0.704 (+8.2%)
    SciQ                       0.578      0.718    0.688      0.692         0.718 (+2.6%)        0.737 (+4.5%)   0.725 (+3.3%)
    Average                    0.555      0.675    0.644      0.653         0.678 (+2.5%)        0.727 (+7.4%)   0.724 (+7.1%)

Table 1: Uncertainty quantification AUROCs of TOKENSAR, SENTSAR, SAR, and baseline methods, across various
instruction-tuned open-source LLMs, over different datasets (e.g., SciQ, and Trivia QA). The threshold of Rouge-L
is set to 0.5. Underline means the second best method.

4.3            Overall Measurement                                      as the token-shifted predictive entropy, sentence-
                                                                        shifted predictive entropy, and both token- and
Token-level shifting and sentence-level shifting
                                                                        sentence-shifted predictive entropy respectively, in
are conceptually different as they emphasize dif-
                                                                        the rest of this paper.
ferent perspectives. However, they are orthogo-
nal and can be naturally combined to shift atten-
                                                                        5     Empirical Evaluations
tion from both token-level and sentence-level, re-
sulting in more effective uncertainty quantifica-                       5.1     Experimental Settings
tion. To achieve that, we simply replace the gen-
                                                                   Baselines. We consider 4 baseline methods in
erative probabilities in Eq. (9), i.e., p(si |x) and
                                                                   our experiments, including Lexical Similarity (Lin
p(sj |x), with the token-shifted probability derived
                                                                   et al., 2022b), Semantic Entropy (SE) (Kuhn et al.,
from Eq. (8), i.e. p′ (si |x) = e−TOKENSAR(si ,x) and
                                                                   2023), Predictive Entropy (PE) (Kadavath et al.,
p′ (sj |x) = e−TOKENSAR(sj ,x) :
                                                                   2022b), and Length-normalized Predictive Entropy
                                    P                  ′           (LN-PE)    (Malinin and Gales, 2020). Lexical Sim-
                          ′           k̸=j g(sj , sk )p (sj |x)
ET,S (sj , S, x) = − log(p (si |x)+                             ). ilarity considers the similarities among multiple
                                                 t
                                                          (11)     sentences. SE introduces the “semantic equiva-
Then the token- and sentence-level shifted predic- lence” difficulty in the uncertainty quantification of
tive entropy  P over K sentences can be defined as                 free-form LLMs and tackles this issue by gathering
SAR = K1 k ET,S (sk , S, x).                                       sentences containing the same meaning into clus-
   We denote TOKENSAR, SENTSAR, and SAR                            ters and calculating cluster-wise entropy. LN-PE is
AUROC

         Figure 5: The performance of SAR and baseline methods over various numbers of generations.

AUROC

         Figure 6: The performance of SAR over various Rouge-L and Sentence Similarity thresholds.

the length normalized PE, i.e., divided by sentence    Gurevych, 2019b). The sensitivity of SAR to these
length N : LN-PE(s, x) = N1 PE(s, x).                  thresholds will be studied in Section 5.4.
Models. We conduct experiments over popu-              Evaluation Metric. Following prior work (Kuhn
lar “off-the-shelf” LLMs, including instruction-       et al., 2023), we evaluate uncertainty quantification
tuned LLMs (e.g., Vicuna (Zheng et al., 2023),         by predicting the correctness of the model’s gener-
LLaMA-2-chat (Touvron et al., 2023b), Wiz-             ations regarding a given question. The area under
ardLM (Xu et al., 2023)) and pre-trained LLMs          the receiver operator characteristic curve (AUROC)
(e.g., OPT (Zhang et al., 2022) and LLaMA (Tou-        indicates the probability that a random correct gen-
vron et al., 2023a)), with model size up to 33B. We    eration has a lower uncertainty than a random in-
leverage greedy search for the most likely genera-     correct generation, predicted by uncertainty quan-
tions which are used to evaluate correctness, and      tification methods. AUROC equals 0.5 meaning
multinominal sampling for reference generations        the assigned uncertainty is no better than random
which are used to estimate uncertainty. More de-       guessing, i.e., they can not differentiate between
tails of generative hyper-parameters can be found      correct and incorrect generations. AUROC equals
in A                                                   1 meaning all the correct generations are assigned
                                                       lower uncertainty than all incorrect generations.
Datasets. We consider 5 free-form question-            Hyperparameters. For OPT-2.7b/6.7b/13b, we
answering datasets: CoQA (Reddy et al., 2019),         generate 10 generations for each question, i.e.
Trivia QA (Joshi et al., 2017), SciQ (Welbl et al.,    K=10. For other models, we generate 5 gener-
2017), MedQA (Jin et al., 2021) and MedM-              ations. The temperature t is set to 0.001. The gen-
CQA (Pal et al., 2022). More details of the used       erative settings can be can be found in Appendix A.
datasets and the splittings can be found in B.         All the experiments are conducted on a server with
Correctness Metrics. We adopt Rouge-L (Lin,            one Intel(R) Xeon(R) Platinum 8358 CPU and two
2004) and sentence similarity as the correctness       NVIDIA A100 GPUs.
metrics when evaluating the correctness of LLMs’
generations. We set the threshold of Rouge-L            5.2   UQ for pre-trained LLMs
and sentence similarity as 0.5, i.e., generations      We compare SAR, TOKENSAR, and SENTSAR with
having above 0.5 semantic similarities/Rouge-L         state-of-the-art methods. Results are summarized
scores with the ground truth are correct. Sentence     in Figure 4. Generally, our methods significantly
similarity is measured by DistillRoBERTa (Sanh         outperform prior methods in most of the settings.
et al., 2019) in SentenceTransformers (Reimers and     For instance, SAR outperforms other methods by at
                               SAR w. sentence similarity                                                               avg. AUROC
  OPT Size    SE     RoBERTa      MiniLM      MPNet       OPT-13b       Method          # Generation       Time (s)
                                                                                                                       SciQ/Trivia QA
      2.7b   0.699    0.735        0.723      0.723       0.716
      6.7b   0.717    0.750        0.740      0.739       0.731         PE                   5              5.28        0.692/0.657
      13b    0.725    0.753        0.741      0.740       0.733         LN-PE                5              5.28        0.666/0.623
      30b    0.726    0.748        0.738      0.739       0.734         SE                   5              6.78        0.673/0.634

Table 2: Sensitivity of SAR to sentence similarity mea-                 SENTSAR              2              2.64        0.708/0.685
surements. We consider popular models from Sentence-
                                                                    Table 3: Efficiency comparisons between 2-generations
Transformers (Appendix D) and also the target LLMs
                                                                    SAR and 5-generations baseline methods.
as the sentence similarity measurement.
                                                                             Model               Dataset       LN-PE     SE      SAR
most 3.6% AUROC over the CoQA dataset, mea-                                                    MedQA           0.572    0.599   0.598
                                                                           Vicuna-13b
sured by Rouge-L 0.5. The results of setting Rouge-                                           MedMCQA          0.649    0.685   0.717

L to 0.3, which is the same as in (Kuhn et al., 2023),                  LLaMA-2-13b-chat
                                                                                               MedQA           0.562    0.609   0.616
                                                                                              MedMCQA          0.647    0.655   0.702
can be found in Appendix C.4.
                                                                          WizardLM-13b           MedQA         0.609    0.620   0.635
   Also, the synergy of TOKENSAR and SENTSAR
achieves remarkable improvements. For instance,                     Table 4: The performance of SAR and baseline methods
TOKEN SAR and SENT SAR achieve 0.723 AUROC                          over medical Q&A datasets. Our method achieves better
in the OPT-30b-CoQA setting yet combining them                      performances for most settings.
results in 0.748 AUROC. It indicates that TO -
KEN SAR and SENT SAR are compatible and can                         tization will be affected as the metrics are getting
be incorporated effectively.                                        harsh. However, our methods significantly outper-
                                                                    form baseline methods in most cases.
5.3      UQ for Instruction-Tuned LLMs                              Efficiency Comparison. In Appendix C.5, we
We estimate the uncertainty of powerful instruction-                provide a detailed computational cost analysis, re-
tuned LLMs, including Vicuna-13b/33b, LLaMA-                        garding the time consumed by each operation. We
2-chat-13b, and WizardLM-13b. All these models                      provide the results of 2-generations SENTSAR with
are obtained from Huggingface, without any fur-                     5-generations baseline methods in Table 3 over
ther modifications. Results are summarized in Ta-                   instruction-tuned LLMs. Our method surpasses
ble 1. It is shown that SAR consistently beat base-                 the baseline methods while consuming less than
line methods in most situations. For example, SAR                   half the time, demonstrating its greater generation
outperforms SE by 7.1% AUROC on average, eval-                      efficiency.
uated by Rouge-L 0.5.
                                                                    5.5     UQ in Medical Domain
5.4      Ablation Studies                                           We evaluate SAR over the AI for science scenarios,
Number of Generations. The effects of the num-                      such as medical domains. As shown in Table 4, we
ber of generations are summarized in Figure 5. It                   perform experiments over MedQA (Jin et al., 2020)
is shown that our SAR is generation-efficient, i.e.,                and MedMCQA (Pal et al., 2022) datasets and our
it achieves 0.750 AUROC with only 5 generations                     methods achieve better performance for most of
and it can be consistently boosted with more gener-                 the settings. This indicates the potential impacts of
ations, while other methods may even drop slightly                  our methods on the real world.
when more generations are provided.
                                                                    6     Conclusion
Sensitivity to Sentence Similarity. We investigate
the sensitivity of SAR to sentence similarity mea-                  In this paper, we disclose the generative inequality
surements. As shown in Table 2, general-purpose                     observation in uncertainty quantification: tokens
sentence similarity models are desirable and more                   and generations are created unequally in reflecting
effective than the target LLMs (last column of Ta-                  semantics yet they are treated equally when esti-
ble 2). This is because LLMs are not specifically                   mating uncertainty, which is counter-intuitive. We
designed for sentence similarity.                                   propose to tackle these inequalities by Shifting At-
Sensitivity to Correctness Metrics. Empirical re-                   tention to Relevance (SAR) from both token-level
sults are presented in Figure 5. Higher thresholds                  (TOKENSAR) and sentence-level (SENTSAR). Ex-
mean the correctness standards are more harsh. It                   periments over “off-the-shelf” LLMs demonstrate
is shown that the performances of uncertainty quan-                 the superior performances of SAR.
7   Ethical Considerations                                 Antonia Creswell, Murray Shanahan, and Irina Higgins.
                                                             2022. Selection-inference: Exploiting large language
Our proposed method has the potential to impact              models for interpretable logical reasoning.
the credibility and reliability of LLMs, particu-
                                                           Jinhao Duan, Renming Zhang, James Diffenderfer,
larly in the context of reducing misinformation.              Bhavya Kailkhura, Lichao Sun, Elias Stengel-Eskin,
LLMs have the potential to generate highly plausi-            Mohit Bansal, Tianlong Chen, and Kaidi Xu. 2024.
ble but false information. Uncertainty quantifica-            Gtbench: Uncovering the strategic reasoning limita-
tion techniques can help distinguish between accu-            tions of llms via game-theoretic evaluations. arXiv
                                                              preprint arXiv:2402.12348.
rate and misleading outputs. Success in adequately
addressing this issue can contribute to the preven-        Marina Fomicheva, Shuo Sun, Lisa Yankovskaya,
tion spread of misinformation and its potential so-         Frédéric Blain, Francisco Guzmán, Mark Fishel,
                                                            Nikolaos Aletras, Vishrav Chaudhary, and Lucia Spe-
cietal consequences
                                                            cia. 2020. Unsupervised quality estimation for neural
                                                            machine translation. Transactions of the Association
8   Limitations                                             for Computational Linguistics, 8:539–555.
Our method will introduce sentence similarity cal-         Yarin Gal and Zoubin Ghahramani. 2016. Dropout as a
culations and comparisons. We tackle this issue by           bayesian approximation: Representing model uncer-
leveraging a small backbone in our implementation            tainty in deep learning. In international conference
                                                             on machine learning, pages 1050–1059. PMLR.
but it still might bring additional latency in practice.
In addition, our methods require access to token           Zorik Gekhman, Jonathan Herzig, Roee Aharoni, Chen
logits. Although token logits are widely supported           Elkind, and Idan Szpektor. 2023. Trueteacher: Learn-
                                                             ing factual consistency evaluation with large lan-
by commercial LLM providers, this still might re-            guage models.
strict the potential application of our methods in
black-box scenarios.                                       Taisiya Glushkova, Chrysoula Zerva, Ricardo Rei, and
                                                             André FT Martins. 2021. Uncertainty-aware machine
Acknowledgement                                              translation evaluation. In Findings of the Association
                                                             for Computational Linguistics: EMNLP 2021, pages
This work was performed under the auspices                   3920–3938.
of the U.S. Department of Energy by Lawrence               Junyuan Hong, Jinhao Duan, Chenhui Zhang,
Livermore National Laboratory under Contract                 Zhangheng Li, Chulin Xie, Kelsey Lieberman, James
DE-AC52-07NA27344 and was supported by the                   Diffenderfer, Brian Bartoldson, Ajay Jaiswal, Kaidi
                                                             Xu, et al. 2024. Decoding compressed trust: Scru-
LLNL-LDRD Program under Project No. 23-ERD-                  tinizing the trustworthiness of efficient llms under
030 (LLNL-CONF-851171). This work was par-                   compression. arXiv preprint arXiv:2403.15447.
tially supported by the National Science Founda-
tion under Grant No.2319242.                               Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng,
                                                             Hanyi Fang, and Peter Szolovits. 2020. What dis-
                                                             ease does this patient have? a large-scale open do-
                                                             main question answering dataset from medical exams.
References                                                   arXiv preprint arXiv:2009.13081.
Ning Bian, Peilin Liu, Xianpei Han, Hongyu Lin, Yaojie     Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng,
  Lu, Ben He, and Le Sun. 2023. A drop of ink makes          Hanyi Fang, and Peter Szolovits. 2021. What disease
  a million think: The spread of false information in        does this patient have? a large-scale open domain
  large language models.                                     question answering dataset from medical exams. Ap-
                                                             plied Sciences, 11(14):6421.
Abeba Birhane, Atoosa Kasirzadeh, David Leslie, and
  Sandra Wachter. 2023. Science in the age of large        Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke
  language models. Nature Reviews Physics, 5:277 –          Zettlemoyer. 2017. Triviaqa: A large scale distantly
  280.                                                      supervised challenge dataset for reading comprehen-
                                                            sion. arXiv preprint arXiv:1705.03551.
Zhipeng Chen, Kun Zhou, Beichen Zhang, Zheng Gong,
  Wayne Xin Zhao, and Ji-Rong Wen. 2023. Chatcot:          Saurav Kadavath, Tom Conerly, Amanda Askell, T. J.
  Tool-augmented chain-of-thought reasoning on chat-         Henighan, Dawn Drain, Ethan Perez, Nicholas
  based large language models.                               Schiefer, Zachary Dodds, Nova DasSarma, Eli Tran-
                                                             Johnson, Scott Johnston, Sheer El-Showk, Andy
Paul F Christiano, Jan Leike, Tom Brown, Miljan Mar-         Jones, Nelson Elhage, Tristan Hume, Anna Chen,
  tic, Shane Legg, and Dario Amodei. 2017. Deep              Yuntao Bai, Sam Bowman, Stanislav Fort, Deep
  reinforcement learning from human preferences. Ad-         Ganguli, Danny Hernandez, Josh Jacobson, John
  vances in neural information processing systems, 30.       Kernion, Shauna Kravec, Liane Lovitt, Kamal
  Ndousse, Catherine Olsson, Sam Ringer, Dario                Andrey Malinin, Sergey Chervontsev, Ivan Provilkov,
  Amodei, Tom B. Brown, Jack Clark, Nicholas Joseph,            and Mark Gales. 2020. Regression prior networks.
  Benjamin Mann, Sam McCandlish, Christopher Olah,              arXiv preprint arXiv:2006.11590.
  and Jared Kaplan. 2022a. Language models (mostly)
  know what they know. ArXiv, abs/2207.05221.                 Andrey Malinin and Mark Gales. 2020. Uncertainty esti-
                                                                mation in autoregressive structured prediction. arXiv
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom                preprint arXiv:2002.07650.
  Henighan, Dawn Drain, Ethan Perez, Nicholas
  Schiefer, Zac Hatfield Dodds, Nova DasSarma, Eli            Andrey Malinin and Mark John Francis Gales. 2021.
  Tran-Johnson, et al. 2022b. Language models                   Uncertainty estimation in autoregressive structured
  (mostly) know what they know. arXiv preprint                  prediction. In International Conference on Learning
  arXiv:2207.05221.                                             Representations.
                                                              Potsawee Manakul, Adian Liusie, and Mark J. F. Gales.
Marzena Karpinska and Mohit Iyyer. 2023. Large lan-             2023a. Selfcheckgpt: Zero-resource black-box hal-
 guage models effectively leverage document-level               lucination detection for generative large language
 context for literary translation, but critical errors per-     models.
 sist.
                                                              Potsawee Manakul, Adian Liusie, and Mark John Fran-
Alex Kendall and Yarin Gal. 2017. What uncertainties            cis Gales. 2023b. Selfcheckgpt: Zero-resource black-
  do we need in bayesian deep learning for computer             box hallucination detection for generative large lan-
  vision? Advances in neural information processing             guage models. ArXiv, abs/2303.08896.
  systems, 30.
                                                              Myle Ott, Michael Auli, David Grangier, and
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.          Marc’Aurelio Ranzato. 2018. Analyzing uncertainty
  Semantic uncertainty: Linguistic invariances for un-         in neural machine translation. In International Con-
  certainty estimation in natural language generation.         ference on Machine Learning, pages 3956–3965.
  arXiv preprint arXiv:2302.09664.                             PMLR.

Salem Lahlou, Moksh Jain, Hadi Nekoei, Victor Ion             Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  Butoi, Paul Bertin, Jarrid Rector-Brooks, Maksym              Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  Korablyov, and Yoshua Bengio. 2021. Deup: Di-                 Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
  rect epistemic uncertainty prediction. arXiv preprint         2022. Training language models to follow instruc-
  arXiv:2102.08501.                                             tions with human feedback. Advances in Neural
                                                                Information Processing Systems, 35:27730–27744.
Balaji Lakshminarayanan, Alexander Pritzel, and
  Charles Blundell. 2017. Simple and scalable pre-            Ankit Pal, Logesh Kumar Umapathi, and Malaikannan
  dictive uncertainty estimation using deep ensembles.          Sankarasubbu. 2022. Medmcqa: A large-scale multi-
  Advances in neural information processing systems,            subject multi-choice dataset for medical domain ques-
  30.                                                           tion answering. In Proceedings of the Conference
                                                                on Health, Inference, and Learning, volume 174 of
Baihan Lin, Djallel Bouneffouf, Guillermo Cecchi, and           Proceedings of Machine Learning Research, pages
  Kush R. Varshney. 2023. Towards healthy ai: Large             248–260. PMLR.
  language models need therapists too.
                                                              Liangming Pan, Alon Albalak, Xinyi Wang, and
Chin-Yew Lin. 2004. Rouge: A package for automatic              William Yang Wang. 2023. Logic-lm: Empower-
  evaluation of summaries. In Annual Meeting of the             ing large language models with symbolic solvers for
  Association for Computational Linguistics.                    faithful logical reasoning.
                                                              Alec Radford, Jeff Wu, Rewon Child, David Luan,
Stephanie Lin, Jacob Hilton, and Owain Evans. 2022a.
                                                                Dario Amodei, and Ilya Sutskever. 2019. Language
  Teaching models to express their uncertainty in
                                                                models are unsupervised multitask learners.
  words. arXiv preprint arXiv:2205.14334.
                                                              Siva Reddy, Danqi Chen, and Christopher D Manning.
Zi Lin, Jeremiah Zhe Liu, and Jingbo Shang. 2022b. To-           2019. Coqa: A conversational question answering
   wards collaborative neural-symbolic graph semantic            challenge. Transactions of the Association for Com-
   parsing via uncertainty. Findings of the Association          putational Linguistics, 7:249–266.
   for Computational Linguistics: ACL 2022.
                                                              Nils Reimers and Iryna Gurevych. 2019a. Sentence-
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-             bert: Sentence embeddings using siamese bert-
  dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,                 networks. arXiv preprint arXiv:1908.10084.
  Luke Zettlemoyer, and Veselin Stoyanov. 2019.
  Roberta: A robustly optimized bert pretraining ap-          Nils Reimers and Iryna Gurevych. 2019b. Sentence-
  proach. arXiv preprint arXiv:1907.11692.                      bert: Sentence embeddings using siamese bert-
                                                                networks. In Proceedings of the 2019 Conference on
Jieyi Long. 2023. Large language model guided tree-of-          Empirical Methods in Natural Language Processing.
   thought.                                                     Association for Computational Linguistics.
Victor Sanh, Lysandre Debut, Julien Chaumond, and            with pre-trained language models: A large-scale em-
  Thomas Wolf. 2019. Distilbert, a distilled version         pirical analysis. arXiv preprint arXiv:2210.04714.
  of bert: smaller, faster, cheaper and lighter. ArXiv,
  abs/1910.01108.                                          Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng,
                                                             Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin
Ashish Sharma, Inna W Lin, Adam S Miner, David C             Jiang. 2023. Wizardlm: Empowering large lan-
  Atkins, and Tim Althoff. 2023. Human–ai collabo-           guage models to follow complex instructions. arXiv
  ration enables more empathic conversations in text-        preprint arXiv:2304.12244.
  based peer-to-peer mental health support. Nature
  Machine Intelligence, 5(1):46–57.                        Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo
                                                              Sun, and Yue Zhang. 2024. A survey on large lan-
Lichao Sun, Yue Huang, Haoran Wang, Siyuan Wu,                guage model (llm) security and privacy: The good,
  Qihui Zhang, Chujie Gao, Yixin Huang, Wenhan                the bad, and the ugly. High-Confidence Computing,
  Lyu, Yixuan Zhang, Xiner Li, et al. 2024. Trustllm:         page 100211.
  Trustworthiness in large language models. arXiv
  preprint arXiv:2401.05561.                               Susan Zhang, Stephen Roller, Naman Goyal, Mikel
                                                             Artetxe, Moya Chen, Shuohui Chen, Christopher De-
Aarne Talman, Hande Celikkanat, Sami Virpioja,               wan, Mona Diab, Xian Li, Xi Victoria Lin, Todor Mi-
  Markus Heinonen, and Jörg Tiedemann. 2023.                 haylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel
  Uncertainty-aware natural language inference with          Simig, Punit Singh Koura, Anjali Sridhar, Tianlu
  stochastic weight averaging. In Proceedings of the         Wang, and Luke Zettlemoyer. 2022. Opt: Open
  24th Nordic Conference on Computational Linguis-           pre-trained transformer language models. ArXiv,
  tics (NoDaLiDa), pages 358–365.                            abs/2205.01068.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier      Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,            Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal         Zhuohan Li, Dacheng Li, Eric. P Xing, Hao Zhang,
  Azhar, Aur’elien Rodriguez, Armand Joulin, Edouard         Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
  Grave, and Guillaume Lample. 2023a. Llama: Open            llm-as-a-judge with mt-bench and chatbot arena.
  and efficient foundation language models. ArXiv,
  abs/2302.13971.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
  Bhosale, et al. 2023b. Llama 2: Open founda-
  tion and fine-tuned chat models. arXiv preprint
  arXiv:2307.09288.
Dennis Ulmer, Jes Frellsen, and Christian Hardmeier.
  2022. Exploring predictive uncertainty and calibra-
  tion in nlp: A study on the impact of method & data
  scarcity. arXiv preprint arXiv:2210.15452.
Artem Vazhentsev, Gleb Kuzmin, Artem Shelmanov,
  Akim Tsvigun, Evgenii Tsymbalov, Kirill Fedyanin,
  Maxim Panov, Alexander Panchenko, Gleb Gusev,
  Mikhail Burtsev, et al. 2022. Uncertainty estima-
  tion of transformer predictions for misclassification
  detection. In Proceedings of the 60th Annual Meet-
  ing of the Association for Computational Linguistics
  (Volume 1: Long Papers), pages 8237–8252.
Yuxia Wang, Daniel Beck, Timothy Baldwin, and Karin
  Verspoor. 2022. Uncertainty estimation and reduc-
  tion of pre-trained models for text regression. Trans-
  actions of the Association for Computational Linguis-
  tics, 10:680–696.
Johannes Welbl, Nelson F. Liu, and Matt Gardner. 2017.
  Crowdsourcing multiple choice science questions.
  ArXiv, abs/1707.06209.
Yuxin Xiao, Paul Pu Liang, Umang Bhatt, Willie
  Neiswanger, Ruslan Salakhutdinov, and Louis-
  Philippe Morency. 2022. Uncertainty quantification
Appendix                                                C         Additional Experimental Analysis

A    Details of LLMs Generation                         C.1          Effects of SAR Temperature t
                                                        The hyperparameter t introduced in Eq. (9) is used
OPT models. We will generate 1 most likely gener-
                                                        to control the scale of sentence shifting. The ef-
ation with the greedy search for all the OPT models.
                                                        fects of t is provided in Table 5. It is shown that t
This generation will be used to evaluate the correct-
                                                        marginally affects the performance of SAR.
ness. For OPT-2.7b/6.7b/13b, we will generate 10
sentences for each question with multinomial sam-
                                                                                   OPT-13b                    LLaMA-7b
pling for uncertainty quantification. For OPT-30b,               t
                                                                             CoQA            SciQ         CoQA         TriviaQA
we will generate 5 sentences. The temperature of
                                                          1 × 10−3         0.753/0.720    0.737/0.784   0.697/0.658   0.823/0.815
generation is fixed at 0.5 for all models. For OPT-       1 × 100          0.752/0.719    0.739/0.786   0.695/0.656   0.822/0.816
2.6b/6.7b/13b, the max length of each generation          1 × 101          0.743/0.714    0.729/0.786   0.686/0.658   0.813/0.812

is set to 256 tokens for the CoQA dataset and SciQ      Table 5: Effects of temperature t in Eq. (9). Results are
dataset and is set to 128 tokens for the Trivia QA      evaluated by Rouge-L with 0.5 as the threshold. Results
dataset. For OPT-30b, the max length of each gen-       are obtained from SAR/TOKENSAR.
eration is set to 128 tokens for all the datasets.
LLaMA/Vicuna/WizardLM. We will generate 1
most likely generation with the greedy search and 5     C.2          Generation Efficiency
sentences with multinomial sampling for all these
                                                        The generation-efficiency of SAR on LLaMA-7b-
models. The max length of each generation is set
                                                        Trivia QA setting is presented in Figure 7.
to 128 tokens. The temperature of generation is set
to 0.5.
                                                                              SAR
                                                                0.82          SE
B   Datasets                                                                  LN-PE
                                                                0.81
CoQA (Reddy et al., 2019) is a large-scale con-                 0.80

                                                        AUROC
versational QA task, with more than 127,000 ques-
                                                                0.79
tions. Each question is equipped with a passage to
provide contextual information. Trivia QA (Joshi                0.78
et al., 2017) is a high-quality reading compre-
                                                                0.77
hension dataset that contains over 650k question-
answer pairs. These questions are obtained from                 0.76
trivia enthusiasts and answers from Wikipedia.                         1              2             3            4            5
                                                                                      Number of Generations
SciQ (Welbl et al., 2017) dataset is a science-
related QA dataset aimed at developing models’ ca-      Figure 7: The performance of SAR over various numbers
pabilities of understanding complex scientific texts.   of generations. Results are obtained from the LLaMA-
                                                        7b model over the Trivia QA dataset.
It consists of approximately 13,679 crowdsourced
science questions. MedQA (Jin et al., 2020) is
a free-form multiple-choice OpenQA dataset for
solving medical problems, collected from the pro-       C.3          Sensitivity to Sentence Length.
fessional medical board exams. MedMCQA (Pal             To study how the SAR is affected by sentence
et al., 2022) is a large-scale, Multiple-Choice Ques-   length, we quantify the uncertainty rank change
tion Answering (MCQA) dataset designed to ad-           for each sentence, caused by SAR and SENTßSAR.
dress real-world medical entrance exam questions.       Assume a sentence has a rank of i among all the
   Following (Kuhn et al., 2023), we randomly se-       sentences, evaluated by LN-PE and has a rank of j
lect around 8,000 questions from the training split     evaluated by SAR, then the uncertainty rank change
of Trivia QA as the questions to be examined. For       is |i − j|. The correlations between average un-
instruction-tuned experiments, we use 2,000 ques-       certainty rank change and sentence length are pre-
tions of Trivia QA. We utilize the full validation      sented in Figure 8. It is shown that our methods
set (1,000 questions) of SciQ and the development       tend to conclude medium- and long-length sen-
split (7,983 questions) of CoQA.                        tences.
                                         SAR                             sentSAR

Uncertainty Rank Change
                   1100                               3000
                   1000                               2500
                          500                             500
                          400                               0
                                0   10    20    30   40         0   10    20   30   40
                                               Sentence Length
    Figure 8: Demographic analysis of sentence length. Un-
    certainty Rank Change between (Left) SAR and LN-PE,
    and between (Right) SENTSAR and LN-PE. It is shown
    that SAR and SENTSAR are more tend to affect medium-
    or long-length sentences.

    C.4                     Different Correctness Metric Threshold
   We report the results of Rouge-L (0.3) (same
   as (Kuhn et al., 2023) in Table 6.

    C.5                     Computational Costs Analysis
   SAR is more generation-efficient. It surpasses base-
   line methods under significantly smaller compu-
   tational constraints. We have quantified the time
   consumed for each step in the overall uncertainty
   quantification pipeline. This includes sequence
   generation, computing logits, semantic clustering
   for SE, and sentence similarity for SAR. We ex-
   clude the time taken for aggregating logits/scores
   as it is negligible (less than 0.001 seconds for all
   methods). The average time consumed per ques-
   tion, based on an evaluation of 1000 questions from
   the Vicuna-13b + SciQ dataset, is provided. These
   measurements were taken using an AMD EPYC
   7302 16-Core CPU and a 1xA40 GPU server. Re-
   sults are summarized in Table 7.

    D                      Sentence Similarity Measurement
   The following is the sentence similarity measure-
   ment models we leveraged in Table 2:

                    • RoBERTa: cross-encoder/stsb-roberta-large

                    • MiniLM: sentence-transformers/all-MiniLM-
                      L6-v2

                    • MPNet:               sentence-transformers/all-mpnet-
                      base-v2
  Dataset         Model              LS          PE     LN-PE         SE       TOKEN SAR        SENTSAR           SAR
                  OPT-2.7b          0.573     0.666      0.719       0.712          0.719         0.689           0.742
                  OPT-6.7b          0.588     0.671      0.745       0.741          0.746         0.696           0.768
                  OPT-13b           0.588     0.666      0.750       0.751          0.752         0.690           0.773
  CoQA
                  OPT-30b           0.550     0.671      0.742       0.751          0.746         0.698           0.767
                  LLaMA-7b          0.511     0.646      0.673       0.672          0.672         0.635           0.686
                  LLaMA-13b         0.522     0.617      0.653       0.652          0.653         0.610           0.665
                  LLaMA-7b          0.533     0.713      0.783       0.814          0.793         0.800           0.818
  Trivia QA
                  LLaMA-13b         0.655     0.492      0.627       0.758          0.635         0.749           0.716
            Average                 0.565     0.643      0.712       0.731          0.715         0.696           0.742

Table 6: Uncertainty estimation AUROCs of TOKENSAR, SENTSAR, SAR, and baseline methods, across various
“off-the-shelf” LLMs and datasets (e.g., CoQA, and Trivia QA). Rouge-L with a threshold of 0.3 is used as the
correctness metric.

  Method      Num. of Generations   Generation    Logits Computing   Semantic Clustering    Sentence Similarity    Sum
  PE                  5               4.09s            1.19s                  0s                    0s             5.28s
  LN-PE               5               4.09s            1.19s                  0s                    0s             5.28s
  SE                  5               4.09s            1.19s                 1.5s                   0s             6.78s
  SENTSAR             5               4.09s            1.19s                 0s                   2.58s            7.86s
  SENTSAR             2               1.64s            0.48s                 0s                   0.52s            2.64s

 Table 7: Computational costs of SAR and baseline methods. We report both SENTSAR with 5 and 2 generations.

```
