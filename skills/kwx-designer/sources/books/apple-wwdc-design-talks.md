# Apple WWDC design talks (craft and premium feel)

- **Status:** free. Videos and transcripts on developer.apple.com.
- **Read (transcripts), October 2026:**
  - Essential Design Principles, WWDC17 802: https://developer.apple.com/videos/play/wwdc2017/802/
  - The Qualities of Great Design, WWDC18 801: https://developer.apple.com/videos/play/wwdc2018/801/
  - Designing Fluid Interfaces, WWDC18 803: https://developer.apple.com/videos/play/wwdc2018/803/ (a dedicated file also exists: `wwdc18-designing-fluid-interfaces.md`)
  - The Life of a Button, WWDC18 804: https://developer.apple.com/videos/play/wwdc2018/804/
  - The Details of UI Typography, WWDC20 10175: https://developer.apple.com/videos/play/wwdc2020/10175/
  - Writing for Interfaces, WWDC22 10037: https://developer.apple.com/videos/play/wwdc2022/10037/
  - Animate with Springs, WWDC23 10158: https://developer.apple.com/videos/play/wwdc2023/10158/
  - Add Personality to Your App Through UX Writing, WWDC24 10140: https://developer.apple.com/videos/play/wwdc2024/10140/
  - Meet Liquid Glass, WWDC25 219: https://developer.apple.com/videos/play/wwdc2025/219/
  - Get to Know the New Design System, WWDC25 356: https://developer.apple.com/videos/play/wwdc2025/356/
  - Make a Big Impact with Small Writing Changes, WWDC25 404: https://developer.apple.com/videos/play/wwdc2025/404/
  - Principles of Great Design, WWDC26 250 (Linda Dong, Doug LeMoine), via the WWDC Notes summary: https://wwdcnotes.com/documentation/wwdc26-250-principles-of-great-design/
- **Who recommends them:** Anthony Hobday's curated list "The best WWDC videos about interface design" (https://anthonyhobday.com/blog/20220614) includes all of the 2017 to 2025 talks above; Emil Kowalski built his public "apple-design" skill from Designing Fluid Interfaces and The Details of UI Typography.

## Principles of Great Design (2026): the eight principles

1. **Purpose:** decide whether it should exist; "design through subtraction"; every feature costs time, attention and trust.
2. **Agency:** let people do things their way; never block; offer choices; forgiveness (easy undo, confirm only destructive actions).
3. **Responsibility:** privacy (ask at the moment of need, only what is necessary, say why); anticipate misuse and harm, especially with AI output; add previews, confirmations, disclaimers; remove a feature whose risk outweighs its value.
4. **Familiarity:** use real world experience and conventions; metaphors neither too literal nor too abstract; never repurpose an established metaphor (trash means delete); things that look the same behave the same and stay in the same place.
5. **Flexibility:** contexts, devices, abilities; tailor to the platform (quick touch on phone, deep work on Mac); let people personalize where one layout cannot fit all.
6. **Simplicity, not minimalism:** remove the unnecessary; one hidden control is minimal, not simple; concise and clear; every element earns its place; sometimes adding context (time remaining on a play button) is simpler.
7. **Craft:** attention to detail shows care. Poor craft: laggy buttons, jittery scrolling, misaligned icons, layouts that break on rotation. Good craft: fonts that look good across devices, colours that adapt to light and dark, clear iconography, fluid animations with immediate natural feedback. Quality comes from iteration.
8. **Delight:** not confetti added at the end; the natural result of the other seven; choose the emotion (relaxed, confident, excited) and reinforce it.

## The Qualities of Great Design (2018)

Quality is "considered and intentional" ("nothing is random"), the result of "time, effort, and care", "not painful to use", "feels like someone thought of you", keeps attention on the task, "your intentions are felt", earns trust by keeping its promise at every touchpoint, and recedes: "you're very aware of an interface which has been poorly designed, and you're not at all aware of an interface which has been well designed." Four aspirations: simple, stunning ("the best apps appear visually perfect", swipe animations line up with gestures), timeless ("a little less trendy and definitely more durable"), positive impact. Practices: prototype and test in context, stay open to critique, know that you do not know.

## Essential Design Principles (2017)

Wayfinding (where am I, where can I go, what is here, how do I get out); feedback (status, completion, warning, error; prevent errors with inline validation, Things 3 turns June 31 into July 1); visibility versus clutter; consistency (external platform conventions, like the iOS share glyph; internal: limited fonts, sizes and colours); mental models (the faucet: a logically better design that breaks expectations fails); proximity; grouping; mapping (if a control needs a label, mapping is weak; direct manipulation is the best mapping); affordance (a shadow under a slider knob says it moves); progressive disclosure (show the 20% that gives 80% of value); symmetry (reflectional, rotational, translational). Principles conflict; balance them for the context.

