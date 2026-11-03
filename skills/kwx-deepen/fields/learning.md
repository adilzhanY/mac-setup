# Learning and teaching

## When this playbook applies

- "Teach me X" or "help me learn X" (a topic, a language, a tool, a skill).
- "Explain X" to a named audience, or "explain it simply".
- Making a course, lesson, workshop, tutorial series or onboarding plan.
- Preparing for an exam or certification.
- Preparing for a job interview (technical, behavioural, case).
- Making flashcards, quizzes, practice sets or study plans.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Cognitive psychologist who studies learning and memory, 20 years, retrieval practice and spacing in classrooms.** Fits study plans, exam prep, flashcards, and any "how should I learn this".
- **Experienced classroom teacher and instructional coach, 15 years, explicit instruction in maths or science.** Fits explaining a topic to beginners and planning a lesson.
- **Instructional designer, 12 years, builds university and corporate courses with backward design.** Fits making a course or workshop.
- **Performance coach in a skill domain (music, chess, sport, programming), 10 years, designs deliberate practice for students.** Fits learning a skill, not a body of facts.
- **Hiring interviewer and interview coach, 10 years, has run hundreds of structured interviews in one field.** Fits interview preparation.

## Moves the expert makes unasked

1. **Define what the learner must be able to do at the end, as an observable task.**
   Why: backward design (Wiggins and McTighe) starts from desired results, then the evidence of learning, then the activities; Bloom's revised taxonomy (Anderson and Krathwohl) names the level (remember, understand, apply, analyse, evaluate, create).
   Check: two to five outcomes are written with action verbs and a level, for example "solve a first order linear ODE given its initial value (apply)".

2. **Find out what the learner already knows before teaching.**
   Why: the same explanation helps a novice and slows down an expert (the expertise reversal effect, Kalyuga and colleagues).
   Check: a short diagnostic (3 to 5 questions or a task) was run and the plan changed based on its result.

3. **Write the test before the lesson.**
   Why: if the outcome cannot be tested, it is not yet defined; the test also shows what the lesson must cover.
   Check: the final check (questions, task, mock interview) exists before any teaching material is written.

4. **Use retrieval practice instead of rereading.**
   Why: in Roediger and Karpicke (2006), students who took recall tests remembered more a week later than students who restudied, although restudy looked better after 5 minutes; Dunlosky and colleagues rate practice testing as high utility.
   Check: every session ends with the learner recalling or producing answers without notes, and rereading and highlighting are not the main activity.

5. **Space practice over days, not one block.**
   Why: distributed practice is the other high utility technique in Dunlosky et al.; Cepeda et al. (2008) found the best gap grows with how long the material must be kept.
   Check: the plan has review dates tied to the exam or use date, with gaps that widen over time.

6. **Mix problem types once each is learned (interleaving).**
   Why: Bjork's desirable difficulties: blocked practice feels faster, mixed practice gives better long term retention and teaches the learner to choose the method.
   Check: practice sets after the first lesson mix types in random order, and the learner must say which method applies.

7. **Start novices on worked examples, then fade them.**
   Why: Sweller and Cooper (1985) showed algebra novices learned more from studying worked examples than from solving the same problems; cognitive load theory explains why, and the benefit fades as expertise grows.
   Check: early material pairs each worked example with a similar problem to solve, and later material removes steps from the examples.

8. **Teach in small steps and check every learner after each step.**
   Why: Rosenshine's principles of instruction, drawn from studies of effective teachers, include small steps, guided practice, and checking understanding by asking all students, not "any questions?"; he reports a success rate of about 80 percent as a good target during practice.
   Check: each step ends with a question the learner must answer, and the next step waits until most answers are right.

9. **Name the common misconceptions and test for them directly.**
   Why: Hake's survey of 6,542 physics students found courses using interactive engagement around misconceptions roughly doubled normalised gains over traditional lectures (about 0.48 vs 0.23).
   Check: a list of 3 to 5 known misconceptions exists, and at least one question per misconception has a wrong option built on it.

10. **Have the learner explain it in plain words and find the gaps (the Feynman move).**
    Why: explaining without jargon exposes what is not understood; Feynman kept a notebook of things he did not know and worked through them.
    Check: the learner wrote or said an explanation for a newcomer, and the gaps it revealed were listed and then studied.

11. **For skills, design deliberate practice: a specific weakness, immediate feedback, repetition at the edge of ability.**
    Why: Ericsson, Krampe and Tesch-Römer (1993) tied expert performance to structured practice aimed at weaknesses, not total hours; later meta-analysis (Macnamara et al. 2014) shows practice explains much less in some domains, so feedback quality matters.
    Check: each practice block names the one sub-skill targeted, how feedback arrives within seconds or minutes, and how success is measured.

12. **Practise under the conditions of the real test.**
    Why: performance transfers best when practice matches the real situation (time limit, format, no notes, a person watching).
    Check: at least one full timed mock exam or mock interview with an external judge is in the plan before the real date.

