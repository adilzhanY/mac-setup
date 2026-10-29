# Copywriting and tone

Words are interface. A premium product sounds like one careful person wrote every string. Apple, *Writing for Interfaces*: treat the app as a conversation, not a one way output. Butterick: the reader's attention "is precious. And finite."

## Contents

1. Voice and tone
2. The PACE method (Apple)
3. Cut: filler, pleasantries, repetition
4. Lead with the why
5. Buttons and labels
6. Alerts and confirmations
7. Errors
8. Empty states
9. Onboarding, instructions and notifications
10. Consistency: the word list
11. Case, numbers, dates, punctuation
12. Inclusive and localizable writing
13. Delight in words (and when not to)
14. Before and after table
15. Checklist
16. Sources

---

## 1. Voice and tone

From Apple, *Add Personality to Your App Through UX Writing* (WWDC24):

- **Voice** is the constant: the personality, the values. It does not change between screens.
- **Tone** is how the voice adapts to the moment. It must change.
- Apple's own voice is four qualities: **clarity, simplicity, friendliness, helpfulness.**
- **Tone is a mixer, not a switch.** Turn qualities up or down for the situation; never drop one entirely.
  - Celebration (tripled your Move goal): friendliness high, "Three cheers!". An exclamation mark is fine here.
  - Serious or urgent (high heart rate): clarity and helpfulness high, friendliness low, specific data: "Your heart rate rose above 120 BPM while you seemed to be inactive for 10 minutes starting at 9:59 AM."
  - Broken connection: clarity and helpfulness high: "Cellular Data is Turned Off. Turn on cellular data or use Wi-Fi to access data." Repeating "data" is deliberate.

**Exercise to define a voice:** imagine the product as a person, write as many adjectives as you can, group them, keep the 2 to 4 strongest as the voice. Keep the leftover words as hints for word choice. Example: an investing app for young people is "smart" and "motivating"; a kids' savings app is "kind, fun, encouraging".

**Then write one sentence three ways** and pick the one that sounds like that voice:
"Save your money." (generic) → "Customize your investment strategy." (empowering) → "Customize your long-term investment strategy." (specific to the audience).

## 2. The PACE method (Apple)

From *Writing for Interfaces* (WWDC22): Purpose, Anticipation, Context, Empathy.

- **Purpose:** state each screen's purpose in one sentence. Lead with the most important thing. Headers and buttons must make sense on their own because people scan. Cut what does not serve the purpose. Say why a feature matters ("Reducing screen time is one of the best things you can do before bed."). Say what comes next ("Activation may take a few minutes. We'll notify you.").
- **Anticipation:** offer the most likely choice first (Clock puts "Change Next Alarm Only" first). Answer the next question before it is asked ("It looks like you're awake. Would you like to turn off your alarm?").
- **Context:** where is the person and how much attention do they have? On a walk, one big button "Record Outdoor Walk"; after the walk, the details. Put instructions where the eye already is (Panorama: the instruction sits under the arrow).
- **Empathy:** plain words, no idioms, no jargon, neutral terms ("person" not "man or woman"), labels for screen readers that describe intent, not only appearance.

## 3. Cut: filler, pleasantries, repetition

From *Make a Big Impact with Small Writing Changes* (WWDC25):

- **Remove filler adverbs and adjectives:** simply, easily, quickly, just, simple. They assume the user's situation.
  - Before: "Simply enter your license plate number to quickly pay for parking."
  - After: "Enter your license plate number to pay for parking."
  - Keep a descriptive word only when it changes meaning: "Feed your pets automatically when you're away."
- **Remove interjections and pleasantries** in alerts and errors: uh oh, oops, oh no, sorry, please, thank you. They read as insincere or flippant. (WWDC22 agrees: use them "sparingly".)
  - Before: "Uh oh. We're running late. We're sorry, your driver won't make it on time. They'll be there in 10 short minutes!"
  - After: "We're running late. Your delivery driver won't make it on time. They'll be there in 10 minutes."
- **Do not say the same thing twice.**
  - After: headline "Delivery delayed 10 minutes", body "Check the app for your driver's location."
- **Direct headlines:** "Test Your Hearing", not "Take a quick and simple hearing test".
- **Exclamation marks:** almost never. Butterick: one per long document. Apple: frequent ones "look silly".

## 4. Lead with the why

Pattern: **"To get X, do Y."** Benefit first, action second (WWDC25). Works for instructions, errors and notifications.

- Before: "Enter your phone number to get reservation updates."
- After: "To get reservation updates, enter your phone number."
- Notification: "Keep your streak going by solving today's crossword."

