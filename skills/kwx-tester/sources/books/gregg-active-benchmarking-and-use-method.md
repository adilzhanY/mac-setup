# Active Benchmarking, the USE Method, the Benchmark Paradox

- Author: Brendan Gregg
- Year: pages from 2012 to 2014, still online
- Legal URL: https://www.brendangregg.com/activebenchmarking.html ; https://www.brendangregg.com/usemethod.html ; https://www.brendangregg.com/USEmethod/use-linux.html ; https://www.brendangregg.com/blog/2014-05-03/the-benchmark-paradox.html

## What I read

The full active benchmarking page, the USE method summary and resource list, the Linux USE checklist (CPU, memory, disk, network rows), and the benchmark paradox post. Not read: Systems Performance 2nd ed. chapter 12 (the book is not free; its "benchmarking sins" list is cited only through these pages).

## Key lessons used in performance/performance.md (also benchmarks.md)

- Active benchmarking: run long, in steady state, and analyse the system during the run to find the true limiter; be able to say why the result is X and not 2X.
- Passive "fire and forget" results are usually wrong or misleading; "iostat first, R later".
- Disturbances: neighbours, resource controls, network throttling, single threaded benchmark tools, version differences, disk vs file system I/O, unrealistic workloads.
- USE: for every resource, check utilization, saturation and errors; use early to find systemic bottlenecks.
- Linux commands: vmstat 1 (r, si/so), mpstat -P ALL 1, iostat -xz 1, sar -n DEV/EDEV 1, dmesg for OOM.
- Benchmark paradox: if each comparison is near a coin toss, winning all of several is unlikely; flawed method turns benchmarks into gambling.
