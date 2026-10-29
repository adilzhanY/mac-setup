# Scanning and information scent

How people actually look at a screen and decide where to go next, and how to design for that instead of for careful reading.

## Contents

1. People scan, satisfice and muddle through
2. Scanning patterns (F, layer cake, spotted, and others)
3. Designing for scanning
4. Information scent: labels that predict their destination
5. The power of position and defaults
6. Information software: show the answer, not the machine (Bret Victor)
7. Checks

---

## 1. People scan, satisfice and muddle through

Krug's observations, confirmed by eye-tracking:

- **Scan:** people do not read screens, they glance for words and shapes that match their goal.
- **Satisfice:** they choose the first reasonable option, not the best one. Guessing is cheap and usually works.
- **Muddle through:** they rarely work out how things work; once something works, they stick with it, even if a much better way exists.

Design consequence: **the first reasonable-looking option must be the correct one,** and the correct option must look reasonable at a glance.

## 2. Scanning patterns

NN/g eye-tracking:

- **F-pattern:** on unformatted text, a horizontal sweep across the top, a shorter sweep lower down, then a vertical scan down the left edge. The first lines and the first two or three words of each line get most fixations. It appears on desktop and mobile, mirrored in right-to-left languages. It happens when the text has no cues, the user wants to be efficient, and is not committed to reading everything. "The F-pattern is the default pattern when there are no strong cues to attract the eyes."
- **Layer cake:** eyes jump between headings and skip the body. This is the pattern you want: it happens when headings are good.
- **Spotted:** skipping blocks to hunt for a specific thing (a number, a link, a keyword).
- **Marking:** eyes stay in one place while the page scrolls (common on mobile).
- **Bypassing:** skipping the repeated first words of list items (so do not start every item with the same word).
- **Commitment:** reading nearly everything; only highly motivated readers.

**Example image studied:** NN/g's heatmap of a "Tigers in Crisis" article page. Heat concentrates in a thick bar over the first lines of the first paragraph, a shorter bar a little lower, and a stripe down the left edge, then fades almost to nothing. The ads in the header and right rail and the social and Twitter widgets in the sidebar receive nearly no fixations (banner blindness). The photo above the text gets little attention compared with the text start.

**Second image studied:** a Wikimedia Commons heatmap of the German Wikipedia main page. Attention concentrates on the opening lines of the featured article box and on the "Did you know?" box lower right, with hot spots on small portrait photos beside text. The long left navigation column and the footer stay cold. Lesson: on a dense portal, eyes go to the opening lines of content blocks and to faces, not to navigation lists, so a task-critical link must not rely on sitting in a long sidebar.

## 3. Designing for scanning

1. **Most important content first:** the first two paragraphs, the first line of every block, the first words of every label.
2. **Headings that stand out and start with the information-carrying word.** "Refunds: how long they take" beats "Some information about our refund process".
3. **Chunk** related items in visually distinct groups (borders, background tint).
4. **Bold key words and phrases,** sparingly.
5. **Lists for items and steps;** numbered lists for sequences.
6. **Descriptive link text.** "Download the 2026 price list (PDF, 2 MB)", never "click here" or "Learn more" alone.
7. **Vary the first word of list items** so bypassing readers still catch the differences.
8. **Cut.** Every unnecessary sentence lowers the chance the necessary ones are read (Krug: remove happy talk and instructions, then cut half of what is left).
9. **Keep important content out of ad-like places and shapes** (right rail boxes, bright banners, carousels), because users have learned to skip them.
10. **Visual hierarchy is a promise:** more important means more prominent; things that belong together are nested together; prominence is never spent on decoration.

## 4. Information scent: labels that predict their destination

Information foraging (Pirolli and Card, Xerox PARC): people follow the link with the strongest "scent", their estimate of how likely it leads to what they want and how fast. Scent is relative to the goal ("Food" smells right for cheese, wrong for face cleanser).

Rules:

1. **Labels say exactly what is behind them.** No "More", "Resources", "Solutions" or "Learn more" without an object.
2. **No jargon or branded names as the only label.** Pair a product name with a plain description.
3. **Summaries add information, they do not repeat the title.**
4. **Images must be representative,** a typical member of the category, not decoration. A generic or unusual image adds no scent.
5. **Labels must stand alone,** because context is often hidden or skipped on small screens ("Christmas gifts", not "Christmas" under a "Gifts" heading that scrolled away).
6. **The destination must confirm the scent.** The page title matches the link the user clicked; the first screen answers the question the link promised. A page that does not confirm scent sends users back.
7. **No clickbait.** It wins one click and burns trust for every later one.
8. **Krug's mindless choices:** each choice should be as easy as "animal, vegetable or mineral". If users must stop and decide which category they are in ("Home office" or "Small business"?), restructure so the choice is obvious or deferred.

## 5. The power of position and defaults

- Joachims et al. (2005), reported by Nielsen: users clicked the first search result 42% of the time and the second 8%. When the two were secretly swapped, the new first result still got 34% and the new second 12%. Position beats relevance.
- **Rule:** the top, first and pre-selected positions are the most powerful real estate on any screen. Put the most likely right answer there.
- **Defaults are decisions most users never change.** Pre-fill the most likely value (country from location, the usual quantity). Avoid arbitrary defaults (alphabetical first, whatever loaded first).
- **Defaults teach.** A representative default value shows what kind of input is expected.
- **Do not abuse defaults** (pre-selecting the most expensive tier or an add-on). It costs credibility and is a deceptive pattern.

## 6. Information software: show the answer, not the machine

Bret Victor, "Magic Ink" (2006): most software exists so people can *learn* something (when is the next train, which flight, what is in my calendar). That software should be designed as an information graphic, not as a machine to operate.

1. **Show the data, arranged so the answer is visible by eye.** A train timetable as a time-distance graph shows crossings and delays at a glance; movie times grouped by film on a shared time axis let the user scan down one column for "around 8 pm".
2. **Interaction is a cost.** Every query the user must formulate requires them to know what to ask and how to ask it. "Interaction should be used judiciously and sparingly." Navigation is excise (Cooper): work that serves the tool, not the goal.
3. **Infer context before asking.** Use environment (time, location, other open documents), history (last values, patterns) and only then interaction. "Most software wakes up each day with a fresh case of amnesia." Start from the last-used value.
4. **Start from a good prediction and let the user correct it** (relative navigation), instead of building context from zero (a map that opens on a whole continent is a bad start).
5. **Point, do not pick.** Choose locations on a map and dates on a calendar, not in decontextualised dropdowns.
6. **Every interaction gives an immediate visible change,** so the user can stop as soon as the answer is close enough.

Related, from "Learnable Programming" (2012), as general UI rules:

- **Show the data:** live values instead of values the user must imagine.
- **Show comparisons:** before and after, this period against last.
- **Eliminate hidden state:** if something changes behaviour, show it.
- **Make meaning transparent:** no unlabelled controls ("a microwave with unlabeled buttons").
- **Explain in context:** hints next to what they describe.
- **Create by reacting:** get something on screen immediately and let users adjust it, rather than asking them to plan in their head.
- **Start concrete, then generalise:** one item before batch operations, one example before a template.

## 7. Checks

- Read only the first two words of every heading, label and button. Do they still say what each is?
- Is there a wall of text without headings, lists or bold key words?
- Does any link or button say "Learn more", "Click here", "More" or "Details" without an object?
- Is the first position in every list, menu and result set the most likely right answer?
- Is every default a predictable winner? Is any default self-serving?
- Does any important content look like an ad or sit where ads usually are?
- Could the answer the user came for be shown directly, without them asking for it?
- Does the product remember the last values and start from them?
