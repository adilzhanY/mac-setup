# Fuzzing

How to find crashes, hangs and memory blowups in code that reads untrusted input, by letting a coverage guided fuzzer generate millions of inputs. Fuzzing is not a replacement for example tests or property tests; it is the tool that reaches inputs nobody thought of. kwx-developer `languages/rust/testing.md` section 9 says "fuzz every parser of untrusted input"; this file is how to do it in Rust, JavaScript and Python, how to pick targets, and how to run it so it pays.

## Contents

1. Property test or fuzz target
2. Where fuzzing pays
3. Writing a good fuzz target
4. Rust: cargo-fuzz and libFuzzer
5. Structure aware fuzzing with `arbitrary`
6. JavaScript: Jazzer.js
7. Python: Atheris
8. Running it: corpus, time, CI
9. Lessons from OSS-Fuzz
10. Checks

## 1. Property test or fuzz target

| | Property test (proptest, fast-check, Hypothesis) | Coverage guided fuzzing (libFuzzer, Jazzer.js, Atheris) |
|---|---|---|
| Input generation | random from a strategy you write | mutation of a corpus, guided by which code paths new inputs reach |
| Finds | violated invariants in a known input space | crashes, panics, hangs, out of memory, sanitizer errors in unknown corners |
| Run time | seconds, in every test run | minutes to days, scheduled |
| Assertion | your property | "does not crash" plus any asserts you add |
| Result kept | regression file with failing seeds | a corpus of interesting inputs and crash artifacts |

Use both: property tests in every PR for invariants; fuzz targets on a schedule for parsers. `bolero` (Rust) lets one harness run in both modes. Evidence: moderate (rust-fuzz book, Atheris and proptest docs).

## 2. Where fuzzing pays

High value targets, in order:

1. Parsers of untrusted bytes: file formats (images, PDFs, archives, fonts, subtitles), network protocols, binary messages.
2. Parsers of untrusted text: config files, markdown, templates, query languages, URL and date parsers, CSV import.
3. Decoders and decompressors.
4. Anything with `unsafe` Rust, FFI, or C libraries underneath.
5. Serializer round trips: `decode(encode(x)) == x` as a fuzz assertion.
6. Differential targets: two implementations (old and new, yours and a reference) must agree.

Low value: CRUD handlers whose input is already validated by a schema (Schemathesis covers those better), UI code, code with heavy IO per call.

For the owner's stacks: a Rust TUI or CLI that reads files or config, a subtitle or lyrics parser, a chess PGN or FEN parser, a JSON import feature, anything that decodes data from the network.

## 3. Writing a good fuzz target

Rules (OSS-Fuzz and libFuzzer guidance):

1. **Fast:** thousands of executions per second. No network, no disk writes, no sleeps. Evidence: strong.
2. **Deterministic:** the same input gives the same path. Seed any randomness from the input itself. Evidence: strong.
3. **No global state carried between runs,** or crashes cannot be reproduced. Evidence: strong.
4. **Limit input size** unless big inputs are needed to reach the code; OSS-Fuzz says a size check significantly improves performance. Evidence: moderate.
5. **Panics are findings, but only real ones.** If the API documents a panic for some input, filter that input out at the top of the target, do not catch all panics. Evidence: opinion.
6. **Add assertions:** round trip equality, "output length is bounded", "never allocates more than X". A fuzzer only reports what fails. Evidence: moderate.
7. **Seed corpus and dictionary:** a few real sample files and a dictionary of keywords (`{`, `"key":`, magic bytes) speed it up a lot. OSS-Fuzz calls a seed corpus one of the best ways to improve coverage. Evidence: moderate.

## 4. Rust: cargo-fuzz and libFuzzer

cargo-fuzz (0.13.2) needs a nightly toolchain because it passes `-Z` flags for sanitizers (rust-fuzz book).

```bash
cargo install cargo-fuzz
cargo fuzz init                 # creates fuzz/ with a first target; commit it
cargo fuzz add parse_config     # fuzz/fuzz_targets/parse_config.rs
cargo +nightly fuzz run parse_config -- -max_total_time=300
cargo fuzz list
```

```rust
// fuzz/fuzz_targets/parse_config.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if data.len() > 64 * 1024 { return; }
    if let Ok(s) = std::str::from_utf8(data) {
        if let Ok(cfg) = my_crate::Config::parse(s) {
            // round trip assertion: a parsed config must serialize and parse back to itself
            let again = my_crate::Config::parse(&cfg.to_string()).expect("round trip parse");
            assert_eq!(cfg, again);
        }
    }
});
```

After a crash:

```bash
# the crashing input is saved under fuzz/artifacts/parse_config/
cargo +nightly fuzz run parse_config fuzz/artifacts/parse_config/crash-<hash>   # reproduce
cargo +nightly fuzz tmin parse_config fuzz/artifacts/parse_config/crash-<hash>  # minimise
cargo +nightly fuzz cmin parse_config      # shrink the corpus, keeping coverage
cargo +nightly fuzz coverage parse_config  # coverage report of the corpus
```

Then copy the minimised input into a normal unit test, so the bug stays fixed on stable without the fuzzer. Evidence: strong (standard practice; kwx-developer bug fix rule).

`-max_total_time`, `-max_len`, `-dict=` and `-jobs=` are libFuzzer flags passed after `--` (LLVM libFuzzer docs). Commands in this section are from the rust-fuzz book and libFuzzer docs; they were not run here because the machine has no nightly toolchain installed.

## 5. Structure aware fuzzing with `arbitrary`

