# Zero To Production In Rust (Luca Palmieri), chapter "Error Handling In Rust: A Deep Dive"

Legal free excerpt published by the author: https://www.lpalmieri.com/posts/error-handling-rust/

## What I read

The full chapter excerpt: purposes of errors, control flow vs reporting, internal vs edge, Debug vs Display, the Error trait and source chains, thiserror vs anyhow, who should log errors.

## Key lessons used in reliability/error-handling-strategy.md

- Errors serve control flow (consumed by machines: enum variants, status codes) and reporting (consumed by humans: operators need full context, users need minimal safe information).
- Debug is the developer facing full representation; Display is the brief description. Implement `source()` so the cause chain is visible.
- "anyhow for applications, thiserror for libraries" is the wrong framing. Use an enum when the caller will behave differently per failure mode; use an opaque error when the caller only reports.
- Log errors once, when they are handled, not at every layer that propagates them.
