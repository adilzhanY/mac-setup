# Mobile foundations: the numbers, iOS and Android side by side

Every number here comes from a primary source (Apple HIG JSON pages as of the September 2026 revision, Material 3 Compose token files in androidx, developer.android.com, Steven Hoober's touch research). Where a value is a framework default rather than a written rule, it says so. Read the safe area and window size at runtime; never hardcode bar heights.

## Contents

1. Units and density
2. Touch targets and spacing
3. Typography and Dynamic Type / font scale
4. Layout: margins, size classes, panes
5. Bars and chrome heights
6. Shape, elevation, state layers
7. Motion tokens
8. Color and contrast floor
9. Checklist before you ship a screen

## 1. Units and density

- Design in points (iOS) and dp (Android). Both are density independent units of roughly the same physical size (about 0.16 mm); treat them as the same unit when you sketch, then check on device.
- Android text uses sp, which also scales with the user's font size setting. Never size a container in sp; size text in sp and containers in dp, and let containers grow with text.
- Work on a 4 unit grid, with 8 as the common step. Material, Fluent 2 and Apple's templates all land on multiples of 4. Use 2, 6, 10 only to align icon padding (Fluent 2 spacing ramp keeps them for exactly that).

## 2. Touch targets and spacing

| Rule | iOS / iPadOS | Android (Material 3) |
|---|---|---|
| Default hit target | 44 x 44 pt | 48 x 48 dp |
| Absolute minimum | 28 x 28 pt (HIG accessibility table) | 48 x 48 dp is the stated floor; Material components enforce it |
| Padding around a bezeled control | about 12 pt | 8 dp between separate targets is the working minimum |
| Padding around a borderless control | about 24 pt around its visible edges | keep the 48 dp target even if the glyph is 24 dp |
| visionOS button centers | at least 60 pt apart | not applicable |

Position matters more than any single number. Hoober's field research (thousands of observed taps, 95 percent hit containment):

| Screen region | Target needed for 95 percent accuracy |
|---|---|
| Center of the screen | as small as 7 mm (about 20 pt / 27 px) |
| Top edge | about 11 mm (about 31 pt / 42 px) |
| Bottom edge | about 12 mm (about 34 pt / 46 px) |
| Corners | about 12 mm |

Rules:

- Make every target at least 44 pt / 48 dp. Make targets on the top and bottom edges larger than that (46 to 48 pt high is a good bar height), because accuracy drops at edges.
- Let the visible glyph be smaller than the target. A 24 pt icon sits in a 44 pt hit box. Good: `IconButton` with a 24 dp icon and a 48 dp touch area. Bad: a 24 x 24 tappable SVG with no padding.
- Make adjacent hit regions contiguous inside bars (no dead gaps between toolbar buttons). Apple calls this out for pointer hit regions too.
- Keep destructive targets far from frequent ones. Delete never sits next to Send.
- Test: overlay the hit boxes (Xcode view debugger, Android "Show layout bounds"). Any box under 44 pt / 48 dp, or any two boxes that overlap, fails.

## 3. Typography and Dynamic Type / font scale

### iOS Dynamic Type, default size (Large)

| Style | Weight | Size pt | Leading pt | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

### How Body grows across the 12 user sizes

| xS | S | M | L (default) | xL | xxL | xxxL | AX1 | AX2 | AX3 | AX4 | AX5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 | 15 | 16 | 17 | 19 | 21 | 23 | 28 | 33 | 40 | 47 | 53 |

Large Title only goes from 34 to 60 at AX5, while Body goes from 17 to 53. Small styles grow fastest in relative terms (Caption 2: 11 to 40). Design consequence: at AX sizes the hierarchy compresses, so stack layouts vertically instead of trusting size contrast.

### Android Material 3 type scale (sp)

| Role | Size / line height | Weight | Tracking |
|---|---|---|---|
| Display L / M / S | 57/64, 45/52, 36/44 | Regular | -0.2, 0, 0 |
| Headline L / M / S | 32/40, 28/36, 24/32 | Regular | 0 |
| Title L / M / S | 22/28, 16/24, 14/20 | Regular, Medium, Medium | 0, 0.2, 0.1 |
| Body L / M / S | 16/24, 14/20, 12/16 | Regular | 0.5, 0.2, 0.4 |
| Label L / M / S | 14/20, 12/16, 11/16 | Medium | 0.1, 0.5, 0.5 |

### Default and minimum body size

| Platform | Default body | Minimum |
|---|---|---|
| iOS / iPadOS | 17 pt | 11 pt |
| Android | 14 sp (Body Medium) to 16 sp (Body Large) | 11 sp (Label Small) is the smallest token; use 12 sp for anything read |
| watchOS | 16 pt | 12 pt |

Rules:

- Use the system text styles (iOS) or the type tokens (Android) instead of literal sizes, so Dynamic Type and font scale work for free. A literal `font-size: 13` is a bug on mobile.
- Support at least 200 percent text enlargement (HIG). Android 14+ allows nonlinear font scaling up to 200 percent; test at 200.
- Prefer Regular, Medium, Semibold, Bold. Avoid Ultralight, Thin, Light at text sizes (HIG).
- At accessibility sizes: stack horizontally adjacent items, let rows grow to multiple lines, drop a column from grids, keep the primary element at the top. Never truncate a row label to one line in a scrolling list at AX sizes.
- Do not scale everything. Tab labels and chrome need not grow as much as content (HIG: people enlarge text to read content, not tab titles).
- Three or more lines of text never get tight leading, even in a cramped row.
- Test: run the screen at xS, Large, xxxL and AX5 (iOS) and at font scale 1.0, 1.3, 2.0 (Android). Fail any clipped text, overlapping views, or a primary action pushed off screen without scroll.

## 4. Layout: margins, size classes, panes

### iOS / iPadOS

- Decide layout by size class, never by device model or orientation (HIG). Horizontal compact = iPhone portrait, most iPhone landscape, narrow iPad windows. Regular = iPad full screen and wide windows.
- Keep functionality identical across size classes; only change how much is visible (tab bar becomes sidebar, overflow items come out).
- UIKit default layout margins are 16 pt in compact width and 20 pt in regular width (framework default, read `layoutMargins` / `safeAreaInsets` rather than hardcoding). Use the readable content guide for long text on iPad so lines stay comfortable.

### Android window size classes (width)

| Class | Width | Typical | Panes (Compose adaptive default) | Navigation (NavigationSuiteScaffold default) |
|---|---|---|---|---|
| Compact | < 600 dp | 99.96 percent of phones in portrait | 1 | Navigation bar |
| Medium | 600 to 839 dp | tablets and unfolded foldables in portrait | 1 (list-detail can use 2) | Navigation rail |
| Expanded | 840 to 1199 dp | tablets in landscape | 2, spacer 24 dp | Rail (or permanent drawer by override) |
| Large | 1200 to 1599 dp | large tablets | up to 3, spacer 24 dp | Rail / drawer |
| Extra-large | >= 1600 dp | desktop displays | up to 3, spacer 24 dp | Rail / drawer |

Height classes: compact < 480 dp (99.78 percent of phones in landscape), medium 480 to 899 dp, expanded >= 900 dp. A phone in landscape is medium width but compact height: do not put two panes there.

- Default pane width is 360 dp (412 dp on extra-large). A list pane narrower than 360 dp starts truncating row text.
- Margins: 16 dp on compact, 24 dp on medium and wider (Material layout guidance; the Compose pane spacer of 24 dp matches).
- Canonical layouts: list-detail (side by side on expanded, one at a time below), feed (adaptive grid, example min column 180 dp), supporting pane (about 70/30 on expanded, 50/50 on medium, stacked or a bottom sheet on compact).
- Optimize expanded first, then decide whether medium needs its own layout (Android guidance).

### Safe areas and edges

- Respect safe areas on iOS (Dynamic Island, home indicator, rounded corners) and window insets on Android. Since Android 15 (targetSdk 35) every app is edge to edge by force.
- Backgrounds, top app bars, bottom bars and scrolling content draw behind system bars. Tappable controls (FABs, buttons, the last list row) are padded out of them. Lists use bottom padding with `clipToPadding=false` so the last row can scroll clear of the gesture bar.
- Keep swipeable controls (carousels, bottom sheets, sliders) out of the system gesture insets: the bottom home gesture strip and the left and right back gesture strips on Android 10+, the home indicator area and the left edge back swipe on iOS.

## 5. Bars and chrome heights

Values marked "default" are framework measurements, not rules. With iOS 26 Liquid Glass the tab bar floats above content and bars are lighter; read insets at runtime.

| Element | iOS (UIKit classic default) | Android (Material 3 token) |
|---|---|---|
| Status bar | 44 to 59 pt depending on notch / Dynamic Island | about 24 dp, taller with cutouts |
| Top bar | navigation bar 44 pt; large title adds about 52 pt | small app bar 64 dp, medium 112 dp, large 152 dp |
| Bottom navigation | tab bar 49 pt plus 34 pt home indicator inset | navigation bar 64 dp (flexible, M3 Expressive) or 80 dp (baseline) |
| Home / gesture area | 34 pt bottom inset portrait, about 21 pt landscape | gesture handle inset, read `systemGestures()` |
| FAB | not a platform pattern | 56 dp (24 icon), medium 80 dp (28 icon), large 96 dp (32 icon) |
| Buttons | system button sizes small / medium / large | XS 32 dp, S 40 dp, M 56 dp container heights |
| List row | 44 pt minimum, grows with text | one line 56 dp, two line 72 dp, three line 88 dp |
| Search bar | system search field | 56 dp |
| Snackbar | not a platform pattern | 48 dp one line, 68 dp two lines |
| Navigation rail | not on iPhone | 80 dp narrow / 96 dp collapsed, 220 to 360 dp expanded |
| Navigation drawer | not a platform pattern | 360 dp wide, item 56 dp tall, indicator 336 dp |
| Bottom sheet handle | grabber | 32 x 4 dp, top corners 28 dp |

## 6. Shape, elevation, state layers (Material 3)

- Corner scale: none 0, extra small 4, small 8, medium 12, large 16, large increased 20, extra large 28, extra large increased 32, extra extra large 48, full (pill). Dialogs and sheets use 28; cards 12; chips and text fields 8 and 4.
- Elevation levels: 0, 1, 3, 6, 8, 12 dp. Navigation bar level 2 (3 dp), modal drawer and sheets level 1, snackbar level 3, standard rail and drawer level 0. In M3 elevation shows mostly as a tonal surface shift, not a heavy shadow.
- State layer opacity: hover 8 percent, focus 10 percent, pressed 10 percent, dragged 16 percent. Disabled content 38 percent, disabled container 12 percent. Scrim behind modals 32 percent.
- iOS: use system materials (ultra thin, thin, regular, thick) and vibrant label colors on them; do not use the quaternary label color on thin materials (too little contrast). Liquid Glass is for the control layer only, never for content. Over bright media with clear glass add a 35 percent dark dimming layer.

## 7. Motion tokens

| Token | Value |
|---|---|
| M3 durations | short 50 / 100 / 150 / 200 ms, medium 250 / 300 / 350 / 400 ms, long 450 to 600 ms, extra long 700 to 1000 ms |
| Emphasized easing | cubic-bezier(0.2, 0, 0, 1); decelerate (0.05, 0.7, 0.1, 1); accelerate (0.3, 0, 0.8, 0.15) |
| Standard easing | cubic-bezier(0.2, 0, 0, 1); decelerate (0, 0, 0, 1); accelerate (0.3, 0, 1, 1) |
| M3 standard springs | spatial: damping 0.9, stiffness 700 (fast 1400, slow 300); effects (color, opacity): damping 1.0, stiffness 1600 |
| M3 Expressive springs | spatial: damping 0.8, stiffness 380 (fast 0.6 / 800, slow 0.8 / 200) |
| Apple (WWDC18 Fluid Interfaces) | specify springs by damping ratio and response, not duration. Default 100 percent damping (no overshoot); about 80 percent when a flick with momentum drives the motion |
| Gesture hysteresis (iOS) | 10 pt of travel before a swipe is recognized |

Rules: spatial movement uses a spring, color and opacity use a critically damped (no bounce) spring or a short ease. Every gesture driven animation must be interruptible and redirectable mid flight. Respect Reduce Motion / "Remove animations" by swapping slides and zooms for cross fades.

## 8. Color and contrast floor

| Text | Minimum contrast |
|---|---|
| Up to 17 pt (iOS) / under 18 sp (Android) | 4.5 : 1 |
| 18 pt and up, or bold (iOS); 18 sp+ or 14 sp+ bold (Android) | 3 : 1 |
| Icons and control boundaries | 3 : 1 against the adjacent color |

- Check both light and dark appearance, and the Increase Contrast setting on iOS.
- Never use color as the only signal of state. Halide learned this in field testing: a yellow "active" tint alone left a tester shooting a whole trip in the wrong RAW mode. Add shape, fill, or a label.

## 9. Checklist before you ship a screen

- [ ] Every target is >= 44 pt / 48 dp, and edge bars are taller than the minimum.
- [ ] Text uses system styles / type tokens; screen works at AX5 and 200 percent scale.
- [ ] Layout decided by size class / window class, tested at compact, medium, expanded and phone landscape.
- [ ] Content draws edge to edge; controls sit inside safe areas and outside gesture insets.
- [ ] Contrast passes in light, dark and high contrast.
- [ ] Motion is interruptible, springs have no overshoot unless a flick drives them, Reduce Motion handled.
- [ ] No hardcoded bar heights: insets read at runtime.