## Designing Fluid Interfaces (2018)

People are very sensitive to latency; look for delays everywhere. Fully redirectable, interruptible interfaces: "The thought and gesture happen in parallel." Pause detection by acceleration, not timers. Spatial consistency: symmetric paths in and out. Hint toward the final state. Small input, big output (momentum). Rubber banding at edges. "It's not just about framerate. It's what's in the frames" (motion blur, stretch). Springs: start at 100% damping (no overshoot); 80% when the gesture had momentum (Music swipe to dismiss); tap to open uses 100%. Think in damping ratio and response, not duration. Project momentum with scroll deceleration to pick the target. Highlight on touch down, act on touch up, extra hit margin, drag off to cancel. 1:1 tracking keeping the grab point. Velocity from touch history. Detect gestures in parallel, then cancel losers. Hysteresis about 10pt. Double tap delays single taps by about half a second. "The interactive demo is worth a million static designs."

## The Life of a Button (2018)

Buttons are indirect controls; design the button and the action separately. Three phases: before touch (perceived affordance, a label that states the action: "Make toast" not "Toast"), during touch (instant highlight, no slow fades, hit area larger than visual, drag to cancel), after lift (feedback on both the button and the action; text plus visual change; give stop its own button rather than swapping the label). Sound optional; frequent controls need very short quiet sounds; coordinate visual, haptic and sound. Test in the real context of use.

## The Details of UI Typography (2020)

Optical sizes: SF Text under 20pt, SF Display at 20pt and up; variable SF Pro transitions between 17 and 28pt. Tracking is size specific; Apple publishes tracking tables; a tight table for tightening before truncation. Kerning is per pair and rarely touched. Line height includes leading; tall scripts get more; tight and loose variants are minus or plus 2pt (watchOS 1pt), body 17pt on 22pt (tight 20, loose 24). Text styles are size + weight + leading; emphasized styles use bold traits (title1 emphasized = 28pt Bold; body emphasized = 17pt Semibold on iOS, 13pt Semibold on macOS). Support Dynamic Type for custom fonts and scale padding with text. Use system fonts and text styles; override only for exceptional cases.

## Animate with Springs (2023)

Two parameters: perceptual duration and bounce (-1 to 1). Default bounce 0. 0.15 brisk, 0.3 noticeably bouncy, over 0.4 use with caution. Pick duration first, then bounce. Springs are the only curve that keep position and velocity continuous from rest or from a gesture; ease curves halt abruptly after a gesture; linear has velocity jumps. Retargeting keeps current velocity. Do not wait for settling time; use the perceptual duration. Conversion with mass 1: stiffness = (2 pi / duration)^2; damping = 1 - 4 pi bounce / duration for bounce >= 0, and 4 pi / (duration + 4 pi bounce) for bounce < 0.

## Writing (2022, 2024, 2025)

PACE: purpose, anticipation, context, empathy. Lead with the most important thing; headers and buttons work alone; say what comes next. Anticipate the likely choice and the next question. Instructions where the eye is. Alerts name the action, no Yes/No; careful with "Cancel"; destructive marked. Errors: say the problem and the fix with action buttons; avoid oops, sorry, please. Empty states explain what will appear. Plain language, localizable, labelled for VoiceOver by intent. Voice is constant (Apple's: clarity, simplicity, friendliness, helpfulness); tone dials those up and down by situation. Define voice from adjectives grouped into themes. Cut filler adverbs, interjections and repetition; lead with the why ("To get updates, enter your phone number"); keep a word list; direct headlines; read aloud.

## Liquid Glass and the new design system (2025)

Glass is for the navigation layer floating above content; never in the content layer; never glass on glass; elements on glass use fills and vibrancy. Glass adapts continuously; small elements flip light and dark, large ones do not; bigger glass is thicker. Regular (default) versus Clear (needs dimming; only over media rich content with bold content on top); never mix. Tint only the primary action; "When every element is tinted, nothing stands out." Glass materializes by bending light, not fading. Accessibility: reduced transparency, increased contrast, reduced motion. Concentricity: fixed, capsule (radius = height / 2), concentric (parent radius minus padding); pinched or flared corners mean it is not concentric; capsules for touch and standout actions, rounded rectangles for dense desktop controls. Hierarchy through layout and grouping, not decoration; remove custom bar backgrounds and borders. Group bar items by function and frequency; the primary action stays separate and tinted. Scroll edge effects replace dividers: soft (default) or hard (dense desktop, pinned headers), one per view. Type is bolder and left aligned in key moments. Action sheets spring from their source.

## Used in

All files in `../../premium/`, especially `motion-and-feel.md`, `typography-craft.md`, `materials-depth-light.md`, `copywriting-and-tone.md`.
