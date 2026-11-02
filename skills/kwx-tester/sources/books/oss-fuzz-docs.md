# OSS-Fuzz documentation

- Author: Google OSS-Fuzz team
- Year: living documentation, read 2026-10-31
- Legal URL: https://google.github.io/oss-fuzz/ ; https://google.github.io/oss-fuzz/getting-started/new-project-guide/

## What I read

The front page and the new project guide.

## Key lessons used in backend/fuzzing.md (also backend.md)

- As of August 2023: over 10,000 vulnerabilities and 36,000 bugs fixed across 1,000 projects.
- Languages beyond C/C++: Rust, Go, Python, Java, JavaScript, Lua.
- Seed corpus is one of the best ways to improve coverage; dictionaries help inputs with repeated tokens; a size check in the target improves performance.
- Link with `$LIB_FUZZING_ENGINE`, keep targets in the project repo, keep sources for coverage.
- Closed source projects can use ClusterFuzzLite.
