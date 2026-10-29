# Mental models and conventions

How users predict what an interface will do, and how to design so their prediction is right.

## Contents

1. Three models: design model, system image, user's model
2. Rules for matching the user's mental model
3. Conventions: when to follow, when to break
4. Metaphors
5. Consistency, in levels
6. Words are part of the model
7. Checks

---

## 1. Three models: design model, system image, user's model

Norman separates three things:

- **The design model:** how the designer thinks the system works.
- **The system image:** everything the user can actually perceive (the screen, labels, behaviour, docs).
- **The user's mental model:** what the user believes, built only from the system image plus prior experience.

The user never sees the design model. If the system image does not communicate it, the user invents a different model and makes "mistakes" that are really design failures. NN/g: "Mental models help the user predict how a system will work", and they rest on belief, not fact. Users build them mostly from *other* products. Designers know their own product far better than users and therefore overestimate how understandable it is.

Kenneth Craik (1943) first proposed that people carry a small-scale model of the world in their heads to predict events. The model is compressed: users keep only enough to predict the next step.

## 2. Rules for matching the user's mental model

1. **Write the user's model before the screen.** List the objects and actions as the user would name them. Card sorting (users group items themselves) shows how they organise content; think-aloud testing shows what they believe while using it.
2. **Make the system conform to the user, not the user to the system.** Move content to where users look for it. Example: if users look for "Invoices" under "Billing", put it there even if engineering stores it under "Documents".
3. **If you cannot change the system, improve the user's model** with clearer labels and a visible structure (a diagram beats a paragraph: Tognazzini's HyperCard case, where twenty pages of text failed and one exploded diagram worked immediately).
4. **One search box per screen.** Users treat any search box as universal. Two boxes (for example "search site" and "search catalogue") send queries to the wrong one and users conclude the content does not exist.
5. **Back means "where I just was".** Users expect Back to undo navigation one step. Back in an overlay closes the overlay. Never make Back jump up a hierarchy the user did not walk down.
6. **The user controls what goes into their cart, list or account.** Never pre-add items (insurance, newsletters, add-ons). It breaks the model of "I put things here" and it is a deceptive pattern.
7. **Expect early misconceptions to stick.** A user who forms a wrong idea in the first minute reads everything after through it (mental-model inertia). The first screen must be the clearest.
8. **Status labels describe state, action labels describe outcome.** A switch labelled "Off" next to an action button labelled "Off" is ambiguous. Show the state ("Bluetooth: Off") and the action ("Turn on") as different kinds of text.
9. **Phrase settings positively.** "Show notifications: On", not "Hide notifications: Off". Double negatives break evaluation.
10. **For binary settings that are not instant, prefer a checkbox to a switch.** A switch means "takes effect now"; a checkbox in a form means "applies when I save". Mixing them breaks the model.
11. **Keep the noun before the verb when possible.** Raskin: select the object, then choose the action (noun-verb). Focus returns to the content after the action and no "cancel tool" step is needed. Verb-noun (pick a tool, then apply it) is right only where it is the norm, such as paint tools.

## 3. Conventions: when to follow, when to break

Jakob's Law: users spend most of their time on other products, so they expect yours to work the same way. Every convention you follow is something the user already knows. Every convention you break is something they must learn.

**Follow by default.** Examples of conventions that are effectively mandatory:

- Logo or product name top left goes home.
- Search is a magnifying glass or a field near the top.
- Primary button on the trailing side of a dialog (right in left-to-right languages on Apple and most web); Cancel always labelled "Cancel".
- Close is an X in the top corner of a dialog, sheet or panel. Escape closes it on desktop.
- Blue (or a clearly distinct colour) underlined text is a link.
- Swipe left on a list row reveals delete or archive; pull down refreshes a list.
- Ctrl/Cmd plus Z undoes, plus S saves, plus F finds, plus C, X and V copy, cut and paste.
- Clicking a column header sorts by it; clicking again reverses.
- A field with a red border and red text below it has an error.
- Greyed-out means unavailable. Do not reuse that look for a different meaning (Southwest's calendar greyed out both past dates and unavailable future dates, so the same signal meant two things).

**Break a convention only if all of these are true:**

1. You can write in one sentence what the user gains.
2. The gain is large, not marginal (Raskin: marginal changes rarely pay for the relearning).
3. The new behaviour is taught in context at first use, not in a tutorial.
4. The old way keeps working where possible, or users can switch back for a while (YouTube's 2017 redesign let desktop users preview, give feedback and revert).
5. The deviation is consistent across the whole product.

**Consistency within the product beats consistency with your taste.** Once a pattern is chosen, every screen uses it.

## 4. Metaphors

- A good metaphor transfers a whole structure at once (a trash can you can open again, a desktop, a shopping cart, a map with progress along a path for lessons).
- Metaphors break when taken too literally. Do not limit features to what the physical object can do (an electronic newspaper can have links; skeuomorphism must not cap function).
- Abandon a metaphor that holds the design back (Tognazzini's satellite-dish app: a map metaphor failed in forests where trees look alike; showing the actual satellites in the sky through augmented reality worked).
- Flat abstraction can fail too: two different compass icons on one phone carry no meaning at all.
- A metaphor must be honoured everywhere. If it looks like a trash can, things dropped in it must be recoverable until "Empty trash".

## 5. Consistency, in levels

Tognazzini's levels, from least to most strict:

1. **Platform:** follow the operating system's standards (dialog button order, shortcuts, gestures).
2. **Product family:** shared look across apps from the same maker (the user's Iris apps share one library for this reason).
3. **Single app:** one visual language, fully transferable behaviour.
4. **Small visible structures:** icons, buttons, scroll bars. Strict control over look and position.
5. **Invisible structures:** anything the user cannot see (edge gestures, hover zones). Demand rigid consistency, and avoid them where possible.
6. **Interpretation of user behaviour (strictest):** shortcut keys, learned gestures and button positions must never move. Moving "Next" from bottom right to top right forces users to unlearn a habit.

Two corollaries:

- **Make different things look different (induced inconsistency).** An object that behaves differently must not borrow a familiar look.
- **Make a changed screen look changed,** so users look around instead of applying old habits.

Over versions, aim for *continuity*: a visible thread from the old design to the new, rather than either freezing the design or replacing it wholesale.

## 6. Words are part of the model

- Use the words users use. Internal names ("workspace entity", "tenant", "job") are the designer's model leaking through.
- NN/g on Cisco's headline: terms like NGFW and AnyConnect mean nothing to outsiders. Branded feature names are jargon until the user learns them; pair them with a plain description.
- Label the same thing with the same word everywhere. If it is "Delete" in one place it is not "Remove" in another unless the behaviours differ (remove from list versus delete from disk). When they differ, the words must differ.
- Put the distinguishing word first. Experienced users recognise labels by the shape of their first one or two words (Tognazzini).

## 7. Checks

- Write the nouns and verbs from the screen. Do they match the user's nouns and verbs from step 2 of the method?
- For every non-standard pattern, is there a written reason and an in-context lesson?
- Does any visual signal (grey, red, bold, a badge) carry two different meanings anywhere in the product?
- Is there more than one search field on a screen?
- Does Back always return to the previous view?
- Could a user who knows only the platform conventions predict what every control does?
