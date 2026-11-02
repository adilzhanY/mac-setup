# Test Heuristics Cheat Sheet

- Authors: Elisabeth Hendrickson, with ideas from James Lyndsay and Dale Emery
- Year: 2006 (Quality Tree Software)
- Legal URL: originally http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf (the author's free download); that host now fails TLS, so I read the Internet Archive copy of the same URL: https://web.archive.org/web/2019id_/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf

## What I read

Both pages: data type attacks (paths and files, time and date, numbers, strings, general), web tests, testing wisdom, heuristics and frameworks.

## Key lessons used in exploratory/heuristics.md and exploratory/edge-case-catalogue.md

- Heuristics: variable analysis, touch points, boundaries, Goldilocks, CRUD, follow the data (enter, search, report, export, import, update, view), configurations, interruptions (log off, shut down, reboot, kill process, disconnect, hibernate, timeout, cancel), starvation, position, selection, count (0, 1, many), multi user, flood, dependencies, constraints, input method, sequences, sorting, state analysis, map making, users and scenarios.
- Data type attacks: numbers 32768, 65536, 2^31, 2^32 and neighbours; European number style 1.234.567,89; Feb 29 in non leap years; DST changeover; long strings 255, 256, 257, 1000, 1024, 2000, 2048; file names over 255 characters and with special characters; no space, write protected, locked, corrupted.
- Frameworks: Lyndsay's judgment (inconsistencies, absences, extras against internal, external specific, external cultural references), nouns and verbs, Gause and Weinberg's users/functions/attributes/constraints.
- Wisdom lines: "Bugs cluster"; "Vary sequences, configurations, and data to increase the probability that, if there is a problem, testing will find it."