13. **Track what is wrong, not what was covered.**
    Why: hours studied and pages read feel like progress and predict little; error logs show where the next session should go.
    Check: an error log (question, wrong answer, why, fix) exists and drives the next session's content.

## Raw material

What the expert starts from:
- **The real target:** the official exam syllabus and past papers, the job description and the company's interview guide, the actual task the learner must perform, the standard the course must meet.
- **Primary sources for the content:** the textbook or reference used in the field, the original paper, official documentation, not a blog summary.
- **The learner's own work:** their answers to a diagnostic, their past mistakes, a recording of their practice.
- **Known misconceptions:** concept inventories (for example the Force Concept Inventory in physics), common wrong answers from past exams, examiner reports, interview feedback.
- **Worked solutions** from a trusted source, for building and fading examples.

Where to get it: the exam board or certifying body, the course's official materials, the company's careers pages and the job ad, examiner reports, field specific question banks with explanations.

What to distrust:
- Learning styles matching (visual, auditory, kinesthetic); Pashler et al. (2008) found no adequate evidence for it, so do not build a plan on it.
- The learner's feeling of knowing after rereading; fluency is not memory.
- Unofficial exam dumps and "top 50 interview questions" lists with no source.
- Summaries and mind maps made by someone else, used as the main study material.
- Speed claims ("learn X in a weekend") that skip practice and spacing.

## Methods and tools

- **Backward design (Understanding by Design):** for any course, lesson or plan; outcomes, then evidence, then activities.
- **Revised Bloom's taxonomy:** to state outcome levels and to check the test asks at the level the goal needs.
- **Retrieval practice:** free recall, flashcards answered before flipping, practice questions, blank page summaries.
- **Spaced repetition (Anki, SuperMemo style schedulers, or a dated review list):** for facts, vocabulary, formulas and definitions.
- **Interleaved problem sets:** for maths, science, programming and any area with several solution methods.
- **Worked examples and faded examples:** for novices learning procedures.
- **Rosenshine's principles of instruction:** for live explanation and tutoring sessions.
- **Peer Instruction and ConcepTests (Mazur):** for groups: a conceptual question, a vote, discussion, a second vote.
- **Feynman explanation:** for checking understanding of a concept.
- **Deliberate practice design:** for skills; target a sub-skill, get fast feedback, repeat.
- **Error log:** for exam and interview prep.
- **Mock exam and mock interview:** for any high stakes performance; timed, with an outside judge.

## Independent proof

What shows the learning or teaching worked, other than the teacher or the learner's feeling:
- **Delayed test:** the learner answers new questions on the outcomes after a gap (at least a day, ideally a week), without notes. Run it: a subagent writes questions from the outcomes and syllabus only, not from the lesson text, and scores the answers.
- **Pre and post comparison:** the same style of diagnostic before and after; report the gain, ideally as Hake's normalised gain (post minus pre, divided by 100 minus pre).
- **Transfer task:** a problem in a form the lessons did not show. Pass if the learner solves it.
- **Misconception probe:** questions whose wrong options encode known misconceptions. Pass if the learner avoids them and explains why.
- **External judge:** a past paper marked against the official mark scheme; a mock interview scored by someone who did not coach.
- **Explanation check:** a fresh subagent given only the explanation and the stated prerequisites answers questions written from the outcomes; wrong answers point to unclear parts. It is a weak stand in for a real novice, so prefer the learner's own answers when they exist.
- **For a course:** a fresh agent with only the stated prerequisites works through it; record where it gets stuck.

## Amateur mistakes

1. Explaining more instead of asking the learner to produce something.
2. Rereading and highlighting as the main study method.
3. Cramming in one block before the exam.
4. Practising each problem type in its own block and never mixing them.
5. Giving a novice open problems with no worked examples, or giving an expert worked examples they do not need.
6. Asking "does that make sense?" and taking "yes" as proof.
7. Writing a course as a list of topics instead of outcomes the learner can show.
8. Testing recall when the goal is application, or the reverse.
9. Studying from unofficial summaries instead of the syllabus and past papers.
10. Interview prep that memorises answers instead of rehearsing out loud with a timer and a judge.
11. Measuring progress by hours spent or chapters covered.
12. Using jargon in an explanation meant for beginners, or defining terms with other undefined terms.

## Scope traps

How "deeper" turns into "bigger" here:
- "Explain X" becomes a full course on the field around X.
- An exam plan grows to cover topics not on the syllabus.
- A lesson grows into a curriculum, a platform, or an app.
- Interview prep grows into a career plan or a CV rewrite.
- A flashcard request becomes a full textbook summary.
- A skill plan tries to fix every weakness at once instead of the top one or two.

Deeper means: the same topic and the same time budget, aimed at stated outcomes, with retrieval, spacing and an outside check built in. Often it means less content and more practice.

