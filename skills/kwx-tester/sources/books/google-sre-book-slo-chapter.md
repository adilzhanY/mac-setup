# Site Reliability Engineering, chapter 4: Service Level Objectives

- Authors: Chris Jones, John Wilkes, Niall Murphy, Cody Smith (eds. Beyer, Jones, Petoff, Murphy)
- Year: 2016
- Legal URL: https://sre.google/sre-book/service-level-objectives/ (free online edition by Google)

## What I read

The chapter sections on indicators, percentiles vs averages, aggregation, and the SLI template.

## Key lessons used in performance/performance.md

- "Using percentiles for indicators allows you to consider the shape of the distribution."
- A simple average can obscure tail latencies and changes in them; example of most requests near 50 ms while 5% are 20 times slower.
- High percentiles (99th, 99.9th) show a plausible worst case.
- Aggregation windows hide bursts: 200 req/s on even seconds and 0 on odd ones averages to 100 req/s.
