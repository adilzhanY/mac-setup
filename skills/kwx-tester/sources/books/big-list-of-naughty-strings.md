# Big List of Naughty Strings (BLNS)

- Author: Max Woolf (minimaxir) and contributors
- Year: 2015 onward (repository, MIT licence)
- Legal URL: https://github.com/minimaxir/big-list-of-naughty-strings (blns.txt, blns.json)

## What I read

The README and the full `blns.txt` section headings; downloaded `blns.json` (515 strings) and ran it through a test driver against a toy local server.

## Key lessons used in exploratory/edge-case-catalogue.md

- Sections: reserved strings, numeric strings, special characters, Unicode symbols, subscripts and accents, quotation marks, two byte characters, strings that change length when lowercased, emoji, Unicode numbers, RTL, trick Unicode, Zalgo, upside down, script, SQL and server code injection, unwanted interpolation, file inclusion, known CVEs, MSDOS and Windows special file names, Scunthorpe problem, terminal escape codes, iMessage crashers.
- `blns.txt` has `#` comment lines for people; `blns.json` is the machine list.
- For software you own; using it against third party software "may be a crime"; not a substitute for a security test.
- Two strings (index 96 and 113) are longer than 255 UTF-16 units, so the list also exercises length limits.
