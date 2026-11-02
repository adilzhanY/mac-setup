# assert_cmd, trycmd, bats-core, ratatui testing recipe, expectrl, vhs

- Authors: assert-rs project; bats-core project; ratatui project; expectrl authors; Charm (vhs)
- Year: read 2026-10-31 (assert_cmd 2.2.2, trycmd 1.2.1, bats-core 1.14, ratatui 0.30.2, termlens 0.11, expectrl 0.9, vhs 0.12.1)
- Legal URL: https://docs.rs/assert_cmd/latest/assert_cmd/ ; https://github.com/assert-rs/assert_cmd/blob/master/CHANGELOG.md ; https://docs.rs/trycmd/latest/trycmd/ ; https://bats-core.readthedocs.io/en/stable/writing-tests.html ; https://ratatui.rs/recipes/testing/snapshots/ ; https://docs.rs/expectrl/latest/expectrl/ ; https://github.com/charmbracelet/vhs

## What I read

assert_cmd docs and changelog; trycmd docs; bats writing tests page; ratatui snapshot testing recipe including the PTY section; expectrl docs; vhs README.

## Key lessons used in desktop/cli-and-tui-testing.md

- assert_cmd: `cargo_bin_cmd!` works with Cargo's build-dir; `Command::cargo_bin` deprecated in 2.1.0, un-deprecated in 2.1.3.
- trycmd: `$` commands, `? code`, `...` and `[..]` wildcards, `[ROOT]`/`[CWD]`/`[EXE]`, `TRYCMD=overwrite`, README as test cases.
- bats: `run -N`, `run !`, `--separate-stderr`, `$BATS_TEST_TMPDIR`, setup_file.
- ratatui: TestBackend plus insta snapshots; colour not captured (issue 1402); PTY tests with termlens, wait for content not time, `wait_idle` before whole screen snapshots.
- vhs: `.txt`/`.ascii` outputs as golden files; `Wait /regex/`; `Require`.
