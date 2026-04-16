---
citation_key: "TianEtAl2023"
title: "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback"
authors: "Katherine Tian; Eric Mitchell; Allan Zhou; Archit Sharma; Rafael Rafailov; Huaxiu Yao; Chelsea Finn; Christopher D. Manning"
year: 2023
doi: "10.48550/arxiv.2305.14975"
source: "local PDF (Katherine2023.pdf)"
access_level: "full-text-pdf"
retrieved_date: "2026-04-15"
arxiv_id: "2305.14975"
is_user_seed: true
tier: 1
composite_score: 4.7
---
# Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
**Authors**: Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, Christopher D. Manning
**Year**: 2023
**Venue**: arXiv (Cornell University)
**DOI**: [10.48550/arxiv.2305.14975](https://doi.org/10.48550/arxiv.2305.14975)

## Full Text (extracted via pdftotext) / 全文（pdftotext 抽取）

```text
                                             Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence
                                               Scores from Language Models Fine-Tuned with Human Feedback
                                                     Katherine Tian,∗† Eric Mitchell,∗‡ Allan Zhou,‡ Archit Sharma,‡ Rafael Rafailov‡
                                                                 Huaxiu Yao,‡ Chelsea Finn,‡ Christopher D. Manning‡
                                                                             †
                                                                                 Harvard University ‡ Stanford University
                                                                                     ktian@college.harvard.edu
                                                                                   eric.mitchell@cs.stanford.edu

                                                                   Abstract
                                                 A trustworthy real-world prediction system
                                                 should produce well-calibrated confidence
                                                 scores; that is, its confidence in an answer

arXiv:2305.14975v2 [cs.CL] 24 Oct 2023
                                                 should be indicative of the likelihood that the
                                                 answer is correct, enabling deferral to an expert
                                                 in cases of low-confidence predictions. Re-
                                                 cent studies have shown that unsupervised pre-
                                                 training produces large language models (LMs)
                                                 whose conditional probabilities are remarkably
                                                 well-calibrated. However, the most widely-
                                                 used LMs are fine-tuned with reinforcement
                                                 learning from human feedback (RLHF-LMs),
                                                 and some studies have suggested that RLHF-                 Figure 1: Verbalized confidence scores (blue) are
                                                 LMs produce conditional probabilities that are             better-calibrated than log probabilities (orange) for
                                                 very poorly calibrated. In light of this perceived         gpt-3.5-turbo. Raw model probabilities (top-left) are con-
                                                 weakness, we conduct a broad evaluation of                 sistently over-confident. Verbalized numerical probabilities
                                                 methods for extracting confidence scores from              (bottom) are better-calibrated. Considering more answer
                                                                                                            choices (bottom-right) further improves verbalized calibra-
                                                 RLHF-LMs. For RLHF-LMs such as ChatGPT,                    tion (as in ‘Considering the Opposite’ in psychology; Lord
                                                 GPT-4, and Claude, we find that verbalized                 et al. (1985)). Verbalized expressions of likelihood (top-right)
                                                 confidences emitted as output tokens are typi-             also provide improved calibration. Bar height is average accu-
                                                 cally better-calibrated than the model’s condi-            racy of predictions in bin. Darker bars mean more predictions
                                                 tional probabilities on the TriviaQA, SciQ, and            fall in that confidence range. Results computed on SciQ.
                                                 TruthfulQA benchmarks, often reducing the ex-
                                                 pected calibration error by a relative 50%.                attention (Brown et al., 2020; Roberts et al., 2020;
                                                                                                            Bubeck et al., 2023), relatively little attention has
                                         1       Introduction                                               been given to their well-calibratedness (Kadavath
                                                                                                            et al., 2022). Further, most existing analyses of the
                                         Real-world prediction systems invariably make er-
                                                                                                            calibratedness of LLMs focus on models trained
                                         rors. However, some mitigation of these errors is
                                                                                                            with maximum likelihood, while in practice, the
                                         possible if the system produces well-calibrated1
                                                                                                            most widely-used LLMs (such as ChatGPT) are
                                         confidence estimates. In this case, the system’s
                                                                                                            fine-tuned using methods such as reinforcement
                                         least confident predictions correspond to those that
                                                                                                            learning from human feedback (Christiano et al.,
                                         are most likely to be incorrect, potentially allowing
                                                                                                            2017). Some findings suggest that RLHF-LMs may
                                         these predictions to be skipped or overridden by
                                                                                                            sacrifice well-calibrated predictions for the sake of
                                         a human. In the context of language models, one
                                                                                                            closer adherence to user instructions in dialogue
                                         consequence of poor calibration may be hallucina-
                                                                                                            (Kadavath et al., 2022; OpenAI, 2023), as the rein-
                                         tion, where a language model confidently asserts
                                                                                                            forcement learning objective encourages the model
                                         incorrect facts or reasoning. While the ability of
                                                                                                            to allocate probability mass to the most preferred
                                         very large LMs to absorb and synthesize knowl-
                                                                                                            answer(s), rather than matching the relative fre-
                                         edge about the outside world has gained significant
                                                                                                            quency of possible answers.
                                                 ∗
                                               Equal contribution.
                                             i.e., the confidence in a prediction accurately reflects the      This paper evaluates several methods for ex-
                                         probability that the prediction is correct (Guo et al., 2017).     tracting confidences about model predictions from
                                       ECE Comparison ( )                               AUC Comparison ( )
                         0.40                                              1.0
                                                                                                          Pre-RLHF    calibrated predictions (Kadavath et al., 2022; Xiao
                         0.35                                                                             Post-RLHF
                                                                           0.8                                        et al., 2022; Kuhn et al., 2023). Other work focuses

Temperature-scaled ECE
                         0.30
                         0.25                                              0.6                                        on the tendency of language and dialogue models
                         0.20                                        AUC
                         0.15                                              0.4                                        to use linguistic expressions of uncertainty in a
                         0.10
                                                                           0.2                                        well-calibrated manner (Zhou et al., 2023; Mielke
                         0.05
                         0.00                                              0.0
                                                                                                                      et al., 2022). However, existing studies focus on
                                TriviaQA      SciQ      TruthfulQA               TriviaQA      SciQ      TruthfulQA
                                                                                                                      LMs trained purely with unsupervised learning
 Figure 2: RLHF generally worsens the calibration of                                                                  (although Kadavath et al. (2022) briefly examine
 Llama-70B’s log probabilities, as measured by ECE (lower
 is better) or AUC (higher is better). However, this paper (Ta-
                                                                                                                      RLHF-LMs), while widely used models in prac-
 bles 1-5) will show that for several strong RLHF-LMs, the                                                            tice are fine-tuned with instruction-tuning or RLHF
 model’s verbalized confidence is often better-calibrated than                                                        (Christiano et al., 2017). RLHF has been shown
 its log probabilities, reversing some of this degradation. This
 reversal is strongest for TruthfulQA, an adversarial dataset                                                         to effectively leverage annotations of human pref-
 testing common misconceptions and other difficult queries.                                                           erences to control sentiment (Ziegler et al., 2020),
                                                                                                                      improve summarization or instruction-following
                                                                                                                      quality (Stiennon et al., 2022; Ouyang et al., 2022),
RLHF-LMs. Due to concerns that RLHF may
                                                                                                                      and inject behavioral priors of harmlessness (Bai
cause systematic overconfidence in the model’s
                                                                                                                      et al., 2022b,a). However, recent work has raised
probabilities (Figure 2), as well as the general un-
                                                                                                                      the question of whether or not RLHF harms cali-
availability of per-token log-probabilities in widely
                                                                                                                      bration (OpenAI, 2023). Our work is the first to
used RLHF-LMs, we pay particular attention to
                                                                                                                      show that verbalized probabilities are often better-
prompts that elicit verbalized probabilities, i.e., the
                                                                                                                      calibrated than the model’s conditional probabili-
model expresses its confidence in token-space, as
                                                                                                                      ties for RLHF-LMs such as ChatGPT, GPT-4, and
either numerical probabilities or another linguistic
                                                                                                                      Claude, and Llama-2-70B-Chat.
expression of uncertainty. We find that, surpris-
ingly, popular RLHF-LMs are able to directly ver-
                                                                                                                      2    Evaluating Calibration in RLHF-LMs
balize confidence scores that are better-calibrated
than the model’s conditional probabilities (esti-                                                                     To study the calibration of RLHF-LMs, we con-
mated via sampling), without any fine-tuning to                                                                       duct experiments with gpt-3.5-turbo (ChatGPT),
learn verbalization. To further improve calibration,                                                                  gpt-4 (GPT-4), claude-1 (Claude 1), claude-2
we take inspiration from research in human psy-                                                                       (Claude 2), and Llama-2-70b-chat (Llama-2-
chology showing that overconfidence can be mit-                                                                       70B-Chat).
igated by considering alternative answers before
responding (Lord et al., 1985; Mussweiler et al.,                                                                     Metrics. We measure calibration with multiple
2000). We show that prompting a model to produce                                                                      metrics. To measure ECE (expected calibration er-
several answer choices before giving its confidence                                                                   ror; Guo et al. (2017)), we bin model predictions by
scores significantly improves calibration of ver-                                                                     their confidence and measure the average accuracy
balized probabilities. Combined with temperature                                                                      of predictions in each confidence bin. The ECE
scaling (Guo et al., 2017), this approach generally                                                                   is defined as the average (squared) error between
provides better calibration than model probabilities                                                                  the average accuracy and confidence within each
for ChatGPT2 , GPT-43 , and Claude 24 across three                                                                    bin, where each error is weighted by the fraction of
datasets, often reducing expected calibration error                                                                   samples falling within the bin. We report raw ECE
(ECE) by over 50%.                                                                                                    as well as ECE with temperature scaling (ECE-t).
                                                                                                                      Temperature scaling fits a single temperature value
Related Work. Several studies have examined                                                                           β to the model’s confidences to minimize negative
the calibration of large LMs (Lin et al., 2022a;                                                                      log likelihood (NLL) on the data, giving scaled
Park and Caragea, 2022; Kadavath et al., 2022;                                                                        probability p̃i of class i as p̃i ∝ pβi . See Figure 1
Xiao et al., 2022; Kuhn et al., 2023), finding that                                                                   for a depiction of ECE binning. Although ECE is a
combining large pre-trained LMs with tempera-                                                                         standard and interpretable measure of calibration
ture scaling (Guo et al., 2017) produces very well-                                                                   error, it completely fails to capture the confidences’
      gpt-3.5-turbo, accessed in June 2023.                                                                           discriminative power.5 We therefore also report
      https://cdn.openai.com/papers/gpt-4-system-card.pdf
    4                                                                                                                    5
      https://www-files.anthropic.com/production/images/Model-                                                             For binary classification, a system that guesses randomly
 Card-Claude-2.pdf                                                                                                    and outputs 50% confidence each time has perfect ECE.
                               TriviaQA                                  SciQ                              TruthfulQA
 Method            ECE ↓   ECE-t ↓    BS-t ↓   AUC ↑     ECE ↓    ECE-t ↓   BS-t ↓      AUC ↑   ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑
 Label prob.       0.140     0.097    0.142    0.869      0.256     0.180       0.223   0.752    0.451    0.317     0.345   0.418
 ‘Is True’ prob.   0.164     0.159    0.165    0.826      0.312     0.309       0.309   0.677    0.470    0.471     0.476   0.384
 Entropy            —         —        —       0.547       —         —           —      0.483     —         —        —      0.236
 Verb. 1S top-1    0.068     0.076    0.138    0.879      0.234     0.084       0.214   0.744    0.389    0.256     0.322   0.545
 Verb. 1S top-2    0.050     0.053    0.139    0.894      0.132     0.050       0.201   0.766    0.361    0.115     0.252   0.485
 Verb. 1S top-4    0.054     0.057    0.144    0.896      0.065     0.051       0.209   0.763    0.203    0.189     0.284   0.455
 Verb. 2S CoT      0.110     0.123    0.168    0.830      0.323     0.246       0.296   0.683    0.419    0.259     0.292   0.551
 Verb. 2S top-1    0.131     0.099    0.148    0.855      0.340     0.203       0.268   0.677    0.431    0.245     0.282   0.483
 Verb. 2S top-2    0.047     0.045    0.147    0.887      0.169     0.040       0.201   0.768    0.395    0.101     0.224   0.517
 Verb. 2S top-4    0.050     0.051    0.156    0.861      0.130     0.046       0.211   0.729    0.270    0.156     0.246   0.463
 Ling. 1S human    0.062     0.069    0.137    0.884      0.166     0.087       0.223   0.703    0.306    0.296     0.333   0.503
 Ling. 1S-opt.     0.058     0.066    0.135    0.878      0.064     0.068       0.220   0.674    0.125    0.165     0.270   0.492

Table 1: Measuring calibration of various methods for extracting confidences from gpt-3.5-turbo (ChatGPT). The model’s
conditional probabilities are relatively poorly calibrated, whether using the model’s conditional probability of the label given the
query (Label prob.) or the probability assigned to ‘True’ given the query, proposed answer, and a prompt asking if the answer is
correct (‘Is True’ prob.). Surprisingly, directly verbalizing a probability (Verb. 1S and Verb. 2S) or an expression of confidence
such as ‘highly likely’ (Ling. 1S) yields significantly better-calibrated confidence estimates. 1S refers to one-stage prediction,
where the model provides an answer and confidence probability/expression together. 2S refers to two-stage prediction, where the
model first gives only an answer, and then in a second stage a confidence. To color the table cells, for each column, we demean
and scale by a constant to obtain a shade in [-1,1], where cyan indicates better and orange worse performance.

                               TriviaQA                                  SciQ                              TruthfulQA
 Method            ECE ↓   ECE-t ↓    BS-t ↓   AUC ↑     ECE ↓    ECE-t ↓   BS-t ↓      AUC ↑   ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑
 Label prob.       0.078     0.067    0.077    0.950      0.219     0.165       0.186   0.820    0.445    0.334     0.362   0.462
 Verb. 1S top-1    0.024     0.038    0.084    0.937      0.201     0.084       0.165   0.843    0.350    0.156     0.227   0.622
 Verb. 1S top-2    0.025     0.034    0.084    0.949      0.140     0.048       0.185   0.813    0.315    0.112     0.228   0.623
 Verb. 1S top-4    0.041     0.039    0.081    0.959      0.056     0.059       0.185   0.815    0.198    0.144     0.245   0.619
 Ling. 1S-human    0.051     0.041    0.086    0.931      0.148     0.024       0.170   0.835    0.241    0.151     0.228   0.651
 Ling. 1S-opt.     0.056     0.051    0.088    0.927      0.028     0.052       0.172   0.828    0.082    0.105     0.212   0.632

Table 2: gpt-4’s verbalized probabilities are substantially better-calibrated than the model probabilities themselves, even after
temperature scaling, similarly to gpt-3.5-turbo in Table 1.

Brier Score (BS; Brier (1950)) on temperature-                      Evaluation protocol. For each dataset, we gener-
scaled confidences (BS-t), a proper scoring rule                    ate a response and corresponding confidence from
(Ovadia et al., 2019) that is the mean squared error                each method on each of the evaluation questions.
between the confidences and the correctness labels.                 Because calibration essentially quantifies the re-
Finally, we assess calibration using a metric from                  lationship between model confidence and correct-
the selective classification literature (Geifman and                ness, computing correctness is crucial to accurate
El-Yaniv, 2017), specifically, the area under the                   measurements of calibration. However, we find
curve of selective accuracy and coverage (AUC).                     doing so to be a challenge, especially in datasets
                                                                    where only a single ground-truth answer (but not
                                                                    aliases or semantically equivalent rephrases) is pro-
Datasets. Our experiments use three question-                       vided. To avoid excessive false negatives in our
answering datasets assessing factual knowledge.                     correctness computation as a result of exact-match
TriviaQA (Joshi et al., 2017) contains 650k                         evaluation, we use either GPT-4 or GPT-3.5 to eval-
question-answer pairs gathered by trivia enthusi-                   uate whether a response is essentially equivalent to
asts; SciQ (Welbl et al., 2017) contains approxi-                   the ground truth answer; see Appendix C for the
mately 14k crowdsourced science exam question-                      complete equivalence-checking procedure.
answer pairs; TruthfulQA (Lin et al., 2022b) con-
tains 817 questions designed to test language mod-                  Methods. We compare a wide variety of methods
els’ tendency to mimic human falsehoods. We                         for extracting confidence estimates from LLMs.
sample 1000 questions from the validation split of                  For a comprehensive list of the prompts used for
TriviaQA (rc.web.nocontext) and SciQ and all                        each method, see Appendix Table 6.
817 questions from the validation split of Truth-                      First, we consider two methods that leverage the
fulQA (generation) for our experiments.                             true conditional distribution of the model to gener-
                              TriviaQA                                 SciQ                               TruthfulQA
 Method           ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑      ECE ↓   ECE-t ↓     BS-t ↓   AUC ↑    ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑
 Label prob.       0.074    0.079     0.117   0.915      0.216     0.149      0.195   0.786     0.432    0.304    0.335    0.418
 Verb. 1S top-1    0.049    0.059     0.160   0.839      0.265     0.103      0.247   0.663     0.440    0.134    0.204    0.411
 Verb. 1S top-2    0.046    0.047     0.158   0.875      0.207     0.040      0.225   0.693     0.450    0.085    0.197    0.409
 Verb. 1S top-4    0.075    0.079     0.176   0.814      0.151     0.057      0.226   0.667     0.372    0.105    0.183    0.377
 Ling. 1S human    0.053    0.050     0.151   0.867      0.253     0.118      0.245   0.664     0.443    0.358    0.340    0.384
 Ling. 1S-opt.     0.074    0.060     0.149   0.863      0.089     0.082      0.238   0.623     0.139    0.148    0.228    0.350

Table 3: Claude-1 produces similar- or better-calibrated log probabilities to gpt-3.5-turbo, but is less able to verbalize
well-calibrated confidences, compared to models in the GPT family of RLHF-LMs. Claude-1 has since been deprecated.
                              TriviaQA                                 SciQ                               TruthfulQA
 Method           ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑      ECE ↓   ECE-t ↓     BS-t ↓   AUC ↑    ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑
 Label prob.       0.089    0.089     0.137   0.882      0.181     0.176      0.237   0.762     0.409    0.368    0.405    0.319
 Verb. 1S top-1    0.072    0.071     0.141   0.903      0.204     0.054      0.201   0.776     0.345    0.115    0.215    0.573
 Verb. 1S top-2    0.049    0.054     0.133   0.918      0.134     0.041      0.211   0.754     0.359    0.085    0.223    0.491
 Verb. 1S top-4    0.072    0.063     0.158   0.890      0.048     0.052      0.216   0.711     0.274    0.075    0.208    0.473
 Ling. 1S human    0.085    0.061     0.151   0.878      0.238     0.026      0.209   0.756     0.381    0.242    0.305    0.530
 Ling. 1S-opt.     0.060    0.070     0.151   0.874      0.049     0.056      0.214   0.738     0.099    0.130    0.266    0.446

Table 4: Claude-2 has weaker conditional probabilities than Claude-1 and GPT-*, but its verbalized calibration provides consistent
improvement over conditional probabilities at a level comparable to GPT-3.5 and surpassing GPT-* on TruthfulQA.

ate confidence scores. The simplest is Label prob.,                sociated probability as the model’s output and con-
which uses the conditional probability distribution                fidence. Verb. 2S top-k similarly uses numeri-
p(y|x) of the model given a question x, which we                   cal probabilities, except the model is first asked
estimate using n = 10 samples, since many RLHF-                    to provide only its answers, and afterwards, in a
LMs are closed-source and do not offer per-token                   second round of dialogue, asked to assign prob-
probabilities.67 We return the most common an-                     abilities of correctness to each answer (i.e., ‘2
swer, using the LLM-based equivalence function                     stages’). Verb. 2S CoT uses a chain-of-thought
to determine when two lexically different answers                  prompt before giving a single answer, and in a
are semantically equivalent. In a variation of the                 second round of dialogue, the model is prompted
method described by Kadavath et al. (2022) (again,                 to assign a probability to that answer (with the
we use samples since model probabilities are not                   chain of thought present in the model’s context).
available), ‘Is True’ prob. samples a single answer                Ling. 1S-human uses linguistic likelihood expres-
ŷ from the model given a question x, and the prob-                sions, rather than numerical probabilities, to ex-
ability it is true is estimated by the probability the             press uncertainty. The model is prompted to assign
model assigns to ‘True’ when asked if the given                    confidences to its guesses by choosing from a set
answer is true (where once again the probabilities                 of linguistic expressions of uncertainty: {Almost
are estimated via samples), i.e., p(True|x, ŷ).                   certain, Likely, . . . , Almost no chance}. Each
    Next, we consider methods that extract con-                    linguistic likelihood expression is mapped to a
fidence scores through verbalization (Lin et al.,                  probability using responses from a human sur-
2022a), i.e., where the model expresses its confi-                 vey on social media with 123 respondents (Fagen-
dence in token space, either with numerical prob-                  Ulmschneider, 2023). Ling. 1S-opt. uses a held
abilities or linguistic expressions of likelihood.8                out set of calibration questions and answers to com-
First, Verb. 1S top-k prompts the model to pro-                    pute the average accuracy for each likelihood ex-
duce k guesses and a probability that each is cor-                 pression, using these ‘optimized’ values instead.
rect all in a single response (i.e., ‘1 stage’). We                Expressions that are not used for at least N1 of
take the highest-probability prediction and its as-                questions, where N is the number of calibration
      We evaluated gpt-3.5-turbo on all three datasets using
                                                                   questions, simply use the human probability.
n = 20 samples, but the calibration did not meaningfully
improve, so we always use n = 10 to reduce API costs.
                                                                   3       Results
      For each closed LM, we use its default sampling param-
eters (top-p 1.0 for GPT-* and top-p 0.7 for Claude). For          Tables 1–5 show the results of evaluating various
Llama-2, we use temperature 1.0 and top-p 1.0.
      However, note that none of the methods described fine-       methods for extracting confidence from RLHF-
tune the model to perform better on verbalization.                 LMs on gpt-3.5-turbo, gpt-4, claude-1,
                             TriviaQA                                SciQ                             TruthfulQA
 Method           ECE ↓   ECE-t ↓   BS-t ↓   AUC ↑     ECE ↓   ECE-t ↓   BS-t ↓     AUC ↑   ECE ↓    ECE-t ↓   BS-t ↓   AUC ↑
 Label prob.      0.151    0.124    0.156    0.865     0.266     0.189      0.243   0.707    0.405    0.361    0.396    0.407
 Verb. 1S top-1   0.071    0.067    0.186    0.793     0.196     0.053      0.239   0.648    0.386    0.172    0.266    0.502
 Verb. 1S top-2   0.060    0.073    0.194    0.815     0.153     0.032      0.230   0.667    0.340    0.037    0.227    0.440
 Verb. 1S top-4   0.069    0.079    0.182    0.816     0.105     0.043      0.229   0.648    0.231    0.102    0.237    0.465
 Ling. 1S human   0.179    0.115    0.195    0.749     0.071     0.101      0.252   0.603    0.376    0.366    0.383    0.407
 Ling. 1S-opt.    0.077    0.068    0.186    0.779     0.019     0.042      0.236   0.590    0.047    0.051    0.239    0.435

Table 5: With Llama2-70B-Chat, verbalized calibration provides improvement over conditional probabilities across some metrics,
but the improvement is much less consistent compared to GPT-* and Claude-*.

claude-2, and Llama-2-70b-chat, respectively.                    elicit calibrated confidences from RLHF-LMs by
We distill several key conclusions from these exper-             prompting the model to verbalize its confidence
iments. 1. Large RLHF-LMs can often directly                     in token space. We find verbalized probabilities
verbalize better-calibrated confidences (either a                are better-calibrated than conditional probabilities
numerical confidence probability or an expres-                   across several closed models, with mixed results
sion such as ‘highly likely’) than the models’                   for Llama-2-70B-Chat.
conditional probabilities. 2. Among the methods
                                                                    Our results raise several questions for future
for verbalizing probabilities directly, we observe
                                                                 work. Most notably, the difference between GPT-*,
that generating and evaluating multiple hypothe-
                                                                 Claude-*, and Llama-2’s ability to verbalize confi-
ses improves calibration (see Figure 1), similarly
                                                                 dence is significant. What factors are important for
to humans (Lord et al., 1985), and corroborating
                                                                 learning this skill? Additionally, the 1-stage and
a similar finding in LMs (Kadavath et al., 2022).
                                                                 2-stage verbalized numerical confidence prompts
3. Language models can express their uncertainty
                                                                 sometimes differ drastically in the calibration of
with numerical probabilities as well or better than
                                                                 their confidences. How can we reduce sensitivity of
with words, which is surprising in light of long-
                                                                 a model’s calibration to the prompt? Going beyond
standing difficulties in representing numbers in lan-
                                                                 question-answering, can we leverage good calibra-
guage models (Thawani et al., 2021). 4. Chain-
                                                                 tion in short-answer settings to improve the reliabil-
of-thought prompting does not improve verbalized
                                                                 ity of long-form generations, perhaps by breaking
calibration (see Appendix Figure 5 for additional
                                                                 down long-form generation into a sequence of short
CoT results). 5. The calibration of both Claude
                                                                 questions? Finally, to what extent does a language
models’ conditional probabilities roughly falls be-
                                                                 model’s calibration depend on the domain; do our
tween gpt-3.5-turbo and gpt-4; however, while
                                                                 conclusions in the context of factual recall hold in
Claude 1 is much weaker at verbalizing its con-
                                                                 the context of reasoning or arithmetic? Answering
fidence, Claude 2 is generally a bit stronger than
                                                                 these questions provides one path toward building
gpt-3.5-turbo at verbalizing. The verbal calibra-
                                                                 more trustworthy and useful language systems.
tion of the open source model Llama-2-70b-chat
is generally weaker than that of closed source mod-              Limitations. While our work demonstrates a
els but still demonstrates improvement over its con-             promising new approach to generating calibrated
ditional probabilities by some metrics, and does so              confidences through verbalization, there are lim-
most clearly on TruthfulQA.                                      itations that could be addressed in future work.
                                                                 First, our experiments are focused on factual recall-
4    Discussion                                                  oriented problems, and the extent to which our ob-
                                                                 servations would hold for reasoning-heavy settings
In summary, we study the calibration of widely                   is an interesting open question. Additionally, the
used RLHF-LMs. We first replicate the finding for                lack of technical details available for many state-of-
GPT-4 (OpenAI, 2023) that RLHF can worsen the                    the-art closed RLHF-LMs may limit our ability to
calibration of a model’s conditional probabilities               understand what factors enable a model to verbalize
using the open-source Llama-2-70B base and chat                  well-calibrated confidences and differences in this
models (Figure 2). To mitigate this regression and               ability across different models. Finally, our study
ease extraction of calibrated confidence scores for              is limited to short-form question-answering; future
models for which log probabilities are not avail-                work should extend this analysis to longer-form
able, we propose and study new methods that can                  generation settings.
Acknowledgements. CF and CDM are CIFAR Fel-              Sébastien Bubeck, Varun Chandrasekaran, Ronen El-
lows. EM gratefully acknowledges funding from              dan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Pe-
                                                           ter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg,
a Knight-Hennessy Graduate Fellowship. AZ is
                                                           Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro,
supported by the NSF graduate research fellowship          and Yi Zhang. 2023. Sparks of artificial general in-
program. This research was supported in part by            telligence: Early experiments with GPT-4. ArXiv
Juniper Networks, Apple, and ONR grant N00014-             preprint arXiv:2303.12712.
20-1-2675. The authors thank Yoonho Lee and              Paul F Christiano, Jan Leike, Tom Brown, Miljan Mar-
Noah Goodman for helpful feedback on calibration           tic, Shane Legg, and Dario Amodei. 2017. Deep
metrics and experiment design.                             reinforcement learning from human preferences. In
                                                           Advances in Neural Information Processing Systems,
                                                           volume 30. Curran Associates, Inc.
References
                                                         Wade Fagen-Ulmschneider. 2023. Perception of proba-
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda              bility words. Ms., UIUC, 05-24-2023.
  Askell, Anna Chen, Nova DasSarma, Dawn Drain,
  Stanislav Fort, Deep Ganguli, Tom Henighan,            Yonatan Geifman and Ran El-Yaniv. 2017. Selective
  Nicholas Joseph, Saurav Kadavath, Jackson Kernion,       classification for deep neural networks. In Proceed-
  Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac          ings of the 31st International Conference on Neu-
  Hatfield-Dodds, Danny Hernandez, Tristan Hume,           ral Information Processing Systems, NIPS’17, page
  Scott Johnston, Shauna Kravec, Liane Lovitt, Neel        4885–4894, Red Hook, NY, USA. Curran Associates
  Nanda, Catherine Olsson, Dario Amodei, Tom               Inc.
  Brown, Jack Clark, Sam McCandlish, Chris Olah,
  Ben Mann, and Jared Kaplan. 2022a. Training a          Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Wein-
  helpful and harmless assistant with reinforcement        berger. 2017. On calibration of modern neural net-
  learning from human feedback.                            works. In Proceedings of the 34th International Con-
                                                           ference on Machine Learning, volume 70 of Pro-
Yuntao Bai, Saurav Kadavath, Sandipan Kundu,               ceedings of Machine Learning Research, pages 1321–
  Amanda Askell, Jackson Kernion, Andy Jones, Anna         1330. PMLR.
  Chen, Anna Goldie, Azalia Mirhoseini, Cameron
  McKinnon, Carol Chen, Catherine Olsson, Christo-       Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke
  pher Olah, Danny Hernandez, Dawn Drain, Deep            Zettlemoyer. 2017. TriviaQA: A large scale distantly
  Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez,      supervised challenge dataset for reading comprehen-
  Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua       sion. In Proceedings of the 55th Annual Meeting of
  Landau, Kamal Ndousse, Kamile Lukosuite, Liane          the Association for Computational Linguistics (Vol-
  Lovitt, Michael Sellitto, Nelson Elhage, Nicholas       ume 1: Long Papers), pages 1601–1611, Vancouver,
  Schiefer, Noemi Mercado, Nova DasSarma, Robert          Canada. Association for Computational Linguistics.
  Lasenby, Robin Larson, Sam Ringer, Scott John-
  ston, Shauna Kravec, Sheer El Showk, Stanislav Fort,   Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
  Tamera Lanham, Timothy Telleen-Lawton, Tom Con-          Henighan, Dawn Drain, Ethan Perez, Nicholas
  erly, Tom Henighan, Tristan Hume, Samuel R. Bow-         Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
  man, Zac Hatfield-Dodds, Ben Mann, Dario Amodei,         Tran-Johnson, Scott Johnston, Sheer El-Showk,
  Nicholas Joseph, Sam McCandlish, Tom Brown, and          Andy Jones, Nelson Elhage, Tristan Hume, Anna
  Jared Kaplan. 2022b. Constitutional AI: Harmless-        Chen, Yuntao Bai, Sam Bowman, Stanislav Fort,
  ness from ai feedback.                                   Deep Ganguli, Danny Hernandez, Josh Jacobson,
                                                           Jackson Kernion, Shauna Kravec, Liane Lovitt, Ka-
Glenn W. Brier. 1950. Verification of Forecasts Ex-        mal Ndousse, Catherine Olsson, Sam Ringer, Dario
  pressed in Terms of Probability. Monthly Weather         Amodei, Tom Brown, Jack Clark, Nicholas Joseph,
  Review, 78(1):1–3.                                       Ben Mann, Sam McCandlish, Chris Olah, and Jared
                                                           Kaplan. 2022. Language models (mostly) know what
Tom Brown, Benjamin Mann, Nick Ryder, Melanie              they know. Arxiv arxiv:2207.05221.
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda       Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,            Semantic uncertainty: Linguistic invariances for un-
  Gretchen Krueger, Tom Henighan, Rewon Child,             certainty estimation in natural language generation.
  Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens       In The Eleventh International Conference on Learn-
  Winter, Chris Hesse, Mark Chen, Eric Sigler, Ma-         ing Representations.
  teusz Litwin, Scott Gray, Benjamin Chess, Jack
  Clark, Christopher Berner, Sam McCandlish, Alec        Stephanie Lin, Jacob Hilton, and Owain Evans. 2022a.
  Radford, Ilya Sutskever, and Dario Amodei. 2020.         Teaching models to express their uncertainty in
  Language models are few-shot learners. In Ad-            words. Transactions on Machine Learning Research.
  vances in Neural Information Processing Systems,
  volume 33, pages 1877–1901. Curran Associates,         Stephanie Lin, Jacob Hilton, and Owain Evans. 2022b.
  Inc.                                                      TruthfulQA: Measuring how models mimic human
  falsehoods. In Proceedings of the 60th Annual Meet-     Avijit Thawani, Jay Pujara, Filip Ilievski, and Pedro
  ing of the Association for Computational Linguistics      Szekely. 2021. Representing numbers in NLP: a
  (Volume 1: Long Papers), pages 3214–3252, Dublin,         survey and a vision. In Proceedings of the 2021
  Ireland. Association for Computational Linguistics.       Conference of the North American Chapter of the
                                                            Association for Computational Linguistics: Human
Charles Lord, Mark Lepper, and Elizabeth Preston.           Language Technologies, pages 644–656, Online. As-
  1985. Considering the opposite: A corrective strat-       sociation for Computational Linguistics.
  egy for social judgment. Journal of personality and
  social psychology, 47:1231–43.                          Johannes Welbl, Nelson F. Liu, and Matt Gardner. 2017.
                                                            Crowdsourcing multiple choice science questions.
Sabrina J. Mielke, Arthur Szlam, Emily Dinan, and Y-        ArXiv, abs/1707.06209.
  Lan Boureau. 2022. Reducing conversational agents’      Yuxin Xiao, Paul Pu Liang, Umang Bhatt, Willie
  overconfidence through linguistic calibration. Trans-     Neiswanger, Ruslan Salakhutdinov, and Louis-
  actions of the Association for Computational Linguis-     Philippe Morency. 2022. Uncertainty quantification
  tics, 10:857–872.                                         with pre-trained language models: A large-scale em-
                                                            pirical analysis. In Findings of the Association for
Thomas Mussweiler, Fritz Strack, and Tim Pfeiffer.          Computational Linguistics: EMNLP 2022, pages
  2000. Overcoming the inevitable anchoring effect:         7273–7284, Abu Dhabi, United Arab Emirates. As-
  Considering the opposite compensates for selective        sociation for Computational Linguistics.
  accessibility. Personality and Social Psychology Bul-
  letin, 26(9):1142–1150.                                 Kaitlyn Zhou, Dan Jurafsky, and Tatsunori Hashimoto.
                                                            2023. Navigating the grey area: Expressions of over-
OpenAI. 2023. Gpt-4 technical report.                       confidence and uncertainty in language models.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,         Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B.
  Carroll Wainwright, Pamela Mishkin, Chong Zhang,          Brown, Alec Radford, Dario Amodei, Paul Chris-
  Sandhini Agarwal, Katarina Slama, Alex Ray, John          tiano, and Geoffrey Irving. 2020. Fine-tuning lan-
  Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,       guage models from human preferences.
  Maddie Simens, Amanda Askell, Peter Welinder,
  Paul F Christiano, Jan Leike, and Ryan Lowe. 2022.
  Training language models to follow instructions with
  human feedback. In Advances in Neural Information
  Processing Systems, volume 35, pages 27730–27744.
  Curran Associates, Inc.

Yaniv Ovadia, Emily Fertig, Jie Ren, Zachary Nado,
  D. Sculley, Sebastian Nowozin, Joshua V. Dillon,
  Balaji Lakshminarayanan, and Jasper Snoek. 2019.
  Can you trust your model’s uncertainty? evaluating
  predictive uncertainty under dataset shift. In Pro-
  ceedings of the 33rd International Conference on
  Neural Information Processing Systems, Red Hook,
  NY, USA. Curran Associates Inc.

Seo Yeon Park and Cornelia Caragea. 2022. On the cal-
  ibration of pre-trained language models using mixup
  guided by area under the margin and saliency. In
  Proceedings of the 60th Annual Meeting of the As-
  sociation for Computational Linguistics (Volume 1:
  Long Papers), pages 5364–5374, Dublin, Ireland. As-
  sociation for Computational Linguistics.

Adam Roberts, Colin Raffel, and Noam Shazeer. 2020.
  How much knowledge can you pack into the param-
  eters of a language model? In Proceedings of the
  2020 Conference on Empirical Methods in Natural
  Language Processing (EMNLP), pages 5418–5426,
  Online. Association for Computational Linguistics.

Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M.
  Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
  Dario Amodei, and Paul Christiano. 2022. Learning
  to summarize from human feedback.
                                            Usage of likelihood expressions by 3.5-turbo
                         0.40                                   TriviaQA

 Fraction of Responses
                         0.35                                   SciQ
                                                                TruthfulQA
                         0.30
                         0.25
                         0.20
                         0.15
                         0.10
                         0.05
                         0.00

                                                  Almost No Chance
                                                                          Highly Unlikely
                                                                                                   Chances are Slight
                                                                                                                             Little Chance
                                                                                                                                               Unlikely
                                                                                                                                                           Probably Not     About Even
                                                                                                                                                                                                Better than Even
                                                                                                                                                                                                                   Likely
                                                                                                                                                                                                                              Probably

                                                                                                                                                                                                                                                 Very Good Chance
                                                                                                                                                                                                                                                                         Highly Likely
                                                                                                                                                                                                                                                                                              Almost Certain

                                                                                                                                Likelihood Expression

Figure 3: gpt-3.5-turbo usage rate of each likelihood ex-
pression; the model displays much lower verbalized confi-
dence on TruthfulQA than on standard factual recall problems.
                                                       Usage of likelihood expressions by GPT-4
                                                                         TriviaQA

                    Fraction of Responses
                                            0.4                          SciQ
                                                                         TruthfulQA
                                            0.3

                                            0.2

                                            0.1

                                            0.0

                                                           Almost No Chance
                                                                                 Highly Unlikely
                                                                                                        Chances are Slight
                                                                                                                               Little Chance
                                                                                                                                               Unlikely
                                                                                                                                                          Probably Not    About Even
                                                                                                                                                                                         Better than Even
                                                                                                                                                                                                               Likely
                                                                                                                                                                                                                        Probably

                                                                                                                                                                                                                                   Very Good Chance
                                                                                                                                                                                                                                                         Highly Likely
                                                                                                                                                                                                                                                                             Almost Certain

                                                                                                                                   Likelihood Expression
                                                                                                                                                                                                                                                                                                               Figure 5: Expected calibration error is not consistently im-
Figure 4: gpt-4 usage rate of each likelihood expression;                                                                                                                                                                                                                                                      proved for any CoT prompt variant on gpt-3.5-turbo.
the model displays markedly lower verbalized confidence on
TruthfulQA than on standard factual recall problems.                                                                                                                                                                                                                                                           each fold, we use it once to fit a temperature and
                                                                                                                                                                                                                                                                                                               evaluate metrics on the remaining folds. We find
A                        Additional Results                                                                                                                                                                                                                                                                    that fitting the temperature on 20% of the data
                                                                                                                                                                                                                                                                                                               yields relatively stable temperatures across folds.
Here, we include the likelihood expression usage                                                                                                                                                                                                                                                               We report the average temperature-scaled ECE and
distribution for gpt-3.5 and gpt-4 in Figures 3                                                                                                                                                                                                                                                                BS as ECE-t and BS-t.
and 4, respectively. gpt-3.5 is systematically less                                                                                                                                                                                                                                                                To compute ECE and AUC for Ling. 1S-opt., we
confident for TruthfulQA. The contrast between                                                                                                                                                                                                                                                                 similarly split our total data into 5 folds, using 4
model confidence for TriviaQA and SciQ compared                                                                                                                                                                                                                                                                folds to fit the probabilities behind each linguistic
with TruthfulQA is even more stark for gpt-4.                                                                                                                                                                                                                                                                  expression of confidence, then evaluating on the
   We also provide additional calibration results                                                                                                                                                                                                                                                              remaining fold. To compute ECE-t and BS-t for
for chain-of-thought methods. We compare a one-                                                                                                                                                                                                                                                                Ling. 1S-opt, we hold out one of the 5 folds to
stage verbalized CoT prompt (Verb. 1S CoT), a                                                                                                                                                                                                                                                                  fit temperature. We use 3 folds to fit probabilities
two-stage verbalized CoT prompt (Verb. 2S CoT),                                                                                                                                                                                                                                                                for linguistic expressions, compute the temperature
and a two-stage verbalized method that uses CoT                                                                                                                                                                                                                                                                based on these probabilities on the temperature
just before eliciting the numerical confidence (Verb.                                                                                                                                                                                                                                                          set, and evaluate metrics on the last fold. We then
2S Cot Prob) instead of before the guess, as shown                                                                                                                                                                                                                                                             average metrics across all 20 rotations of folds.
for gpt-3.5 on Trivia QA, SciQ, and Truthful QA
in Figure 5. We find that CoT does not noticeably                                                                                                                                                                                                                                                              C    Prompt Templates
improve calibration across any setting or dataset.
                                                                                                                                                                                                                                                                                                               The prompt template for each sampling method
B Fitting Procedure for Temperature and                                                                                                                                                                                                                                                                        is provided in Table 6. The question is substi-
                                                                                                                                                                                                                                                                                                               tuted for the variable ${THE_QUESTION} in each
  Probabilities for Linguistic Expressions
                                                                                                                                                                                                                                                                                                               prompt. To evaluate answer correctness, we
To fit the temperature that is used to compute ECE-                                                                                                                                                                                                                                                            use gpt-3.5-turbo for SciQ and TruthfulQA
t and BS-t we split our total data into 5 folds. For                                                                                                                                                                                                                                                           and gpt-4 for TriviaQA due to gpt-3.5-turbo’s
   Method            Template
   Label prob.       Provide your best guess for the following question. Give ONLY the guess, no
                     other words or explanation.\n\nFor example:\n\nGuess: <most likely guess, as
                     short as possible; not a complete sentence, just the guess!>\n\nThe question
                     is:${THE_QUESTION}
   ‘Is True’ prob.   Question: ${QUESTION}\nProposed Answer: ${ANSWER}\nIs the proposed answer:\n\t(A)
                     True or\n\t(B) False?\n The proposed answer is:

   Verb. 1S top-1    Provide your best guess and the probability that it is correct (0.0 to 1.0) for
                     the following question. Give ONLY the guess and probability, no other words or
                     explanation. For example:\n\nGuess: <most likely guess, as short as possible; not
                     a complete sentence, just the guess!>\n Probability: <the probability between 0.0
                     and 1.0 that your guess is correct, without any extra commentary whatsoever; just
                     the probability!>\n\nThe question is: ${THE_QUESTION}
   Verb. 1S top-k    Provide your ${k} best guesses and the probability that each is correct (0.0 to
                     1.0) for the following question. Give ONLY the guesses and probabilities, no other
                     words or explanation. For example:\n\nG1: <first most likely guess, as short as
                     possible; not a complete sentence, just the guess!>\n\nP1: <the probability between
                     0.0 and 1.0 that G1 is correct, without any extra commentary whatsoever; just
                     the probability!> ... G${k}: <${k}-th most likely guess, as short as possible;
                     not a complete sentence, just the guess!>\n\nP${k}: <the probability between 0.0
                     and 1.0 that G${k} is correct, without any extra commentary whatsoever; just the
                     probability!> \n\nThe question is: ${THE_QUESTION}
   Verb. 2S CoT      Provide your best guess for the following question. Before giving your answer,
                     provide a step-by-step explanation of your thought process. Then on a new line
                     give the guess with no other words or explanation.\n\nFor example:\n\nExplanation:
                     <one sentence step-by-step explanation of your thought process>\n\nGuess: <most
                     likely guess, as short as possible; not a complete sentence, just the guess!>\n\nThe
                     question is: ${THE_QUESTION}
                     Provide the probability that your guess is correct. Give ONLY the probability, no
                     other words or explanation.\n\nFor example:\n\nProbability: <the probability between
                     0.0 and 1.0 that your guess is correct, without any extra commentary whatsoever;
                     just the probability!>\n
   Verb. 2S top-1    Provide your best guess for the following question. Give ONLY the guess, no
                     other words or explanation.\n\nFor example:\n\nGuess: <most likely guess, as
                     short as possible; not a complete sentence, just the guess!>\n\nThe question
                     is:${THE_QUESTION}
                     Provide the probability that your guess is correct. Give ONLY the probability, no
                     other words or explanation.\n\nFor example:\n\nProbability: <the probability between
                     0.0 and 1.0 that your guess is correct, without any extra commentary whatsoever;
                     just the probability!>\n
   Verb. 2S top-k    Provide your ${k} best guesses for the following question. Give ONLY the guesses,
                     no other words or explanation. For example:\n\nG1: <first most likely guess, as
                     short as possible; not a complete sentence, just the guess!>\n\nP1: <the probability
                     between 0.0 and 1.0 that G1 is correct, without any extra commentary whatsoever;
                     just the probability!> ... G${k}: <${k}-th most likely guess, as short as possible;
                     not a complete sentence, just the guess!>\n\nThe question is:${THE_QUESTION}
                     Provide the probability that each of your guesses is correct.             Give ONLY
                     the probabilities, no other words or explanation.\n\nFor example:\n\nP1: <the
                     probability between 0.0 and 1.0 that G1 is correct, without any extra commentary
                     whatsoever; just the probability!>\n... P${k}: <the probability between 0.0 and
                     1.0 that G${k} is correct, without any extra commentary whatsoever; just the
                     probability!>
   Ling. 1S          Provide your best guess for the following question, and describe how likely it is
                     that your guess is correct as one of the following expressions: ${EXPRESSION_LIST}.
                     Give ONLY the guess and your confidence, no other words or explanation. For
                     example:\n\nGuess: <most likely guess, as short as possible; not a complete sentence,
                     just the guess!>\nConfidence: <description of confidence, without any extra
                     commentary whatsoever; just a short phrase!>\n\nThe question is: ${THE_QUESTION}

Table 6: Prompt templates for each method evaluated. Methods above the double line use multiple samples in order to estimate
confidence scores; methods below the double line use the verbalized confidences directly, requiring only a single sample.
high disagreement with a human evaluator on
TriviaQA. Using the ground truth answer as
${GOLD_ANSWER} and the model-generated answer
as ${PRED_ANSWER}, we use the following prompt
template:
   Are the following two answers to my
question Q semantically equivalent?\n\nQ:
${THE_QUESTION}\nA1: ${GOLD_ANSWER}\nA2:
${PRED_ANSWER}\n\nPlease answer with a
single word, either “Yes." or “No.", and
explain your reasoning.

```
