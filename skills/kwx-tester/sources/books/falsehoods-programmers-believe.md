# Falsehoods programmers believe (collection)

- Authors: collection by Kevin Deldycke (awesome-falsehood); essays by Patrick McKenzie (names, 2010), Noah Sussman (time, 2012), Google libphonenumber team (phone numbers), Michael Tandy (addresses), and others
- Year: 2010 onward
- Legal URLs: https://github.com/kdeldycke/awesome-falsehood ; https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/ ; https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time (returned 403, read via the Internet Archive copy) ; https://github.com/google/libphonenumber/blob/master/FALSEHOODS.md

## What I read

The awesome-falsehood index; the first 25 name falsehoods; the full time list (archived copy); the libphonenumber falsehood headings.

## Key lessons used in exploratory/edge-case-catalogue.md

- Names: not one canonical name, do not fit a fixed space, change, are not ASCII or one script, not uniformly cased, may contain numbers, may lack a family name, first and last can be equal, order varies, not unique.
- Time: not always 24 hours in a day, months not only 30 or 31 days, weeks cross months and years, the zone a program runs in can change, system clocks can be wildly wrong, client and server clocks differ (even by decades).
- Phone numbers: not numbers, reused, one calling code for several countries, not always ASCII digits, cannot always be texted, the plus sign is not optional.
