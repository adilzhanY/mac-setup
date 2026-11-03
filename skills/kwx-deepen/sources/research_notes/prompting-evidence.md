# Prompting evidence for kwx-deepen

What the research and the model vendors' own guides say about the techniques the six steps borrow from. Every claim is tied to a source. Numbers were checked against the paper's abstract or HTML version in November 2026 unless marked "(from the paper, not rechecked)".

## 1. Persona and role prompting

**A role label alone does not make answers more accurate.**

- Zheng, Pei, Logeswaran, Lee, Jurgens. "When 'A Helpful Assistant' Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models". arXiv 2311.10054, v3 Oct 2024 (first title: "Is 'A Helpful Assistant' the Best Role for Large Language Models?"). https://arxiv.org/abs/2311.10054
  - Measured: 162 personas, 4 model families, 2,410 factual questions. Adding a persona to the system prompt "does not improve model performance" against a no persona control.
  - The best persona per question would help if you knew it in advance, but automatic selection was often no better than random.
  - Persona gender, type and domain do move accuracy around, which means the effect is noise, not a lever.
- Basil, Shapiro, Shapiro, Mollick, Mollick, Meincke. "Prompting Science Report 4: Playing Pretend: Expert Personas Don't Improve Factual Accuracy". Wharton GAIL, Dec 2025. arXiv 2512.05858. https://arxiv.org/abs/2512.05858
  - Measured: GPQA Diamond (198 questions) and an MMLU-Pro subset (300 questions), 6 models, many repeated runs per prompt.
  - For 5 of 6 models no expert persona gave a significant gain. There were 9 significant negative differences. Matching the expert's domain to the question did not help on GPQA.
  - Low knowledge personas ("Toddler", "Layperson") hurt. Domain mismatched experts made one model refuse questions.
  - The authors note personas may still shape tone, perspective and approach, which accuracy benchmarks do not measure.
- Kim, Yang, Jung. "Persona is a Double-edged Sword: Mitigating the Negative Impact of Role-playing Prompts in Zero-shot Reasoning Tasks". arXiv 2408.08631, 2024. https://arxiv.org/abs/2408.08631
  - Role prompts degraded reasoning on 7 of 12 datasets for Llama 3. LLM generated personas were more stable than handwritten ones. Their fix runs persona and neutral prompts side by side and picks one with an evaluator.
- Gupta, Shrivastava, Deshpande, Kalyan, Clark, Sabharwal, Khot. "Bias Runs Deep: Implicit Reasoning Biases in Persona-Assigned LLMs". ICLR 2024. arXiv 2311.04892. https://arxiv.org/abs/2311.04892
  - 24 reasoning datasets, 19 socio-demographic personas. For ChatGPT 3.5, 80% of personas showed bias, with drops of 70% or more on some datasets. GPT-4 Turbo still showed it in 42% of personas. Personas also caused refusals ("As a ... I can't answer this").

**Where role framing has helped, it carried content, not just a title.**

