# How Not to Measure Latency (talk slides) and the wrk2 README

- Author: Gil Tene (Azul Systems)
- Year: 2012 slides (QCon San Francisco 2012; the talk was given again until 2016); wrk2 README, about 2014
- Legal URL: https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/GilTene_HowNotToMeasureLatency.pdf (conference hosted slides); https://github.com/giltene/wrk2 (README)

## What I read

The full slide deck as text (requirements interview, the four kinds of latency needs, fallacies, the coordinated omission section with the 100 second stall example, the "real world" examples, lessons learned, HdrHistogram). The wrk2 README sections on coordinated omission, constant throughput and corrected vs uncorrected latency.

## Key lessons used in performance/performance.md (also load-testing.md)

- Latency requirements are pass/fail criteria at several percentiles plus a max; an interview turns "20 ms average" into "50% < 20 ms, 90% < 50 ms, 99.9% < 500 ms, 100% < 2 s".
- Latency is multi modal ("hiccups"), not normal; do not use or derive from standard deviation.
- "Always measure Max time." "Measure %'iles. Lots of them."
- A user has many interactions per session, so high percentiles are common experiences.
- Coordinated omission: a closed loop tester backs off during stalls. Example: 1 ms responses then a 100 s stall gives a naive p99.99 of 1 ms and an average of 10.9 ms, while the honest average is about 25 s and p99.99 about 100 s.
- "Whatever your measurement technique is, test it" against an artificial system with known pauses.
- wrk2 measures from the intended send time at a constant rate; with a 1.4 s pause its corrected p99 was about 1.27 s vs about 6 ms uncorrected (about 200x).
- HdrHistogram: wide dynamic range at fixed precision, constant recording cost.