## 5. Buttons and labels

- **A button names its action with a verb and, when useful, the object:** "Save API Key", "Add Payment Method", "Make toast" (Vercel, Apple *The Life of a Button*). Not "OK", "Continue", "Submit", "Yes".
- **Match the button to the sentence above it.** If the copy says "pair", the button says "Start Pairing" (WWDC24).
- **Same action, same word, every time.** If "Next" moves forward on one screen, it is "Next" on all of them (WWDC25).
- **Use specific navigation names** for what is inside ("Library", "Progress"), not vague umbrellas like "Home" or "Dashboard" where a specific name exists (Apple WWDC26 notes).
- **Labels are a last resort for data with an obvious format** (Refactoring UI). Show "jane@site.com", not "Email: jane@site.com", when the context is clear.
- **Ellipsis** on menu items that open a further step ("Rename..." with the real ellipsis character) and on in-progress labels ("Saving...") (Vercel).
- **Placeholders show an example**, not the label, and end with an ellipsis (Vercel).
- **Link text describes the destination**, never "click here".

## 6. Alerts and confirmations

- **Alerts interrupt. Use them only when the person must decide now** (Apple WWDC22).
- **Title is a question that names the action:** "Cancel Platinum Subscription?"
- **Buttons are the answers, named as actions:** "Cancel Subscription" and "Keep Subscription". Never Yes and No.
- **Body gives the consequence:** "You'll continue to have access until June 21, 2022."
- **Be careful with the word "Cancel"** when the action itself is cancelling something; "Confirm Cancellation" with a "Cancel" button is a trap.
- **Mark destructive buttons** with the destructive style (red), and keep the safe choice obvious.
- **Permission requests explain the use, at the moment of need:** "to show local weather and send relevant notifications" (WWDC22). Never at launch before the user knows what the app does (WWDC26 Responsibility).
- **Prefer undo to confirmation** for reversible actions; confirmation dialogs used too often train people to click through (Apple WWDC26 Agency).

## 7. Errors

Every error message answers three questions (Apple WWDC22, Vercel):

1. **What happened**, in the user's terms.
2. **Why**, if it helps.
3. **What to do now**, with a button that does it.

- Bad: "Oops! You can't do that." / "Error 1234567" / "Sorry, bad input."
- Good: "Your payment method was declined. Add a new card to keep your subscription." Buttons: "Add Payment Method", "Not Now".
- **Frame positively and constructively** (Vercel): say what will work, not only what failed.
- **Put the message next to the cause** (the field), not in a toast far away (Rauno, Vercel).
- **Prevent instead of reporting:** accept "June 31" and turn it into July 1 (Things 3, Apple WWDC17). Accept phone numbers with spaces and strip them.
- **Never blame the user.** "We couldn't find that address" beats "You entered an invalid address".
- **Error codes go in a secondary line** for support, never as the headline.

## 8. Empty states

- **Say what will appear here and how to make it appear** (Apple WWDC22):
  - Bad: "Nothing strike your fancy?" / "Please come back later..."
  - Good: "No Saved Episodes" + "Save episodes you want to listen to later, and they'll show up here."
- **Offer the first action** (and templates if useful) (Rauno, Refactoring UI).
- **Empty states can teach or celebrate** depending on context: an empty inbox can be a reward ("All caught up").
- **Search with no results:** repeat the query, suggest a correction or a broader filter, offer a way out.

## 9. Onboarding, instructions and notifications

- **Greet like a person** when it fits: Apple's setup opens with "Good morning" (WWDC24).
- **Only what the user needs to know now:** "If you have an Apple Watch, you can pair it with your iPhone here."
- **Instructions in place,** close to the control, at the moment they are needed (WWDC22 Panorama example).
- **Teach by doing** where possible; people remember what they experience (Apple *Qualities of Great Design*). Tooltips and coach marks are a last resort and should appear only for gestures used repeatedly (WWDC18).
- **Notifications lead with the benefit** and contain the key fact: "Delivery delayed 10 minutes", not "Update about your order".

## 10. Consistency: the word list

Keep a living table of terms (WWDC22, WWDC25):

| Use | Avoid | Meaning |
|---|---|---|
| Alias | Handle, User Name, Title | The player's in-game name shown to others. Not used to sign in. |
| Health | Lives, Hearts, Energy | How long the player can keep going. |

- One concept, one word, across app, site, emails and docs.
- Button verbs belong on the list ("Delete" vs "Remove": decide what each means; a common convention is Remove for taking out of a collection and Delete for destroying).
- Add terms as they come up; do not try to finish the list first.