- Kong, Zhao, Chen, Li, Qin, Sun, Zhou, Wang, Dong. "Better Zero-Shot Reasoning with Role-Play Prompting". NAACL 2024. arXiv 2308.07702. https://arxiv.org/abs/2308.07702
  - ChatGPT, zero shot: AQuA 53.5% to 63.8%, Last Letter 23.8% to 84.2%. The method is a two stage "immersion" (a designed role setting prompt plus the model's own in-role reply), tested on older models.
- Xu, Yang, Lin, Wang, Zhou, Zhang, Mao. "ExpertPrompting: Instructing Large Language Models to be Distinguished Experts". arXiv 2305.14688, 2023. https://arxiv.org/abs/2305.14688
  - Generates a detailed, task specific description of the expert (what they know, how they work) for each instruction. GPT-4 judged answers better than vanilla ones. Note the judge is an LLM, and the result is about answer quality, not factual accuracy.
- Suzgun, Kalai. "Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding". arXiv 2401.12954, 2024. https://arxiv.org/abs/2401.12954
  - A conductor model splits the task and gives each "expert" instance tailored instructions, with a Python interpreter available. Averaged over Game of 24, Checkmate-in-One and Python puzzles (GPT-4): +17.1% over standard prompting, +17.3% over expert (dynamic) prompting, +15.2% over multipersona prompting. The gain over "expert prompting" shows the expert label is not what does the work. Decomposition, instructions and the tool do.
- Anthropic, "Prompting best practices" (Give Claude a role). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - A role "focuses Claude's behavior and tone for your use case". Anthropic frames it as focus and tone, and the same page says the bigger lever is being explicit: "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows."
- Salewski, Alaniz, Rio-Torto, Schulz, Akata. "In-Context Impersonation Reveals Large Language Models' Strengths and Biases". NeurIPS 2023. arXiv 2305.14930. https://arxiv.org/abs/2305.14930
  - Impersonating domain experts helped on some tasks, but impersonation also reproduced social biases (from the paper, not rechecked).

**Reading:** the label is noise or harm. What can help is the content an expert brings: what they check, what they start from, what they refuse to do. The skill should use "who is the expert" only as a lens to produce that content, and never put "act as a world class X" in the rewritten task.

## 2. Query and prompt rewriting

- Zheng, Mishra, Chen, Cheng, Chi, Le, Zhou. "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models". ICLR 2024. arXiv 2310.06117. https://arxiv.org/abs/2310.06117
  - First ask for the underlying principle or concept, then answer using it. PaLM-2L: MMLU Physics +7%, Chemistry +11%, TimeQA +27%, MuSiQue +7%. The TimeQA gain came with retrieval on the step back question, so part of the benefit is "fetch the right general material first".
- Deng, Zhang, Chen, Gu. "Rephrase and Respond: Let Large Language Models Ask Better Questions for Themselves". arXiv 2311.04205, 2023. https://arxiv.org/abs/2311.04205
  - The model rephrases and expands the question, then answers. Improves many tasks and stacks with chain of thought. A two step version lets a stronger model rephrase for a weaker one. Supports the skill rewriting the task before doing it.
- Press, Zhang, Min, Schmidt, Smith, Lewis. "Measuring and Narrowing the Compositionality Gap in Language Models". Findings of EMNLP 2023. arXiv 2210.03350. https://arxiv.org/abs/2210.03350
  - Models often answer every sub question right and still fail the combined question, and the gap does not shrink with scale. Self-ask (explicit follow up questions) narrows it, and answering the follow ups with a search engine narrows it further. Supports naming sub questions and grounding each one.
- Zhou, Schärli, Hou, Wei, Scales, Wang, Schuurmans, Cui, Bousquet, Le, Chi. "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models". ICLR 2023. arXiv 2205.10625. https://arxiv.org/abs/2205.10625
  - Decompose, then solve sub problems in order. SCAN length split: 99.7% versus 16.2% for chain of thought (from the paper, not rechecked).
- Wang, Xu, Lan, Hu, Lan, Lee, Lim. "Plan-and-Solve Prompting". ACL 2023. arXiv 2305.04091. https://arxiv.org/abs/2305.04091
  - "Devise a plan, then carry it out" beat zero shot chain of thought on math and commonsense sets and approached few shot CoT (from the paper, not rechecked).
- OpenAI, "GPT-4.1 Prompting Guide". https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
  - Three agentic reminders (persistence, tool calling, planning) raised internal SWE-bench Verified "by close to 20%". "Inducing explicit planning increased the pass rate by 4%." The model follows instructions "more closely and more literally than its predecessors".
- Zhou, Muresanu, Han, Paster, Pitis, Chan, Ba. "Large Language Models Are Human-Level Prompt Engineers" (APE). ICLR 2023. arXiv 2211.01910. https://arxiv.org/abs/2211.01910
  - Model generated instructions matched or beat human written ones on 19 of 24 instruction induction tasks. Needs a scored set of examples to search against.
- Yang, Wang, Lu, Liu, Le, Zhou, Chen. "Large Language Models as Optimizers" (OPRO). ICLR 2024. arXiv 2309.03409. https://arxiv.org/abs/2309.03409
  - Optimized prompts beat human designed ones by up to 8% on GSM8K and up to 50% on Big-Bench Hard tasks. Again needs a scorer.
- Sclar, Choi, Tsvetkov, Suhr. "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design". ICLR 2024. arXiv 2310.11324. https://arxiv.org/abs/2310.11324
  - Formatting changes alone moved LLaMA-2-13B accuracy by up to 76 points. Exact wording effects are fragile and model specific, so claims about magic phrases should be tested, not trusted.
- OpenAI, "Reasoning best practices". https://developers.openai.com/api/docs/guides/reasoning-best-practices
  - For reasoning models: "Keep prompts simple and direct", "Avoid chain-of-thought prompts" (they reason internally), "Be very specific about your end goal".
- Anthropic, "Best practices for Claude Code". https://code.claude.com/docs/en/best-practices
  - "think step by step" or "be thorough" are "ordinary prompt text rather than keywords"; effort level, not wording, controls how hard the model thinks. A specific prompt helps because "it gives Claude information it doesn't already have": name the file, the symptom, and what "fixed" looks like.

**Reading:** rewriting helps when it adds information (principles, sub questions, end goal, inputs, the check) and decomposes. Rewriting that only adds "think harder" or style wording does little on current reasoning models. APE and OPRO show prompt changes should be judged by a scorer, which matches the skill's own evals folder.

## 3. Verification

**Self checking without an outside signal does not work reliably.**

- Huang, Chen, Mishra, Zheng, Yu, Song, Zhou. "Large Language Models Cannot Self-Correct Reasoning Yet". ICLR 2024. arXiv 2310.01798. https://arxiv.org/abs/2310.01798
  - GPT-3.5, intrinsic self-correction (no external feedback): GSM8K 75.9 to 75.1 to 74.7 over two rounds, CommonSenseQA 75.8 to 38.1 to 41.8, HotpotQA 26.0 to 25.0 to 25.0. The model talked itself out of right answers.
  - Earlier reported gains used ground truth labels to decide when to stop. Without the oracle, gains vanish.
  - Multi agent debate did not beat self-consistency at an equal number of samples (GSM8K 83.2 vs 85.3 with 6 responses, 83.0 vs 88.2 with 9). The gain was from sampling agreement, not from critique.
- Kamoi, Zhang, Zhang, Han, Zhang. "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs". TACL 2024. arXiv 2406.01297. https://arxiv.org/abs/2406.01297
  - Self-correction works with reliable external feedback, with large scale fine tuning, or on unusually suitable tasks. No prior work showed success with feedback from a prompted LLM alone outside those cases. Many positive studies used unfair setups.
- Madaan et al. "Self-Refine: Iterative Refinement with Self-Feedback". NeurIPS 2023. arXiv 2303.17651. https://arxiv.org/abs/2303.17651
  - About 20% absolute average gain over 7 tasks, mostly on open ended quality (dialogue, code readability, sentiment rewriting) judged by preference. It is the case Kamoi calls "suitable": tasks where quality is easy to see. Weak on math reasoning (from the paper, not rechecked).
- Panickssery, Bowman, Feng. "LLM Evaluators Recognize and Favor Their Own Generations". arXiv 2404.13076, 2024. https://arxiv.org/abs/2404.13076
  - Models rate their own outputs higher than equally good outputs from others, and the bias grows with how well they recognise their own text. So "I checked and it looks right" from the same model is weak evidence.
- Zheng et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena". NeurIPS 2023. arXiv 2306.05685. https://arxiv.org/abs/2306.05685
  - LLM judges show position bias, verbosity bias and self enhancement bias (from the paper, not rechecked).
- Sharma, Tong, Korbak et al. "Towards Understanding Sycophancy in Language Models". ICLR 2024. arXiv 2310.13548. https://arxiv.org/abs/2310.13548
  - Five assistants consistently tilted answers toward the user's stated views. Humans and preference models sometimes preferred convincing sycophantic answers over correct ones. So the user's approval is not independent evidence either. This backs the original prompt's "other than you or me".

**What does work: independent checks.**

- Dhuliawala, Komeili, Xu, Raileanu, Li, Celikyilmaz, Weston. "Chain-of-Verification Reduces Hallucination in Large Language Models". arXiv 2309.11495, 2023. https://arxiv.org/abs/2309.11495
  - Draft, plan verification questions, answer them independently, revise. Llama 65B: Wikidata list precision 0.17 to 0.36 (two step), MultiSpanQA F1 0.39 to 0.48, biography FActScore 55.9 to 71.4 (factor plus revise).
  - "Factored" (each check answered without the draft in context) beat "joint" on every task (biographies 60.8 vs 63.7). Single facts asked alone were right about 70% of the time against 17% inside the long answer. Independence of the check is the active ingredient.
- Wang, Wei, Schuurmans, Le, Chi, Narang, Chowdhery, Zhou. "Self-Consistency Improves Chain of Thought Reasoning in Language Models". ICLR 2023. arXiv 2203.11171. https://arxiv.org/abs/2203.11171
  - Sample several reasoning paths, take the majority. GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2% (from the paper, not rechecked). A cheap signal when nothing external exists, but agreement is not truth.
- Gou, Shao, Gong, Shen, Yang, Duan, Chen. "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing". ICLR 2024. arXiv 2305.11738. https://arxiv.org/abs/2305.11738
  - Critique using search, a code interpreter or a calculator improves QA, math and toxicity. The paper reports that critique without the tools gives small or negative gains (from the paper, not rechecked).
- Chen, Lin, Schärli, Zhou. "Teaching Large Language Models to Self-Debug". ICLR 2024. arXiv 2304.05128. https://arxiv.org/abs/2304.05128
  - Code repair driven by execution results and unit tests improves code generation (up to about 12% in the paper, not rechecked).
- Sprague, Yin, Rodriguez, Jiang, Wadhwa, Singhal, Zhao, Ye, Mahowald, Durrett. "To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning". ICLR 2025. arXiv 2409.12183. https://arxiv.org/abs/2409.12183
  - Meta analysis of 100+ papers plus 20 datasets and 14 models: CoT helps mostly on math and logic, almost nothing elsewhere. Even there, a symbolic solver or tool beats CoT.
- Anthropic, "Best practices for Claude Code" (Give Claude a check to run). https://code.claude.com/docs/en/best-practices
  - "Claude stops when the work looks done." Give it "something it can run that comes back pass or fail": a test file, a build exit code, a linter, a diff against a fixture, a screenshot next to the mockup. Ask for "evidence: the command it ran and its output". And a warning: "A reviewer that's asked to find problems will always find something. If you fix every finding, you end up with extra abstraction layers and tests for cases that can't happen."
- Anthropic, "Building effective agents" (Schluntz, Zhang, Dec 2024). https://www.anthropic.com/engineering/building-effective-agents
  - Agents must "gain 'ground truth' from the environment at each step". The evaluator optimizer loop "is particularly effective when we have clear evaluation criteria".
- Anthropic, "Prompting Claude Opus 5" (Task scope and over-verification; Self-correction). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
  - The model already verifies its own work. Instructions like "include a final verification step" or "double-check your answer" cause over-verification and "add cost without improving results".

**Reading:** step 5 is the best supported step, provided the evidence is external to the model and to the person asking. A generic "review it again" step is not.

## 4. Clarifying questions

- Vijayvargiya, Zhou, Yerukola, Sap, Neubig. "Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering". ICLR 2026. arXiv 2502.13069. https://arxiv.org/abs/2502.13069
  - On underspecified SWE-bench issues, letting the agent ask raised resolve rates by up to 74% over not asking. Sonnet 4 recovered 89% of its fully specified score.
  - "Without explicit prompting, models almost never interact, even for severely underspecified inputs." Detecting underspecification was unreliable for most models (0.47 to 0.89 accuracy depending on model and prompt): "prompt engineering alone proves insufficient".
  - "The most effective questions are specific, actionable, and task-level"; "vague prompts or implementation details recoverable from the codebase add little value". Interaction also cost steps (65 to 75 for Sonnet 4).
- Zhang, Choi. "Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs". arXiv 2311.09469, 2023. https://arxiv.org/abs/2311.09469
  - Split into: when to ask, what to ask, how to use the answer. Choosing which 10% of cases to clarify by uncertainty over user intents doubled the gain compared with choosing at random. Asking is valuable when targeted, not as a habit.
- Zhang, Qin, Deng et al. "CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models". ACL 2024. arXiv 2405.12063. https://arxiv.org/abs/2405.12063
  - About 12K examples. LLMs are weak at spotting ambiguity and at writing good clarifying questions. CoT and few shot gave "only marginal enhancements" and can add overconfidence.
- Min, Michael, Hajishirzi, Zettlemoyer. "AmbigQA: Answering Ambiguous Open-domain Questions". EMNLP 2020. arXiv 2004.10645. https://arxiv.org/abs/2004.10645
  - Over half of sampled NQ-open questions were ambiguous (from the paper, not rechecked). Ambiguity is common, not rare.
- Anthropic, "Prompting Claude Opus 5". https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
  - "Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work."
- OpenAI, "GPT-5 prompting guide". https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
  - In agentic mode: "Bias towards not asking the user for help if you can find the answer yourself." The more eager template says "Do not ask the human to confirm or clarify assumptions, as you can always adjust later."
- Anthropic, "Best practices for Claude Code". https://code.claude.com/docs/en/best-practices
  - When the person does not know what they want yet: "Interview me until you could write the spec", with multiple choice questions about the parts not pinned down.

**Reading:** asking helps a lot when the request is truly underspecified and the question is about the task itself. Models do not ask on their own and are poor at telling when to. So the skill needs an explicit, concrete test (two readings that lead to different deliverables) rather than "ask if unclear". Anything the agent can look up must be looked up, not asked.

## 5. Scope: keeping "deeper" from becoming "bigger"

- Anthropic, "Prompting best practices" (Overeagerness). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - Opus 4.5 and 4.6 "overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested." Sample fix: "Only make changes that are directly requested or clearly necessary... The right amount of complexity is the minimum needed for the current task."
  - Also: the newer models are more responsive to the system prompt, so aggressive wording ("CRITICAL: You MUST") now overtriggers. Old "be thorough" prompts should be toned down.
- Anthropic, "Prompting Claude Opus 5" (Task scope; Written deliverable length; Response length). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
  - The model "can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be." Sample fix: "Deliver what was asked, at the scope intended... If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it."
  - Written documents run long: "cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate." Lower effort does not reliably shorten visible output, length must be asked for.
- Anthropic, "Best practices for Claude Code". https://code.claude.com/docs/en/best-practices
  - The opposite default also exists: Claude "tends to read a request conservatively and build the smallest thing that satisfies it"; "be ambitious" tells it scope "which only you know". Scope is the person's call, so the skill must not silently decide it.
- Dubois, Galambosi, Liang, Hashimoto. "Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators". COLM 2024. arXiv 2404.04475. https://arxiv.org/abs/2404.04475
  - LLM judges favour longer outputs. Removing length raised correlation with Chatbot Arena from 0.94 to 0.98.
- Singhal, Goyal, Xu, Durrett. "A Long Way to Go: Investigating Length Correlations in RLHF". arXiv 2310.03716, 2023. https://arxiv.org/abs/2310.03716
  - Much of the measured RLHF improvement came from longer outputs (from the paper, not rechecked). Training pressure pushes toward length, so "more" will feel like "better" to the model unless the size is fixed.
- Saito, Wachi, Wataoka, Akimoto. "Verbosity Bias in Preference Labeling by Large Language Models". arXiv 2310.10076, 2023. https://arxiv.org/abs/2310.10076
  - LLM labelers prefer longer answers more than humans do (from the paper, not rechecked).
- OpenAI, "GPT-5 prompting guide". https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
  - Contradictory or vague instructions are "more damaging to GPT-5 than to other models" because it spends reasoning tokens reconciling them. A rewritten task with conflicting asks costs real quality.

**Reading:** models already drift toward bigger (more features, more files, longer documents) and judges reward length. A skill that says "what would the expert add" will feed that drift unless each addition is forced to change the method, the inputs or the check, and the deliverable size is written down.

## 6. Cost: when pre steps are not worth it

- Chen, Xu, Liang et al. "Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs". arXiv 2412.21187, 2024. https://arxiv.org/abs/2412.21187
  - o1 like models used 1,953% more tokens than conventional models for the same answers on easy problems. QwQ produced 13 solutions to "2 plus 3" (901 tokens, first solution correct at 39 tokens). The first solution was already right in more than 92% of cases.
- Liu, Geng, Wu, Sucholutsky, Lombrozo, Griffiths. "Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse". arXiv 2410.21333, 2024. https://arxiv.org/abs/2410.21333
  - On 3 of 6 tasks where deliberation hurts humans, CoT hurt models too, up to 36.3% absolute for o1-preview versus GPT-4o. Extra deliberation is not free even in accuracy.
- Sprague et al. 2024 (above): CoT can be applied selectively with no loss outside math and logic.
- Mallen, Asai, Zhong, Das, Khashabi, Hajishirzi. "When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories". ACL 2023. arXiv 2212.10511. https://arxiv.org/abs/2212.10511
  - Adaptive retrieval (retrieve only for less popular facts) improved accuracy and cut inference cost. The model to copy: decide per item whether the extra step is needed.
- Anthropic, "Prompting best practices" (Overthinking; adaptive thinking). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - Current Claude models decide how much to think by query complexity, and "On easier queries that don't require thinking, the model responds directly." Sample prompt: "Thinking adds latency and should only be used when it will meaningfully improve answer quality". Also: replace blanket defaults ("If in doubt, use [tool]") with conditions.
- Anthropic, "Prompting Claude Opus 5" (Controlling subagent spawning). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
  - "Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work."
- OpenAI, "GPT-5 prompting guide": "Many workflows can be accomplished with consistent results at medium or even low reasoning_effort"; tool call budgets and early stop criteria ("Top hits converge (~70%) on one area/path") for bounded context gathering.

**Reading:** a fixed six step ritual on every request is the overthinking pattern. The skill should run only where a gap between the asked task and the expert's task plausibly changes the result, and should scale its own length to the task.

## 7. Grounding in primary sources

- Walters, Wilder. "Fabrication and errors in the bibliographic citations generated by ChatGPT". Scientific Reports 13, 14045 (2023). https://www.nature.com/articles/s41598-023-41032-5
  - 636 citations in 84 short literature reviews. Fabricated: about 55% (GPT-3.5) and 18% (GPT-4). Of the real ones, 43% and 24% had substantive errors.
- Mallen et al. 2023 (above): models "struggle with less popular factual knowledge", scaling does not fix the long tail, and retrieval augmented small models beat much larger unaided ones there. Unaided models stay competitive only on very popular facts.
- Liu, Zhang, Liang. "Evaluating Verifiability in Generative Search Engines". Findings of EMNLP 2023. arXiv 2304.09848. https://arxiv.org/abs/2304.09848
  - Even with retrieval, only about 51.5% of generated sentences were fully supported by their citations, and about 74.5% of citations supported their sentence. Fetching is necessary but the claim to source link must still be checked.
- Magesh, Surani, Dahl, Suzgun, Manning, Ho. "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools". Journal of Empirical Legal Studies 2025. arXiv 2405.20362. https://arxiv.org/abs/2405.20362
  - Commercial legal RAG tools (Lexis+ AI, Westlaw) hallucinated 17% to 33% of the time, less than GPT-4 alone but far from zero.
- Lewis, Perez, Piktus et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". NeurIPS 2020. arXiv 2005.11401. https://arxiv.org/abs/2005.11401
  - Retrieval plus generation beat parametric only models on open domain QA and produced more specific, factual text (from the paper, not rechecked).
- Shuster, Poff, Chen, Kiela, Weston. "Retrieval Augmentation Reduces Hallucination in Conversation". Findings of EMNLP 2021. arXiv 2104.07567. https://arxiv.org/abs/2104.07567
  - Retrieval substantially cut hallucinated knowledge in dialogue (from the paper, not rechecked).
- Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni, Liang. "Lost in the Middle: How Language Models Use Long Contexts". TACL 2024. arXiv 2307.03172. https://arxiv.org/abs/2307.03172
  - Use of retrieved material drops when the relevant passage sits in the middle of a long context (from the paper, not rechecked). Fetch the specific part, not everything.
- Anthropic, "Reduce hallucinations". https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
  - Allow "I don't know". For long documents, "extract word-for-word quotes first". After drafting, find a supporting quote for each claim, "If it can't find a quote, it must retract the claim."
- Anthropic, "Prompting best practices" (Minimizing hallucinations in agentic coding): "Never speculate about code you have not opened... read the file before answering."

**Reading:** step 3 ("fetch the raw material") is strongly supported, and the evidence sharpens it: fetch rather than recall, quote with location, check every citation resolves, and fetch selectively (long tail, recent, load bearing claims), not everything.

## Implications for the skill

### Step by step verdict

1. **Name the expert. Keep, but change what it produces.** A title alone does not raise accuracy and can lower it (Zheng 2024, Basil 2025, Kim 2024, Gupta 2023). Matching the expert to the domain does not help by itself (Basil 2025). What helped in positive studies was content: a detailed description of how the expert works (ExpertPrompting), decomposition with tailored instructions and a tool (Meta-Prompting beat "expert prompting" by 17.3%).
   - Rule: name the expert narrowly (the role and the setting, for example "a clinical trial statistician reviewing a phase 2 readout", not "an expert"), and immediately turn the name into 3 to 6 concrete moves, checks and refusals. The name is scaffolding for steps 2 to 5.
   - Rule: never write "act as", "you are a world class" or any persona line into the rewritten task. Write the moves.
   - Rule: never use demographic or low knowledge personas.
2. **What the expert would do that was not asked. Keep, with a filter.** Step back and RaR support adding the principle and the missing sub questions (Zheng 2023, Deng 2023, Press 2022). But models already over-expand scope (Anthropic overeagerness, Opus 5 scope guidance), and a critic asked to find gaps always finds some (Claude Code best practices).
   - Rule: an item counts as "deeper" only if it changes how the deliverable is made or checked (a better input, a method, a control, a check, a known failure mode). An item that adds a section, a feature, a file or an option is "bigger" and goes to the not doing list.
   - Rule: cap at 3 to 5 items, ranked by how much each could change the answer. Drop the rest silently.
3. **Name and fetch the raw material. Keep, strongest after step 5.** Citation fabrication (55% and 18%, Walters and Wilder 2023), long tail failure (Mallen 2023), and vendor guidance ("Never speculate about code you have not opened") all point the same way. Retrieval is not a cure (Liu 2023: 51.5% fully supported; Magesh 2024: 17% to 33%).
   - Rule: fetch, do not recall, for anything load bearing: numbers, quotes, citations, APIs, versions, laws, file contents. Record where each came from (URL, file and line, table and row).
   - Rule: quote the source verbatim before reasoning over it, and drop any claim that has no supporting quote.
   - Rule: fetch selectively. Popular, stable facts can come from memory. Long tail, recent, contested or load bearing facts must be fetched.
   - Rule: prefer the primary source (dataset, spec, statute, source code, original paper) over a summary of it, but say when the primary source could not be reached.
4. **Name methods and tools. Keep, and prefer executable ones.** CoT helps mostly on math and logic, and tools beat CoT even there (Sprague 2024). Tool backed critique works where prompt only critique does not (CRITIC, Self-Debug, Kamoi 2024).
   - Rule: each method must be something you can run or do (a command, a test, a statistical test, a named procedure, a search query), not "analyse carefully" or "think step by step".
   - Rule: do not add reasoning phrases. On current models effort, not wording, controls thinking (Claude Code best practices, OpenAI reasoning best practices).
5. **Independent evidence. Keep, this is the core of "deeper".** Intrinsic self-correction fails or hurts (Huang 2024: CommonSenseQA 75.8 to 38.1). Models favour their own outputs (Panickssery 2024). Users and preference models reward agreement (Sharma 2023), which justifies "other than you or me". Independent checks work: factored verification beat joint (CoVe), tool feedback works (CRITIC, Self-Debug), and "give Claude a check to run" is Anthropic's top lever for agents.
   - Rule: the check must come from outside the model and the requester: a test, a tool output, a primary source, a measurement, a known correct case, a second method that does not share the first one's inputs.
   - Rule: define the check before doing the work, make it pass or fail where possible, and report the evidence (command and output, quote and location), not "verified".
   - Rule: when verifying facts, ask each check question without the draft in view (CoVe factored).
   - Rule: if no external check exists, say so, and use sampling agreement only as a weak signal (self-consistency), never as proof.
   - Rule: do not add generic "double-check" or "re-verify" steps. Current models already self check, and these add cost without gain (Opus 5 guidance).
6. **Rewrite with the same deliverable size and a not doing list. Keep, and make size explicit.** Models drift longer and broader, and judges reward length (Dubois 2024, Singhal 2023, Saito 2023, Opus 5 guidance). Vague or contradictory rewrites cost quality (GPT-5 guide). Newer models follow instructions literally (GPT-4.1 guide), so what is written is what gets done.
   - Rule: the rewrite states, in this order: deliverable and its size (same as asked, in words, pages, files or items), inputs to fetch, methods, the check, the not doing list.
   - Rule: the not doing list holds every tempting addition from step 2 that failed the deeper test, in one line each.
   - Rule: no contradictions and no shouting ("CRITICAL", "MUST"). Newer models overtrigger on it (Anthropic best practices).
   - Rule: if the deeper version changes what is delivered (not only how), say so in one sentence and let the person choose, instead of quietly transforming the task (Opus 5 scope guidance).

### Rules the six steps do not cover yet

- **Trigger gate (new step 0).** Skip the method for trivial work: lookups, one line edits, formatting, casual conversation, or anything where the first answer is almost always right (overthinking: 92% first round correct; adaptive retrieval and adaptive thinking both decide per case). Run it when at least one holds: the result will be relied on, there is a known gap between what amateurs and experts do in the field, it depends on facts the model may misremember, or an external check exists that the request did not mention.
- **Scale the pre steps to the task.** For a small task, one line per step. The analysis should be much shorter than the deliverable.
- **Clarifying question gate.** Ask only when two readings of the request lead to materially different deliverables, and the answer cannot be found with tools (Anthropic Opus 5, GPT-5 guide, Ambig-SWE). Ask specific, task level questions, at most two or three, multiple choice where possible. Do not rely on "ask if unclear": models rarely ask unprompted and detect ambiguity poorly (Ambig-SWE, CLAMBER), so apply the two readings test explicitly. Otherwise state the assumption in the rewrite and proceed.
- **Measure the skill itself.** Prompt effects are fragile (Sclar 2023: up to 76 points from formatting), and APE and OPRO only work against a scorer. The evals folder should compare the skill against the plain request on tasks with an external answer key, and should score length separately so a longer output is not counted as a deeper one (Dubois 2024).
- **Do not stack with the harness.** If the agent harness already plans, verifies or delegates, the skill should not add another layer of the same (Opus 5 guidance on over-verification and subagent overuse).
