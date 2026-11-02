# AI agents that drive browsers, mobile apps and desktop GUIs for software testing (2024 to 2026)

Research date: 2026-10-31. Evidence strength tags: [strong] = primary source fetched or peer reviewed paper; [medium] = primary source seen only through search snippets, or vendor self report; [weak] = aggregator, vendor marketing or blog; [prior] = from the researcher's background knowledge of a well known primary source, URL not re-fetched in this session, so the report writer should treat the exact number as needing a spot check.

## Benchmarks and success rates: how capable are GUI agents in 2024 to 2026?

### Takeaway
Capability rose very fast: OSWorld (desktop) went from about 12% (2024) to 61% (Claude Sonnet 4.5, Sept 2025) to 80 to 86% on OSWorld-Verified by late 2026, above the 72.36% human baseline, and AndroidWorld top claims reach 97 to 100% (self reported). But the harder successors (OSWorld 2.0 at about 20.6% full completion) and live web evaluation (Online-Mind2Web, Operator 61% vs near 90% claimed on WebVoyager) show that saturated benchmark scores overstate real world reliability, and that per task success still falls well short of what a deterministic test suite gives.

### Cited Findings
Desktop (OSWorld family)
- OSWorld original paper (2024): best model 12.24% vs human 72.36% on 369 real computer tasks. [prior] [OSWorld paper](https://arxiv.org/abs/2404.07972)
- Anthropic's first computer use release (Oct 2024, Claude 3.5 Sonnet): 14.9% on OSWorld screenshot only category, described by Anthropic as experimental, "cumbersome and error prone". [prior] [Anthropic: Developing computer use](https://www.anthropic.com/news/developing-computer-use)
- OpenAI CUA / Operator (Jan 2025): 38.1% OSWorld, 58.1% WebArena, 87% WebVoyager. [prior] [OpenAI: Computer-Using Agent](https://openai.com/index/computer-using-agent/) (page returned HTTP 403 on fetch this session)
- Claude Sonnet 4.5 (Sept 2025): 61.4% OSWorld, up from 42.2% for Sonnet 4 and 44.4% for Opus 4.1; trackers list 62.9% on OSWorld-Verified. [medium] [Leanware summary of Anthropic results](https://leanware.co/insights/claude-sonnet-4-5-overview); [Engadget](https://www.engadget.com/claude-sonnet-45-is-anthropics-safest-ai-model-yet-170000161.html)
- OSWorld-Verified, as of Oct 2026: most top entries 80 to 86%, i.e. above the 72.36% human baseline. presenc.ai lists Intelligence-Indeed Agent 90.19%, Claude Fable 5 85.96%, Claude Opus 5 83.39% (as of 2026-10-01); Yutori lists Claude Fable 5 86.0%, Navigator n2 85.3%; Steel.dev lists Qwen3.8-Max 86.1%. The leaderboards disagree on the leader. [weak] [presenc.ai](https://presenc.ai/research/osworld-computer-use-leaderboard-2026); [Yutori](https://yutori.com/leaderboards/osworld-verified); [Steel.dev](https://leaderboard.steel.dev/leaderboards/osworld/)
- OSWorld 2.0 (harder successor): best reported 20.6% binary completion (54.8% partial credit) for Claude Opus 4.8 at max thinking with a 500 step limit. [weak, single aggregator] [presenc.ai](https://presenc.ai/research/osworld-computer-use-leaderboard-2026)

Web (WebArena, VisualWebArena, Mind2Web family)
- WebArena (self hosted e-commerce, GitLab, Reddit clone, CMS, maps): GPT-4 agent 14.41% vs human 78.24% at publication (2023/ICLR 2024). [prior] [WebArena paper](https://arxiv.org/abs/2307.13854)
- VisualWebArena (visually grounded web tasks): best GPT-4V agent about 16.4% vs human about 88.7% at publication (2024). [prior] [VisualWebArena paper](https://arxiv.org/abs/2401.13649)
- Mind2Web (2023) is an offline, static, step level dataset (2,000+ tasks, 137 sites); it measures element and action prediction, not live task completion. [prior] [Mind2Web paper](https://arxiv.org/abs/2306.06070)
- Online-Mind2Web ("An Illusion of Progress?", Xue et al., 2025, v4 Oct 2025): 300 live tasks on 136 websites, human evaluated. Operator reaches only about 61%; Browser Use about 30%, close to the simple SeeAct baseline (about 31%); most recent agents except Claude Computer Use 3.7 and Operator did not beat SeeAct. Frontier agents had claimed close to 90% on WebVoyager. [strong for Operator 61%, medium for Browser Use 30%] [arXiv 2504.01382](https://arxiv.org/abs/2504.01382); [HAL leaderboard](https://hal.cs.princeton.edu/online_mind2web)
- Gemini 2.5 Computer Use (Oct 2025, preview via Gemini API): Google's chart shows about 70%+ on Online-Mind2Web (Browserbase harness) with about 225 s latency; a secondary summary gives 65.7% vs Claude Sonnet 4 61.0% and OpenAI Agent 44.3%. Google says it is optimized for browsers, promising on mobile, and "not yet optimized for desktop OS-level control". [medium; numbers conflict between sources] [Google blog](https://blog.google/technology/google-deepmind/gemini-computer-use-model/); [InfoQ](https://www.infoq.com/news/2025/10/gemini-computer-use)

Mobile (AndroidWorld)
- AndroidWorld original paper (2024): M3A agent 30.6% vs human 80.0% on 116 tasks across 20 real apps. [strong] [arXiv 2405.14573](https://arxiv.org/html/2405.14573)
- Gemini 2.5 Computer Use: 69.7% AndroidWorld (secondary source attributing to DeepMind). [medium] [implicator.ai](https://www.implicator.ai/googles-gemini-2-5-computer-use-bets-on-the-browser-not-the-desktop)
- 2026 claims: Minitap multi agent system 100% on all 116 tasks (single agent baseline in same paper 64%) (Feb 2026 preprint); benchmarklist snapshot (about June 2026) ranks AGI-0 at 97.4% pass@1, a Sonnet 4.5 + Sonnet 4 entry at 86.2%; Fluiz (Korean startup) claims 100% (Sept 2026); UI Voyager claims 81.0% with about a 4B model. All self reported, no single verified leaderboard. [weak to medium] [Minitap arXiv 2602.07787](https://www.arxiv.org/pdf/2602.07787); [benchmarklist](https://benchmarklist.com/benchmarks/androidworld/); [AlphaMaven on Fluiz](https://alpha-maven.com/story/venture-capital/korean-startup-fluiz-achieves-100-on-androidworld-mobile-ai-benchmark-donga-science)

### Inferences
- Benchmarks like AndroidWorld and OSWorld-Verified are near saturation; scores on them no longer predict whether an agent will reliably finish a novel, long, or visually unusual flow in a real product. Live web (Online-Mind2Web) and harder successors (OSWorld 2.0) are better reality checks.
- Even an 85% task success rate means about 1 in 7 runs fails for agent reasons, not product reasons. For QA this is the core problem: a failed agent run is ambiguous (product bug or agent error) and needs triage.
- Best fit today: exploratory testing, smoke checks of a new feature, reproducing a reported bug, and drafting tests; poor fit: the gate that blocks a merge.

### Gaps
- Could not fetch OpenAI's CUA page (403) or Anthropic's model cards to re-verify the 2025 numbers; listed as [prior]/[medium].
- No verified current WebArena or VisualWebArena leaderboard top score was retrieved for 2026.
- Project Mariner standalone numbers (Google reported 83.5% on WebVoyager in Dec 2024 per prior knowledge) were not re-verified this session.
- Several 2026 model names (Claude Fable 5, Opus 5, Qwen3.8-Max) appear only via aggregators; cross check against the official OSWorld site (os-world.github.io) before quoting.

## Tooling: Playwright MCP, Chrome DevTools MCP, browser-use, Stagehand, and which interface works best

### Takeaway
For driving a web app, structured text (the accessibility tree via Playwright MCP snapshots, or DOM via CDP) is cheaper, more precise and more deterministic than screenshots, which cost roughly 10x to 50x more tokens; screenshots remain necessary for visual and layout bugs, canvas and custom widgets. Chrome DevTools MCP is the better tool for debugging (console, network, performance traces) than for flow testing. No rigorous reliability benchmark of these tools for testing exists; numbers are vendor or blog level.

### Cited Findings
- Playwright MCP gives every interactive element in an accessibility snapshot a ref, so the agent targets "this button" instead of guessing from pixels; refs are only valid for one snapshot and page state, not across navigation or rerenders; recommended loop is snapshot, act, verify a semantic postcondition, snapshot again. [medium] [Playwright MCP snapshots docs](https://playwright.dev/mcp/snapshots); [Codex CLI with Playwright MCP](https://codex.danielvaughan.com/2026/08/14/codex-cli-playwright-mcp-browser-automation-accessibility-snapshots-testing/)
- Token cost: snapshot about 2 to 5 KB vs 100 KB+ for a screenshot of the same page; Playwright MCP docs estimate screenshots at about 10,000 to 50,000 tokens with a vision model; simple page snapshots 2,000 to 5,000 tokens. A typical MCP browser session about 114,000 tokens; Playwright CLI about 4x fewer (about 27,000); Playwright MCP tool definitions alone cost about 15,000 tokens before any action (mitigation: --caps=none or the CLI). [weak to medium, blog figures] [DEV: why snapshots beat screenshots](https://dev.to/pointchecknote/browser-automation-with-claude-playwright-mcp-why-accessibility-snapshots-beat-screenshots-2pke); [TestDino](https://testdino.com/blog/playwright-mcp); [Mintlify Playwright MCP docs](https://www.mintlify.com/microsoft/playwright-mcp/concepts/accessibility-snapshots)
- Limits of snapshots: an accessibility tree does not show wrong colours, stuttering animation, or a layout that collapses at a given width; canvas and custom widgets outside the tree are hard. Recommendation: snapshots drive interaction, screenshots are a second evidence channel for visual regressions. Same sources advise MCP for exploration and targeted verification, not bulk regression. [weak] [Shiplight: Playwright MCP](https://www.shiplight.ai/blog/playwright-mcp); [Codex CLI with Playwright MCP](https://codex.danielvaughan.com/2026/08/14/codex-cli-playwright-mcp-browser-automation-accessibility-snapshots-testing/)
- Chrome DevTools MCP: lets coding agents (Antigravity, Claude, Cursor, Copilot) control and inspect a live Chrome; tools include performance_start_trace, performance_analyze_insight, list_network_requests, list_console_messages; a roughly 30 MB raw performance trace is condensed to about 4 KB for the model. The server collects usage statistics (tool success rates, latency, environment) by default. [medium] [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp); [Addy Osmani talk deck](https://talks.addy.ie/openai-devtoolsmcp-2026/deck); [DEV: Chrome DevTools MCP](https://dev.to/grove_chatforest/chrome-devtools-mcp-server-browser-debugging-and-performance-profiling-for-ai-agents-a0h)
- Stagehand (Browserbase): primitives act (single action), extract (typed data with a schema), observe (list candidate actions); the LLM picks elements and plans, but all browser control is deterministic CDP commands; caching replays successful actions with no LLM call (keyed on instruction, URL and page state) and "self heals" by updating selectors when the page changes. Stagehand publishes no WebVoyager style success score. [medium, vendor docs] [Stagehand act docs](https://docs.stagehand.dev/v3/basics/act); [Stagehand caching](https://docs.stagehand.dev/v2/best-practices/caching); [How Stagehand works](https://www.mintlify.com/browserbase/stagehand/concepts/how-stagehand-works)
- browser-use: self reported 89.1% on WebVoyager (586 tasks, GPT-4o, Dec 2024 technical report); independently measured at about 30% on live Online-Mind2Web. [medium] [AgenticWire browser-use vs Stagehand](https://www.agenticwire.news/article/browser-use-vs-stagehand); [arXiv 2504.01382](https://arxiv.org/abs/2504.01382)
- Interface tradeoff in vendor products: Gemini 2.5 Computer Use and OpenAI CUA are screenshot (pixel) based models that output click coordinates. [medium] [Google blog](https://blog.google/technology/google-deepmind/gemini-computer-use-model/)

### Inferences
- Interface ranking for a testing agent on web: (1) accessibility tree / role and name locators (Playwright MCP, CLI), which also nudges teams toward accessible markup; (2) DOM/CDP with an LLM choosing elements (Stagehand, browser-use); (3) screenshots plus coordinates, used for visual checks and for apps with no usable tree (canvas, games, remote desktops, some desktop apps).
- A page that is hard for the agent to drive through the accessibility tree is often also an accessibility defect worth reporting.
- Token cost shapes design: prefer the CLI or reduced capability MCP for long sessions, and avoid screenshots per step unless the check is visual.

### Gaps
- No controlled study found comparing accessibility tree vs screenshot vs DOM agents on the same testing tasks with failure rates.
- No published reliability rate for Playwright MCP or Chrome DevTools MCP on testing tasks.

## LLM based mobile GUI testing research vs Monkey, Stoat, APE

### Takeaway
Research tools (GPTDroid, DroidAgent, AUITestAgent, VisionDroid, AutoDroid, LLMDroid, GraphDroid) show LLM guidance helps with semantic inputs (forms, logins) and with functional, non crash bugs, but pure step by step LLM exploration is slow and expensive; third party comparisons find its coverage per hour is often lower than self reported, and hybrids (cheap random or model based exploration with the LLM called only when stuck) win on coverage, bugs and cost.

### Cited Findings
- GPTDroid (ICSE 2024): frames testing as a Q&A with the LLM; authors report about 71% activity coverage on 86 apps, more than 32% above the best of 9 baselines, and 72 bugs. [strong, self reported] [arXiv 2305.09434](https://arxiv.org/pdf/2305.09434); [arXiv 2310.15780](https://arxiv.org/pdf/2310.15780)
- DroidAgent (Yoon et al., ICST 2024): intent driven agent that sets its own task goals; 61% average activity coverage, above all baselines, and higher feature coverage than the best baseline Humanoid. [strong, self reported] [arXiv 2311.08649](https://www.alphaxiv.org/abs/2311.08649)
- LLMDroid (FSE 2025) independent comparison: per app hour, DroidAgent (GPT-3.5) 10.77% code / 18.71% activity coverage vs GPTDroid 7.43% / 7.33%; both spend 69.7% and 59.2% of time blocked waiting on the LLM at each action. LLMDroid calls the LLM only when coverage stalls. [strong] [LLMDroid, ACM](https://dl.acm.org/doi/10.1145/3715763)
- GraphDroid (2026 preprint), deduplicated crashing bugs found: GraphDroid 13, LLMDroid 7, LLMExplorer 5, DQT 4, DroidAgent 3, VisionDroid 2, GPTDroid 1; vs the best pure LLM baseline DroidAgent, improvements of 36.4%, 49.7% and 87.5% on its metrics at under one eighth of the cost. [medium, preprint] [arXiv 2609.10031](https://arxiv.org/html/2609.10031v1)
- AUITestAgent (Fudan with Meituan, 2024): natural language requirement in, test executed and verified; separates interaction from verification, which works on the interaction trace; 94% verification accuracy on the authors' own benchmark, recalls 90% of functional bugs with under 5% false positives; at Meituan it found 4 new functional bugs in 10 regression runs over two months (one arXiv version has "xx" placeholders, so deployment scale is unconfirmed). [medium, self reported] [arXiv 2407.09018](https://arxiv.org/html/2407.09018v1)
- VisionDroid (Liu et al., 2024): multimodal LLM using screenshots plus view hierarchy to detect non crash functional bugs (wrong display, logic errors that do not crash). Appears mostly as a baseline in later work (2 crashes in GraphDroid's comparison). [medium] [LLM-Brained GUI Agents survey](https://arxiv.org/pdf/2411.18279); [GraphDroid](https://arxiv.org/html/2609.10031v1)
- AutoDroid (MobiCom 2024) is a task automation agent (not a tester) that combines LLM with app specific knowledge from offline exploration; reported about 90.9% action accuracy and 71.3% task completion. [prior] [AutoDroid arXiv 2308.15272](https://arxiv.org/abs/2308.15272)
- 2026 hybrid direction: LLM used to escape "UI tarpits" during random testing, and dependency guided recomposition for deep state discovery. [medium] [arXiv 2604.06763](https://arxiv.org/pdf/2604.06763); [EpiDroid arXiv 2604.01522](https://arxiv.org/pdf/2604.01522)

### Inferences
- Classic tools (Monkey, APE, Stoat, Humanoid) remain strong cheap baselines for crash finding and raw coverage; the LLM's advantage is semantic: valid form inputs, login, multi step business flows, and judging whether the screen is functionally wrong.
- A QA agent on mobile should use the LLM for intent (what to test, what input to type, is this output correct) and let deterministic machinery (Maestro, Espresso, random or model based explorers) do the bulk stepping.
- Most coverage numbers are self reported on different app sets; independent comparisons report much lower figures.

### Gaps
- Could not retrieve VisionDroid's own headline numbers this session.
- No head to head of these research tools against industrial tools (Maestro, Appium plus LLM, commercial AI testers) was found.

## Generated test scripts (Playwright, Maestro) vs agents clicking live: which is more reliable for regression?

### Takeaway
For regression, the agent should write deterministic scripts (Playwright tests, Maestro flows) that run without an LLM in CI; live agent clicking is better for exploration, bug reproduction and drafting. Playwright itself ships this pattern (planner, generator, healer) since late 2025. Evidence is mostly practitioner level: generated suites need review and rework, and live agent runs add LLM nondeterminism as a new flakiness source.

### Cited Findings
- Playwright Test Agents: Planner explores the app and writes a Markdown plan in specs/ (from a request, a seed test and optional PRD); Generator turns the plan into Playwright Test files in tests/, verifying selectors and assertions against the live app as it goes, and the files may contain initial errors; Healer reruns failing tests, inspects the current UI, and patches locators, waits or data, looping until pass or guardrails stop it; if it judges the feature itself broken it skips the test. Setup: npx playwright init-agents --loop=vscode|claude|codex|opencode; VS Code 1.105 (Oct 9, 2025) needed. [strong] [Playwright Test Agents docs](https://playwright.dev/docs/test-agents)
- Stagehand's cache records successful AI actions and replays them with zero LLM calls, i.e. it converts live agent actions into deterministic replays. [medium] [Stagehand caching](https://docs.stagehand.dev/v2/best-practices/caching)
- International Journal of Contents (Mar 2026): GPT-4o plus Playwright MCP generating and running web tests, compared against script based Playwright on 12 scenarios run 5 times each (full results tables not retrieved). [medium] [IJCon 22(1)](https://accesson.kr/ijcon/assets/pdf/59002/journal-22-1-77.pdf)
- Practitioner six month report: agent suite 3.2% flakiness in month one vs 0.8% for a hand written suite, but the agent found 47 bugs the hand written suite missed; the agent hardcoded a value seen during generation, which broke tests. [weak] [ScrollTest](https://scrolltest.com/ai-agent-testing-playwright-6-months-production/)
- Guidance to budget 15 to 30% rework on AI generated tests (struggles with framework utilities and business logic). [weak] [Medium review of Playwright agents](https://medium.com/@valentijnvanwynsberghe/i-tested-playwrights-new-ai-agents-against-ai-native-testing-platforms-here-s-what-i-found-250e36ba89dd)
- Agent generated tests fail in clusters tied to when they were generated and can masquerade as flakiness; tag agent authored tests to track them separately and review before CI. [weak] [Currents](https://currents.dev/posts/reviewing-ai-generated-playwright-tests-before-they-reach-ci)
- Named flakiness sources in AI driven testing: nondeterministic LLM output, and retries abandoned because of token cost. [weak] [TestQuality](https://testquality.com/playwright-flaky-tests-diagnostic-playbook-2026/)

### Inferences
- Rule for a QA skill: agent explores live, then emits a script; the script (not the agent) is the regression asset; the script is reviewed like code and run in CI with no model in the loop.
- Self healing must not be allowed to silently change what a test asserts: a healer that "fixes" a locator can also hide a real regression (Playwright's healer skipping tests it believes reflect broken functionality is a case to review, not accept).
- Watch for values the agent copied from the live run (IDs, dates, prices) being frozen into assertions.

### Gaps
- No peer reviewed study found that quantifies repeatability of live agent runs vs generated scripts on the same suite.
- No sourced data found on Maestro specific AI generation (Maestro's own AI features were not researched this session).

## Risks and vendor recommended guards

### Takeaway
Prompt injection from page content is the dominant unsolved risk: vendor numbers fell from about 24% attack success (Claude for Chrome, Aug 2025, no mitigations) to about 1% or lower with layered defenses, but adaptive attackers with many attempts still succeed often, and independent researchers keep finding exploit chains. Vendors converge on the same guards: isolated VM or browser profile with no real credentials, site allowlists, human confirmation for consequential actions, and taking over manually for logins and payments.

### Cited Findings
- Claude for Chrome pilot (Aug 25, 2025): 123 test cases, 29 attack scenarios; attack success 23.6% without mitigations, 11.2% with; on 4 browser specific attack types, 35.7% to 0%. Mitigations: per site permissions, confirmation before publishing, purchasing or sharing personal data, blocked categories (financial services, adult, pirated content), classifiers for suspicious instructions. Dec 18, 2025: admins can set site allowlists and blocklists org wide. [strong] [Anthropic: Piloting Claude in Chrome](https://www.claude.com/blog/claude-for-chrome)
- Later Anthropic numbers: adaptive best of N (100 attempts per environment) 1.4% for Claude Opus 4.5 with safeguards vs 8.0% model alone; support page says current configuration keeps success below 0.08% on the internal suite but the risk is "non-zero". [medium; vendor self report] [Agentic Cyber Explorer summary](https://agentic-cyber-explorer.pages.dev/events/anthropic-browser-use-pi-mitigations-2025/); [Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)
- Independent: a frontier model benchmark found attack success rising with attempts, Claude Opus 4.5 from 4.7% at 1 attempt to 63% at 100; a University of Washington study (July 2026) of seven agentic browsers found four let attackers bypass same origin policy; a disclosed Claude in Chrome injection chain escalated to account takeover. [weak, aggregators, primary not verified] [cruxdigits](https://cruxdigits.nl/blog/ai-browser-agents-2026-security/); [nohacks](https://nohacks.co/blog/agentic-browser-landscape-2026); [Penligent on ShadowPrompt](https://www.penligent.ai/hackinglabs/claude-extension-prompt-injection-how-shadowprompt-turned-a-trusted-subdomain-into-a-browser-scale-risk/); [arXiv 2606.05233, 793 episode browser safety benchmark](https://arxiv.org/pdf/2606.05233)
- Google Gemini 2.5 Computer Use: an out of model, inference time per step safety service assesses each proposed action before execution; developers can require user confirmation for sensitive actions such as purchases or system level interactions. [medium] [Google blog](https://blog.google/technology/google-deepmind/gemini-computer-use-model/); [InfoQ](https://www.infoq.com/news/2025/10/gemini-computer-use)
- Anthropic computer use docs recommend: a dedicated VM or container with minimal privileges; no access to sensitive data such as account logins; limit internet access to an allowlist of domains; ask a human to confirm decisions with real world consequences (accepting cookies, financial transactions, agreeing to terms). [prior] [Anthropic computer use tool docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool)
- OpenAI Operator safeguards: takeover mode (user types credentials and payment details themselves), confirmation before significant actions, watch mode on sensitive sites (pauses if the user leaves the tab), refusal of high risk tasks, prompt injection monitor. [prior] [OpenAI: Introducing Operator](https://openai.com/index/introducing-operator/)
- Chrome DevTools MCP collects usage telemetry by default, a data handling point for testing internal apps. [medium] [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- Cost and latency: Gemini Computer Use about 225 s per Online-Mind2Web task; a Playwright MCP session about 114k tokens; step by step LLM Android testers spend 60 to 70% of wall time blocked on the model. [medium] [Google blog](https://blog.google/technology/google-deepmind/gemini-computer-use-model/); [TestDino](https://testdino.com/blog/playwright-mcp); [LLMDroid](https://dl.acm.org/doi/10.1145/3715763)

### Inferences
- Guards a QA skill should require before an agent drives a GUI: run against local, staging or a seeded test environment, never production with real customer data; fresh isolated browser profile or emulator with test only accounts; domain allowlist limited to the app under test; no real payment methods (use sandbox cards); explicit human confirmation before anything irreversible (delete, send email, publish, pay, change permissions); treat all page text as untrusted data, never as instructions; record a trace (Playwright trace, video) of every agent session for review.
- Destructive clicks are most likely on admin UIs and anything with bulk actions; seed data should be disposable and resettable between runs.
- Since attack success climbs with attempts, a long unattended exploratory session on pages containing user generated content (comments, emails, tickets) is the highest risk configuration.

### Gaps
- Primary sources for the UW agentic browser study and the 4.7% to 63% repeated attempt figure were not fetched; treat as unverified.
- Could not re-fetch OpenAI Operator and Anthropic computer use docs this session; their guard lists are from prior knowledge of those pages.
- No quantitative data found on how often testing agents perform unintended destructive actions in practice.
