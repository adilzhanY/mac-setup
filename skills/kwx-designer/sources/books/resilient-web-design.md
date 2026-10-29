# Resilient Web Design (Jeremy Keith)

- **Status:** free online, PDF, EPUB and audio; CC BY-SA 4.0.
- **Legal source:** https://resilientwebdesign.com
- **Read:** table of contents, Chapter 2 (Materials), Chapter 5 (Layers), October 2026.
- **Who recommends it:** a standard web craft recommendation among front end and design engineers; quoted by Vercel and Rauno-style "work with the material" designers (Rauno Freiberg's own advice: "Work with the material").

## Key lessons

**Materials (ch. 2)**
- HTML is a vocabulary of meaning, not visual instructions. Presentation tags (`FONT`, `CENTER`) and spacer GIF and table layouts were hacks that made HTML a "visual instruction language".
- Honesty of materials, from architecture: "One material should not be used as a substitute for another. Otherwise the end result is deceptive." Table layouts look fine "but won't stand up to scrutiny".
- Browsers ignore unknown HTML and CSS without throwing errors. That tolerance is why new features (`border-radius`) could ship before full support: "Some people will see rounded corners. Others won't. And that's okay."

**Layers (ch. 5)**
- Shearing layers (Duffy, popularized by Stewart Brand): a building has layers that change at different speeds. On the web: URLs slowest, then HTML structure, CSS presentation, JavaScript behaviour, content fastest. Build from the bottom up.
- Progressive enhancement (Champeon and Finck, 2003): separate semantic markup from presentation and behaviour. Same content for everyone, experience scaled to the device.
- Feature detection ("cutting the mustard", BBC): test for the feature, enhance when present, omit the else branch.
- "There is a difference between support and optimization" (Brad Frost). Support everyone at the core; optimize for capable browsers.
- Core functionality reaches everyone; enhancements may fail without breaking it ("reading the news" should work when JavaScript breaks).

## Rules taken for the skill

- Use the real platform property for an effect (radius, shadow, blur), never an image or hack that imitates it.
- Every premium effect (glass, blur, motion, custom font) must degrade to a clean, usable base: reduced transparency, reduced motion, slow network, no JavaScript where possible.
- Decide what is core and what is enhancement before designing the polish.

## Used in

`../../premium/materials-depth-light.md`, `../../premium/details-and-polish.md`.
