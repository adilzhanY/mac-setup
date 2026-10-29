# Craft lessons from mobile apps known for quality

What award winning mobile apps do that ordinary apps do not, turned into rules. Sources: Apple "Behind the Design" articles on Flighty (Apple Design Award 2023, interaction) and Halide Mark II, MacStories review of Things 3, WWDC18 "Designing Fluid Interfaces". Secondary analyses (blog guides) were read but only primary quotes are relied on.

## Flighty: boringly obvious, strongest when things go wrong

- Goal stated by Ryan Jones: "work so well that it feels almost boringly obvious." Rule: if a screen needs explaining, it is not done.
- Borrow a real world convention that already solved the problem. Flighty copied the airport departure board: "one line per flight ... they've had 50 years of figuring out what's important." Rule: before inventing a layout, look for a physical or industry display that already ranks the information (boards, tickets, dashboards, receipts).
- Design the bad path first: "We really have to shine when things go awry." Delays, cancellations and gate changes get the most care, not the happy path.
- Plan for no network: on takeoff the Live Activity switches to a simple circular progress of flight duration that needs no data.
- Information that is always there beats information you have to check. Live Activities, Dynamic Island and widgets mean the user stops opening the app to compute "how many minutes until boarding".
- Process: draw 20 concepts on one sheet. The ones after the obvious first six or seven are often better. Do not start from the old asset library.

## Halide: a camera, not an app

- Muscle memory is the product: "We need to have consistent gestures. We need to be flexible without changing buttons around all the time." Rule: in a tool used repeatedly, never move a control between modes.
- Controls stay out of the way; advanced features are "never more than a few taps away". Pro depth without the "flight simulator with lots of dials".
- Every control within one thumb's reach on all iPhones; edge gestures for mode switching.
- Color alone failed: a tester shot a whole trip in the wrong RAW state because the yellow "active" tint was ambiguous. Rule: every on/off state differs in shape or fill and label, not only hue. Field test in real conditions (sunlight, travel), not only at a desk.
- Simplify the expert workflow instead of exposing it: Instant RAW processes automatically. "Let's just skip to the part where you create nice photos."

## Things 3: direct manipulation with physical feel

- The Magic Plus button is dragged to where the new item should go: drop in a list position to insert there, on a day in Upcoming to schedule, on the Inbox target to file. Rule: let the place where the user drops something carry the meaning, so one control replaces several.
- Tapping a to-do expands it into a card in place while the list fades back. Rule: edit in context; avoid navigating away for small edits.
- Only a title is required to create an item; everything else can be added later. Rule: minimum required input for creation is one field.
- Haptics on lift, drop and pull to search give a sense of depth (reviewer noted the iPad without haptics felt flatter).
- Swipe right to reschedule, swipe left for selection; drag across selection circles to select many at once.
- Pull down anywhere to search on iOS; on Mac, just start typing ("Type Travel") and search opens.

## Apple's own fluid interface rules (WWDC18)

- Response first: remove every timer and delay in the touch path.
- Interruptible and redirectable motion, one to one tracking, momentum projection, springs by damping ratio, rubber banding, symmetric paths.
- Teach with the interface itself: hints that grow toward the final state, clipped content, grabbers.

## Rules distilled

1. Design the error, delay and offline paths with the same care as the happy path.
2. Steal proven ranking from the physical world before inventing.
3. Keep controls in fixed positions in tools people use every day.
4. Never encode state in color only.
5. Make creation take one field.
6. Edit in place.
7. Put the answer where the user already looks (widgets, Live Activities, notifications) so they do not need to open the app.
8. Sketch at least 20 options before committing to one.
