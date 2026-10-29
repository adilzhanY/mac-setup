# Cited research: what the sources really say

Every study, paper, book, report and reference page cited in the seven video notes in `sources/videos/`, chased back to the source (research done 2026-10-27). For each one: the citation, a legal URL, what the source actually found, its replication status, and what a UI designer may and may not conclude from it.

Access legend, used in every entry:

- **Full text read**: the PDF or full page was downloaded and read (with `pdftotext`).
- **Abstract only**: no legal full text was reachable; the abstract and reputable summaries were read.
- **Secondary only**: no primary source could be found or opened; only reputable secondary write-ups were read.
- **Background**: a classic used as context, not re-read for this file. Treat its numbers as "commonly reported".

Downloaded copies (untrusted data, kept out of the skill) sat in a scratch folder. No pirate site was used. Two author-hosted PDFs (Nunes and Drèze, Scheibehenne et al.) have since gone offline at their authors' university sites, so they were read from the Internet Archive's copy of those same author pages.

The companion file for designers is `psychology/research-evidence.md`.

## Contents

1. [Choice overload and defaults](#1-choice-overload-and-defaults)
2. [Progress: endowed progress and goal gradient](#2-progress-endowed-progress-and-goal-gradient)
3. [Ownership: IKEA effect and endowment effect](#3-ownership-ikea-effect-and-endowment-effect)
4. [Reciprocity and free samples](#4-reciprocity-and-free-samples)
5. [Loss aversion and loss framing](#5-loss-aversion-and-loss-framing)
6. [Contrast, anchoring and decoys](#6-contrast-anchoring-and-decoys)
7. [Aesthetics, fluency and premium perception](#7-aesthetics-fluency-and-premium-perception)
8. [Consistency](#8-consistency)
9. [Failure, recovery and bad experiences](#9-failure-recovery-and-bad-experiences)
10. [AI generated interfaces](#10-ai-generated-interfaces)
11. [Platform reference pages](#11-platform-reference-pages)
12. [Cited but not research](#12-cited-but-not-research)
13. [Access log](#13-access-log)

---

## 1. Choice overload and defaults

### 1.1 Iyengar and Lepper 2000, the jam study

- **Citation:** Iyengar, S. S., and Lepper, M. R. (2000). When choice is demotivating: Can one desire too much of a good thing? *Journal of Personality and Social Psychology*, 79(6), 995-1006. DOI 10.1037/0022-3514.79.6.995.
- **Legal URL:** University of Washington course copy, https://faculty.washington.edu/jdb/345/345%20Articles/Iyengar%20&%20Lepper%20(2000).pdf
- **Access:** Full text read.
- **Cited by:** 2TlIg3VokY8 ("Columbia jam study: 24 flavours 3% bought, 6 flavours 30% bought").
- **What it found:** Three studies. Study 1, an upscale grocery store (Draeger's, Menlo Park) on two Saturdays, a tasting booth of Wilkin and Sons jams showing either 6 or 24 flavours, rotated hourly, N = 502 passers-by. The big display drew more people: 60% (145 of 242) stopped at 24 jams versus 40% (104 of 260) at 6. People sampled the same amount (about 1.5 jams) at both. Of those who stopped, about 30% (31) bought jam after the 6 display versus 3% (4) after the 24 display. As a share of everyone who passed, that is about 12% versus 1.7%. Study 2: Stanford students offered an extra credit essay with 6 or 30 topics; 74% versus 60% handed it in, and essays were rated slightly better in the 6 group. Study 3: lab, Godiva chocolates, 6 or 30 to choose from; people in the 30 condition enjoyed choosing more but also found it harder, were less satisfied with the chocolate they picked, and only 12% (versus 48% with 6) took chocolates instead of cash as payment.
- **Replication and caveats:** The video's numbers are right but leave out that the 24 display attracted more people. The two Saturdays, a single store and a single brand make Study 1 a small field demonstration. Direct replications failed: Scheibehenne (2008) repeated the jam booth in a German supermarket and found no effect, Greifeneder (2008) found none with chocolates (both reported in 1.2). The meta-analyses in 1.2 and 1.3 show the effect is real only under specific conditions.
- **A designer may conclude:** large unsorted sets of similar, hard to compare options can stop people deciding, especially newcomers without a preference. A big set can still attract attention.
- **A designer may not conclude:** "6 options convert 10 times better than 24", or that any list above 6 hurts. The 10x figure is one booth on two days and did not replicate.

### 1.2 Scheibehenne, Greifeneder and Todd 2010, meta-analysis

- **Citation:** Scheibehenne, B., Greifeneder, R., and Todd, P. M. (2010). Can there ever be too many options? A meta-analytic review of choice overload. *Journal of Consumer Research*, 37(3), 409-425. DOI 10.1086/651235.
- **Legal URL:** author copy, https://abcwest.cogs.indiana.edu/pmwiki/pdf/scheibehenne.options.2010.pdf (now offline; read from the Internet Archive copy of that page). Record: https://edoc.unibas.ch/20586
- **Access:** Full text read.
- **What it found:** 63 conditions from 50 published and unpublished experiments, N = 5,036. Mean effect of choice overload D = 0.02 (95% CI -0.09 to 0.12), "virtually zero", with real heterogeneity (I² = 68%). Trimming the six highest and six lowest studies gave D = 0.001. People with expertise or clear prior preferences did better with more options (meta-regression coefficient -0.50, p = .013). A slight publication bias in favour of overload results. The paper reports the failed direct replications of the jam and chocolate studies.
- **Caveats:** Effect size averaging across very different tasks hides real conditional effects, which is the point Chernev et al. (1.3) make.
- **Designer conclusion:** "more options always hurt" is false. "More options sometimes hurt" is true. Experts and people who know what they want benefit from more choice.

### 1.3 Chernev, Böckenholt and Goodman 2015, meta-analysis

- **Citation:** Chernev, A., Böckenholt, U., and Goodman, J. (2015). Choice overload: A conceptual review and meta-analysis. *Journal of Consumer Psychology*, 25(2), 333-358. DOI 10.1016/j.jcps.2014.08.002.
- **Legal URL:** Kellogg listing with abstract, https://www.kellogg.northwestern.edu/faculty/research/detail/2015/when-product-assortment-leads-to-choice-overload-a-conceptual . The author PDF link on chernev.com no longer serves a PDF.
- **Access:** Abstract only.
- **What it found:** 99 observations, N = 7,202. Four factors make choice overload more likely: choice set complexity (for example no clear best option, many attributes), decision task difficulty (time pressure, effort), preference uncertainty (no prior preference or expertise), and a goal of minimising effort. When these moderators are present the effect of assortment size is significant, which the authors say contradicts the earlier near zero mean. Satisfaction or confidence, regret, deferral and switching all measure the effect about equally.
- **Designer conclusion:** cut or structure options when the options are hard to compare, the user is new or unsure, or the user wants to be done fast. Leave large catalogues alone when users know what they want, and help them with search, filters, sorting and a recommended pick instead of hiding items.

### 1.4 Johnson and Goldstein 2003, "Do defaults save lives?"

- **Citation:** Johnson, E. J., and Goldstein, D. G. (2003). Do defaults save lives? *Science*, 302(5649), 1338-1339. DOI 10.1126/science.1091721. Follow-up with the same data: Johnson, E. J., and Goldstein, D. G. (2004). Defaults and donation decisions. *Transplantation*, 78(12), 1713-1716.
- **Legal URL:** 2004 follow-up hosted by HODS, https://hods.org/pdf/Defaults%20and%20Donation%20Decisions.pdf . The Science paper is paywalled; no legal free copy was found.
- **Access:** 2003 abstract only; the 2004 follow-up was read, but its PDF is partly damaged, so only pages 3 to 4 could be extracted.
- **What it found:** Effective consent in European countries: four opt-in countries all well below six opt-out countries, "no overlap and nearly 60 percentage points" apart. Controlling for infrastructure, education and religion, an opt-out default went with a significant increase in actual deceased donations, from 14.1 to 16.4 per million (a 16.3% rise). An online survey (161 respondents) found agreement of about 42% with opt-in, 82% with opt-out and 79% when forced to choose with no default. The 42 and 82 figures come from summaries of the 2003 paper; the 79% neutral figure and "opt-out did not differ from neutral" were read in the 2004 paper.
- **Replication and caveats:** The gap in registered consent is huge; the gap in actual donations is much smaller (16%). Arshad, Anderson and Sharif (2019, *Kidney International* 96(6), 1453-1460; abstract only) compared opt-out and opt-in countries and found no significant difference in deceased donors per million between opt-out and opt-in (about 20.3 versus 15.4, p = .195), and fewer living donors in opt-out countries.
- **Designer conclusion:** defaults change what gets recorded far more than what people truly want or end up doing. A default does well when it matches what most people would pick anyway (the neutral 79% was close to the opt-out 82%).

### 1.5 Jachimowicz, Duncan, Weber and Johnson 2019, defaults meta-analysis

- **Citation:** Jachimowicz, J. M., Duncan, S., Weber, E. U., and Johnson, E. J. (2019). When and why defaults influence decisions: A meta-analysis of default effects. *Behavioural Public Policy*, 3(2), 159-186.
- **Legal URL:** open access (CC BY 4.0), https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0
- **Access:** Full text read (the first 100,000 characters of the article page, which hold the results).
- **What it found:** 58 datasets from 55 studies in 35 articles, pooled N = 73,675. Average effect d = 0.68 (95% CI 0.53 to 0.83), about a 27 percentage point increase in choosing the pre-selected option for yes or no outcomes. Very large spread: some studies show no effect or a backfire. Defaults worked better in consumer domains and worse for environmental choices. They worked better when the default reads as a recommendation (endorsement) or as what you already have (endowment); making the choice easier (ease) did not explain the effect. Trim-and-fill suggested missing studies with larger effects (corrected d = 0.80); Egger's test was not significant.
- **Designer conclusion:** defaults are one of the strongest tools available, and the video is right that people read them as recommendations. The size depends on context: a default that the user can see is self-serving loses much of its power.

### 1.6 Spool 2011, "Do users change their settings?"

- **Citation:** Spool, J. M. (2011, September 14). Do users change their settings? UIE Brain Sparks.
- **Legal URL:** https://archive.uie.com/brainsparks/2011/09/14/do-users-change-their-settings/
- **Access:** Full text read.
- **What it found:** In "the early days of PC computing", several hundred people mailed their Microsoft Word settings file. Less than 5% had changed any of the 150+ settings. Programmers and designers changed far more (often over 40%). Word's autosave was off by default by accident, so 95% ran without autosave.
- **Caveats:** An informal practitioner study of one app, with no year or sample details.
- **Why it is here:** It is the closest real source to the video's uncited "70 to 90% of users never change default values". The video's number has no source; the nearest evidence says more than 95% never change settings, while the meta-analysis in 1.5 says defaults shift choices by about 27 points on average when people actively decide. The two are different situations (ignored settings versus an active choice).

---

## 2. Progress: endowed progress and goal gradient

### 2.1 Nunes and Drèze 2006, the car wash cards

- **Citation:** Nunes, J. C., and Drèze, X. (2006). The endowed progress effect: How artificial advancement increases effort. *Journal of Consumer Research*, 32(4), 504-512.
- **Legal URL:** author copy at USC, https://msbfile03.usc.edu/digitalmeasures/jnunes/intellcont/Endowed%20Progress%20Effect-1.pdf (now offline; read from the Internet Archive copy of that page).
- **Access:** Full text read.
- **Cited by:** 2TlIg3VokY8, as the "Columbia car wash study". The authors were at USC and Wharton, not Columbia.
- **What it found:** Study 1, a car wash, 300 loyalty cards handed out over 9 months. Half needed 8 stamps (0 of 8 filled, 0% progress), half needed 10 with 2 pre-stamped (20% progress); both needed 8 paid washes. Completion was 34% versus 19%, and the endowed group came back 2.9 days sooner on average between washes, speeding up as they got closer. Study 3 (a hypothetical wine programme): the endowment worked best when a reason for the gift was given, and even a specious reason worked as well as a realistic one. When progress was counted in purchases with no reason given, the head start had little effect; counted in points, it worked without a reason.
- **Caveats:** One field site, a modest sample, and an effect measured on redemptions. Not a goal gradient study as the video labels it, though the two effects are related.
- **Designer conclusion:** framing a task as already started increases completion. A stated reason for the head start ("Your account is set up, that is step 1") makes it stronger.
- **Not:** that any fake progress number works. The progress has to be framed as real and has to stay honest (see `psychology/research-evidence.md`).

### 2.2 Kivetz, Urminsky and Zheng 2006, goal gradient

- **Citation:** Kivetz, R., Urminsky, O., and Zheng, Y. (2006). The goal-gradient hypothesis resurrected: Purchase acceleration, illusionary goal progress, and customer retention. *Journal of Marketing Research*, 43(1), 39-58.
- **Legal URL:** Columbia Business School copy (reprinted with AMA permission), https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf
- **Access:** Full text read.
- **What it found:** At the Columbia University café, members of a "buy 10, get 1 free" coffee programme bought coffee more often the closer they were to the reward; time between purchases fell by about 20% (0.7 days) from the start to the end of a card. A field experiment: a 12-stamp card with 2 "bonus" stamps was completed in 12.7 days on average versus 15.6 days for a plain 10-stamp card (medians 10 versus 15 days), about 20% faster. On a music rating site, users rated more songs per visit and visited more often as the reward neared. After earning the reward people slowed down again ("post-reward resetting"). Stronger acceleration predicted higher retention.
- **Caveats:** Effects are real but moderate (around 20% faster), measured in reward programmes.
- **Designer conclusion:** make the remaining distance visible and short; expect a slump right after a reward and design the next goal to start immediately.

---

## 3. Ownership: IKEA effect and endowment effect

### 3.1 Norton, Mochon and Ariely 2012, the IKEA effect

- **Citation:** Norton, M. I., Mochon, D., and Ariely, D. (2012). The IKEA effect: When labor leads to love. *Journal of Consumer Psychology*, 22(3), 453-460. DOI 10.1016/j.jcps.2011.08.002.
- **Legal URL:** Harvard DASH open access, https://dash.harvard.edu/handle/1/12136084
- **Access:** Full text read.
- **What it found:** Experiment 1 (students): people who assembled an IKEA storage box bid $0.78 for it versus $0.48 from people who got it pre-built, and liked it more. Origami: builders valued their frogs and cranes at $0.23, about five times what others would pay for them ($0.05), and nearly as much as others paid for expert made origami ($0.27). Lego: the effect vanished when people built and then destroyed their creation; it also vanished when they failed to finish. It held for people with and without a DIY habit.
- **Replication:** Sarstedt, Neubert and Barth (2017), "The IKEA effect: A conceptual replication", *Journal of Marketing Behavior* 2(4), 307-312 (abstract only), found the effect robust and pointed to psychological ownership as the mechanism.
- **Caveats:** Small student samples, cents-level valuations, simple objects. The effect needs successful completion.
- **Designer conclusion:** letting people build something small and finish it makes them value the result more. The task must end in a finished thing; an abandoned or failed setup creates no attachment.
- **Not:** that more effort always means more love. Failure and unfinished work erase it.

### 3.2 Kahneman, Knetsch and Thaler 1990, the endowment effect

- **Citation:** Kahneman, D., Knetsch, J. L., and Thaler, R. H. (1990). Experimental tests of the endowment effect and the Coase theorem. *Journal of Political Economy*, 98(6), 1325-1348.
- **Legal URL:** record, https://doi.org/10.1086/261737
- **Access:** Abstract only.
- **What it found:** People randomly given a coffee mug demand far more to sell it than others will pay to buy it; trading volume stays well below what theory predicts, even with repeated market rounds. Ratios of about two are commonly reported (background).
- **Caveats:** Background, not re-read: later work (for example Plott and Zeiler 2005) found the gap shrinks or disappears with careful elicitation procedures. Named in 2TlIg3VokY8 without a source.
- **Designer conclusion:** a feeling of ownership raises value; showing a user "your" workspace, file or plan before asking for sign up is reasonable.

---

## 4. Reciprocity and free samples

### 4.1 Cialdini, Influence, and the author's own pages

- **Citation:** Cialdini, R. B. *Influence: The Psychology of Persuasion* (1984, revised 2006, expanded 2021). Not free, not read. Author's own material read instead: Influence at Work, "Principles of persuasion", https://www.influenceatwork.com/7-principles-of-persuasion/ . Also: Cialdini, R. B. (2001). Harnessing the science of persuasion. *Harvard Business Review*, 79(9), https://hbr.org/2001/10/harnessing-the-science-of-persuasion (paywalled; only the summary could be read).
- **Access:** Secondary only for the book; the author's principles page read in full.
- **What it says:** People feel obliged to return a behaviour, gift or service received first. Cialdini's page reports the restaurant mint studies: one mint with the bill raised tips by about 3%, two mints by about 14%, and one mint followed by the waiter returning with "for you nice people, here's an extra mint" by 23%. The lesson he draws: be the first to give, and make the gift personal and unexpected. His principles are listed side by side (reciprocity, scarcity, authority, consistency, liking, social proof, unity), with no ranking.
- **Cited by:** 2TlIg3VokY8 says Cialdini "ranked reciprocity as the single most powerful driver of behaviour". Nothing in the author's own material ranks it first.
- **Underlying study:** Strohmetz, D. B., Rind, B., Fisher, R., and Lynn, M. (2002). Sweetening the till: The use of candy to increase restaurant tipping. *Journal of Applied Social Psychology*, 32(2), 300-309 (abstract only). Two experiments: a small chocolate with the bill raised tips; tips varied with the amount and the way it was offered; the authors argue reciprocity explains it better than mood or impression management. A related study by Rind and Strohmetz found no effect of its reciprocity manipulation (secondary report), so the effect is not universal.
- **Designer conclusion:** give real value first, unexpectedly and personally (a result, a useful free tier), then ask. The size of the mint numbers is specific to tipping.

### 4.2 "Free samples increase purchases by up to 2,000%"

- **Claim in:** 2TlIg3VokY8, no source.
- **Access:** Secondary only. No primary study was found.
- **What exists:** The figure appears in a 2014 *Atlantic* article on Costco samples (could not be opened) and in many blogs that quote one another; one attributes it to a single Marsh Supermarkets result. Interactions, the firm that runs Costco's demos, is quoted with 600% for one frozen pizza sample and an average 71% for beer (secondary). Costco has never published sample figures. The peer reviewed evidence (Dotson, Chandukala and Liu, BYU, *Journal of Retailing*; university release read at https://news.byu.edu/news/study-free-samples-increase-sales-work-better-end-aisle-promotions ) shows sampling lifts snack sales for weeks and beats end-of-aisle displays, but gives no headline percentage.
- **Designer conclusion:** sampling works. "2,000%" is an outlier anecdote and should never be quoted.

---

## 5. Loss aversion and loss framing

### 5.1 Kahneman and Tversky 1979, prospect theory

- **Citation:** Kahneman, D., and Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.
- **Legal URL:** Princeton (Kahneman's page; personal or classroom use), https://kahneman.scholar.princeton.edu/document/11 . Nobel citation: https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/facts/
- **Access:** Abstract only (the Princeton link did not return a PDF to a script).
- **What it says:** The value function is concave for gains, convex for losses and steeper for losses. The "about twice" figure comes from the later cumulative prospect theory paper, Tversky and Kahneman (1992), whose median loss aversion coefficient was 2.25 (confirmed in Brown et al., 5.2). Kahneman received the 2002 economics prize (shared with Vernon Smith); Tversky had died in 1996, so the work is joint, not Kahneman's alone.

### 5.2 Brown, Imai, Vieider and Camerer 2024, loss aversion meta-analysis

- **Citation:** Brown, A. L., Imai, T., Vieider, F. M., and Camerer, C. F. (2024). Meta-analysis of empirical estimates of loss aversion. *Journal of Economic Literature*, 62(2), 485-516. DOI 10.1257/jel.20221698.
- **Legal URL:** working paper version, https://epub.ub.uni-muenchen.de/75121/1/275.pdf
- **Access:** Full text read (2021 working paper).
- **What it found:** 607 estimates from 150 articles. Mean loss aversion coefficient between 1.8 and 2.1 (published: 1.955, interval 1.82 to 2.10). The distribution is skewed: the median is 1.69. Estimates vary with study design.
- **Caveat:** Almost all of this is about money gambles and riskless trades, not about how a headline is worded.

### 5.3 Gal and Rucker 2018, the critique

- **Citation:** Gal, D., and Rucker, D. D. (2018). The loss of loss aversion: Will it loom larger than its gain? *Journal of Consumer Psychology*, 28(3), 497-516. DOI 10.1002/jcpy.1047.
- **Legal URL:** working paper record, https://papers.ssrn.com/abstract=3049660
- **Access:** Abstract only.
- **What it says:** The authors argue the evidence does not show that losses are, on balance, more impactful than gains, and that the impact depends on context. A shorter opinion piece in the same direction: Mukherjee (2019), "Revise the belief in loss aversion", *Frontiers in Psychology* 10:2723 (open access, read).
- **Designer conclusion from 5.1 to 5.3:** losses usually weigh more than equal gains in choices about money, by a factor near 2. It is not a law that applies to every message.

### 5.4 O'Keefe and Jensen 2007 and 2009, gain versus loss framed messages

- **Citation:** O'Keefe, D. J., and Jensen, J. D. (2007). The relative persuasiveness of gain-framed and loss-framed messages for encouraging disease prevention behaviors: A meta-analytic review. *Journal of Health Communication*, 12(7), 623-644. And O'Keefe and Jensen (2009), the same question for disease detection, *Journal of Communication*, 59(2), 296-316.
- **Access:** Abstract only.
- **What it found:** 93 studies, N = 21,656: gain-framed messages were very slightly more persuasive (r = .03), almost all from dental hygiene; no difference for safer sex, skin cancer or diet messages. For detection behaviours (53 studies), loss-framed messages had a tiny edge (r = -.04), only for breast cancer screening. A charity advertising meta-analysis (27 studies) found no difference (r = .002, secondary).
- **Why it matters:** The video's rule "don't sell what they'll gain, show what they'll lose" is a message framing rule. Message framing meta-analyses show loss framing is not reliably more persuasive.

---

## 6. Contrast, anchoring and decoys

Cited in 2TlIg3VokY8 without sources (AppleCare+ example, $90 Wagyu next to $40 salmon, real estate agents showing an overpriced house first).

### 6.1 Anchoring and relative thinking (background)

- **Tversky, A., and Kahneman, D. (1974).** Judgment under uncertainty: Heuristics and biases. *Science*, 185, 1124-1131. Arbitrary numbers bias later estimates. Background.
- **Tversky, A., and Kahneman, D. (1981).** The framing of decisions and the psychology of choice. *Science*, 211, 453-458. The "jacket and calculator" problem: people will travel to save $5 on a $15 item but not on a $125 item. This is the real mechanism behind the video's "Just 2.6%" label. Background.
- **Northcraft, G. B., and Neale, M. A. (1987).** Experts, amateurs, and real estate: An anchoring-and-adjustment perspective on property pricing decisions. *Organizational Behavior and Human Decision Processes*, 39, 84-97. Abstract not available. As commonly reported (background): estate agents' value estimates moved with the listed price they were given, and most denied using it. This supports the real estate example in a lab setting; it does not show agents use the trick deliberately.

### 6.2 Decoys in real choices

- **Huber, J., Payne, J. W., and Puto, C. (1982).** Adding asymmetrically dominated alternatives. *Journal of Consumer Research*, 9, 90-98. The original attraction (decoy) effect. Background.
- **Trendl, A., Stewart, N., and Mullett, T. L. (2021).** A zero attraction effect in naturalistic choice. *Decision*, 8(1), 55-68. Legal URL: https://wrap.warwick.ac.uk/id/eprint/143538/ . Full text read. With movie choices built to meet Huber and colleagues' own criteria, the attraction effect was "precisely zero". It follows Frederick, Lee and Baskin (2014), who reported the effect mostly appears with numeric attributes on paper and not with real products.
- **Designer conclusion:** the order and context of prices really do shape judgement (anchoring and relative thinking are among the best replicated effects in the field). A dominated decoy plan added "to make the middle plan look good" is far less reliable than the folklore says.

---

## 7. Aesthetics, fluency and premium perception

### 7.1 Reber, Schwarz and Winkielman 2004, processing fluency

- **Citation:** Reber, R., Schwarz, N., and Winkielman, P. (2004). Processing fluency and aesthetic pleasure: Is beauty in the perceiver's processing experience? *Personality and Social Psychology Review*, 8(4), 364-382.
- **Legal URL:** Winkielman's UCSD page, https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf ; also University of Bergen, https://bora.uib.no/bora-xmlui/bitstream/handle/1956/594/BORA_PSPR04.pdf
- **Access:** Full text read.
- **What it says:** A theory and review paper, not a single experiment. The more fluently a perceiver processes an object, the more positive the aesthetic response. Symmetry, figure-ground contrast, clarity, repetition, prototypicality and priming all raise fluency and liking. The effect is moderated by expectations and attribution: when people attribute the ease to an irrelevant source, the boost disappears. Fluency feels best when it is unexpected; experts and art trained viewers also value some complexity and novelty.
- **Cited by:** 8EAYZe6y3I8 ("what is easy to take in is judged more kindly"). The note's extension, "every 'did the tap work?' is processing effort that lowers the judgement", goes beyond the paper: it is about perceiving stimuli, not about interaction feedback. The extension is plausible but untested there.
- **Designer conclusion:** clear contrast, symmetry or strong alignment, familiar patterns and legible type make an interface look better as well as read faster.

### 7.2 Reimann et al. 2010, aesthetic package design

- **Citation:** Reimann, M., Zaichkowsky, J., Neuhaus, C., Bender, T., and Weber, B. (2010). Aesthetic package design: A behavioral, neural, and psychological investigation. *Journal of Consumer Psychology*, 20(4), 431-441.
- **Legal URL:** Sapienza University of Rome course page, https://elearning.uniroma1.it/mod/resource/view.php?id=31991 ; record, https://experts.arizona.edu/en/publications/aesthetic-package-design-a-behavioral-neural-and-psychological-in/
- **Access:** Full text read.
- **What it found:** Four experiments with pictures of grocery packages, pre-sorted as "aesthetic" or "standardized". Experiment 1a: aesthetic packages chosen 69% versus 57% of the time, with slower choices. 1b (82 graduate students, within subjects): 73% versus 54%. Experiment 2 (176 respondents, brand and price varied): an aesthetic package of an unknown brand was chosen 51% of the time at a high price, more than a well-known brand in standard packaging at the high price (42%). Experiment 3 (fMRI, 17 people): aesthetic packages raised activity in the nucleus accumbens and ventromedial prefrontal cortex, regions tied to reward.
- **Caveats:** Hypothetical yes or no choices on images, not purchases. Small samples, especially the brain imaging study. "Aesthetic" was defined by a pretest, so it is a mix of qualities.
- **Designer conclusion:** looks win attention and the first pick, even against a known brand and a higher price. It does not show that looks alone keep customers.

### 7.3 Pombo and Velasco 2021, brand premiumness

- **Citation:** Pombo, M., and Velasco, C. (2021). How aesthetic features convey the concept of brand premiumness. *Psychology and Marketing*. DOI 10.1002/mar.21534.
- **Legal URL:** open access (CC BY), https://doi.org/10.1002/mar.21534 ; preprint on OSF, https://osf.io/7kpwz ; BI repository, https://hdl.handle.net/11250/3041133
- **Access:** Full text read (the OSF preprint; the published version adds experiments, read as abstract).
- **What it found:** Orange juice and strawberry jam packages, online participants (Prolific), roughly 90 to 180 per experiment, two exploratory and four preregistered experiments plus four more with a second product. Quality was manipulated through a label claim ("Freshly squeezed, 100% orange juice" versus "Orange flavoured, 30% orange juice"). Quality drove both preference and premiumness strongly. Symmetry and curvature both affected preference, but only symmetry affected premiumness, and in orange juice only in the low quality condition (for jam it was a main effect). The authors conclude the link between aesthetics and premiumness is product specific.
- **Designer conclusion:** evidence of quality is what makes something read as premium; aesthetics add to it, unevenly. This supports the video's thesis in spirit, but it is a packaging study, not an app study.

---

## 8. Consistency

### 8.1 Petrie, Papadofragkakis, Power and Swallow 2009, the York study

- **Citation:** Petrie, H., Papadofragkakis, G., Power, C., and Swallow, D. (2009). Navigational consistency in websites: What does it mean to users? In *Human-Computer Interaction: INTERACT 2009*, LNCS 5727, 423-427. Springer. DOI 10.1007/978-3-642-03655-2_46.
- **Legal URL:** listed by Unpaywall as a free publisher PDF, https://link.springer.com/content/pdf/10.1007/978-3-642-03655-2_46.pdf , but Springer's login redirect blocked every scripted request.
- **Access:** Not read. No abstract was retrievable either. The numbers below are those shown on screen in 8EAYZe6y3I8.
- **What the video reports:** Mid task, a site's navigation moved from left to right. Time on that page rose from 1.9 s to 6.8 s and on following pages from 2.2 s to 6.2 s. 85.7% noticed the position change, 42.9% a font size change, 21.4% font type and order changes; perceived impact was rated low (2.38, 1.67 and 1.38 out of 5).
- **Caveats:** A four-page short paper; the percentages (85.7, 42.9, 21.4) imply about 14 participants. Treat as a small pilot. The supporting standard is WCAG 2.2 success criterion 3.2.3 Consistent Navigation (level AA): navigation repeated on several pages appears in the same relative order, https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html (background).
- **Designer conclusion:** keep shared navigation in the same place and order. "Users are three times slower and don't notice" is a pilot result from about 14 people, not a general law.

---

## 9. Failure, recovery and bad experiences

### 9.1 de Matos, Henrique and Rossi 2007, service recovery paradox meta-analysis

- **Citation:** de Matos, C. A., Henrique, J. L., and Rossi, C. A. V. (2007). Service recovery paradox: A meta-analysis. *Journal of Service Research*, 10(1), 60-77. DOI 10.1177/1094670507303012.
- **Legal URL:** record, https://doi.org/10.1177/1094670507303012 (paywalled).
- **Access:** Abstract only (read via OpenAlex).
- **What it found:** Across the studies, a well handled failure leaves satisfaction significantly higher than no failure, supporting the paradox for **satisfaction**. The effect on **repurchase intention, word of mouth and corporate image was not significant**. Study design (cross-sectional versus longitudinal), student versus non-student samples and service type moderate the effect.
- **Related:** Michel, S., and Meuter, M. L. (2008). The service recovery paradox: True but overrated? *Journal of Service Management*, 19(4), 441-457 (abstract only). More than 11,000 bank customer interviews: the paradox exists but is rare and small. A secondary source puts it at about 5% of customers with a failure.
- **Designer conclusion:** a fast, clear, helpful recovery limits the damage of a failure and can win back satisfaction. Do not count on it to create loyalty, and never accept failures because recovery "turns them into wins".

### 9.2 PwC 2018, "Experience is everything"

- **Citation:** PwC (2018). Experience is everything: Here's how to get it right. Future of Customer Experience Survey 2017/18.
- **Legal URL:** https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/future-of-customer-experience.html (blocked automated access; refused with HTTP 403).
- **Access:** Secondary only (Adobe's summary of the report, https://blog.adobe.com/en/publish/2018/04/05/new-study-finds-consumers-would-pay-more-for-better-cx-pwc , plus several consistent summaries).
- **What it says:** 15,000 people in 12 countries. 32% say they would walk away from a brand they love after one bad experience. In the US, 17% after one and 59% after several (secondary). Up to a 16% price premium for great experience; 73% call experience key to loyalty.
- **Caveats:** Stated intentions in a survey about hypothetical behaviour, not observed churn.
- **Designer conclusion:** bad moments matter, and survey respondents say so. "A third of people leave after one bad experience" should be read as "say they would".

### 9.3 Google 2018, the Chrome dino

- **Citation:** Google, The Keyword (2018, September 6). As the Chrome dino runs, we caught up with the Googlers who built it.
- **Legal URL:** https://blog.google/products/chrome/chrome-dino/
- **Access:** Full text read.
- **What it says:** Built by Chrome designers Edward Jung, Sebastien Gabriel and Alan Bettes; submitted in September 2014 "under the guise of a page redesign"; rewritten for older Android devices and on all platforms by December 2014. About 270 million games played a month across desktop and mobile, mostly in markets with unreliable or expensive data (India, Brazil, Mexico, Indonesia). Motive in Jung's words: "There's nothing fun about getting kicked offline."
- **Caveat:** 270 million is games played, not people.
- **Designer conclusion:** an error state can carry personality and value. The dino keeps the real help on the page (the network suggestions and the error code) next to the game.

---

## 10. AI generated interfaces

### 10.1 Imteyaz et al. 2026, "Design Theater"

- **Citation:** Imteyaz, K., Imteyaz, K., Rajpal, N., Shaikh, K., Muller, M., and Savage, S. (2026). Design Theater: Evaluating the gap between user-facing design reasoning and implementation in generative UI tools. arXiv:2607.22928 (v2, 31 Jul 2026); AAAI/ACM Conference on AI, Ethics, and Society.
- **Legal URL:** https://arxiv.org/abs/2607.22928
- **Access:** Full text read.
- **What it found:** 24 UI generation tasks (structural, styling and functional tiers), each run once on five tools: ChatGPT (Canvas), Claude (Artifacts), Firebase Studio, Vercel v0 and Bolt, so 120 interfaces. Every tool had to use plain HTML, CSS and JavaScript, no libraries and no web search. Two raters scored each interface (κ = 0.70 for the reasoning metric). About 25% of the tools' stated design rationales were not implemented, rising to 34% for functional requirements. Tools implemented about half of the UX principles implied by the prompts (mean 0.54), and four of the five implemented 6% or fewer of the functional principles. Firebase scored lowest overall. Interfaces converged in visual appearance and layout across tools, with more variety in colour. The authors name the shared weakness: visibility of system status, user control and freedom, and error prevention and recovery.
- **Caveats:** One generation per tool and task, a no-library constraint, and tools that change fast. The authors state they did not measure how people perceive the rationales.
- **Cited by:** 8EAYZe6y3I8, accurately. The paper is stronger than the video on functional UX (6% or fewer).
- **Designer conclusion:** for any AI built screen, check the built UI against its stated rationale, state by state: loading, empty, error, undo, back, disabled. Do not trust the rationale text.

---

## 11. Platform reference pages

### 11.1 Apple Human Interface Guidelines

- **Pages:** Typography, https://developer.apple.com/design/human-interface-guidelines/typography ; Accessibility, https://developer.apple.com/design/human-interface-guidelines/accessibility ; Tab bars, https://developer.apple.com/design/human-interface-guidelines/tab-bars
- **Access:** Full text read (through Apple's JSON data behind the pages).
- **What they say:** Default and minimum text sizes: iOS and iPadOS 17 pt default, 11 pt minimum; macOS 13 pt default, 10 pt minimum. Minimum control size on iOS and iPadOS: 44x44 pt. Tab bars: when space runs out the last tab becomes a More tab that makes hidden tabs harder to find, and a user customisable tab list should default to five or fewer.
- **Checks against Gfsd8NNuD9g:** "iOS base 17px, macOS 13px" and "over a 44 pixel target" are correct in Apple's points, not pixels. "Five links is the limit" matches the HIG's five or fewer.

---

## 12. Cited but not research

These appear in the "cited" lists but are products, sponsors, fonts or examples, not claims of evidence. They were not chased: Mobbin and the Mobbin MCP (sponsor in six of seven videos), UX Peak Plus, Builder.io, Figma files, Cursor, Replit, the font list (DM Sans, Axiforma, SF Pro, Geist, Plus Jakarta Sans, Montserrat, Unbounded, Lato, Mulish), icon libraries (Phosphor, Lucide), example apps (LinkedIn, Duolingo, Notion, Spotify, Costco, WeTransfer, Vercel, Resend, Supabase, Linear, Uber, Apple Reminders, Slack, Bolt), the Undertone redesign and the unnamed crypto card client (+60% accounts, +79% money loaded: an agency's own case study with no published method, treat as marketing). Three books in `sources/books/` are covered by their own files.

---

## 13. Access log

| Source | Access | Where read |
|---|---|---|
| Iyengar and Lepper 2000 | Full text | U. Washington course copy |
| Scheibehenne et al. 2010 | Full text | author copy (Internet Archive) |
| Chernev et al. 2015 | Abstract | Kellogg page |
| Johnson and Goldstein 2003 | Abstract | OpenAlex; 2004 follow-up partly read (HODS) |
| Jachimowicz et al. 2019 | Full text | Cambridge Core, open access |
| Arshad et al. 2019 | Abstract | conference abstract via search |
| Spool 2011 | Full text | UIE archive |
| Nunes and Drèze 2006 | Full text | author copy at USC (Internet Archive) |
| Kivetz et al. 2006 | Full text | Columbia Business School |
| Norton et al. 2012 | Full text | Harvard DASH |
| Sarstedt et al. 2017 | Abstract | OpenAlex |
| Kahneman, Knetsch and Thaler 1990 | Abstract | OpenAlex |
| Cialdini (Influence at Work page) | Full text | author's site |
| Cialdini 2001 HBR | Summary only | HBR (paywalled) |
| Strohmetz et al. 2002 | Abstract | OpenAlex |
| Free samples 2,000% | No primary source | secondary only |
| Dotson et al. (sampling) | University release | BYU News |
| Kahneman and Tversky 1979 | Abstract | OpenAlex, Princeton link |
| Brown et al. 2024 | Full text | LMU working paper |
| Gal and Rucker 2018 | Abstract | OpenAlex |
| Mukherjee 2019 | Full text | PubMed Central |
| O'Keefe and Jensen 2007, 2009 | Abstract | OpenAlex, search summaries |
| Northcraft and Neale 1987 | Background | not available |
| Trendl et al. 2021 | Full text | Warwick repository |
| Reber et al. 2004 | Full text | UCSD author page |
| Reimann et al. 2010 | Full text | Sapienza course page |
| Pombo and Velasco 2021 | Full text (preprint) | OSF |
| Petrie et al. 2009 | Not read | Springer blocked scripts |
| de Matos et al. 2007 | Abstract | OpenAlex |
| Michel and Meuter 2008 | Abstract | search summaries |
| PwC 2018 | Secondary only | Adobe summary (PwC blocked) |
| Chrome dino 2018 | Full text | Google blog |
| Imteyaz et al. 2026 | Full text | arXiv |
| Apple HIG | Full text | Apple developer data |
