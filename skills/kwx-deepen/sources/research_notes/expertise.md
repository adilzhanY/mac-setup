# Research notes: how experts differ from novices, and how to make an agent think like the expert

Scope: expertise research, problem framing, how experts check their work, typical amateur mistakes, and what the LLM literature says about "act as an expert" prompting. Every claim is tied to a source. Where a detail was confirmed only through secondary summaries, or comes from reading the book rather than a page checked for these notes, it says so. Full citations are in `../books-and-papers.md` under "Expertise".

Verification marks used below:
- (checked) the claim was confirmed against the primary page, abstract or full text while writing these notes.
- (secondary) confirmed only through summaries or reviews of the source.
- (book) from the book itself, not re-checked online for these notes. Verify wording before quoting.

---

## 1. How experts differ from novices

### 1.1 Experts see deep structure, novices see surface features

- Chi, Feltovich and Glaser (1981), "Categorization and representation of physics problems by experts and novices", Cognitive Science 5(2), 121-152. Asked to sort physics problems, experts grouped them by the underlying principle (conservation of energy, Newton's second law), novices by the literal objects in the problem (inclined planes, springs). Experts "initially abstract physics principles" to build a problem representation, novices rely on the problem's literal features. (checked, via the abstract and the DTIC technical report: https://apps.dtic.mil/sti/pdfs/ADA100301.pdf)
- Glaser and Chi (1988), overview chapter in Chi, Glaser and Farr (eds.), The Nature of Expertise, Erlbaum. Gives a seven point list of expert traits that is still widely used. Items confirmed for these notes: expertise is domain bound; experts perceive large meaningful patterns; they represent problems at a deeper, principled level; and they "spend a great deal of time analyzing a problem qualitatively" before acting. (secondary for the exact list; the self monitoring item is commonly cited but was not confirmed here)
- Larkin, McDermott, Simon and Simon (1980), "Expert and novice performance in solving physics problems", Science 208(4450), 1335-1342. Experts reason forward from the givens to the unknown, novices start from the unknown and hunt backward for an equation that contains it. Expert knowledge is indexed by patterns that trigger the right action. (secondary, via the CogSci summary at https://www.jimdavies.org/summaries/larkin1980.html)
- Chase and Simon (1973), "Perception in chess", Cognitive Psychology 4(1), 55-81, building on de Groot. Masters recall real game positions far better than weaker players, but the advantage largely disappears on random positions. The edge is not a bigger memory but larger meaningful "chunks" learned from experience. (secondary; later critique: Linhares and Freitas 2010)

What this gives the skill: the first thing an expert does differently is not working harder, it is seeing a different problem. A request described in surface terms ("make a landing page", "write a migration") hides a deep type ("persuade a skeptical buyer", "change a live schema without losing data"). Naming the deep type is what lets the right methods come to mind.

### 1.2 Mental representations and deliberate practice

- Ericsson, Krampe and Tesch-Romer (1993), "The role of deliberate practice in the acquisition of expert performance", Psychological Review 100(3), 363-406. Expert performance is the result of years of practice designed to improve specific weaknesses, with feedback, not of talent alone. The top violinists had accumulated far more solitary deliberate practice than less accomplished peers. (checked, via review in PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC6731745/)
- Ericsson and Pool (2016), Peak: Secrets from the New Science of Expertise, Houghton Mifflin Harcourt. Argues that what sets experts apart is the quality and quantity of their mental representations: internal models of the domain that let them see patterns, predict what comes next, plan, and notice their own errors. (secondary, via the book's summaries; exact quote not confirmed)
- Caveat. Macnamara, Hambrick and Oswald (2014), "Deliberate practice and performance in music, games, sports, education, and professions: a meta-analysis", Psychological Science 25(8), 1608-1618: practice explains about 26% of variance in games, 21% in music, 18% in sports, 4% in education, under 1% in professions. (secondary for the per domain figures) Practice matters but is not the whole story, and in professional work it explains little.

What this gives the skill: an agent cannot practice for ten years, but it can borrow the expert's representation: the model of what matters, what usually goes wrong, and what a good result looks like. Step 1 and step 2 are a way to load that representation before acting. The professions caveat is a warning that "has done this for years" is a weak signal by itself. The skill should name experts whose field gives them feedback (see 1.5).

### 1.3 Recognition primed decisions and the cues experts notice

- Klein, Calderwood and Clinton-Cirocco (1986), "Rapid decision making on the fire ground", Proceedings of the Human Factors Society 30, 576-580. Experienced fireground commanders rarely compared options. They recognized the situation as a typical case, which brought with it plausible goals, cues to watch, expectations and a workable action, then checked that action by imagining it play out. Later work by the same group: fewer than 12% of critical decision points showed any comparison of alternatives. (checked, abstract; technical report: https://apps.dtic.mil/sti/pdfs/ADA199492.pdf)
- Klein (1998), Sources of Power: How People Make Decisions, MIT Press. Experts spend most of their effort on situation assessment, not on choosing between options; once the situation is read correctly the action is often obvious. They mentally simulate a candidate action to find where it breaks. (secondary) Klein also stresses that experts notice what is missing, the expected cue that did not appear. (book)
- Klein, Calderwood and MacGregor (1989), "Critical decision method for eliciting knowledge", IEEE Transactions on Systems, Man, and Cybernetics 19(3), 462-472. A structured interview that pulls tacit expertise out of real, non routine incidents with probes about the cues noticed, the basis for discriminations, typicality judgments, analogies the expert was reminded of, goals, options, and "what if" variations. (checked for scope; exact probe wording from the paper's probe table is book level, verify before quoting. Method page: https://www.gary-klein.com/cdm)

What this gives the skill: the useful questions to ask an imagined expert are the Critical Decision Method probes. Not "what would you do?" but "what would you look at first, what would tell you this is not the usual case, what does a novice miss here, what would make you change course?"

### 1.4 Dreyfus: rules first, situations later

- Dreyfus and Dreyfus (1980), "A five-stage model of the mental activities involved in directed skill acquisition", ORC 80-2, UC Berkeley Operations Research Center, for the US Air Force. Learners move from following context free rules (novice), through recognizing situational aspects, to choosing a plan and taking responsibility for it (competent), to seeing the situation as a whole (proficient), to acting fluidly from experience (expert). (checked: https://apps.dtic.mil/sti/pdfs/ADA084551.pdf, stage names vary between editions)

What this gives the skill: a novice version of a task applies the generic rule list. An expert version starts from "what kind of situation is this?" and lets that decide which rules apply. Step 2 should produce situation specific moves, not a generic best practices list.

### 1.5 When expert intuition can be trusted

- Kahneman and Klein (2009), "Conditions for intuitive expertise: a failure to disagree", American Psychologist 64(6), 515-526. Intuition is trustworthy only when (a) the environment is regular enough to be predictable and (b) the person had prolonged practice with fast, clear feedback to learn those regularities. "Subjective experience is not a reliable indicator of judgment accuracy." (checked: https://pubmed.ncbi.nlm.nih.gov/19739881/)
- Kahneman and Klein interview, "Strategic decisions: When can you trust your gut?", McKinsey Quarterly, March 2010. Kahneman: experts "will feel confident regardless of how well grounded it is in reality" and "experts don't know exactly where the boundaries of their expertise are". Klein: "You need strategies that help rule things out." (checked)

What this gives the skill: in step 1, prefer experts from fields with fast, unambiguous feedback (a structural engineer whose bridges stand or fall, a site reliability engineer who sees the outage) over fields where feedback is slow or absent (long range forecasting, many strategy roles). In step 5, the imagined expert's confidence is never the check. An agent playing an expert inherits the same problem: it will sound sure regardless.

### 1.6 Experts spend longer on the problem before solving it

- Glaser and Chi (1988), as above: experts spend relatively more time on qualitative analysis of the problem. (secondary)
- Schoenfeld (1985), Mathematical Problem Solving, Academic Press. Novices read a problem, pick an approach quickly and pursue it to the end even when it is failing. Experts spend more time analyzing and planning, and keep monitoring ("control") whether the approach is working, abandoning it when it is not. (secondary for the framework; the time-line graph detail is book level)
- Getzels and Csikszentmihalyi (1976), The Creative Vision: A Longitudinal Study of Problem Finding in Art, Wiley. Art students who explored more objects and kept the problem open longer before committing produced work judged more original, and were more successful years later. (secondary; follow-up intervals differ across accounts)
- Wedell-Wedellsborg (2017), "Are you solving the right problems?", Harvard Business Review, Jan-Feb 2017. Managers are good at solving problems but poor at diagnosing which problem to solve. Example: tenants complain the elevator is slow; the expensive fix is a faster elevator; the reframe is that waiting is boring, and mirrors next to the elevator cut complaints. (checked for the framing; the survey percentage differs across sources, do not quote it)

### 1.7 Experts go to the raw material and check where it came from

- Wineburg (1991), "Historical problem solving: a study of the cognitive processes used in the evaluation of documentary and pictorial evidence", Journal of Educational Psychology 83(1), 73-87. Historians and top high school students read the same documents about the Battle of Lexington. Historians used three heuristics the students did not: sourcing (who wrote this, when, why), contextualization (place it in its time), and corroboration (check it against other documents). Students treated a textbook passage as the most trustworthy source; historians treated it as the least. (secondary for the full text; the three heuristics are confirmed)
- Wineburg and McGrew (2017), "Lateral reading: reading less and learning more when evaluating digital information", Stanford History Education Group Working Paper 2017-A1 (shorter version in Teachers College Record 121, 2019). Ten professional fact checkers, ten PhD historians and 25 Stanford undergraduates judged live websites. Fact checkers left the site almost immediately and opened new tabs to see what others said about the source. They reached better conclusions in a fraction of the time. Historians and students read vertically and were fooled by logos and domain names. (checked: https://news.stanford.edu/stories/2017/10/fact-checkers-outperform-historians-evaluating-online-information)
- Simkin and Roychowdhury (2003), "Read before you cite!", Complex Systems 14(3), 269-274. From how misprints in references propagate, they estimate only about 20% of people who cite a paper have read it. (checked: https://arxiv.org/abs/cond-mat/0212043)

What this gives the skill: step 3 is backed by direct evidence. Experts start from the primary record (the document, the log, the data, the source code, the contract), not from someone's summary, and they judge a source by leaving it and checking what independent sources say about it. Summaries carry errors forward silently.

---

## 2. Problem framing

- Polya (1945), How to Solve It, Princeton University Press. Four phases: understand the problem (What is the unknown? What are the data? What is the condition? Can you restate it?), devise a plan (Do you know a related problem? Can you solve a simpler or special case? Can you work backward from the goal?), carry out the plan (check each step), look back (Can you check the result? Can you derive it differently? Can you use the method for some other problem?). (checked, via https://en.wikipedia.org/wiki/How_to_Solve_It; exact question wording is book level)
- First principles. Aristotle, Physics I.1 and Posterior Analytics: knowledge of a thing comes from knowing its first principles and causes. In practice: strip a problem to the facts and constraints that cannot be reduced further, and rebuild from there instead of reasoning by analogy to how it is usually done. (book)
- "What would have to be true?" Lafley and Martin (2013), Playing to Win: How Strategy Really Works, Harvard Business Review Press. For each option, list the conditions that would have to hold for it to be right, find the ones least likely to hold, and test those first. Moves the discussion from advocacy to testing. (secondary)
- The goal behind the request. The XY problem: someone wants X, decides Y is the way, and asks only about Y. The helper solves Y well and X stays unsolved. Canonical write ups: https://xyproblem.info and the Stack Exchange meta post "What is the XY problem?" (checked via https://en.wikipedia.org/wiki/XY_problem)
- Jobs to be done. Christensen, Hall, Dillon and Duncan (2016), "Know your customers' jobs to be done", Harvard Business Review, September 2016; book version Competing Against Luck (2016). People "hire" a product to make progress in a specific circumstance. The milkshake study: morning buyers hired a milkshake for a long boring commute, which no flavor tweak would have revealed. (secondary)
- The AI analogue of framing. Zheng, Mishra et al. (2023), "Take a step back: evoking reasoning via abstraction in large language models", arXiv 2310.06117 (Google DeepMind, ICLR 2024). Asking the model first for the general principle or concept behind a question, then answering from it, beat chain of thought by up to 36% on some benchmarks (for PaLM-2L: +7% MMLU physics, +11% chemistry, +27% TimeQA). Most remaining errors were in reasoning, not in the abstraction step, which models did well. (checked)

---

## 3. How experts check their own work

- Pre-mortem. Klein (2007), "Performing a project premortem", Harvard Business Review 85(9), 18-19. Before starting, tell the team the project has failed, then everyone writes down why it failed. Unlike "what might go wrong", it assumes failure, which makes dissent safe and specific. Klein: "a sneaky way to get people to do contrarian, devil's advocate thinking without encountering resistance." Kahneman: "a low-cost, high-payoff kind of thing" (both McKinsey Quarterly 2010, checked). Basis: Mitchell, Russo and Pennington (1989), "Back to the future: temporal perspective in the explanation of events", Journal of Behavioral Decision Making 2(1), 25-38. People who imagine an outcome has already happened generate more and more concrete explanations for it. The often quoted "30% better" figure is not confirmed in the original paper; do not quote it.
- Red teaming. UK Ministry of Defence, Development, Concepts and Doctrine Centre (2021), Red Teaming Handbook, 3rd edition. Structured techniques (key assumptions check, alternative futures, devil's advocacy, pre-mortem, outside in thinking) run by people separate from the plan's authors, to challenge it before reality does. (checked: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- Checklists. Gawande (2009), The Checklist Manifesto, Metropolitan Books. Checklists do not replace expertise, they catch the "killer items" that skilled people still skip under pressure (term from Boeing's Dan Boorman). Keep them short (about five to nine items), at a defined pause point, either read-do or do-confirm. (secondary) Evidence: Haynes et al. (2009), "A surgical safety checklist to reduce morbidity and mortality in a global population", New England Journal of Medicine 360(5), 491-499. Eight hospitals, 7,688 patients, a 19 item checklist: deaths fell from 1.5% to 0.8%, major complications from 11% to 7%. Before and after design, not randomized. (checked: https://pubmed.ncbi.nlm.nih.gov/19144931/)
- Back of the envelope. Tetlock and Gardner (2015), Superforecasting: The Art and Science of Prediction, Crown. The "Ten commandments for aspiring superforecasters" include: break seemingly intractable problems into tractable sub-problems (Fermi-ize), and balance inside and outside views. (checked: https://goodjudgment.com/philip-tetlocks-10-commandments-of-superforecasting/) Weinstein and Adam (2008), Guesstimation, Princeton University Press, teach order of magnitude estimates as a sanity check on any number. (book)
- Outside view. Lovallo and Kahneman (2003), "Delusions of success: how optimism undermines executives' decisions", Harvard Business Review 81(7), 56-63. Planners take the inside view (this project's details) and are too optimistic. The fix: pick a reference class of similar past cases, look at its distribution of outcomes, and adjust from there. (secondary) Also Kahneman (2011), Thinking, Fast and Slow, chapter 23. (book)
- Independent judgments. Kahneman, Sibony and Sunstein (2021), Noise: A Flaw in Human Judgment, Little, Brown. "Decision hygiene": get judgments independently before they are discussed, because once people see each other's views the errors become correlated and averaging no longer cancels them. (book)
- Triangulation. Denzin (1970, 2nd ed. 1978), The Research Act, Aldine. Confirm a finding through different data sources, different investigators, different theories, or different methods. Agreement between methods that fail in different ways is the strong evidence. (secondary)
- Not fooling yourself. Feynman (1974), "Cargo cult science", Caltech commencement address, Engineering and Science 37(7). "The first principle is that you must not fool yourself, and you are the easiest person to fool." Report everything that could make the result invalid, "a kind of leaning over backwards". (checked: https://calteches.library.caltech.edu/51/2/CargoCult.htm)
- The same holds for language models. Huang et al. (2023), "Large language models cannot self-correct reasoning yet", arXiv 2310.01798, ICLR 2024. Without external feedback, asking a model to review its own reasoning often does not help and sometimes makes answers worse, because it cannot reliably judge its own correctness. (checked) Dhuliawala et al. (2023), "Chain-of-verification reduces hallucination in large language models", arXiv 2309.11495, Findings of ACL 2024. Planning specific verification questions and answering each one independently of the draft (so the draft cannot bias the answer) reduced hallucinated facts. (checked)

What this gives the skill: step 5 must name a check that does not route through the author's or the requester's judgment: a test that can fail, a measurement, an independent source, a reference class, a pre-mortem list, a domain checklist. "I reviewed it and it looks right" is exactly what Huang et al. found to be unreliable.

---

## 4. Typical amateur mistakes, as a general category

Each one is the mirror image of an expert habit above.

1. Solving the stated problem instead of the real one. The XY problem; the slow elevator (Wedell-Wedellsborg 2017); the milkshake (Christensen et al. 2016). Novices jump to solution mode (Schoenfeld 1985).
2. Classifying by surface features. The request's nouns decide the approach instead of its deep type (Chi et al. 1981; Larkin et al. 1980).
3. Starting from digested summaries. Students trust the textbook over the documents (Wineburg 1991); most citers never read the cited paper (Simkin and Roychowdhury 2003); readers judge a site by its own look instead of reading laterally (Wineburg and McGrew 2017).
4. Generic rules instead of situational judgment. Applying the context free rule list (Dreyfus and Dreyfus 1980).
5. Committing early and not monitoring. Pursuing the first approach to the end even when it is failing (Schoenfeld 1985).
6. No independent check, or a check that is just confidence. Confidence does not track accuracy (Kahneman and Klein 2009); models cannot reliably self-correct without outside signal (Huang et al. 2023).
7. Inside view only. Plans built from the case's own details, too optimistic (Lovallo and Kahneman 2003).
8. Over-scoping. Doing more instead of doing it better. Anthropic's prompting guide notes that recent models "tend to overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested" and recommends: "Only make changes that are directly requested or clearly necessary." (checked: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) The checklist literature points the same way: the value is in a few killer items, not in long lists (Gawande 2009).

---

## 5. Making "name the expert" work for an AI

What the evidence says about persona prompting:

- Generic personas do little for factual accuracy. Zheng, Pei and Jurgens (2023, revised 2024), "When 'A helpful assistant' is not really helpful: personas in system prompts do not improve performances of large language models", arXiv 2311.10054. 162 roles, 2,410 factual questions: adding a persona did not improve performance over no persona on average. The best persona for each question did help, but choosing it automatically was hard. Note: version 1 of this paper reported the opposite; cite version 3. (checked)
- Personas can hurt. Kim, Yang and Jung (2024), "Persona is a double-edged sword: mitigating the negative impact of role-playing prompts in zero-shot reasoning tasks", arXiv 2408.08631. Role prompts lowered accuracy on several of twelve reasoning datasets. Running a persona solver and a neutral solver and letting an evaluator pick improved results. LLM generated personas were more stable than handcrafted ones. (secondary for the numbers)
- Domain fit matters. Salewski et al. (2023), "In-context impersonation reveals large language models' strengths and biases", NeurIPS 2023, arXiv 2305.14930. Models impersonating a domain expert did better than when impersonating a non expert in that domain; impersonation also carried social biases. (checked)
- Detailed, task specific expert descriptions help on open ended tasks. Xu et al. (2023), "ExpertPrompting: instructing large language models to be distinguished experts", arXiv 2305.14688. The model first writes a detailed description of the ideal expert for this exact instruction, then answers as that expert. Answers were judged better than vanilla answers (by GPT-4, not by humans). (checked)
- Role play can act as an implicit reasoning trigger. Kong et al. (2023), "Better zero-shot reasoning with role-play prompting", arXiv 2308.07702, NAACL 2024. Role play prompts beat standard zero shot on most of twelve reasoning benchmarks, for example AQuA 53.5% to 63.8% on ChatGPT. (checked)
- Vendor guidance. Anthropic's prompting guide: setting a role "focuses Claude's behavior and tone for your use case", and explaining the motivation behind an instruction "can give Claude more information about your goals and help it deliver more targeted responses". (checked, same URL as above)

Synthesis. A bare label ("you are an expert designer") is close to useless and sometimes harmful. What works is a description specific enough to load a mental representation (1.2): what the expert's situation is, what they have seen go wrong, what they look at first. ExpertPrompting's gain comes from a detailed, instruction specific description; Salewski's from domain fit; the Jekyll and Hyde result says the persona's answer should still be checked against something neutral. The persona is a means to retrieve methods, cues and checks (steps 2, 4, 5), not a source of authority.

A specific expert has:
- Role and specialty, as narrow as the task: not "a security expert" but "an application security engineer who reviews OAuth and session handling in web apps".
- Experience in terms of situations, not just years: "has shipped and then debugged schema migrations on tables with hundreds of millions of rows". Kahneman and Klein (2009) say years only count where feedback was fast and clear, so name a field with feedback.
- What they are accountable for: what goes wrong for them personally if the result is wrong (the outage, the failed audit, the rejected paper). This points at the real goal.
- What they would refuse or push back on in the request as written.

Questions to ask the imagined expert (adapted from the Critical Decision Method probes, Klein et al. 1989, and Polya 1945):
1. What is this really? What type of problem is it underneath the wording? (deep structure, Chi et al. 1981)
2. What is the goal behind the request, and what would the requester be upset to find missing? (XY problem, jobs to be done)
3. What do you look at first, and what source do you trust for it? (cues, sourcing)
4. What would tell you this is not the usual case? (typicality, anomalies)
5. What does a beginner always get wrong here? (expert versus novice contrast)
6. Have you seen a case like this before, and how did it go? (analogues; reference class)
7. It is six months later and this failed. Why? (pre-mortem)
8. How would you know it worked, without asking the person who made it? (independent check)

---

## Implications for the skill

Step 1, name the specific expert.
- Name a person by role, narrow specialty and the kind of situations they have handled, not a title. One sentence, concrete enough that two readers would picture the same person.
- Prefer experts from fields with fast, clear feedback on exactly this kind of work (Kahneman and Klein 2009). If the field gives no feedback, say so and lean harder on step 5.
- Have the model write the description for this exact request rather than pick from a fixed menu (ExpertPrompting 2023; LLM generated personas were more stable, Kim et al. 2024).
- Treat the expert as a way to retrieve methods, cues and checks. Never cite "the expert would agree" as evidence (Zheng et al. 2023; Kim et al. 2024).

Step 2, what the expert would do that was not asked for.
- Start by naming the deep type of the problem, then the real goal behind the request (Chi et al. 1981; XY problem; Christensen et al. 2016).
- List situation specific moves, not generic best practice (Dreyfus and Dreyfus 1980). Each item should be something a novice in this exact situation would miss.
- Include what the expert would look at first and what would make them change course (Critical Decision Method probes).
- Run a quick pre-mortem: "this failed, why?" and turn the top causes into moves (Klein 2007).
- These are changes in depth, not added features. If an item makes the deliverable bigger, it belongs on the "not doing" list.

Step 3, the raw material, and go get it.
- Name the primary record the expert would open: the source code, the log, the dataset, the spec, the original paper, the contract, the user's actual words. Not a blog summary, not memory of how it usually works (Wineburg 1991; Simkin and Roychowdhury 2003).
- Actually fetch it before planning. For any secondary source, check it laterally: what do independent sources say about it? (Wineburg and McGrew 2017)
- Note who produced each source and why (sourcing, contextualization).

Step 4, concrete methods and tools.
- Name methods at the level of a procedure someone could follow, with the tool by name (the test runner, the profiler, the statistical test, the style guide), not "best practices".
- Include one sanity estimate where numbers are involved: a Fermi breakdown or a reference class figure (Tetlock and Gardner 2015; Lovallo and Kahneman 2003).
- Include the domain's short checklist of killer items, if one exists (Gawande 2009; Haynes et al. 2009).

Step 5, what proves it right, other than the author or the requester.
- The check must be able to fail and must not depend on the author's judgment: a test, a measurement, a reproduction, an independent source, a comparison to a reference class, a known correct example (Huang et al. 2023; Feynman 1974).
- Prefer two checks that fail in different ways (triangulation, Denzin 1970). When the agent checks a claim, it answers the check independently of its own draft (Dhuliawala et al. 2023; Kahneman et al. 2021).
- Write the check down before doing the work, so it cannot be bent to fit the result (pre-registration logic, Feynman 1974).
- If no external check exists, say so plainly instead of claiming confidence (Kahneman and Klein 2009).

Step 6, rewrite the task.
- The rewrite names the deep problem and the real goal, the raw material, the methods, and the check, in the same deliverable size as the original (Anthropic prompting guide on overengineering; Wedell-Wedellsborg 2017: reframing, not enlarging).
- The "not doing" list holds everything the expert would do that would grow the deliverable, plus anything outside the requester's goal. It is what keeps depth from turning into scope.
- Look back (Polya 1945): after the work, run the step 5 check and say what it showed.
