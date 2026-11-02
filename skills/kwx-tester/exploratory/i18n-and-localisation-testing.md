# Internationalisation and localisation testing

Internationalisation (i18n) is making the product able to work in any language and region; localisation (l10n) is the actual translation and regional settings for one of them. Testers find i18n bugs long before any translator does, with pseudo localisation, plural checks, formatted numbers and dates, glyph coverage and RTL layouts. This file covers what to test, how an agent tests it without looking at a screen, and the traps for Russian and Kazakh, which the owner's users type every day. Values marked **verified** were run on this machine (Node 24.21 with its bundled ICU, Python 3.14, fontconfig, 2026-10-31).

## Contents

1. The rules that matter most
2. Pseudo localisation
3. Text expansion
4. Plural rules (Russian, Kazakh, ICU MessageFormat)
5. Dates, numbers and currency with Intl
6. Fonts and missing glyphs
7. Right to left layout
8. Sorting, searching and case rules
9. Input methods and keyboards
10. Hard coded text and concatenation
11. Checks

## 1. The rules that matter most

| # | Rule | Why | Evidence |
|---|---|---|---|
| I1 | Run the app in a pseudo locale before any real translation exists. | It shows hard coded strings, clipped text and broken placeholders in one pass, with no translator. | moderate (Android docs, Microsoft and Google practice) |
| I2 | Check every plural message against the CLDR categories of every shipped locale (`Intl.PluralRules(locale).resolvedOptions().pluralCategories`). | Russian needs `one`, `few`, `many`, `other`; English only `one`, `other`. A missing `many` shows "5 привычки". | strong (CLDR is the standard) |
| I3 | Never build sentences by concatenation. Use one message with placeholders. | Word order and grammar differ; "You have " + n + " habits" cannot be translated. | moderate |
| I4 | Format numbers, dates, money and lists only with `Intl` (or the platform's equivalent), never by hand. | Separators, order, week start and calendars vary by locale. | strong (platform docs) |
| I5 | Compare formatted output in tests with the exact characters `Intl` produces, or test the parts with `formatToParts`. | Russian and Kazakh use U+00A0 between digit groups, French U+202F; tests that type a normal space fail. | strong (**verified**) |
| I6 | Check glyph coverage of every font for every script you support (`fc-list ':charset=4d9' family` on Linux). | A font without `ә` draws a box or falls back to a different looking font for one letter. | strong (**verified**) |
| I7 | Normalise user text to NFC before storing and comparing. | Equal looking strings must compare equal (UAX 15). | strong |
| I8 | Use locale aware collation for sorting and locale aware case folding for search. | Default sort orders by code point: Kazakh letters land after `я`. | strong (**verified**) |
| I9 | Design for growth: at least 30 percent longer text, and up to 200 to 300 percent for strings under 10 characters. | IBM's expansion figures, quoted by the W3C. | moderate |
| I10 | Test RTL with a pseudo RTL locale or `dir="rtl"`, even if no RTL language ships yet. | Mirroring bugs are cheap to find early and expensive later. | moderate |

## 2. Pseudo localisation

Pseudo localisation replaces each string with an accented, longer, bracketed version of itself: `Save` becomes `[Sávé····]`. Read the result:

- Text without accents and brackets is hard coded (not in the catalogue).
- A missing closing bracket means the text was clipped or truncated.
- Broken placeholders (`{{náme}}`) mean the pseudo tool or the message syntax is wrong.
- Two bracket groups in one label mean a sentence was concatenated from pieces.

### Android

The platform ships two pseudo locales (Android developer docs): **en-XA** adds accents, expands the text and brackets each message; **ar-XB** reverses text direction to test RTL layout. Enable them in the debug build:

```kotlin
// build.gradle.kts (from the Android docs)
android {
    buildTypes.getByName("debug") {
        isPseudoLocalesEnabled = true
    }
}
```

Then pick "English (XA)" or "AR (XB)" in system Settings, Languages, with developer options on. That step is on the device: hand it to the owner as a checklist item ([human-check-handoff.md](human-check-handoff.md)) if the user's rules forbid the agent to drive the emulator. React Native and Expo apps do not use Android string resources for JS text, so they need a JS pseudo locale (below).

### Web, React Native, Expo (i18next, FormatJS)

Generate a pseudo catalogue from the source catalogue and load it as a locale such as `en-XA`. A minimal generator (**verified**: run on a sample catalogue, placeholders and tags kept intact):

```js
// pseudo.mjs: node pseudo.mjs locales/en.json > locales/en-XA.json
import { readFileSync } from "node:fs";
const map = { a: "á", e: "é", i: "í", o: "ö", u: "ü", c: "ç", n: "ñ", y: "ý", A: "Å", E: "É", I: "Ï", O: "Ø", U: "Ü", C: "Ç", N: "Ñ" };
const pseudo = (s) => {
  const parts = s.split(/(\{\{?[^}]+\}\}?|<[^>]+>)/); // keep placeholders and tags intact
  const body = parts.map((p, i) => (i % 2 ? p : [...p].map((ch) => map[ch] ?? ch).join(""))).join("");
  const pad = "·".repeat(Math.ceil(s.length * (s.length <= 10 ? 1 : 0.4))); // short strings grow most
  return `[${body}${pad}]`;
};
const walk = (o) => (typeof o === "string" ? pseudo(o) : Object.fromEntries(Object.entries(o).map(([k, v]) => [k, walk(v)])));
console.log(JSON.stringify(walk(JSON.parse(readFileSync(process.argv[2], "utf8"))), null, 2));
```

Output for `"Hello, {{name}}! You have <b>{{count}}</b> habits today."` is `"[Héllö, {{name}}! Yöü hávé <b>{{count}}</b> hábíts tödáý.·······················]"`.

An agent can check for hard coded strings without rendering: search the components for string literals in JSX text (`rg -n '>[A-Z][a-z]+[^<{]*<' src --glob '*.tsx'`), or run `eslint-plugin-i18next` (`no-literal-string`) if the project uses i18next. For Kotlin, Android lint flags `HardcodedText`. For QML, look for `text: "` without `qsTr(`.

### Better than accents: real long languages

Pseudo text checks mechanics. Also run once with a real long locale (German, Russian) and a real script locale (Kazakh), because real words do not break where pseudo text does (German compound nouns like `Benachrichtigungseinstellungen` have no break point).

## 3. Text expansion

IBM's guideline for English source text, as quoted by the W3C article "Text size in translation":

| English length (characters) | Typical expansion |
|---|---|
| up to 10 | 200 to 300 percent |
| 11 to 20 | 180 to 200 percent |
| 21 to 30 | 160 to 180 percent |
| 31 to 50 | 140 to 160 percent |
| over 70 | 130 percent |

(The W3C table also lists 51 to 70 as 151 to 170 percent, which looks out of order; do not rely on that row.)

What to test:

- Buttons, tabs, chips and badges with short labels: these grow the most. "Save" (4) can become "Сохранить" (9) or "Speichern" (9); "Settings" becomes "Einstellungen" or "Параметры".
- Fixed width containers, `maxLines={1}` with no ellipsis, `numberOfLines`, `white-space: nowrap`.
- Vertical growth: Thai, Arabic, Devanagari and CJK need more line height; diacritics stacked above capitals (`Ё`, `Й`, Kazakh `Ә` is fine, Vietnamese stacks two marks) get clipped by tight `line-height` or `overflow: hidden`.
- Database and API limits in bytes: a 50 character Russian name is 100 bytes in UTF-8.

Agent check without a screen: for each label, estimate width as characters times average glyph width (about 0.55 to 0.6 of the font size for Latin and Cyrillic proportional fonts) and compare with the container width in code. Report predicted overflows as predictions and put the worst ones on the owner's checklist.

## 4. Plural rules (Russian, Kazakh, ICU MessageFormat)

CLDR defines the plural categories per language. Read them from `Intl`, do not guess (**verified** output):

| n | ru | kk | en | ar |
|---|---|---|---|---|
| 0 | many | other | other | zero |
| 1 | one | one | one | one |
| 2, 3 | few | other | other | two, few |
| 5 | many | other | other | few |
| 11 | many | other | other | many |
| 21 | one | other | other | many |
| 22 | few | other | other | many |
| 25 | many | other | other | many |
| 101 | one | other | other | other |
| 1.5 | other | other | other | other |

- **Russian** has four categories: `one` (1, 21, 101: "1 привычка"), `few` (2 to 4, 22 to 24: "2 привычки"), `many` (0, 5 to 20, 25: "5 привычек"), `other` (fractions: "1,5 привычки").
- **Kazakh** has two: `one` and `other`. In Kazakh, a noun after a numeral stays singular ("5 әдет", not "5 әдеттер"), so both forms are often the same text. That is correct; do not "fix" it by adding the plural suffix. (Language fact, moderate evidence; ask a native speaker when in doubt.)
- Test values for any plural message: **0, 1, 2, 5, 11, 21, 22, 25, 101, 1.5**. These hit every Russian category and the classic "11 is not one" trap.

ICU MessageFormat (FormatJS, `intl-messageformat`, Android `MessageFormat`, Java) writes plurals like this:

```
{count, plural,
  one {# привычка}
  few {# привычки}
  many {# привычек}
  other {# привычки}
}
```

i18next uses separate keys with suffixes `_one`, `_few`, `_many`, `_other` (since i18next v21, based on `Intl.PluralRules`). A completeness check for i18next style catalogues (**verified**: it caught a Russian file that put the 5+ form under `_other` instead of `_many`):

```js
// plural-check.mjs: node plural-check.mjs locales/   (files named <locale>.json)
import { readdirSync, readFileSync } from "node:fs";
import { join, basename } from "node:path";
const dir = process.argv[2];
let bad = 0;
for (const f of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
  const locale = basename(f, ".json");
  const need = new Intl.PluralRules(locale).resolvedOptions().pluralCategories;
  const keys = Object.keys(JSON.parse(readFileSync(join(dir, f), "utf8")));
  const bases = new Set(keys.filter((k) => /_(zero|one|two|few|many|other)$/.test(k)).map((k) => k.replace(/_[a-z]+$/, "")));
  for (const b of bases) for (const c of need) if (!keys.includes(`${b}_${c}`)) { console.log(`${locale}: ${b}_${c} missing`); bad++; }
}
process.exit(bad ? 1 : 0);
```

Other grammar traps: gender agreement ("Вы удалили" vs a past tense that depends on the user's gender: use ICU `select`), cases after prepositions (a name inserted into a Russian sentence may need a different case: avoid by putting names in a neutral position, like "Автор: {name}"), and ordinals ("1st", "2nd" do not exist in that form in Russian or Kazakh: use `Intl.PluralRules(locale, {type: "ordinal"})` or avoid ordinals).

## 5. Dates, numbers and currency with Intl

Facts from this machine (**verified**):

| What | Output |
|---|---|
| `new Intl.NumberFormat("de-DE").format(1234567.891)` | `1.234.567,891` |
| `ru-RU` and `kk-KZ` same number | `1 234 567,891` with U+00A0 between groups |
| `fr-FR` | groups separated by U+202F (narrow no break space) |
| `en-IN` | `12,34,567.891` |
| `kk-KZ` currency KZT 1234.5 | `1 234,50 ₸` |
| `ru-RU` currency KZT 1234.5 | `1 234,50 KZT` (code, not symbol) |
| `ja-JP` currency JPY 1234.5 | `￥1,235` (rounded, 0 minor units) |
| `kk-KZ` full date, 29 March 2026 | `2026 ж. 29 наурыз, жексенбі` |
| `ru-RU` full date | `воскресенье, 29 марта 2026 г.` (genitive month name) |
| `en-US` week info | `firstDay: 7` (Sunday); `ru-RU` `firstDay: 1` (Monday) |

What to test:

- **Parsing user input**, not only display: does the amount field accept `1,5` from a Russian keyboard? Does it accept `1 234` with a normal space and with U+00A0 pasted from a formatted value?
- **Round trip**: format a number, then parse it back with the app's own parser. It often fails on the app's own output.
- **Month names in context**: Russian uses the genitive in dates ("29 марта") and nominative standalone ("Март"). Kazakh month names differ from Russian entirely (наурыз, сәуір, мамыр). Hand built date strings from a month array get this wrong.
- **Week start and weekend** from the locale (`Intl.Locale.prototype.getWeekInfo()`), not hard coded Sunday.
- **Time zone of "today"** (see [edge-case-catalogue.md](edge-case-catalogue.md) section 5).
- **ICU version drift**: `Intl` output changes between ICU versions (the space before AM/PM was U+202F in some versions and is a normal space in Node 24). Snapshot tests of formatted strings break on upgrades; assert on `formatToParts` or on a normalised string.

Run the suite under several locales and zones in CI or locally: `LANG=ru_RU.UTF-8 TZ=Asia/Almaty npm test`. In JS tests, pass the locale explicitly to `Intl` rather than relying on the process default.

## 6. Fonts and missing glyphs

A font that lacks a glyph shows a box (tofu) or falls back to another font, which gives one letter a different weight or height. Kazakh letters are missing from many Latin plus basic Cyrillic fonts, especially display and icon heavy fonts.

The nine Kazakh specific lowercase letters and their code points: ә U+04D9, ө U+04E9, ү U+04AF, ұ U+04B1, қ U+049B, ғ U+0493, ң U+04A3, һ U+04BB, і U+0456. Capitals: U+04D8, U+04E8, U+04AE, U+04B0, U+049A, U+0492, U+04A2, U+04BA, U+0406.

Check coverage on Linux (**verified** command):

```bash
# fonts on this system that cover all nine Kazakh lowercase letters
fc-list ':charset=4d9 4e9 4af 4b1 49b 493 4a3 4bb 456' family | sort -u
# does one specific font cover them? (prints the family if yes, nothing if no)
fc-list 'Inter:charset=4d9 4e9 4af 4b1 49b 493 4a3 4bb 456' family
```

For a font file shipped in an app or website, check the file directly with fontTools (from the fontTools docs): `python3 -c "from fontTools.ttLib import TTFont; import sys; c=TTFont(sys.argv[1]).getBestCmap(); print([hex(x) for x in [0x4d9,0x4e9,0x4af,0x4b1,0x49b,0x493,0x4a3,0x4bb,0x456] if x not in c])" font.ttf` (an empty list means full coverage). Also check the web font subset: Google Fonts and `unicode-range` subsets often include `cyrillic` but put Kazakh letters in `cyrillic-ext`.

Also check: every weight used (a bold file may lack glyphs the regular file has), PDF and email generation (server side fonts differ from the app), and the system font on Android when the app uses the default.

## 7. Right to left layout

For Arabic, Hebrew, Persian and Urdu the whole layout mirrors: navigation, back arrows, progress, text alignment, padding.

In the table, `\|` inside a command is Markdown escaping for the table: type a plain `|` when you run it.

| Platform | How to switch for testing | What to check |
|---|---|---|
| Web | `<html dir="rtl" lang="ar">` | Use CSS logical properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`); `rg -n 'margin-left\|padding-right\|left:\|right:\|text-align: left' src` lists the physical ones |
| Android (Kotlin, Compose) | `android:supportsRtl="true"`, pseudo locale ar-XB | `start`/`end` instead of `left`/`right`; Compose mirrors automatically except custom drawing and some icons |
| React Native | `I18nManager.forceRTL(true)` then reload | `marginStart`/`marginEnd`; icons that indicate direction (back, next, send) must flip; others (play, checkmark, clock) must not |
| Qt/QML | `LayoutMirroring.enabled: true` with `childrenInherit: true` | Anchors and Row order mirror; text alignment |

Also test bidirectional text inside an LTR UI: a Hebrew name in an English list, an English brand in an Arabic sentence, numbers and phone numbers inside RTL text. Use `<bdi>` or `unicode-bidi: isolate` around user content, and check that a user name containing U+202E does not reverse the rest of the line ([edge-case-catalogue.md](edge-case-catalogue.md) section 3).

## 8. Sorting, searching and case rules

**Sorting** (**verified**):

- `["ә","а","б","я","ё","е"].sort()` orders by code point; with `new Intl.Collator("kk").compare` the order is `аәбеёя`.
- Swedish puts `ä` after `z`; German puts it after `a`.
- In Postgres, sort with a collation that knows the language (`ORDER BY name COLLATE "kk-KZ-x-icu"` when ICU collations exist), or sort in the app.

**Searching**:

- Case insensitive search must work for Cyrillic: `ILIKE` and `lower()` work in Postgres for Cyrillic; SQLite's `LIKE` folds ASCII only, so "АЛМАТЫ" does not match "алматы" without the ICU extension.
- Decide whether `ё` matches `е` (Russian users often type е for ё) and test it both ways.
- Kazakh users without a Kazakh layout type look alike Latin or Russian letters: `і` (U+0456) as Latin `i`, `һ` as Latin `h`, `ө` as `о`, `ү` as `у`. Decide in the spec whether search should fold these, then test.
- Normalise both the query and the stored text to NFC before comparing.

**Case rules** (**verified**):

- Turkish and Azerbaijani: `"i".toLocaleUpperCase("tr")` is `İ` and `"I".toLocaleLowerCase("tr")` is `ı`. Code that uppercases identifiers with the user's locale breaks on Turkish devices (the classic "TITLE" vs "TİTLE" bug). Use locale independent case mapping (`toUpperCase()`, `Locale.ROOT` in Kotlin) for identifiers, keys and protocol values.
- Kazakh Cyrillic has no special case rules: `"i".toLocaleUpperCase("kk")` is `I`, and Kazakh `і` (U+0456) uppercases to `І` (U+0406). If the product supports Kazakh in Latin script, test the dotted and dotless i explicitly, because the rules there depend on the alphabet version.
- `"ß".toUpperCase()` is `"SS"` and `"İ".toLowerCase()` is two code points: length changes with case.
- Greek final sigma: lowercasing `ΟΔΟΣ` gives `οδος` with a final `ς`.

## 9. Input methods and keyboards

- **Kazakh layout**: the standard Windows and Linux Kazakh layouts put Kazakh letters on the number row, so digits need a modifier. Fields that react to digit shortcuts, or validate per keystroke, can break. On Linux some users add Kazakh letters with AltGr through a custom xkb file. Test that fields accept these letters from paste as well as typing.
- **IME composition** (Chinese, Japanese, Korean, and some mobile keyboards for any language): text is "composed" before it is committed. Bugs: Enter during composition submits the form; character counters and validation run on uncommitted text; search fires on every composition step. Web check in code: handlers should respect `event.isComposing` or listen to `compositionend`. Test on the device with Gboard (owner checklist).
- **Autocorrect and predictive text**: may change emails, usernames and codes; set `autoCorrect={false}`, `autoCapitalize="none"` and the right `keyboardType`/`inputMode` on such fields, and test that the right keyboard appears (owner checklist).
- **Voice input and paste** insert whole strings at once, bypassing per key handlers.
- **Numeric keyboards** on Android in some locales show a comma, not a dot, as the decimal key. The parser must accept it.

## 10. Hard coded text and concatenation

Search for the common i18n smells in code (adapt the globs):

```bash
rg -n '" \+ |\+ "' src --glob '*.{ts,tsx,js}'          # string concatenation in UI code
rg -n 'toLocaleString\(\)|toLocaleDateString\(\)' src   # no explicit locale
rg -n "toFixed\(" src                                    # number formatting by hand
rg -n "'s\b|s'\)" src --glob '*.{tsx,jsx}'               # English possessive or plural hacks
rg -n 'count > 1 \?|=== 1 \?' src                         # hand made plurals
rg -n 'January|Monday|AM|PM' src --glob '!**/*.test.*'   # hard coded calendar words
```

Each hit is a candidate bug, not a confirmed one; read the context.

## 11. Checks

- [ ] A pseudo locale build (en-XA on Android, or a generated JS catalogue) was produced; hard coded strings and clipped labels were listed (predicted from code, or confirmed by the owner).
- [ ] Every plural message has all CLDR categories for every shipped locale (`plural-check.mjs` or equivalent passes); values 0, 1, 2, 5, 11, 21, 22, 25, 101, 1.5 were tried.
- [ ] No sentence is built by concatenation; names sit in neutral positions or use ICU `select`.
- [ ] Numbers, dates, money and lists are formatted with `Intl` (or platform APIs) with an explicit locale; parsing accepts a comma decimal separator and U+00A0 group separators.
- [ ] Tests that compare formatted strings use `formatToParts` or the exact `Intl` characters.
- [ ] Glyph coverage of every shipped font and weight was checked for Kazakh letters (`fc-list` or fontTools), including server side PDF and email fonts.
- [ ] RTL was tried (`dir="rtl"`, ar-XB, `forceRTL`, or `LayoutMirroring`); physical left and right properties were listed.
- [ ] Sorting uses `Intl.Collator` or a DB collation; search folds case for Cyrillic and the ё/е and look alike Latin letter decisions are tested.
- [ ] Identifiers and keys use locale independent case mapping (Turkish i test passes).
- [ ] Input method items (Kazakh layout, IME composition, numeric keyboard comma) are tested or on the owner's checklist.
