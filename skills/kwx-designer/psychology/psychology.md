# Behavioural psychology in UI: how to use it honestly

The master file for `psychology/`. Read it before using any persuasion pattern, then open the topic file you need. Every pattern here must pass the honesty test in section 3 before it ships.

## Contents

1. What the videos claim, in one paragraph
2. The principle map (which file, which effect)
3. The honesty test (run it on every pattern)
4. ETHICS: the hard line, forbidden patterns and their honest alternatives
5. Patterns from the videos that need correcting
6. How strong the evidence is
7. Source key

---

## 1. What the videos claim

Users do not decide logically (uxpeak, UX psychology video). A default reads as a recommendation, the first number seen becomes the ruler, a gift creates a debt, building something makes it yours, progress creates momentum, and a loss weighs about twice as much as an equal gain. The premium video adds the other half (Tim Gabe): the brain "has no premium detector, but it does keep score" of evidence that a product is good, and what is easy to process is judged more kindly.

Use these effects to **remove friction and make the honest choice the easy one**. Never use them to make a choice the user would regret once they understood it.

## 2. The principle map

| Effect | One line rule | File |
|---|---|---|
| Default effect, decision fatigue, choice overload | Preselect the most common answer, show 4 to 6 options, hide the rest | `defaults-and-choice.md` |
| Goal gradient, endowed progress | Count real work already done; never start a bar at 0% when something is done | `progress-and-motivation.md` |
| Streaks, checklists | Make progress visible and forgiving, never a guilt engine | `progress-and-motivation.md` |
| Reciprocity | Give real value before any ask | `value-before-ask.md` |
| IKEA effect, endowment effect | Let users build or customise before sign up | `value-before-ask.md` |
| Contrast effect, anchoring | Show a cost next to the thing it relates to, never in isolation | `pricing-psychology.md` |
| Decoy effect | Every tier must be a real option a rational person could pick | `pricing-psychology.md` |
| Loss aversion, status quo bias | Name a real loss plainly; never invent one | `pricing-psychology.md`, section 4 below |
| Processing fluency, consistency, social proof | Easy to take in reads as trustworthy; inconsistency costs more than users say | `trust-and-fluency.md` |
| Service recovery paradox | A failure handled well can beat no failure | `trust-and-fluency.md` |

## 3. The honesty test

Run these five checks on every persuasion pattern before it ships. One "no" means redesign it.

1. **True.** Every claim on the screen is true right now: the deadline exists, the stock count is real, the struck price was really charged, "Free" is free. Verify by finding the data source in code. A hard coded countdown, a hard coded "Only 3 left" or a random number generator feeding urgency is a fail.
2. **Reversible.** The user can undo the choice as easily as they made it. Cancelling takes no more steps than subscribing. Unticking an option is one tap.
3. **Visible.** Nothing that costs money, data or consent is preselected, hidden below the fold or added silently. The total is shown before the commit.
4. **Respectful exit.** The dismiss option is plain, neutral and the same size class as other secondary actions. It never mocks or guilts the user.
5. **Would they thank you?** If the user later understood exactly how the screen worked, would they feel helped or tricked? Helped is the only pass.

## 4. ETHICS: the hard line

**No dark patterns. Ever.** The patterns below are forbidden in every product made with this skill, **including where one of the source videos showed or recommended them**. A video showing a technique is not permission. When a brief asks for one of these, build the honest alternative and say why in one line.

| Forbidden | What it looks like | Honest alternative |
|---|---|---|
| **Confirmshaming** | A dismiss link that guilts or mocks: "I'll Risk It" (shown in the uxpeak loss aversion example), "No thanks, I like losing money", "I don't want to be healthy" | A neutral dismiss: "Not now", "Close", "Keep current plan". State the real consequence once, in the body copy, as a fact |
| **Fake urgency** | Countdown timers that reset, "Offer ends in 10:00" with no real end, "3 days" that is not true | Show a deadline only when it exists in the data, with the exact date ("On September 12, your sessions will be refreshed"). No deadline, no timer |
| **Fake scarcity** | "Only 2 left!", "12 people are viewing this" from hard coded or random values | Show stock only from real inventory, and only when it helps the decision. Otherwise show nothing |
| **Hidden costs** | Fees, shipping or tax appearing only at the last step; a monthly price shown where a yearly charge is taken | Show the total early and in the primary button ("Add to cart · $18.60"). Show the billing period and the amount actually charged together |
| **Roach motel cancellation** | Sign up in one tap, cancel only by phone, chat, or a five screen maze | Cancel from the same settings area in at most the same number of steps as subscribing. One retention offer is allowed, shown once, with a plain "Cancel subscription" next to it |
| **Nagging** | The same upgrade, rating or notification prompt shown again and again after a no | Ask once at a moment of value. After a no, wait for a meaningful new event (a new limit reached, a new feature), and never more than the cadence stated in settings |
| **Sneak into basket** | Add ons, insurance or donations preselected in the cart | Offer the add on unticked, next to its anchor, with a compact "Add" button |
| **Preselected consent** | Marketing opt in, data sharing or a paid upgrade ticked by default | Defaults only for neutral, reversible choices (date, party size, seating). Consent is always opt in |
| **Disguised ads, bait and switch** | A button that says "Continue" but creates a paid trial; an ad styled as content | The label says what happens: "Start free trial, then $9/mo", "Create free account" |
| **Fake social proof** | Invented reviews, ratings, "Most popular" on an arbitrary tier | Ratings from real data with the count ("4.8 (89 reviews)"). "Most common" only when it is measured |
| **Holding results hostage** | Blurring results the user already worked for behind "Sign up to unlock" (named as the anti example in the uxpeak video) | Show the useful result; gate only a deeper extra, and say what the account adds |
| **Fake progress** | A bar that starts at 20% for work the user never did, a spinner that pretends to work | Count only steps that are really complete. Show real progress or an honest indeterminate state |