## 11. Case, numbers, dates, punctuation

- **Pick one case style per surface and never mix.** Apple and Vercel use Title Case for buttons and headings in product UI; Vercel uses sentence case on marketing pages. Many modern products use sentence case everywhere. Either is premium; mixing is not. (For this skill's own outputs: follow the platform. iOS and macOS: Title Case for buttons and alert titles. Web apps: sentence case unless the brand says otherwise.)
- **Numerals for counts:** "3 files" (Vercel).
- **Currency:** 0 or 2 decimals, never both in one context (Vercel).
- **Units:** a non breaking space between number and unit.
- **Dates and numbers in the user's locale;** detect language from `Accept-Language` and `navigator.languages`, never from IP (Vercel).
- **Relative times** ("2 min ago") for recent items, absolute dates for older ones, with the full timestamp on hover.
- **Curly quotes, real ellipsis, no double hyphens** (Butterick). House rule for this skill: no long dashes at all in UI copy; use commas, full stops, colons or parentheses.
- **"&" instead of "and"** is a Vercel house style for tight UI; use it only if the whole product does.
- **Second person** ("your projects"), active voice ("Install the CLI") (Vercel).
- **Placeholder values in docs:** `YOUR_API_TOKEN_HERE`, numbers as `0123456789` (Vercel).

## 12. Inclusive and localizable writing

- Plain language at about a B1 to B2 reading level for general products. No idioms or puns that do not translate (WWDC22).
- Leave room for text to grow 30 to 40% in translation; never bake text into images.
- Do not assume calendar formats or abbreviations (US English uses one letter weekdays, Catalan uses two, Arabic does not abbreviate).
- Every icon, image, chart and control has a meaningful accessible label that describes intent (WWDC22: the Memoji label describes the gesture's meaning).
- `translate="no"` on brand names and code (Vercel).
- Neutral, person-first terms.

## 13. Delight in words (and when not to)

Chimero, *The Shape of Design*: delight is the overlap of **empathy, surprise and clarity**, and "one of the best opportunities to delight the audience is when something goes wrong". But delight is a long term relationship, not a gimmick.

- Allowed: a warm line in a rare moment (first project created, a streak milestone, an empty inbox).
- Not allowed: jokes in errors that cost the user money, time or data; whimsy that hides the information ("Nothing strike your fancy?"); the same joke on every screen.
- Rule: clarity first, then personality if there is room. "Don't sacrifice usefulness for personality" (WWDC24).
- Read every string aloud (WWDC22, WWDC24, WWDC25). If it sounds like a form letter or a press release, rewrite it.

## 14. Before and after table

| Before | After | Rule |
|---|---|---|
| "Simply click here to easily get started!" | "Create your first project" | Cut filler; verb + object |
| "Oops! Something went wrong." | "We couldn't save your changes. Check your connection and try again." + "Try Again" | What, why, next step |
| "Are you sure?" Yes / No | "Delete 3 files?" Delete / Cancel | Name the action |
| "No data" | "No invoices yet. Invoices you send will appear here." + "New Invoice" | Explain and offer action |
| "Error 0x8004: invalid input" | "Enter a date after today." (code in small text) | User's terms, fix first |
| "Submit" | "Send Request" | Specific label |
| "Please wait while we process your request..." | "Processing payment..." | Short, specific |
| "Welcome to the Dashboard!" heading | (removed) | Do not narrate the obvious |
| "You have 1 new messages" | "1 new message" / "3 new messages" | Plurals handled (Intl.PluralRules) |
| "Enter your email to get updates" | "To get updates, enter your email" | Lead with the why |

## 15. Checklist

- [ ] Each screen's purpose fits in one sentence; the first line says it
- [ ] Every button is a specific verb; no Yes/No, no bare OK where a verb fits
- [ ] No simply, easily, just, oops, sorry, please in UI strings
- [ ] Errors: what, why, what now, with a fixing action, next to the cause
- [ ] Empty states: what goes here, how to add it, the first action
- [ ] One term per concept; word list exists
- [ ] One case style per surface
- [ ] Numbers as numerals, locale formatting, plurals handled, non breaking spaces before units
- [ ] Curly quotes and real ellipsis; no long dashes
- [ ] Read aloud once

## 16. Sources

`../sources/books/apple-wwdc-design-talks.md`, `vercel-web-interface-guidelines.md`, `practical-typography.md`, `shape-of-design.md`, `refactoring-ui.md`, `rauno-freiberg-craft.md`.
