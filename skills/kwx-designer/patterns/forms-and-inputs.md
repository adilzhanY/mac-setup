# Forms and inputs

A form is a list of decisions the user has to make. The best form asks fewer questions, answers the predictable ones itself, shows every state of every field, and tells the user what happens before they submit. Sources: uxpeak (UX psychology, strawberry redesign), Kole Jain (every UI concept, vibe coded SaaS).

## Contents

1. Fewer fields, smart defaults
2. Pick the right control
3. Field anatomy
4. Field states
5. Layout
6. The submit action
7. Validation and errors
8. Labels and consistency
9. Checks

---

## 1. Fewer fields, smart defaults

1. Remove every field not needed for the result (the booking form dropped "Occasion").
2. Preselect the most common answer for every field you can predict (date tomorrow, guests 2, the most popular time). 70 to 90% of users never change defaults (uxpeak, unsourced figure).
3. A default is a real value in body colour, not placeholder text.
4. Never preselect consent, marketing opt ins, paid add ons or destructive options.
5. Ask later for what is not needed now (profile details after the first win).

## 2. Pick the right control

| Situation | Control |
|---|---|
| 4 to 6 likely values | Chips with one preselected, plus "View all" |
| A small count | Stepper (minus, bold value, plus) |
| A quantity with a unit | Stepper with the unit inside ("- 3 kg +") |
| 2 to 4 categories | Icon tiles |
| Common bundles | Preset tiles with name and price ("1 kg Regular $6.20"), plus the free stepper |
| Long list | Searchable select, most used first |
| Domain plus slug, currency plus amount | Joined input: dropdown attached to the text field ("linkguard.co" + "pOg8x1e" with a regenerate icon) |
| Options the user rarely needs | Collapsed pill buttons that expand (Password, Targeting, Expiration) |

## 3. Field anatomy

- Label above the field. Kole Jain's input: small caps grey label "EMAIL" above a rounded field, placeholder in light grey ("hello@kolejain.com"). The label stays visible when the field has a value; placeholder never replaces the label.
- Optional fields say "(optional)" in the label ("Title (optional)"); required is the default.
- Helper text below in grey when the format is not obvious.
- On dark surfaces: dark fill with a subtle 1 px border, not a light grey filled box (vibe coded SaaS).
- Height and padding come from tokens; touch fields at least 44 px tall on mobile.

## 4. Field states

Every input needs these designed, not left to the browser default:

| State | Look (Kole Jain, every UI concept) |
|---|---|
| Default | Hairline border, grey placeholder |
| Hover | Slightly stronger border (desktop) |
| Focus | Accent 2 px border plus a faint accent outer ring, caret visible |
| Filled | Value in body colour; section icon may turn accent |
| Error | Red border plus a red message below: "Please enter a valid email address" |
| Warning | Yellow border plus an olive message with a fix link: "This email already exists. Login instead?" |
| Disabled | Lower contrast fill and text, no hover, not focusable, with a reason nearby |
| Loading | Spinner inside the field on the right (a search field fetching "Mens shoes") |
| Success (when verifying) | Small check, no loud colour |

Warning is for optional issues that do not block; error blocks submission.

## 5. Layout

1. A sparse form that stacks one full width field per row in a tall flyout, with empty space beside it, is a tell. Use a centred modal with a two column grid when there are 4 or more short fields (the "Create New Link" redesign).
2. Pair fields that belong together on one row (Destination URL | Title; Short Link | Description). Keep long text fields full width.
3. Group related fields with proximity (16 px inside a group, 32 px between groups, Kole Jain's hero spacing used as the default rhythm).
4. On mobile, one column, and one task per screen.
5. Align every field to the same left edge; labels share one baseline grid.

## 6. The submit action

1. Enabled on first paint when defaults make the form valid. A disabled CTA on load signals work to do.
2. The label states the outcome, ideally with a real number: "Search 12 Available Tables", "Generate Secure Link", "Add to cart · $18.60".
3. Show the consequence inside the button and update it live with the inputs (the total updates as the stepper changes).
4. Place inputs next to the action they feed: the quantity stepper directly left of Add to cart.
5. Sized to its label, bottom right in a modal; sticky at the bottom on a long mobile page.
6. Loading state with a spinner while submitting, then a success message or the next screen. No double submit: disable during the request.
7. Sentence case, not ALL CAPS ("Add to cart", not "ADD TO CART").

## 7. Validation and errors

1. Validate on blur or on submit, not on every keystroke while the user is still typing a valid value.
2. The message says what is wrong and how to fix it, in plain words, next to the field.
3. Keep what the user typed after an error. Never clear a form on failure.
4. Offer the fix when you know it: "This email already exists. Login instead?" as a link; "Did you mean 'Sprint'?" for a typo.
5. On submit failure, move focus to the first invalid field and announce it to screen readers.
6. Server errors: say what happened, keep the data, offer retry, and a support path for money or account flows.

## 8. Labels and consistency

1. Drop labels the format explains (no "Price:" before "$6.20").
2. If one control in a group has a label, its siblings get one too; otherwise none do.
3. Small uppercase labels need added letter spacing.
4. The same field has the same name everywhere in the product.
5. Field icons: one icon set, one style (all outline), one colour; they turn accent when the field is filled, if used at all.

## 9. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| No needless fields | Each field is used by the submit handler or needed later in this flow | Map every field to where its value is consumed |
| Defaults set | Predictable fields have initial values | Read initial form state |
| All states exist | Focus, error, warning, disabled, loading styles defined for the input component | Read the input component's style variants |
| Focus visible | Focus ring defined, never `outline: none` without a replacement | `grep -n "outline: *none\|outline-none"` |
| Label always visible | A label element, not placeholder only | Each input has `<label>`/`aria-label` |
| Error copy specific | Every validation rule has its own message | Read the validation schema messages |
| Data kept on error | Form state is not reset in the error branch | Read the submit error handler |
| CTA outcome | Label is not "Submit"/"OK"; includes the action and, when known, the count or total | Read the label |
| No double submit | Button disabled or loading while pending | Check the pending flag on the button |
| Two column when sparse | Modal with 4+ short fields uses a grid | Read the layout |
