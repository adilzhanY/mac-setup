# Writing and editing

## When this playbook applies

- An article, blog post, essay or op ed.
- An email or message that needs a reply, a decision or an action.
- A cover letter, application answer, or personal statement.
- Documentation: a README, tutorial, how to guide, API reference, or design doc.
- A report, memo, proposal or executive summary.
- A speech, talk script, or presentation narrative.
- Editing or shortening someone else's text.
- Translating a text into another language.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Magazine features editor, 15 years, cuts and restructures other people's drafts.** Fits articles, essays, and "make this better" edits.
- **Management consultant trained in the Pyramid Principle, 10 years writing board memos.** Fits reports, proposals, executive summaries and business emails.
- **Technical writer, 12 years, developer documentation for a large open source project.** Fits READMEs, tutorials, reference and how to guides.
- **Speechwriter, 8 years, writes for executives and officials who read aloud.** Fits speeches and talk scripts.
- **Certified professional translator who also revises others' translations, 10 years, one language pair and one domain.** Fits translation and localisation.

## Moves the expert makes unasked

1. **Name the reader and what they must do or know after reading.**
   Why: Pinker calls the curse of knowledge the main cause of bad writing: the writer cannot imagine not knowing what they know.
   Check: one line at the top of the notes says who the reader is, what they already know, and the single action or belief the text should produce.

2. **Put the point first.**
   Why: Minto's Pyramid Principle puts the governing answer at the top with grouped support below, because busy readers stop early; on the web, NN/g's eyetracking shows readers scan in an F pattern and miss what is low and right.
   Check: the main point or request is in the first two sentences (or the subject line for email).

