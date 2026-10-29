# Value before the ask: reciprocity, IKEA and endowment effects, when to ask for sign up

"If the user does not trust you, nothing else matters." Most apps ask before they give: "Sign up to see your results", "Create an account to continue", "Enter your email to unlock" (uxpeak, UX psychology video). Reverse the order: give real value, let the user build something, then ask, and frame the ask as keeping what they already have.

## Contents

1. The effects
2. The order: give, let them build, then ask
3. When to ask for sign up
4. How to word the ask
5. Before and after examples
6. Honest limits
7. Checks

---

## 1. The effects

- **Reciprocity**: receiving something creates a pull to return the favour. Cialdini (Influence) ranks it among the strongest drivers of behaviour. Examples given: Costco free samples, Spotify 30 days of Premium, Notion lets you use the whole product before paying. "They're not being generous. They're being strategic." The video also says free samples raise purchases "by up to 2,000%" with no source; do not quote it as fact.
- **IKEA effect**: things people assemble themselves are valued more than identical ready made ones (Norton, Mochon, Ariely, Journal of Consumer Psychology 2012).
- **Endowment effect**: just feeling you own something raises its value, so leaving feels like losing.
- A restaurant that asks for your credit card before showing the menu: that is what a gate before value feels like. "You're holding the results hostage."

## 2. The order: give, let them build, then ask

Follow the Duolingo order (labelled "SMART DESIGN" in the video):

1. **Choose**: the user picks something meaningful (language: Spanish, French, German...).
2. **Commit**: they set a goal (multi select: Just for fun, Boost my career, Prepare for travel...).
3. **Achieve**: they complete a first real task (a first lesson, "Great job!"). About 10 minutes invested.
4. **Then ask**: account creation, framed as saving that progress.

For a tool: let them run it and see the result first. For a profile or workspace: let them customise it with a live preview first.

## 3. When to ask for sign up

Ask at the first moment the account protects or extends something the user already has. Concretely:

| Ask here | Do not ask here |
|---|---|
| Right after a completed win (end of the first lesson, first report generated) | On the first screen before any use ("Log in or create an account to get started", WeTransfer style modal) |
| When the user wants to keep, sync or share what they made | Over a blurred result they just worked for |
| When they hit a real limit of the free use and the account lifts it | In the middle of a task, breaking their flow |
| When a feature genuinely needs identity (payments, collaboration) | Repeatedly after they said no (nagging) |

Exception: products that cannot do anything without an identity (banking, KYC, private messaging). There, explain why up front and how long it takes ("Verify your identity, takes about 3 minutes", the neobank KYC flow in the Tim Gabe video).

## 4. How to word the ask

1. Frame the ask as saving or completing: "Want the full 50-page report? Save your results and get fix-by-fix instructions", button "Save My Report, Free".
2. Say "Free" on the button only when it is free, with no card required.
3. List what is unsaved, specifically: "Don't lose tonight's work / Everything below lives only on this phone, for now", then a "YOUR PROGRESS" list with an "Unsaved" status dot: "The anchor effect, Lesson 1 of 7, 8/10", "Streak started, Day 1", "XP earned, Level 1, +40". Use this only when it is true that the data lives only on the device.
4. The button names what it does. The uxpeak video recommends "Continue" instead of "Sign up" after the user invested. Keep the spirit (frame it as continuing their work) but never hide that an account is created: "Save my profile" with a line "Creates a free account" is honest; "Continue" that silently creates an account is not.
5. Keep the sign up itself short: email or a one tap provider (Apple, Google), no extra fields that the product does not need yet.

## 5. Before and after examples (uxpeak)

**SEO report tool**

| Before | After |
|---|---|
| User enters a URL, taps "Analyze". Result card blurred with a "Sign up to unlock" padlock chip, then Email, Password, "Create Account" | "Your SEO Report" with a green "Free" pill. Hero score card: "Overall SEO Score", huge "72" with small grey "/100", a pill "Good, 16 issues found". Three status cards: red "3 Critical Issues / Missing meta descriptions, broken links", amber "5 Warnings / Slow images, missing alt text", green "8 Passed / Mobile-friendly, encrypted data". Then a soft card "Want the full 50-page report? Save your results..." and "Save My Report, Free" |

**Workspace sign up**

| Before | After |
|---|---|
| "Create Your Workspace / Sign up to start building your custom workspace", grey plus placeholder, Email, Password, "Sign Up". Nothing on screen belongs to the user, so closing the tab costs nothing | "Design Your Profile / Customize how you'll appear to others". A live preview card at the top (avatar, name that becomes "Sarah Johnson", "Product Designer", chips "San Francisco", "5 years exp"). "Color Palette" with four pastel swatches, the selected one checked. "Card Style" tiles: Soft (selected), Dark, Minimal. Then the save action |

**Empty result after effort** (Tim Gabe, Undertone therapy app): users tested their mic, hit stop, and got "Looks like we didn't get enough content! This session was too short to create a summary." The founder: "I was expecting anything instead of nothing." Rule: never answer user effort with nothing. Give something back, say it did not cost them a session, and offer the next step.

## 6. Honest limits

- The value given must be real. A "free report" that is three generic sentences is bait.
- What is free stays free. Do not take back a free feature after sign up to force an upgrade.
- The user's creation belongs to the user. If they refuse to sign up, let them export or keep it locally where the platform allows. Never delete their work as pressure.
- Do not invent loss ("your work will be lost") when the app actually keeps it.
- One ask per moment of value. After a no, do not show it again in the same session.

## 7. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Value first | The first useful result renders without an account | Follow the route from landing to first result; no auth guard before it |
| No hostage results | No result the user generated is blurred or hidden behind sign up | `grep -niE "blur|locked|unlock|sign ?up to"` near result components |
| Ownership before the ask | The user makes or customises something before sign up | The sign up route comes after a create or customise step in the flow |
| Ask is framed as saving | Copy names what is kept | Read the sign up prompt strings |
| Label is honest | The button says an account is created, or the line below does | Read the button label and helper text |
| True loss only | "Unsaved" or "will be lost" appears only when data is really local only | Trace where the progress is stored |
| No nag | The prompt is suppressed after a dismiss | Find the dismissed flag and its persistence |
