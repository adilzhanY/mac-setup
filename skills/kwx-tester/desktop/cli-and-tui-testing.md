# CLI and TUI testing

How to test command line tools and terminal user interfaces as their users meet them: arguments in, bytes on stdout and stderr out, an exit code, files changed, and for TUIs, a screen that reacts to keys. The core idea is to run the real binary for a few end to end cases and to test rendering and key handling in process for everything else. Rust specific basics (test layout, insta) are in kwx-developer `languages/rust/testing.md`; this file covers the CLI and TUI layer on top.

## Contents

1. What to test in a CLI
2. Rust CLIs: assert_cmd
3. Golden output: trycmd, snapbox, insta
4. Shell scripts: bats
5. Exit codes, streams and signals
6. TUIs: render tests with ratatui TestBackend
7. TUIs: key handling as events
8. TUIs: PTY end to end tests
9. Recorded demos with vhs
10. Checks

## 1. What to test in a CLI

The contract of a CLI is: arguments, environment, stdin and files in; stdout, stderr, exit code and files out. Case list per command:

| Area | Cases |
|---|---|
| Arguments | no args; `--help` and `--version` exit 0 and print to stdout; unknown flag exits 2 with a usage hint on stderr; missing required value; conflicting flags; `--` before a value that starts with `-` |
| Input | empty stdin; stdin not a terminal; huge input; invalid UTF-8; CRLF line endings; a file that does not exist, is a directory, has no read permission |
| Output | stdout holds only the data (pipeable); messages, progress and errors go to stderr; no colour when stdout is not a TTY or `NO_COLOR` is set; machine readable mode (`--json`) is stable |
| Exit codes | 0 on success; documented non zero codes per failure class; partial failure behaviour |
| Files | writes are atomic (no half written file on error); existing files not clobbered without `--force`; paths with spaces and unicode |
| Environment | `HOME`, `XDG_CONFIG_HOME` missing or pointing to a temp dir; locale `C` vs UTF-8; config file invalid |
| Signals | Ctrl+C during work: cleans up temp files, exits 130; `SIGPIPE` when piped into `head` exits quietly |

Rule: **run every end to end test with a clean temp `HOME` and working directory,** so tests never read or write the user's real config. Evidence: strong (tests must not depend on or damage the machine).

## 2. Rust CLIs: assert_cmd

assert_cmd 2.2 runs your binary and asserts on the result. Use the `cargo_bin_cmd!` macro: it finds the binary through Cargo's environment and works with Cargo's `build-dir` setting (assert_cmd changelog; `Command::cargo_bin` was deprecated in 2.1.0 and un-deprecated in 2.1.3, the macro is the safer choice).

Verified 2026-10-31 with assert_cmd 2.2.2 and predicates 3:

```rust
use assert_cmd::cargo::cargo_bin_cmd;
use predicates::prelude::*;

#[test]
fn good_input_exits_zero() {
    cargo_bin_cmd!("kwxv")
        .write_stdin("a = 1\nb=2\n")
        .assert()
        .success()
        .stdout("a=1\nb=2\n")
        .stderr("");
}

#[test]
fn bad_line_exits_two_and_reports_on_stderr() {
    cargo_bin_cmd!("kwxv")
        .write_stdin("=1\n")
        .assert()
        .code(2)
        .stdout("")
        .stderr(predicate::str::contains("bad line"));
}
```

Patterns:

- Isolate the environment: `.env_clear()` then set only what the test needs, or at least `.env("HOME", tmp.path()).current_dir(tmp.path())` with `tempfile::tempdir()`.
- Files: use `assert_fs` (`TempDir`, `child("config.toml").write_str(...)`, `assert(predicate::path::exists())`) for file in, file out tests.
- Prefer in process tests for logic: put parsing and the work in the library crate and test it directly; keep `main.rs` tiny. End to end tests are for the wiring (argument parsing, exit codes, streams).
- With clap, also run `Cli::command().debug_assert()` in one unit test; it catches conflicting argument definitions (clap docs).

