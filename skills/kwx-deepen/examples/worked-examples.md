# Worked examples

Short requests from different fields, the output block the skill shows, and what changed.
The field playbooks each have one longer worked example.

## 1. Writing: "Write a cover letter for a senior backend job at a payments company"

```
Deepened: writing, same size (one page, under 350 words)
Expert: technical recruiter who screens backend CVs for payments companies every week
Real goal: get past the first 30 second screen to a call with the hiring manager
Moves: match the posting's top 3 requirements to 3 real results with numbers; open with the
  strongest match, not "I am writing to apply"; name one thing about the company's product
  that only someone who looked would know
Raw material: the job posting (fetched), the applicant's CV and two shipped projects (asked for)
Method: requirement to evidence table first, then the letter; read aloud for length
Proof: each of the 3 requirements has a sentence that a stranger can check against the CV
Not doing: inventing experience, a second version, redesigning the CV
```
What changed: the letter is built from the posting and the CV, not from a template, and
each claim can be checked.

## 2. Software: "Fix the flaky test in checkout.spec.ts"

```
Deepened: software, same size (one fix, one PR)
Expert: test infrastructure engineer who has hunted timing and shared state flakes in CI
Real goal: a test that fails only when checkout is broken
Moves: reproduce first (run it 50 times, and alone vs in the suite); classify the cause
  (timing, shared state, order, network) before touching code; fix the cause, not the wait
Raw material: the last 20 CI logs for this test, the test file, the code it covers
Method: repeated runs with a fixed seed, then with shuffled order
Proof: 100 green runs in CI order and shuffled, and the test still fails when the guarded
  line is broken on purpose
Not doing: refactoring the suite, raising global timeouts, adding retries
```

## 3. Product: "Make my landing page convert better"

```
Deepened: product, same size (changes to one page)
Expert: conversion specialist who has run message tests for B2B SaaS signups
Real goal: more qualified signups, not more clicks
Moves: find where people drop (the funnel), not what looks dated; test the headline against
  the top reason customers gave for buying; cut the step with the biggest drop
Raw material: analytics funnel for 90 days, 20 recent support or sales questions, 5 session
  recordings
Method: five second test on the hero, funnel by source and device
Proof: an A/B test on signups with the sample size worked out before it starts
Not doing: a rebrand, a new design system, new pages
```

## 4. Research: "Summarise this paper for my team"

```
Deepened: research, same size (half a page)
Expert: methods reviewer who reads trials for a journal club
Real goal: know whether the headline result should change what the team does
Moves: read methods and limitations before the abstract; check the effect size and the
  comparison group; note who funded it
Raw material: the full paper and its supplementary data (fetched), not the press release
Method: claim by claim check against the paper's own tables
Proof: every number in the summary is quoted with its table or page
Not doing: a literature review, other papers, recommendations beyond the paper
```

## 5. No playbook: "/deepen plan a three day trip to Lisbon"

```
Deepened: general, same size (a three day plan, one screen per day)
Expert: local guide who plans short trips for first time visitors
Real goal: see the main things without queues or crossing the city twice a day
Moves: group sights by neighbourhood; put timed entry places first in the morning; leave one
  slack block per day
Raw material: official opening hours and closing days, the transit map, this week's events
Method: day plans by area, travel times from the transit planner
Proof: every opening time and closing day checked on the official site for those dates
Not doing: restaurant reviews, a budget sheet, a fourth day
Assumptions: dates not given; plan for any weekday, flagged Monday closures
```
