# Canarying Releases (The Site Reliability Workbook, chapter 16)

- Authors: Google SRE (Alec Warner, Štěpán Davidovič)
- Year: 2018
- Legal URL: https://sre.google/workbook/canarying-releases/ (free online edition from Google)

## What I read

The chapter, through a summary of its sections: definition, canary versus control, metric selection, duration and size, before and after versus simultaneous comparison, rollback.

## Key lessons used in quality/regression-and-release-testing.md

- A canary is "a partial and time-limited deployment of a change in a service and its evaluation".
- Compare canary and control at the same time; before and after comparisons are distorted by time effects.
- Break metrics down per population: a 5% canary failing 20% of requests shows as about 1% overall.
- Choose a few user facing metrics (at most about a dozen); prefer error rate and latency over CPU and memory.
- Run one canary at a time; size and duration must fit the release cadence and include real traffic.
- If the canary's error rate is far from the control's, pause and roll back or escalate.
