---
citation_key: "LiuEtAl2025c"
title: "Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey"
authors: "Xiaoou Liu; Tiejin Chen; Longchao Da; Chacha Chen; Zhen-Yu Lin; Hua Wei"
year: 2025
doi: "10.1145/3711896.3736569"
source: "local PDF (Xiaoou2025.pdf)"
access_level: "full-text-pdf"
retrieved_date: "2026-04-15"
arxiv_id: "2503.15850"
tier: 1
composite_score: 4.85
---
# Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey
**Authors**: Xiaoou Liu, Tiejin Chen, Longchao Da, Chacha Chen, Zhen-Yu Lin, Hua Wei
**Year**: 2025
**Venue**: Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2
**DOI**: [10.1145/3711896.3736569](https://doi.org/10.1145/3711896.3736569)

## Full Text (extracted via pdftotext) / 全文（pdftotext 抽取）

```text
                                        Uncertainty Quantification and Confidence Calibration in Large
                                                        Language Models: A Survey
                                                               Xiaoou Liu∗                                                   Tiejin Chen∗                                  Longchao Da
                                                          xiaoouli@asu.edu                                               tchen169@asu.edu                               longchao@asu.edu
                                                       Arizona State University                                       Arizona State University                        Arizona State University
                                                        Tempe, Arizona, USA                                            Tempe, Arizona, USA                             Tempe, Arizona, USA

                                                             Chacha Chen                                                        Zhen Lin                                     Hua Wei†
                                                        chacha@uchicago.edu                                             zhenlin4@illinois.edu                           hua.wei@asu.edu
                                                        University of Chicago                                            University of Illinois                      Arizona State University
                                                          Chicago, IL, USA                                               Urbana-Champaign                             Tempe, Arizona, USA

arXiv:2503.15850v2 [cs.CL] 3 Jun 2025
                                                                                                                         Champaign, IL, USA

                                        Abstract                                                                                        3–7, 2025, Toronto, ON, Canada. ACM, New York, NY, USA, 11 pages.
                                        Uncertainty quantification (UQ) enhances the reliability of Large                               https://doi.org/10.1145/3711896.3736569
                                        Language Models (LLMs) by estimating confidence in outputs, en-
                                        abling risk mitigation and selective prediction. However, traditional
                                        UQ methods struggle with LLMs due to computational constraints
                                        and decoding inconsistencies. Moreover, LLMs introduce unique                                   1   Introduction
                                        uncertainty sources, such as input ambiguity, reasoning path di-                                Large Language Models (LLMs) like GPT-4 [1] have achieved re-
                                        vergence, and decoding stochasticity, that extend beyond classical                              markable capabilities in text generation, reasoning, and decision-
                                        aleatoric and epistemic uncertainty. To address this, we introduce                              making, driving their adoption in high-stakes domains such as
                                        a new taxonomy that categorizes UQ methods based on compu-                                      healthcare diagnostics [20, 91], legal analysis [10, 59], and trans-
                                        tational efficiency and uncertainty dimensions, including input,                                portation systems [16, 55, 118]. However, their reliability remains a
                                        reasoning, parameter, and prediction uncertainty. We evaluate ex-                               critical concern: LLMs often produce plausible but incorrect or in-
                                        isting techniques, summarize existing benchmarks and metrics for                                consistent outputs, with studies showing that over 30% of answers
                                        UQ, assess their real-world applicability, and identify open chal-                              in medical QA tasks contain factual errors [47]. In sensitive appli-
                                        lenges, emphasizing the need for scalable, interpretable, and robust                            cations, these limitations pose risks ranging from misinformation
                                        UQ approaches to enhance LLM reliability.                                                       to life-threatening misdiagnoses, underscoring the urgent need for
                                                                                                                                        robust reliability frameworks.
                                        CCS Concepts                                                                                       Uncertainty quantification (UQ) emerges as an important mech-
                                                                                                                                        anism to enhance LLM reliability by explicitly modeling confidence
                                        • Computing methodologies → Machine learning; Natural
                                                                                                                                        in model outputs. By estimating uncertainty, users can identify
                                        language processing.
                                                                                                                                        low-confidence predictions for human verification, prioritize high-
                                                                                                                                        certainty responses, and mitigate risks like overconfidence in hallu-
                                        Keywords
                                                                                                                                        cinations [71]. For instance, in clinical settings, uncertainty-aware
                                        Uncertainty Quantification; Large Language Models                                               LLMs could flag uncertain diagnoses for specialist review, reducing
                                        ACM Reference Format:                                                                           diagnostic errors by up to 41% [99]. This capability is particularly
                                        Xiaoou Liu, Tiejin Chen, Longchao Da, Chacha Chen, Zhen Lin, and Hua                            critical as LLMs’ transition from experimental tools to production
                                        Wei. 2025. Uncertainty Quantification and Confidence Calibration in Large                       systems requiring accountability.
                                        Language Models: A Survey. In Proceedings of the 31st ACM SIGKDD Con-                              Traditional UQ methods face significant hurdles when applied
                                        ference on Knowledge Discovery and Data Mining V.2 (KDD ’25), August                            to LLMs. Bayesian approaches like Monte Carlo dropout [28] are
                                                                                                                                        computationally prohibitive for trillion-parameter models and nat-
                                        ∗ Both authors contributed equally to this research.
                                        † Corresponding author
                                                                                                                                        ural language generation (NLG) tasks, while ensemble methods
                                                                                                                                        struggle with consistency across diverse decoding strategies [73].
                                                                                                                                        Furthermore, LLMs introduce unique uncertainty sources, such
                                        Permission to make digital or hard copies of all or part of this work for personal or
                                        classroom use is granted without fee provided that copies are not made or distributed           as input ambiguity [7, 33], reasoning path divergence, and decod-
                                        for profit or commercial advantage and that copies bear this notice and the full citation       ing stochasticity that transcend classical aleatoric and epistemic
                                        on the first page. Copyrights for components of this work owned by others than the              categorizations [42]. The complexity of LLMs, characterized by
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission   sequence generation over vast parameter spaces and reliance on
                                        and/or a fee. Request permissions from permissions@acm.org.                                     massive datasets, exacerbates uncertainty challenges. This complex-
                                        KDD ’25, Toronto, ON, Canada                                                                    ity, coupled with the critical need for reliable outputs in high-stakes
                                        © 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM ISBN 979-8-4007-1454-2/2025/08                                                              applications, positions UQ for LLMs as a compelling yet underex-
                                        https://doi.org/10.1145/3711896.3736569                                                         plored research frontier.
KDD ’25, August 3–7, 2025, Toronto, ON, Canada                                                                                            Liu et al.

    Targeting the unique challenges of UQ in LLMs, this survey            or a combination of both. The technical methods on how to quantify
firstly introduces a novel taxonomy for LLM UQ, categorizing meth-        these uncertainties will be discussed later in Section 3.
ods along two axes: (1) computational efficiency (e.g., single-pass vs.   • Input Uncertainty (Aleatoric Uncertainty): Input uncertainty
sampling-based techniques) and (2) uncertainty dimensions (input,         arises when a prompt is ambiguous or underspecified, making it
reasoning, parametric, predictive). This framework addresses three        impossible for an LLM to generate a single definitive response. This
gaps in prior works: First, it decouples uncertainty sources unique       is inherently aleatoric, as even a “perfect model” cannot resolve
to LLMs from traditional ML contexts. Second, it evaluates methods        the ambiguity. For instance, “What is the capital of this country?”
through the lens of different dimensions of the responses from LLM:       lacks sufficient context, leading to unpredictable outputs. Similarly,
input uncertainty, reasoning uncertainty, parameter uncertainty,          “Summarize this document” may yield different responses depending
and prediction uncertainty. Each of these dimensions may involve          on different expected details.
aleatoric uncertainty, epistemic uncertainty, or a mixture of both.       • Reasoning Uncertainty (Mixed Uncertainty): Reasoning uncer-
Third, it identifies understudied areas like reasoning uncertainty,       tainty occurs when an LLM derives answers through multi-step
challenges, and possible future directions.                               reasoning [81] or retrieval [61], where the uncertainty of each step
Connection to Existing Surveys: Prior surveys [37, 40, 102] focus         can lead to ambiguous or incorrect results. This uncertainty is
on hallucination detection or retrofitting classical UQ taxonomies,       aleatoric when the problem itself is ambiguous and epistemic when
neglecting LLM-specific challenges like prompt-driven input uncer-        the model cannot offer robust reasoning.
tainty. Our work uniquely addresses the interplay between model           • Parameter Uncertainty (Epistemic Uncertainty): Parameter un-
scale, open-ended generation, and uncertainty dynamics, which are         certainty stems from training data gaps, where the model has either
critical for modern LLMs but overlooked in earlier frameworks.            never seen relevant information or has learned an incorrect repre-
   The remainder of this survey is structured as follows: Section 2       sentation. Unlike aleatoric uncertainty, epistemic uncertainty can
characterizes LLM uncertainty dimensions and differentiates confi-        be reduced by improving the model’s knowledge base. Bayesian
dence from uncertainty. Section 3 evaluates UQ methods using our          methods [28], deep ensembles [56], and uncertainty-aware train-
taxonomy. Section 4 introduces the evaluation of UQ methods for           ing [83] can help quantify and mitigate this type of uncertainty.
LLM, including benchmarks and metrics. Sections 5 and 6 introduce
                                                                          • Prediction Uncertainty (Mixed Uncertainty): Prediction uncer-
the applications of UQ in different domains with LLMs and identify
                                                                          tainty refers to variability in generated outputs across different
open challenges and future directions.
                                                                          sampling runs, influenced by both aleatoric and epistemic sources.
                                                                          For example, when asked “What are the side effects of a new ex-
2 Perliminaries                                                           perimental drug?”, the model’s responses might vary significantly
                                                                          across different sampling runs, especially if no reliable data is avail-
2.1 Sources of Uncertainty in LLMs                                        able in its training set. A high-variance output distribution in such
2.1.1 Aleatoric vs. Epistemic Uncertainty. For UQ on traditional          scenarios suggests that the model is both aware of multiple possi-
machine learning tasks such as classification or regression [129],        ble answers, reflecting aleatoric uncertainty, and uncertain due to
there are mainly two types of uncertainty [23, 127]: aleatoric un-        incomplete knowledge, highlighting epistemic uncertainty.
certainty, which models the uncertainty from noise in the dataset,
and epistemic uncertainty, which arises from the model’s lack of          2.2    Uncertainty and Confidence in LLMs
knowledge about the underlying data distribution.                         2.2.1 Classical Confidence Estimation. UQ and confidence estima-
   Aleatoric uncertainty in LLMs primarily stems from data sources        tion are closely related yet distinct concepts. In traditional machine
used to train LLMs, which contain inconsistencies, biases, and con-       learning, uncertainty is a property of the model’s predictive dis-
tradicting information. Additionally, ambiguity in natural language       tribution, capturing the degree of variability or unpredictability
also contributes to aleatoric uncertainty, as different interpreta-       given a particular input. In contrast, confidence reflects the model’s
tions of the same prompt can lead to multiple plausible responses.        belief in the correctness of a particular prediction. If we follow the
On the other hand, when encountering unfamiliar topics, LLMs              definition in classification tasks, the confidence measure would be
may exhibit high epistemic uncertainty, often manifesting as hal-         the predicted probability 𝑝ˆ (𝑌 = 𝑦|𝑥) given input 𝑥 (an uncertainty
lucinations or overconfident yet incorrect statements. Epistemic          measure which does not depend on the particular prediction 𝑦 could
uncertainty can be reduced through domain-specific fine-tuning or         be entropy, taking the form of 𝑦 −𝑝ˆ (𝑌 = 𝑦|𝑥) log 𝑝ˆ (𝑌 = 𝑦|𝑥)). Ta-
                                                                                                            Í
retrieval-augmented generation techniques that allow the model to         ble 1 shows a similar notation in a question-answering (QA) task
access external knowledge sources.                                        in Natural Language Generation (NLG). The corresponding confi-
                                                                          dence score in NLG tasks for an auto-regressive language model
2.1.2 Uncertainty with Different Dimensions. While the uncertainty        would be the joint probability for the generated sequence:
for LLMs can also be classified through aleatoric and epistemic                                                  Ö
uncertainty, these two categories alone are insufficient to fully                          𝐶 (x, s) = 𝑝ˆ (s|x) =    𝑝ˆ (𝑠𝑖 |s<𝑖 , x).         (1)
capture the complexities of uncertainty in LLMs. In particular, LLMs                                            𝑖
exhibit uncertainty not only due to training data limitations but         The log of Eq. (1) is sometimes referred to as sequence likeli-
also due to input variability and decoding mechanisms. Therefore,         hood [139]. In general, an uncertainty estimate in existing literature
in the following, we formulate four dimensions of uncertainty, each       usually takes the form of 𝑈 (x), while confidence estimates are usu-
of which may involve aleatoric uncertainty, epistemic uncertainty,        ally expressed as 𝐶 (x, s). Note that, unlike classification tasks, not
Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey                                   KDD ’25, August 3–7, 2025, Toronto, ON, Canada

             Notation                  Description                                     parameters are available, researchers mostly compute the confi-
            x               The question that LLMs answer                              dence from the output logits, either through normalizing Eq. (1)
            s                    Generation from LLMs                                  with the length of s [75], replacing the logit-sum or mean with
            𝑤𝑖               i-th token in the generation s                            weighted sum by attention values [67] or by importance inferred
            D                       Corpus of LLMs                                     from natural language inference (NLI) models [24]. Such variants
            𝑈 (x)              Uncertainty of question x                               of sequence likelihood could then be fed for (entropy-style) uncer-
            𝐶 (x, s)       Confidence of generation s given x                          tainty computation [51, 67].
            𝐻 (s)               Entropy of generation s                                • LLM-as-a-judge. Another popular approach is asking the LM
 Table 1: Notations used in this paper for an exemplary QA task.                       itself whether a particular free-form generation is correct [49]. How-
                                                                                       ever, this formulation also poses a restriction on the confidence
all NLG applications have the notion of a “correct” answer (e.g.,
                                                                                       estimation method, as it is essentially a scalar logit. Thus, many
summarization). Thus, while for the ease of writing we use the term
                                                                                       extensions focus on applying calibration methods from classifica-
correctness throughout this section, it should really be interpreted as
                                                                                       tion to calibrate such self-evaluation. The few exceptions include
the gold-label for the particular application. Note also that in most
                                                                                       [49, 97], which converts samples from free-form generation into a
cases, the correct answer is not unique, and thus such gold-label
                                                                                       multiple-choice question (with generations being the options) and
typically takes the form of a “correctness function” that decides
                                                                                       adds a "None of the above" option to elicit the confidence.
whether a particular generation s is good or not. We will denote
such a function as 𝑓 (s|x).                                                            • Trainable Confidence Estimators. Since we typically care
                                                                                       about the LM’s confidence in the “semantic space” due to semantic
2.2.2 Confidence Improvement. There are usually two dimensions                         invariance, instead of manipulating logits, a popular approach is to
along which researchers improve confidence estimates in NLG,                           perform additional training for confidence estimation. This could
which is unsurprisingly largely influenced by confidence scoring                       be done on the base LM (either fully [46, 50, 139] or partially [71])
literature from classification [45], especially binary classification.                 with a different loss, or using a separate model on the internal or
We refer to them as ranking performance and calibration:                               external representations from the base LM [44, 109]. On the other
• Ranking performance refers to the discriminative power of the                        end of the spectrum, without any training, prompting could be
confidence measure on the correctness. Like in classification, LLM                     used to elicit verbalized confidence values [107]. Finally, one could
confidence is often evaluated by its ability to separate correct and                   combine multiple confidence estimation methods and enjoy the
incorrect answers, thus typically measured by evaluation metrics                       benefit of ensembling [29].
like AUROC [49] or AUARC [67] as detailed in Section 4.                                   As with UQ evaluation (more in Section 4), the choice of correct-
                                                                                       ness function has a profound impact on the conclusion of the exper-
• Calibration refers to closing the gap between the confidence
                                                                                       iments, especially for free-form generation tasks. Popular choices
score and the expected correctness conditioned on confidence score.
                                                                                       include using (potentially larger) LLM as judges [66, 71, 107], human
It has a long history preceding even modern machine learning [85],
                                                                                       annotations [97], or lexical similarities such as ROUGE [51, 139].
but bears slightly different meanings in NLP. In general, we
                                                                                       Recently, Liu et al. [72] proposes to evaluate free-form generation
could define a perfectly calibrated confidence measure to achieve:
                                                                                       confidence measures with selected multiple-choice datasets as an
∀𝑐, E[𝑓 (s|x)|𝐶 (x, s) = 𝑐] = 𝑐, where the expectation is taken over
                                                                                       efficient complement. For longer generations, Huang et al. [41]
the joint distribution of x and generation s. A lot of papers focus
                                                                                       proposes to use ordinal (not binary) correctness values to capture
on evaluating the calibration quality of specific language models
                                                                                       the ambiguity in the quality of a generation. In a similar flavor, [3]
(LMs) and tasks [52, 114]. Evaluation typically relies on variants
                                                                                       studies the issues in the evaluation of calibration when there is
of Expected Calibration Error (ECE) [52, 107]. Oftentimes confi-
                                                                                       intrinsic human disagreement on the label.
dence scores from classification could be directly applied [103] in
order to evaluate whether an LM is over- or under-confident, es-                       Remarks. Existing literature sometimes uses the terms uncertainty
pecially for de facto classification tasks like sentiment analysis or                  and confidence interchangeably. They do often seemingly coincide:
multiple-choice QA.                                                                    When a model’s prediction has low confidence, we naturally con-
                                                                                       sider this as a high uncertainty case. This, however, is treating
2.2.3 Confidence Estimation for LLMs. Confidence estimation in                         𝑈 (x) = − maxs 𝐶 (x, s) as an uncertainty estimate. In general, a
large language models (LLMs) refers to the task of quantifying how                     model may exhibit high uncertainty over its output space but still
certain a model is about a specific generated output. In this subsec-                  express high confidence in a specific output. Conversely, a model
tion, we review three major families of approaches to confidence                       could have low overall uncertainty but low confidence in a partic-
estimation in LLMs:                                                                    ular prediction. While the “low uncertainty low confidence case”
• UQ methods with Confidence Estimation. As uncertainty                                is relatively less interesting in classification or regression tasks
and confidence are often intertwined, many approaches used in                          due to MLE point prediction, this scenario is notably more com-
UQ have their counterpart in confidence estimation. For example,                       mon in NLG, as the output is typically randomly sampled 1 from
for black-box settings where the parameters of LLMs are unavail-                       the predictive distribution. There are also applications that require
able, [66, 133] computes a similarity matrix of sampled responses                      one but not the other (e.g. conformal language modeling [92] or
and derives confidence estimates for each generation via its degree                    seletive generation [13]). In the rest of this paper, we sometimes
or distance derived from the graph Laplacian, before using these                       1 In fact, even if the output is greedily generated, it might not have the highest confi-
scores to compute uncertainty. For white-box settings where model                      dence as measured by Eq. (1).
KDD ’25, August 3–7, 2025, Toronto, ON, Canada                                                                                                                     Liu et al.

         Method                                       Uncertainty Dimensions                       Efficency Features               Access to Model   Confidence
         Input clarification ensembles [36]              Input Uncertainty                     Multi Rounds Generations               Black-box          No
         ICL-Sample [68]                                 Input Uncertainty                     Multi Rounds Generations               Black-box          No
         SPUQ [29]                                       Input Uncertainty            Multi Rounds Generations + Additional Model     Black-box          No
         UAG [128]                                     Reasoning Uncertainty                   Single Round Generation                White-box          No
         CoT-UQ [132]                                  Reasoning Uncertainty                   Single Round Generation                White-box          Yes
         TouT [80]                                     Reasoning Uncertainty                   Multi Rounds Generations               Black-box          No
         TopologyUQ [18]                               Reasoning Uncertainty                   Multi Rounds Generations               Black-box          No
         Stable Explanations Confidence [5]            Reasoning Uncertainty                   Multi Rounds Generation                Black-box          Yes
         SAPLMA [2]                              Parameter + Prediction Uncertainty                   Fine-tuning                     White-box          Yes
         Supervised estimation[69]               Parameter + Prediction Uncertainty                   Fine-tuning                     White-box          Yes
         UaIT [70]                               Parameter + Prediction Uncertainty                   Fine-tuning                     White-box          Yes
         LoRA ensembles [4]                           Parameter Uncertainty                           Fine-tuning                     White-box          Yes
         BloB [115]                                   Parameter Uncertainty                           Fine-tuning                     White-box          Yes
         BLoRA [121]                                  Parameter Uncertainty                           Fine-tuning                     White-box          Yes
         Perplexity [77, 82]                           Prediction Uncertainty                  Single Round Generation                White-box          Yes
         SAR [24]                                      Prediction Uncertainty                  Single Round Generation                White-box          Yes
         P(True) [49]                                  Prediction Uncertainty                  Single Round Generation                White-box          Yes
         Response improbability [26]                   Prediction Uncertainty                  Single Round Generation                White-box          Yes
         Average log probability [76]                  Prediction Uncertainty                  Single Round Generation                White-box          Yes
         Predictive Entropy [49]                       Prediction Uncertainty                  Multi Rounds Generations               White-box          Yes
         Relative Mahalanobis distance [96]            Prediction Uncertainty                  Multi Rounds Generations               White-box          Yes
         HUQ [112]                                     Prediction Uncertainty                  Multi Rounds Generations               White-box          Yes
         Conformal Prediction (CP) [53, 92]            Prediction Uncertainty                  Multi Rounds Generations               White-box          No
         ConU [116]                                    Prediction Uncertainty                  Multi Rounds Generations               White-box          No
         Level-adaptive CP [11]                        Prediction Uncertainty                  Multi Rounds Generations               White-box          No
         LoFreeCP [104]                                Prediction Uncertainty                  Multi Rounds Generations               Black-box          No
         Ecc(J),Deg(J) [66]                            Prediction Uncertainty                  Multi Rounds Generations               Black-box          Yes
         Eig(J) [66]                                   Prediction Uncertainty                  Multi Rounds Generations               Black-box          No
         Normal length predictive entropy [75]         Prediction Uncertainty         Multi Rounds Generations +Additional Model      White-box          Yes
         Semantic Entropy [51]                         Prediction Uncertainty         Multi Rounds Generations + Additional Model     White-box          Yes
         Kernel Language Entropy [87]                  Prediction Uncertainty         Multi Rounds Generations + Additional Model     White-box          Yes
         Ecc(C),Ecc(E),Deg(C),Deg(E) [66]              Prediction Uncertainty         Multi Rounds Generations + Additional Model     Black-box          Yes
         Eig(C),Eig(E) [66]                            Prediction Uncertainty         Multi Rounds Generations + Additional Model     Black-box          No
         MD-UQ [8]                                     Prediction Uncertainty         Multi Rounds Generations + Additional Model     Black-box          No
         D-UE [15]                                     Prediction Uncertainty         Multi Rounds Generations + Additional Model     Black-box          Yes
             Table 2: An overview of UQ methods discussed in this paper for different dimensions, efficiency, and model settings.
follow the language of the original papers and treat confidence                          natural language, more effort is needed into input uncertainty and
estimates as uncertainty, but will clearly mark the methods that                         its application.
provide confidence estimates.
                                                                                         3.2      Reasoning Uncertainty
3 UQ Methods for Different Dimensions
                                                                                         Reasoning is the process of drawing conclusions based on available
3.1 Input Uncertainty                                                                    information. As the LLMs have demonstrated remarkable perfor-
As mentioned in Section 2.1.2, input uncertainty arises from the                         mance on tasks involving reasoning, recent research has focused
ambiguous or incomplete input to the LLMs. While there are works                         on using UQ in LLM reasoning and analyzing the internal reason-
in the LLMs domain that try to benchmark or deal with ambigu-                            ing process. For example, TopologyUQ [18] introduces a formal
ity [7, 22, 33, 130], they did not model the uncertainties induced by                    method to extract and structure LLM explanations into graph repre-
ambiguity. Existing UQ methods that specifically consider input                          sentations, quantifying reasoning uncertainty by employing graph-
uncertainty focus on perturbing the input prompts of LLMs. For                           edit distances and revealing redundancy through stable topology
instance, [36] proposes an approach that generates multiple clarifi-                     measures. Stable-Explanation Confidence [5] treats each possible
cations for a given prompt and ensembles the resulting generations                       model and its explanation pair as a test-time classifier to construct
by using mutual information to capture the disagreement among                            a posterior answer distribution that reflects overall reasoning con-
the predictions arising from different clarifications. Similarly, [68]                   fidence. CoT-UQ [132] integrates chain-of-thought reasoning into
proposed ICL-Sample, which quantified the input uncertainty in                           a response-level UQ framework, thereby leveraging the inherent
the setting of in-context learning using different in-context samples.                   multi-step reasoning capability of LLMs to further improve uncer-
[29] proposes SPUQ, which perturbs the input by techniques such                          tainty assessment. Collectively, these approaches provide a robust
as paraphrasing and dummy tokens to expose the model’s sensitiv-                         and interpretable framework for enhancing LLM reasoning by quan-
ity and capture uncertainty. Specifically, SPUQ quantified the input                     tifying uncertainty at local or global levels.
uncertainty by using a similarity metric such as BERTScore [135]                            The quantified uncertainty could be used to guide the exploration
to measure how consistent the responses are across different per-                        of reasoning steps and improving the final performance in com-
turbations. In general, there are only a few papers that consider                        pleting the tasks. In [80], they propose Tree of Uncertain Thoughts
input uncertainty. Since ambiguity is common and important in                            (TouT), which extend the Tree of Thoughts (ToT) [125] framework
Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey                                     KDD ’25, August 3–7, 2025, Toronto, ON, Canada

by quantifying the uncertainties in intermediate reasoning steps                       the model spreads its probability more broadly over possible words,
with Monte Carlo Dropout and assigning uncertainty scores to                           indicating that it has a higher uncertainty.
important decision points. Similarly, [128] reduces the error ac-                      • Maximum Token Log-Probability. Apart from the perplexity,
cumulation in multi-step reasoning by monitoring the predicted                         Maximum token log-probability [76] measures the sentence’s like-
probability of the next token at each generation step, dynamically                     lihood by assessing the least likely token in the sentence. A higher
retracting to more reliable states and incorporating certified rea-                    Maximum(𝑝) indicates higher uncertainty of the whole generation.
soning clues when high uncertainty is detected. Their experimental                     It is calculated by 𝑀𝑎𝑥 (𝑝) = max (− ln 𝑝 (𝑤𝑖 )).
results shows that integrating uncertainty enhances the precision                                                                𝑖
of generated responses by integrating these local measures with                        • Entropy reflects how widely distributed a model’s predictions
global search techniques.                                                              are for a given input, indicating the level of uncertainty in its
                                                                                       outputs [49, 51]. Entropy for the i-th token is provided by H𝑖 =
                                                                                         Í
                                                                                       − 𝑤˜ ∈ D 𝑝𝑖 ( ˜
                                                                                                    𝑤) log 𝑝𝑖 ( ˜
                                                                                                               𝑤). Then it is possible to use the mean or
3.3     Parameter Uncertainty                                                          maximum value of entropy as the final uncertainty [76]: 𝐴𝑣𝑔(H ) =
Parameter uncertainty arises when an LLM lacks sufficient knowl-                        1 Í𝑁
                                                                                       𝑁 𝑖=1 H𝑖 ; 𝑀𝑎𝑥 (H ) = max (H𝑖 ). Furthermore, Shifting Attention
edge due to limitations in its training data or model parameters. It                                                     𝑖
                                                                                       to Relevance (SAR) [24], enhanced the performance of entropy by
reflects the model’s uncertainty about its own predictions, which
                                                                                       adjusting attention to more relevant tokens inside the sentence. In
can be reduced with additional training or adaptation techniques.
                                                                                       detail, SAR assigned weight for H𝑖 and the weight 𝑅(𝑤𝑖 , 𝑠, 𝑥) can
   Traditional UQ methods like Monte Carlo Dropout and Deep En-
                                                                                       be obtained by: 𝑅(𝑤𝑖 , 𝑠, 𝑥) = 1 − |𝑔(𝑥 ∪ 𝑠, 𝑥 ∪ 𝑠 \ {𝑤𝑖 })| , where 𝑔
sembles have been widely used but are computationally infeasible
                                                                                       is a function that measures the semantic similarity between two
for large-scale LLMs due to the need for multiple forward passes or
                                                                                       sentences, which can be estimated with NLI models [24].
model replicas. To address this, Bayesian Low-Rank Adaptation by
Backpropagation (BLoB) [115] and Bayesian Low-Rank Adaptation                          • Response Improbability [26] uses response improbability,
(BLoRA) [121] incorporate Bayesian modeling into LoRA adapters,                        which computes the probability of a given sentence and subtracts
allowing uncertainty estimation through parameter distributions                        the resulting value from one. In detail, response improbability is
                                                                                                                    Î
without a full-model ensemble. However, these methods still incur                      provided by 𝑀𝑃 (𝑠) = 1 − 𝑖=1 𝑝𝑖 (𝑤𝑖 ). If the sentence is certain
significant computational costs.                                                       (i.e., the product of token probabilities is high), 𝑀𝑃 (𝑠) will be low.
   Finetuning-based approaches offer a more practical alternative.                     • P(True) [49] measures the uncertainty of the claim by asking
Techniques such as Supervised Uncertainty Estimation [69] train                        the LLM itself whether the generation is true or not. Specifically,
auxiliary models to predict the confidence of LLM outputs based on                     P(True) is calculated 2 : P(True) = 1 − 𝑝 (𝑦1 = “True”). Note that
activation patterns and logit distributions. Similarly, Uncertainty-                   here we are using 𝑦1 as the first token instead of 𝑤 1 because 𝑤 1
aware Instruction Tuning (UaIT) [70] modifies the fine-tuning pro-                     represents the first token in the generation 𝑠 while 𝑦1 represents the
cess to explicitly train models to express uncertainty in their out-                   first token when asking LLM whether the generation 𝑠 is correct
puts. SAPLMA [2] refines probabilistic alignment techniques to dy-                     or not. P(True) requires running the LLM twice. However, it does
namically adjust model uncertainty estimates, ensuring adaptability                    not require multiple generations 𝑠. Therefore, we still classify this
to different downstream tasks. Additionally, LoRA ensembles [4]                        method as a single-round generation 3 .
provide an alternative to full-model ensembles by training multiple
lightweight LoRA-adapted variants of an LLM instead of retraining                      3.4.2 Multiple rounds generation. Multiple rounds generation
the entire network.                                                                    methods estimate uncertainty by generating multiple predictions
                                                                                       from the LLMs and analyzing their consistency, similarity, or vari-
                                                                                       ability. These approaches assume that if a model is confident, its
3.4     Prediction Uncertainty                                                         outputs should be stable across different sampling conditions.
Most off-the-shelf UQ methods focus on prediction uncertainty                          • Token-Level Entropy. Token-level entropy quantifies uncer-
since it is the most straightforward way to estimate the uncertainty.                  tainty in LLMs by analyzing the probability distribution of gener-
Considering the number of generations and models when estimat-                         ated tokens across multiple samples. A confident model assigns
ing uncertainties, existing methods for predicting uncertainty can                     high probability to a specific token, resulting in low entropy, while
be categorized into the following three categories.                                    uncertain predictions distribute probability across multiple tokens,
                                                                                       leading to higher entropy.
3.4.1 Single Round Generation. Most single-round generation                               Multiple responses are generated for the same input to estimate
methods utilize the logit or hidden states during generation. With                     token-level entropy, and the entropy of the token probability dis-
only one round of generation, these methods usually methods are                        tribution is computed. For example, predictive entropy [49] can
usually efficient in estimating uncertainties.                                         also be applied to multiple response settings and shows a better
• Perplexity is a measure of how well a probabilistic language                         uncertainty quality based on the variability of multiple outputs.
model predicts a sequence of text [111] while Mora-Cross and                           Similarly, SAR [24] could also be applied to multiple responses. [75]
Calderon-Ramirez [82], Margatina et al. [77] and Manakul et al.                        extends with Monte Carlo-based approximations and focuses on
[76] utilize the perplexity as the uncertainty. In detail, using
                                                                                       2 The original name is P(IK), which stands for “I Know”.
𝑤𝑖 as the i-th token in the generation,
                                          perplexity is given by                      3 This could be considered an uncertainty estimate as the sequence to be evaluated is
Perplexity = exp − 𝑁1 𝑖=1
                      Í𝑁
                           ln 𝑝 (𝑤𝑖 ) . A higher perplexity means                      the prediction given the input.
KDD ’25, August 3–7, 2025, Toronto, ON, Canada                                                                                         Liu et al.

how probability distributions evolve across tokens during autore-        This approach uses an NLI model to determine entailment relation-
gressive generation. There are two main approaches to get the            ships among responses, grouping them into meaning-preserving
final uncertainty: one averages entropy across multiple sampled          clusters. Instead of calculating entropy over individual responses,
outputs, and the other decomposes sequence-level uncertainty into        SE computes entropy over these clusters. Kernel Language Entropy
token-level contributions using entropy approximation.                   (KLE) [87] takes a different approach by avoiding explicit cluster-
• Conformal Prediction. Conformal Prediction (CP) [101] is a             ing. Instead, it embeds the responses in a semantic space using a
statistical framework that provides formal coverage guarantees           positive semidefinite kernel function. By computing von Neumann
for uncertainty estimation in LLMs. Its distribution-free properties     entropy over these response distributions, KLE provides an even
make it suitable for both black-box and white-box models.                more fine-grained measure of uncertainty that considers nuanced
   In the black-box setting, where model internals are inaccessible,     semantic variations.
CP estimates uncertainty using response frequency, semantic simi-        • Pairwise similarity methods construct a pairwise semantic
larity, or self-consistency. One study proposes a method tailored        similarity matrix between responses and analyze its structural prop-
for API-only LLMs [104], using frequency-based sampling com-             erties to estimate uncertainty. Methods like [66] use NLI models to
bined with normalized entropy and semantic similarity to define          score entailment and contradiction between every pair of generated
nonconformity scores. Another black-box CP method introduces             outputs, forming a weighted similarity graph. A confident model
a self-consistency-based uncertainty measure [116], which clus-          yields semantically coherent responses with strong mutual agree-
ters sampled generations and selects a representative response to        ment (high similarity), while inconsistent or ambiguous outputs
construct prediction sets with correctness guarantees, making it         lead to greater dispersion in the matrix. To quantify this dispersion,
particularly effective for open-ended NLG tasks.                         spectral graph metrics are applied: Eccentricity (Ecc) captures vari-
   On the other hand, white-box CP methods use logits, internal          ability spread, Eigenvalue-based (Eig) measures assess global struc-
activations, and calibration techniques for more refined uncertainty     ture, and Degree (Deg) evaluates local consistency. Recent works
estimation. One study proposes Conformal Language Modeling [92],         further extend this by modeling the response similarity graph as
which integrates CP with autoregressive text generation by dynam-        directed [15] or multi-dimensional [8], allowing for richer repre-
ically calibrating a stopping rule to ensure at least one response       sentation of semantic asymmetry or latent factors in uncertainty.
in the generated set is statistically valid. Another work adapts CP
for multiple-choice QA [53], using model confidence scores to cali-      4 Evaluation of Uncertainty in LLMs
brate prediction sets, ensuring coverage with minimal set size. A
                                                                         4.1 Benchmark Datasets
more advanced technique, conditional CP [11], dynamically adjusts
coverage guarantees based on the difficulty of the input, optimizing     Datasets used in previous studies can be organized into several
prediction set size while maintaining reliability.                       categories based on their focus. An overall summary of the catego-
                                                                         rization of datasets and benchmarks for UQ is shown in Table 3.
• Consistency-Based Methods. Consistency-based uncertainty
estimation methods analyze the agreement between multiple gener-         • Reading comprehension benchmarks include CoQA [94] for
ated responses from an LLM to determine uncertainty. The underly-        conversational question answering tasks, RACE [54] for general
ing assumption is that if the model is confident, its responses should   reading comprehension, TriviaQA [48] for fact-based questions,
be consistent, while high variability among responses suggests un-       CosmosQA [39] for contextual understanding, SQuAD [93] for
certainty. [66] measures the overlap between words through Jaccard       question answering on passages, and HotpotQA [123] for multi-
similarity in different generations. This method evaluates the devi-     hop reasoning.
ation from self-consistency, where a high Jaccard similarity across      • Reasoning and math benchmarks include HotpotQA [123] and
generations implies low uncertainty.                                     StrategyQA [30], which test multi-hop reasoning, GSM8K [12] for
   However, word-level similarity alone is insufficient, as different    solving math problems, and CalibratedMath [64], designed to eval-
responses can convey the same meaning using different phrasing.          uate confidence expression in arithmetic. These benchmarks are
Moreover, the generated response might include long reasoning            helpful to evaluate the reasoning uncertainty.
steps that require detailed analysis [32]. To address this problem,      • Factuality evaluation draws on datasets such as TruthfulQA [65]
some methods incorporate external models to assess semantic simi-        for addressing common misconceptions, FEVER [106] for claim
larity rather than relying solely on lexical overlap.                    verification, HaluEval [58] for detecting hallucinations, and an
                                                                         annotated FActScore [78] dataset for evaluating the factuality of
3.4.3 Multiple Rounds Generation with External Models. Semantic-         long-form text generated by LLMs.
based uncertainty estimation methods expand multiple generation          • General knowledge benchmarks can be adapted for UQ to test
approaches by incorporating external models, such as Natural Lan-        the models’ general knowledge, such as MMLU [34] for a wide
guage Inference (NLI) or pretrained language models, to evalu-           range of subjects, GPQA [95] for multiple-choice questions in phys-
ate the semantic relationships among generated responses beyond          ical sciences, and HellaSwag [131] for common-sense reasoning
surface-level similarity.                                                through sentence completion. These benchmarks can be adapted
• Distribution-based entropy methods quantify uncertainty by             for UQ because the tasks can be reduced to a classification prob-
modeling the distribution of generated responses in a semantic           lem, determining whether the model is confident or uncertain. The
space. Semantic Entropy (SE) [51] refines uncertainty estimation         structured nature of these benchmarks allows for clear evaluation
by clustering generated responses based on semantic equivalence.         of the model’s confidence in its predictions.
Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey                           KDD ’25, August 3–7, 2025, Toronto, ON, Canada

       Category                  Benchmarks                                            to LLM-as-a-judge evaluations, wherein a large language model
       Reading Comprehension     TriviaQA [48], CoQA [94], RACE [54], Cos-             (e.g., GPT-4) is prompted to assess text quality or correctness. This
                                 mosQA [39], SQuAD [93], HotpotQA [123]                approach can capture nuanced aspects like coherence, style, and
       Reasoning & Math          StrategyQA [30], HotpotQA [123],
                                 GSM8K [12], CalibratedMath [64]                       factuality, but also introduces risks of bias and inconsistency. Hu-
       Factuality                TruthfulQA [65], FEVER [106], HaluE-                  man annotation, however, is expensive and is often limited to a
                                 val [58], FActScore [78]                              small scale [51, 133].
       General Knowledge         MMLU [34], GPQA [95], HellaSwag [131]
       Consistency & Ambiguity   ParaRel [25], AmbigQA [79], AmbigInst [36],
                                                                                          Apart from the binary classification framework, there are also
                                 Abg-SciQA [7]                                         multiple evaluation methods designed for the specific treatment
      Table 3: Categorization of benchmarking datasets for UQ.                         of uncertainty, sometimes qualitative. For example, focusing on
                                                                                       decomposing aleatoric and epistemic uncertainty, [36] evaluates
• Consistency and ambiguity are two additional kind of bench-                          only the aleatoric part by using AmbigQA [79], as high ambiguity
marks for UQ. Consistency benchmarks such as ParaRel [25] tests                        questions should incur higher aleatoric uncertainty (whereas math
semantic consistency across 328 paraphrases for 38 relations, and                      questions, for examples, might have lower). The evaluation in [31],
datasets like AmbigQA and AmbigInst, which feature inherent am-                        on the other hand, is a comparison between the variability of human
biguities [7, 36, 79]. Ambiguity datasets are useful in UQ evaluation                  production (generation) with that of the LM. With an emphasis on
because they introduce aleatoric uncertainty by highlighting cases                     UQ for longer generations, [133] compares the uncertainty estimate
where multiple plausible interpretations exist, helping to assess                      against FActScore [78], as the “correctness” of a long paragraph
how well models distinguish between data-driven randomness and                         could be ill-defined or ambiguous.
model-based uncertainty. These datasets enable a more precise
decomposition of uncertainty into aleatoric and epistemic compo-                       5   UQ Applications in LLMs
nents, improving model reliability and interpretability.
                                                                                       LLMs are increasingly applied in diverse domains, offering flexibil-
   Recently, there have been efforts to develop UQ benchmarks
                                                                                       ity and reasoning capabilities. However, UQ is crucial for ensuring
for dedicated sources of uncertainty or specific methods. For ex-
                                                                                       their reliability, particularly in high-stakes applications. This sec-
ample, MAQA [122] is a dataset specifically designed to evaluate
                                                                                       tion will introduce the applications that integrate the UQ of LLMs
epistemic uncertainty in language models; LM-Polygraph [27] was
                                                                                       from some example domains. Many other fields like energy man-
later adopted as a comprehensive uncertainty benchmark [110].
                                                                                       agement, operations research, etc., employ LLMs and would require
[126] developed a benchmark for conformal prediction methods.
                                                                                       such discussions on the need for UQ as well.
These contributions represent specialized datasets explicitly de-
signed to assess UQ capabilities in LLMs, rather than adapting                         • Robotics. LLM-based robotic planning suffers from ambiguity
existing general-purpose benchmarks.                                                   and hallucinations, motivating the need for UQ in the planning loop.
                                                                                       For example, closed-loop planners [141] employ an uncertainty-
4.2     Evaluation Metrics                                                             based failure detector to continuously assess and adjust plans in
                                                                                       real-time, while non-parametric UQ methods [108] use an efficient
UQ is often evaluated from binary classification tasks, with the
                                                                                       querying strategy to improve reliability. [84] integrates action fea-
rationale being that high uncertainty should correspond to low
                                                                                       sibility checks to align the LLM’s confidence with real-world con-
expected accuracy. This is typically modeled by assigning a binary
                                                                                       straints, improving success rates from approximately 70% to 80%.
label to each response with a correctness function and using the
                                                                                       Similarly, [88] dynamically adjusts thresholds for alternative paths
uncertainty estimates to predict the label. AUROC (Area Under the
                                                                                       in adaptive skill selection, achieving higher success rates. [62] de-
Receiver Operating Characteristic curve), which measures how
                                                                                       velops an introspective planning framework with LLMs self-assess
effectively the uncertainty score separates correct from incorrect
                                                                                       their uncertainty to enhance safety and human-robot collaboration.
responses, is often used. With values ranging from 0 to 1, higher
AUROCs indicate better performance. Responses with confidence                          • Transportation. Preliminary research explores how LLMs can
above the threshold are classified as predicted positives, while those                 enhance transportation systems [17, 19, 124]. For example, LLM
below are treated as predicted negatives. Many prior studies use                       inference has been used to bridge the sim-to-real gap in traffic
AUROC to evaluate how well the uncertainty score discriminates cor-                    signal control [16, 19] and smooth mixed-autonomy traffic [124].
rect from incorrect predictions [6, 51, 69, 72, 119]. Similarly, AUPRC                 However, both cases reveal the potential risk posed by hallucina-
(Area Under the Precision-Recall Curve) and AUARC (Area Under the                      tion. A few works have investigated the uncertainty measure while
Accuracy-Rejection Curve) [86] also offer further insights into UQ.                    using the LLMs [21], which tries to link the use of VLMs with deep
AUPRC measures how well the uncertainty score separates correct                        probabilistic programming for UQ while conducting multimodal
from incorrect responses [68], while AUARC assesses how effectively                    traffic accident forecasting tasks.
the uncertainty measure aids in selecting accurate responses by                        • Healthcare. In healthcare, LLMs and VLMs can be good refer-
determining which uncertain questions to reject [67].                                  ences for diagnosis, but uncertainty is a critical dimension that
   In the context of NLG where the correctness label is hard to                        should be considered together with the generation of more reliable
obtain, researchers also compute heuristic-based fuzzy matching                        treatment plans [98]. In [9], it quantifies uncertainty in a white-box
metrics such as BLEU [90] and ROUGE [51] between the generated                         setting, and reveals that an effective reduction of model uncer-
text and the reference output(s) to gauge the quality. However,                        tainty can be achieved by using the proposed multi-tasking and
these metrics often fail to capture semantic fidelity or factual cor-                  ensemble methods in EHRs. However, as [117] benchmarks pop-
rectness. Consequently, many researchers are increasingly turning                      ular uncertain quantification methods with different model sizes
KDD ’25, August 3–7, 2025, Toronto, ON, Canada                                                                                                        Liu et al.

on medical question-answering datasets, the challenge of UQ for           correctness. Even for structured tasks like question answering, de-
medical applications is still severe.                                     termining whether a free-form generation is correct can be nontriv-
                                                                          ial due to semantic variability and ambiguity. This issue becomes
                                                                          even more pronounced in open-ended tasks. Moreover, LLM-as-a-
6    Challenges and Future Directions
                                                                          judge evaluation approaches are themselves subject to systematic
While significant strides have been made in integrating uncertainty       biases [65, 89, 140]. In addition, common evaluation metrics such
quantification into LLMs, several unaddressed challenges persist.         as AUROC and AUARC often fail to capture what might be considered
This section will explore these unresolved issues, ranging from           “meaningful" uncertainty. These metrics typically assess a model’s
efficiency-performance trade-offs to cross-modal uncertainty, and         ability to distinguish between correct and incorrect outputs, but do
outline promising avenues for future research, aiming to advance          not differentiate between confidently wrong responses and those
the reliability of LLMs in high-stakes applications.                      accompanied by an appropriate level of uncertainty.
• Efficiency-Performance Trade-offs. Multi-sample uncertainty
methods incur prohibitive costs for trillion-parameter LLMs ($12k         7      Conclusion
per million queries [57]), yet yield marginal reliability gains (≤ 0.02
                                                                          In this survey, we offer a comprehensive overview of uncertainty
AUROC improvement [120]). Hybrid approaches combining low-
                                                                          quantification (UQ) in Large Language Models (LLMs). We first
cost proxies (attention variance [35], hidden state clustering [87])
                                                                          introduce the fundamental concepts relevant to both UQ and LLMs,
could resolve this by achieving 90% of maximal performance at
                                                                          highlighting the importance of reliability in high-stakes applica-
10% computational cost. For example, precomputing uncertainty
                                                                          tions. Following this, we propose a detailed taxonomy for character-
“hotspots" during inference could trigger targeted multi-sampling
                                                                          izing uncertainty dimensions in LLMs, including input, reasoning,
only for high-risk outputs like medical diagnoses.
                                                                          parameter, and prediction uncertainty. We systematically introduce
• Interpretability Deficits. Users struggle to distinguish whether        existing UQ methods using our novel taxonomy, reviewing their
uncertainty stems from ambiguous inputs, knowledge gaps, or               effectiveness across different uncertainty types. Ultimately, we iden-
decoding stochasticity. Modular architectures that decouple uncer-        tify and discuss some of the persistent challenges in UQ for LLMs,
tainty estimation layers [38, 100] or employ causal tracing of trans-     providing insightful directions for future research. The primary goal
former attention pathways [113] could clarify uncertainty origins.        of this survey is to promote the integration of UQ techniques into
For instance, perturbing model weights [28] might reveal paramet-         LLM development, motivating both machine learning researchers
ric uncertainty in low-resource languages, while input modules flag       and practitioners to participate in this rapidly advancing area.
underspecified terms for clarification.
• Cross-Modality Uncertainty. Integrating vision, text, and sen-          ACKNOWLEDGMENTS
sor data introduces misaligned confidence estimates between modal-
                                                                          The work was partially supported by NSF awards #2421839. The
ities: LVLMs exhibit 2.4× higher uncertainty in visual vs. textual
                                                                          views and conclusions contained in this paper are those of the
components [136], causing 63% of errors in multi-modal QA [134].
                                                                          authors and should not be interpreted as representing any funding
Dynamic contrastive decoding and uncertainty-aware fusion proto-
                                                                          agencies. We thank Amazon Research Awards and OpenAI for
cols show promise[43, 105], but require domain-specific adaptations
                                                                          providing us with API credits under the Researcher Access program.
(e.g., aligning radiology images with reports [60, 138]). Future work
must develop unified uncertainty embeddings to harmonize modal-
ity confidence scales and adversarial training against cross-modal        References
                                                                              [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-
backdoor attacks [63, 137].                                                       cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal
• System-level Uncertainty in Agents and Reasoning. As LLMs                       Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774
                                                                                  (2023).
are increasingly deployed as autonomous agents or reasoning en-               [2] Amos Azaria and Tom Mitchell. 2023. The Internal State of an LLM Knows
gines, the propagation and accumulation of uncertainty across steps               When It‘s Lying. (2023), 967–976.
becomes critical. Errors in early steps can lead to cascading failures,       [3] Joris Baan, Wilker Aziz, Barbara Plank, and Raquel Fernández. 2022. Stop
                                                                                  Measuring Calibration When Humans Disagree. In Proceedings of the 2022
especially when the model expresses misplaced confidence. How-                    Conference on Empirical Methods in Natural Language Processing. 1892–1915.
ever, most existing UQ methods operate at one round of outputs                [4] Oleksandr Balabanov and Hampus Linander. 2024. Uncertainty quantification in
                                                                                  fine-tuned LLMs using LoRA ensembles. arXiv preprint arXiv:2402.12264 (2024).
from LLM, lacking mechanisms to capture uncertainty over multi-               [5] Evan Becker and Stefano Soatto. 2024. Cycles of thought: Measuring llm confi-
step reasoning chains or multi-action plans. As studies suggest that              dence through stable explanations. arXiv preprint arXiv:2406.03441 (2024).
LLMs often fail to revise earlier decisions when presented with con-          [6] Jiuhai Chen and Jonas Mueller. 2024. Quantifying Uncertainty in Answers
                                                                                  from any Language Model and Enhancing their Trustworthiness. In Proceedings
tradictory information [14], there is a need for temporally-aware                 of the 62nd Annual Meeting of the Association for Computational Linguistics.
uncertainty tracking. Enhancing LLMs with structured memory or                    5186–5200.
model-based planning, or leveraging graph-based representations               [7] Tiejin Chen, Kuan-Ru Liou, Mithun Shivakoti, Aaryan Gaur, Pragya Kumari,
                                                                                  Meiqi Guo, and Hua Wei. 2025. Abg-SciQA: A dataset for Understanding and Re-
to trace and revise uncertain steps [74, 125], could possibly provide             solving Ambiguity in Scientific Questions. In ICLR 2025 Workshop on Navigating
more reliable behavior.                                                           and Addressing Data Problems for Foundation Models.
                                                                              [8] Tiejin Chen, Xiaoou Liu, Longchao Da, Jia Chen, Vagelis Papalexakis, and Hua
• UQ Evaluation. Evaluating the quality of UQ remains a fun-                      Wei. 2025. Uncertainty Quantification of Large Language Models through
damental challenge. While the binary classification metrics intro-                Multi-Dimensional Responses. arXiv preprint arXiv:2502.16820 (2025).
                                                                              [9] Zizhang Chen, Peizhao Li, Xiaomeng Dong, and Pengyu Hong. 2024. Uncertainty
duced in Section 4.2 are widely used, they are not always suitable:               Quantification for Clinical Outcome Predictions with (Large) Language Models.
many tasks, especially in NLG, cannot be easily reduced to binary                 arXiv preprint arXiv:2411.03497 (2024).
Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey                                        KDD ’25, August 3–7, 2025, Toronto, ON, Canada

 [10] Inyoung Cheong, King Xia, KJ Kevin Feng, Quan Ze Chen, and Amy X Zhang.                [32] Olga Golovneva, Moya Peng Chen, Spencer Poff, Martin Corredor, Luke Zettle-
      2024. (A) I am not A lawyer, but...: engaging legal experts towards responsible             moyer, Maryam Fazel-Zarandi, and Asli Celikyilmaz. [n. d.]. ROSCOE: A Suite
      LLM policies for legal advice. In Proceedings of the 2024 ACM Conference on                 of Metrics for Scoring Step-by-Step Reasoning. In The Eleventh International
      Fairness, Accountability, and Transparency. 2454–2469.                                      Conference on Learning Representations.
 [11] John Cherian, Isaac Gibbs, and Emmanuel Candes. 2025. Large language model             [33] Meiqi Guo, Mingda Zhang, Siva Reddy, and Malihe Alikhani. 2021. Abg-coqa:
      validity via enhanced conformal prediction methods. Advances in Neural Infor-               Clarifying ambiguity in conversational question answering. 3rd Conference on
      mation Processing Systems 37 (2025), 114812–114842.                                         Automated Knowledge Base Construction (2021).
 [12] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun,                 [34] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn
      Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano,             Song, and Jacob Steinhardt. 2020. Measuring massive multitask language un-
      Christopher Hesse, and John Schulman. 2021. Training Verifiers to Solve Math                derstanding. arXiv preprint arXiv:2009.03300 (2020).
      Word Problems. arXiv preprint arXiv:2110.14168 (2021).                                 [35] Jay Heo, Hae Beom Lee, Saehoon Kim, Juho Lee, Kwang Joon Kim, Eunho
 [13] Jeremy Cole, Michael Zhang, Dan Gillick, Julian Eisenschlos, Bhuwan Dhingra,                Yang, and Sung Ju Hwang. 2018. Uncertainty-aware attention for reliable
      and Jacob Eisenstein. 2023. Selectively Answering Ambiguous Questions. In                   interpretation and prediction. Advances in neural information processing systems
      Proceedings of the 2023 Conference on Empirical Methods in Natural Language                 31 (2018).
      Processing. 530–543.                                                                   [36] Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas, Shiyu Chang, and Yang
 [14] Antonia Creswell, Murray Shanahan, and Irina Higgins. [n. d.]. Selection-                   Zhang. 2024. Decomposing Uncertainty for Large Language Models through
      Inference: Exploiting Large Language Models for Interpretable Logical Rea-                  Input Clarification Ensembling. In Forty-first International Conference on Machine
      soning. In The Eleventh International Conference on Learning Representations.               Learning.
 [15] Longchao Da, Tiejin Chen, Lu Cheng, and Hua Wei. 2024. Llm uncertainty                 [37] Hsiu-Yuan Huang, Yutong Yang, Zhaoxi Zhang, Sanwoo Lee, and Yunfang Wu.
      quantification through directional entailment graph and claim level response                2024. A survey of uncertainty estimation in llms: Theory meets practice. arXiv
      augmentation. arXiv preprint arXiv:2407.00994 (2024).                                       preprint arXiv:2410.15326 (2024).
 [16] Longchao Da, Minquan Gao, Hao Mei, and Hua Wei. 2024. Prompt to transfer:              [38] Jingwang Huang, Jiang Zhong, Qin Lei, Jinpeng Gao, Yuming Yang, Sirui Wang,
      Sim-to-real transfer for traffic signal control with prompt learning. In Proceedings        Peiguang Li, and Kaiwen Wei. 2025. Latent Distribution Decoupling: A Proba-
      of the AAAI Conference on Artificial Intelligence, Vol. 38. 82–90.                          bilistic Framework for Uncertainty-Aware Multimodal Emotion Recognition.
 [17] Longchao Da, Kuanru Liou, Tiejin Chen, Xuesong Zhou, Xiangyong Luo, Yezhou                  arXiv preprint arXiv:2502.13954 (2025).
      Yang, and Hua Wei. 2024. Open-ti: Open traffic intelligence with augmented             [39] Lifu Huang, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi. 2019. Cosmos
      language model. International Journal of Machine Learning and Cybernetics 15,               QA: Machine reading comprehension with contextual commonsense reasoning.
      10 (2024), 4761–4786.                                                                       arXiv preprint arXiv:1909.00277 (2019).
 [18] Longchao Da, Xiaoou Liu, Jiaxin Dai, Lu Cheng, Yaqing Wang, and Hua Wei.               [40] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian
      2025. Understanding the Uncertainty of LLM Explanations: A Perspective Based                Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, et al. 2025.
      on Reasoning Topology. arXiv preprint arXiv:2502.17026 (2025).                              A survey on hallucination in large language models: Principles, taxonomy,
 [19] Longchao Da, Hao Mei, Romir Sharma, and Hua Wei. 2023. Uncertainty-aware                    challenges, and open questions. ACM Transactions on Information Systems 43, 2
      grounded action transformation towards sim-to-real transfer for traffic signal              (2025), 1–55.
      control. In 2023 62nd IEEE Conference on Decision and Control (CDC). 1124–1129.        [41] Yukun Huang, Yixin Liu, Raghuveer Thirukovalluru, Arman Cohan, and Bhuwan
 [20] Longchao Da, Rui Wang, Xiaojian Xu, Parminder Bhatia, Taha Kass-Hout, Hua                   Dhingra. 2024. Calibrating Long-form Generations From Large Language Mod-
      Wei, and Cao Xiao. 2024. Segment as You Wish–Free-Form Language-Based                       els. In Findings of the Association for Computational Linguistics: EMNLP 2024.
      Segmentation for Medical Images. arXiv preprint arXiv:2410.12831 (2024).                    13441–13460.
 [21] Irene de Zarzà, Joachim de Curtò, Gemma Roig, and Carlos T Calafate. 2023.             [42] Eyke Hüllermeier and Willem Waegeman. 2021. Aleatoric and epistemic uncer-
      LLM multimodal traffic accident forecasting. Sensors 23, 22 (2023), 9225.                   tainty in machine learning: An introduction to concepts and methods. Machine
 [22] Yang Deng, Shuaiyi Li, and Wai Lam. 2023. Learning to ask clarification ques-               learning 110, 3 (2021), 457–506.
      tions with spatial reasoning. In Proceedings of the 46th International ACM SIGIR       [43] Fushuo Huo, Wenchao Xu, Zhong Zhang, Haozhao Wang, Zhicheng Chen, and
      Conference on Research and Development in Information Retrieval. 2113–2117.                 Peilin Zhao. 2024. Self-introspective decoding: Alleviating hallucinations for
 [23] Armen Der Kiureghian and Ove Ditlevsen. 2009. Aleatory or epistemic? Does it                large vision-language models. arXiv preprint arXiv:2408.02032 (2024).
      matter? Structural safety 31, 2 (2009), 105–112.                                       [44] Abhyuday Jagannatha and Hong Yu. 2020. Calibrating Structured Output
 [24] Jinhao Duan, Hao Cheng, Shiqi Wang, Alex Zavalny, Chenan Wang, Renjing Xu,                  Predictors for Natural Language Processing. In Proceedings of the 58th Annual
      Bhavya Kailkhura, and Kaidi Xu. 2024. Shifting Attention to Relevance: Towards              Meeting of the Association for Computational Linguistics. 2078–2092.
      the Predictive Uncertainty Quantification of Free-Form Large Language Models.          [45] Heinrich Jiang, Been Kim, Maya Gupta, and Melody Y. Guan. 2018. To trust or
      In Proceedings of the 62nd Annual Meeting of the Association for Computational              not to trust a classifier. In Advances in Neural Information Processing Systems.
      Linguistics (Volume 1: Long Papers). 5050–5063.                                        [46] Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham Neubig. 2021. How Can We
 [25] Yanai Elazar, Nora Kassner, Shauli Ravfogel, Abhilasha Ravichander, Eduard                  Know When Language Models Know? On the Calibration of Language Models
      Hovy, Hinrich Schütze, and Yoav Goldberg. 2021. Measuring and improving                     for Question Answering. Transactions of the Association for Computational
      consistency in pretrained language models. Transactions of the Association for              Linguistics (2021), 962–977.
      Computational Linguistics 9 (2021), 1012–1031.                                         [47] Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng, Hanyi Fang, and Peter
 [26] Ekaterina Fadeeva, Aleksandr Rubashevskii, Artem Shelmanov, Sergey Petrakov,                Szolovits. 2021. What disease does this patient have? a large-scale open domain
      Haonan Li, Hamdy Mubarak, Evgenii Tsymbalov, Gleb Kuzmin, Alexander                         question answering dataset from medical exams. Applied Sciences 11, 14 (2021),
      Panchenko, Timothy Baldwin, et al. 2024. Fact-Checking the Output of Large                  6421.
      Language Models via Token-Level Uncertainty Quantification. In Findings of             [48] Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer. 2017. Trivi-
      the Association for Computational Linguistics ACL 2024. 9367–9385.                          aQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Com-
 [27] Ekaterina Fadeeva, Roman Vashurin, Akim Tsvigun, Artem Vazhentsev, Sergey                   prehension. In Proceedings of the 55th Annual Meeting of the Association for
      Petrakov, Kirill Fedyanin, Daniil Vasilev, Elizaveta Goncharova, Alexander                  Computational Linguistics. 1601–1611.
      Panchenko, Maxim Panov, et al. 2023. LM-Polygraph: Uncertainty Estima-                 [49] Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain,
      tion for Language Models. In Proceedings of the 2023 Conference on Empirical                Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-
      Methods in Natural Language Processing: System Demonstrations. 446–461.                     Johnson, et al. 2022. Language models (mostly) know what they know. arXiv
 [28] Yarin Gal and Zoubin Ghahramani. 2016. Dropout as a bayesian approximation:                 preprint arXiv:2207.05221 (2022).
      Representing model uncertainty in deep learning. In international conference on        [50] Sanyam Kapoor, Nate Gruver, Manley Roberts, Arka Pal, Samuel Dooley, Micah
      machine learning. PMLR, 1050–1059.                                                          Goldblum, and Andrew Wilson. 2024. Calibration-Tuning: Teaching Large
 [29] Xiang Gao, Jiaxin Zhang, Lalla Mouatadid, and Kamalika Das. 2024. SPUQ:                     Language Models to Know What They Don‘t Know. In Proceedings of the 1st
      Perturbation-Based Uncertainty Quantification for Large Language Models. In                 Workshop on Uncertainty-Aware NLP (UncertaiNLP 2024). 1–14.
      Proceedings of the 18th Conference of the European Chapter of the Association for      [51] Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023. Semantic Uncertainty:
      Computational Linguistics (Volume 1: Long Papers). 2336–2346.                               Linguistic Invariances for Uncertainty Estimation in Natural Language Genera-
 [30] Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Be-              tion. In The Eleventh International Conference on Learning Representations.
      rant. 2021. Did Aristotle Use a Laptop? A Question Answering Benchmark with            [52] Aviral Kumar and Sunita Sarawagi. 2019. Calibration of encoder decoder models
      Implicit Reasoning Strategies. Transactions of the Association for Computational            for neural machine translation. arXiv preprint arXiv:1903.00802 (2019).
      Linguistics (2021), 346–361.                                                           [53] Bhawesh Kumar, Charlie Lu, Gauri Gupta, Anil Palepu, David Bellamy, Ramesh
 [31] Mario Giulianelli, Joris Baan, Wilker Aziz, Raquel Fernández, and Barbara Plank.            Raskar, and Andrew Beam. 2023. Conformal prediction with large language
      2023. What Comes Next? Evaluating Uncertainty in Neural Text Generators                     models for multi-choice question answering. arXiv preprint arXiv:2305.18404
      Against Human Production Variability. In Proceedings of the 2023 Conference on              (2023).
      Empirical Methods in Natural Language Processing. 14349–14371.
KDD ’25, August 3–7, 2025, Toronto, ON, Canada                                                                                                                        Liu et al.

 [54] Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang, and Eduard Hovy. 2017.                 Models. In 2023 Conference on Empirical Methods in Natural Language Processing.
      RACE: Large-scale ReAding Comprehension Dataset From Examinations. In              [77] Katerina Margatina, Timo Schick, Nikolaos Aletras, and Jane Dwivedi-Yu. 2023.
      Proceedings of the 2017 Conference on Empirical Methods in Natural Language             Active Learning Principles for In-Context Learning with Large Language Models.
      Processing. 785–794.                                                                    In Findings of the Association for Computational Linguistics. 5011–5034.
 [55] Siqi Lai, Zhao Xu, Weijia Zhang, Hao Liu, and Hui Xiong. 2025. LLMLight:           [78] Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Koh,
      Large Language Models as Traffic Signal Control Agents. 31st ACM SIGKDD                 Mohit yyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. 2023. FActScore: Fine-
      Conference on Knowledge Discovery and Data Mining (2025).                               grained Atomic Evaluation of Factual Precision in Long Form Text Generation.
 [56] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. 2017. Simple          In Proceedings of the 2023 Conference on Empirical Methods in Natural Language
      and scalable predictive uncertainty estimation using deep ensembles. Advances           Processing. 12076–12100.
      in neural information processing systems 30 (2017).                                [79] Sewon Min, Julian Michael, Hannaneh Hajishirzi, and Luke Zettlemoyer. 2020.
 [57] Baolin Li, Yankai Jiang, Vijay Gadepally, and Devesh Tiwari. 2024. Llm in-              AmbigQA: Answering Ambiguous Open-domain Questions. In EMNLP.
      ference serving: Survey of recent advances and opportunities. arXiv preprint       [80] Shentong Mo and Miao Xin. 2024. Tree of uncertain thoughts reasoning for
      arXiv:2407.12391 (2024).                                                                large language models. In ICASSP 2024-2024 IEEE International Conference on
 [58] Junyi Li, Xiaoxue Cheng, Wayne Xin Zhao, Jian-Yun Nie, and Ji-Rong Wen.                 Acoustics, Speech and Signal Processing (ICASSP). IEEE, 12742–12746.
      2023. HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large         [81] Philipp Mondorf and Barbara Plank. 2024. Beyond Accuracy: Evaluating the
      Language Models. In Proceedings of the 2023 Conference on Empirical Methods in          Reasoning Behavior of Large Language Models-A Survey. In First Conference on
      Natural Language Processing. 6449–6464.                                                 Language Modeling.
 [59] Lincan Li, Jiaqi Li, Catherine Chen, Fred Gui, Hongjia Yang, Chenxiao Yu, Zheng-   [82] Maria Mora-Cross and Saul Calderon-Ramirez. 2024. Uncertainty estimation
      guang Wang, Jianing Cai, Junlong Aaron Zhou, Bolin Shen, et al. 2024. Political-        in large language models to support biodiversity conservation. In Proceedings
      llm: Large language models in political science. arXiv preprint arXiv:2412.06864        of the 2024 Conference of the North American Chapter of the Association for
      (2024).                                                                                 Computational Linguistics: Human Language Technologies (Volume 6: Industry
 [60] Yaowei Li, Bang Yang, Xuxin Cheng, Zhihong Zhu, Hongxiang Li, and Yuexian               Track). 368–378.
      Zou. 2023. Unify, align and refine: Multi-level semantic alignment for radiology   [83] Subhabrata Mukherjee and Ahmed Awadallah. 2020. Uncertainty-aware self-
      report generation. In Proceedings of the IEEE/CVF international conference on           training for few-shot text classification. Advances in Neural Information Process-
      computer vision. 2863–2874.                                                             ing Systems 33 (2020), 21199–21212.
 [61] Zixuan Li, Jing Xiong, Fanghua Ye, Chuanyang Zheng, Xun Wu, Jianqiao Lu,           [84] James F Mullen Jr and Dinesh Manocha. 2024. LAP, Using Action Feasibility
      Zhongwei Wan, Xiaodan Liang, Chengming Li, Zhenan Sun, et al. 2024. Un-                 for Improved Uncertainty Alignment of Large Language Model Planners. arXiv
      certaintyRAG: Span-Level Uncertainty Enhanced Long-Context Modeling for                 preprint arXiv:2403.13198 (2024).
      Retrieval-Augmented Generation. arXiv preprint arXiv:2410.02719 (2024).            [85] Allan H. Murphy and Robert L. Winkler. 1977. Reliability of Subjective Probabil-
 [62] Kaiqu Liang, Zixu Zhang, and Jaime Fisac. 2024. Introspective Planning: Align-          ity Forecasts of Precipitation and Temperature. Journal of The Royal Statistical
      ing Robots’ Uncertainty with Inherent Task Ambiguity. Advances in Neural                Society Series C-applied Statistics 26 (1977), 41–47.
      Information Processing Systems 37 (2024), 71998–72031.                             [86] Malik Sajjad Ahmed Nadeem, Jean-Daniel Zucker, and Blaise Hanczar. 2009.
 [63] Siyuan Liang, Jiawei Liang, Tianyu Pang, Chao Du, Aishan Liu, Ee-Chien Chang,           Accuracy-rejection curves (ARCs) for comparing classification methods with a
      and Xiaochun Cao. 2024. Revisiting backdoor attacks against large vision-               reject option. In Machine Learning in Systems Biology. 65–81.
      language models. arXiv preprint arXiv:2406.18844 (2024).                           [87] Alexander Nikitin, Jannik Kossen, Yarin Gal, and Pekka Marttinen. 2024. Kernel
 [64] Stephanie Lin, Jacob Hilton, and Owain Evans. 2022. Teaching models to express          language entropy: Fine-grained uncertainty quantification for LLMs from se-
      their uncertainty in words. arXiv preprint arXiv:2205.14334 (2022).                     mantic similarities. Advances in Neural Information Processing Systems 37 (2024),
 [65] Stephanie Lin, Jacob Hilton, and Owain Evans. 2022. TruthfulQA: Measuring               8901–8929.
      How Models Mimic Human Falsehoods. In Proceedings of the 60th Annual Meet-         [88] Hyobin Ong, Youngwoo Yoon, Jaewoo Choi, and Minsu Jang. 2024. A Simple
      ing of the Association for Computational Linguistics (Volume 1: Long Papers).           Baseline for Uncertainty-Aware Language-Oriented Task Planner for Embodied
      3214–3252.                                                                              Agents. In 2024 21st International Conference on Ubiquitous Robots (UR). 677–682.
 [66] Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. 2023. Generating with Confi-          [89] Arjun Panickssery, Samuel Bowman, and Shi Feng. 2024. Llm evaluators recog-
      dence: Uncertainty Quantification for Black-box Large Language Models. Trans-           nize and favor their own generations. Advances in Neural Information Processing
      actions on Machine Learning Research (2023).                                            Systems 37 (2024), 68772–68802.
 [67] Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. 2024. Contextualized Sequence         [90] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. Bleu: a
      Likelihood: Enhanced Confidence Scores for Natural Language Generation. In              method for automatic evaluation of machine translation. In Proceedings of the
      Proceedings of the 2024 Conference on Empirical Methods in Natural Language             40th annual meeting of the Association for Computational Linguistics. 311–318.
      Processing. 10351–10368.                                                           [91] Jianing Qiu, Kyle Lam, Guohao Li, Amish Acharya, Tien Yin Wong, Ara Darzi,
 [68] Chen Ling, Xujiang Zhao, Xuchao Zhang, Wei Cheng, Yanchi Liu, Yiyou Sun,                Wu Yuan, and Eric J Topol. 2024. LLM-based agentic systems in medicine and
      Mika Oishi, Takao Osaki, Katsushi Matsuda, Jie Ji, Guangji Bai, Liang Zhao, and         healthcare. Nature Machine Intelligence 6, 12 (2024), 1418–1420.
      Haifeng Chen. 2024. Uncertainty Quantification for In-Context Learning of          [92] Victor Quach, Adam Fisch, Tal Schuster, Adam Yala, Jae Ho Sohn, Tommi S
      Large Language Models. In Proceedings of the 2024 Conference of the North Amer-         Jaakkola, and Regina Barzilay. [n. d.]. Conformal Language Modeling. In The
      ican Chapter of the Association for Computational Linguistics: Human Language           Twelfth International Conference on Learning Representations.
      Technologies (Volume 1: Long Papers). 3357–3370.                                   [93] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. 2016.
 [69] Linyu Liu, Yu Pan, Xiaocheng Li, and Guanting Chen. 2024. Uncertainty estima-           Squad: 100,000+ questions for machine comprehension of text. arXiv preprint
      tion and quantification for llms: A simple supervised approach. arXiv preprint          arXiv:1606.05250 (2016).
      arXiv:2404.15993 (2024).                                                           [94] Siva Reddy, Danqi Chen, and Christopher D Manning. 2019. Coqa: A con-
 [70] Shudong Liu, Zhaocong Li, Xuebo Liu, Runzhe Zhan, Derek Wong, Lidia Chao,               versational question answering challenge. Transactions of the Association for
      and Min Zhang. 2024. Can LLMs learn uncertainty on their own? expressing                Computational Linguistics 7 (2019), 249–266.
      uncertainty effectively in a self-training manner. In Proceedings of the 2024      [95] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe
      Conference on Empirical Methods in Natural Language Processing. 21635–21645.            Pang, Julien Dirani, Julian Michael, and Samuel R Bowman. 2024. Gpqa: A
 [71] Xin Liu, Muhammad Khalifa, and Lu Wang. 2024. LitCab: Lightweight Lan-                  graduate-level google-proof q&a benchmark. In First Conference on Language
      guage Model Calibration over Short- and Long-form Responses. In The Twelfth             Modeling.
      International Conference on Learning Representations.                              [96] Jie Ren, Jiaming Luo, Yao Zhao, Kundan Krishna, Mohammad Saleh, Balaji Laksh-
 [72] Xiaoou Liu, Zhen Lin, Longchao Da, Chacha Chen, Shubhendu Trivedi, and                  minarayanan, and Peter J Liu. 2023. Out-of-Distribution Detection and Selective
      Hua Wei. 2025. MCQA-Eval: Efficient Confidence Evaluation in NLG with                   Generation for Conditional Language Models. In The Eleventh International
      Gold-Standard Correctness Labels. arXiv preprint arXiv:2502.14268 (2025).               Conference on Learning Representations.
 [73] Jinliang Lu, Ziliang Pang, Min Xiao, Yaochen Zhu, Rui Xia, and Jiajun Zhang.       [97] Jie Ren, Yao Zhao, Tu Vu, Peter J. Liu, and Balaji Lakshminarayanan. 2023.
      2024. Merge, ensemble, and cooperate! a survey on collaborative strategies in           Self-Evaluation Improves Selective Generation in Large Language Models. In
      the era of large language models. arXiv preprint arXiv:2407.06089 (2024).               Proceedings on "I Can’t Believe It’s Not Better: Failure Modes in the Age of Foun-
 [74] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah              dation Models" at NeurIPS 2023 Workshops, Vol. 239. 49–64.
      Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al.          [98] Thomas Savage, John Wang, Robert Gallo, Abdessalem Boukil, Vishwesh Patel,
      2023. Self-refine: Iterative refinement with self-feedback. Advances in Neural          Seyed Amir Ahmad Safavi-Naini, Ali Soroush, and Jonathan H Chen. 2024. Large
      Information Processing Systems 36 (2023), 46534–46594.                                  language model uncertainty measurement and calibration for medical diagnosis
 [75] Andrey Malinin and Mark Gales. 2021. Uncertainty Estimation in Autoregressive           and treatment. medRxiv (2024), 2024–06.
      Structured Prediction. In International Conference on Learning Representations.    [99] Sagar Sen, Victor Gonzalez, Erik Johannes Husom, Simeon Tverdal, Shukun
 [76] Potsawee Manakul, Adian Liusie, and Mark Gales. [n. d.]. SelfCheckGPT: Zero-            Tokas, and Svein O Tjøsvoll. 2024. ERG-AI: enhancing occupational ergonomics
      Resource Black-Box Hallucination Detection for Generative Large Language                with uncertainty-aware ML and LLM feedback. Applied Intelligence 54, 23 (2024),
Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey                                        KDD ’25, August 3–7, 2025, Toronto, ON, Canada

      12128–12155.                                                                               International Conference on Learning Representations.
[100] Murat Sensoy, Lance Kaplan, and Melih Kandemir. 2018. Evidential deep learning       [122] Yongjin Yang, Haneul Yoo, and Hwaran Lee. 2025. MAQA: Evaluating Uncer-
      to quantify classification uncertainty. Advances in neural information processing          tainty Quantification in LLMs Regarding Data Uncertainty. In Findings of the
      systems 31 (2018).                                                                         Association for Computational Linguistics: NAACL 2025. 5846–5863.
[101] Glenn Shafer and Vladimir Vovk. 2008. A tutorial on conformal prediction.            [123] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan
      Journal of Machine Learning Research 9, 3 (2008).                                          Salakhutdinov, and Christopher D Manning. 2018. HotpotQA: A dataset for di-
[102] Ola Shorinwa, Zhiting Mei, Justin Lidard, Allen Z Ren, and Anirudha Majum-                 verse, explainable multi-hop question answering. arXiv preprint arXiv:1809.09600
      dar. 2024. A survey on uncertainty quantification of large language models:                (2018).
      Taxonomy, open research challenges, and future directions. arXiv preprint            [124] Huaiyuan Yao, Longchao Da, Vishnu Nandam, Justin Turnau, Zhiwei Liu, Linsey
      arXiv:2412.05563 (2024).                                                                   Pang, and Hua Wei. 2025. Comal: Collaborative multi-agent large language
[103] Elias Stengel-Eskin and Benjamin Van Durme. 2023. Calibrated Interpretation:               models for mixed-autonomy traffic. In Proceedings of the 2025 SIAM International
      Confidence Estimation in Semantic Parsing. Transactions of the Association for             Conference on Data Mining (SDM). 409–418.
      Computational Linguistics 11 (2023), 1213–1231.                                      [125] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and
[104] Jiayuan Su, Jing Luo, Hongwei Wang, and Lu Cheng. 2024. API Is Enough:                     Karthik Narasimhan. 2023. Tree of thoughts: Deliberate problem solving with
      Conformal Prediction for Large Language Models Without Logit-Access. In                    large language models. Advances in neural information processing systems 36
      Findings of the Association for Computational Linguistics: EMNLP 2024. 979–995.            (2023), 11809–11822.
[105] Wei Suo, Lijun Zhang, Mengyang Sun, Lin Yuanbo Wu, Peng Wang, and Yanning            [126] Fanghua Ye, Mingming Yang, Jianhui Pang, Longyue Wang, Derek Wong, Emine
      Zhang. 2025. Octopus: Alleviating Hallucination via Dynamic Contrastive                    Yilmaz, Shuming Shi, and Zhaopeng Tu. 2025. Benchmarking llms via uncer-
      Decoding. arXiv preprint arXiv:2503.00361 (2025).                                          tainty quantification. Advances in Neural Information Processing Systems (2025),
[106] James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal.              15356–15385.
      2018. FEVER: a large-scale dataset for fact extraction and VERification. arXiv       [127] Kai Ye, Tiejin Chen, Hua Wei, and Liang Zhan. 2024. Uncertainty regularized evi-
      preprint arXiv:1803.05355 (2018).                                                          dential regression. In Proceedings of the AAAI Conference on Artificial Intelligence,
[107] Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov,                 Vol. 38. 16460–16468.
      Huaxiu Yao, Chelsea Finn, and Christopher Manning. 2023. Just Ask for Cali-          [128] Zhangyue Yin, Qiushi Sun, Qipeng Guo, Zhiyuan Zeng, Xiaonan Li, Junqi
      bration: Strategies for Eliciting Calibrated Confidence Scores from Language               Dai, Qinyuan Cheng, Xuan-Jing Huang, and Xipeng Qiu. 2024. Reasoning in
      Models Fine-Tuned with Human Feedback. In Proceedings of the 2023 Conference               flux: Enhancing large language models reasoning through uncertainty-aware
      on Empirical Methods in Natural Language Processing. 5433–5442.                            adaptive guidance. In Proceedings of the 62nd Annual Meeting of the Association
[108] Yao-Hung Hubert Tsai, Walter Talbott, and Jian Zhang. 2024. Efficient Non-                 for Computational Linguistics (Volume 1: Long Papers). 2401–2416.
      Parametric Uncertainty Quantification for Black-Box Large Language Models            [129] Spencer Young, Porter Jenkins, Lonchao Da, Jeff Dotson, and Hua Wei. 2025.
      and Decision Planning. arXiv preprint arXiv:2402.00251 (2024).                             Flexible heteroscedastic count regression with deep double poisson networks.
[109] Dennis Ulmer, Martin Gubri, Hwaran Lee, Sangdoo Yun, and Seong Oh. 2024.                   International Conference on Machine Learning (2025).
      Calibrating Large Language Models Using Their Generations Only. In Proceed-          [130] Hamed Zamani, Susan Dumais, Nick Craswell, Paul Bennett, and Gord Lueck.
      ings of the 62nd Annual Meeting of the Association for Computational Linguistics           2020. Generating clarifying questions for information retrieval. In Proceedings
      (Volume 1: Long Papers). 15440–15459.                                                      of the web conference 2020. 418–428.
[110] Roman Vashurin, Ekaterina Fadeeva, Artem Vazhentsev, Lyudmila Rvanova,               [131] Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. 2019.
      Daniil Vasilev, Akim Tsvigun, Sergey Petrakov, Rui Xing, Abdelrahman Sadallah,             HellaSwag: Can a Machine Really Finish Your Sentence?. In Proceedings of the
      Kirill Grishchenkov, Alexander Panchenko, Timothy Baldwin, Preslav Nakov,                  57th Annual Meeting of the Association for Computational Linguistics. 4791–4800.
      Maxim Panov, and Artem Shelmanov. 2025. Benchmarking Uncertainty Quan-               [132] Boxuan Zhang and Ruqi Zhang. 2025. CoT-UQ: Improving Response-wise
      tification Methods for Large Language Models with LM-Polygraph. Transactions               Uncertainty Quantification in LLMs with Chain-of-Thought. arXiv preprint
      of the Association for Computational Linguistics (2025), 220–248.                          arXiv:2502.17214 (2025).
[111] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,             [133] Caiqi Zhang, Fangyu Liu, Marco Basaldella, and Nigel Collier. 2024. LUQ: Long-
      Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you             text Uncertainty Quantification for LLMs. In Proceedings of the 2024 Conference
      need. Advances in neural information processing systems 30 (2017).                         on Empirical Methods in Natural Language Processing. 5244–5262.
[112] Artem Vazhentsev, Gleb Kuzmin, Akim Tsvigun, Alexander Panchenko, Maxim              [134] Ruiyang Zhang, Hu Zhang, and Zhedong Zheng. 2024. VL-Uncertainty: Detect-
      Panov, Mikhail Burtsev, and Artem Shelmanov. 2023. Hybrid uncertainty quan-                ing Hallucination in Large Vision-Language Model via Uncertainty Estimation.
      tification for selective text classification in ambiguous tasks. In Proceedings of         arXiv preprint arXiv:2411.11919 (2024).
      the 61st Annual Meeting of the Association for Computational Linguistics (Volume     [135] Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q Weinberger, and Yoav Artzi.
      1: Long Papers). 11659–11681.                                                              [n. d.]. BERTScore: Evaluating Text Generation with BERT. In International
[113] Boshi Wang, Xiang Yue, Yu Su, and Huan Sun. 2024. Grokking of implicit                     Conference on Learning Representations.
      reasoning in transformers: A mechanistic journey to the edge of generalization.      [136] Yuan Zhang, Tao Huang, Chun-Kai Fan, Hongyuan Dong, Jiawen Li, Jiacong
      Advances in Neural Information Processing Systems 37 (2024), 95238–95265.                  Wang, Kuan Cheng, Shanghang Zhang, Haoyuan Guo, et al. 2024. Unveiling the
[114] Shuo Wang, Zhaopeng Tu, Shuming Shi, and Yang Liu. 2020. On the Inference                  tapestry of consistency in large vision-language models. Advances in Neural
      Calibration of Neural Machine Translation. In Proceedings of the 58th Annual               Information Processing Systems 37 (2024), 118632–118653.
      Meeting of the Association for Computational Linguistics.                            [137] Zheng Zhang, Xu Yuan, Lei Zhu, Jingkuan Song, and Liqiang Nie. 2024. BadCM:
[115] Yibin Wang, Haizhou Shi, Ligong Han, Dimitris Metaxas, and Hao Wang. 2025.                 Invisible backdoor attack against cross-modal learning. IEEE Transactions on
      Blob: Bayesian low-rank adaptation by backpropagation for large language                   Image Processing (2024).
      models. Advances in Neural Information Processing Systems 37 (2025), 67758–          [138] Guosheng Zhao, Zijian Zhao, Wuxian Gong, and Feng Li. 2023. Radiology report
      67794.                                                                                     generation with medical knowledge and multilevel image-report alignment: A
[116] Zhiyuan Wang, Jinhao Duan, Lu Cheng, Yue Zhang, Qingni Wang, Xiaoshuang                    new method and its verification. Artificial Intelligence in Medicine 146 (2023),
      Shi, Kaidi Xu, Heng Tao Shen, and Xiaofeng Zhu. 2024. ConU: Conformal                      102714.
      Uncertainty in Large Language Models with Correctness Coverage Guarantees.           [139] Yao Zhao, Mikhail Khalman, Rishabh Joshi, Shashi Narayan, Mohammad Saleh,
      In Findings of the Association for Computational Linguistics. 6886–6898.                   and Peter J Liu. 2023. Calibrating Sequence likelihood Improves Conditional
[117] Jiaxin Wu, Yizhou Yu, and Hong-Yu Zhou. 2024. Uncertainty Estimation                       Language Generation. In The Eleventh International Conference on Learning
      of Large Language Models in Medical Question Answering. arXiv preprint                     Representations.
      arXiv:2407.08662 (2024).                                                             [140] Chujie Zheng, Hao Zhou, Fandong Meng, Jie Zhou, and Minlie Huang. 2023.
[118] Shuo Xing, Yuping Wang, Peiran Li, Ruizheng Bai, Yueqi Wang, Chan-wei Hu,                  Large language models are not robust multiple choice selectors. arXiv preprint
      Chengxuan Qian, Huaxiu Yao, and Zhengzhong Tu. 2025. Re-Align: Aligning Vi-                arXiv:2309.03882 (2023).
      sion Language Models via Retrieval-Augmented Direct Preference Optimization.         [141] Zhi Zheng, Qian Feng, Hang Li, Alois Knoll, and Jianxiang Feng. 2024. Evaluating
      arXiv preprint arXiv:2502.13146 (2025).                                                    uncertainty-based failure detection for closed-loop llm planners. arXiv preprint
[119] Miao Xiong, Zhiyuan Hu, Xinyang Lu, YIFEI LI, Jie Fu, Junxian He, and Bryan                arXiv:2406.00430 (2024).
      Hooi. 2024. Can LLMs Express Their Uncertainty? An Empirical Evaluation
      of Confidence Elicitation in LLMs. In The Twelfth International Conference on        Received 11 March 2025; accepted 6 May 2025
      Learning Representations.
[120] Miao Xiong, Andrea Santilli, Michael Kirchhof, Adam Golinski, and Sinead
      Williamson. 2024. Efficient and effective uncertainty quantification for LLMs.
      In Neurips Safe Generative AI Workshop 2024.
[121] Adam X Yang, Maxime Robeyns, Xi Wang, and Laurence Aitchison. [n. d.].
      Bayesian Low-rank Adaptation for Large Language Models. In The Twelfth

```
