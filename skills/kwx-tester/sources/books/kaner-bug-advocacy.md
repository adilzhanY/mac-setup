# Bug Advocacy

- Author: Cem Kaner
- Year: 2002 (Quality Week 2002 slides, Florida Institute of Technology; NSF supported)
- Legal URL: https://kaner.com/pdfs/BugAdvocacy.pdf (author's site)

## What I read

The full slide paper: selling bugs, motivating the fixer, overcoming objections, follow up testing, configuration dependence, uncornering corner cases, non reproducible errors and the conditions often missed, the dumpster, writing and editing the report.

## Key lessons used in exploratory/bug-reports.md

- "The best tester isn't the one who finds the most bugs ... The best tester is the one who gets the most bugs fixed"; a report also succeeds if it "enables an informed business decision".
- Motivate the buyer and overcome objections (cannot replicate, too complex, not enough information, unrealistic corner case, "it's a feature").
- Follow up testing: vary behaviour, options and settings, configuration; check whether the bug is new to this version.
- Replicate every bug on a second machine; name configuration dependence.
- Uncorner corner cases: retry with mainstream values; report the narrow range if only extremes fail.
- Never say reproducible unless you recreated it; say "No" or "Sometimes" and explain.
- One failure per report; shortest steps first, numbered; variations in an "Additional conditions" section.
- Non reproducible bugs are data: hidden inputs, delayed effects, initial state, timing, error handling after errors, corrupted data, co resident software. Watts Humphrey's idea of keeping a personal list of missed conditions.
- RIMGEA is Kaner's BBST mnemonic (Replicate, Isolate, Maximize, Generalize, Externalize, And say it clearly and dispassionately); not spelled out in this 2002 paper, confirmed through Bolton's 2017 slides.