3. **Write the whole message in two sentences before drafting.**
   Why: if it cannot be said briefly, the writer does not yet know what they think (Orwell's first question: "What am I trying to say?").
   Check: a two sentence summary exists and the draft's opening matches it.

4. **Choose the document type and keep to it.**
   Why: Diátaxis argues that tutorials, how to guides, reference and explanation serve different needs, and mixing them makes all four worse; the same holds for a memo that turns into a story.
   Check: the type is named and no section belongs to another type.

5. **Make characters the subjects and actions the verbs.**
   Why: Williams shows that sentences feel clear when the doer is the subject and the action is a verb, not a noun ("we analysed", not "an analysis was performed").
   Check: scan for nominalisations (-tion, -ment, -ance) and passive verbs; each one left in has a reason.

6. **Put old information first and new information last in each sentence.**
   Why: Gopen and Swan show readers expect the start of a sentence to link back and the end (the stress position) to carry what is new and important.
   Check: in each paragraph, sentence openings refer to something already mentioned, and the key term of each sentence sits near its end.

7. **Replace abstractions with a concrete example, number or name.**
   Why: Strunk's "use definite, specific, concrete language" and Orwell's warning against stale phrases both target text that sounds fine and says nothing.
   Check: every claim of quality ("significant", "robust", "great results") is replaced by or followed by the number or case behind it.

8. **Cut by a fixed share on the second pass.**
   Why: "Omit needless words" works only as an actual pass with a target (for example 15 percent); without a target, writers defend every word.
   Check: word count before and after the edit pass is recorded, and nothing a reader needs was removed.

9. **Read it aloud.**
   Why: the ear catches long sentences, repeated words and missing links that the eye skips; speechwriters keep most sentences short enough to say in one breath.
   Check: an aloud pass (or text to speech) was done; no sentence needed a second breath unless intended.

10. **Test it on a real reader from the audience.**
    Why: plain language guidance (Plain Writing Act, digital.gov) ends with testing for understanding, because the writer is the worst judge.
    Check: a reader who did not write it paraphrased the main point back, or completed the task, and the gaps were fixed.

11. **Check every fact, name and number in the text.**
    Why: one wrong name in a cover letter or one wrong figure in a report outweighs any style gain.
    Check: a list of every proper noun and number in the text, each with its source or confirmation.

12. **Fit the length and form to where it will be read.**
    Why: a phone screen, an inbox preview, a podium and a printed report each need different length, paragraphing and headings.
    Check: the reading context is named and the format follows it (an email subject that shows in full in an inbox preview, one idea per slide line for a speech, scannable headings for docs).

13. **For translation: translate meaning for the target reader, then have a second linguist revise.**
    Why: ISO 17100 requires revision by a second qualified person; word for word fidelity produces text no native writes.
    Check: a glossary of key terms exists, and a second pass compared source and target line by line.

14. **Match the voice of whoever signs it.**
    Why: text sent as a person (a letter, an application) that reads as a different person loses trust.
    Check: compared against two or three real samples of that person's writing for sentence length, vocabulary and formality.

## Raw material

What the expert starts from:
- **The facts and the source material**, not a summary of them: the data, the meeting notes, the code, the job posting, the original text to be translated.
- **The reader's own words**: the email being answered, the job ad, the support tickets, the questions users actually ask, search queries that lead to the doc.
- **Real samples of the target form**: three strong examples of the genre in this venue (published articles in the target outlet, docs from a well regarded project, successful applications in this field).
- **The author's own past writing**, when the text goes out in their name.
- **For translation:** the full source, any existing glossary or translation memory, and the target market's style conventions.

Where to get it: from the requester (ask for the original, not a paraphrase), from the publication or project itself, from the issue tracker or inbox.

What to distrust:
- The requester's summary of what the reader wants; check the reader's own words.
- Templates and "best cover letter" examples, which every other applicant also uses.
- Style rules applied mechanically (Orwell's sixth rule: break any of them sooner than say anything barbarous).
- Readability scores alone; a short sentence can still be unclear.
- Machine translation output as a base without full revision.

## Methods and tools

- **Pyramid Principle and SCQA (situation, complication, question, answer):** for any report, memo, proposal or decision email.
- **Inverted pyramid:** for news style articles, announcements and web pages; most important first.
- **Diátaxis:** to decide what kind of documentation page is needed and what belongs in it.
- **Williams' principles (characters as subjects, actions as verbs, old before new, cohesion and coherence):** for line editing.
- **Gopen and Swan's reader expectations (topic position, stress position):** for dense technical or scientific prose.
- **Orwell's six rules and four questions:** as a final sentence level pass.
- **Strunk's composition rules (omit needless words, use the active voice, definite specific concrete language):** as a cutting pass.
- **Plain language guidelines:** for any public, legal, medical or instructional text.
- **Reverse outline:** list the point of each paragraph after drafting; reorder or cut paragraphs that repeat or wander.
- **Read aloud or text to speech:** for speeches, emails and anything with rhythm.
- **Paraphrase test and task test:** a reader restates the point or performs the task; for docs and instructions.
- **Translation workflow (translate, self check, second linguist revision, optional review by a domain expert):** per ISO 17100.
- **Style linting (Vale, write-good, LanguageTool):** to catch mechanical issues, never as the judge of quality.

## Independent proof

What shows the text works, other than the writer:
- **Paraphrase test:** a fresh subagent, given only the text and the reader's profile, writes what the main point is and what it is asked to do. Pass if it matches the two sentence summary.
- **Task test (docs and instructions):** a fresh agent follows the doc from a clean environment. Pass if it completes the task without information outside the doc.
- **Cold read for the first screen:** a subagent sees only the subject line and first 50 words. Pass if it can say what the message is about and what is asked.
- **Fact list check:** a script or subagent extracts every name, number, date and claim, and each one is confirmed against its source.
- **Before and after counts:** word count, average sentence length, passive count and nominalisation count, compared between draft and final.
- **Back translation or bilingual revision:** for translation, a second agent translates back or reviews line by line; differences in meaning are listed and resolved.
- **Real reader signal, when available:** replies, completion rates, support tickets, or a human from the audience reading it.

## Amateur mistakes

1. Opening with background or throat clearing ("I hope this finds you well", "In today's world") instead of the point.
2. Writing for the writer: jargon, abbreviations and steps skipped because they feel obvious.
3. Hedging every claim ("somewhat", "arguably", "may potentially"), so nothing is said.
4. Burying the request in the last paragraph of an email.
5. Claims of quality with no number or example ("passionate", "results driven", "world class").
6. Mixing tutorial, reference and explanation in one documentation page.
7. Long noun stacks and nominalisations ("implementation of the optimisation of the configuration").
8. Editing at the word level before fixing the structure, so well polished paragraphs sit in the wrong order.
9. A cover letter that retells the CV instead of matching two or three real proofs to the job's stated needs.
10. A speech written for the eye: long sentences, nested clauses, numbers no listener can hold.
11. Translating word for word, keeping source idioms and sentence order.
12. Never testing the text on anyone before sending it.

## Scope traps

How "deeper" turns into "bigger" here:
- "Improve this email" becomes a rewrite of the whole thread or a new policy proposal.
- A README edit becomes a full documentation site with tutorials, guides and reference.
- A cover letter becomes a rewritten CV and LinkedIn profile.
- A 600 word article becomes 2,000 words because the research was interesting.
- An edit becomes a change of the author's argument or voice.
- A translation becomes a localisation of the whole product.

Deeper means: the same piece at the same length, aimed at a named reader, built on real material, and tested. Usually the deeper version is shorter.

Typical "not doing" items:
- Not changing the length beyond plus or minus 10 percent of what was asked.
- Not changing the author's argument or position, only how it is made.
- Not writing other documents (CV, other pages, follow up emails).
- Not adding sections the reader did not need.
- Not localising images, layout or product strings, text only.
- Not designing or formatting beyond the target medium's defaults.

## Worked example

Request: "Write a README for my CLI tool."

1. **Expert:** a technical writer who maintains docs for a widely used open source CLI.
2. **Unasked moves:** name the reader (a developer finding the repo for the first time) and the one thing they must do (install and run the first command in under two minutes); put what it does and a working example first; decide this page is a short tutorial plus pointers, not reference; test every command; cut features the reader does not need on day one.
3. **Raw material:** the actual `--help` output, the source of the main commands, open issues asking "how do I...", and READMEs of three well regarded CLIs in the same ecosystem; distrust the author's description of what users want.
4. **Methods:** Diátaxis (tutorial versus reference), inverted pyramid, Williams line edit, a cutting pass.
5. **Independent proof:** a fresh agent in a clean container follows the README from install to first result with no other help; every code block is run and its output matches the README.
6. **Rewritten task:**

```
Write a README for <tool> for a developer who has never seen it.
Goal: install and get a first useful result in under two minutes.
Order: one sentence on what it does, install, a first example with real output, the 3 most common tasks, links to full reference.
Start from the real --help output, the source of the main commands, and open issues that ask "how do I".
Run every command in the README in a clean environment; outputs shown must be real.
Proof: a fresh agent completes install and the first example using only the README.
Deliverable: one README.md, roughly one screen to the first example, same as asked.
Not doing: a docs site, full flag reference, contributing guide, logo or badges.
```

## Sources

- Orwell G. Politics and the English Language, 1946. https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/
- Strunk W. The Elements of Style, 1918 (Project Gutenberg edition). https://www.gutenberg.org/ebooks/37134
- Williams JM, Bizup J. Style: Lessons in Clarity and Grace, 12th ed., 2016. Course summary of its principles (Yale-NUS): https://yale-nus.edu.sg/academics/wp-content/uploads/sites/8/2021/12/Grammar-Style-Actions-Characters.pdf
- Pinker S. The Sense of Style, 2014. On the curse of knowledge: https://www.psychologicalscience.org/observer/the-curse-of-knowledge-pinker-describes-a-key-cause-of-bad-writing
- Gopen GD, Swan JA. The Science of Scientific Writing. American Scientist 78, 1990. https://www.jstor.org/stable/29774235
- Minto B. The Pyramid Principle: Logic in Writing and Thinking. Summary of the method and SCQA: https://www.antoinebuteau.com/lessons-from-barbara-minto/
- Procida D. Diátaxis, a systematic approach to technical documentation. https://diataxis.fr/
- Digital.gov (US General Services Administration). Plain language guide, incorporating the Federal Plain Language Guidelines. https://digital.gov/guides/plain-language
- Nielsen Norman Group. F-Shaped Pattern of Reading on the Web. https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- ISO 17100:2015 Translation services, requirements (overview of the translate, revise, review workflow). https://en.wikipedia.org/wiki/ISO_17100
