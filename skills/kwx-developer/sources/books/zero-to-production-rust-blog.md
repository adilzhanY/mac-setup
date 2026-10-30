# Zero To Production In Rust (Luca Palmieri): free chapters on the author's blog

Legal free excerpts published by the author (the full book is paid, I did not read it):

- Chapter 4, "Are we observable yet? Telemetry": https://www.lpalmieri.com/posts/2020-09-27-zero-to-production-4-are-we-observable-yet/
- Chapter 6, "Reject invalid subscribers (domain modelling)": https://www.lpalmieri.com/posts/2020-12-11-zero-to-production-6-domain-modelling/
- "Error Handling In Rust: A Deep Dive": https://www.lpalmieri.com/posts/error-handling-rust/ (see also zero-to-production-error-handling.md written by another agent)

## Key lessons used in languages/rust/

- Parse, don't validate: newtype with a private field and a fallible `parse` that never panics; pass the newtype, not the raw string; read access through `AsRef<str>`, never `&mut`; test both sides of every boundary (256 vs 257 graphemes, empty, whitespace, each forbidden character). (api-design.md, testing.md)
- Errors: enum when the caller branches, opaque otherwise; HTTP mapping lives on the handler's error type, not on low level errors; `Display` brief, `Debug` with the source chain; `.context()` adds the operator facing intent; log once where handled. (errors.md)
- Telemetry: `tracing` not `log`; `#[tracing::instrument]` with `skip` for large or secret arguments; never hold `span.enter()` across `.await`, use `.instrument()`; secrets in `secrecy` types; request ids from middleware only; subscriber initialised once, test logs silent unless `TEST_LOG` is set; `RUST_LOG` with `EnvFilter`. (async-and-concurrency.md section 12, testing.md)
- Note: the book uses `once_cell::sync::Lazy`; modern code uses `std::sync::LazyLock` (stable since Rust 1.80).
