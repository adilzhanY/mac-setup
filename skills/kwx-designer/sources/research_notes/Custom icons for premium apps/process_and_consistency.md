# Designing a custom icon set and keeping it consistent: process and quality checks

Note on format: each finding ends with its source link. Where a finding comes only from a search snippet (the page itself could not be opened), it is marked "(snippet)".

## 1. What is the end to end process (inventory, metaphors, sketching, style definition, seed set, expansion, testing)?

### Takeaway
The working method shared by Adobe, Atlassian, Streamline, Lucide and NN/g is: audit and list what the product needs, research the existing conventions for each concept, pick familiar metaphors, define the style rules early (grid, stroke, radius, caps, keyshapes, badge slot), draw a small reference set that fixes those rules, then expand by reusing the same base shapes and reviewing every new icon against the set and at real size. No primary source names a fixed "seed set of 5 to 10 icons"; the closest documented equivalents are Lucide's `circle` and `square` reference icons for weight and Adobe's "core keyshapes" that set proportions for the whole set.

### Cited Findings
**Inventory and audit**
- Atlassian's rebuild started from an audit: the legacy system had more than 350 icons built over six years by different teams, and an audit of Atlassian apps found over 1,000 custom icons "of varying quality and consistency" living in isolated repos. [Atlassian Design, Sanderson-Harris, Bauer, Campbell, Sep 2025](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Atlassian built a custom extractor that scans repos for SVGs, screenshots them and generates a document for manual review, i.e. the inventory was tooled, not done by hand. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Noun Project advises defining the subject first (what message the set conveys and how it will be used) and keeping a set to "one singular, unifying topic". [Noun Project blog, Jeremy Elliott](https://blog.thenounproject.com/?p=8558)

