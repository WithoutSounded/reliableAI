---
citation_key: "GengEtAl2023"
title: "A Survey of Confidence Estimation and Calibration in Large Language Models"
authors: "Jiahui Geng; Fengyu Cai; Yuxia Wang; Heinz Koeppl; Preslav Nakov; Iryna Gurevych"
year: 2023
doi: "10.48550/arxiv.2311.08298"
source: "local PDF (Jiahui2024.pdf)"
access_level: "full-text-pdf"
retrieved_date: "2026-04-15"
arxiv_id: "2311.08298"
is_user_seed: true
tier: 1
composite_score: 4.7
---
# A Survey of Confidence Estimation and Calibration in Large Language Models
**Authors**: Jiahui Geng, Fengyu Cai, Yuxia Wang, Heinz Koeppl, Preslav Nakov, Iryna Gurevych
**Year**: 2023
**Venue**: arXiv (Cornell University)
**DOI**: [10.48550/arxiv.2311.08298](https://doi.org/10.48550/arxiv.2311.08298)

## Full Text (extracted via pdftotext) / 全文（pdftotext 抽取）

```text
                                                          A Survey of Confidence Estimation and Calibration
                                                                      in Large Language Models
                                                                     Jiahui Geng1 , Fengyu Cai2 , Yuxia Wang1 ,
                                                                 Heinz Koeppl2 , Preslav Nakov1 , Iryna Gurevych1
                                                                Mohamed bin Zayed University of Artificial Intelligence
                                                                           Technical University of Darmstadt
                                                       {jiahui.geng, yuxia.wang,preslav.nakov,iryna.gurevych}@mbzuai.ac.ae,
                                                                     {fengyu.cai,heinz.koeppl}@tu-darmstadt.de

                                                               Abstract                              However, applying these methods directly to
                                                                                                  LLMs presents several challenges. The output
                                             Large language models (LLMs) have demon-             space of these models is significantly larger than
                                             strated remarkable capabilities across a wide

arXiv:2311.08298v2 [cs.CL] 25 Mar 2024
                                                                                                  that of discriminative models. The number of pos-
                                             range of tasks in various domains. Despite their
                                             impressive performance, they can be unreliable       sible outcomes grows exponentially with the gen-
                                             due to factual errors in their generations. As-      eration length, making it impossible to access all
                                             sessing their confidence and calibrating them        potential responses. Additionally, different expres-
                                             across different tasks can help mitigate risks       sions may convey the same meaning, suggesting
                                             and enable LLMs to produce better generations.       that confidence estimation should consider seman-
                                             There has been a lot of recent research aiming       tics. Lastly, LLMs show unique properties, such as
                                             to address this, but there has been no compre-
                                                                                                  expressing confidence in words (Lin et al., 2022;
                                             hensive overview to organize it and outline the
                                             main lessons learned. The present survey aims        Xiong et al., 2023) and the ability to perform zero-
                                             to bridge this gap. In particular, we outline the    shot or few-shot learning (Brown et al., 2020a).
                                             challenges and we summarize recent technical         Nonetheless, their responses can be sensitive to
                                             advancements for LLM confidence estimation           the prompts, e.g., the examples provided and their
                                             and calibration. We further discuss their ap-        order, which can cause a lot of instability in the
                                             plications and suggest promising directions for      results. Given this, confidence estimation and cali-
                                             future work.                                         bration for LLMs is growing as an emerging area
                                                                                                  of interest (Jiang et al., 2021; Lin et al., 2022, 2023;
                                         1   Introduction
                                                                                                  Shrivastava et al., 2023).
                                         Large language models (LLMs) have demonstrated              While existing surveys mainly focused on
                                         a wide range of capabilities, such as world knowl-       issues such as hallucination and factuality in
                                         edge storage, sophisticated language-based reason-       LLMs (Zhang et al., 2023b; Wang et al., 2023b),
                                         ing, and in-context learning (Petroni et al., 2019;      there are no comprehensive surveys systematically
                                         Wei et al., 2022; Brown et al., 2020a). However,         discussing the technical advancements in LLMs,
                                         LLMs do not consistently achieve good perfor-            and here we aim to bridge this gap. We explore
                                         mance (Wang et al., 2023a; Zhang et al., 2023b).         the unique challenges posed by LLMs and exam-
                                         Their generation still includes biases (Zhao et al.,     ine the latest studies addressing these issues. We
                                         2021; Wang et al., 2023c) and hallucinations that        first discuss key concepts such as confidence, un-
                                         do not align with reality (Zhang et al., 2023b). Eval-   certainty, and calibration in the context of neural
                                         uating the trustworthiness of responses from these       models, as detailed in Section 2. Then, we pursue
                                         models remains challenging (Liu et al., 2023c).          two different directions: one addressing confidence
                                            Confidence (or uncertainty) estimation is cru-        estimation and calibration techniques for genera-
                                         cial for tasks like out-of-distribution detection and    tion tasks in Section 3, and the other for classifica-
                                         selective prediction (Kendall and Gal, 2017; Lu          tion tasks in Section 4. We conclude by exploring
                                         et al., 2022), and it has been extensively studied       their practical applications (Section 5) and looking
                                         and applied in various contexts (Lee et al., 2018;       at potential future research directions (Section 6).
                                         DeVries and Taylor, 2018). A related concept is          Figure 1 provides a comprehensive representation
                                         that of model calibration, which focuses on align-       of the survey’s structure. By conducting a detailed
                                         ing predictive probabilities (estimated confidence)      examination of existing research, our goal is to il-
                                         to actual accuracy (Guo et al., 2017).                   luminate this vital facet of LLMs, contributing to
                                                                    Classification     Guo et al. (2017); Nixon et al. (2019); Kull et al. (2019); Bradley (1997)
                                                    Metrics
                                                                    Generation         Kumar and Sarawagi (2019); Lin et al. (2023); Zhu et al. (2023a); Huang et al. (2024)

                                                                                                           Logit-based methods               Duan et al. (2023); Kuhn et al. (2023)

                                                                                                           Internal state-based              Ren et al. (2022); Kadavath et al. (2022); Burns et al. (2023)
                                                                                                           methods

 Confidence Estimation and Calibration in LLMs
                                                                                                                                             Li et al. (2023); Azaria and Mitchell (2023)

                                                                                       Estimation          Linguistic confidence             Mielke et al. (2022); Xiong et al. (2023)

                                                                                                           Consistency-based
                                                                                                                                             Manakul et al. (2023b); Lin et al. (2023)
                                                                                                           estimation
                                                                    Generation                             Surrogate models                  Shrivastava et al. (2023); Touvron et al. (2023b)

                                                                                                                                             Kumar and Sarawagi (2019); Wang et al. (2020); Lu et al. (2022)
                                                                                                           Improving generation              Xiao and Wang (2021); van der Poel et al. (2022); Zablotskaia et al. (2023)
                                                                                                                                             Zhao et al. (2022, 2023a)
                                                    Methods                            Calibration
                                                                                                           Improving linguistic
                                                                                                                                             Mielke et al. (2022); Lin et al. (2022); Zhou et al. (2023)
                                                                                                           confidence

                                                                                       Estimation          Logit-based method                Mielke et al. (2022); Lin et al. (2022); Zhou et al. (2023)
                                                                    Classification
                                                                                       Calibration         Bias mitigation                   Zhao et al. (2021); Fei et al. (2023); Nie et al. (2022); Han et al. (2022)

                                                                    Hallucination Detection       Manakul et al. (2023a); Zhang et al. (2023a)
                                                                    and Mitigation                Varshney et al. (2023)

                                                                    Ambiguity detection           Kamath et al. (2020); Zablotskaia et al. (2023)
                                                    Application
                                                                    and selective generation      Cole et al. (2023); Hou et al. (2023)

                                                                    Uncertainty-guided data
                                                                                                  Yu et al. (2022); Su et al. (2022); Jiang et al. (2023)
                                                                    exploitation

                                                                  Figure 1: The taxonomy of confidence estimation and calibration in LLMs.

the development of more reliable applications.                                                                               an event with a 70% probability, that event should
                                                                                                                             actually happen about 70% of the time under sim-
2                                                Preliminaries and Background                                                ilar circumstances. The equation for this relation-
2.1                                               Basic Concepts                                                             ship is as follows:

In machine learning, confidence and uncertainty                                                                                                P (ŷ = y | conf(x, ŷ) = q) = q                                            (2)
are two facets of a single principle: higher confi-
dence corresponds to lower uncertainty (Xiao et al.,                                                                         When the model’s predicted confidence scores con-
2022; Chen and Mueller, 2023). Research on quan-                                                                             sistently align with this principle, the model is con-
tifying model confidence has led to the develop-                                                                             sidered to be well-calibrated.
ment of two key concepts: relative confidence score                                                                             Kendall and Gal (2017) proposed categorizing
and absolute confidence score, offering different                                                                            uncertainty in machine learning into aleatoric and
methods to assess and to interpret confidence lev-                                                                           epistemic uncertainty. Aleatoric or data uncertainty
els (Kamath et al., 2020; Vazhentsev et al., 2023a).                                                                         emerges from the inherent randomness or variabil-
Given input x, ground truth y, and prediction ŷ,                                                                            ity of a system or a process. It is an intrinsic feature
the model’s predictive confidence is denoted as                                                                              of the system and is typically irreducible. Epis-
conf(x, ŷ). Relative confidence scores emphasize                                                                            temic uncertainty, in contrast, is known as model
the ability to rank samples, distinguishing correct                                                                          uncertainty or systematic uncertainty. It arises from
predictions from incorrect ones. Ideally, for every                                                                          the lack of knowledge or information about the
pair of (xi , yi ) and (xj , yj ) and their corresponding                                                                    system being modeled and is reducible, as it can
predictions ŷi and ŷj , we have                                                                                            diminish with the acquisition of more data and im-
                                                                                                                             proved modeling techniques (Gal and Ghahramani,
                                                          conf(xi , ŷi ) ≤ conf(xj , ŷj )                                  2016; Lakshminarayanan et al., 2017).
                                                                                                                 (1)
                                                  ⇐⇒ P (ŷi = yi |xi ) ≤ P (ŷj = yj |xj )
                                                                                                                             2.2        Metrics and Methods
  An absolute confidence score indicates that a                                                                              Metrics Due to the continuous nature of confi-
model’s score reflects its true accuracy in real-                                                                            dence scores, it is impossible to accurately calcu-
world scenarios. For example, if a model predicts                                                                            late the probability as in Eq. 2. Expected calibra-
tion error (ECE; Guo et al. 2017) approximates                    the overall correctness and confidence of answers
it by clustering instances with similar confidence.               directly, especially in tasks like classification and
The predicted probabilities are first segmented into              question answering (Lin et al., 2022; Kadavath
various bins. ECE is then calculated by taking the                et al., 2022). Huang et al. (2024) treated correct-
weighted average of the discrepancies between the                 ness as distributions instead of binary values, as-
mean predicted probability and the actual accuracy                sessing calibration through the distance between
across all bins Bm , m = 1 · · · , M :                            correctness and confidence.
            M                                                     Methods in discriminative models Common
            X |Bm |
 ECE =                  |acc(Bm ) − conf (Bm )| (3)               methods for confidence estimation include logit-
                   N
           m=1                                                    based methods (Pearce et al., 2021; Pereyra
One drawback of the ECE metric is its sensitivity                 et al., 2017), ensemble-based and Bayesian meth-
to various factors such as bucket width and the vari-             ods (Lakshminarayanan et al., 2017; Gal and
ance of samples within these buckets. To overcome                 Ghahramani, 2016), density-based methods (Lee
these issues, more sophisticated schemes have been                et al., 2018), and confidence-learning methods (De-
developed, including static calibration error (SCE),              Vries and Taylor, 2018). Model calibration (Guo
adaptive calibration error (ACE; Nixon et al. 2019),              et al., 2017) can either occur during the model’s
and classwise ECE (Kull et al., 2019). ECE can                    training phase, for example, by improving loss
also be visualized as a reliability diagram, which                functions (Szegedy et al., 2016) or be applied after
plots predicted probabilities against observed fre-               the model has been trained, such as temperature
quencies, with points or lines above the diagonal                 scaling (TS; Guo et al. 2017) and feature-based
indicating overconfidence. Additionally, metrics                  calibrators (FBC; Jiang et al. 2021). Table 3 rep-
such as F1 score, area under receiver operating                   resents significant research in the discriminative
characteristic curve (AUROC; Bradley 1997) and                    LMs, with a list of models, tasks, and calibration
area under accuracy-rejection curve (AUARC; Lin                   methods. Due to space limitations, please refer to
et al. 2023), can indicate whether the confidence                 the Appendix A for detailed principles and compar-
score can appropriately differentiate between cor-                isons.
rect and incorrect answers.
   However, it’s necessary to adapt metrics to ef-                3     LLMs for Generation Tasks
fectively process sequence of tokens with seman-                  3.1     Confidence Estimation
tics. A common approach is to evaluate whether
the next token probability is well-calibrated. As-                In this section, we generally divide the methods
suming that yi = yi1 , · · · , yiT denotes the se-                into white-box and black-box methods. We first
quence of generated tokens (target sentence) and                  provide a detailed overview of these methods and
that xi = xi1 , · · · , xiS denotes the sequence of               then summarize their strengths, weaknesses, and
input tokens (source sentence), the probability                   connections.
of generating
            QTthe target sequence can be repre-                   3.1.1    White-Box Methods
sented as: t=1 P (yit |xi , yi,<t ). For simplicity,
                                                                  White-box methods operate on the premise that the
we use Pit (yit ) to represent P (yit |yi,<t , xi ) and
                                                                  state at every position of the LLMs is accessible
Cit (y) = δ(yit = y) to denote if y matches the
                                                                  during inference.
correct label yit . The ECE can be mathematically
expressed as:                                                     Logit-based methods The logit-based method
       M                                                          evaluates sentence uncertainty using token-level
    1 X          X
                                                                  probabilities or entropy (Huang et al., 2023b). To
        |                      Cit (ŷit ) − Pit (ŷit )|   (4)
    L                                                             ensure an evaluation consistent across sentences
      m=1 i,t:Pit (ŷit )∈Bm
                                                                  of different lengths, the length-normalized likeli-
where L = N
            P
               i=1 |yi | is the total number of gener-            hood probability is widely utilized (Murray and
ated tokens. Kumar and Sarawagi (2019) claimed                    Chiang, 2018). Moreover, alternatives such as the
that such metric focuses solely on the highest score              minimum or average token probabilities and the
label, neglecting the entire probability distribution,            average entropy are also widely used (Vazhentsev
and thereby introduced weighted ECE for refined                   et al., 2023b). Logit-based techniques readily adapt
calibration distinction. Another approach analyzes                to scenarios involving multiple sampling (Vazhent-
 Study                           Model                                  Proposed Methods
 Duan et al. (2023)              OPT (Zhang et al., 2022)               SAR (Shifting Attention to Relevance): consider semantic relevance when evaluating
                                                                        token and sentence-level uncertainty
 Manakul et al. (2023b)          GPT-3 (Brown et al., 2020b)            Semantic uncertainty: evaluate the consistency of responses by various methods
 Kuhn et al. (2023)              OPT (Zhang et al., 2022)               Cluster answers according to semantics and then computes the sum of probabilities
                                                                        within each cluster to represent confidence
 Kadavath et al. (2022)          Anthropic LLM (Bai et al., 2022)       P(True): the probability a model assigns to its answer as True, P(IK): probability a
                                                                        model assigns to "I know" by leveraging a binary classifier
                                 GPT3/3.5/4 (Brown et al., 2020b),
 Xiong et al. (2023)                                               Hybrid methods combining linguistic confidence and consistency-based confidence
                                 Vicuna (Chiang et al., 2023)
 Lin et al. (2023)               GPT-3.5                                Estimate confidence by evaluating the lexical and semantic similarity among responses
 Shrivastava et al. (2023)       GPT-3.5/4, Claude                      Hybrid methods combing confidence from surrogate models and linguistic confidence
                                                                        of target models

Table 1: Recent studies of LLM confidence estimation. These studies evaluate confidence estimation in question-
answering tasks, utilizing metrics such as ECE, AUROC, etc.

                                                                                    can self-assess to differentiate between correct and
                    Logit                              Consistency
                                                                                    incorrect answers. They suggested a method called
             1              2                         1             2               P(True), where the LLM first generates responses
                     4                                      4                       and then evaluates them as "True" or "False". The
   Internal state
                            Semantics        Linguistic
                                                                     Surrogate      probability the model assigns the confidence level
                                             confidence               model
                                                                                    to "True” determines the confidence level.
          (a) White-box                           (b) Black-box
                                                                                    Internal state-based methods Ren et al. (2022)
Figure 2: Venn diagram: the taxonomy of informa-
                                                                                    introduced a technique for out-of-distribution detec-
tion sources for white-box (Left) and black-box (Right)                             tion and selective generation. The method starts by
confidence estimation methods. These two families of                                computing embeddings for both inputs and outputs
methods can be categorized into the methods relying on                              in the training data, fitting them to a Gaussian dis-
logit, internal state, or semantics, and those relying on                           tribution. It then assesses the model’s confidence
consistency, linguistic confidence, or surrogate model,                             in its generated data by calculating the relative Ma-
respectively. The intersections of these methods are                                halanobis distance of the evaluated data pair from
located in Zone 1 - 4.
                                                                                    this Gaussian distribution.
                                                                                       Recent studies have posited the existence of a di-
                                                                                    rection in activation space that effectively separates
sev et al., 2023b) or ensemble models (Malinin and                                  true and false inputs (Kadavath et al., 2022; Burns
Gales, 2021a).                                                                      et al., 2023; Li et al., 2023; Azaria and Mitchell,
   To incorporate semantics, Duan et al. (2023)                                     2023). Kadavath et al. (2022) proposed training
introduced the concept of token-level relevance,                                    a classifier (the probe), named P(IK), on the acti-
which evaluates the relevance of the token by com-                                  vations of a network to predict whether an LLM
paring semantic change before and after moving                                      knows the answer. They sampled multiple answers
the token with a semantic similarity metric like Sen-                               for each question at a consistent temperature, la-
tence Transformer (Reimers and Gurevych, 2019).                                     beled the correctness of each answer, and then used
Then, sentence uncertainty can be adjusted based                                    the question-correctness pair as the training data.
on the token’s relevance. Duan et al. (2023) fur-                                   Similarly, Li et al. (2023) and Azaria and Mitchell
ther proposed sentence-level relevance in multi-                                    (2023) employed linear probes to examine whether
ple sampling settings, considering the similarity                                   attention heads in various layers can differentiate
between the returned sentence and other sampled                                     between correct and incorrect answers. Their em-
ones. Kuhn et al. (2023) proposed semantic uncer-                                   pirical findings indicated that certain middle layers
tainty, which first clusters semantically equivalent                                and a few attention heads exhibit strong perfor-
samples based on the bidirectional entailment be-                                   mance in this task, although the layer positions
tween samples and then approximates semantic                                        vary across models. Burns et al. (2023) intro-
entropy by summing probabilities in each cluster.                                   duced an unsupervised approach to map hidden
   Kadavath et al. (2022) discovered that LLMs                                      states to probabilities. It entails responding to ques-
 Study                        Model                                   Task                                  Calibration Methods
                              LSTM (Bahdanau et al., 2015),
 Kumar and Sarawagi                                                   Machine Translation                   TS with Learnable Parameters
                              Transformer (Vaswani et al., 2017)
 (2019)
 Lu et al. (2022)             Transformer (Vaswani et al., 2017)      Machine Translation                   Confidence-Based LS
 Wang et al. (2020)           Transformer (Vaswani et al., 2017)      Machine Translation                   LS, Dropout
                              LSTM (Bahdanau et al., 2015),           Data2Text Generation,
 Xiao and Wang (2021)                                                                                       Uncertainty-Aware Decoding
                              Transformer (Vaswani et al., 2017)      Image Captioning
 van der Poel et al. (2022)   BART (Lewis et al., 2020)               Text Summarization                    CPMI-Based Decoding
                                                                                                            MC-Dropout, BE, SNGP,
 Zablotskaia et al. (2023)    T5 (Raffel et al., 2020)                Text Summarization
                                                                                                            DeepEnsemble
                                                                      Text Summarization,
 Zhao et al. (2022)           PEGASUS (Zhang et al., 2020a)                                                 SLiC
                                                                      Question Answering
 Zhao et al. (2023a)          T5 (Raffel et al., 2020)                Text Summarization                    SLiC-HF
 Mielke et al. (2022)         BlenderBot (Roller et al., 2021)        Dialogue Generation                   Linguistic Calibration
 Lin et al. (2022)            GPT-3 (Brown et al., 2020b)             Math Question Answering               Fine-Tuning
                                                                      Text Classification, Fact Retrieval
 Zhao et al. (2021)           GPT-3 (Brown et al., 2020b)                                                   Contextual Calibration
                                                                      Information Extraction
                              PALM-2 (Anil et al., 2023),
 Fei et al. (2023)                                                    Text Classification                   Domain-Context Calibration
                              CLIP (Radford et al., 2021)
 Han et al. (2022)            GPT-2 (Radford et al., 2019)            Text Classification                   Prototypical Calibration
 Kumar (2022)                 GPT-2 (Radford et al., 2019)            Multiple Choice Question Answering    Answer-Level Calibration
                              GPT-2(Radford et al., 2019),
 Holtzman et al. (2021)                                               Multiple Choice Question Answering    PMIDC
                              GPT-3 (Brown et al., 2020b)
                              LLaMA (Touvron et al., 2023a),
 Zheng et al. (2023)          Vicuna (Chiang et al., 2023),           Multiple Choice Question Answering    PriDE
                              Falcon (Penedo et al., 2023), GPT-3.5

Table 2: Studies of LLM calibration. The first half is about generation tasks, and the second half is about
classification tasks. Calibration methods: LS: label smoothing, TS: temperature scaling, BE: Bayesian ensemble,
SNGP: spectral-normalized Gaussian process, MCDropout: Monte Carlo dropout, SLiC: sequence likelihood
calibration, HF: human feedback, FBC: feature-based calibrator, CPMI: conditional pointwise mutual information,
PMIDC: domain conditional pointwise mutual information, PriDE: debiasing with prior estimation.

tions with "Yes" or "No," extracting and convert-                            works (Kuhn et al., 2023; Duan et al., 2023) achieve
ing model activations into truth probabilities, and                          outstanding performance on uncertainty estimation
optimizing unsupervised loss for consistency. It                             for open-domain question answering by combin-
ultimately gauges the model’s confidence by esti-                            ing logit-based approaches with semantics, using
mating the likelihood of a "Yes" response.                                   tools like bi-directional entailment or sentence en-
                                                                             coders, aligning with Zone 2. Rephrasing and
Summary White-box methods, as illustrated in                                 round-trip translation can also be considered as us-
Figure 2a, primarily utilize logits, internal states,                        ing semantics to augment the remaining two meth-
and semantics as sources of information. Logit-                              ods (Jiang et al., 2021; Zhao et al., 2023b), corre-
based approaches, easy to implement during infer-                            sponding to Zones 2 and 3. P(True) leverages the
ence, face a limitation in that low logit probabilities                      self-evaluation capability of large language mod-
may reflect various properties of language. Meth-                            els (Kadavath et al., 2022). While it primarily uses
ods focusing on internal states (Kadavath et al.,                            logit probability, it is clear that this probability is in-
2022; Li et al., 2023; Azaria and Mitchell, 2023)                            fluenced by internal states and semantics, related to
provide insights into the model’s linguistic under-                          Zone 4. Anticipated advancements in collaborative
standing, though they typically require supervised                           information utilization will heighten computational
training on specially annotated data. Levinstein                             demands, especially for nuanced semantic analy-
and Herrmann (forthcoming) highlighted the lim-                              sis (Duan et al., 2023). This underscores the need
itations of the probing method in generalizing to                            for a careful balance between performance and re-
unseen examples with negations. Semantics are of-                            source efficiency.
ten used to complement other methods, providing
them with interpretability (Kuhn et al., 2023; Duan
                                                                             3.1.2          Black-box Methods
et al., 2023).
   To leverage their respective strengths, the cur-                          Black-box methods assume that all parameters dur-
rent advanced methods tend to combine different                              ing inference are unknown, allowing access only
dimensions during confidence estimation. Recent                              to the generations.
Linguistic confidence (verbalized method)                their effectiveness. Consistency methods are com-
refers to prompting language models to express           putationally intensive but have proven effective in
uncertainty in human language. This involves dis-        various tasks. They can benefit the remaining two
cerning different levels of uncertainty from the         approaches (Zone 1 and 2), such as the hybrid
model’s responses, such as "I don’t know," "most         method proposed by Xiong et al. (2023). Addi-
probably," or "Obviously" (Mielke et al., 2022) or       tionally, integrating all three methods (Zone 4) has
prompting the model to output various verbalized         been explored by Shrivastava et al. (2023) to offer
words (e.g., "lowest", "low", "medium", "high",          further benefits. Table 1 presents the latest repre-
"highest") or numbers (e.g., "85%"). Xiong et al.        sentative works in confidence estimation for large
(2023) demonstrated that prompting strategies like       language models, briefly describing their proposed
CoT (Wei et al., 2022), top-k (Tian et al., 2023),       methods.
and their proposed multi-step method can improve
the calibration of linguistic confidence.                3.2     Calibration Methods
                                                         This section categories related work in terms of
Consistency-based estimation assumes that a
                                                         calibration objectives: to enhance the quality of
model’s lack of confidence correlates with various
                                                         generated text through calibration techniques and
responses, often leading to hallucinatory outputs.
                                                         to improve the model’s handling of unknown or am-
SelfCheckGPT (Manakul et al., 2023b) proposed
                                                         biguous issues by enabling it to express uncertainty
a simple sampling-based approach that uses con-
                                                         more accurately. The first half of Table 2 presents
sistency among generations to find potential hal-
                                                         recent work on calibrating LLMs over generation
lucinations. Five variants are utilized to measure
                                                         tasks.
the consistency: BERTScore (Zhang et al., 2020b),
question-answering, n-gram, natural language in-         3.2.1    Improve the quality of generation
ference (NLI) model (He et al., 2023), and LLM           Many studies (Kumar and Sarawagi, 2019; Wang
prompting. Lin et al. (2023) proposed to calculate       et al., 2020; Lu et al., 2022) indicated that the mis-
the similarity matrix between generations and then       calibration of token-level logit probabilities dur-
estimate the uncertainty based on the analysis of        ing generation is one of the reasons for the de-
the similarity matrix, such as the sum of the eigen-     cline in generation quality. Kumar and Sarawagi
values of the graph Laplacian, the degree matrix,        (2019) introduced a modified temperature scaling
and the eccentricity.                                    approach where the temperature value adjusts ac-
Surrogate models Shrivastava et al. (2023) in-           cording to various factors, including the entropy
troduced white-box models as surrogate models,           of attention, token logit, token identity, and input
like LLaMA-2 (Touvron et al., 2023b) and then            coverage. Wang et al. (2020) noted a pronounced
employed logit-based methods to estimate the con-        prevalence of over-estimated tokens compared to
fidence of the target model when prompted with the       under-estimated ones. They introduced graduated
same task. They also showed that integrating such        label smoothing, applying heightened smoothing
confidence with linguistic confidence from black-        penalties to confident predictions. Xiao and Wang
box LLMs can provide better confidence estimates         (2021) and van der Poel et al. (2022) calibrated the
across various tasks.                                    token probability separately by adding a weighted
                                                         uncertainty estimated with model ensembles (Lak-
Summary Figure 2b illustrates the information            shminarayanan et al., 2017) and pointwise mutual
sources for confidence evaluation when model             information between the source and the target to-
states are not accessible: linguistic confidence, con-   kens. Zablotskaia et al. (2023) adapted diverse
sistency, including lexical and semantic similarity,     methods to improve model calibration in neural
and surrogate models. Linguistic confidence can          summarization tasks.
be elicited through prompts, but in practice, a mis-        Zhao et al. (2022) suggested that MLE training
match between these has been observed (Lin et al.,       can result in poorly calibrated sentence-level con-
2022; Liu et al., 2023c). Surrogate models (Shri-        fidence, as the model is only exposed to one gold
vastava et al., 2023) facilitate white-box methods       reference. They proposed the sequence likelihood
on black-box LLMs. However, they rely on the             calibration (SLiC) technique to rectify this. It first
assumption of approximate parameter distribution         generates m multiple sequences {ŷ}m from the
of models, necessitating further work to validate        initial model θ0 , then calibrates the model’s confi-
dence with:                                             4.1     In-Context Learning
  X                                                     In-context learning (ICL) is a new learning
      Lcal (θ, x, ȳ, {ŷ}m ) + λLreg (θ, θ0 , x, ȳ)
                                                        paradigm with LLMs, where the model learns
    {x,ȳ}
                                                  (5)   to perform a task based on a few examples
where the calibration loss Lcal aims to align mod-      and the context in which the task is pre-
els’ decoded candidates’ sequence likelihood ac-        sented. Assuming that k selected input-label pairs
cording to their similarity to the reference ȳ, and    (x1 , y1 ), · · · , (xk , yk ) are given as demonstrations,
the regularization loss Lreg prevents models from       with the predictive probability as the confidence,
deviating strongly. They further introduced SLiC-       ICL makes predictions as follows:
HF (Zhao et al., 2023a), which was designed to
                                                              ŷ = arg max P (y|x1 , y1 , · · · , xk , yk , x)   (6)
learn from human preferences.                                           y

3.2.2        Improve the linguistic confidence          When there are no demonstrations, the model per-
Mielke et al. (2022) proposed a calibrator-             forms zero-shot classification.
controlled method for chatbots, which involves a
trained calibrator to return the model confidence       Calibration methods We refer to the input-label
score and fine-tuned generative models to enable        pairs as C for context, and the original predictive
control over linguistic confidence. Lin et al. (2022)   probability is denoted as P (y|C, x). Zhao et al.
fine-tuned GPT-3 with the human-labeled dataset         (2021) introduced a method called contextual cal-
containing verbalized words and numbers to ex-          ibration. It gauges the model’s bias with context-
press uncertainty naturally. Zhou et al. (2023) em-     free prompts such as "[N/A]", "[MASK]" and an
pirically found that injecting expressions of un-       empty string. Then the context-free score is ob-
certainty into prompts significantly increases the      tained by P̂cf = P (y|C, [N/A]). Subsequently, it
accuracy of GPT-3’s answers and the calibration         transforms the scores with W = diag(p̂cf )−1 to
scores.                                                 offset the miscalibration. Fei et al. (2023) proposed
   Different datasets (Amayuelas et al., 2023; Yin      domain-context calibration, which estimates the
et al., 2023; Wang et al., 2023d; Liu et al., 2023a)    prior bias for each class with n times model aver-
have been presented on questions that language          age with random text   of an average sentence length:
                                                                          1 Pn
models cannot answer or for which there is no clear     P̄rd (y|C) = n i=1 P (y|C, [RANDOM TEXT]).
answer. Amayuelas et al. (2023) analyzed how dif-       The prediction is obtained with:
ferent language models, including both smaller and                                       P (y|C, x)
open-source models, classify a dataset of various                       ŷ = arg max                             (7)
                                                                                  y      P̄rd (y|C)
unanswerable questions. They observed that LLMs
show varying accuracy levels depending on the              Some methods aim to improve few-shot learn-
question type, while smaller and open-source mod-       ing performance by combining classic statistical
els tend to perform almost randomly. Liu et al.         machine learning techniques. Nie et al. (2022)
(2023a) evaluated both open-source models like          enhanced predictions by integrating a k-nearest-
LLaMA-2 (Touvron et al., 2023b), Vicuna (Chi-           neighbor classifier with a datastore containing
ang et al., 2023), and closed-source models such        cached few-shot instance representations, while
as GPT-3.5 and GPT-4, focusing on their refusal         Han et al. (2022) introduced prototypical calibra-
rate, accuracy, and uncertainty in handling unan-       tion, which employs Gaussian mixture models
swerable questions.                                     (GMM) to learn decision boundaries.
4     LLMs for Classification Tasks                     4.2     ICL Application: Multiple-Choice
LLMs are recognized for their efficiency in classi-             Question Answering
fication tasks, enabling rapid task implementation      Multiple-choice question answering (MCQA) is
via prompts (Brown et al., 2020a; Zhao et al., 2021).   an application of ICL, which is used in evaluat-
Although the underlying principles of confidence        ing LLMs by prompting them to answer ques-
estimation are similar to those in generation tasks,    tions with predefined choices. The context C
the objectives of calibration and the approaches        contains the question q, and the set of options
differ significantly.                                   I(q) = {o1 , · · · , oK }, where each is prefaced
with an identifier such as "A", and, if available,      to integrate semantics (Kumar, 2022). Besides, a
with a demonstration as an instruction.                 systematic benchmark for evaluating different cali-
   It is worth noting that implementing the evalua-     bration methods is still missing.
tion protocols can significantly impact the ranking
of models. For instance, the original evaluation of     5   Applications
the MMLU (Hendrycks et al., 2021) ranks the prob-
abilities of the four option identifiers. The answer    Confidence estimation and calibration can be effec-
is considered correct when the highest probabil-        tively employed in the following applications as an
ity corresponds to the correct option. The HELM         indispensable component in ensuring reliable AI.
implementation (Liang et al., 2022) considers prob-
abilities over the complete vocabulary. The HAR-
                                                        Hallucination detection and mitigation Confi-
NESS implementation1 prefers length-normalized
                                                        dence or uncertainty can be applied as a signal for
probabilities of the entire answer sequence.
                                                        detecting and mitigating hallucinations generated
Calibration methods Jiang et al. (2021) pro-            by LLMs (Zhang et al., 2023b; Huang et al., 2023a).
posed various fine-tuning loss functions and tem-       SelfCheckGPT (Manakul et al., 2023a) and SAC 3
perature scaling for calibrating the performance        (Zhang et al., 2023a) both explored hallucinations
of MQCA datasets. Additionally, they proposed           in the generation with self-consistency, while the
techniques such as candidate output paraphrasing        latter also checked cross-model response consis-
and input augmentation to calibrate the confidence.     tency by taking generations from other models as
Holtzman et al. (2021) claimed that surface form        the reference. Varshney et al. (2023) proposed a
competition occurs when different valid surface         method that leverages the model’s logits to iden-
forms compete for probability. Thus, they intro-        tify potential hallucinations, checks their correct-
duced domain conditional pointwise mutual infor-        ness through a validation procedure, appends the
mation (PMIDC), which reweighs each option ac-          repaired sentence to the prompt, and continues to
cording to a term that is proportional to its prior     generate.
likelihood within the context of the specific zero-
shot task. To overcome the bias from the choice po-     Ambiguity detection and selective generation
sition, Zheng et al. (2023) proposed PriDe, which       When identifying ambiguity in data or unanswer-
first decomposes the observed model prediction          able questions, reliable LLMs are anticipated to
distribution into an intrinsic prediction over option   refrain from providing answers rather than gener-
contents and a prior distribution over option iden-     ating responses arbitrarily (Kamath et al., 2020).
tifiers and then estimates the prior by permuting       Ren et al. (2022) proposed a selective generation
option contents on a small number of test sam-          method based on relative Mahalanobis distance.
ples. Kumar (2022) believed that under the neu-         Zablotskaia et al. (2023) provided a comprehen-
tral context Cϕ , the probabilities of different op-    sive benchmark study that evaluates various cal-
tions should be the same, but obviously, the LLM        ibration methods in neural summarization. Cole
cannot meet this condition, so they proposed us-        et al. (2023) and Hou et al. (2023) respectively em-
ing log P (ok |C) − sim(C, Cϕ ) log P (ok |Cϕ ) to      ployed a disambiguate-and-answer approach and
make the prediction. Given that C is very similar       input clarification ensembling to measure data un-
to the neutral context Cϕ , the approach will assign    certainty for detecting ambiguous questions.
an equal score to each choice.
                                                        Uncertainty-guided data exploitation Through
Summary The second half of Table 2 lists recent
                                                        measuring data uncertainty, the most representa-
calibration studies over classification tasks. Cur-
                                                        tive instances will be selected for few-shot learning
rent calibration methods primarily aim to mitigate
                                                        (Yu et al., 2022) or human annotation (Su et al.,
biases associated with labels or choice positions in
                                                        2022). Regarding the knowledge enhancement to
MCQA (Zhao et al., 2021; Jiang et al., 2021). A
                                                        LLMs, Jiang et al. (2023) proposed an adaptive
growing trend in the field is to deepen the under-
                                                        multi-retrieval method that first forecasts future
standing of the ICL (Holtzman et al., 2021) and
                                                        content and retrieves relevant documents stimu-
    https://github.com/EleutherAI/lm-evaluation-        lated by low-confidence tokens within upcoming
harness/tree/v0.3.0                                     sentences.
6   Future Directions                                    and presented distinctive challenges. We first in-
                                                         troduced the fundamental concepts of confidence
Comprehensive Benchmarks While confidence
                                                         and uncertainty, along with common metrics, esti-
estimation and calibration have wide-ranging appli-
                                                         mation methods, and calibration techniques used
cations, a comprehensive benchmark across tasks
                                                         in traditional discriminative models. We then iden-
and domains is required to better understand and
                                                         tified the challenges these methods face in LLMs.
evaluate these techniques’ robustness and utility.
                                                         Next, we delved into the latest research, introduc-
Addressing this issue requires extensive human
                                                         ing the principles, advantages, and drawbacks of
efforts to annotate the responses of LLMs, espe-
                                                         various methods in generation and classification
cially in long-form generation (Huang et al., 2024;
                                                         tasks. We concluded by discussing the current ap-
Mishra et al., 2024). Treating LLMs’ long gen-
                                                         plications and future research directions.
eration for confidence estimation and calibration
by parts, instead of as a whole, offers a promising      Limitations
direction for further enhancement.
                                                         This survey mainly has the following limitations:
Multi-modal LLMs By employing additional
pre-training with image-text pairings or by fine-        No experimental benchmarks Without original
tuning on specialized visual-instruction datasets,       experiments, this paper cannot offer empirical vali-
LLMs can be transited into the multimodal do-            dation of the theories or concepts. This limits the
main (Dai et al., 2023; Liu et al., 2023b; Zhu et al.,   paper’s ability to contribute new, verified knowl-
2023b). However, it remains unclear whether these        edge to the field.
confidence estimation methods are effective for          Potential omissions We have made our best ef-
multimodal large language models (MLLMs) and             fort to compile the latest advancements. Due to
whether these models are well-calibrated. We look        the rapid development in this field, there is still
forward to more efforts in detecting hallucinations      a possibility that some important work may have
in MLLMs through confidence estimation and in            been overlooked.
calibrating these models to discern events that are
impossible in the real world.                            Ethical Considerations and Potential Risks
Calibration to human variation Plank (2022)              We anticipate no significant ethical concerns in our
clarified the prevalent existence of human varia-        work. Our review surveys the latest developments
tion, i.e., humans have different opinions when la-      in this research field, and as we did not conduct
beling the same data. Human disagreement (Jiang          experiments, nor did we engage with risky datasets;
and de Marneffe, 2022) can be attributed to task         we also did not employ any workers for manual
ambiguity (Tamkin et al., 2022), annotator’s sub-        annotation.
jectivity (Sap et al., 2022), and input ambiguity
(Meissner et al., 2021). Recent work (Baan et al.,
2022; Lee et al., 2023) demonstrated the misalign-
                                                         References
ment between LLM calibration measures and hu-            Alfonso Amayuelas, Liangming Pan, Wenhu Chen, and
man disagreement in various learning paradigms.            William Wang. 2023. Knowledge of knowledge: Ex-
                                                           ploring known-unknowns uncertainty with large lan-
Expressing the concern regarding different types           guage models. ArXiv preprint, abs/2305.13712.
of ambiguity (Xiong et al., 2023), abstaining from
answering ambiguous questions (Yoshikawa and             Rohan Anil, Andrew M. Dai, Orhan Firat, Melvin John-
                                                           son, Dmitry Lepikhin, Alexandre Passos, Siamak
Okazaki, 2023), and further resolving ambiguity            Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng
(Varshney and Baral, 2023) are necessary for trust-        Chen, Eric Chu, Jonathan H. Clark, Laurent El
worthy and reliable LLMs aligned with human vari-          Shafey, Yanping Huang, Kathy Meier-Hellstern, Gau-
ation.                                                     rav Mishra, Erica Moreira, Mark Omernick, Kevin
                                                           Robinson, Sebastian Ruder, Yi Tay, Kefan Xiao,
                                                           Yuanzhong Xu, Yujing Zhang, Gustavo Hernández
7   Conclusion
                                                           Ábrego, Junwhan Ahn, Jacob Austin, Paul Barham,
This survey highlights the critical role of confi-         Jan A. Botha, James Bradbury, Siddhartha Brahma,
                                                           Kevin Brooks, Michele Catasta, Yong Cheng, Colin
dence estimation and calibration in addressing er-         Cherry, Christopher A. Choquette-Choo, Aakanksha
rors and biases in LLMs. The evolution of LLMs             Chowdhery, Clément Crepy, Shachi Dave, Mostafa
has paved the way for novel research opportunities         Dehghani, Sunipa Dev, Jacob Devlin, Mark Díaz,
  Nan Du, Ethan Dyer, Vladimir Feinberg, Fangxi-            Clemens Winter, Christopher Hesse, Mark Chen, Eric
  aoyu Feng, Vlad Fienber, Markus Freitag, Xavier           Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
  Garcia, Sebastian Gehrmann, Lucas Gonzalez, and           Jack Clark, Christopher Berner, Sam McCandlish,
  et al. 2023. Palm 2 technical report. ArXiv preprint,     Alec Radford, Ilya Sutskever, and Dario Amodei.
  abs/2305.10403.                                           2020b. Language models are few-shot learners. In
                                                            Advances in Neural Information Processing Systems
Amos Azaria and Tom Mitchell. 2023. The internal            33: Annual Conference on Neural Information Pro-
 state of an llm knows when its lying. ArXiv preprint,      cessing Systems 2020, NeurIPS 2020, December 6-
 abs/2304.13734.                                            12, 2020, virtual.
Joris Baan, Wilker Aziz, Barbara Plank, and Raquel        Collin Burns, Haotian Ye, Dan Klein, and Jacob Stein-
   Fernandez. 2022. Stop measuring calibration when         hardt. 2023. Discovering latent knowledge in lan-
   humans disagree. In Proceedings of the 2022 Con-         guage models without supervision. In The Eleventh
   ference on Empirical Methods in Natural Language         International Conference on Learning Representa-
  Processing, pages 1892–1915, Abu Dhabi, United            tions.
  Arab Emirates. Association for Computational Lin-
   guistics.                                              Jiuhai Chen and Jonas Mueller. 2023. Quantifying un-
                                                             certainty in answers from any language model via
Joris Baan, Nico Daheim, Evgenia Ilia, Dennis Ul-            intrinsic and extrinsic confidence assessment. ArXiv
   mer, Haau-Sing Li, Raquel Fernández, Barbara              preprint, abs/2308.16175.
   Plank, Rico Sennrich, Chrysoula Zerva, and Wilker
  Aziz. 2023. Uncertainty in natural language gener-      Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng,
   ation: From theory to applications. ArXiv preprint,     Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan
   abs/2307.15703.                                         Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al.
                                                           2023. Vicuna: An open-source chatbot impressing
Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Ben-
                                                           gpt-4 with 90%* chatgpt quality. See https://vicuna.
  gio. 2015. Neural machine translation by jointly
                                                           lmsys. org (accessed 14 April 2023).
  learning to align and translate. In 3rd International
  Conference on Learning Representations, ICLR 2015,
                                                          Jeremy R Cole, Michael JQ Zhang, Daniel Gillick, Ju-
  San Diego, CA, USA, May 7-9, 2015, Conference
                                                             lian Martin Eisenschlos, Bhuwan Dhingra, and Jacob
  Track Proceedings.
                                                             Eisenstein. 2023. Selectively answering ambiguous
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda                questions. ArXiv preprint, abs/2305.14613.
  Askell, Anna Chen, Nova DasSarma, Dawn Drain,
  Stanislav Fort, Deep Ganguli, Tom Henighan, et al.      Charles Corbière, Nicolas Thome, Avner Bar-Hen,
  2022. Training a helpful and harmless assistant with      Matthieu Cord, and Patrick Pérez. 2019. Address-
  reinforcement learning from human feedback. ArXiv         ing failure prediction by learning model confidence.
  preprint, abs/2204.05862.                                 In Advances in Neural Information Processing Sys-
                                                            tems 32: Annual Conference on Neural Information
Andrew P. Bradley. 1997. The use of the area under          Processing Systems 2019, NeurIPS 2019, December
  the roc curve in the evaluation of machine learning       8-14, 2019, Vancouver, BC, Canada, pages 2898–
  algorithms. Pattern Recognition, 30(7):1145–1159.         2909.

Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie          Wenliang Dai, Junnan Li, Dongxu Li, Anthony
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind         Meng Huat Tiong, Junqi Zhao, Weisheng Wang,
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda         Boyang Li, Pascale Fung, and Steven C. H. Hoi.
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,            2023. Instructblip: Towards general-purpose vision-
  Gretchen Krueger, Tom Henighan, Rewon Child,             language models with instruction tuning. ArXiv
  Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,            preprint, abs/2305.06500.
  Clemens Winter, Christopher Hesse, Mark Chen, Eric
  Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,     Shrey Desai and Greg Durrett. 2020. Calibration of
  Jack Clark, Christopher Berner, Sam McCandlish,           pre-trained transformers. In Proceedings of the 2020
  Alec Radford, Ilya Sutskever, and Dario Amodei.           Conference on Empirical Methods in Natural Lan-
  2020a. Language models are few-shot learners. In          guage Processing (EMNLP), pages 295–302, Online.
  Advances in Neural Information Processing Systems         Association for Computational Linguistics.
  33: Annual Conference on Neural Information Pro-
  cessing Systems 2020, NeurIPS 2020, December 6-         Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
  12, 2020, virtual.                                         Kristina Toutanova. 2019. BERT: Pre-training of
                                                             deep bidirectional transformers for language under-
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie             standing. In Proceedings of the 2019 Conference of
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind           the North American Chapter of the Association for
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda          Computational Linguistics: Human Language Tech-
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,              nologies, Volume 1 (Long and Short Papers), pages
  Gretchen Krueger, Tom Henighan, Rewon Child,              4171–4186, Minneapolis, Minnesota. Association for
  Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,              Computational Linguistics.
Terrance DeVries and Graham W Taylor. 2018. Learn-         Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas,
  ing confidence for out-of-distribution detection in        Shiyu Chang, and Yang Zhang. 2023. Decompos-
  neural networks. ArXiv preprint, abs/1802.04865.           ing uncertainty for large language models through
                                                             input clarification ensembling. ArXiv preprint,
Jinhao Duan, Hao Cheng, Shiqi Wang, Chenan Wang,             abs/2311.08718.
   Alex Zavalny, Renjing Xu, Bhavya Kailkhura, and
   Kaidi Xu. 2023. Shifting attention to relevance: To-    Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong,
   wards the uncertainty estimation of large language        Zhangyin Feng, Haotian Wang, Qianglong Chen,
   models. ArXiv preprint, abs/2307.01379.                   Weihua Peng, Xiaocheng Feng, Bing Qin, et al.
                                                             2023a. A survey on hallucination in large language
Yu Fei, Yifan Hou, Zeming Chen, and Antoine Bosselut.        models: Principles, taxonomy, challenges, and open
  2023. Mitigating label biases for in-context learning.     questions. ArXiv preprint, abs/2311.05232.
  ArXiv preprint, abs/2305.19148.
                                                           Yuheng Huang, Jiayang Song, Zhijie Wang, Huam-
Yarin Gal and Zoubin Ghahramani. 2016. Dropout               ing Chen, and Lei Ma. 2023b. Look before you
  as a bayesian approximation: Representing model            leap: An exploratory study of uncertainty measure-
  uncertainty in deep learning. In Proceedings of the        ment for large language models. ArXiv preprint,
  33nd International Conference on Machine Learning,         abs/2307.10236.
  ICML 2016, New York City, NY, USA, June 19-24,           Yukun Huang, Yixin Liu, Raghuveer Thirukovalluru,
  2016, volume 48 of JMLR Workshop and Conference            Arman Cohan, and Bhuwan Dhingra. 2024. Cali-
  Proceedings, pages 1050–1059. JMLR.org.                    brating long-form generations from large language
                                                             models. ArXiv preprint, abs/2402.06544.
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Wein-
  berger. 2017. On calibration of modern neural net-       Abhyuday Jagannatha and Hong Yu. 2020. Calibrat-
  works. In Proceedings of the 34th International Con-       ing structured output predictors for natural language
  ference on Machine Learning, ICML 2017, Sydney,            processing. In Proceedings of the 58th Annual Meet-
  NSW, Australia, 6-11 August 2017, volume 70 of             ing of the Association for Computational Linguistics,
  Proceedings of Machine Learning Research, pages            pages 2078–2092, Online. Association for Computa-
  1321–1330. PMLR.                                           tional Linguistics.
Zhixiong Han, Yaru Hao, Li Dong, Yutao Sun, and            Nan-Jiang Jiang and Marie-Catherine de Marneffe.
  Furu Wei. 2022. Prototypical calibration for few-          2022. Investigating reasons for disagreement in natu-
  shot learning of language models. ArXiv preprint,          ral language inference. Transactions of the Associa-
  abs/2205.10183.                                            tion for Computational Linguistics, 10:1357–1374.

Marton Havasi, Rodolphe Jenatton, Stanislav Fort,          Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham
 Jeremiah Zhe Liu, Jasper Snoek, Balaji Lakshmi-             Neubig. 2021. How can we know when language
 narayanan, Andrew Mingbo Dai, and Dustin Tran.              models know? on the calibration of language models
 2021. Training independent subnetworks for robust           for question answering. Transactions of the Associa-
 prediction. In 9th International Conference on Learn-       tion for Computational Linguistics, 9:962–977.
 ing Representations, ICLR 2021, Virtual Event, Aus-
 tria, May 3-7, 2021. OpenReview.net.                      Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing
                                                             Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang,
Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2023.           Jamie Callan, and Graham Neubig. 2023. Active
  DeBERTav3: Improving deBERTa using ELECTRA-                retrieval augmented generation. ArXiv preprint,
  style pre-training with gradient-disentangled embed-       abs/2305.06983.
  ding sharing. In The Eleventh International Confer-      Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
  ence on Learning Representations.                          Henighan, Dawn Drain, Ethan Perez, Nicholas
                                                             Schiefer, Zac Hatfield Dodds, Nova DasSarma,
Dan Hendrycks, Collin Burns, Steven Basart, Andy             Eli Tran-Johnson, et al. 2022. Language models
  Zou, Mantas Mazeika, Dawn Song, and Jacob Stein-           (mostly) know what they know. ArXiv preprint,
  hardt. 2021. Measuring massive multitask language          abs/2207.05221.
  understanding. In 9th International Conference on
  Learning Representations, ICLR 2021, Virtual Event,      Amita Kamath, Robin Jia, and Percy Liang. 2020. Se-
  Austria, May 3-7, 2021. OpenReview.net.                   lective question answering under domain shift. In
                                                            Proceedings of the 58th Annual Meeting of the Asso-
Ari Holtzman, Peter West, Vered Shwartz, Yejin Choi,        ciation for Computational Linguistics, pages 5684–
  and Luke Zettlemoyer. 2021. Surface form com-             5696, Online. Association for Computational Lin-
  petition: Why the highest probability answer isn’t        guistics.
  always right. In Proceedings of the 2021 Conference
  on Empirical Methods in Natural Language Process-        Alex Kendall and Yarin Gal. 2017. What uncertainties
  ing, pages 7038–7051, Online and Punta Cana, Do-           do we need in bayesian deep learning for computer
  minican Republic. Association for Computational            vision? In Advances in Neural Information Pro-
  Linguistics.                                               cessing Systems 30: Annual Conference on Neural
  Information Processing Systems 2017, December 4-9,        Benjamin A. Levinstein and Daniel A. Herrmann. forth-
  2017, Long Beach, CA, USA, pages 5574–5584.                 coming. Still no lie detector for language models:
                                                              Probing empirical and conceptual roadblocks. Philo-
Jaeyoung Kim, Dongbin Na, Sungchul Choi, and Sung-            sophical Studies, pages 1–27.
   bin Lim. 2023. Bag of tricks for in-distribution cali-
   bration of pretrained transformers. In Findings of the   Mike Lewis, Yinhan Liu, Naman Goyal, Marjan
  Association for Computational Linguistics: EACL             Ghazvininejad, Abdelrahman Mohamed, Omer Levy,
   2023, pages 551–563, Dubrovnik, Croatia. Associa-          Veselin Stoyanov, and Luke Zettlemoyer. 2020.
   tion for Computational Linguistics.                        BART: Denoising sequence-to-sequence pre-training
Lingkai Kong, Haoming Jiang, Yuchen Zhuang, Jie               for natural language generation, translation, and com-
  Lyu, Tuo Zhao, and Chao Zhang. 2020. Cali-                  prehension. In Proceedings of the 58th Annual Meet-
  brated language model fine-tuning for in- and out-          ing of the Association for Computational Linguistics,
  of-distribution data. In Proceedings of the 2020 Con-       pages 7871–7880, Online. Association for Computa-
  ference on Empirical Methods in Natural Language            tional Linguistics.
  Processing (EMNLP), pages 1326–1340, Online. As-
  sociation for Computational Linguistics.                  Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter
                                                              Pfister, and Martin Wattenberg. 2023. Inference-time
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.         intervention: Eliciting truthful answers from a lan-
  Semantic uncertainty: Linguistic invariances for un-        guage model. ArXiv preprint, abs/2306.03341.
  certainty estimation in natural language generation.
  ArXiv preprint, abs/2302.09664.                           Percy Liang, Rishi Bommasani, Tony Lee, Dimitris
                                                              Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian
Alex Kulesza and Ben Taskar. 2012. Determinantal
                                                              Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Ku-
  point processes for machine learning. Foundations
                                                              mar, et al. 2022. Holistic evaluation of language
  and Trends® in Machine Learning, 5(2–3):123–286.
                                                              models. ArXiv preprint, abs/2211.09110.
Meelis Kull, Miquel Perelló-Nieto, Markus Kängsepp,
 Telmo de Menezes e Silva Filho, Hao Song, and              Stephanie Lin, Jacob Hilton, and Owain Evans. 2022.
 Peter A. Flach. 2019. Beyond temperature scaling:            Teaching models to express their uncertainty in
 Obtaining well-calibrated multi-class probabilities          words. ArXiv preprint, abs/2205.14334.
 with dirichlet calibration. In Advances in Neural
 Information Processing Systems 32: Annual Confer-          Tsung-Yi Lin, Priya Goyal, Ross B. Girshick, Kaim-
 ence on Neural Information Processing Systems 2019,          ing He, and Piotr Dollár. 2017. Focal loss for dense
 NeurIPS 2019, December 8-14, 2019, Vancouver, BC,            object detection. In IEEE International Conference
 Canada, pages 12295–12305.                                   on Computer Vision, ICCV 2017, Venice, Italy, Octo-
                                                              ber 22-29, 2017, pages 2999–3007. IEEE Computer
Aviral Kumar and Sunita Sarawagi. 2019. Calibration           Society.
  of encoder decoder models for neural machine trans-
  lation. ArXiv preprint, abs/1903.00802.                   Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. 2023.
Sawan Kumar. 2022. Answer-level calibration for free-         Generating with confidence: Uncertainty quantifi-
  form multiple choice question answering. In Pro-            cation for black-box large language models. ArXiv
  ceedings of the 60th Annual Meeting of the Associa-         preprint, abs/2305.19187.
  tion for Computational Linguistics (Volume 1: Long
  Papers), pages 665–679, Dublin, Ireland. Association      Genglin Liu, Xingyao Wang, Lifan Yuan, Yangyi Chen,
  for Computational Linguistics.                              and Hao Peng. 2023a. Prudent silence or foolish
                                                              babble? examining large language models’ responses
Balaji Lakshminarayanan, Alexander Pritzel, and               to the unknown. ArXiv preprint, abs/2311.09731.
  Charles Blundell. 2017. Simple and scalable pre-
  dictive uncertainty estimation using deep ensembles.      Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae
  In Advances in Neural Information Processing Sys-           Lee. 2023b. Visual instruction tuning. ArXiv
  tems 30: Annual Conference on Neural Information            preprint, abs/2304.08485.
  Processing Systems 2017, December 4-9, 2017, Long
  Beach, CA, USA, pages 6402–6413.                          Yang Liu, Yuanshun Yao, Jean-Francois Ton, Xiaoying
Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin.           Zhang, Ruocheng Guo Hao Cheng, Yegor Klochkov,
  2018. A simple unified framework for detecting out-         Muhammad Faaiz Taufiq, and Hang Li. 2023c. Trust-
  of-distribution samples and adversarial attacks. In         worthy llms: a survey and guideline for evaluating
  Advances in Neural Information Processing Systems           large language models’ alignment. ArXiv preprint,
  31: Annual Conference on Neural Information Pro-            abs/2308.05374.
  cessing Systems 2018, NeurIPS 2018, December 3-8,
  2018, Montréal, Canada, pages 7167–7177.                  Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
                                                              dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
Noah Lee, Na Min An, and James Thorne. 2023. Can              Luke Zettlemoyer, and Veselin Stoyanov. 2019.
  large language models infer and disagree like hu-           Roberta: A robustly optimized bert pretraining ap-
  mans? ArXiv preprint, abs/2305.13788.                       proach. ArXiv preprint, abs/1907.11692.
Yu Lu, Jiali Zeng, Jiajun Zhang, Shuangzhi Wu, and           focal loss. In Advances in Neural Information Pro-
  Mu Li. 2022. Learning confidence for transformer-          cessing Systems 33: Annual Conference on Neural
  based neural machine translation. In Proceedings           Information Processing Systems 2020, NeurIPS 2020,
  of the 60th Annual Meeting of the Association for          December 6-12, 2020, virtual.
  Computational Linguistics (Volume 1: Long Papers),
  pages 2353–2364, Dublin, Ireland. Association for        Kenton Murray and David Chiang. 2018. Correcting
  Computational Linguistics.                                 length bias in neural machine translation. In Proceed-
                                                             ings of the Third Conference on Machine Translation:
Andrey Malinin and Mark J. F. Gales. 2021a. Uncer-           Research Papers, pages 212–223, Brussels, Belgium.
  tainty estimation in autoregressive structured predic-     Association for Computational Linguistics.
  tion. In 9th International Conference on Learning
  Representations, ICLR 2021, Virtual Event, Austria,      Feng Nie, Meixi Chen, Zhirui Zhang, and Xu Cheng.
  May 3-7, 2021. OpenReview.net.                             2022. Improving few-shot performance of language
                                                             models via nearest neighbor calibration. ArXiv
Andrey Malinin and Mark J. F. Gales. 2021b. Uncer-           preprint, abs/2212.02216.
  tainty estimation in autoregressive structured predic-
  tion. In 9th International Conference on Learning        Jeremy Nixon, Michael W. Dusenberry, Linchuan
  Representations, ICLR 2021, Virtual Event, Austria,         Zhang, Ghassen Jerfel, and Dustin Tran. 2019. Mea-
  May 3-7, 2021. OpenReview.net.                              suring calibration in deep learning. In IEEE Confer-
                                                              ence on Computer Vision and Pattern Recognition
Potsawee Manakul, Yassir Fathullah, Adian Liusie,            Workshops, CVPR Workshops 2019, Long Beach, CA,
  Vyas Raina, Vatsal Raina, and Mark Gales. 2023a.            USA, June 16-20, 2019, pages 38–41. Computer Vi-
  CUED at ProbSum 2023: Hierarchical ensemble                 sion Foundation / IEEE.
  of summarization models. In The 22nd Workshop
  on Biomedical Natural Language Processing and            Seo Yeon Park and Cornelia Caragea. 2022. On the cal-
  BioNLP Shared Tasks, pages 516–523, Toronto,               ibration of pre-trained language models using mixup
  Canada. Association for Computational Linguistics.         guided by area under the margin and saliency. In
                                                             Proceedings of the 60th Annual Meeting of the As-
Potsawee Manakul, Adian Liusie, and Mark JF Gales.           sociation for Computational Linguistics (Volume 1:
  2023b. Selfcheckgpt: Zero-resource black-box hal-          Long Papers), pages 5364–5374, Dublin, Ireland. As-
  lucination detection for generative large language         sociation for Computational Linguistics.
  models. ArXiv preprint, abs/2303.08896.
                                                           Tim Pearce, Alexandra Brintrup, and Jun Zhu. 2021.
Johannes Mario Meissner, Napat Thumwanit, Saku Sug-          Understanding softmax confidence and uncertainty.
  awara, and Akiko Aizawa. 2021. Embracing ambi-             ArXiv preprint, abs/2106.04972.
  guity: Shifting the training target of NLI models. In
  Proceedings of the 59th Annual Meeting of the Asso-      Guilherme Penedo, Quentin Malartic, Daniel Hesslow,
  ciation for Computational Linguistics and the 11th         Ruxandra Cojocaru, Alessandro Cappelli, Hamza
  International Joint Conference on Natural Language         Alobeidli, Baptiste Pannier, Ebtesam Almazrouei,
  Processing (Volume 2: Short Papers), pages 862–869,        and Julien Launay. 2023. The refinedweb dataset
  Online. Association for Computational Linguistics.         for falcon LLM: outperforming curated corpora with
                                                             web data, and web data only. ArXiv preprint,
Sabrina J. Mielke, Arthur Szlam, Emily Dinan, and Y-         abs/2306.01116.
  Lan Boureau. 2022. Reducing conversational agents’
  overconfidence through linguistic calibration. Trans-    Gabriel Pereyra, George Tucker, Jan Chorowski, Łukasz
  actions of the Association for Computational Linguis-      Kaiser, and Geoffrey Hinton. 2017. Regularizing
  tics, 10:857–872.                                          neural networks by penalizing confident output dis-
                                                             tributions. ArXiv preprint, abs/1701.06548.
Abhika Mishra, Akari Asai, Vidhisha Balachandran,
  Yizhong Wang, Graham Neubig, Yulia Tsvetkov, and         Fabio Petroni, Tim Rocktäschel, Sebastian Riedel,
  Hannaneh Hajishirzi. 2024. Fine-grained hallucina-         Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and
  tion detection and editing for language models. ArXiv      Alexander Miller. 2019. Language models as knowl-
  preprint, abs/2401.06855.                                  edge bases? In Proceedings of the 2019 Confer-
                                                             ence on Empirical Methods in Natural Language Pro-
Jooyoung Moon, Jihyo Kim, Younghak Shin, and                 cessing and the 9th International Joint Conference
  Sangheum Hwang. 2020. Confidence-aware learn-              on Natural Language Processing (EMNLP-IJCNLP),
  ing for deep neural networks. In Proceedings of the        pages 2463–2473, Hong Kong, China. Association
  37th International Conference on Machine Learning,         for Computational Linguistics.
  ICML 2020, 13-18 July 2020, Virtual Event, volume
  119 of Proceedings of Machine Learning Research,         Barbara Plank. 2022. The “problem” of human label
  pages 7034–7044. PMLR.                                     variation: On ground truth in data, modeling and
                                                             evaluation. In Proceedings of the 2022 Conference
Jishnu Mukhoti, Viveka Kulharia, Amartya Sanyal, Stu-        on Empirical Methods in Natural Language Process-
   art Golodetz, Philip H. S. Torr, and Puneet K. Doka-      ing, pages 10671–10682, Abu Dhabi, United Arab
   nia. 2020. Calibrating deep neural networks using         Emirates. Association for Computational Linguistics.
Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya            models for confidence estimation. ArXiv preprint,
  Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sas-          abs/2311.08877.
  try, Amanda Askell, Pamela Mishkin, Jack Clark,
  Gretchen Krueger, and Ilya Sutskever. 2021. Learn-        Chenglei Si, Chen Zhao, Sewon Min, and Jordan Boyd-
  ing transferable visual models from natural language        Graber. 2022. Re-examining calibration: The case
  supervision. In Proceedings of the 38th International       of question answering. In Findings of the Associa-
  Conference on Machine Learning, ICML 2021, 18-24            tion for Computational Linguistics: EMNLP 2022,
  July 2021, Virtual Event, volume 139 of Proceedings         pages 2814–2829, Abu Dhabi, United Arab Emirates.
  of Machine Learning Research, pages 8748–8763.              Association for Computational Linguistics.
  PMLR.
                                                            Hongjin Su, Jungo Kasai, Chen Henry Wu, Weijia Shi,
Alec Radford, Jeff Wu, Rewon Child, David Luan,               Tianlu Wang, Jiayi Xin, Rui Zhang, Mari Ostendorf,
  Dario Amodei, and Ilya Sutskever. 2019. Language            Luke Zettlemoyer, Noah A Smith, et al. 2022. Selec-
  models are unsupervised multitask learners. Techni-         tive annotation makes language models better few-
  cal report.                                                 shot learners. ArXiv preprint, abs/2209.01975.
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine         Hao Sun, Boris van Breugel, Jonathan Crabbe, Nabeel
  Lee, Sharan Narang, Michael Matena, Yanqi Zhou,             Seedat, and Mihaela van der Schaar. 2022. Daux: a
  Wei Li, and Peter J. Liu. 2020. Exploring the limits        density-based approach for uncertainty explanations.
  of transfer learning with a unified text-to-text trans-     ArXiv preprint, abs/2207.05161.
  former. J. Mach. Learn. Res., 21:140:1–140:67.
                                                            Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe,
Nils Reimers and Iryna Gurevych. 2019. Sentence-              Jonathon Shlens, and Zbigniew Wojna. 2016. Re-
  BERT: Sentence embeddings using Siamese BERT-               thinking the inception architecture for computer vi-
  networks. In Proceedings of the 2019 Conference on          sion. In 2016 IEEE Conference on Computer Vision
  Empirical Methods in Natural Language Processing            and Pattern Recognition, CVPR 2016, Las Vegas,
  and the 9th International Joint Conference on Natu-         NV, USA, June 27-30, 2016, pages 2818–2826. IEEE
  ral Language Processing (EMNLP-IJCNLP), pages               Computer Society.
  3982–3992, Hong Kong, China. Association for Com-
  putational Linguistics.                                   Alex Tamkin, Kunal Handa, Avash Shrestha, and Noah
                                                              Goodman. 2022. Task ambiguity in humans and
Jie Ren, Jiaming Luo, Yao Zhao, Kundan Krishna, Mo-           language models. ArXiv preprint, abs/2212.10711.
   hammad Saleh, Balaji Lakshminarayanan, and Pe-
   ter J Liu. 2022. Out-of-distribution detection and       Katherine Tian, Eric Mitchell, Allan Zhou, Archit
   selective generation for conditional language models.      Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn,
   ArXiv preprint, abs/2209.15558.                            and Christopher Manning. 2023. Just ask for cali-
Stephen Roller, Emily Dinan, Naman Goyal, Da Ju,              bration: Strategies for eliciting calibrated confidence
   Mary Williamson, Yinhan Liu, Jing Xu, Myle Ott,            scores from language models fine-tuned with human
   Eric Michael Smith, Y-Lan Boureau, and Jason We-           feedback. In Proceedings of the 2023 Conference
   ston. 2021. Recipes for building an open-domain            on Empirical Methods in Natural Language Process-
   chatbot. In Proceedings of the 16th Conference of          ing, pages 5433–5442, Singapore. Association for
   the European Chapter of the Association for Compu-         Computational Linguistics.
   tational Linguistics: Main Volume, pages 300–325,
                                                            Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
   Online. Association for Computational Linguistics.
                                                              Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Maarten Sap, Swabha Swayamdipta, Laura Vianna,                Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
 Xuhui Zhou, Yejin Choi, and Noah A. Smith. 2022.             Azhar, Aurélien Rodriguez, Armand Joulin, Edouard
 Annotators with attitudes: How annotator beliefs             Grave, and Guillaume Lample. 2023a. Llama: Open
 and identities bias toxic language detection. In Pro-        and efficient foundation language models. ArXiv
 ceedings of the 2022 Conference of the North Amer-           preprint, abs/2302.13971.
 ican Chapter of the Association for Computational
 Linguistics: Human Language Technologies, pages            Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
 5884–5906, Seattle, United States. Association for           Martinet, Marie-Anne Lachaux, Timothée Lacroix,
 Computational Linguistics.                                   Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
                                                              Azhar, et al. 2023b. Llama: Open and effi-
Artem Shelmanov, Evgenii Tsymbalov, Dmitri Puzyrev,           cient foundation language models. ArXiv preprint,
  Kirill Fedyanin, Alexander Panchenko, and Maxim             abs/2302.13971.
  Panov. 2021. How certain is your Transformer? In
  Proceedings of the 16th Conference of the European        Liam van der Poel, Ryan Cotterell, and Clara Meis-
  Chapter of the Association for Computational Lin-           ter. 2022. Mutual information alleviates hallucina-
  guistics: Main Volume, pages 1833–1840, Online.             tions in abstractive summarization. In Proceedings
  Association for Computational Linguistics.                  of the 2022 Conference on Empirical Methods in Nat-
                                                              ural Language Processing, pages 5956–5965, Abu
Vaishnavi Shrivastava, Percy Liang, and Ananya Kumar.         Dhabi, United Arab Emirates. Association for Com-
  2023. Llamas know what gpts don’t show: Surrogate           putational Linguistics.
Neeraj Varshney and Chitta Baral. 2023.         Post-         and Yue Zhang. 2023a. Survey on factuality in large
  abstention: Towards reliably re-attempting the ab-          language models: Knowledge, retrieval and domain-
  stained instances in QA. In Proceedings of the 61st         specificity. ArXiv preprint, abs/2310.07521.
  Annual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers), pages 967–982,       Cunxiang Wang, Xiaoze Liu, Yuanhao Yue, Xian-
  Toronto, Canada. Association for Computational Lin-         gru Tang, Tianhang Zhang, Cheng Jiayang, Yunzhi
  guistics.                                                   Yao, Wenyang Gao, Xuming Hu, Zehan Qi, et al.
                                                              2023b. Survey on factuality in large language mod-
Neeraj Varshney, Wenlin Yao, Hongming Zhang, Jian-            els: Knowledge, retrieval and domain-specificity.
  shu Chen, and Dong Yu. 2023. A stitch in time saves         ArXiv preprint, abs/2310.07521.
  nine: Detecting and mitigating hallucinations of
  llms by validating low-confidence generation. ArXiv       Shuo Wang, Zhaopeng Tu, Shuming Shi, and Yang Liu.
  preprint, abs/2307.03987.                                   2020. On the inference calibration of neural machine
                                                              translation. In Proceedings of the 58th Annual Meet-
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob              ing of the Association for Computational Linguistics,
  Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz              pages 3070–3079, Online. Association for Computa-
  Kaiser, and Illia Polosukhin. 2017. Attention is all        tional Linguistics.
  you need. In Advances in Neural Information Pro-
  cessing Systems 30: Annual Conference on Neural           Xiaosu Wang, Yun Xiong, Beichen Kang, Yao Zhang,
  Information Processing Systems 2017, December 4-9,          Philip S. Yu, and Yangyong Zhu. 2023c. Reducing
  2017, Long Beach, CA, USA, pages 5998–6008.                 negative effects of the biases of language models in
                                                              zero-shot setting. In Proceedings of the Sixteenth
Artem Vazhentsev, Gleb Kuzmin, Artem Shelmanov,               ACM International Conference on Web Search and
  Akim Tsvigun, Evgenii Tsymbalov, Kirill Fedyanin,           Data Mining, WSDM ’23, page 904–912, New York,
  Maxim Panov, Alexander Panchenko, Gleb Gusev,               NY, USA. Association for Computing Machinery.
  Mikhail Burtsev, Manvel Avetisian, and Leonid
                                                            Yuxia Wang, Haonan Li, Xudong Han, Preslav Nakov,
  Zhukov. 2022. Uncertainty estimation of transformer
                                                              and Timothy Baldwin. 2023d. Do-not-answer: A
  predictions for misclassification detection. In Pro-
                                                              dataset for evaluating safeguards in LLMs. ArXiv
  ceedings of the 60th Annual Meeting of the Associa-
                                                              preprint, abs/2308.13387.
  tion for Computational Linguistics (Volume 1: Long
  Papers), pages 8237–8252, Dublin, Ireland. Associa-       Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  tion for Computational Linguistics.                          Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
                                                               et al. 2022. Chain-of-thought prompting elicits rea-
Artem Vazhentsev, Gleb Kuzmin, Akim Tsvigun,
                                                               soning in large language models. Advances in Neural
  Alexander Panchenko, Maxim Panov, Mikhail Burt-
                                                               Information Processing Systems, 35:24824–24837.
  sev, and Artem Shelmanov. 2023a. Hybrid uncer-
  tainty quantification for selective text classification   Jason Wei and Kai Zou. 2019. EDA: Easy data augmen-
  in ambiguous tasks. In Proceedings of the 61st An-           tation techniques for boosting performance on text
  nual Meeting of the Association for Computational            classification tasks. In Proceedings of the 2019 Con-
  Linguistics (Volume 1: Long Papers), pages 11659–            ference on Empirical Methods in Natural Language
  11681, Toronto, Canada. Association for Computa-             Processing and the 9th International Joint Confer-
  tional Linguistics.                                          ence on Natural Language Processing (EMNLP-
                                                               IJCNLP), pages 6382–6388, Hong Kong, China. As-
Artem Vazhentsev, Akim Tsvigun, Roman Vashurin,                sociation for Computational Linguistics.
  Sergey Petrakov, Daniil Vasilev, Maxim Panov,
  Alexander Panchenko, and Artem Shelmanov. 2023b.          Yijun Xiao and William Yang Wang. 2021. On hal-
  Efficient out-of-domain detection for sequence to se-       lucination and predictive uncertainty in conditional
  quence models. In Findings of the Association for           language generation. In Proceedings of the 16th Con-
  Computational Linguistics: ACL 2023, pages 1430–            ference of the European Chapter of the Association
  1454, Toronto, Canada. Association for Computa-             for Computational Linguistics: Main Volume, pages
  tional Linguistics.                                         2734–2744, Online. Association for Computational
                                                              Linguistics.
Vikas Verma, Alex Lamb, Christopher Beckham, Amir
  Najafi, Ioannis Mitliagkas, David Lopez-Paz, and          Yuxin Xiao, Paul Pu Liang, Umang Bhatt, Willie
  Yoshua Bengio. 2019. Manifold mixup: Better repre-          Neiswanger, Ruslan Salakhutdinov, and Louis-
  sentations by interpolating hidden states. In Proceed-      Philippe Morency. 2022. Uncertainty quantification
  ings of the 36th International Conference on Machine        with pre-trained language models: A large-scale em-
  Learning, ICML 2019, 9-15 June 2019, Long Beach,            pirical analysis. In Findings of the Association for
  California, USA, volume 97 of Proceedings of Ma-            Computational Linguistics: EMNLP 2022, pages
  chine Learning Research, pages 6438–6447. PMLR.             7273–7284, Abu Dhabi, United Arab Emirates. As-
                                                              sociation for Computational Linguistics.
Cunxiang Wang, Xiaoze Liu, Yuanhao Yue, Xiangru
  Tang, Tianhang Zhang, Jiayang Cheng, Yunzhi Yao,          Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie
  Wenyang Gao, Xuming Hu, Zehan Qi, Yidong Wang,              Fu, Junxian He, and Bryan Hooi. 2023. Can llms
  Linyi Yang, Jindong Wang, Xing Xie, Zheng Zhang,            express their uncertainty? an empirical evaluation
  of confidence elicitation in llms. ArXiv preprint,        Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q.
  abs/2306.13063.                                             Weinberger, and Yoav Artzi. 2020b. Bertscore: Eval-
                                                              uating text generation with BERT. In 8th Inter-
Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu,              national Conference on Learning Representations,
  Xipeng Qiu, and Xuanjing Huang. 2023. Do large              ICLR 2020, Addis Ababa, Ethiopia, April 26-30,
  language models know what they don’t know? ArXiv            2020. OpenReview.net.
  preprint, abs/2305.18153.
                                                            Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu,
KiYoon Yoo, Jangho Kim, Jiho Jang, and Nojun Kwak.            Tingchen Fu, Xinting Huang, Enbo Zhao, Yu Zhang,
  2022. Detection of word adversarial examples in text        Yulong Chen, et al. 2023b. Siren’s song in the ai
  classification: Benchmark and baseline via robust           ocean: A survey on hallucination in large language
  density estimation. ArXiv preprint, abs/2203.01677.         models. ArXiv preprint, abs/2309.01219.

Hiyori Yoshikawa and Naoaki Okazaki. 2023. Selective-       Yao Zhao, Rishabh Joshi, Tianqi Liu, Misha Khalman,
  LAMA: Selective prediction for confidence-aware             Mohammad Saleh, and Peter J Liu. 2023a. Slic-hf:
  evaluation of language models. In Findings of the As-       Sequence likelihood calibration with human feed-
  sociation for Computational Linguistics: EACL 2023,         back. ArXiv preprint, abs/2305.10425.
  pages 2017–2028, Dubrovnik, Croatia. Association
  for Computational Linguistics.                            Yao Zhao, Misha Khalman, Rishabh Joshi, Shashi
                                                              Narayan, Mohammad Saleh, and Peter J Liu.
Yue Yu, Rongzhi Zhang, Ran Xu, Jieyu Zhang, Ji-               2022. Calibrating sequence likelihood improves
  aming Shen, and Chao Zhang. 2022. Cold-start data           conditional language generation. ArXiv preprint,
  selection for few-shot language model fine-tuning:          abs/2210.00045.
  A prompt-based uncertainty propagation approach.
  ArXiv preprint, abs/2209.06995.                           Yukun Zhao, Lingyong Yan, Weiwei Sun, Guoliang
                                                              Xing, Chong Meng, Shuaiqiang Wang, Zhicong
Polina Zablotskaia, Du Phan, Joshua Maynez, Shashi            Cheng, Zhaochun Ren, and Dawei Yin. 2023b.
  Narayan, Jie Ren, and Jeremiah Liu. 2023. On un-            Knowing what llms do not know: A simple yet
  certainty calibration and selective generation in prob-     effective self-detection method. ArXiv preprint,
  abilistic neural summarization: A benchmark study.          abs/2310.17918.
  ArXiv preprint, abs/2304.08653.
                                                            Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and
Hongyi Zhang, Moustapha Cissé, Yann N. Dauphin, and           Sameer Singh. 2021. Calibrate before use: Improv-
  David Lopez-Paz. 2018. mixup: Beyond empirical              ing few-shot performance of language models. In
  risk minimization. In 6th International Conference          Proceedings of the 38th International Conference on
  on Learning Representations, ICLR 2018, Vancouver,          Machine Learning, ICML 2021, 18-24 July 2021, Vir-
  BC, Canada, April 30 - May 3, 2018, Conference              tual Event, volume 139 of Proceedings of Machine
  Track Proceedings. OpenReview.net.                          Learning Research, pages 12697–12706. PMLR.

Jiaxin Zhang, Zhuohang Li, Kamalika Das, Bradley A.         Chujie Zheng, Hao Zhou, Fandong Meng, Jie Zhou,
   Malin, and Kumar Sricharan. 2023a. Sac3: Reliable          and Minlie Huang. 2023. Large language models are
   hallucination detection in black-box language models       not robust multiple choice selectors. ArXiv preprint,
   via semantic-aware cross-check consistency. ArXiv          abs/2309.03882.
   preprint, abs/2311.01740.                                Kaitlyn Zhou, Dan Jurafsky, and Tatsunori Hashimoto.
                                                              2023. Navigating the grey area: Expressions of
Jingqing Zhang, Yao Zhao, Mohammad Saleh, and Pe-
                                                              overconfidence and uncertainty in language models.
   ter J. Liu. 2020a. PEGASUS: pre-training with ex-
                                                              ArXiv preprint, abs/2302.13439.
   tracted gap-sentences for abstractive summarization.
   In Proceedings of the 37th International Conference      Chiwei Zhu, Benfeng Xu, Quan Wang, Yongdong
   on Machine Learning, ICML 2020, 13-18 July 2020,           Zhang, and Zhendong Mao. 2023a. On the calibra-
   Virtual Event, volume 119 of Proceedings of Machine        tion of large language models and alignment. ArXiv
   Learning Research, pages 11328–11339. PMLR.                preprint, abs/2311.13240.
Shujian Zhang, Chengyue Gong, and Eunsol Choi. 2021.        Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and
  Knowing more about questions can help: Improving            Mohamed Elhoseiny. 2023b. Minigpt-4: Enhancing
  calibration in question answering. In Findings of           vision-language understanding with advanced large
  the Association for Computational Linguistics: ACL-         language models. ArXiv preprint, abs/2304.10592.
  IJCNLP 2021, pages 1958–1970, Online. Association
  for Computational Linguistics.

Susan Zhang, Stephen Roller, Naman Goyal, Mikel
  Artetxe, Moya Chen, Shuohui Chen, Christopher De-
  wan, Mona Diab, Xian Li, Xi Victoria Lin, et al. 2022.
  Opt: Open pre-trained transformer language models.
  ArXiv preprint, abs/2205.01068.
 Study                       Model                         Task                            Calibration Methods
                                                         Nature Language Inference,
 (Desai and Durrett, 2020)   BERT (Devlin et al., 2019), Paraphrase Detection,             TS, LS
                             RoBERTa (Liu et al., 2019)  Commonsense Reasoning
                                                                                           BL, ERL, MixUp, DeepEnsemble,
 (Kim et al., 2023)          RoBERTa (Liu et al., 2019)    Text Classification
                                                                                           MCDropout, MIMO
                                                           Nature Language Inference,
 (Park and Caragea, 2022)    BERT (Devlin et al., 2019),   Paraphrase Detection,           TS, LS, MixUp, Manifold-MixUp,
                             RoBERTa (Liu et al., 2019)    Commonsense Reasoning           AUM-guided MixUp
                             BERT-based Span Extractor
 (Zhang et al., 2021)                                      Extractive Question Answering   FBC
                             (Zhang et al., 2021)
                             BERT-based Span Extractor
 (Si et al., 2022)                                         Extractive Question Answering   LS, TS, FBC
                             (Si et al., 2022)

Table 3: Studies of discriminative LM calibration. Calibration methods: LS=label smoothing, TS=temperature
scaling, BL=brier loss, ERL=entropy regularization loss, BE=Bayesian Ensemble, SNGP: spectral-normalized
Gaussian process, FBC=feature-based calibrator

A     Appendix                                                      Gales, 2021b; Shelmanov et al., 2021; Vazhentsev
                                                                    et al., 2022), and there is the need to optimize the
A.1      Confidence Estimation Methods
                                                                    computation. For example, determinantal point pro-
The methods for confidence estimation have been                     cess (Kulesza and Taskar, 2012) can be applied to
extensively studied and can generally be catego-                    facilitate MCDropout by sampling diverse neurons
rized into the following groups:                                    in the dropout layer (Shelmanov et al., 2021).
Logit-based estimation Given the model input
                                                                    Density-based estimation Density-based ap-
x, the logit z, along with the prediction ŷ (i.e.,
                                                                    proaches (Lee et al., 2018; Yoo et al., 2022) are
the class with the highest probability emitted by
                                                                    based on the assumption that regions of the in-
softmax activation σ), the model confidence is esti-
                                                                    put space where training data is dense are regions
mated directly using the probability value:
                                                                    where the model is likely to be more confident in its
                                                                    predictions. Conversely, regions with sparse train-
            confsp (x, ŷ) = P (ŷ|x) = σ(z)ŷ             (8)
                                                                    ing data are areas of higher uncertainty. Lee et al.
There are methods for estimating confidence based                   (2018) first proposed a Mahalanobis distance-based
on transformations of the logit probabilities, such                 confidence score, which calculates the distance be-
as examining the gap between the two highest prob-                  tween one test point and a Gaussian distribution
abilities (Yoshikawa and Okazaki, 2023) or utiliz-                  fitting test data. The confidence estimation is ob-
ing entropy, which indicates the uncertainty with a                 tained by exponentiating the negative value of the
larger value.                                                       distance.

Ensemble-based & Bayesian methods Deep-                             Confidence learning employs a specific network
Ensemble methods (Lakshminarayanan et al., 2017)                    branch to learn the confidence of model predictions.
train multiple neural networks independently and                    DeVries and Taylor (2018) leveraged a confidence
estimate the uncertainty by computing the variance                  estimation branch to forecast scalar confidence, and
of the outputs from these models. Monte Carlo                       the original probability is modified by interpolating
dropout (MCDropout, Gal and Ghahramani 2016)                        the ground truth according to the confidence to pro-
methods extend the dropout techniques to estimat-                   vide “hints” during the training process. Addition-
ing uncertainty. As in the training phase, dropout                  ally, it discourages the network from always asking
is also applied during inference, and multiple for-                 for hints by applying a small penalty. Corbière et al.
ward passes are performed to obtain predictions.                    (2019) empirically demonstrated that confidence
The final prediction is obtained through averaging                  based on true class probability (TCP) is better for
predictions, with the variability of the predictions                distinguishing between correct and incorrect pre-
reflecting the model uncertainty.                                   dictions. Given the ground truth y, TCP can be
   Methods such as deep-ensemble and MC-                            represented as P (y|x). However, y is not available
Dropout introduce a heavy computational overhead,                   when estimating the confidence of the predictions.
especially when applied to LLMs (Malinin and                        Hence, Corbière et al. (2019) used a confidence
learning network to learn TCP confidence during        et al., 2017). Using a validation set, they fine-
training.                                              tune the predicted probabilities to better align with
                                                       the true outcomes, leveraging the negative log-
A.2     Model Calibration                              likelihood (NLL) loss. Among them, temperature
Calibration methods can be categorized based on        scaling (TS) is popular due to its low complexity
their execution time as in-training and post-hoc       and efficiency. It involves re-weighting the logits
methods.                                               before the softmax function by a learned scalar τ ,
                                                       known as the temperature.
A.2.1    In-Training Calibration
                                                       Feature-based calibrator leverages both input
Research indicates that model generalization meth-
                                                       features and model predictions to refine the pre-
ods can be used for calibration (Kim et al., 2023),
                                                       dicted probabilities. To train the calibrator, one
and calibration methods can enhance model per-
                                                       first applies a trained model on a validation dataset.
formance, particularly in out-of-domain genera-
                                                       Subsequently, both the original input features and
tion (Desai and Durrett, 2020).
                                                       the model’s predictions from this dataset are passed
Novel loss functions Many studies considered           to a binary classifier (Jagannatha and Yu, 2020;
the cross-entropy (CE) loss to be one of the causes    Jiang et al., 2021; Si et al., 2022).
leading to model miscalibration (Mukhoti et al.,
                                                       A.3   Summary
2020; Kim et al., 2023). Mukhoti et al. (2020)
demonstrated that focal loss (Lin et al., 2017), de-   Confidence estimation Logit-based methods
signed to give more importance to hard-to-classify     stand out as the most straightforward to implement
examples and to down-weight the easy-to-classify       and interpret. Reducing computational cost and
examples, can improve the calibration of neural net-   improving the sampling efficiency pose challenges
works. The correctness ranking loss (CRL; Moon         to ensemble-based and Bayesian methods. Density-
et al. 2020) calibrated models by penalizing in-       based estimation can be used to identify which data
correct rankings within the same batch and by us-      points are associated with different types of un-
ing the difference in proportions as the margin to     certainties. However, it requires assumptions of
differentiate sample confidence. Besides, entropy      data distribution (Baan et al., 2023) and can also
regularization loss (ERL; Pereyra et al. 2017) and     be computationally intensive when dealing with
label smoothing (LS; Szegedy et al. 2016) were         large datasets (Sun et al., 2022). Confidence learn-
introduced to discourage overly confident output       ing can acquire task-relevant confidence; however,
distributions.                                         it requires modifying the neural network and per-
                                                       forming specific training.
Data augmentation involves creating new train-
ing examples by applying various transformations       Model calibration Post-hoc methods are gen-
or perturbations to the original data. It has been     erally model-independent and can calibrate prob-
widely used for calibration of discriminative LMs      abilities without impacting the model’s perfor-
by alleviating the issue of over-confidence, such      mance (Guo et al., 2017). Desai and Durrett
as MixUp (Zhang et al., 2018), EDA (Wei and            (2020) empirically found that temperature scal-
Zou, 2019), Manifold-MixUp (Verma et al., 2019),       ing effectively reduces calibration error in-domain,
MIMO (Havasi et al., 2021) and AUM-guided              whereas label smoothing is more beneficial in out-
MixUp (Park and Caragea, 2022).                        of-domain settings. Kim et al. (2023) found that
                                                       augmentation can enhance both classification ac-
Ensemble and Bayesian methods were initially           curacy and calibration performance. However, en-
introduced to quantify model uncertainty. However,     semble methods may sometimes degrade model
both can also be valuable for model calibration, as    calibration if individual members produce similar
they can enhance accuracy, mitigate overfitting,       predictions due to overfitting. Table 3 represents
and reduce overconfidence (Kong et al., 2020; Kim      significant work in calibrating discriminative LMs.
et al., 2023).                                         We have comprehensively listed the models, tasks,
                                                       and calibration methods they employed.
A.2.2    Post-Hoc Calibration
Scaling methods are exemplified by matrix scal-
ing, vector scaling and temperature scaling (Guo

```
