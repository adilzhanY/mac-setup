# Defaults and choice

Every blank field is a decision the user must make before anything happens. Stacked decisions lead to no decision, and the user leaves. The job of this file: turn "fill this out from scratch" into "scan and adjust what does not fit".

## Contents

1. Why it works
2. Rules for defaults
3. Rules for the number of options
4. Replace inputs with direct controls
5. Presets from real data
6. Before and after: the table booking screen
7. Where defaults are forbidden
8. Checks

---

## 1. Why it works

- **Decision fatigue**: each empty field costs a decision. "Blank = Friction" (uxpeak, UX psychology video).
- **Choice overload**: 24 jam flavours, 3% bought; 6 flavours, 30% bought (Columbia jam study as cited by uxpeak; replications are mixed, so read it as a direction). "More choices doesn't mean better. It means harder."
- **Default effect**: "70 to 90% of users in most products never change the default values" (uxpeak, no source named). Not laziness, trust: a default reads as "this is what most people pick".
- **Hick's law in practice**: fewer visible options, faster choice.

## 2. Rules for defaults

1. For every input, ask: do we know the most common answer? If yes, preselect it. Date = today or tomorrow, guests = 2, seating = the usual choice, time = the most popular slot. "Don't make users think when you already know the answer."
2. Show the default as a real value in full contrast text, not as grey placeholder text. A placeholder looks empty and is read as empty.
3. Mark recommended values explicitly: a small accent "Popular times" tag on the label row, or a "Most common" badge on the option. Only when it is measured.
4. Drop every field that is not needed to get a result. The booking redesign removed "Occasion" completely.
5. Enable the primary button on first paint once defaults make the form valid. A disabled grey CTA on load tells the user "you have work to do".
6. The primary button states the outcome and a number: "Search 12 Available Tables", not "Search". The count comes from real data.
7. Give filled sections a visible state change: the section icon turns from grey to the accent colour once it has a value.
8. Defaults remember the user: after the first booking, the default is their last choice, not the global most common.

## 3. Rules for the number of options

1. Show the 4 to 6 most likely options. Put the rest behind "View all" (the booking screen shows 4 time chips plus a full width outline "View All Times" button with a clock icon).
2. A wall of 8 or more chips (Anniversary Special Dish, Outdoor Heater, Kitchen View, Pet Friendly Area...) is an exit sign. Collapse it.
3. For a tab bar: 3 or 4 items is ideal, 5 is the hard limit (Kole Jain, mobile UI).
4. For pricing: 3 to 4 plans, not 5 (Kole Jain, vibe coded SaaS).
5. When the list must be long (countries, fonts), give search at the top and the 3 to 5 most used at the start.

## 4. Replace inputs with direct controls

When the option set is small, a direct control beats a dropdown or a text field, because the options are visible and one tap picks one.

| Data | Control | Example from the videos |
|---|---|---|
| 4 to 6 likely values from many | Chips, one preselected, plus "View all" | Time: 6:00 / 6:30 / 7:00 / 7:30, 7:00 selected |
| A small count | Stepper: minus, big bold value, plus | Guests: "- 2 +" |
| 2 to 4 categories | Icon tiles, one preselected | Seating: Indoor / Outdoor / Bar |
| A quantity with a unit | Stepper with the unit inside | "- 3 kg +" (uxpeak, strawberry redesign) |
| A common choice set with names | Preset tiles with label and price | 0.5 kg Snack $3.10, 1 kg Regular $6.20, 2 kg Family $12.40, 3 kg Party $18.60 |
| A main goal | Single select list, the most common preselected | "Lose weight" preselected; "Large gym" with a "Most common" badge |

Selected state: light accent fill plus accent border. Unselected: white (or surface) with a hairline border.

## 5. Presets from real data

- Base presets on what people actually choose (the strawberry video shows a "30% 1 kg" chip: the most bought size). Name them in plain words ("Snack", "Regular", "Family", "Party") with the price on each.
- Keep the free control (stepper, custom input) next to the presets for flexibility.
- Presets cut many taps to one: "a small UX improvement with a real business impact".

## 6. Before and after: the table booking screen (uxpeak)

| Before | After |
|---|---|
| Five stacked empty fields: DATE, TIME, GUESTS, SEATING, OCCASION, grey placeholders ("Select date"...) | DATE: "Tomorrow, Fri 25 Mar" in dark text |
| | TIME: four chips, 7:00 preselected, "POPULAR TIMES" tag, "View All Times" |
| | GUESTS: stepper "- 2 +" |
| | SEATING: three icon tiles, Indoor preselected |
| | OCCASION: removed |
| Disabled grey-blue "Search Available Tables" | Enabled accent "Search 12 Available Tables" |
| Section icons grey | Section icons accent once filled |

Other examples shown: a ride app with "Economy" preselected and the CTA "Select Economy"; a restaurant app with "Tomorrow 08 Aug" and "Dinner" preselected.

## 7. Where defaults are forbidden

A default is a recommendation, so it must be one the user would make for themselves. Never preselect:

- marketing or newsletter opt in, data sharing, tracking consent;
- a paid add on, insurance, donation, or a more expensive tier;
- auto renewal of a trial without saying so in the button label;
- a destructive option (delete, overwrite) in a confirm dialog.

The default focus in a destructive confirm dialog is the safe option (Cancel).

## 8. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Known answers preselected | Every input with a predictable answer has an initial value | Read initial state / `defaultValue` / `useState(...)` for each field; none is `""` or `null` where an answer is known |
| Defaults are values, not placeholders | Default renders in body text colour | Field has a value, not only a `placeholder` attribute |
| Visible options | No group shows more than 6 options without "View all" | Count items in each chip/radio array rendered at once |
| CTA enabled on first paint | `disabled` is false with defaults | Trace the `disabled` expression with initial state |
| CTA states the outcome | Label is verb + object, ideally with a real count | Read the label string; a bare "Submit"/"Search" fails |
| No forbidden defaults | No consent, paid or destructive choice is pre ticked | `grep -nE "checked|defaultChecked|: true"` near consent, add on, newsletter fields |
