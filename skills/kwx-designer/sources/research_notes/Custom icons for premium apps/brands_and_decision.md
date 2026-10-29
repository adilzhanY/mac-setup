# Custom icons for premium apps: brand case studies and the custom vs pack decision

Note on punctuation: the brief forbids em and en dashes, so any dash inside a quoted source has been replaced with a comma. Wording is otherwise kept as the source gave it.

## Which premium products draw their own icons, and what did they say about why?

### Takeaway
Almost every large product with a public design system draws its own icon set (Apple, Figma, Atlassian, Uber, Spotify, Shopify, GitHub, IBM, Raycast, Airbnb). The stated reasons are rarely "brand" in the abstract. They are concrete: the old set drifted into inconsistency across products, metaphors no longer fit the domain, icons did not match the typeface, and legibility or state contrast failed at small sizes. Several of the most cited "custom" sets actually started from packs (Raycast) or were redrawn after years of piecemeal growth (Atlassian, Uber, Spotify).

### Cited Findings

**Apple (SF Symbols)**
- WWDC19 "Introducing SF Symbols": symbols "come in weights that match our family of system fonts, San Francisco, all the weights", "they're specified in typographic points, like text", and "when symbols appear next to text, they all sit nicely on the same baseline" ([WWDC19 session 206](https://developer.apple.com/videos/play/wwdc2019/206/)).
- Same session: "Every weight has been drawn manually, and special consideration went into each design", and scales are "not just linearly-scaled, the stroke thickness is adjusted to the weight of the text". Launch count was "over 1,000" ([WWDC19 session 206](https://developer.apple.com/videos/play/wwdc2019/206/)).
- Same session framed the motive as familiarity and developer effort: "This creates a sense of familiarity throughout the user interface" and "We use symbols a lot, and so do you. We want to make your job easier." It also argues symbols simplify Dynamic Type, localization and accessibility ([WWDC19 session 206](https://developer.apple.com/videos/play/wwdc2019/206/)).
- WWDC21 reported more than 3,000 symbols, automatically vertically centred to San Francisco's cap height in all scales and weights; WWDC22 added 700+ (past 4,000) ([WWDC21 10097](https://developer.apple.com/videos/play/wwdc2021/10097), [WWDC22 10157 notes](https://wwdcnotes.com/notes/wwdc22/10157)).
- Current HIG: nine weights, ultralight to black, each corresponding to a San Francisco weight "helping you achieve precise weight matching between symbols and adjacent text"; three scales defined relative to SF cap height ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)).
- Inference from the above: SF Symbols is Apple's own custom set, and its core design idea is that icons are part of the typeface system, not a separate asset class.

**Figma (UI3, 2024)**
- UI3 introduced "200 expressive icons" hand-drawn by Figma designer Tim Van Damme, intended as "visual explanations of how to interact with the platform" ([Figma blog, Inside the redesigned Figma](https://www.figma.com/blog/behind-our-redesign-ui3/)).
- Rationale: Figma's earlier minimalist UI (sharp edges, abstract icons, subtle affordances) was a differentiator, but as complex controls were added "that visual language became harder to parse" ([Figma blog](https://www.figma.com/blog/behind-our-redesign-ui3/)).
- Van Damme: maintaining the icon system "is a balancing act between ensuring visual consistency" and conveying complex ideas abstractly ([Figma blog](https://www.figma.com/blog/behind-our-redesign-ui3/)).
- Users can toggle labels on for clarity or off for an icon-forward view ([Figma blog](https://www.figma.com/blog/behind-our-redesign-ui3/)).
- Cost side: Figma's design-approach post admits a simplified appearance panel slowed workflows because users had to wait for a tooltip on an icon to learn the blend mode ([Figma blog, Our approach to designing UI3](https://www.figma.com/blog/our-approach-to-designing-ui3/)). Forum users complained they "had to re-learn the icons and sections" ([Figma forum UI3 feedback](https://forum.figma.com/share-your-feedback-26/ui3-feedback-3058/index14.html)).

**Linear**
- 2024 redesign aimed to "reduce visual noise, maintain visual alignment" and increase hierarchy and density of navigation (Karri Saarinen). Designer Yann-Edern Gillet aligned labels, icons and buttons in the sidebar and tabs, "a challenge given the amount of UI elements we have on this tiny surface", and darkened/lightened neutral icons for contrast. Headings moved to Inter Display ([Linear, How we redesigned the Linear UI part II](https://linear.app/blog/how-we-redesigned-the-linear-ui)).
- March 2026 refresh: Linear "relies on [icons] to make projects, issues, initiatives, and statuses recognizable at a glance", found icon use had become excessive in some views, so it reduced icon usage, "scales their sizes down, and removes unnecessary visual treatments like colored team icon backgrounds"; desktop tabs became smaller icon-only tabs ([Linear, A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh); [Linear changelog 2026-03-12](https://linear.app/changelog/2026-03-12-ui-refresh)).
- Neither Linear post says whether the icons are custom-drawn or stock. The domain-specific status icons (issue states, priority) are Linear's own, but I found no primary writeup about who drew the general set.

**Atlassian (2024 to 2025)**
- Legacy library had 350+ icons from six years of work, "inconsistent sizing, spacing, and metaphors", and a style "too heavy for current UI". Teams often drew their own icons in isolated repos, which shipped faster but caused duplication. An audit found over 1,000 custom icons across apps; 16,000+ callsites needed updating ([Atlassian blog, Behind the screens: Building Atlassian's new icon system](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)).
- Specs moved from 2px stroke on a 24px canvas to 1.5px stroke on a 16px canvas, stroke edges pixel-aligned for low-resolution crispness; a 12px utility trial was too limited, so 12px downscaled versions of core icons were made ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)).
- "Icons are a cornerstone of Atlassian's visual language." Same icon carried different meanings across products, confusing users. Fix included splitting icons into single-purpose (named by concept, e.g. "Share") and multi-purpose (named by appearance, e.g. "globe") ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)).
- Developers had been scaling icons, causing stroke and padding variations, so the new system removed the ability to scale icons ([Atlassian RFC-81](https://community.developer.atlassian.com/t/rfc-81-upcoming-changes-to-iconography/87753)). New icons described as optically balanced with the UI and a better fit with refreshed text styles ([Atlassian UI refresh](https://atlassian.design/whats-new/atlassian-ui-refresh-updates)).

**Uber (Base, 2026)**
- Group Product Design Manager Samira Rahimi (25 March 2026): the old set used 3px outlines, sharp corners and a geometric style; at scale "There simply weren't enough pixels to express complex ideas with precision." Filled icons became the default to keep legibility, but because Uber's brand colour is black the selected state shifted from gray to black, a contrast change many users could not see. Products diverged (some filled, some outline) ([Uber Design, When to evolve a design system](https://uber.design/when-to-evolve-a-design-system)).
- New set based on the Uber Move typeface, "two expressions of one visual alphabet": 2px stroke, square caps "to match the precision of the typeface", generous negative space, exaggerated roundness, defined filled/outline relationship. 1,500 icons redrawn in under four months, plus naming system, guidelines, and tooling so design files and code update together ([Uber Design](https://uber.design/when-to-evolve-a-design-system); summary at [Design Compass](https://designcompass.org/en/2026/08/21/uber-rebuilds-icon-system/)).
- Rahimi on divergence: "it's no longer drift, it's feedback" (dash replaced) and "this wasn't a tweak, it was a redesign" ([Uber Design](https://uber.design/when-to-evolve-a-design-system)).

**Raycast**
- Raycast's previous set "combined icons from packs and custom variations to fit our needs". It teamed up with designer James McDonald to redesign the set, introducing 400+ icons, also available in its extension API. Rules on stroke widths and an agreed radius "unblocked us from creating new icons at speed in the future" ([Raycast blog, Launch Week Summary](https://www.raycast.com/blog/launch-week-summary)).
- This is the clearest primary example of the "started on packs, graduated to custom" path.

**Spotify (Encore)**
- Spotify's design blog post "Refreshing our Icon System" says the Encore Foundation team worked with the iconographer who led the 2016 redesign to unify icon sets that had diverged across Encore systems, and moved icon source files and creation flows fully into Figma (summarised in search results; the spotify.design URL now redirects and the mirror would not render, so I could not read it in full) ([Notion mirror of Spotify Design post](https://theblock.notion.site/Refreshing-our-Icon-System-the-why-and-how-behind-the-changes-Spotify-Design-6bd125b2ce94404399a7352a881b8dd4)).
- The earlier (2016 era) redesign was "a four month process of creating and implementing six hundred individually crafted icons", each produced in 5 custom sizes ([Hypebot, A look inside the Spotify redesign process](https://www.hypebot.com/a-look-inside-une-spotify-redesign-process/)). Studio credit: [Hicks Design, Spotify iconography](https://hicks.design/work/spotify).

**GitHub (Octicons)**
- Launch post: "With metaphors that just barely fit what we needed them to, we felt like new icons were long overdue", plus retina sharpness "at any zoom level" ([GitHub blog, Say Hello to Octicons](https://github.blog/news-insights/say-hello-to-octicons/)).
- 2016 move from icon font to SVG because font icons rendered poorly on 1x displays and blurred in some WebKit browsers; SVG locks "nicely to whole pixel values at any resolution" ([GitHub blog, Delivering Octicons with SVG](https://github.blog/2016-02-22-delivering-octicons-with-svg/)).
- Brand toolkit: Octicons are GitHub's default icons, part of Primer, meant "to primarily serve GitHub's needs across product" ([GitHub brand toolkit](https://brand.github.com/graphic-elements/iconography)).

**Shopify (Polaris)**
- Shopify's uplift settled "after numerous iterations" on a 1.5px outline set with filled variants for navigation, aiming to "inject a dash of joy" and feel more approachable (via search summary; the Medium page returned 403 to me) ([Shopify UX, Uplifting Shopify Polaris](https://medium.com/shopify-ux/uplifting-shopify-polaris-7c54fc6564d9)).
- The Polaris icon licence restricts use to apps that integrate with Shopify, i.e. the set is a brand asset, not a general pack ([npm @shopify/polaris-icons](https://www.npmjs.com/package/@shopify/polaris-icons)).

**IBM (Carbon)**
- UI icons drawn on a 32px grid and scaled down linearly, 2px padding zone, consistent 2px strokes, 2px corner radius on rounded shapes, squared corners where the real object is square, straight-on (no perspective), angles in multiples of 15 degrees, monotone ([IBM Design Language, UI icons design](https://www.ibm.com/design/language/iconography/ui-icons/design/)). Carbon components typically use 16px icons, with 20, 24 and 32 allowed ([Carbon icon usage](https://carbondesignsystem.com/elements/icons/usage/)).
- Third-party icons need the owner's permission before entering the library ([IBM UI icons contribute](https://www.ibm.com/design/language/iconography/ui-icons/contribute)).

**Airbnb (Summer Release, May 2025)**
- Moved to 3D, skeuomorphic, animated icons. A spokesperson said the app design, UI, 3D and illustrations "were all done by an in-house team" ([It's Nice That](https://www.itsnicethat.com/articles/airbnb-app-redesign-140525)). Bloomberg framed it as Apple and Airbnb ditching flat icons ([Bloomberg](https://www.bloomberg.com/news/articles/2025-06-13/apple-airbnb-ditch-flat-app-icons-for-new-3d-ui-design)).
- The animated icons reportedly use an internal micro-video format called "Lava" (secondary source, unverified) ([Medium, Airbnb's Lava icon format](https://medium.com/@waldobear002/airbnbs-new-lava-icon-format-a-technical-deep-dive-b2604626c7e0)).
- Critique: some found the hyper-realistic icons so specific they detract from their message ([Medium, Design Bootcamp](https://medium.com/design-bootcamp/airbnb-summer-2025-update-heres-what-s-new-and-why-it-matters-0ced2338b921)).
- This is brand/expressive iconography (category tabs, hero moments), not utility glyphs.

**Things, Notion, Teenage Engineering, Stripe, Dropbox, Duolingo, Arc**
- Things 3: MacStories praised its "lovely icons" and the app holds two Apple Design Awards, but Cultured Code has published no icon writeup I could find ([MacStories review](https://www.macstories.net/reviews/things-3-beauty-and-delight-in-a-task-manager/)).
- Teenage Engineering: secondary analysis says it uses only monospaced type across products, packaging and web, and its screens refuse to imitate analog panels; nothing primary on how its pictograms are drawn ([Blake Crosley guide](https://blakecrosley.com/de/guides/design/teenage-engineering)).
- Stripe, Notion, Dropbox, Duolingo, Arc: see Gaps.

### Inferences
- The common pattern is not "premium apps start custom". It is "products that grow large enough end up with icon drift, and the cure is a redrawn, typeface-matched set with rules and tooling". Atlassian, Uber, Spotify and Raycast all describe the redraw as a fix for inconsistency.
- The most repeated technical motive is matching the typeface: Apple (SF weights and cap height), Uber (Uber Move, square caps), Atlassian (fit with refreshed text styles), Linear (alignment of icons and labels). An icon set that shares stroke weight, terminal shape and vertical metrics with the UI font is what reads as "one product".
- Domain metaphors are the second motive: GitHub ("metaphors that just barely fit"), Figma (icons as "visual explanations" of design tool operations), Linear (status icons recognisable at a glance). Generic packs do not ship "auto layout", "pull request" or "issue in progress".

### Gaps
- Stripe: no official writeup on its product icon set found; third-party "Stripe-inspired" specs (1.5px outline, 16/20/24px) are unverifiable.
- Notion: no official post on its built-in icon set or who drew it.
- Dropbox, Duolingo, Arc browser: searches surfaced no primary icon writeups within the time budget.
- Linear: no source states whether the general UI glyphs are drawn in-house or adapted from a pack.
- Spotify: the primary post could not be read in full (redirect and blank mirror).

## What does a custom set buy, and how are stock icons perceived?

### Takeaway
Primary sources credit custom sets with four things: coherence with the typeface and text baseline, metaphors specific to the domain, consistent state language (filled vs outline, selected vs not), and visual identity. The "looks like every other app" critique of stock packs is real but is mostly made by blogs about AI-generated and template UIs, not by research.

### Cited Findings
- Typeface coherence: SF Symbols are drawn per weight to match SF and sit on the text baseline ([WWDC19 206](https://developer.apple.com/videos/play/wwdc2019/206/)); Uber icons are "two expressions of one visual alphabet" with Uber Move ([Uber Design](https://uber.design/when-to-evolve-a-design-system)).
- Domain metaphors: GitHub replaced icons whose metaphors "just barely fit" ([GitHub blog](https://github.blog/news-insights/say-hello-to-octicons/)); Figma's 200 icons explain how to interact with the tool ([Figma blog](https://www.figma.com/blog/behind-our-redesign-ui3/)).
- State and accessibility: Uber redesigned the filled/outline relationship because black-on-black selected states were not distinguishable ([Uber Design](https://uber.design/when-to-evolve-a-design-system)).
- Brand voice: Material calls product icons "the visual expression of a brand and product" ([Material 1 icons](https://m1.material.io/style/icons.html)); Atlassian calls icons "a cornerstone of Atlassian's visual language" ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)); Shopify aimed to "inject a dash of joy" ([Shopify UX](https://medium.com/shopify-ux/uplifting-shopify-polaris-7c54fc6564d9)).
- Speed after the investment: Raycast said rules for stroke and radius let it create new icons "at speed in the future" ([Raycast blog](https://www.raycast.com/blog/launch-week-summary)).
- Stock perception: critics list Lucide and Heroicons as the default picks in AI-generated interfaces, with a generic 1.5 or 2px stroke everywhere, and the "icon in a tinted rounded square on every feature card" pattern as filler ([UX Skill, Why AI design uses the same icons](https://uxskill.laithjunaidy.com/blog/ai-icon-design-generic.html); [Mowgli, 15 tells](https://mowgli.ai/blog/why-ai-built-apps-look-the-same); [Medium, Why every AI-generated app looks the same](https://medium.com/design-bootcamp/why-every-ai-generated-app-looks-same-51a9459055ae)).
- Counterpoint: Lucide's defenders point to its consistent 24 grid and adjustable stroke as giving one visual language, and its status as the shadcn/ui default ([pistack, Icon libraries in 2026](https://www.pistack.xyz/posts/2026-08-22-icon-libraries-lucide-react-icons-heroicons-comparison/)).
- Suggested fixes in that literature: tune icons to the brand, choose a less common library (Hugeicons, Phosphor, Tabler), or remove decorative icons entirely ([Mowgli](https://mowgli.ai/blog/why-ai-built-apps-look-the-same); [Hugeicons blog](https://hugeicons.com/blog/design/8-lucide-icons-alternatives-that-offer-better-icons), note: vendor source).

### Inferences
- The "generic" signal comes less from the glyphs themselves than from using them decoratively and untuned (default stroke, default size, every card gets one). Linear's 2026 move of using fewer and smaller icons is the same lesson from the other side.
- Recognisability of a set at a glance is plausibly highest for the few icons users see constantly (nav, primary actions, status), which is where custom drawing pays most.

### Gaps
- No user research or A/B data was found that measures whether users perceive or prefer custom vs stock icons. The perception claims are designer and blogger opinion.

## What does a custom set cost?

### Takeaway
The cost is mostly not drawing. It is coverage, the rules that keep a growing set consistent, migration tooling, naming, and the re-learning cost for existing users. Companies that published numbers report months of work by dedicated teams.

### Cited Findings
- Uber: 1,500 icons in under four months, within a project spanning about a year, plus naming, guidelines, and design-to-code tooling ([Uber Design](https://uber.design/when-to-evolve-a-design-system)).
- Spotify: 600 icons in 5 sizes over four months (earlier redesign) ([Hypebot](https://www.hypebot.com/a-look-inside-une-spotify-redesign-process/)).
- Atlassian: 16,000+ callsites, an ESLint rule with auto-fixer, a runtime "icon facade", feature flags, an Icon Explorer, a custom Figma plugin ("Icon Lab"); 275+ icons contributed by designers; about 75% of 350 old icons migrated automatically. Lessons: "Technical tooling matters as much as visual design", backwards compatibility and gradual migration are needed ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)).
- Consistency risk over time: Atlassian's teams drew icons in isolated repos, producing 1,000+ customs and conflicting meanings ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)); Spotify's sets diverged across Encore systems ([Notion mirror](https://theblock.notion.site/Refreshing-our-Icon-System-the-why-and-how-behind-the-changes-Spotify-Design-6bd125b2ce94404399a7352a881b8dd4)).
- Learnability cost: Figma users reported re-learning icons; Figma admitted an icon-only control forced users to wait for tooltips ([Figma forum](https://forum.figma.com/share-your-feedback-26/ui3-feedback-3058/index14.html); [Figma blog](https://www.figma.com/blog/our-approach-to-designing-ui3/)).
- Accessibility obligations transfer to you: HIG requires alternative text labels for custom interface icons and custom symbols ([HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons); [HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)). Custom SF Symbols must provide at least regular at medium scale, and bold variants to support Bold Text ([WWDC19 206](https://developer.apple.com/videos/play/wwdc2019/206/)).
- Custom SF Symbols also need layer annotation and testing under every animation preset because "shapes and paths might not appear how you expect when the layers are in motion" ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)).
- Rendering: GitHub abandoned its custom icon font because it rendered poorly on 1x screens ([GitHub blog](https://github.blog/2016-02-22-delivering-octicons-with-svg/)); Atlassian pixel-aligns 1.5px strokes for low-resolution displays ([Atlassian blog](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)).

### Inferences
- For a small team the biggest hidden cost is coverage: every new feature needs a new glyph in the same style, forever. A pack gives thousands up front; a custom set gives dozens and a backlog.
- Recognition cost: users already know the pack/platform metaphors (share, trash, search). Redrawing them in a new form buys little and can cost learnability.

### Gaps
- No published per-icon hour or cost figures beyond the Uber and Spotify team-level timelines.

## When is a pack the right call, and what is the hybrid approach?

### Takeaway
A pack is right for prototypes, for generic utility glyphs that users must recognise instantly, and on Apple platforms where SF Symbols is the native vocabulary. The hybrid that the primary sources describe in practice is: system or pack glyphs for common actions, custom-drawn glyphs for brand and domain concepts, all held to one stroke, radius, size and weight spec so they read as a single set. Apple's own HIG explicitly endorses mixing custom and system icons under that consistency rule.

### Cited Findings
- Apple explicitly allows the mix: "Whether you use only custom icons or mix custom and system-provided ones, all interface icons in your app need to use a consistent size, level of detail, stroke thickness (or weight), and perspective", and "In general, match the weights of interface icons and adjacent text" ([HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons)).
- Apple's custom-symbol workflow is itself the hybrid: "export the template for a symbol that's similar to the design you want, then use a vector-editing tool to modify it", keeping consistency "in level of detail, optical weight, alignment, position, and perspective"; use the component library for enclosures and badges rather than drawing variants ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)).
- Apple publishes a list of "standard icons" (SF Symbol names) for common actions such as copy, paste, share, delete, undo, search, filter ([HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons)).
- Raycast's pre-redesign state ("icons from packs and custom variations") is the hybrid at an early stage; it moved to a fully ruled custom set once the product and extension API grew ([Raycast blog](https://www.raycast.com/blog/launch-week-summary)).
- Pack customisation knobs: Lucide's default stroke is 2px, a strokeWidth prop changes it, absoluteStrokeWidth keeps the stroke fixed in pixels as the icon scales, and a provider sets global size, colour and stroke ([Lucide docs, stroke width](https://lucide.dev/guide/react/basics/stroke-width)). Material Symbols is a variable font with weight, fill, grade and optical size axes in outlined, rounded and sharp styles ([Material blog, Introducing Symbols](https://m3.material.io/blog/introducing-symbols); [Google Fonts icons](https://fonts.google.com/icons)).
- Licence limits can force custom: SF Symbols terms prohibit use "in app icons, logos, or any other trademarked use", Apple product symbols cannot be customised ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)); Polaris icons are licensed only for Shopify-integrated apps ([npm](https://www.npmjs.com/package/@shopify/polaris-icons)).

### Inferences
- Decision rule synthesised from the sources:
  1. Prototype or pre-product-market-fit: pack only, tuned once (stroke, size, corner style) to the UI font. The cost of a custom set is not justified before the feature list stabilises.
  2. Generic utility actions (close, search, chevrons, share, trash, settings): use the pack or platform glyph. Recognition beats distinction, and Apple publishes exactly these as standard.
  3. Native Apple app: SF Symbols by default, custom symbols from SF templates only for missing domain concepts.
  4. Domain and brand concepts that the pack lacks or approximates poorly (the "metaphors that just barely fit" problem): draw custom, on the pack's grid and stroke spec, so the two halves are indistinguishable in weight.
  5. Product with many surfaces, several teams, or a public extension API (Atlassian, Uber, Raycast stage): a fully owned, documented set with naming rules and tooling, because drift is the failure mode.
- Whatever the source, the non-negotiable spec is shared: one stroke width matched to the body text weight, one corner radius, one canvas and padding, one filled/outline state rule. All four large redraws in this research were triggered by violating one of these.

### Gaps
- No source compared Phosphor, Heroicons or Font Awesome customisation in a primary-source way within this session (e.g. Phosphor's weight set). Treat claims about those packs as needing verification.
- No company described its pack-to-custom migration threshold in numbers (icon count, team size).

## Do platform guidelines recommend system icons or custom ones, and when?

### Takeaway
Apple recommends SF Symbols where one fits and custom symbols, built from SF templates, only when nothing fits, with mixing allowed under strict consistency rules. Material separates system icons (use Material Symbols, or draw custom on Material keylines) from product icons (always the brand's own expression).

### Cited Findings
- Apple: interface icons can be designed or chosen from SF Symbols, "using them as-is or customizing them to suit your needs" ([HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons)).
- Apple: "If you need a symbol that SF Symbols doesn't provide, you can create your own", starting from a similar symbol's template; strive for simple, recognizable, inclusive, directly related to the action ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)).
- Apple: system colours on symbols adapt automatically to accessibility settings, vibrancy and Dark Mode; the system handles selected states in standard components so you need not supply them ([HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols); [HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons)).
- Apple: custom icons should be vector (PDF or SVG), optically centred via padding, and include localised or flipped variants for text and reading direction ([HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons)).
- Apple: some system icons became symbols in iOS 13, so apps using them "will automatically use the new designs", an upgrade path custom art does not get ([WWDC19 206](https://developer.apple.com/videos/play/wwdc2019/206/)).
- Material: product icons are "the visual expression of a brand and product" and should share consistent graphic elements across a brand's icons; system icons represent commands, files, devices and common actions; product icons 48dp, system icons 24dp, both built on keyline shapes ([Material 1 icons](https://m1.material.io/style/icons.html); [Material 2 iconography](https://m2.material.io/design/iconography)).
- Material: Google publishes design principles for custom icons where Symbols lack one, and Material Symbols' axes let designers match icon weight to the product's font ([Google Material Icons guide](https://developers.google.com/fonts/docs/material_icons); [Material blog](https://m3.material.io/blog/introducing-symbols)).

### Inferences
- Both platforms converge on the same position as the brand case studies: system glyphs for shared vocabulary, custom only where meaning or brand requires it, and always tuned to the typography.

### Gaps
- The current M3 icons pages render client-side and could not be read directly; the product/system icon distinction is cited from M1/M2 pages, and M3 wording may differ.
