---
citation_key: "ManakulEtAl2023"
title: "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models"
authors: "Potsawee Manakul; Adian Liusie; Mark Gales"
year: 2023
doi: "10.18653/v1/2023.emnlp-main.557"
source: "local PDF (Potsawee2023.pdf)"
access_level: "full-text-pdf"
retrieved_date: "2026-04-15"
is_user_seed: true
tier: 1
composite_score: 4.7
---
# SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models
**Authors**: Potsawee Manakul, Adian Liusie, Mark Gales
**Year**: 2023
**Venue**: —
**DOI**: [10.18653/v1/2023.emnlp-main.557](https://doi.org/10.18653/v1/2023.emnlp-main.557)

## Full Text (extracted via pdftotext) / 全文（pdftotext 抽取）

```text
                                             S ELF C HECK GPT: Zero-Resource Black-Box Hallucination Detection
                                                           for Generative Large Language Models

                                                               Potsawee Manakul, Adian Liusie, Mark J. F. Gales
                                                         ALTA Institute, Department of Engineering, University of Cambridge
                                                          pm574@cam.ac.uk, al826@cam.ac.uk, mjfg@eng.cam.ac.uk

                                                                Abstract                                                                        Stochastically-generated responses

                                                                                                                   LLM                   sample1                            sampleN
                                             Generative Large Language Models (LLMs)                            e.g. GPT-3               Giuseppe Mariani was an            Giuseppe Mariani was an
                                                                                                                                         Italian painter, sculptor,         Italian violinist,
                                             such as GPT-3 are capable of generating highly                                              and engraver. He was         ...   pedagogue and
                                                                                                                                         born in Naples, Italy, in          composer. He was born
                                             fluent responses to a wide variety of user

arXiv:2303.08896v3 [cs.CL] 11 Oct 2023
                                                                                                                                         1882, and died in Paris,           in Pavia, Italy, on 4 June
                                                                                                                            N samples                                       1836. [truncated]
                                                                                                                                         France, in 1944.
                                             prompts. However, LLMs are known to hal-                                                    [truncated]

                                             lucinate facts and make non-factual statements
                                             which can undermine trust in their output. Ex-                 Giuseppe Mariani was        LLM
                                                                                                            an Italian professional
                                             isting fact-checking approaches either require                 footballer who played         Does {sample1}                    Does {sampleN}
                                                                                                            as a forward. He was
                                             access to the output probability distribution                  born in Milan, Italy. He
                                                                                                                                          support {sentence}?         ...   support {sentence}?

                                                                                                             died in Rome, Italy.         Answer: [Yes/No]                  Answer: [Yes/No]
                                             (which may not be available for systems such                         [truncated]
                                             as ChatGPT) or external databases that are in-                     LLM's passage
                                                                                                                                                    No       ...      Yes     ...      No
                                             terfaced via separate, often complex, modules.                   to be evaluated at
                                                                                                                sentence-level
                                             In this work, we propose "SelfCheckGPT", a                                                                    SelfCheckGPT Score
                                                                                                                                        (e.g. how often is the sentence supported by the samples)
                                             simple sampling-based approach that can be
                                             used to fact-check the responses of black-box
                                             models in a zero-resource fashion, i.e. with-                Figure 1: SelfCheckGPT with Prompt. Each LLM-generated
                                                                                                          sentence is compared against stochastically generated re-
                                             out an external database. SelfCheckGPT lever-                sponses with no external database. A comparison method
                                             ages the simple idea that if an LLM has knowl-               can be, for example, through LLM prompting as shown above.
                                             edge of a given concept, sampled responses
                                             are likely to be similar and contain consistent
                                             facts. However, for hallucinated facts, stochas-             tools to draft reports, virtual assistants and sum-
                                             tically sampled responses are likely to diverge              marization systems. Despite the convincing and
                                             and contradict one another. We investigate this              realistic nature of LLM-generated texts, a growing
                                             approach by using GPT-3 to generate passages
                                                                                                          concern with LLMs is their tendency to halluci-
                                             about individuals from the WikiBio dataset, and
                                             manually annotate the factuality of the gener-
                                                                                                          nate facts. It has been widely observed that mod-
                                             ated passages. We demonstrate that SelfCheck-                els can confidently generate fictitious information,
                                             GPT can: i) detect non-factual and factual sen-              and worryingly there are few, if any, existing ap-
                                             tences; and ii) rank passages in terms of factu-             proaches to suitably identify LLM hallucinations.
                                             ality. We compare our approach to several base-                 A possible approach of hallucination detection
                                             lines and show that our approach has consider-               is to leverage existing intrinsic uncertainty metrics
                                             ably higher AUC-PR scores in sentence-level                  to determine the parts of the output sequence that
                                             hallucination detection and higher correlation
                                                                                                          the system is least certain of (Yuan et al., 2021; Fu
                                             scores in passage-level factuality assessment
                                             compared to grey-box methods.1                               et al., 2023). However, uncertainty metrics such
                                                                                                          as token probability or entropy require access to
                                         1   Introduction                                                 token-level probability distributions, information
                                                                                                          which may not be available to users for example
                                         Large Language Models (LLMs) such as GPT-3                       when systems are accessed through limited exter-
                                         (Brown et al., 2020) and PaLM (Chowdhery et al.,                 nal APIs. An alternate approach is to leverage
                                         2022) are capable of generating fluent and realistic             fact-verification approaches, where evidence is re-
                                         responses to a variety of user prompts. They have                trieved from an external database to assess the ve-
                                         been used in many applications such as automatic                 racity of a claim (Thorne et al., 2018; Guo et al.,
                                               Code and dataset can be found on the project page at       2022). However, facts can only be assessed relative
                                         https://github.com/potsawee/selfcheckgpt.                        to the knowledge present in the database. Addition-

ally, hallucinations are observed over a wide range         internal states of the LLM, which may not be avail-
of tasks beyond pure fact verification (Kryscinski          able through API calls, and requires labelled data
et al., 2020; Maynez et al., 2020).                         for supervised training. Another recent approach
   In this paper, we propose SelfCheckGPT, a                is self-evaluation (Kadavath et al., 2022), where an
sampling-based approach that can detect whether             LLM is prompted to evaluate its previous predic-
responses generated by LLMs are hallucinated or             tion, e.g., to predict the probability that its gener-
factual. To the best of our knowledge, SelfCheck-           ated response/answer is true.
GPT is the first work to analyze model halluci-
nation of general LLM responses, and is the first           2.2    Sequence Level Uncertainty Estimation
zero-resource hallucination detection solution that         Token probabilities have been used as an indica-
can be applied to black-box systems. The motivat-           tion of model certainty. For example, OpenAI’s
ing idea of SelfCheckGPT is that when an LLM                GPT-3 web interface allows users to display token
has been trained on a given concept, the sampled re-        probabilities (as shown in Figure 2), and further un-
sponses are likely to be similar and contain consis-        certainty estimation approaches based on aleatoric
tent facts. However, for hallucinated facts, stochas-       and epistemic uncertainty have been studied for
tically sampled responses are likely to diverge and         autoregressive generation (Xiao and Wang, 2021;
may contradict one another. By sampling multiple            Malinin and Gales, 2021). Additionally, condi-
responses from an LLM, one can measure informa-             tional language model scores have been used to
tion consistency between the different responses            evaluate properties of texts (Yuan et al., 2021; Fu
and determine if statements are factual or halluci-         et al., 2023). Recently, semantic uncertainty has
nated. Since SelfCheckGPT only leverages sam-               been proposed to address uncertainty in free-form
pled responses, it has the added benefit that it can        generation tasks where probabilities are attached
be used for black-box models, and it requires no            to concepts instead of tokens (Kuhn et al., 2023).
external database. Five variants of SelfCheckGPT
for measuring informational consistency are con-
sidered: BERTScore, question-answering, n-gram,
NLI, and LLM prompting. Through analysis of an-
notated articles generated by GPT-3, we show that
SelfCheckGPT is a highly effective hallucination
detection method that can even outperform grey-
box methods, and serves as a strong first baseline
for an increasingly important problem of LLMs.

2     Background and Related Work
2.1    Hallucination of Large Language Models
                                                            Figure 2: Example of OpenAI’s GPT-3 web interface with
Hallucination has been studied in text generation           output token-level probabilities displayed.
tasks, including summarization (Huang et al., 2021)
and dialogue generation (Shuster et al., 2021), as
well as in a variety of other natural language gen-         2.3    Fact Verification
eration tasks (Ji et al., 2023). Self-consistency           Existing fact-verification approaches follow a
decoding has shown to improve chain-of-thought              multi-stage pipeline of claim detection, evidence
prompting performance on complex reasoning                  retrieval and verdict prediction (Guo et al., 2022;
tasks (Wang et al., 2023). Further, Liu et al. (2022)       Zhong et al., 2020). Such methods, however, re-
introduce a hallucination detection dataset, how-           quire access to external databases and can have
ever, texts are obtained by perturbing factual texts        considerable inference costs.
and thus may not reflect true LLM hallucination.
   Recently, Azaria and Mitchell (2023) trained a           3     Grey-Box Factuality Assessment
multi-layer perception classifier where an LLM’s
hidden representations are used as inputs to pre-           This section will introduce methods that can be
dict the truthfulness of a sentence. However, this          used to determine the factuality of LLM responses
approach is a white-box approach that uses the              in a zero-resource setting when one has full access

to output distributions.2 We will use ‘factual’ to                    Entropy
define when statements are grounded in valid infor-                   The entropy of the output distribution is:
mation, i.e. when hallucinations are avoided, and
‘zero-resource’ when no external database is used.
                                                                                              X
                                                                                Hij = −              pij (w̃) log pij (w̃)
                                                                                              w̃∈W
3.1       Uncertainty-based Assessment
To understand how the factuality of a generated                       where pij (w̃) is the probability of the word w̃ being
response can be determined in a zero-resource set-                    generated at the j-th token of the i-th sentence, and
ting, we consider LLM pre-training. During pre-                       W is the set of all possible words in the vocabu-
training, the model is trained with next-word pre-                    lary. Similar to the probability-based metrics, two
diction over massive corpora of textual data. This                    entropy-based metrics are used:
gives the model a strong understanding of language
(Jawahar et al., 2019; Raffel et al., 2020), power-                                  1X
                                                                       Avg(H) =         Hij ; Max(H) = max (Hij )
ful contextual reasoning (Zhang et al., 2020), as                                    J                  j
                                                                                          j
well as world knowledge (Liusie et al., 2023). Con-
sider the input "Lionel Messi is a _". Since                          4    Black-Box Factuality Assessment
Messi is a world-famous athlete who may have
appeared multiple times in pre-training, the LLM                      A drawback of grey-box methods is that they re-
is likely to know who Messi is. Therefore given                       quire output token-level probabilities. Though this
the context, the token "footballer" may be as-                        may seem a reasonable requirement, for massive
signed a high probability while other professions                     LLMs only available through limited API calls,
such as "carpenter" may be considered improba-                        such token-level information may not be available
ble. However, for a different input such as "John                     (such as with ChatGPT). Therefore, we consider
Smith is a _", the system will be unsure of the                       black-box approaches which remain applicable
continuation which may result in a flat probability                   even when only text-based responses are available.
distribution. During inference, this is likely to lead
to a non-factual word being generated.                                Proxy LLMs
   This insight allows us to understand the con-                      A simple approach to approximate the grey-box
nection between uncertainty metrics and factuality.                   approaches is by using a proxy LLM, i.e. another
Factual sentences are likely to contain tokens with                   LLM that we have full access to, such as LLaMA
higher likelihood and lower entropy, while halluci-                   (Touvron et al., 2023). A proxy LLM can be used
nations are likely to come from positions with flat                   to approximate the output token-level probabilities
probability distributions with high uncertainty.                      of the black-box LLM generating the text. In the
Token-level Probability                                               next section, we propose SelfCheckGPT, which is
                                                                      also a black-box approach.
Given the LLM’s response R, let i denote the i-th
sentence in R, j denote the j-th token in the i-th
                                                                      5    SelfCheckGPT
sentence, J is the number of tokens in the sentence,
and pij be the probability of the word generated by                   SelfCheckGPT is our proposed black-box zero-
the LLM at the j-th token of the i-th sentence. Two                   resource hallucination detection scheme, which op-
probability metrics are used:                                         erates by comparing multiple sampled responses
                                                                      and measuring consistency.
                                   1X
            Avg(− log p) = −          log pij                            Notation: Let R refer to an LLM response
                                   J
                                       j                              drawn from a given user query. SelfCheckGPT
            Max(− log p) = max (− log pij )                           draws a further N stochastic LLM response sam-
                                  j
                                                                      ples {S 1 , S 2 , ..., S n , ..., S N } using the same query,
Max(− log p) measures the sentence’s likelihood                       and then measures the consistency between the
by assessing the least likely token in the sentence.                  response and the stochastic samples. We design
                                                                      SelfCheckGPT to predict the hallucination score of
                                                                      the i-th sentence, S(i), such that S(i) ∈ [0.0, 1.0],
      Alternate white-box approaches such as that of Azaria
and Mitchell (2023) require access to full internal states, and       where S(i) → 0.0 if the i-th sentence is grounded
is less practical and so not considered in this work.                 in valid information and S(i) → 1.0 if the i-th sen-

                                                                     Nn
tence is hallucinated.3 The following subsections                  Nm +Nn . To take into account the answerability of
will describe each of the SelfCheckGPT variants.                   generated questions, we show in Appendix B that
                                                                   we can modify the inconsistency score by applying
5.1    SelfCheckGPT with BERTScore                                 soft-counting, resulting in:
Let B(., .) denote the BERTScore between two sen-
                                                                                                             N′
tences. SelfCheckGPT with BERTScore finds the                                                        γ2 n
                                                                                 SQA (i, q) =       N′            N′
                                                                                                                       (5)
average BERTScore of the i-th sentence with the                                                 γ1 m + γ2 n
most similar sentence from each drawn sample:
                                                                   where Nm′ = the effective match count, Nn′ = the
                              N
                          1   X                                    effective mismatch count, with γ1 and γ2 defined
      SBERT (i) = 1 −               max (B(ri , snk ))   (1)
                          N          k                             in Appendix B.1. Ultimately, SelfCheckGPT with
                              n=1
                                                                   QA is the average of inconsistency scores across q,
where ri represents the i-th sentence in R and snk
represents the k-th sentence in the n-th sample S n .                            SQA (i) = Eq [SQA (i, q)]             (6)
This way if the information in a sentence appears
in many drawn samples, one may assume that the                     5.3   SelfCheckGPT with n-gram
information is factual, whereas if the statement ap-               Given samples {S 1 , ..., S N } generated by an LLM,
pears in no other sample, it is likely a hallucination.            one can use the samples to create a new language
In this work, RoBERTa-Large (Liu et al., 2019) is                  model that approximates the LLM. In the limit as
used as the backbone of BERTScore.                                 N gets sufficiently large, the new language model
                                                                   will converge to the LLM that generated the re-
5.2    SelfCheckGPT with Question Answering                        sponses. We can therefore approximate the LLM’s
We also consider using the automatic multiple-                     token probabilities using the new language model.
choice question answering generation (MQAG)                           In practice, due to time and/or cost constraints,
framework (Manakul et al., 2023) to measure con-                   there can only be a limited number of samples N .
sistency for SelfCheckGPT. MQAG assesses con-                      Consequently, we train a simple n-gram model us-
sistency by generating multiple-choice questions                   ing the samples {S 1 , ..., S N } as well as the main
over the main generated response, which an inde-                   response R (which is assessed), where we note
pendent answering system can attempt to answer                     that including R can be considered as a smoothing
while conditioned on the other sampled responses.                  method where the count of each token in R is in-
If questions on consistent information are queried,                creased by 1. We then compute the average of the
the answering system is expected to predict similar                log-probabilities of the sentence in response R,
answers. MQAG consists of two stages: question
                                                                               Avg              1X
generation G and question answering A. For the sen-                           Sn-gram (i) = −      log p̃ij            (7)
tence ri in the response R, we draw questions q                                                 J
                                                                                                         j
and options o:
                                                                   where p̃ij is the probability (of the j-th token of the
                 q, o ∼ PG (q, o|ri , R)                 (2)       i-th sentence) computed using the n-gram model.
                                                                   Similar to the grey-box approach, we can also use
The answering stage A selects the answers:                         the maximum of the negative log probabilities,

           aR = argmax [PA (ok |q, R, o)]                (3)                   Max
                                                                              Sn-gram (i) = max (− log p̃ij )          (8)
                      k                                                                         j

          aS n = argmax [PA (ok |q, S n , o)]            (4)
                      k                                            5.4   SelfCheckGPT with NLI
                                                                   Natural Language Inference (NLI) determines
We compare whether aR is equal to aS n for each
                                                                   whether a hypothesis follows a premise, classified
sample in {S 1 , ..., S N }, yielding #matches Nm and
                                                                   into either entailment/neutral/contradiction. NLI
#not-matches Nn . A simple inconsistency score
                                                                   measures have been used to measure faithfulness in
for the i-th sentence and question q based on the
                                                                   summarization, where Maynez et al. (2020) use
match/not-match counts is defined: SQA (i, q) =
                                                                   a textual entailment classifier trained on MNLI
      With the exception of SelfCheckGPT with n-gram as the        (Williams et al., 2018) to determine if a summary
score of the n-gram language model is not bounded.                 contradicts a context or not. Inspired by NLI-based

summary assessment, we consider using the NLI                6    Data and Annotation
contradiction score as a SelfCheckGPT score.
                                                             As, currently, there are no standard hallucination
  For SelfCheck-NLI, we use DeBERTa-v3-large
                                                             detection datasets available, we evaluate our hallu-
(He et al., 2023) fine-tuned to MNLI as the NLI
                                                             cination detection approaches by 1) generating syn-
model. The input for NLI classifiers is typically the
                                                             thetic Wikipedia articles using GPT-3 on the indi-
premise concatenated to the hypothesis, which
                                                             viduals/concepts from the WikiBio dataset (Lebret
for our methodology is the sampled passage S n
                                                             et al., 2016); 2) manually annotating the factuality
concatenated to the sentence to be assessed ri .
                                                             of the passage at a sentence level; 3) evaluating the
Only the logits associated with the ‘entailment’
                                                             system’s ability to detect hallucinations.
and ‘contradiction’ classes are considered,
                                                                WikiBio is a dataset where each input contains
                                    exp(zc )                 the first paragraph (along with tabular information)
  P (contradict|ri , S n ) =                       (9)
                               exp(ze ) + exp(zc )           of Wikipedia articles of a specific concept. We rank
                                                             the WikiBio test set in terms of paragraph length
where ze and zc are the logits of the ‘entailment’
                                                             and randomly sample 238 articles from the top
and ‘contradiction’ classes, respectively. This nor-
                                                             20% of longest articles (to ensure no very obscure
malization ignores the neutral class and ensures
                                                             concept is selected). GPT-3 (text-davinci-003) is
that the probability is bounded between 0.0 and
                                                             then used to generate Wikipedia articles on a con-
1.0. The SelfCheckGPT with NLI score for each
                                                             cept, using the prompt "This is a Wikipedia
sample S n is then defined as,
                                                             passage about {concept}:". Table 1 provides
                     N                                       the statistics of GPT-3 generated passages.
                 1 X
      SNLI (i) =     P (contradict|ri , S n )     (10)
                 N
                    n=1                                          #Passages     #Sentences      #Tokens/passage
5.5    SelfCheckGPT with Prompt                                     238            1908            184.7±36.9
LLMs have recently been shown to be effective in
                                                             Table 1: The statistics of WikiBio GPT-3 dataset where the
assessing information consistency between a doc-             number of tokens is based on the OpenAI GPT-2 tokenizer.
ument and its summary in zero-shot settings (Luo
et al., 2023). Thus, we query an LLM to assess               We then annotate the sentences of the generated
whether the i-th sentence is supported by sample             passages using the guidelines shown in Figure 3
S n (as the context) using the following prompt.             such that each sentence is classified as either:
------------------------------------------------
Context: {}                                                      • Major Inaccurate (Non-Factual, 1): The sen-
Sentence: {}                                                       tence is entirely hallucinated, i.e. the sentence
Is the sentence supported by the context above?
Answer Yes or No:                                                  is unrelated to the topic.
------------------------------------------------
                                                                 • Minor Inaccurate (Non-Factual, 0.5): The
Initial investigation showed that GPT-3 (text-                     sentence consists of some non-factual infor-
davinci-003) will output either Yes or No 98% of                   mation, but the sentence is related to the topic.
the time, while any remaining outputs can be set to
N/A. The output from prompting when comparing                    • Accurate (Factual, 0): The information pre-
the i-th sentence against sample S n is converted to               sented in the sentence is accurate.
score xni through the mapping {Yes: 0.0, No: 1.0,
N/A: 0.5}. The final inconsistency score is then             Of the 1908 annotated sentences, 761 (39.9%) of
calculated as:                                               the sentences were labelled major-inaccurate, 631
                                                             (33.1%) minor-inaccurate, and 516 (27.0%) accu-
                                   N
                             1 X n                           rate. 201 sentences in the dataset had annotations
               SPrompt (i) =    xi                (11)       from two different annotators. To obtain a single la-
                             N
                                  n=1
                                                             bel for this subset, if both annotators agree, then the
SelfCheckGPT-Prompt is illustrated in Figure 1.              agreed label is used. However, if there is disagree-
Note that our initial investigations found that less         ment, then the worse-case label is selected (e.g.,
capable models such as GPT-3 (text-curie-001) or             {minor inaccurate, major inaccurate} is mapped to
LLaMA failed to effectively perform consistency              major inaccurate). The inter-annotator agreement,
assessment via such prompting.                               as measured by Cohen’s κ (Cohen, 1960), has κ

                                                                                    N =20 samples. For the proxy LLM approach, we
                    Is it related to       No        Major Inaccurate               use LLaMA (Touvron et al., 2023), one of the best-
                      the context                    (Non-factual 1)
                                                                                    performing open-source LLMs currently available.
                                                                                    For SelfCheckGPT-Prompt, we consider both GPT-
                              Yes                                                   3 (which is the same LLM that is used to generate
                                                                                    passages) as well as the newly released ChatGPT
                      Is it Factual?       No                                       (gpt-3.5-turbo). More details about the systems in
                                                     Minor Inaccurate
                 e.g. using Wikipedia /
                                                    (Non-factual 0.5)               SelfCheckGPT and results using other proxy LLMs
                    Google Search
                                                                                    can be found in the appendix.
                              Yes
                                                                                    7.1        Sentence-level Hallucination Detection
                      Accurate                                                      First, we investigate whether our hallucination de-
                     (Factual 0)
                                                                                    tection methods can identify the factuality of sen-
             Figure 3: Flowchart of our annotation process                          tences. In detecting non-factual sentences, both
                                                                                    major-inaccurate labels and minor-inaccurate la-
                                                                                    bels are grouped together into the non-factual class,
values of 0.595 and 0.748, indicating moderate and
                                                                                    while the factual class refers to accurate sentences.
substantial agreement (Viera et al., 2005) for the
                                                                                    In addition, we consider a more challenging task of
3-class and 2-class scenarios, respectively.4
                                                                                    detecting major-inaccurate sentences in passages
   Furthermore, passage-level scores are obtained
                                                                                    that are not total hallucination passages, which we
by averaging the sentence-level labels in each pas-
                                                                                    refer to as non-factual∗ .5 Figure 5 and Table 2
sage. The distribution of passage-level scores is
                                                                                    show the performance of our approaches, where
shown in Figure 4, where we observe a large peak
                                                                                    the following observations can be made:
at +1.0. We refer to the points at this peak as total
hallucination, which occurs when the information                                       1) LLM’s probabilities p correlate well with
of the response is unrelated to the real concept and                                factuality. Our results show that probability mea-
is entirely fabricated by the LLM.                                                  sures (from the LLM generating the texts) are
                                                                                    strong baselines for assessing factuality. Factual
                                                                                    sentences can be identified with an AUC-PR of
                                                                                    53.97, significantly better than the random baseline
            25                                                                      of 27.04, with the AUC-PR for hallucination detec-
            20                                                                      tion also increasing from 72.96 to 83.21. This sup-
    Count   15
                                                                                    ports the hypothesis that when the LLMs are uncer-
                                                                                    tain about generated information, generated tokens
                                                                                    often have higher uncertainty, paving a promising
            5                                                                       direction for hallucination detection approaches.
            0                                                                       Also, the probability p measure performs better
                    0.0        0.2         0.4       0.6        0.8       1.0
                     Avg. Factuality per Document (0=Factual, +1=Non-Factual)       than the entropy H measure of top-5 tokens.
                                                                                       2) Proxy LLM perform noticeably worse than
     Figure 4: Document factuality scores histogram plot
                                                                                    LLM (GPT-3). The results of proxy LLM (based
                                                                                    on LLaMA) show that the entropy H measures
7      Experiments                                                                  outperform the probability measures. This sug-
                                                                                    gests that using richer uncertainty information can
The generative LLM used to generate passages for                                    improve factuality/hallucination detection perfor-
our dataset is GPT-3 (text-davinci-003), the state-                                 mance, and that previously the entropy of top-5
of-the-art system at the time of creating and anno-                                 tokens is likely to be insufficient. In addition, when
tating the dataset. To obtain the main response, we                                 using other proxy LLMs such as GPT-NeoX or
set the temperature to 0.0 and use standard beam                                    OPT-30B, the performance is near that of the ran-
search decoding. For the stochastically generated                                   dom baseline. We believe this poor performance
samples, we set the temperature to 1.0 and generate                                 occurs as different LLMs have different generating
      3-class refers to when selecting between accurate, mi-                        patterns, and so even common tokens may have a
nor inaccurate, major inaccurate. 2-class refers to when mi-
nor/major inaccuracies are combined into one label.                                       5
                                                                                              There are 206 non-factual∗ passages (1632 sentences).

                                                                                        1.0                                    Random                         1.0                                         Random
            1.00                                         Random
                                                         GPT-3 Avg(-logP)                                                      GPT-3 Avg(-logP)                                                           GPT-3 Avg(-logP)
                                                         SelfCk-BERTScore               0.9                                    SelfCk-BERTScore               0.9                                         SelfCk-BERTScore
            0.95                                         SelfCk-QA                                                             SelfCk-QA                                                                  SelfCk-QA
                                                         SelfCk-Unigram                 0.8                                    SelfCk-Unigram                 0.8                                         SelfCk-Unigram
                                                         SelfCk-Prompt                                                         SelfCk-Prompt                                                              SelfCk-Prompt
            0.90                                                                                                               SelfCk-NLI                     0.7                                         SelfCk-NLI
                                                         SelfCk-NLI                     0.7
Precision   0.85                                                            Precision   0.6                                                       Precision   0.6
                                                                                                                                                              0.5
            0.80                                                                        0.5
                                                                                                                                                              0.4
            0.75
                                                                                        0.4
                                                                                                                                                              0.3
                                                                                        0.3
            0.70                                                                                                                                              0.2
                   0.0       0.2    0.4            0.6      0.8       1.0                     0.0   0.2   0.4            0.6      0.8       1.0                     0.0     0.2      0.4            0.6      0.8       1.0
                                          Recall                                                                Recall                                                                     Recall

                    (a) Non-Factual Sentences                                                  (b) Non-Factual* Sentences                                                 (c) Factual Sentences

                         Figure 5: PR-Curve of detecting non-factual and factual sentences in the GPT-3 generated WikiBio passages.

                                                                                Sentence-level (AUC-PR)                                           Passage-level (Corr.)
                                   Method
                                                                              NonFact NonFact* Factual                                            Pearson Spearman
                                   Random               72.96        29.72     27.04    -                                                                                           -
                                   GPT-3 (text-davinci-003)’s probabilities (LLM, grey-box)
                                   Avg(−logp)           83.21        38.89     53.97  57.04                                                                                       53.93
                                   Avg(H)†              80.73        37.09     52.07  55.52                                                                                       50.87
                                   Max(−logp)           87.51        35.88     50.46  57.83                                                                                       55.69
                                   Max(H)†              85.75        32.43     50.27  52.48                                                                                       49.55
                                   LLaMA-30B’s probabilities (Proxy LLM, black-box)
                                   Avg(−logp)           75.43        30.32     41.29  21.72                                                                                       20.20
                                   Avg(H)               80.80        39.01     42.97  33.80                                                                                       39.49
                                   Max(−logp)           74.01        27.14     31.08 -22.83                                                                                       -22.71
                                   Max(H)               80.92        37.32     37.90  35.57                                                                                       38.94
                                   SelfCheckGPT (black-box)
                                   w/ BERTScore         81.96        45.96     44.23  58.18                                                                                       55.90
                                   w/ QA                84.26        40.06     48.14  61.07                                                                                       59.29
                                   w/ Unigram (max)     85.63        41.04     58.47  64.71                                                                                       64.91
                                   w/ NLI               92.50        45.17     66.08  74.14                                                                                       73.78
                                   w/ Prompt            93.42        53.19     67.09  78.32                                                                                       78.30

Table 2: AUC-PR for sentence-level detection tasks. Passage-level ranking performances are measured by Pearson correlation
coefficient and Spearman’s rank correlation coefficient w.r.t. human judgements. The results of other proxy LLMs, in addition to
LLaMA, can be found in the appendix. † GPT-3 API returns the top-5 tokens’ probabilities, which are used to compute entropy.

low probability in situations where the response                                                                   across different setups. Essentially, when assessing
is dissimilar to the generation style of the proxy                                                                 a sentence, this method picks up the token with
LLM. We note that a weighted conditional LM                                                                        the lowest occurrence given all the samples. This
score such as BARTScore (Yuan et al., 2021) could                                                                  suggests that if a token only appears a few times
be incorporated in future investigations.                                                                          (or once) within the generated samples (N =20), it
   3) SelfCheckGPT outperforms grey-box ap-                                                                        is likely non-factual.
proaches. It can be seen that SelfCheckGPT-                                                                           4) SelfCheckGPT with n-gram. When inves-
Prompt considerably outperforms the grey-box ap-                                                                   tigating the n-gram performance from 1-gram to
proaches (including GPT-3’s output probabilities)                                                                  5-gram, the results show that simply finding the
as well as other black-box approaches. Even other                                                                  least likely token/n-gram is more effective than
variants of SelfCheckGPT, including BERTScore,                                                                     computing the average n-gram score of the sen-
QA, and n-gram, outperform the grey-box ap-                                                                        tence, details in appendix Table 7. Additionally,
proaches in most setups. Interestingly, despite be-                                                                as n increases, the performance of SelfCheckGPT
ing the least computationally expensive method,                                                                    with n-gram (max) drops.
SelfCheckGPT with unigram (max) works well                                                                            5) SelfCheckGPT with NLI. The NLI-based

               0.7                                                                                                                                              1.0
               0.6                                                                      25
                                                                                                                                                                0.8
               0.5                                                                      20

Method Score                                                             Method Score                                                            Method Score
               0.4                                                                                                                                              0.6
               0.3                                                                                                                                              0.4
               0.2
                                                                                                                                                                0.2
               0.1                                                                      5

               0.0                                                                                                                                              0.0
                     0.0      0.2       0.4      0.6      0.8      1.0                       0.0      0.2       0.4      0.6      0.8      1.0                        0.0      0.2       0.4      0.6      0.8      1.0
                           Human Score (0=Factual, +1=Non-Factual)                                 Human Score (0=Factual, +1=Non-Factual)                                  Human Score (0=Factual, +1=Non-Factual)

                           (a) GPT-3 Avg(− log p)                                                  (b) LLaMA-30B Avg(H)                                                 (c) SelfCheckGPT-Prompt

Figure 6: Scatter plot of passage-level scores where Y-axis = Method scores, X-axis = Human scores. Correlations are reported
in Table 2. The scatter plots of other SelfCheckGPT variants are provided in Figure 10 in the appendix.

method outperforms all black-box and grey-box                                                                         7.3      Ablation Studies
baselines, and its performance is close to the per-                                                                   External Knowledge (instead of SelfCheck)
formance of the Prompt method. As SelfCheck-
                                                                                                                      If external knowledge is available, one can measure
GPT with Prompt can be computationally heavy,
                                                                                                                      the informational consistency between the LLM
SelfCheckGPT with NLI could be the most practi-
                                                                                                                      response and the information source. In this exper-
cal method as it provides a good trade-off between
                                                                                                                      iment, we use the first paragraph of each concept
performance and computation.
                                                                                                                      that is available in WikiBio.6
7.2                   Passage-level Factuality Ranking                                                                                                   Sent-lvl AUC-PR                             Passage-lvl
                                                                                                                        Method
                                                                                                                                                       NoFac NoFac* Fact                            Pear. Spear.
Previous results demonstrate that SelfCheckGPT
is an effective approach for predicting sentence-                                                                       SelfCk-BERT                      81.96               45.96       44.23 58.18 55.90
                                                                                                                        WikiBio+BERT                     81.32               40.62       49.15 58.71 55.80
level factuality. An additional consideration is
whether SelfCheckGPT can also be used to de-                                                                            SelfCk-QA                        84.26               40.06       48.14 61.07 59.29
                                                                                                                        WikiBio+QA                       84.18               45.40       52.03 57.26 53.62
termine the overall factuality of passages. Passage-
                                                                                                                        SelfCk-1gm                       85.63               41.04       58.47 64.71 64.91
level factuality scores are calculated by averaging                                                                     WikiBio+1gm                      80.43               31.47       40.53 28.67 26.70
the sentence-level scores over all sentences.
                                                                                                                        SelfCk-NLI                       92.50               45.17       66.08 74.14 73.78
                                                                                                                        WikiBio+NLI                      91.18               48.14       71.61 78.84 80.00
                                                1 X
                                    Spassage =      S(i)                                                 (12)           SelfCk-Prompt  93.42                                 53.19       67.09 78.32 78.30
                                               |R|
                                                                i                                                       WikiBio+Prompt 93.59                                 65.26       73.11 85.90 86.11

where S(i) is the sentence-level score, and |R|                                                                       Table 3: The performance when using SelfCheckGPT samples
is the number of sentences in the passage. Since                                                                      versus external stored knowledge.
human judgement is somewhat subjective, averag-
ing the sentence-level labels would lead to ground                                                                    Our findings in Table 3 show the following. First,
truths with less noise. Note that for Avg(− log p)                                                                    SelfCheckGPT with BERTScore/QA, using self-
and Avg(H), we compute the average over all to-                                                                       samples, can yield comparable or even better per-
kens in a passage. Whereas for Max(− log p) and                                                                       formance than when using the reference passage.
Max(H), we first take the maximum operation over                                                                      Second, SelfCheckGPT with n-gram shows a large
tokens at the sentence level, and we then average                                                                     performance drop when using the WikiBio pas-
over all sentences following Equation 12.                                                                             sages instead of self-samples. This failure is at-
   Our results in Table 2 and Figure 6 show that all                                                                  tributed to the fact that the WikiBio reference text
SelfCheckGPT methods correlate far better with                                                                        alone is not sufficient to train an n-gram model.
human judgements than the other baselines, in-                                                                        Third, in contrast, SelfCheckGPT with NLI/Prompt
cluding the grey-box probability and entropy meth-                                                                    can benefit considerably when access to retrieved
ods. SelfCheckGPT-Prompt is the best-performing                                                                       information is available. Nevertheless, in practice,
method, achieving the highest Pearson correlation
of 78.32. Unsurprisingly, the proxy LLM approach                                                                           6
                                                                                                                             This method is no longer zero-resource as it requires
again achieves considerably lower correlations.                                                                       retrieving relevant knowledge from external data.

it is infeasible to have an external database for ev-                                     8   Conclusions
ery possible use case of LLM generation.
                                                                                          This paper is the first work to consider the task
The Impact of the Number of Samples                                                       of hallucination detection for general large lan-
                                                                                          guage model responses. We propose SelfCheck-
Although sample-based methods are expected to
                                                                                          GPT, a zero-resource approach that is applicable
perform better when more samples are drawn, this
                                                                                          to any black-box LLM without the need for ex-
has higher computational costs. Thus, we inves-
                                                                                          ternal resources, and demonstrate the efficacy of
tigate performance as the number of samples is
                                                                                          our method. SelfCheckGPT outperforms a range
varied. Our results in Figure 7 show that the per-
                                                                                          of considered grey-box and black-box baseline de-
formance of SelfCheckGPT increases smoothly as
                                                                                          tection methods at both the sentence and passage
more samples are used, with diminishing gains as
                                                                                          levels, and we further release an annotated dataset
more samples are generated. SelfCheckGPT with
                                                                                          for GPT-3 hallucination detection with sentence-
n-gram requires the highest number of samples
                                                                                          level factuality labels.
before its performance reaches a plateau.

                            80                                                            Limitations
                                                                                          In this study, the 238 GPT-3 generated texts were

        Spearman's RankCC
                            60                                                            predominantly passages about individuals in the
                                                                                          WikiBio dataset. To further investigate the nature
                                                                                          of LLM’s hallucination, this study could be ex-
                            40                                 SelfCk-BERTScore           tended to a wider range of concepts, e.g., to also
                                                               SelfCk-QA
                                                               SelfCk-Unigram             consider generated texts about locations and ob-
                            30                                 SelfCk-NLI
                                                               SelfCk-Prompt              jects. Further, this work considers factuality at the
                                 0   2   4   6   8 10 12 14       16   18   20            sentence level, but we note that a single sentence
                                                  Num. samples
                                                                                          may consist of both factual and non-factual infor-
Figure 7: The performance of SelfCheckGPT methods on                                      mation. For example, the following work by Min
ranking passages (Spearman’s) versus the number of samples.                               et al. (2023) considers a fine-grained factuality eval-
                                                                                          uation by decomposing sentences into atomic facts.
                                                                                          Finally, SelfCheckGPT with Prompt, which was
The Choice of LLM for SelfCheckGPT-Prompt                                                 convincingly the best selfcheck method, is quite
                                                                                          computationally heavy. This might lead to impracti-
We investigate whether the LLM generating the
                                                                                          cal computational costs, which could be addressed
text can self-check its own text. We conduct this
                                                                                          in future work to be made more efficient.
ablation using a reduced set of the samples (N =4).

   Text-Gen                          SelfCk-Prompt        N       Pear.      Spear.       Ethics Statement
   GPT-3                             ChatGPT              20     78.32       78.30
   GPT-3                             ChatGPT               4     76.47       76.41        As this work addresses the issue of LLM’s halluci-
   GPT-3                             GPT-3                4      73.11       74.69        nation, we note that if hallucinated contents are not
   †
       SelfCheck w/ unigram (max)                         20     64.71       64.91        detected, they could lead to misinformation.
   †
       SelfCheck w/ NLI                                   20     74.14       73.78

Table 4: Comparison of GPT-3 (text-davinci-003) and Chat-                                 Acknowledgments
GPT (gpt-3.5.turbo) as the prompt-based text evaluator in
SelfCheckGPT-Prompt. † Taken from Table 2 for comparison.                                 This work is supported by Cambridge University
                                                                                          Press & Assessment (CUP&A), a department of
The results in Table 4 show that GPT-3 can self-                                          The Chancellor, Masters, and Scholars of the Uni-
check its own text, and is better than the unigram                                        versity of Cambridge, and the Cambridge Com-
method even when using only 4 samples. However,                                           monwealth, European & International Trust. We
ChatGPT shows a slight improvement over GPT-3                                             would like to thank the anonymous reviewers for
in evaluating whether the sentence is supported by                                        their helpful comments.
the context. More details are in Appendix C.

References                                                       Madotto, and Pascale Fung. 2023. Survey of halluci-
                                                                 nation in natural language generation. ACM Comput.
Amos Azaria and Tom Mitchell. 2023. The internal                 Surv., 55(12).
 state of an llm knows when its lying. arXiv preprint
 arXiv:2304.13734.
                                                               Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
Iz Beltagy, Matthew E. Peters, and Arman Cohan. 2020.            Henighan, Dawn Drain, Ethan Perez, Nicholas
   Longformer: The long-document transformer.                    Schiefer, Zac Hatfield Dodds, Nova DasSarma,
                                                                 Eli Tran-Johnson, et al. 2022. Language models
Sidney Black, Stella Biderman, Eric Hallahan, Quentin            (mostly) know what they know. arXiv preprint
  Anthony, Leo Gao, Laurence Golding, Horace                     arXiv:2207.05221.
   He, Connor Leahy, Kyle McDonell, Jason Phang,
   Michael Pieler, Usvsn Sai Prashanth, Shivanshu Puro-        Wojciech Kryscinski, Bryan McCann, Caiming Xiong,
   hit, Laria Reynolds, Jonathan Tow, Ben Wang, and             and Richard Socher. 2020. Evaluating the factual
   Samuel Weinbach. 2022. GPT-NeoX-20B: An open-                consistency of abstractive text summarization. In
   source autoregressive language model. In Proceed-            Proceedings of the 2020 Conference on Empirical
   ings of BigScience Episode #5 – Workshop on Chal-            Methods in Natural Language Processing (EMNLP),
   lenges & Perspectives in Creating Large Language             pages 9332–9346, Online. Association for Computa-
  Models, pages 95–136, virtual+Dublin. Association             tional Linguistics.
   for Computational Linguistics.
                                                               Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie                    Semantic uncertainty: Linguistic invariances for un-
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind             certainty estimation in natural language generation.
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda               In The Eleventh International Conference on Learn-
  Askell, et al. 2020. Language models are few-shot              ing Representations.
  learners. Advances in neural information processing
  systems, 33:1877–1901.                                       Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang,
                                                                 and Eduard Hovy. 2017. RACE: Large-scale ReAd-
Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,                ing comprehension dataset from examinations. In
  Maarten Bosma, Gaurav Mishra, Adam Roberts,                    Proceedings of the 2017 Conference on Empirical
  Paul Barham, Hyung Won Chung, Charles Sutton,                  Methods in Natural Language Processing, pages 785–
  Sebastian Gehrmann, et al. 2022. Palm: Scaling                 794, Copenhagen, Denmark. Association for Compu-
  language modeling with pathways. arXiv preprint                tational Linguistics.
  arXiv:2204.02311.

Jacob Cohen. 1960. A coefficient of agreement for              Rémi Lebret, David Grangier, and Michael Auli. 2016.
   nominal scales. Educational and Psychological Mea-            Generating text from structured data with application
   surement, 20:37 – 46.                                         to the biography domain. CoRR, abs/1603.07771.

Jinlan Fu, See-Kiong Ng, Zhengbao Jiang, and Pengfei           Tianyu Liu, Yizhe Zhang, Chris Brockett, Yi Mao,
   Liu. 2023. Gptscore: Evaluate as you desire.                  Zhifang Sui, Weizhu Chen, and Bill Dolan. 2022.
                                                                 A token-level reference-free hallucination detection
Zhijiang Guo, Michael Schlichtkrull, and Andreas Vla-            benchmark for free-form text generation. In Proceed-
  chos. 2022. A survey on automated fact-checking.               ings of the 60th Annual Meeting of the Association
  Transactions of the Association for Computational              for Computational Linguistics (Volume 1: Long Pa-
  Linguistics, 10:178–206.                                       pers), pages 6723–6737, Dublin, Ireland. Association
                                                                 for Computational Linguistics.
Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2023.
  DeBERTav3: Improving deBERTa using ELECTRA-                  Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
  style pre-training with gradient-disentangled embed-           dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
  ding sharing. In The Eleventh International Confer-            Luke Zettlemoyer, and Veselin Stoyanov. 2019.
  ence on Learning Representations.                              Roberta: A robustly optimized bert pretraining ap-
                                                                 proach. arXiv preprint arXiv:1907.11692.
Yichong Huang, Xiachong Feng, Xiaocheng Feng, and
  Bing Qin. 2021. The factual inconsistency problem
  in abstractive text summarization: A survey.                 Adian Liusie, Vatsal Raina, and Mark Gales. 2023.
                                                                “world knowledge” in multiple choice reading com-
Ganesh Jawahar, Benoît Sagot, and Djamé Seddah.                  prehension. In Proceedings of the Sixth Fact Ex-
  2019. What does BERT learn about the structure of              traction and VERification Workshop (FEVER), pages
  language? In Proceedings of the 57th Annual Meet-              49–57, Dubrovnik, Croatia. Association for Compu-
  ing of the Association for Computational Linguistics,          tational Linguistics.
  pages 3651–3657, Florence, Italy. Association for
  Computational Linguistics.                                   Zheheng Luo, Qianqian Xie, and Sophia Ananiadou.
                                                                 2023. Chatgpt as a factual inconsistency evaluator
Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan             for abstractive text summarization. arXiv preprint
  Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea                  arXiv:2303.15621.

Andrey Malinin and Mark Gales. 2021. Uncertainty                 Anthony J Viera, Joanne M Garrett, et al. 2005. Under-
  estimation in autoregressive structured prediction. In           standing interobserver agreement: the kappa statistic.
  International Conference on Learning Representa-                 Fam med, 37(5):360–363.
  tions.
                                                                 Ben Wang and Aran Komatsuzaki. 2021. GPT-J-
Potsawee Manakul, Adian Liusie, and Mark JF Gales.                 6B: A 6 Billion Parameter Autoregressive Lan-
  2023. MQAG: Multiple-choice question answering                   guage Model. https://github.com/kingoflolz/
  and generation for assessing information consistency             mesh-transformer-jax.
  in summarization. arXiv preprint arXiv:2301.12307.
                                                                 Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le,
Joshua Maynez, Shashi Narayan, Bernd Bohnet, and                   Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
  Ryan McDonald. 2020. On faithfulness and factu-                  and Denny Zhou. 2023. Self-consistency improves
  ality in abstractive summarization. In Proceedings               chain of thought reasoning in language models. In
  of the 58th Annual Meeting of the Association for                The Eleventh International Conference on Learning
  Computational Linguistics, pages 1906–1919, On-                  Representations.
  line. Association for Computational Linguistics.
                                                                 Adina Williams, Nikita Nangia, and Samuel Bowman.
Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike                        2018. A broad-coverage challenge corpus for sen-
  Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer,                   tence understanding through inference. In Proceed-
  Luke Zettlemoyer, and Hannaneh Hajishirzi. 2023.                 ings of the 2018 Conference of the North American
  Factscore: Fine-grained atomic evaluation of factual             Chapter of the Association for Computational Lin-
  precision in long form text generation. arXiv preprint           guistics: Human Language Technologies, Volume
  arXiv:2305.14251.                                                1 (Long Papers), pages 1112–1122, New Orleans,
                                                                   Louisiana. Association for Computational Linguis-
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine                tics.
  Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
  Wei Li, and Peter J Liu. 2020. Exploring the limits            Yijun Xiao and William Yang Wang. 2021. On hal-
  of transfer learning with a unified text-to-text trans-          lucination and predictive uncertainty in conditional
  former. The Journal of Machine Learning Research,                language generation. In Proceedings of the 16th Con-
  21(1):5485–5551.                                                 ference of the European Chapter of the Association
                                                                   for Computational Linguistics: Main Volume, pages
Vatsal Raina and Mark Gales. 2022. Answer uncertainty              2734–2744, Online. Association for Computational
  and unanswerability in multiple-choice machine read-             Linguistics.
  ing comprehension. In Findings of the Association
  for Computational Linguistics: ACL 2022, pages                 Weizhe Yuan, Graham Neubig, and Pengfei Liu. 2021.
  1020–1034, Dublin, Ireland. Association for Compu-              Bartscore: Evaluating generated text as text gener-
  tational Linguistics.                                           ation. Advances in Neural Information Processing
                                                                  Systems, 34:27263–27277.
Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and
   Percy Liang. 2016. SQuAD: 100,000+ questions for              Susan Zhang, Stephen Roller, Naman Goyal, Mikel
   machine comprehension of text. In Proceedings of                Artetxe, Moya Chen, Shuohui Chen, Christopher De-
   the 2016 Conference on Empirical Methods in Natu-               wan, Mona Diab, Xian Li, Xi Victoria Lin, et al. 2022.
   ral Language Processing, pages 2383–2392, Austin,               Opt: Open pre-trained transformer language models.
  Texas. Association for Computational Linguistics.                arXiv preprint arXiv:2205.01068.

Kurt Shuster, Spencer Poff, Moya Chen, Douwe Kiela,              Zhuosheng Zhang, Yuwei Wu, Hai Zhao, Zuchao Li,
  and Jason Weston. 2021. Retrieval augmentation                   Shuailiang Zhang, Xi Zhou, and Xiang Zhou. 2020.
  reduces hallucination in conversation. In Findings               Semantics-aware bert for language understanding. In
  of the Association for Computational Linguistics:                Proceedings of the AAAI Conference on Artificial
  EMNLP 2021, pages 3784–3803, Punta Cana, Do-                     Intelligence, volume 34, pages 9628–9635.
  minican Republic. Association for Computational                Wanjun Zhong, Jingjing Xu, Duyu Tang, Zenan Xu, Nan
  Linguistics.                                                     Duan, Ming Zhou, Jiahai Wang, and Jian Yin. 2020.
                                                                   Reasoning over semantic-level graph for fact check-
James Thorne, Andreas Vlachos, Oana Cocarascu,
                                                                   ing. In Proceedings of the 58th Annual Meeting of
  Christos Christodoulopoulos, and Arpit Mittal. 2018.
                                                                   the Association for Computational Linguistics, pages
  The Fact Extraction and VERification (FEVER)
                                                                   6170–6180, Online. Association for Computational
  shared task. In Proceedings of the First Workshop on
                                                                   Linguistics.
  Fact Extraction and VERification (FEVER).

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,
  Baptiste Rozière, Naman Goyal, Eric Hambro,
  Faisal Azhar, et al. 2023. Llama: Open and effi-
  cient foundation language models. arXiv preprint
  arXiv:2302.13971.

A     Models and Implementation                                   unanswerable questions which have α lower than
                                                                  a threshold. Next, we derive how Bayes’ theorem
A.1    Entropy
                                                                  can be applied to take into account the number of
The entropy of the output distribution is imple-                  answerable/unanswerable questions.
mented as follows,
                    P                                             B.1    SelfCheckGPT-QA with Bayes
         Hij = 2−       w̃∈W pij (w̃) log2 pij (w̃)   (13)        Let P (F) denote the probability of the i-th sentence
                                                                  being non-factual, and P (T) denote the probability
where W is the set of all possible words in the
                                                                  of the i-th sentence being factual. For a question q,
vocabulary.
                                                                  the probability of i-th sentence being non-factual
A.2    Proxy LLMs                                                 given a set of matched answers Lm and a set of
The proxy LLMs considered are LLaMA-{7B,                          not-matched answers Ln is:
13B, 30B} (Touvron et al., 2023), OPT-{125m,                          P (F|Lm , Ln )
1.3B, 13B, 30B} (Zhang et al., 2022), GPT-J-6B
                                                                                      P (Lm , Ln |F)P (F)
(Wang and Komatsuzaki, 2021) and GPT-NeoX-                              =
                                                                          P (Lm , Ln |F)P (F) + P (Lm , Ln |T)P (T)
20B (Black et al., 2022).
                                                                                   P (Lm , Ln |F)
                                                                        =                                          (16)
A.3    SelfCheckGPT’s Systems                                             P (Lm , Ln |F) + P (Lm , Ln |T)
Question Answering: The generation systems                        where we assume the sentence is equally likely to
G1 and G2 are T5-Large fine-tuned to SQuAD                        be False or True, i.e. P (F) = P (T). The probabil-
(Rajpurkar et al., 2016) and RACE (Lai et al.,                    ity of observing Lm , Ln when the sentence is False
2017), respectively. The answering system A is                    (non-factual):
Longformer (Beltagy et al., 2020) fine-tuned to the
RACE dataset. The answerability system U is also                        P (Lm , Ln |F)
Longformer, but fine-tuned to SQuAD2.0.                                     Y                   Y
                                                                        =        P (a = aR |F )   P (a′ ̸= aR |F )
                                                                            a∈Lm                    a′ ∈Ln
LLM for Prompting: We consider two LLMs,                                                Nm     Nn
GPT-3 (text-davinci-003) and ChatGPT (gpt-3.5-                          = (1 − β1 ) (β1 )                                   (17)
turbo) We note that during the data creation and                  and probability of observing Lm , Ln when the sen-
annotation, GPT-3 (text-davinci-003) was the state-               tence is True (factual):
of-the-art LLM available; hence, GPT-3 was used
as the main LLM generating WikiBio passages.                            P (Lm , Ln |T)
                                                                            Y                   Y
B     SelfCheckGPT with QA                                              =        P (a = ar |T )   P (a′ ̸= ar |T )
                                                                            a∈Lm                  a′ ∈Ln
Previous work showed that implementing question                                    Nm
                                                                         = (β2 ) (1 − β2 )      Nn
                                                                                                                            (18)
generation (in Equation 2) with two generators (G1
generates the question and associated answer, and                 where Nm and Nn are the number of matched an-
G2 generates distractors) yields higher-quality dis-              swers and the number of not-matched answers, re-
tractors (Manakul et al., 2023). Thus, a two-stage                spectively. Hence, we can simplify Equation 16:
generation is adopted in this work as follows:
                                                                                                             γ2Nn
                                                                                P (F|Lm , Ln ) =                            (19)
    q, a ∼ PG1 (q, a|ri ); o\a ∼ PG2 (o\a |q, a, R)                                                  γ1Nm + γ2Nn
                                                  (14)
                                                                                 β2             β1
where o = {a, o\a } = {o1 , ..., o4 }. In addition, to            where γ1 = 1−β    1
                                                                                      and γ2 = 1−β 2
                                                                                                     . Lastly, instead
filter out bad (unanswerable) questions, we define                of rejecting samples having an answerability score
an answerability score (Raina and Gales, 2022):                   below a threshold,7 we find empirically that soft-
                                                                  counting (defined below) improves the detection
          α = PU (answerable|q, context)              (15)        performance. We set both β1 and β2 to 0.8.
where the context is either the response R or sam-                       α is between 0.0 (unanswerable) and 1.0 (answerable).
                                                                  Standard-counting Nm and Nn can be considered as a special
pled passages S n , and α → 0.0 for unanswerable                  case of soft-counting where α is set to 1.0 if α is greater than
and α → 1.0 for answerable. We use α to filter out                the answerability threshold and otherwise α is 0.0.

                  X                              X
    Nm′ =                     αn ; Nn′ =                      αn (20)           n-gram
                                                                                                            Sent-lvl AUC-PR                   Passage-lvl
                                                                                                         NoFac NoFac*      Fact              Pear. Spear.
              n s.t. an ∈Lm                n s.t. an ∈Ln
                                                                                Avg(−logp)
where αn = PU (answerable|q, S n ). Therefore, the                              1-gram   81.52                      40.33      41.76         40.68          39.22
                                                                                2-gram   82.94                      44.38      52.81         58.84          58.11
SelfCheckGPT with QA score, SQA , is:                                           3-gram   83.56                      44.64      53.99         62.21          63.00
                                                  N′
                                                                                4-gram   83.80                      43.55      54.25         61.98          63.64
                                             γ2 n                               5-gram   83.45                      42.31      53.98         60.68          62.96
       SQA = P (F|Lm , Ln ) =              N′          N′
                                                                  (21)          Max(−logp)
                                         γ1 m + γ2 n                            1-gram   85.63                      41.04      58.47         64.71          64.91
                                                                                2-gram   85.26                      39.29      58.29         62.48          66.04
In Table 5, we show empically that applying Bayes’                              3-gram   84.97                      37.10      57.08         57.34          60.49
theorem and soft counting α (in Equation 20) im-                                4-gram   84.49                      36.37      55.96         55.77          57.25
                                                                                5-gram   84.12                      36.19      54.89         54.84          55.97
proves the performance of the SelfCheckGPT with
QA method.                                                                    Table 7: The performance using different n-gram models in
                                                                              the SelfCheckGPT with n-gram method.
                          Sentence-lvl              Passage-lvl
    Varaint
                       NoF NoF* Fact               PCC SCC
    SimpleCount       83.97      40.07   47.78     57.39       55.15
    + Bayes           83.04      38.58   47.41     56.43       55.03
    + Bayes + α       84.26      40.06   48.14     61.07       59.29
                                                                                              92.5
    Table 5: Performance of SelfCheckGPT-QA’s variants.                                       90.0

                                                                                              87.5

C     SelfCheckGPT with Prompt                                                     AUC-PR     85.0

                                                                                              82.5
We use the prompt template provided in the main                                                                                           SelfCk-BERTScore
                                                                                              80.0                                        SelfCk-QA
text (in Section 5.5) for both GPT-3 (text-davinci-                                                                                       SelfCk-Unigram
                                                                                              77.5                                        SelfCk-NLI
003) and ChatGPT (gpt-3.5-turbo). For ChatGPT,                                                                                            SelfCk-Prompt
a standard system message "You are a helpful                                                         0     2   4    6   8 10 12 14           16   18    20
                                                                                                                         Num. samples
assistant." is used in setting up the system.
   At the time of conducting experiments, the API                             Figure 8: The performance of SelfCheckGPT methods on
costs per 1,000 tokens are $0.020 for GPT-3 and                               sentence-level non-factual detection (AUC-PR) versus the
$0.002 for ChatGPT. The estimated costs for run-                              number of samples. This Figure extends the passage-level
                                                                              results in Figure 7.
ning the models to answer Yes/No on all 1908 sen-
tences and 20 samples are around $200 for GPT-3
and $20 for ChatGPT. Given the cost, we conduct
the experiments on 4 samples when performing
the ablation about LLM choice for SelfCheckGPT-                                                40
Prompt (Section 7.3). Table 6 shows the breakdown                                              30
of predictions made by GPT-3 and ChatGPT.

                                                                                   Spearman
                              ChatGPT                                                          10
                                           Yes         No
              GPT-3
                        Yes                3179        1038                                      0
                         No                367         3048                                                                               LLaMA
                                                                                                                                          OPT,GPT-J,NeoX
Table 6: Breakdown of predictions made by GPT-3/ChatGPT                                                                  B            B                B
                                                                                                  1.53m        6B
when prompted to answer Yes(supported)/No(not-supported).                                             B                 13        20                   30
                                                                                                                         Model Size

                                                                              Figure 9: Passage-level ranking performance of the Avg(H)
D     Additional Experimental Results                                         method using proxy LLM where the sizes are: LLaMA={7B,
                                                                              13B, 30B}, OPT={125m, 1.3B, 13B, 30B}, GPT-J=6B,
Here, we provide experimental results that are com-                           NeoX=20B. The full results are provided in Table 8.
plementary to those presented in the main paper.

                                                                                         0.8
                                                                                                                                                                                                                                             1.0
               0.12                                                                      0.7                                                                       8.0
                                                                                         0.6                                                                                                                                                 0.8
                                                                                                                                                                   7.5
               0.10
                                                                                         0.5

Method Score                                                              Method Score                                                              Method Score                                                              Method Score
                                                                                                                                                                   7.0                                                                       0.6
               0.08                                                                      0.4
                                                                                         0.3                                                                       6.5
               0.06                                                                                                                                                                                                                          0.4
                                                                                         0.2
                                                                                                                                                                   6.0
               0.04                                                                      0.1                                                                                                                                                 0.2
                                                                                                                                                                   5.5
                      0.0      0.2       0.4      0.6      0.8      1.0                        0.0      0.2       0.4      0.6      0.8      1.0                         0.0      0.2       0.4      0.6      0.8      1.0                         0.0      0.2       0.4      0.6      0.8      1.0
                            Human Score (0=Factual, +1=Non-Factual)                                  Human Score (0=Factual, +1=Non-Factual)                                   Human Score (0=Factual, +1=Non-Factual)                                   Human Score (0=Factual, +1=Non-Factual)

(a) SelfCheckGPT-BERTScore                                                                     (b) SelfCheckGPT-QA                                  (c) SelfCheckGPT-1gram(max)                                                                    (d) SelfCheckGPT-NLI

Figure 10: Scatter plot of passage-level scores where Y-axis = Method scores, X-axis = Human scores. Correlations are reported
in Table 2. This figure provides results in addition to Figure 6.

                                                                                                                   Sentence-level (AUC-PR)                                                        Passage-level (Corr.)
                                                                  LLM                          Size
                                                                                                                 NonFact NonFact* Factual                                                         Pearson Spearman
                                                            Random -          72.96                                                        29.72                                27.04                    -                              -
                                                            Avg(−logp) Method
                                                             LLaMA 30B        75.43                                                        30.32                                41.29              21.72                     20.20
                                                             LLaMA 13B        74.16                                                        30.01                                37.36              13.33                     12.89
                                                             LLaMA 7B         71.69                                                        27.87                                31.30               -2.71                     -2.59
                                                                OPT 30B       67.70                                                        24.43                                25.04              -32.07                    -31.45
                                                               NeoX 20B       69.00                                                        24.38                                26.18              -31.79                    -34.15
                                                                OPT 13B       67.46                                                        24.39                                25.20              -33.05                    -32.79
                                                             GPT-J 6B         67.51                                                        24.28                                24.26              -38.80                    -40.05
                                                                OPT 1.3B      66.19                                                        24.47                                23.47              -35.20                    -38.95
                                                                OPT 125m      66.63                                                        25.31                                23.07              -30.38                    -37.54
                                                            Avg(H) Method
                                                             LLaMA 30B        80.80                                                        39.01                                42.97              33.80                     39.49
                                                             LLaMA 13B        80.63                                                        38.98                                40.59              29.43                     33.12
                                                             LLaMA 7B         78.67                                                        37.22                                33.81              19.44                     21.79
                                                                OPT 30B       77.13                                                        33.67                                29.55               -0.43                     3.43
                                                               NeoX 20B       77.40                                                        32.78                                30.13               5.41                      7.43
                                                                OPT 13B       76.93                                                        33.71                                29.68               0.25                      1.39
                                                             GPT-J 6B         76.15                                                        33.29                                28.30               -2.50                     -1.37
                                                                OPT 1.3B      74.05                                                        31.91                                26.33              -10.59                    -10.00
                                                                OPT 125m      71.51                                                        30.88                                25.36              -14.16                    -13.76
                                                            Max(−logp) Method
                                                             LLaMA 30B        74.01                                                        27.14                                31.08              -22.83                    -22.71
                                                             LLaMA 13B        71.12                                                        26.78                                28.82              -34.93                    -31.70
                                                             LLaMA 7B         69.57                                                        25.91                                26.54              -42.57                    -38.24
                                                                OPT 30B       67.32                                                        24.40                                24.32              -49.51                    -45.50
                                                               NeoX 20B       67.51                                                        23.88                                24.82              -47.96                    -44.54
                                                                OPT 13B       67.36                                                        24.67                                24.46              -50.15                    -44.42
                                                             GPT-J 6B         67.58                                                        23.94                                23.93              -51.23                    -47.68
                                                                OPT 1.3B      68.16                                                        25.85                                24.66              -45.60                    -42.39
                                                                OPT 125m      69.23                                                        27.66                                24.14              -39.22                    -37.18
                                                            Max(H) Method
                                                             LLaMA 30B        80.92                                                        37.32                                37.90              35.57                     38.94
                                                             LLaMA 13B        80.98                                                        37.94                                36.01              32.07                     34.01
                                                             LLaMA 7B         79.65                                                        35.57                                31.32              22.10                     22.53
                                                                OPT 30B       76.58                                                        33.44                                29.31               1.63                      6.41
                                                               NeoX 20B       76.98                                                        31.96                                29.13               5.97                      9.31
                                                                OPT 13B       76.26                                                        32.81                                29.25               1.42                      2.82
                                                             GPT-J 6B         75.30                                                        32.51                                28.13               -2.14                     1.41
                                                                OPT 1.3B      73.79                                                        31.42                                26.38               -9.84                     -9.80
                                                                OPT 125m      71.32                                                        31.65                                25.36              -18.05                    -17.37

Table 8: AUC-PR for Detecting Non-Factual and Factual Sentences in the GPT-3 generated WikiBio passages. Passage-level
PCC and SCC with LLMs used to assess GPT-3 responses. This table is an extension to Table 2.


```