**Brief and metaphor research**
- Adobe: start by identifying how the icon helps the user complete a task, then translate that action into a visual metaphor; research existing metaphors on Noun Project, Iconfinder or Google Images; use familiar metaphors and do not use familiar shapes (like arrows) in unfamiliar ways. Example: a paperclip for "attach" combines two familiar concepts. [Adobe Design, How to design effective icons, Part 1](https://adobe.design/ideas/how-to-design-effective-icons-part-1)
- NN/g: research competitor icons and the conventions of your target platforms first; keep icons simple and schematic. [NN/g, Aurora Harley, Icon Usability, 2014](https://www.nngroup.com/articles/icon-usability/)
- NN/g's designer side "5 second rule": "if it takes you more than 5 seconds to think of an appropriate icon for something" it probably will not communicate that meaning well (a signal to use a label instead). [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Universal icons are rare: only home, print and the magnifying glass for search were found to be widely recognised; heart and star mean different things on different sites. [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Atlassian split icons into single purpose icons, named for the concept (for example "Share"), and multi purpose icons, named for what they look like (for example "globe"), because the same icon carried different meanings across products. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Streamline's recognisability criterion: "It's not about being conventional, it's about being functional." Wi-Fi symbol reads clearly; a router drawing confuses. [Streamline blog, How to create the perfect icons](https://blog.streamlinehq.com/evaluating-icons/)
- Susan Kare continues to "place a premium on context and metaphor". [AIGA, 2018 Medalist Susan Kare](https://www.aiga.org/membership-community/aiga-awards/2018-aiga-medalist-susan-kare) (snippet)

**Sketching and construction**
- Kare started the original Macintosh icons on the smallest graph paper she could find, mocking up 32 x 32 pixel images at Andy Hertzfeld's suggestion, then moved to a rudimentary on screen editor that worked "pretty much" like clickable graph paper. [Stanford, Interview with Susan Kare, 2000](https://web.stanford.edu/dept/SUL/sites/mac/primary/interviews/kare/trans.html) (snippet)
- Kare described the process as "definitely an iterative process". [VentureBeat](https://venturebeat.com/business/macintosh-icons-susan-kare) (snippet)
- Adobe's "scrapbook" approach: mask overlapping areas to test look and feel before building final shapes; natural forms (drops) take extra time, so iterate and keep duplicates because an early version may be the best. Work at 3200% zoom for editing and keep a second window at 100% to check the real result. [Adobe Design, Part 1](https://adobe.design/ideas/how-to-design-effective-icons-part-1)

**Defining the style**
- Adobe: define the style early (corner radius, size, colour, stroke weight, end caps, modifiers and internal proportions); add a 1 to 2 px safe space; reuse existing shapes (arrows, rectangles, plus) rather than near duplicates; plan badges early with a defined cutout and consistent placement because sets grow. [Adobe Design, Part 1](https://adobe.design/ideas/how-to-design-effective-icons-part-1)
- Adobe: use the core keyshapes (circle, square, rectangle, triangle) to set proportions for the whole set and establish key metaphors early. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Atlassian compared three styling options in context before choosing one, and found that the bold brand shapes overpowered the UI once placed in the actual apps, so the UI set uses lighter outlined forms. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Noun Project: start with an icon grid, symmetrical guides and buffer white space; choose outline or filled, minimal or detailed to suit end use. [Noun Project blog](https://blog.thenounproject.com/?p=8558)

**Concrete style specs published by open sets (useful as reference values)**
- Lucide: 24 x 24 canvas, at least 1 px padding to the edge, 2 px centred stroke, round joins and caps, corner radius 2 px for shapes 8 px or larger and 1 px for smaller ones, at least 2 px gap between elements, match the optical weight of the `circle` and `square` reference icons, centre visually not just geometrically, prefer simple arcs, snap to the pixel grid where it does not hurt recognition, reuse base shapes unchanged. When rules conflict: clarity, visual balance, then consistency with the library. [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)
- GitHub Octicons: draw every icon twice (16 px and 24 px), 12 px only when 16 px will not work; 1.5 px stroke at both sizes; round caps and joins; 1 px corner radius by default, 0.25 px on small filled elements; 1 px gap between overlapping objects, 1.5 px around modifiers; 2D unless depth aids recognition; align the outer edges of shapes to pixels; line arrowheads unless there is no room. [Primer, Octicons design guidelines](https://primer.style/foundations/icons/design-guidelines)
- Atlassian 2025: moved from a 2 px stroke on 24 px to a 1.5 px stroke on a 16 px canvas with stroke edges on the pixel grid, plus 12 x 12 downscaled versions for compact contexts. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Adobe: standard sizes 16, 18, 20 or 24 px, think in multiples of four; corner radius 0 to 4 px for workflow icons; stroke 1 to 1.5 px for minimal styles and 2 px for bolder ones. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Streamline micro icons use a 10 x 10 grid; its "Sharp" style uses straight ends and pointed corners. [Streamline blog](https://blog.streamlinehq.com/evaluating-icons/)
- Phosphor is drawn on a 16 x 16 grid in six weights (thin, light, regular, bold, fill, duotone), with an icon grid shipped so users can draw matching additions. [Framer marketplace listing](https://marketplace.development.framer.com/marketplace/vectors/blah) (snippet, secondary)

**Expansion**
- Lucide: keep base shapes from existing icons unchanged in geometry, placement and orientation, and keep add ons (badges, modifiers) consistent in size and placement. [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)
- Lucide: group related icons in one PR (for example `arrow-up` with `arrow-down`) and keep unrelated icons in separate PRs. [Lucide CONTRIBUTING](https://github.com/lucide-icons/lucide/blob/main/CONTRIBUTING.md)
- Adobe: keep a version of each icon "with its vector stroke intact", since expanded strokes make later resizing and weight changes hard. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)

### Inferences
- A practical seed set is the reference shapes (circle, square, a wide rectangle) plus a handful of icons that exercise every rule at once: one with a badge, one with a diagonal, one with an inner gap, one organic form, one dense icon. Lucide's `circle` and `square` references and Adobe's keyshapes are the documented core of this idea.
- The order matters: test the style in the real UI before expanding (Atlassian's lesson that the brand style overpowered the product only surfaced in context).

### Gaps
- No primary source found that prescribes a specific seed set size (5 to 10). This is common workshop advice but I found no citable expert source.
- Streamline's long form "Designing icon sets: a masterclass" (Vincent Le Moign, Medium, Dec 2022, after 43 sets and 150,000+ icons) exists but its content could not be retrieved, so its steps are not reported here.
- Jon Hicks's talk slides "The Principles of Icon Design" (2010) are a 17 MB PDF linked from [hicks.design](https://hicks.design/journal/principles-of-icon-design); not read.

## 2. How do designers test icons?

### Takeaway
NN/g separates four tests: recognition (icon alone, "what is this?"), information scent (icon plus minimal context, "what happens if you click?"), findability (icon in the full interface, time to locate and first click), and attractiveness (ratings and family comparison). Designers add craft checks: view at 100% real size, blur or squint to compare visual weight across the family, place icons beside real type and buttons, and check contrast and high contrast modes with a tool rather than by eye. Visible labels are the default recommendation.

### Cited Findings
- Findability: test in the full interface; measure time to select the correct icon and first click accuracy. Wrong first clicks suggest icons look too alike; slow correct clicks suggest a discoverability problem. [NN/g, Usability Testing of Icons, Harley, Feb 2016](https://www.nngroup.com/articles/icon-testing/)
- Recognition: show the icon alone with no label or interface and ask what it represents; if guesses do not match, abandon the icon and start over. NN/g does not favour icon to label matching tasks because real users may ignore labels. [NN/g, Icon Testing](https://www.nngroup.com/articles/icon-testing/)
- Information scent: same isolated setup but with minimal context (for example "this is a shop"); ask what they expect to happen. In live products, A/B test with the same position and label and watch "probing" (click and quick return). [NN/g, Icon Testing](https://www.nngroup.com/articles/icon-testing/)
- Attractiveness: rate icons on a 1 to 7 scale, compare alternatives, and show the full family to ask which icon is liked most and least; the family test catches the one or two weak icons in a set. [NN/g, Icon Testing](https://www.nngroup.com/articles/icon-testing/)
- Memorability: ask a repeat set of users a couple of weeks later whether they remember what the icon means. [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- No participant used a clock icon meant for "recently viewed", and NN/g could not tell if it was missed or misunderstood, which is why standard usability tests alone are not enough for icons. "Obscure icon = wasted feature." [NN/g, Icon Testing](https://www.nngroup.com/articles/icon-testing/); [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Labels: pair icons with a visible text label, even standard icons; hover only labels add cost and fail on touch. Quotes Tognazzini: "a word is worth a thousand pictures." [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Relative size affects noticeability: a mobile hamburger takes roughly 20 to 25% of header width, about 3.5% on a desktop site. [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Adobe's glance test: scale an icon down, look away, look back; if it takes long to read, others will struggle. Place icons in the real UI with type and buttons. Check high contrast modes and use a contrast checker: "Do not rely on your perception." [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Lucide's weight and density checks: blur the icon at its intended size to spot crowded areas, and blur test against the `circle` and `square` references to match visual weight. [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)
- Atlassian used a "squint test" to check that the icons looked like one family, checked downscaled icons in tags and metadata, and validated designs in Jira through feature flags and a runtime "icon facade" before migrating. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Streamline's three criteria for every icon: recognisable (clear message, cross cultural, durable), consistent (same construction rules, balanced, shared style), legible (meaning holds at the size of use; heavy, detailed line icons fail small, simple solid icons work). [Streamline blog](https://blog.streamlinehq.com/evaluating-icons/)
- Noun Project: preview at several sizes while designing ("Icons that look great at 256x256 pixels might lose their impact when scaled down to 16x16") and confirm each icon has a clear focal point. [Noun Project blog](https://blog.thenounproject.com/?p=8558)
- Lucide requires screenshots in PRs that add icons, so reviewers see the rendered result. [Lucide CONTRIBUTING](https://github.com/lucide-icons/lucide/blob/main/CONTRIBUTING.md)

### Inferences
- A cheap internal sequence: recognition test on the riskiest new metaphors (icon alone), then a family "most and least liked" pass to find outliers, then findability in a mock of the real screen, then contrast checks on light and dark.
- Dark versus light: none of the sources gives a dark mode specific rule beyond contrast checking; a stroke icon in a light colour on dark tends to look heavier (irradiation), which is a known type design effect but was not sourced here.

### Gaps
- The "5 second test" in the sense of a timed first impression test (show a screen for 5 seconds, then ask) was not found in an NN/g icon article; NN/g's "5 second rule" is the designer side heuristic quoted above. Do not conflate them.
- No source with quantitative recognition rates or sample size guidance for icon tests was found (NN/g icon testing article gives none).
- No sourced guidance on dark mode stroke compensation for icons.

## 3. How is consistency kept as the set grows?

### Takeaway
Big sets stay consistent through four layers: a written construction guide with numbers, templates and reference shapes, automated lint on the SVG source and metadata, and a human review ritual with one approver. Naming by what the icon shows (not what it does), plus tags and categories in a metadata file, keeps the set searchable and stops duplicates.

### Cited Findings
**Written guide and templates**
- Lucide publishes a numbered design guide and offers templates for Illustrator, Inkscape, Figma and Affinity, plus Lucide Studio, a web editor that formats icons in Lucide style. [Lucide CONTRIBUTING](https://github.com/lucide-icons/lucide/blob/main/CONTRIBUTING.md)
- Adobe: document guidelines for how the team modifies or adds to a set, and know where the repository lives and who has access; shared libraries keep linked shapes updated. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)

**Automated linting**
- Lucide's pre PR checklist: 24 x 24 viewBox, `fill="none"`, `stroke="currentColor"`, default stroke width, caps and joins, tidy paths with appropriate precision (minify to 3 decimals), only allowed elements (`path`, `line`, `polygon`, `polyline`, `circle`, `ellipse`, `rect`), no transforms, filters, fills, explicit stroke colours or `<use>`, and a matching JSON metadata file. [Lucide code conventions](https://lucide.dev/contribute/icons/code-conventions)
- Lucide lint commands: `pnpm run lint:icons` (SVG validity), `lint:icons-fix` (Prettier), `lint:icons:all` (names, categories, metadata and SVG structure together), `lint:json:icons` (metadata). [Lucide code conventions](https://lucide.dev/contribute/icons/code-conventions)
- Lucide's GitHub Actions include linting, "Lucide font checks", a PR labeler and an "Add Changed Icons comment" bot that previews changed icons on the PR. [Lucide Actions](https://github.com/lucide-icons/lucide/actions) (snippet)
- Lucide treats the SVGs in `icons/` as the single source of truth; build scripts generate every package from them. [Lucide CONTRIBUTING](https://github.com/lucide-icons/lucide/blob/main/CONTRIBUTING.md)
- Simple Icons uses an `.svglintrc.js` config for svglint in its repo, an example of rule based SVG lint in an icon project. [Simple Icons mirror, .svglintrc.js](https://git.mibew.org/Mibew/simple-icons/commits/commit/67825e3d6ea16823e3e0190c4a7b23741009cb18/.svglintrc.js) (snippet; rules not read)
- Atlassian wrote an ESLint rule with an auto fixer mapping 350 old icons to new ones (about 75% migrated safely) and updated more than 16,000 call sites; a Figma plugin automates layout and export and prompts for category, usage guidelines and keywords. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)

**Review rituals**
- Streamline: designers post work daily in Slack, the Art Director and teammates comment, the designer revises and resubmits next day, the Art Director gives final approval; the AD periodically reviews whole sets in Figma, and at most two designers make the corrections before export. [Streamline blog](https://blog.streamlinehq.com/evaluating-icons/)
- Atlassian centralises team contributions in "Icon Lab" inside the core Figma library (275+ contributed icons) with guides for planning, metaphor, drawing and contributing; goal: a set that "feels as if it were designed by one hand". Lessons: tooling matters as much as visual design, gradual migration paths are essential, clear naming is fundamental. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Lucide: search existing requests first, open an icon request issue, link it from the PR. [Lucide CONTRIBUTING](https://github.com/lucide-icons/lucide/blob/main/CONTRIBUTING.md)

**Naming conventions**
- Lucide: lowercase kebab case; American spelling; name the picture, not the purpose (`floppy-disk`, not `save`, because save is a use case); group first (`badge-plus`, `badge-check`); alternates named by visual difference (`send-horizontal`, not `send-2`); numbers only when drawn (`clock-3`); largest element first (`moon-star`); equal elements by front then reading order (`pencil-ruler`, `sun-snow`); modifier right after its element (`bone-broken`). [Lucide naming conventions](https://lucide.dev/contribute/icons/naming-conventions)
- Contrasting approach: Atlassian names single purpose icons by meaning and multi purpose icons by appearance. Adobe suggests function based file names (for example `save_file_to_cloud`) that also help screen readers. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system); [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)

**Metadata and tags**
- Lucide's per icon JSON holds `contributors`, `use-cases`, `tags` and `categories` (schema validated). Tags: lowercase, prefer single words, cover synonyms and contexts, never repeat the name or add "icon", check existing tags first. Categories: only those allowed in `icon.schema.json`, never invent new ones. Aliases: only when an icon was renamed from a non compliant name. [Lucide metadata conventions](https://lucide.dev/contribute/icons/metadata-conventions)

### Inferences
- For a one person set, the minimum viable version of this stack is: a short spec file with the numbers, a template SVG, a lint script that checks root attributes and allowed elements, a JSON sidecar with tags, and a contact sheet render of the whole set reviewed every time an icon is added (the "family" view NN/g and Streamline both rely on).
- Naming by picture (Lucide) suits a general library; naming by meaning (Atlassian, Adobe) suits a product set where each icon has one job. A product can keep both: file name by picture, alias or tag by meaning.

### Gaps
- Exact Lucide font check and svglint rule contents were not read.
- Phosphor's and Tabler's contribution checks were not retrieved.

## 4. How should icons relate to the typeface and UI?

### Takeaway
Match icon stroke to the stem weight of the text beside it, size icons to the text line height (not the font size), and centre them on the cap height. Apple formalises this in SF Symbols: nine weights mapped to San Francisco weights, three scales, and template guides for baseline and cap height. Exact stroke values differ by system because they depend on the font.

### Cited Findings
- Apple: each of the nine SF Symbols weights corresponds to a weight of the San Francisco system font; custom symbol templates have three scales (S, M, L) and per weight and scale variants; the system centres symbols vertically on the cap height and computes baseline offset and cap height from the template guides, so custom symbols must be placed on those guides. Template v3 lets each variant have its own margins. [Apple, Creating custom symbol images for your app](https://developer.apple.com/documentation/uikit/creating-custom-symbol-images-for-your-app); [Apple WWDC21 10097](https://developer.apple.com/videos/play/wwdc2021/10097) (snippet)
- Apple treats the baseline as a flexible guide: some symbols (infinity, folder) sit above or below it to balance optically. [WWDC20 10207 SF Symbols 2](https://developer.apple.com/videos/play/wwdc2020/10207?time=329) (snippet)
- Atlassian tuned its 1.5 px stroke on 16 px so the icons "match the stroke of standard UI text" and blended brand angularity with the rounded features of Atlassian Sans. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- GitLab's estimate: at 16 px, most regular weight sans serif system fonts have stems of about 1.5 px. [GitLab design issue 1432](https://gitlab.com/gitlab-org/gitlab-design/-/issues/1432) (snippet)
- Ant Design: icon size follows a scale relative to font size and line height; 20 px icons pair with 14 and 16 px text, 12 px icons can be used with tiny (10 px) text. [Ant Design icon spec](https://ant.design/docs/spec/icon.md) (snippet)
- React Magma pairs 20 px icons with 14 px text on a 20 px line height. [React Magma icon guidelines](https://react-magma.cengage.com/version/5.2.0/design/icon/) (snippet)
- Flatstudio synced a 2 px icon stroke with the stem thickness of the font at 14 to 16 px. [Flatstudio blog](https://flatstudio.co/blog/beyond-the-pixel-the-engineering-of-icon-and-typeface-integration) (snippet, vendor blog)
- Adobe: place icons in the real UI alongside type and buttons to judge balance; check contrast with a tool. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Octicons draws separate 16 px and 24 px versions instead of scaling one, i.e. optical sizes. [Primer Octicons](https://primer.style/foundations/icons/design-guidelines)

### Inferences
- If a UI scales fonts with one factor, icon stroke should scale with it too, or the stroke will drift away from the text stem weight at large scales.
- A 2 px stroke on a 24 px grid rendered at 16 to 18 px gives an on screen stroke of roughly 1.3 to 1.5 px, which lines up with the 1.5 px regular stem estimate above; that arithmetic is mine, not a source.

### Gaps
- No source gives a formula for stroke versus font weight beyond "match the stem". Apple's internal stroke compensation per weight is not published.
- No sourced colour rule for icons beyond contrast checking (for example whether icons should use the text colour or a secondary tone).

## 5. Common mistakes in custom icon sets and how they look

### Takeaway
The repeat offenders are small drift in stroke weight or radius (the set looks "broken" next to itself), too much detail for the size (mush at 16 px), uneven optical weight (circles looking small next to squares, dense icons looking darker), inconsistent padding, unfamiliar metaphors, near duplicate base shapes, and production faults such as expanded strokes and stray anchor points.

### Cited Findings
- "A common mistake designers make is allowing small variations between icons", especially in stroke weight; also excessive padding, mixing unrelated concepts in one set, and complexity over clarity. [Noun Project blog](https://blog.thenounproject.com/?p=8558)
- Circles look larger than rectangles of the same size, so resize until they look right; stroke alignment (inside, centre, outside) changes apparent size. [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Dense or closely spaced strokes add weight; overcrowded areas show up when blurred at size. [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)
- Heavy, detailed line icons fail at small sizes. [Streamline blog](https://blog.streamlinehq.com/evaluating-icons/)
- Thin outline styles can look "frail"; overly complex shapes are hard to scan; excess anchor points cause rounding errors and make cutouts hard; unexpanded strokes can render badly in some engines (so keep a live stroke master and export a clean copy). [Adobe Design, Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Using a familiar shape such as an arrow in an unfamiliar way; making near duplicates instead of reusing shapes. [Adobe Design, Part 1](https://adobe.design/ideas/how-to-design-effective-icons-part-1)
- Brand style dropped straight into UI: Atlassian's bold brand shapes overpowered the product UI. [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Same icon, different meanings across one product (Atlassian), and ambiguous icons like heart, star, hamburger (NN/g). [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system); [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- Hiding labels until hover. [NN/g, Icon Usability](https://www.nngroup.com/articles/icon-usability/)
- SVG level faults that break theming: hard coded fills or stroke colours instead of `currentColor`, transforms, `<use>` with clashing IDs. [Lucide code conventions](https://lucide.dev/contribute/icons/code-conventions)
- Jon Hicks: "Keep it as simple as possible... but not too simple", and follow existing conventions where they exist. [Creative Bloq, 5 killer icon design tips](https://www.creativebloq.com/advice/5-killer-icon-design-tips) (snippet)

### Inferences
- Most of these mistakes are invisible when an icon is reviewed alone at large zoom and obvious in a contact sheet at real size, which is why every source above ends up recommending a family view.

### Gaps
- No source with before and after images was read in full, so "how they look" is described from text only.

## 6. Books and long essays by expert icon designers (legal sources)

### Takeaway
The best freely available long reads are Jon Hicks's The Icon Handbook (now a free download from the author), Adobe's two part icon essay, Atlassian's 2025 rebuild write up, Streamline's evaluation essay, NN/g's two icon articles, and the Lucide and Octicons guides. Kare's process is documented in the Stanford oral history interview.

### Cited Findings
- The Icon Handbook (Jon Hicks, Five Simple Steps, Dec 2011, two years of work) covers the process "from the metaphor to drawing symbols and implementing" and includes interviews with Susan Kare, David Lanham and Gedeon Maheux of the Iconfactory; the author now offers it as a free download. [hicks.design, The Icon Handbook](https://hicks.design/journal/the-icon-handbook) (snippet)
- A review describes the book as moving quickly between topics with interviews, case studies and tutorials interspersed; a reader calls its tooling sections outdated. [Designers Review of Books, Andy Polaine](https://designersreviewofbooks.com/2012/10/the-icon-handbook/) (snippet); [Jared Russell notes](https://jaredrussell.notion.site/The-Icon-Handbook-by-Jon-Hicks-1b19a122e2e080d7bf96da250d88fbbc) (snippet)
- Hicks talks: "The Principles of Icon Design" (Future of Web Design, May 2010, slides with notes as PDF) and "The Icon Design Process" (brief to deployment of resolution independent icons). [hicks.design](https://hicks.design/journal/principles-of-icon-design); [beyond tellerrand 2014](https://beyondtellerrand.com/events/berlin-2014/speakers/jon-hicks) (snippet)
- Hicks works in Illustrator and values its stroke width tool for making many shapes from one path. [WooCommerce Q&A, Apr 2015](https://woocommerce.com/posts/qa-with-jon-hicks-iconographer/)
- Susan Kare oral history (Stanford, Alex Pang, 2000). [Stanford](https://web.stanford.edu/dept/SUL/sites/mac/primary/interviews/kare/trans.html)
- Adobe Design: "How to design effective icons" Part 1 and Part 2 (an Adobe icon designer). [Part 1](https://adobe.design/ideas/how-to-design-effective-icons-part-1); [Part 2](https://adobe.design/ideas/how-to-design-effective-icons-part-2)
- Atlassian: "Reinventing our iconography system at scale" (Sep 2025). [Atlassian Design](https://atlassian.design/whats-new/building-atlassians-new-icon-system)
- Streamline: "How to create the perfect icons" and a post on drawing hands. [Streamline blog](https://blog.streamlinehq.com/evaluating-icons/)
- Phosphor authors Helena Zhang and Tobias Fried appear on Changelog Interviews #618. [Changelog #618](https://changelog.com/podcast/618) (description only)
- Vincent Le Moign, "Designing icon sets: a masterclass from Streamline" (Medium, Dec 2022). [Medium, @webalys](https://medium.com/@webalys) (snippet only)

### Inferences
- For a short reading list: Hicks's handbook for the process and interviews, Adobe Part 1 and 2 for craft, Lucide and Octicons guides for numeric rules, NN/g for testing, Atlassian for scaling and governance.

### Gaps
- Not read in full: The Icon Handbook text, Hicks's slides, Le Moign's masterclass, the Phosphor podcast, Nucleo's author material (no source found), Apple HIG pages (JavaScript rendered, could not be fetched; Apple findings above come from search snippets of Apple docs).
- Material Design 3 icon pages could not be fetched (JavaScript rendered), so Material's keyline and optical size rules are not included.
