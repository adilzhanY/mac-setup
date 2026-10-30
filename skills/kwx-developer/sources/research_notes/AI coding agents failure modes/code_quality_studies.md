# Measured quality, security and maintainability of AI generated code (as of October 2026)

## Q1. Duplication, churn and refactoring in the AI era (GitClear, DORA)

### Takeaway
Repository-scale data from GitClear shows duplication rising and refactoring (moved code) falling since AI assistants spread, and Google DORA's survey data links AI adoption to lower delivery stability in both 2024 and 2025, while the throughput link flipped from slightly negative (2024) to positive (2025). All of it is correlational, and GitClear is a vendor with an analytics product to sell.

### Cited Findings
- GitClear 2025 report ("AI Copilot Code Quality", published February 2025): 211 million changed lines authored January 2020 to December 2024, from private repos (it names repos owned by Google, Microsoft, Meta and enterprise companies) plus large open source projects. [GitClear 2025 research page](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- GitClear 2025: "moved" lines (its proxy for refactoring and reuse) fell from about 25% of changed lines in 2021 to under 10% in 2024. Copy/pasted (cloned) lines rose from 8.3% in 2021 to 12.3% in 2024. 2024 was the first year copy/pasted lines exceeded moved lines. Headline: "4x more code cloning". [GitClear 2025 research page](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- Secondary coverage gives slightly different numbers for the same report (moved code 24.8% in 2021 to 9.5% in 2024, copy/paste 8.4% to 12.3%, and an eightfold rise in duplicated blocks of 5+ lines in 2024). [DevClass, Feb 2025](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/); [LeadDev](https://leaddev.com/software-quality/how-ai-generated-code-accelerates-technical-debt)
- GitClear's own page does not attribute the trend causally to AI per line; it compares years with rising AI adoption. The page also frames "cloned blocks in 10% of all authored commits" as a possibility, not a measurement. [GitClear 2025 research page](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- GitClear "The Maintainability Gap: AI Code Quality in 2026" (June 2026): 623M analyzed changes 2023-2026, eight quality signals. Versus 2022: refactoring down 70%, long-term legacy maintenance down 74%, code block duplication up 81%, "error-masking" up 47%, within-commit copy/paste up 41%. Methodology beyond sample size is not described on the summary page, and figures are relative changes without absolute baselines. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- Secondary sources on the 2026 report also cite a 15% rise in two-week churn and cross-file function calls down 35% in H1 2026 vs 2022; one gives refactoring share as 3.8% YTD 2026 vs 13% in 2023. These were not visible on GitClear's own summary page. [SoftwareSeni summary](https://www.softwareseni.com/the-evidence-against-vibe-coding-what-research-reveals-about-ai-code-quality/); [tech-insider](https://tech-insider.org/ai-code-quality-crisis-2026/)
- GitClear January 2026 study ("Coding Tools Attract Top Performers, But Do They Create Them?"): heavy AI users produce 4-10x more durable code than non-AI users but also 9x more code churn. GitClear itself says the gap partly reflects who adopts AI (selection bias). No sample size or method on the summary page. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- DORA 2024 (Google Cloud): as AI adoption increased, estimated delivery throughput fell 1.5% and estimated delivery stability fell 7.2%. Secondary sources frame this as per 25% increase in AI adoption. Survey-based associations, not causal. [Google Cloud blog, 2024 DORA report](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report); [RedMonk analysis](https://redmonk.com/rstephens/2024/11/26/dora2024/); [full report PDF](https://services.google.com/fh/files/misc/2024_final_dora_report.pdf)
- DORA 2025 ("State of AI-assisted Software Development", September 2025): nearly 5,000 respondents, about 90% use AI at work. AI adoption now correlates positively with throughput but is still associated with increased instability (change fail rate, rework rate). Frames AI as an "amplifier" of existing team strengths and weaknesses; about 30% of respondents say they do not trust AI generated code. [InfoQ](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025); [RedMonk 2025](https://redmonk.com/rstephens/2025/12/18/dora2025/); [Google Cloud blog 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
- DORA AI Capabilities Model (2025), as summarized by GitClear: flow efficiency about 21% (about 24.5 active hours vs 92.5 waiting hours); one AI-resolved microservice change took under 5 minutes of processing but a 5-day cycle time because of review waits. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)

### Inferences
- The direction is consistent across GitClear 2025, GitClear 2026 and DORA: more code and more duplication, less consolidation, and stability not improving. The magnitude is uncertain, because none of these can tell AI-written lines apart from human-written lines with certainty.
- DORA's move from negative to positive throughput while instability persists fits the pattern "AI speeds up output but the delivery system absorbs the cost downstream".

### Gaps
- I could not open the full GitClear 2026 report, so its churn definition and per-tool breakdowns are unverified; secondary numbers conflict.
- I did not verify DORA 2025 effect sizes (no per-25% numbers found) from the primary PDF.
- No independent (non-vendor) replication of GitClear's duplication metrics was found.

## Q2. Security flaw rates in AI generated code

### Takeaway
Benchmark and user studies converge on roughly 40-55% of AI generated security-relevant code containing a weakness, and this rate has barely improved with newer models (Veracode 2025 and 2026). User studies add that people with AI assistance write less secure code while feeling more confident.

### Cited Findings
- Pearce et al., "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions" (IEEE S&P 2022; arXiv 2021): 89 scenarios, 1,689 programs, approximately 40% vulnerable (abstract figures). [arXiv 2108.09293](https://arxiv.org/abs/2108.09293)
- Search summaries of the paper's detailed results report, for the CWE-diversity part, 54 scenarios over 18 CWEs, 1,084 valid programs, 477 (44.0%) with a CWE, and the top-ranked suggestion vulnerable in 44.44% of scenarios. A version appeared in Communications of the ACM in February 2025. [arXiv PDF 2108.09293](https://arxiv.org/pdf/2108.09293)
- Majdinasab et al. targeted replication (2023/2024, newer Copilot 1.77, MITRE top 25 CWEs): 39.33% of top suggestions and 40.73% of all suggestions vulnerable across languages; Python only 37.93% top / 36.54% total. Some newer suggestions had more weaknesses than in the original study. [arXiv 2311.11177](https://arxiv.org/pdf/2311.11177v1.pdf); [replication repo](https://github.com/CommissarSilver/CVT)
- Perry, Srivastava, Kumar, Boneh (Stanford), "Do Users Write More Insecure Code with AI Assistants?" (ACM CCS 2023): 47 participants, 5 security tasks in Python, JavaScript and C, using codex-davinci-002. The AI group wrote insecure solutions more often on 4 of 5 tasks and was more likely to believe its code was secure. Participants who trusted the AI less and reworked prompts produced fewer security problems. Results on the C task were mixed. [arXiv 2211.03622](https://arxiv.org/html/2211.03622v3); [Computing coverage](https://computing.co.uk/news/4061952/ai-assistants-produce-buggy-insecure-code)
- Veracode 2025 GenAI Code Security Report (July 30, 2025): 80 curated tasks built around CWE weaknesses, 100+ LLMs. Models chose the insecure option in 45% of cases. Java worst at over 70% failure; Python, C# and JavaScript 38-45%. XSS (CWE-80) defended against in only 14% of relevant samples (86% failure). Security performance flat across model generations even as syntax correctness improved. [Veracode press release](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/); [Help Net Security](https://www.helpnetsecurity.com/2025/08/07/create-ai-code-security-risks/)
- Veracode 2026 GenAI Code Security Report (July 28, 2026): average security pass rate about 56% (about 55% in a spring 2026 snapshot), so barely moved in a year. Leaderboard: GPT-5.5 at 68%, GPT-5.3-Codex and Claude Opus 4.8 at 62%; 6 of 11 leaderboard models between 50% and 53%. Coding-specialized models no safer than general ones. Category spread: crypto algorithms 87% pass, XSS 15%, log injection 12%. [SD Times](https://sdtimes.com/agentic-security/veracode-finds-ai-generated-code-security-has-barely-improved-since-last-year/); [Las Vegas Sun / Business Wire release](https://lasvegassun.com/news/2026/jul/28/llms-are-getting-smarter-but-not-safer-veracode-20/); [eSecurity Planet](https://www.esecurityplanet.com/fr/threats/veracode-finds-ai-generated-code-still-struggles-with-security/); [tech-insider](https://tech-insider.org/ie/ai-generated-code-security-2026/)
- CodeRabbit "State of AI vs Human Code Generation" (December 17, 2025): 470 open source GitHub PRs (320 AI co-authored, 150 human only). AI PRs averaged 10.83 issues vs 6.45 (about 1.7x); 1.4x more critical and 1.7x more major issues; security issues about 1.57x, XSS 2.74x; logic/correctness 1.75x, maintainability 1.64x, performance 1.42x. Humans had more spelling and testability issues. [CodeRabbit report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report); [The Register](https://www.theregister.com/2025/12/17/ai_code_bugs/); [InfoWorld](https://infoworld.com/article/4109129/ai-assisted-coding-creates-more-problems-report.html)

### Inferences
- The roughly 40% vulnerability rate from 2021 Copilot to the roughly 45% insecure choice rate (Veracode 2025) and roughly 44% failure rate (Veracode 2026, 56% pass) suggests model capability gains have not translated into secure-by-default code. Security needs explicit prompting, review and scanning.
- Perry et al. is the strongest evidence of a human factor: overconfidence, not just model output, drives the risk.

### Gaps
- No 2025 or 2026 peer-reviewed replication of Perry et al. with agentic tools was found.
- Veracode tasks are designed to offer a secure vs insecure choice; they are not a sample of production AI code, so 45%/56% are benchmark rates, not field rates.
- Snyk and Sonar 2025/2026 quantitative reports were not retrieved in this pass.

## Q3. Package hallucination (slopsquatting) and outdated APIs

### Takeaway
LLMs invent package names at substantial rates (about 20% of recommended packages across 16 models in Spracklen et al.), the fake names repeat across runs (making them squattable), and models also use deprecated APIs. Retrieval, self-checking and fine-tuning cut hallucination, and registry verification plus lockfiles and agent sandboxing are the practical defenses.

### Cited Findings
- Spracklen et al., "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs" (arXiv June 2024; USENIX Security 2025): 19.7% of generated packages across tested LLMs were hallucinated, 205,474 unique hallucinated names. [arXiv 2406.10279](https://arxiv.org/abs/2406.10279v1)
- Same study, per secondary write-ups: about 576,000 code samples, 16 models (Python and JavaScript); open source models hallucinated 21.7% on average vs 5.2% for commercial; GPT-4 Turbo best at 3.59%; CodeLlama worst, over a third. [Socket blog](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks); [The Register](https://www.theregister.com/2024/09/30/ai_code_helpers_invent_packages/)
- Persistence: re-running a triggering prompt 10 times, 43% of hallucinated packages recurred every time and 39% never recurred. More verbose models (recommending more unique packages) hallucinated more. [Socket blog](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks)
- Mitigations in the paper: RAG, self-detection feedback and fine-tuning reduced hallucination, one model to under 3%, but fine-tuning reduced code quality (26.1% for DeepSeek, 3.1% for CodeLlama, per The Register). Simple cross-referencing against a known-package list is not sufficient because an attacker may already have registered the name. [The Register](https://www.theregister.com/2024/09/30/ai_code_helpers_invent_packages/); [arXiv HTML v3](https://arxiv.org/html/2406.10279v3)
- Real-world proof of concept: researcher Bar Lanyado registered an empty "huggingface-cli" package that LLMs kept recommending; it drew over 30,000 downloads in about three months (2023/2024, sources disagree on the date). As of the Wikipedia article, no confirmed slopsquatting attack in the wild had been reported. [Wikipedia: Slopsquatting](https://en.wikipedia.org/wiki/Slopsquatting)
- Recommended defenses (consistent across practitioner sources): committed lockfiles, verifying names exist in the official registry and checking their age/downloads, blocking agents from running installs outside a sandbox, pre-execution hooks on install commands. [Codex CLI defence write-up, June 2026](https://codex.danielvaughan.com/2026/06/16/slopsquatting-hallucinated-packages-codex-cli-supply-chain-defence-pretooluse-hooks-lockfile-discipline/); [Wikipedia: Slopsquatting](https://en.wikipedia.org/wiki/Slopsquatting)
- Deprecated APIs: Wang et al., "How and Why LLMs Use Deprecated APIs in Code Completion?" (ICSE 2025): 7 LLMs, 145 API mappings from 8 Python libraries, 28,125 prompts. All 7 models had trouble with deprecated API usage; outdated context in the prompt pushes models toward deprecated APIs. Proposed fixes REPLACEAPI and INSERTPROMPT are baselines; INSERTPROMPT alone was not sufficiently effective. [arXiv 2406.09834](https://arxiv.org/abs/2406.09834); [arXiv HTML](https://arxiv.org/html/2406.09834v1)

### Inferences
- Because many hallucinated names recur deterministically, slopsquatting is a targeted, repeatable attack, and agents that install dependencies autonomously widen the exposure (no human sees the install).
- Deprecated API usage is driven by training cutoff plus surrounding code; giving the model current docs (retrieval) is the natural mitigation, consistent with the RAG result for packages.

### Gaps
- I did not find the exact deprecated-API usage percentages; the abstract does not state them.
- Claims of 2026 agent incidents installing hallucinated packages come only from blogs and were not verified.
- Package hallucination rates for 2026 frontier models were not found; the 3.59% best case is GPT-4 Turbo era.

## Q4. Controlled studies on productivity and quality together, and review burden

### Takeaway
Rigorous trials disagree: METR found experienced open source developers 19% slower with early-2025 AI while believing they were 20% faster, and its late-2025 rerun points to a modest speedup but METR calls that data unreliable. Telemetry studies show large output gains but also much longer reviews, larger PRs and more bugs per developer, so the bottleneck moves to review.

### Cited Findings
- METR RCT (published July 10, 2025): 16 experienced developers on their own large open source repos, 246 tasks (about 2 hours each), randomized AI-allowed vs disallowed, mainly Cursor Pro with Claude 3.5/3.7 Sonnet. AI-allowed tasks took 19% longer (95% CI +2% to +39%). Developers predicted 24% speedup and afterwards still believed 20% speedup. Time went to prompting, waiting and reviewing/cleaning AI output. Developers had limited Cursor experience. [METR blog](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [arXiv 2507.09089](https://web3.arxiv.org/pdf/2507.09089)
- METR follow-up (February 24, 2026): 57 developers (10 returning, 47 new), 143 repos, 800+ tasks, pay cut from $150 to $50/hour. Returning developers: -18% time (speedup), 95% CI -38% to +9%; new developers: -4%, CI -15% to +9%. METR calls it "very weak evidence": developers refused to work without AI, 30-50% withheld tasks they would not do without AI, task substitution, quality differences, multi-agent time tracking errors. METR treats the estimate as a likely lower bound and is redesigning the study. [METR uplift update](https://metr.org/blog/2026-02-24-uplift-update/)
- Google enterprise RCT (Paradis et al., ICSE 2025 SEIP; arXiv October 2024): 96 Google engineers, one complex enterprise task, three internal AI features. Best estimate about 21% faster, with a wide confidence interval; may not generalize beyond Google tooling. [arXiv 2410.12944](https://arxiv.org/abs/2410.12944)
- Faros AI "AI Productivity Paradox" (2025, telemetry, about 10,000 developers across about 1,200 to 1,255 teams, comparing each org's own low vs high adoption periods): high-adoption teams completed 21% more tasks and merged 98% more PRs, but PR review time rose 91%, average PR size grew 154%, and bugs per developer rose 9%; no significant correlation with company-level improvement. Primary report gated; figures from secondary summaries. [Faros AI page](https://www.faros.ai/ai-productivity-paradox); [Augment Code summary](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery)
- Popescu et al. (arXiv 2604.00917, April 2026) as summarized by GitClear: Claude-authored PRs averaged about 6x human PR size and Copilot about 3x; Codex PRs had an 87.5% merge-qualification rate vs 75.1% for humans. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- Large telemetry studies (2026), as summarized by GitClear: Heilman, Kyloo, Murphy-Hill (16,223 developers over 43 weeks) found Copilot users completed 40.5% more PRs in their highest-usage weeks; Demirer, Musolff, Yang (NBER w35275, 100,000+ developers) found commit effects of 40% (autocomplete), 140% (interactive) and 180% (autonomous agents), but the 180% shrinks to 50% for projects and 30% for releases. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- Trust: Stack Overflow 2025 survey, 33% trust AI output vs 46% distrust, only 3.1% "highly trust". [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)

### Inferences
- Commit and PR counts inflate far more than shipped outcomes (180% commits vs 30% releases in NBER w35275), so activity metrics overstate AI gains.
- Review is the new constraint: bigger PRs, more of them, and longer review times (Faros, Popescu, DORA flow efficiency) mean quality depends on review capacity.
- Self-reported speedup is unreliable (METR perception gap), so claims based on developer surveys should be discounted.

### Gaps
- The METR follow-up does not measure code quality directly; quality differences were only self-reported.
- I did not open the NBER and Heilman et al. primary papers; numbers come from GitClear's summary page.

## Q5. Weak, contested or vendor-marketing findings

### Takeaway
Most widely quoted numbers come from vendors that sell the remedy (GitClear analytics, Veracode and Snyk scanners, CodeRabbit review, Faros metrics) and are observational; the strongest causal designs (METR, Google RCT, Perry et al.) are small and point in different directions.

### Cited Findings
- GitClear sells code analytics; its research is first party, several 2026 figures are relative changes without baselines, and the January 2026 study has no published sample or method on the summary page. [GitClear AI research background page](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- Secondary outlets report inconsistent GitClear 2025 numbers (moved code "24.8% to 9.5%" vs "about 25% to under 10%"; copy/paste "8.3%" vs "8.4%" vs "almost 15%"). [GitClear 2025 page](https://www.gitclear.com/ai_assistant_code_quality_2025_research); [DevClass](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/)
- CodeRabbit sells AI code review; its sample is 470 PRs and depends on PRs being labeled AI co-authored. [CodeRabbit report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report); [The Register](https://www.theregister.com/2025/12/17/ai_code_bugs/)
- Veracode's 45% / 56% are rates on its own 80-task benchmark that forces a secure vs insecure choice, not field measurements of shipped code. [Veracode 2025 press release](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/)
- DORA's AI findings are survey correlations; 2024 and 2025 disagree on throughput direction. [Google Cloud 2024 DORA blog](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report); [InfoQ 2025](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)
- METR itself marks its 2025 result as no longer reflecting current models and calls its 2026 data unreliable; the 2025 RCT had only 16 developers. [METR uplift update](https://metr.org/blog/2026-02-24-uplift-update/)
- The often quoted 55.8% Copilot speedup came from an earlier small trial (95 participants, a simple HTTP server task) and is contrasted by Google's 21% estimate on a realistic task. [arXiv 2410.12944](https://arxiv.org/abs/2410.12944)
- Faros figures circulate mainly through vendor blogs; the report is registration gated and sample size is quoted as both 1,200 and 1,255 teams. [Augment Code summary](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery)

### Inferences
- The most robust claims: (1) AI code often contains security weaknesses at rates similar to or above human baselines, and newer models have not fixed this; (2) LLMs hallucinate package names repeatably; (3) AI raises code volume, PR size and review load; (4) self-reported productivity overstates measured productivity. The least robust: precise duplication percentages, "1.7x more bugs", and any single speedup number.

### Gaps
- No large independent (academic, non-vendor) longitudinal study of AI vs human code maintainability in production was found.
- Sonar and Snyk quantitative reports were not covered in this pass.
