# Touch Design for Mobile Interfaces (Steven Hoober, Smashing Media, 2021)

## What was read, and where

- Official free sample from the publisher (40 pages): https://smashingmagazine.com/provide/eBooks/touch-design-for-mobile/touch-design-for-mobile-interfaces-sample-chapter.pdf (read via pdftotext). It contains the front matter, full table of contents, chapter 1 "Defining Mobile Devices" and the full index.
- The book's research chapters (5 "Finding Out How People Hold and Touch", 6 "Touch Accuracy and the Center-Out Preference", 11 "Designing By Zones") are not in the sample. Their headline numbers were taken from Hoober's own free articles and from Smashing's article summarizing the book:
  - "How Do Users Really Hold Mobile Devices?" UXmatters 2013: https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php (read)
  - "Design for Fingers, Touch, and People, Part 1" UXmatters 2017: https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php (read)
  - "Fitts's Law in the Touch Era" Smashing 2022: https://www.smashingmagazine.com/2022/02/fitts-law-touch-era/ (read)
  - Smashing "Accessible Target Sizes Cheatsheet" 2023 (cites the book's region sizes): https://www.smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/ (read)

## Key lessons

1. Touch is learned, not natural. Touchscreen conventions are as learned as using a mouse or a doorknob, so do not assume touch "just works" (chapter 1).
2. Mobile means always on, always with us, and aware (sensors, connectivity). Laptops are increasingly touch devices too: over 40 percent of laptops sold in 2020 were 2 in 1s and over half of laptops in 2021 had touchscreens, used tablet style (chapter 1). Desktop UI must survive a finger.
3. Grip: 49 percent one handed, 36 percent cradled, 15 percent two handed (2013, 780 people). About 75 percent of touches use one thumb, but fewer than half of people hold the phone in one hand (2017). Grips change every few seconds with the task.
4. Center out preference: people look at, scroll to and tap the center most; accuracy is best in the center. The old thumb reach arc diagrams were withdrawn by Hoober himself.
5. Target size by region for 95 percent of taps: center as small as 7 mm (about 20 pt), top about 11 mm (31 pt), bottom about 12 mm (34 pt), corners about 12 mm. Sizes include padding. Finger size does not predict accuracy; the 22 mm ISO figure is obsolete.
6. Three zones: content in the middle, secondary persistent actions (tabs, search, compose) on the top and bottom edges, tertiary functions in menus from a corner.
7. Fitts's law does not map cleanly to touch: the hand's start position is unknown, so no edge is "close". Edges and corners are the hardest areas to tap, not magic edges.
8. Avoid timed controls and timed notifications; prefer undo over confirmation; prefer contextual UI (accordions, drawers, in place expansion) over disconnected pop ups.
9. Build a device lab of the phones your users actually own, including cheap Android phones and feature phones; test on cellular, not only Wi-Fi.
10. Index topics worth knowing exist in the book: parallax compensation, contact patch and centroid, "phones are not flat" (edges and curved screens), "people only touch what they see" (visible affordances), progressive disclosure patterns (accordions, drawers, tabs, chyrons).

## Where this lives in the skill

`platforms/mobile/mobile-foundations.md` section 2 (target sizes by region), `platforms/mobile/gestures-and-haptics.md` sections 1 and 2 (grips, center out, zones), `platforms/mobile/states-loading-empty-offline.md` section 9 (undo over confirm), `platforms/desktop/desktop-foundations.md` section 3 (touch laptops).
