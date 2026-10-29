# Designing a whole set and keeping it consistent

A set feels premium when it "feels as if it were designed by one hand" (Atlassian's goal). That comes from a fixed order of work and from checking icons in company, never one at a time: every common fault (stroke drift, a circle that looks small, a dense icon that looks dark, a near duplicate) is invisible on one icon at large zoom and obvious on a contact sheet at real size.

## Contents

1. Inventory: what needs an icon
2. Brief and metaphor research
3. The seed set
4. Expanding the set
5. Testing
6. Lint and review
7. Naming and metadata
8. Set level mistakes

---

## 1. Inventory: what needs an icon

1. **Audit what exists.** Search the codebase for every icon in use and its source:
   - Web: `rg -n "lucide-react|@heroicons|react-icons|<svg|Icon\b" src`
   - QML: `rg -n 'MaterialSymbol|text: "iris_|\.svg"' ~/.config/quickshell/ii`
   - Native: asset catalogs (`*.xcassets`), `res/drawable*/ic_*.xml`.
   Atlassian's audit found 1,000+ team-drawn icons with conflicting meanings; yours will find duplicates too.
2. **List every concept** in a table and keep it in the project:

| Concept | Kind | Where shown | Size | Label | Source | Metaphor | Status |
|---|---|---|---|---|---|---|---|
| Search | verb | top bar | 20 | no (universal) | pack, retuned | magnifier | done |
| Deck | noun | sidebar, deck card | 20, 24 | yes | custom | stack of cards | recognition test |
| Day done | noun + state | calendar cell | 16 | no, tooltip | custom | calendar + check badge | seed |

3. **Mark each concept verb or noun.** Verbs (search, close, share, delete, edit, settings, chevrons) keep the conventional metaphor, redrawn or retuned to spec. Nouns (the product's own objects, states and features) get custom drawings.
4. **Apply the restraint test to every row** (Hicks): remove the icon in your head; if the screen works as well without it, cut the row. Cut icons that are pure decoration, repeated so often they lose meaning, or crowded together. Keep a label on everything except the universal few.
5. **Ask the five brief questions per row** (Hicks): What is it for (action, warning, wayfinding)? What is its context and size? Who is it for? Is there a single message ("history", not "history of support requests")? Does it need to be an icon, and does it need text?

## 2. Brief and metaphor research

**Convention first, always.** Familiarity is what makes an icon work, and variations of a standard are recognised less than the standard itself (Iconglobe's test of four "information" symbols, cited by Hicks).

1. Search the platform and pack vocabularies first:
   - Apple's standard icons and SF Symbols names (HIG Icons lists copy, paste, share, delete, undo, search, filter...).
   - Material Symbols names.
   - Lucide tags, locally: `python3 -c "import json;t=json.load(open('$HOME/.local/share/lucide/package/tags.json'));q='calendar';print([k for k,v in t.items() if q in k or q in v])"`
   - The Noun Project and image search for photos of the real object, to see how others draw it.
2. If a convention exists, use it unless one of Hicks's three exceptions applies: a licence or trademark blocks it, it clashes with another icon in the same set (the magnifier for both search and zoom), or it carries a negative meaning for the audience (an owl means wisdom in the west, stupidity in parts of Asia; thumbs up is obscene in Iran).
3. **No convention: invent with a mind map.** Write the concept in the middle, branch out every association, and sketch (or describe as primitives) at least five candidates. Hicks's "view" map gave glasses, eye, binoculars, magnifier.
4. **Score each candidate** on the four checks Hicks used to pick binoculars, plus size:
   - unique profile, not confusable with any other icon in this set;
   - a familiar object that renders without looking like something else (no weight that reads as a handbag);
   - no negative or cultural connotation for the audience;
   - one meaning, without too many alternatives;
   - enough detail to read at the shipped size, and no more ("a padlock can still be recognisable at 8px, but a train doesn't stand a chance").
5. Avoid letters (they do not translate; the "i" for information is the rare exception), body parts and hand gestures, flags for languages, and any familiar shape used in an unfamiliar way (Adobe: never an arrow that does not mean direction).
6. Write the decision in the inventory table: the metaphor in one sentence and why it won.

## 3. The seed set

Before drawing the whole set, draw a seed set that exercises every rule in the spec, and test it in the real UI. Atlassian only found that its bold brand style overpowered the product once the icons sat in the actual apps.

The seed set (no source prescribes a size; this mix covers every rule):

1. The reference **circle** and **square** keyshapes (`construction-spec.md` section 2). They stay in every contact sheet.
2. One icon with a **badge** (sets the badge slot for the whole set).
3. One with a **diagonal** (sets how 45 degree strokes look).
4. One with an **inner gap or counter** (tests the 2 unit gap at 16 px).
5. One **organic** form (a leaf, a flame, a person; tests curves against the straight icons).
6. The **densest** icon you expect (tests the detail ceiling).
7. The **filled twin** of one icon (sets the state rule and the knock-out size).

Place them in a mock of the real screen next to real text at real size, light and dark (section 5). Change the spec now if needed: after 40 icons it is too late.

## 4. Expanding the set

- **Reuse base geometry byte for byte.** When ten icons share a document body, copy the same `<rect ...>` line into each. Never redraw a near duplicate (Adobe; Lucide: keep base shapes unchanged in geometry, placement and orientation).
- **Badges stay in one slot** at one size (bottom right, inside 14..22), on every base.
- **Draw in company** (Hicks): work on the whole family at once and rerun the checker on all of it after every new icon. Draw related icons together in one pass (`arrow-up` with `arrow-down`, all calendar variants), so they share decisions.
- **Draw in context**: check each icon on the background it will sit on (toolbar colour, photos, dark mode), not only on white.
- **Keep drafts.** Move rejected versions to a `drafts/` folder instead of deleting them; an early version of an organic form is sometimes the best one (Adobe, Hicks).
- **Keep the stroke master.** The source SVG keeps live strokes. Expanded outlines (for SF Symbols or some font pipelines) are generated at build time, never edited by hand.
- **Coverage first**: draw the inventory in order of how often users see each icon (navigation and primary actions first), since that is where the set is judged.

## 5. Testing

Run all of these on the seed set, and the automated ones on every new icon.

### 5.1 Automated checks (every icon, every time)

```bash
S=~/.claude/skills/kwx-designer
python3 $S/scripts/icon_check.py $S/icons/examples/ref-circle.svg $S/icons/examples/ref-square.svg icons/*.svg --sheet /tmp/sheet.png
```

0 errors; every warning fixed or justified in one line (the reference circle always warns about its 1 unit overshoot; that is by design). Open the sheet with the image reader.

### 5.2 Family weight: the blur and squint test

Lucide blurs each icon at its intended size and compares it with the reference circle and square; Atlassian squints at the set. The agent version:

- Compare `coverage` at 24 px across the family. Outline icons in one set should sit within a narrow band; the reference circle is about 22% and the square 24%, and 250 Lucide icons spread from 16% (10th percentile) to 34.5% (90th). An icon far outside its family's band looks lighter or darker.
- Blur the contact sheet and read it: `magick /tmp/sheet.png -blur 0x2 /tmp/sheet-blur.png`. In the blurred image every icon should be a similar grey blob of similar size. A darker blob is too dense; a smaller blob does not fill its keyshape.

### 5.3 Real size, light and dark

- The contact sheet shows each icon at 48 and 24 px on light and on dark. Look at the 24 px tiles, not the 48 px ones, to judge.
- Render at the exact size the product uses, including UI scaling: `resvg -w 26 -h 26 icon.svg out.png` for 24 px at scale 1.1 (26.4 rounds to 26).
- Check contrast: icons that carry meaning need 3:1 against their background (WCAG 2.2, 1.4.11 Non-text Contrast). Measure with a tool, "Do not rely on your perception" (Adobe).
- Check that selected and resting states differ by fill, not only colour, on both themes.

### 5.4 Next to text

Render the icon beside its real label at real size and look at weight and alignment:

```bash
FONT=$(fc-match -f '%{file}' "Open Runde:style=Regular")
resvg -w 20 -h 20 lock.svg lock20.png
magick -background white \( lock20.png -flatten \) \( -size 8x20 xc:white \) \
  \( +size -font "$FONT" -pointsize 16 -fill black label:"Private" \) \
  -gravity center +append -bordercolor white -border 12 -scale 300% strip.png
```

(`+size` matters: without it the label inherits the 8 by 20 spacer size and is cropped.) The icon's stroke should look as heavy as the letter stems or slightly heavier, and its centre should sit on the middle of the capital letters. On this machine the house lock at 20 px next to 16 px Open Runde reads slightly heavier than the text, as the stem arithmetic predicts (1.24 times).

### 5.5 Recognition (new metaphors only)

NN/g separates four tests; run the ones that fit:

1. **Recognition**: show the icon alone, no label, no UI, and ask what it is. If the guesses miss, abandon the metaphor and start again rather than tweaking it.
2. **Information scent**: minimal context ("this is a flashcard app"), ask what clicking it would do.
3. **Findability**: the icon in the full screen, measure time and first click. Wrong first clicks mean icons look too alike.
4. **Attractiveness**: show the whole family, ask which icon is liked most and least. This catches the one or two weak members of a set.

The agent version of Sebastiaan de With's "mom test": give a fresh subagent with no context only the rendered PNG (or the ASCII picture) and ask "what does this icon represent, and what would clicking it do?" Treat a miss as a failed test. Then ask the user, who is the real test.

## 6. Lint and review

- `icon_check.py` is the lint: root attributes, allowed elements, geometry only children, precision, grid, padding, gaps, counters. It enforces what Lucide's `lint:icons` enforces, plus raster checks.
- Run it on the whole family, not only the changed icon, so the sheet always shows the family.
- **Every change to the set ships with its contact sheet** (Lucide requires screenshots on every icon PR). Show the user the sheet, not single icons.
- One approver for the whole set (Streamline: an art director approves, at most two designers make corrections). For an agent, the approver is the user; never call a set finished without their look at the sheet.
- Review the whole set again whenever ten new icons have been added, with the most liked and least liked question.
- Record every defect the user reports in the project's mistakes list with its cause and the check that catches it (for this user: `~/.claude/ui-designer/mistakes.md`).

## 7. Naming and metadata

- File names: lowercase kebab case, American spelling, `.svg`.
- **Name multi purpose icons by the picture** (Lucide, Atlassian): `floppy-disk`, not `save`; `globe`, not `language`.
- **Name single purpose product icons by the concept** (Atlassian): `deck`, `work-item`, `day-done`. A product set may name files by picture and add the meaning as an alias.
- Order: group first, then modifier (`calendar-check`, `calendar-plus`), largest element first (`moon-star`), alternates by their visual difference (`send-horizontal`, never `send-2`). Numbers only when drawn (`clock-3`).
- State and size suffixes: `-filled` for the filled twin, `-16` for a separate 16 master. Never put a state in a different file name pattern.
- Keep a metadata sidecar so the set stays searchable and duplicates are caught before drawing:

```json
{
  "deck": {
    "meaning": "a flashcard deck the user studies",
    "tags": ["cards", "stack", "study", "flashcards"],
    "kind": "noun",
    "variants": ["deck", "deck-filled"],
    "used_in": ["sidebar", "deck card header"]
  }
}
```

Tags: lowercase, single words, synonyms and contexts, never the name itself or the word "icon" (Lucide metadata rules).

A real local example of a hybrid set's naming: the user's shell maps Material Symbols names to Lucide glyphs in `~/.local/share/lucide/aliases.json`, and every custom glyph is `custom/iris-<name>.svg`, aliased as `iris_<name>` in `aliases.json` and `manual-map.json`, then built into the font (README in `~/.local/share/lucide`).

## 8. Set level mistakes

- Small variations in stroke weight or radius between icons (the classic fault, Noun Project).
- Circles drawn the same size as squares and looking smaller; dense icons looking darker (Adobe, Lucide).
- Near duplicate base shapes instead of reused ones (Adobe).
- One glyph with two meanings, or two glyphs for one meaning (Atlassian).
- A product noun that looks like a known verb (the deck that read as "copy" in `drawing-svg-by-hand.md`).
- A brand style dropped into UI glyphs, overpowering the interface (Atlassian).
- Icons everywhere: every nav item, card and heading (Linear's 2026 refresh removed them; Hicks's "Christmas tree").
- Hover only labels on icon only controls (fail on touch, NN/g).
- Hard-coded colours that break theming (Lucide).