## 3. Golden output: trycmd, snapbox, insta

Golden (snapshot) tests store the expected output in files and compare.

**trycmd** (1.2) runs commands written in markdown or `.toml` files, which doubles as documentation:

```rust
// tests/cli_tests.rs
#[test]
fn cli_tests() {
    trycmd::TestCases::new()
        .case("tests/cmd/*.toml")
        .case("tests/cmd/*.md")
        .case("README.md");
}
```

````markdown
```console
$ kwxv --help
Usage: kwxv [OPTIONS]
...

$ kwxv missing.txt
? 1
error: could not read missing.txt: [..]
```
````

Syntax (trycmd docs): `$` starts a command, `? <code>` sets the expected exit status, a line with only `...` matches any lines, `[..]` matches the rest of a line, `[ROOT]`, `[CWD]` and `[EXE]` are built in redactions, and `TestCases::insert_var` adds your own. Update expected output with `TRYCMD=overwrite cargo test --test cli_tests` and read the diff before committing.

**snapbox** (1.2) is the library under trycmd, for custom harnesses. **insta** with `assert_snapshot!(String::from_utf8(output.stdout)?)` works too, or the `insta-cmd` crate for whole command snapshots.

Rules:

1. **Redact anything that varies:** paths, durations, timestamps, versions, temp dir names, colour codes. Evidence: strong.
2. **Run your README examples as tests** (trycmd `.case("README.md")`), so the docs never lie. Evidence: moderate.
3. **Never bulk accept new snapshots.** Read each diff; accepting a wrong snapshot bakes the bug in (kwx-developer). Evidence: strong.

## 4. Shell scripts: bats

bats-core (1.14) tests shell scripts and any command line program (bats docs):

```bash
#!/usr/bin/env bats

setup() {
  export HOME="$BATS_TEST_TMPDIR"          # unique temp dir per test
  PATH="$BATS_TEST_DIRNAME/../bin:$PATH"
}

@test "prints usage and exits 2 without arguments" {
  run -2 mytool                            # asserts exit status 2
  [[ "$output" == *"Usage:"* ]]
}

@test "errors go to stderr, not stdout" {
  run --separate-stderr mytool missing.txt
  [ "$status" -eq 1 ]
  [ -z "$output" ]                         # stdout empty
  [[ "$stderr" == *"missing.txt"* ]]
}

@test "fails when it should" {
  run ! mytool --bad-flag                  # expects a non zero exit
}
```

- `run` captures `$status`, `$output` (stdout and stderr combined unless `--separate-stderr`), and `$lines`.
- `setup`/`teardown` run per test; `setup_file`/`teardown_file` once per file.
- The bats-assert and bats-support libraries add `assert_success`, `assert_output --partial` and readable failure messages.
- Lint scripts with `shellcheck` first; it finds quoting bugs that tests rarely hit.
- On this kind of machine the user's interactive shell may not be bash (for example fish). Test scripts run with their shebang interpreter; do not assume the user's shell. Check the user's notes.

## 5. Exit codes, streams and signals

