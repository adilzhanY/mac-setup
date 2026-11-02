# Empirical studies of LLM generated tests and the test oracle problem

Evidence strength key used below: [Strong] = peer reviewed or industrial deployment with stated numbers, read from the primary source. [Moderate] = primary arXiv preprint with numbers, or a peer reviewed paper where only the abstract was read. [Weak] = secondary coverage, self reported leaderboard entry, or qualitative claim only. Newest evidence first inside each list where dates differ.

## Meta TestGen-LLM (2024), ACH (2025) and JiTTest (2026): method, acceptance rates, filters and why

### Takeaway
Meta's three generations of LLM test generation all wrap the LLM in hard, automatic filters and treat the LLM as a noisy proposer. TestGen-LLM (2024) only keeps tests that build, pass 5 out of 5 runs and add line coverage, which makes them regression ("hardening") tests that by construction assert current behaviour; ACH (2025) steers generation with targeted mutants so each kept test must kill a plausible fault; JiTTest (2026) generates "catching" tests per code change that are meant to fail, and needs rule based plus LLM assessors because most raw failures are false alarms (only 8 of 41 reported candidates were real bugs).

### Cited Findings
- JiTTest, "Just-in-Time Catching Test Generation at Meta" (Becker, Harman et al., arXiv 2601.22832, Jan 2026): catching tests are generated per diff and are meant to FAIL to surface a bug before the code lands, unlike hardening tests that pass when generated. 22,126 generated tests analysed. Code change aware methods produced 4x more candidate catches than hardening tests and 20x more than coincidentally failing tests. Rule based and LLM based assessors cut human review load by 70%. 41 candidate catches were reported to engineers, 8 were confirmed true positives (about 20%), and 4 of those would have caused serious failures. [Moderate, abstract read] [arXiv 2601.22832](https://arxiv.org/abs/2601.22832)
- Meta's blog describes the JiTTest pipeline as: infer the intent of the change, create mutants ("dodgy" variants of the code), generate and run tests against them, then filter with ensembles of rule based and LLM based assessors before anything reaches the pull request. [Moderate] [Meta Engineering, 11 Feb 2026](https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/); [InfoQ, 17 Apr 2026](https://www.infoq.com/news/2026/04/meta-jit-testing-ai-detection)
- A secondary blog claims a 15% mutant kill rate for JiTTest vs 2.4% for TestGen-LLM. I could not find this in a primary source. [Weak, unconfirmed] [DEV Community](https://dev.to/ayyazzafar/metas-jittests-how-ai-writes-22000-tests-finds-4x-more-bugs-then-deletes-them-all-2kpf)
- The conceptual frame is Harman, O'Hearn and Sengupta, "Harden and Catch for Just-in-Time Assured LLM-Based Software Testing" (FSE 2025 keynote paper): "hardening" tests pass today and protect against future regressions, "catching" tests find bugs in the change under review; the catching case runs straight into the test oracle problem because a failing generated test may be wrong rather than the code. [Moderate] [arXiv 2504.16472](https://arxiv.org/html/2504.16472v2)
- ACH, "Mutation-Guided LLM-based Test Generation at Meta" (arXiv 2501.12862, FSE 2025 industry): generates relatively few mutants, aimed at currently undetected faults tied to one concern (privacy), then generates tests that kill them. 10,795 Android Kotlin classes across 7 platforms, 9,095 mutants, 571 privacy hardening tests. Engineers accepted 73% of tests in Messenger and WhatsApp test-a-thons; 36% were judged privacy relevant. An LLM agent detects equivalent mutants with precision 0.79 and recall 0.47, rising to 0.95 and 0.96 with simple preprocessing. [Strong] [arXiv 2501.12862](https://arxiv.org/abs/2501.12862)
- ACH trial ran October to December 2024 on Facebook, Instagram, WhatsApp and wearables; Meta lists the Test Oracle Problem as open work. [Moderate] [InfoQ, Jan 2026](https://www.infoq.com/news/2026/01/meta-llm-mutation-testing); [Meta Engineering, Feb 2025](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/); [Meta Engineering, Sept 2025](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)
- TestGen-LLM (Alshahwan et al., FSE 2024 industry, arXiv 2402.09171). Filters, in order, with stated reasons: (1) builds, else discarded; (2) passes on first run, because with no automatable oracle a failure could be a real bug or a wrong assertion, so only regression tests are kept; (3) passes all 5 repeated runs, since flakiness is "one of the most significant problems in industrial testing"; (4) increases line coverage, to avoid duplicates and give a measurable claim. The filters are the stated defence against hallucination. [Strong] [arXiv 2402.09171 HTML](https://arxiv.org/html/2402.09171)
- TestGen-LLM funnel on 86 Instagram Reels and Stories classes: 75% had a test that builds, 57% one that builds and passes reliably, 25% one that also raises coverage. Test-a-thons: 196 of 1,979 classes improved (about 10%; abstract says 11.5%), engineers accepted 73% of recommendations. Nov 2023 Instagram: 17 diffs, 16 landed. Dec 2023 Facebook: 280 diffs, 144 accepted, 64 rejected or abandoned, 61 unreviewed. Rejections cited missing assertions; tests with a TODO in place of an assertion were not landed. [Strong] [arXiv 2402.09171](https://arxiv.org/abs/2402.09171); [HTML](https://arxiv.org/html/2402.09171)

### Inferences
- The "73% accepted" figure recurs for both TestGen-LLM and ACH but measures acceptance of already filtered output, not raw LLM quality. Raw yield is much lower (25% of classes got a coverage raising test).
- The pass filter in TestGen-LLM means every kept test encodes whatever the code did at generation time. That is fine for regression hardening but it cannot find existing bugs, which is why Meta moved to mutants (ACH) and change aware catching (JiTTest).
- JiTTest shows the cost of trying to catch bugs: even after filtering, about 80% of reported catches were false positives. Any system that lets failing LLM tests through needs a strong triage layer.

### Gaps
- Meta has not published per-filter rejection reasons for ACH or the JiTTest assessor precision and recall in sources I could read.
- No primary source found for JiTTest mutant kill rates.

## Coverage vs fault detection: tool and benchmark numbers

### Takeaway
LLM tools reach high coverage on modules and functions (CoverUp 80% median, TestPilot 70% statements), but on realistic whole-file or repo tasks coverage and especially mutation score stay low (TestGenEval: GPT-4o 35.2% coverage, 18.8% mutation score), and several studies show coverage is a weak proxy for bug finding. Agentic issue reproduction (SWT-bench) has climbed from under 20% in 2024 to over 80% on the Verified split in late 2025 and 2026.

### Cited Findings
- SWT-bench (Mündler et al., NeurIPS 2024): tasks from real GitHub issues; a test succeeds if it fails on the original code and passes after the fix (fail to pass), and no generated test fails on the fixed code. Leaderboard (fetched Oct 2026): Verified split top entries DPIAgent (GPT-5, with test selection) 87.5%, TEX-T (Claude 4 Sonnet) 87.0%, LogicStar L*Agent v1 84.0%, PatchTwin+Guard (GPT-5) 82.9%, OpenHands (GPT-5) 79.8%, DPIAgent (Claude Opus 4.5) 78.8%. Lite split: DevstralTestGen 89.1% (stand alone reproduction scripts), ReProAgent (GPT-5-mini) 56.2%, e-Otter++ 52.5%, Amazon Q Developer Agent 39.9%, AssertFlip (GPT-4o) 38.0%, while May 2024 baselines were SWE-Agent+ (GPT-4) 18.5%. Mean coverage delta of the patched code is 57% to 79% for top entries. [Moderate, self submitted leaderboard; site footer date inconsistent with entry dates and ordering not strictly by score] [swtbench.com](https://swtbench.com/)
- A single self reported SWT-bench score of 69.3% for MiniMax M2.1 appears on a third party tracker. [Weak] [llm-stats](https://llm-stats.com/benchmarks/swt-bench)
- LLM vs human tests on real Python bugs (Vathana et al., arXiv 2606.08588, June 2026): Gemini 2.5 Flash with lexical retrieval of bug relevant context detected faults in 69% of cases vs 17.2% for general purpose human tests (Fisher p < 0.001, Cohen's h = 1.10), while coverage was nearly identical (line 84.8% vs 88.5%, branch 75.2% vs 82.1%). Authors conclude coverage is a weak proxy for fault detection. Caveat: the LLM was given bug context, so this is not like for like. [Moderate] [arXiv 2606.08588](https://arxiv.org/abs/2606.08588)
- VibeCheck (arXiv 2609.05978, Sept 2026): Kiro, Antigravity and Cursor (all Claude Sonnet 4.5) on 15 student Python and JS/TS repos; tests are "often runnable but frequently lack strong assertions and meaningful behavioral coverage"; weak assertions and missing edge cases are more common than blocking failures. [Weak, qualitative only on abstract page] [arXiv 2609.05978](https://arxiv.org/abs/2609.05978)
- CoverUp (Pizzorno and Berger, FSE 2025, arXiv 2403.16218), coverage guided prompting for Python: per-module median line+branch coverage 80% vs 47% for CodaMosa; overall 89% vs 77% for MuTAP. [Strong] [arXiv 2403.16218](https://arxiv.org/abs/2403.16218)
- TestGenEval (Jain, Synnaeve, Rozière, ICLR 2025, Meta): real world Python files. Full file generation: GPT-4o 35.2% average coverage, 18.8% mutation score, 7.5% all-pass@1; Llama 3.1 405B 35.0% coverage, 16.4% mutation score. Test completion is easier (GPT-4o 66.6%). Failures attributed to poor execution reasoning and frequent assertion errors. [Strong] [arXiv 2410.00752](https://arxiv.org/html/2410.00752v2)
- TestForge (agentic, on TestGenEval): 84.3% pass@1, 44.4% line coverage, 33.8% mutation score. [Moderate] [arXiv 2503.14713](https://arxiv.org/pdf/2503.14713)
- TestEval (Wang et al., NAACL 2025 Findings): 210 LeetCode Python programs, 16 LLMs, tasks of overall, targeted line/branch and targeted path coverage; targeting specific lines, branches or paths is "still challenging", read as limited understanding of execution paths. [Moderate, numbers not on abstract page] [arXiv 2406.04531](https://arxiv.org/abs/2406.04531)
- HITS (ASE 2024): slices complex methods and generates tests per slice; reported to beat LLM baselines and EvoSuite on line and branch coverage. [Moderate, no numbers on abstract page] [arXiv 2408.11324](https://arxiv.org/abs/2408.11324)
- ChatUniTest (FSE 2024 demo): generate, validate, repair loop for Java; beats TestSpark and EvoSuite in half the projects and has the highest overall line coverage. [Moderate] [arXiv 2305.04764](https://arxiv.org/abs/2305.04764)
- TestPilot (Schäfer et al., arXiv 2302.06527, later IEEE TSE 2024): 25 npm packages, 1,684 functions, gpt-3.5-turbo; median statement coverage 70.2% and branch 52.8% vs Nessie 51.3% and 25.6%; 92.8% of tests have at most 50% similarity to existing tests; StarCoder only 54.0% statements. [Strong] [arXiv 2302.06527](https://arxiv.org/abs/2302.06527)
- CodaMosa (Lemieux et al., ICSE 2023): runs search based testing (Pynguin) and calls Codex only when coverage plateaus; on 486 Python modules significantly higher coverage on 173 and reduced on 10 vs SBST, and 279 vs 4 against LLM only. [Strong] [GitHub microsoft/codamosa](https://github.com/microsoft/codamosa); [abstract record](https://aminer.org/pub/64c78ba33fda6d7f06dbcd01/codamosa-escaping-coverage-plateaus-in-test-generation-with-pre-trained-large-language)

### Inferences
- Coverage numbers in tool papers (70 to 90%) are on function or module targets and are not comparable with TestGenEval's whole-file setting (35%).
- Mutation score sits at about half of coverage in TestGenEval (18.8 vs 35.2), so roughly half of covered code is executed without an assertion that would notice a change. That gap is the most direct quantitative sign of weak oracles.
- The SWT-bench jump is the clearest positive trend: agents that can run code, reproduce, and check against the fixed version write tests that genuinely fail on the bug. This is the fail to pass oracle, which needs a known fix or an issue description.

### Gaps
- No exact per-model numbers for TestEval, HITS or ChatUniTest were available on the pages read.
- No independent 2026 SWT-bench replication found; entries are self submitted.

## The oracle problem: LLM tests that pass on buggy code, how often, and what helps

### Takeaway
Consistent evidence from 2024 to 2026 shows that showing the implementation to the model pulls its assertions toward the implementation's actual behaviour. With buggy code in the prompt, misguided (bug enshrining) tests rise about 8x and effective bug finding tests fall to about a third, compared with prompting from fixed code. Writing the test from a specification or docstring instead of the code, mutation feedback, and differential testing all measurably help; no approach removes the problem.

### Cited Findings
- Zhao, Zhou, Cohen, "Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests" (ISSTA 2026, arXiv 2607.22883): Defects4J v3.0, 318 focal methods covering 233 bugs, 11 LLMs (Gemini 2.5 Pro/Flash, Claude 4 Sonnet, GPT-4.1, o4-mini, DeepSeek V3/R1, Qwen3, Grok 3/4). Averages per model: buggy code in prompt gives 137.69 misguided tests (3.84%) and 104.15 effective (2.98%); fixed code gives 16.46 misguided (0.46%) and 304.08 effective (8.51%). Of tests that pass on buggy code, about 93.8% are harmless true negatives and 6.2% are misguided. Log-probability analysis shows buggy code shifts model preference toward tests asserting the buggy behaviour. [Strong] [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1)
- Same paper, mitigation: replace the code in the prompt with an LLM written specification docstring. Docstring only: 113.00 misguided (2.69%), 186.77 effective (4.50%), vs buggy code 137.69 / 104.15. Giving both docstring and buggy code is no better than code alone (146.08 / 121.92), so the code must be removed, not supplemented. An advanced docstring prompt reaches 87.38 misguided / 230.23 effective, but false positives (hallucinated behaviour) are 16 to 18%. Over three refinement rounds docstring input added 35.69 effective tests vs 17.62 for code. 15 to 21% of model written docstrings still preserved the bug; 47 to 62% recovered correct behaviour. On bug free code the approach costs nothing: compile failure 20.1% vs 21.3%, line coverage 75.1% vs 71.5%. [Strong] [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1)
- Konstantinou, Degiovanni, Papadakis, "Do LLMs Generate Test Oracles that Capture the Actual or the Expected Program Behaviour?" (arXiv 2410.21136, v2): 24 Java repos, GPT-3.5-turbo, GPT-4o-mini, DeepSeek V3, Codestral, GPT-5-mini replication. Conclusion: LLM test generation mainly captures actual behaviour. Accuracy at classifying a correct assertion as correct falls when the code is buggy: GPT-4o-mini 60.3% to 46.6%, DeepSeek V3 55.2% to 39.0%; GPT-5-mini 92.5% to 65.4% (27 points). Anonymising test and variable names drops accuracy by up to 15.4 points (GPT-4o-mini), so models lean on names. LLM oracles beat EvoSuite oracles only slightly in mutation score (about 19 to 21% vs 17 to 20%). [Moderate, preprint] [arXiv 2410.21136](https://arxiv.org/html/2410.21136v2)
- Huang, Zhang, Harman et al., "Measuring the Influence of Incorrect Code on Test Generation" (arXiv 2409.09464): 11 models, 3 benchmarks, 41 repo level cases. Correct code vs incorrect code in the prompt: +57% test accuracy, +12% coverage, +24% bug detection; on real world code, tests for incorrect code have 47% worse bug detection. Adding natural language descriptions improves accuracy 18%, coverage 4%, bug detection 34%. Zhao et al. argue this metric overstates the effect because over 90% of tests passing on buggy code are true negatives. [Moderate, under review] [arXiv 2409.09464](https://arxiv.org/abs/2409.09464); critique in [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1)
- He et al. (2025, cited by Zhao et al.): in iterative code and test co-generation, tests derived from buggy earlier code can reinforce existing flaws. [Weak, secondhand] [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1)
- TrickCatcher (Liu, Chen, ..., Harman et al., ACL 2025, arXiv 2404.10304): differential testing for "plausible programs" that pass existing tests. LLM writes program variants from the spec plus an input generator from the spec, runs inputs on the program and the variants, flags disagreements. Recall 1.80x, precision 2.65x, F1 1.66x over baselines on TrickyBugs (366 programs) and EvalPlus (151). [Strong] [arXiv 2404.10304](https://arxiv.org/abs/2404.10304)
- MuTAP (Dakhel et al., arXiv 2308.16557, later Information and Software Technology 2024): feed surviving mutants back into the prompt; 93.57% mutation score on synthetic buggy code; detects up to 28% more faulty human written snippets, 17% of which neither Pynguin nor zero/few shot LLMs caught. [Moderate] [arXiv 2308.16557](https://arxiv.org/abs/2308.16557)
- The TestGen-LLM paper states plainly that a failing generated test cannot be trusted without an oracle, which is why it discards failing tests. [Strong] [arXiv 2402.09171 HTML](https://arxiv.org/html/2402.09171)

### Inferences
- Rates: in Zhao et al.'s setup only about 4% of tests are misguided in absolute terms, but they outnumber effective tests when the code is buggy (3.84% vs 2.98%). A suite generated from buggy code is more likely to lock the bug in than to expose it.
- "Ask for expected values before showing code" is supported indirectly: the docstring only and no-code conditions both have fewer misguided tests than code conditions, and adding code back on top of a docstring cancels the benefit. Order or separation matters: the model should never see the implementation while choosing expected values.
- Model written specs inherit bugs 15 to 21% of the time when written from buggy code, so a human or upstream spec (issue text, docs, requirements) is better than a spec the model derives from the same code.

### Gaps
- I found no study isolating the exact "predict expected output first, then see code" two step protocol as a named intervention with its own numbers; evidence is through the docstring only conditions above.
- No large industrial measurement of how often accepted LLM tests in production enshrine a real bug.

## LLM generated property based tests and fuzz harnesses

### Takeaway
LLMs can write property based tests and fuzz harnesses that find real, previously unknown bugs, but raw output needs heavy validation: 2023 to 2024 work found GPT-4 got only 21% of documented properties right; a 2025 agent found real bugs across 100 Python packages with 56% of reports valid; Google's OSS-Fuzz-gen added 370k+ covered lines and 26 new vulnerabilities including an OpenSSL CVE.

### Cited Findings
- Agentic property based testing (Maaz, DeVoe, Hatfield-Dodds, Carlini, arXiv 2510.09907, Oct 2025): an agent reads code and docs, infers properties, writes and runs Hypothesis tests, reflects on failures and writes bug reports. Across 100 popular Python packages, 56% of bug reports were valid bugs and 32% were bugs the authors would report; of the 21 top ranked, 86% valid and 81% reportable. 5 reported, 4 with patches, 3 merged. [Moderate] [arXiv 2510.09907](https://arxiv.org/abs/2510.09907)
- Vikram, Lemieux, Sunshine, Padhye, "Can Large Language Models Write Good Property-Based Tests?" (arXiv 2307.04346, v2 July 2024): 40 Python API methods, GPT-4, Gemini 1.5 Pro, Claude 3 Opus. Best setup needed 2.4 samples on average to get one valid and sound PBT. GPT-4 correctly captured 21% of properties extractable from the API docs (property coverage, measured with property mutants). Soundness metric matched human judgement with 100% precision, 97% recall. [Moderate] [arXiv 2307.04346](https://arxiv.org/abs/2307.04346)
- OSS-Fuzz-gen (Google, Nov 2024): LLM written fuzz targets gained coverage in 272 C/C++ projects (up from 160), 370k+ new lines covered, largest single project from 77 to 5,434 lines; 26 new vulnerabilities in already heavily fuzzed projects, including OpenSSL CVE-2024-9143, likely present for two decades and not reachable by human written targets. Google notes line coverage is not a guarantee of absence of bugs. [Strong] [Google Security Blog](https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html)
- The google/oss-fuzz-gen README lists about 30 bugs found by generated targets; counts vary between snapshots and bug details are withheld while undisclosed. [Weak] [GitHub google/oss-fuzz-gen](https://github.com/google/oss-fuzz-gen)

### Inferences
- PBTs and fuzz harnesses sidestep the regression oracle trap: their oracles are generic (crash, sanitizer report, a property from documentation) rather than a value copied from the current output. That is why they find bugs in mature code where example based LLM tests mostly harden.
- The cost moves to triage: the PBT agent's 44% invalid reports and the per-property soundness problem mirror JiTTest's false positive rate.

### Gaps
- No primary 2025 or 2026 OSS-Fuzz-gen results update found in this session.
- Cost per valid bug for agentic PBT not on the abstract page.

## Flakiness of LLM generated tests

### Takeaway
LLM generated tests flake slightly more than human tests and copy flaky patterns from context; industry filters by repeated execution (Meta: 5 runs).

### Cited Findings
- "On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems" (arXiv 2601.08998, 2026): GPT-4o and Mistral Large wrote tests for 5,000+ C++ and SQL test files (SAP HANA, MySQL); slightly higher flaky share than existing tests; top cause was assuming a guaranteed result set order (72 of 115 flaky tests, 63%). A flaky assertion injected into the prompt context was copied into about two thirds of new SAP HANA tests and half of MySQL tests. Advice: fix existing flaky tests before using LLM generation. [Moderate] [arXiv 2601.08998](https://arxiv.org/abs/2601.08998)
- TestGen-LLM discards any test that does not pass 5 of 5 runs. [Strong] [arXiv 2402.09171 HTML](https://arxiv.org/html/2402.09171)

### Inferences
- Existing tests used as few shot context are a major source of both style and defects (flaky assertions, ordering assumptions), so the quality of the surrounding suite caps the quality of generated tests.

### Gaps
- No cross language flakiness rate for LLM tests beyond the DBMS study.

## What makes an LLM written test trustworthy, according to the evidence

### Takeaway
A generated test is trustworthy to the degree that something other than the current implementation decided its expected values, and something automatic proved it can fail. The evidence supports: oracle from a spec, issue or property not from the code; a demonstrated fail on a known fault (mutant kill or fail to pass on the bug); stability over repeated runs; real assertions; and human or assessor triage of any failing test.

### Cited Findings
- Expected behaviour must come from outside the code: docstring only prompts cut misguided tests and raise effective ones; adding code back cancels it. [Strong] [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1); natural language descriptions raise bug detection 34%. [Moderate] [arXiv 2409.09464](https://arxiv.org/abs/2409.09464)
- Proof it can fail: ACH accepts only tests that kill a targeted mutant (73% engineer acceptance) [Strong] [arXiv 2501.12862](https://arxiv.org/abs/2501.12862); SWT-bench counts a test only if it fails before the fix and passes after [Moderate] [swtbench.com](https://swtbench.com/); MuTAP's surviving mutant feedback raises bug detection up to 28% [Moderate] [arXiv 2308.16557](https://arxiv.org/abs/2308.16557).
- Mutation score, not coverage, is the better health metric: TestGenEval mutation score about half of coverage [Strong] [arXiv 2410.00752](https://arxiv.org/html/2410.00752v2); equal coverage with very different fault detection [Moderate] [arXiv 2606.08588](https://arxiv.org/abs/2606.08588); Google warns coverage is no guarantee [Strong] [Google Security Blog](https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html).
- Build, pass, 5x stability and coverage gain as minimum mechanical gates; missing assertions caused rejections. [Strong] [arXiv 2402.09171](https://arxiv.org/html/2402.09171)
- Weak assertions, not crashes, are the dominant failure of agent written tests in 2026 tools. [Weak] [arXiv 2609.05978](https://arxiv.org/abs/2609.05978)
- Failing LLM tests need triage: 8 of 41 JiTTest catches were real [Moderate] [arXiv 2601.22832](https://arxiv.org/abs/2601.22832); 56% valid PBT bug reports [Moderate] [arXiv 2510.09907](https://arxiv.org/abs/2510.09907); 16 to 18% hallucinated behaviour in spec first tests [Strong] [arXiv 2607.22883](https://arxiv.org/html/2607.22883v1).
- Independent oracles help: differential testing against spec derived variants gives 2.65x precision [Strong] [arXiv 2404.10304](https://arxiv.org/abs/2404.10304); property oracles and fuzzing find bugs in mature code [Strong] [Google Security Blog](https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html).
- Descriptive names steer the model: anonymising names cut oracle accuracy up to 15 points. [Moderate] [arXiv 2410.21136](https://arxiv.org/html/2410.21136v2)

### Inferences
- Practical rule set implied by the evidence: (1) write expected values from the spec, issue or docs before the model reads the implementation; (2) require each new test to fail on at least one plausible mutant or on the pre-fix code; (3) run it several times; (4) reject tests without meaningful assertions; (5) when a generated test fails on current code, treat it as a candidate bug to triage, not as a test to "fix" by changing the assertion, since changing the assertion is exactly how the bug gets enshrined.
- Passing tests generated from the code itself are best labelled regression snapshots: useful for change detection, not evidence of correctness.

### Gaps
- No controlled study found measuring developer trust or long term maintenance cost of accepted LLM tests.
- No head to head comparison of spec first vs mutation guided vs differential approaches on one benchmark.