### How to verify by reading code

- `grep -rniE "only [0-9]+ left|people (are )?(viewing|watching)|hurry|ends in|last chance" src/` and trace every hit to a real data source.
- Find every `setInterval`/timer feeding a countdown: the end time must come from the server or a stored deadline, not `Date.now() + N`.
- Find every checkbox or toggle with `checked`/`defaultChecked`/`value: true`: none may control consent, marketing, a paid add on or data sharing.
- Read every dismiss, decline and cancel label. Each must be neutral ("Not now", "Cancel", "Close", "Keep my plan").
- Count the steps of subscribe vs cancel in the router or flow definition. Cancel must not be longer.

## 5. Patterns from the videos that need correcting

The uxpeak UX psychology video is the main source of persuasion patterns. Keep its insight, change its execution where it crosses the line.

| Video says | Keep | Change |
|---|---|---|
| "Your Files Will Be Deleted" modal, red deadline, "I'll Risk It" dismiss | Name the user's real files, the real size at risk ("2.8 GB"), the real date | Only when deletion is actually scheduled. Dismiss reads "Not now" or "Manage storage". Never invent a deletion to sell storage |
| "Progress, even a fake one, creates real momentum" | Count account creation as step 1 of 5 when it is a real step | Never pre fill progress for work not done. 20% must equal 1 of 5 real steps |
| Button reads "Continue" instead of "Sign up" after the user invested | Sign up after value, framed as saving their work | If the button creates an account, say so: "Save my profile" with "Creates a free account" beneath |
| "Only 13 left!" as a colour example (Kole Jain, every UI concept) | Accent colour for a meaningful note | Only with real stock data |
| "Don't sell what they'll gain, show what they'll lose" | Concrete, specific framing beats generic feature lists | Loss framing only for a real, imminent loss. For an ordinary upgrade, state the concrete benefit and the price |
| "Don't lose tonight's work" sign up prompt | Valid when the progress really lives only on this device | Also offer a way to keep it without an account where possible (export, local save) |

## 6. How strong the evidence is

Numbers quoted in the videos, with a confidence note. Quote them as the video does, not as settled law.

| Claim | Source as given | Strength |
|---|---|---|
| 24 jams: 3% bought; 6 jams: 30% bought | "Columbia jam study" (Iyengar and Lepper 2000) | Classic, but later replications are mixed; treat as direction, not a 10x law |
| 70 to 90% of users never change defaults | No source named (uxpeak) | Unsourced; the default effect itself is well established |
| Car wash: 2 of 10 stamps prefilled nearly doubled completion | "Columbia" (matches Nunes and Dreze 2006, about 34% vs 19%) | Solid |
| Losses about twice as powerful as gains | Kahneman (prospect theory) | Solid in lab, smaller in some field settings |
| Free samples raise purchases up to 2,000% | No source | Unsourced; do not repeat as fact |
| Nav moved left to right: 1.9 s to 6.8 s on that page, 2.2 s to 6.2 s after | Petrie et al., University of York 2009 | Small study, strong direction |
| About a third of people leave after one bad experience | PwC 2018 | Survey, self report |
| Well handled failure can match or beat no failure | "A 2007 review" (likely de Matos, Henrique, Rossi 2007) | Meta analysis, effect varies |
| Easy to process is judged more beautiful | Reber, Schwarz, Winkielman 2004 | Solid |
| About a quarter of AI tools' stated design reasoning never reached the UI | "Design Theater" paper, 31 Jul 2026 | One study |

## 7. Source key

- uxpeak, UX psychology video: "The UX Psychology Behind Apps People Can't Stop Using" (2TlIg3VokY8)
- uxpeak, strawberry redesign: "This UI/UX Redesign Will Teach You More Than 100 Tutorials Combined" (GGg61sdEjeI)
- Kole Jain, every UI concept: "Every UI/UX Concept Explained in Under 10 Minutes" (EcbgbKtOELY)
- Kole Jain, mobile UI: "Everything you need to know about Mobile App UI's in 8 minutes" (Gfsd8NNuD9g)
- Kole Jain, dashboard flaws: "The 3 dashboard UI flaws that give away you've NEVER built one" (Ksx9C2-3yMo)
- Kole Jain, vibe coded SaaS: "5 SaaS UI/UX mistakes that SCREAM you Vibe Code" (PDcQJOPby1k)
- Tim Gabe, premium apps: "The Psychology of Premium Apps" (8EAYZe6y3I8)

Full notes live in `sources/videos/<id>.md`.