Typical "not doing" items:
- Not covering topics outside the syllabus or the stated outcomes.
- Not building software, an app or a course platform.
- Not producing reading material longer than the practice material.
- Not teaching prerequisites beyond a short refresher; gaps are listed.
- Not changing the learner's tools or schedule beyond the plan asked for.
- Not writing model answers for the learner to memorise.

## Worked example

Request: "Help me learn statistics for my exam in three weeks."

1. **Expert:** a cognitive psychologist who studies exam learning and has coached students through university statistics exams.
2. **Unasked moves (top 5):** start from the official syllabus and past papers; run a short diagnostic and plan around its errors; build retrieval practice on a spaced schedule to the exam date; interleave test choice questions (t-test vs chi-square vs regression); probe known misconceptions (p-value meaning, correlation vs causation).
3. **Raw material:** the exam board syllabus, past papers and mark schemes, the course textbook, examiner reports on common errors; distrust unofficial summaries and the learner's feeling of knowing.
4. **Methods:** backward design, worked then faded examples, retrieval practice, spaced review dates, interleaved sets, an error log.
5. **Independent proof:** a past paper sat under timed conditions and marked against the official mark scheme in week 1 and again in week 3; questions written from the syllabus, not from the lessons.
6. **Rewritten task:**

```
Build a 3 week study plan for <exam>, from its official syllabus and past papers.
Day 1: a 20 minute diagnostic from a past paper; plan the rest around its errors.
Each syllabus topic: one outcome with a Bloom level, 2 worked examples then 3 faded ones, and recall questions.
Schedule spaced reviews to the exam date; mix question types from week 2 on.
Include questions aimed at known misconceptions (p-values, causation, test choice).
Proof: timed past paper in week 1 and week 3, marked with the official mark scheme.
Deliverable: one plan and its question sets, same as asked.
Not doing: topics outside the syllabus, long reading notes, software, model answers to memorise.
```

## Sources

- Roediger HL, Karpicke JD. Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. Psychological Science 17(3), 2006, 249-255. https://gwern.net/doc/spaced-repetition/2006-roediger.pdf
- Dunlosky J, Rawson KA, Marsh EJ, Nathan MJ, Willingham DT. Improving Students' Learning With Effective Learning Techniques. Psychological Science in the Public Interest 14(1), 2013. https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html
- Cepeda NJ, Vul E, Rohrer D, Wixted JT, Pashler H. Spacing Effects in Learning: A Temporal Ridgeline of Optimal Retention. Psychological Science 19(11), 2008. https://www.evullab.org/pdf/CepedaVulRohrerWixtedPashler-PS-2008.pdf
- Bjork RA, Bjork EL. Desirable difficulties (UCLA Bjork Learning and Forgetting Lab). https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/RBjork_inpress.pdf
- Ericsson KA, Krampe RT, Tesch-Römer C. The Role of Deliberate Practice in the Acquisition of Expert Performance. Psychological Review 100(3), 1993. https://doi.org/10.1037/0033-295X.100.3.363
- Macnamara BN, Hambrick DZ, Oswald FL. Deliberate practice and performance in music, games, sports, education, and professions: a meta-analysis. Psychological Science 25(8), 2014. https://pubmed.ncbi.nlm.nih.gov/24986855/
- Sweller J, Cooper GA. The use of worked examples as a substitute for problem solving in learning algebra. Cognition and Instruction 2, 1985. Overview: https://en.wikipedia.org/wiki/Worked-example_effect
- Kalyuga S, Ayres P, Chandler P, Sweller J. The Expertise Reversal Effect. Educational Psychologist 38(1), 2003. https://typeset.io/pdf/the-expertise-reversal-effect-5y3mqyx7oo.pdf
- Krathwohl DR. A Revision of Bloom's Taxonomy: An Overview. Theory Into Practice 41(4), 2002. https://quincycollege.edu/wp-content/uploads/Anderson-and-Krathwohl_Revised-Blooms-Taxonomy.pdf
- Wiggins G, McTighe J. Understanding by Design. Backward design summary (University of Vermont CTL): https://www.uvm.edu/ctl/backward-design-and-learning-objectives
- Rosenshine B. Principles of Instruction: Research-Based Strategies That All Teachers Should Know. American Educator, Spring 2012. https://www.aft.org/sites/default/files/Rosenshine.pdf
- Hake RR. Interactive-engagement versus traditional methods: A six-thousand-student survey of mechanics test data for introductory physics courses. American Journal of Physics 66, 1998. https://www.montana.edu/msse/Old_Data_analysis/Hake_1998_Normalized_gain.pdf
- Pashler H, McDaniel M, Rohrer D, Bjork R. Learning Styles: Concepts and Evidence. Psychological Science in the Public Interest 9(3), 2008. https://pubmed.ncbi.nlm.nih.gov/26162104/
- Mazur E. Peer Instruction (Harvard Mazur Group). https://mazur.harvard.edu/presentations/using-clickers-peer-instruction
- Newport C. The Feynman Notebook Method (on Feynman's "Notebook of Things I Don't Know About", from Gleick's biography). https://calnewport.com/the-feynman-notebook-method/