When the input is a structured value (a sequence of API calls, an AST, a config struct), let the fuzzer build it from bytes:

```rust
use libfuzzer_sys::{arbitrary::Arbitrary, fuzz_target};

#[derive(Debug, Arbitrary)]
enum Op { Insert(u16, String), Remove(u16), Get(u16) }

fuzz_target!(|ops: Vec<Op>| {
    let mut real = my_crate::Store::new();
    let mut model = std::collections::HashMap::new();
    for op in ops {
        match op {
            Op::Insert(k, v) => { real.insert(k, v.clone()); model.insert(k, v); }
            Op::Remove(k) => { assert_eq!(real.remove(k), model.remove(&k)); }
            Op::Get(k) => { assert_eq!(real.get(k), model.get(&k)); }
        }
    }
});
```

This is model based (differential) fuzzing: the store must behave like a `HashMap`. It finds logic bugs, not only crashes. Evidence: moderate (rust-fuzz book "Structure-Aware Fuzzing").

## 6. JavaScript: Jazzer.js

Jazzer.js is a libFuzzer based, in process fuzzer for Node.js. Status check (2026-10-31): `@jazzer.js/core` 4.0.0 was published 2026-04-15 and is not marked deprecated on npm. Some web pages say open source maintenance stopped in 2025; the 2026 release shows it is active again. Check the npm page before adopting it.

```bash
npm install --save-dev @jazzer.js/core
npx jazzer fuzz/parse-csv        # runs module.exports.fuzz from fuzz/parse-csv.js
```

```js
// fuzz/parse-csv.js
const { parseCsv } = require('../src/csv');

module.exports.fuzz = function (data /* Buffer */) {
  const text = data.toString();
  try {
    parseCsv(text);
  } catch (e) {
    if (e instanceof SyntaxError) return;   // documented error for bad input
    throw e;                                 // anything else is a finding
  }
};
```

Jest integration (Jazzer.js README) keeps fuzz tests next to unit tests: `import "@jazzer.js/jest-runner";` then `it.fuzz("parses any input", (data) => { ... })`. In normal Jest runs it replays the corpus as regression tests; in fuzzing mode it explores.

If Jazzer.js is not an option, use fast-check property tests with large `numRuns` on a schedule; they are not coverage guided but they need no native build.

## 7. Python: Atheris

Atheris (Google) supports Python 3.11 to 3.14 and ships wheels with libFuzzer built in (Atheris README). Useful for helper scripts and Python services.

```python
import sys
import atheris

with atheris.instrument_imports():      # instruments modules imported inside this block
    import my_parser

def TestOneInput(data: bytes):
    fdp = atheris.FuzzedDataProvider(data)
    text = fdp.ConsumeUnicodeNoSurrogates(4096)
    try:
        my_parser.parse(text)
    except my_parser.ParseError:
        pass

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

Run: `python3 fuzz_parse.py -max_total_time=300 corpus/`. `FuzzedDataProvider` turns bytes into ints, strings and choices when the target needs typed values.

## 8. Running it: corpus, time, CI

- **Keep the corpus.** Commit a small minimised seed corpus (`fuzz/corpus/<target>/`) or store the full corpus as a CI artifact or cache. Each run starts where the last one ended. Evidence: strong.
- **Short run per PR, long run on a schedule.** A 60 to 300 second run per PR on changed parsers catches shallow regressions; a nightly or weekly run of an hour or more finds deep bugs. Evidence: moderate.
- **Replay the corpus as a regression test on stable.** Iterate over `fuzz/corpus/<target>/*` in a normal test and call the parser; it costs seconds and protects past findings.
- **Track coverage of the corpus** with `cargo fuzz coverage` to find code the fuzzer never reaches, then add seeds or a structure aware target.
- **Open source projects** can apply to OSS-Fuzz (free); closed source projects can run ClusterFuzzLite in their own CI (OSS-Fuzz docs).
- **Resource limits:** set `-rss_limit_mb` and `-timeout` so the fuzzer reports out of memory and hangs as findings instead of killing the CI machine.

## 9. Lessons from OSS-Fuzz

- Scale: over 10,000 vulnerabilities and 36,000 bugs fixed across 1,000 projects (OSS-Fuzz, August 2023). Fuzzing keeps finding bugs in mature, heavily tested code. Evidence: strong.
- Memory safe languages still crash: OSS-Fuzz expanded to Rust, Go and Python because panics, hangs, unbounded allocation and logic bugs remain. In Rust, a panic on input is a denial of service bug. Evidence: strong.
- Integration advice from the new project guide: link against `$LIB_FUZZING_ENGINE` instead of assuming libFuzzer, keep fuzz targets in the project's own repository, keep source files so coverage works, and add a size check to the target. Evidence: moderate.
- The bugs found are only useful if fixed: every crash gets a minimised regression test before the fix (section 4). Evidence: strong.

## 10. Checks

| Check | Pass condition |
|---|---|
| Targets exist | one fuzz target per parser of untrusted input |
| Target quality | fast, deterministic, no global state, input size limited, real assertions added |
| Structured inputs | stateful components have an `arbitrary` based model target |
| Seeds | seed corpus and dictionary committed for each target |
| Schedule | short run on PRs touching parsers; long run nightly or weekly |
| Corpus kept | corpus cached or committed between runs |
| Regression | every crash minimised and copied into a normal unit test; corpus replayed on stable |
| Limits | `-rss_limit_mb` and `-timeout` set |
| Coverage | corpus coverage checked at least once per target |