Exit code conventions to test (BSD `sysexits.h`, shells, and clap's defaults): 0 success; 1 general failure; 2 usage error (clap uses 2); 126 found but not executable; 127 not found; 128 + N killed by signal N (130 for Ctrl+C / SIGINT, 143 for SIGTERM). Whatever the tool uses, document it and test each code.

Streams:

- `mytool | head -1` must not print a "broken pipe" panic. In Rust, `println!` panics on a closed pipe; test it: run the binary with stdout connected to a pipe that is closed early and assert no panic text on stderr and a quiet exit. Evidence: moderate (common Rust CLI bug).
- Test both "stdout is a TTY" and "stdout is a pipe" when output changes (colour, progress bars, pagers). assert_cmd always uses pipes; use a PTY (section 8) for the TTY case.

Signals:

```rust
// send SIGINT to a running child and check cleanup (Unix)
use std::process::{Command, Stdio};
let mut child = Command::new(assert_cmd::cargo::cargo_bin!("mytool"))
    .arg("long-task").stdout(Stdio::piped()).spawn()?;
// wait for a "started" line on stdout instead of sleeping, then:
nix::sys::signal::kill(nix::unistd::Pid::from_raw(child.id() as i32), nix::sys::signal::Signal::SIGINT)?;
let status = child.wait()?;
assert_eq!(std::os::unix::process::ExitStatusExt::signal(&status).or(status.code().map(|c| c - 128)), Some(2));
assert!(!tmp.path().join("partial.out").exists());
```

(Sketch, not run here. The exit check accepts either "killed by signal 2" or "exited with 130", because a tool that handles SIGINT itself exits with 130.)

## 6. TUIs: render tests with ratatui TestBackend

Test what the UI draws for a given state, in process, without a terminal. ratatui's `TestBackend` keeps a buffer, and insta snapshots it as text (ratatui testing recipe).

Verified 2026-10-31 with ratatui 0.30.2 and insta 1.49:

```rust
use ratatui::{Terminal, backend::TestBackend, widgets::{Block, Paragraph}};

#[test]
fn renders_title_and_body() {
    let mut terminal = Terminal::new(TestBackend::new(20, 3)).unwrap();
    terminal
        .draw(|f| f.render_widget(Paragraph::new("hello").block(Block::bordered().title("kwx")), f.area()))
        .unwrap();
    insta::assert_snapshot!(terminal.backend(), @r#"
    "┌kwx───────────────┐"
    "│hello             │"
    "└──────────────────┘"
    "#);
}
```

Rules:

1. **Render from state.** Structure the app so `render(&State, &mut Frame)` is a pure function of state; then each test builds a state and snapshots the frame. Evidence: moderate (ratatui recipe).
2. **Test several terminal sizes:** the smallest supported (for example 40x10), a typical 80x24, and a wide one. Layout bugs (overlap, truncated labels, panics on tiny sizes) appear at the edges. Evidence: moderate.
3. **Test unicode width:** CJK, emoji and combining characters take different cell widths. Snapshot a row with them. Evidence: moderate.
4. **Snapshots do not include colour** (ratatui issue 1402). Assert important styles directly on cells: `terminal.backend().buffer()[(x, y)].fg == Color::Red`. Evidence: moderate (ratatui docs).
5. **Snapshot states, not frames of an animation.** Make time an input of the state. Evidence: opinion.

## 7. TUIs: key handling as events

Test key handling by sending events to the app's update function, not by typing into a terminal. Never inject real keystrokes into the user's terminal or desktop.

```rust
use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};

fn key(code: KeyCode) -> KeyEvent { KeyEvent::new(code, KeyModifiers::NONE) }

#[test]
fn j_moves_selection_down_and_q_quits() {
    let mut app = App::with_items(["a", "b", "c"]);
    app.handle_key(key(KeyCode::Char('j')));
    app.handle_key(key(KeyCode::Char('j')));
    assert_eq!(app.selected(), 2);
    app.handle_key(key(KeyCode::Char('j')));          // at the end: stays, does not wrap or panic
    assert_eq!(app.selected(), 2);
    app.handle_key(key(KeyCode::Char('q')));
    assert!(app.should_quit());
}
```

Cases: every key binding; modifiers (Ctrl, Alt, Shift); keys in each mode (normal, insert, dialog open); keys on empty lists; resize events; paste events; key release events on terminals that send them (crossterm on Windows sends press and release; filter `kind == KeyEventKind::Press`). Combine with section 6: apply keys, then snapshot the frame. A property test can send random key sequences and assert the app never panics and invariants hold (selection in range).

## 8. TUIs: PTY end to end tests

Render and key tests do not cover the event loop, terminal setup and teardown (raw mode, alternate screen, restoring the terminal after a panic) or exit codes. For a few key flows, run the real binary in a pseudo terminal.

**termlens** (0.11; named in the ratatui testing recipe) spawns the binary in a PTY, sends keys and waits for screen content:

```rust
use std::time::Duration;
use termlens::{Key, Terminal};

#[test]
fn counts_up_and_quits() -> termlens::Result<()> {
    let mut t = Terminal::builder()
        .size(80, 24)
        .env_clear()
        .timeout(Duration::from_secs(5))
        .spawn(env!("CARGO_BIN_EXE_counter-app"))?;
    t.wait_until(|s| s.contains("Counter: 0"))?;
    t.send(Key::Char('j'))?;
    t.send(Key::Char('j'))?;
    t.wait_until(|s| s.contains("Counter: 2"))?;
    t.wait_idle(Duration::from_millis(50))?;   // PTY output is async: let the frame finish
    insta::assert_snapshot!(t.screen());
    t.send(Key::Char('q'))?;
    assert!(t.wait_exit()?.success());
    Ok(())
}
```

(From the ratatui recipe; not run here.)

**expectrl** (0.9) and **rexpect** (0.7) are expect style alternatives for line oriented interactive programs (prompts, REPLs): `spawn`, `expect(Regex(...))`, `send_line`, `expect(Eof)`. They read the raw byte stream, not a rendered screen, so they suit prompts better than full screen TUIs.

Rules:

1. **Wait for visible content, never sleep.** The ratatui recipe says waiting for content keeps the interaction deterministic. Evidence: moderate.
2. **Keep PTY tests few:** start up, the main flow, quit, and "terminal restored after a panic" (raw mode off, cursor visible). Evidence: moderate.
3. **The PTY is the test's own, not the user's terminal.** These tests are safe under a "never type for the user" rule because the input goes to a child process in a private PTY. Evidence: opinion.

## 9. Recorded demos with vhs

vhs (0.12) records a terminal session from a `.tape` script into a GIF, video or text. It is mainly for demos, but the `.txt` and `.ascii` outputs can be committed as golden files and compared in CI (vhs README).

```text
# demo.tape
Require kwx
Output demo.gif
Output demo.txt
Set FontSize 18
Set Width 1000
Set Height 500
Type "kwx --help"
Enter
Wait /Usage/
Sleep 1s
```

`Wait /regex/` waits for screen content (default timeout 15 s), which beats fixed `Sleep`. `Require` fails early when a program is missing. In CI, `charmbracelet/vhs-action` keeps demo GIFs up to date. vhs drives its own headless terminal, not the user's. Evidence: moderate.

Use vhs golden files for a smoke check of the real binary; use TestBackend snapshots for detailed layout tests.

## 10. Checks

| Check | Pass condition |
|---|---|
| Clean environment | every end to end test uses a temp `HOME` and working directory |
| Arguments | help, version, unknown flag (exit 2), missing value, conflicting flags tested |
| Streams | data on stdout only; errors on stderr; no colour when piped or `NO_COLOR` set |
| Exit codes | each documented code has a test |
| Broken pipe | piping into `head` does not panic |
| Signals | SIGINT cleanup and exit status tested for long running commands |
| Files | atomic writes; no clobber without `--force`; odd paths covered |
| Golden files | redacted; README examples run as tests; diffs read before accepting |
| Shell scripts | bats tests with `--separate-stderr` where streams matter; shellcheck clean |
| TUI render | state based render tests at small, typical and wide sizes; unicode width row; key styles asserted on cells |
| TUI keys | every binding tested as events per mode; random key sequence property test |
| TUI end to end | few PTY tests: start, main flow, quit, terminal restored after panic |
| No real input | no keystrokes sent to the user's terminal or desktop |
