# Serde conventions

How to put `Serialize`/`Deserialize` on types without leaking internals, losing validation or producing a wire format you cannot evolve. Sources: serde.rs (container, field and enum representation docs), API Guidelines C-SERDE.

## Contents

1. Where serde derives belong
2. Naming and casing
3. Missing, unknown and optional fields
4. Enums: pick the representation on purpose
5. Validation on deserialize
6. Config files
7. Untrusted input
8. Checks

## 1. Where serde derives belong

- **Libraries:** serde support is an optional feature named exactly `serde` (C-SERDE, C-FEATURE), never `serde_impls` or `with-serde`:

```toml
[dependencies]
serde = { version = "1", optional = true, features = ["derive"] }

[features]
serde = ["dep:serde"]
```

```rust
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Point { x: f64, y: f64 }
```

- **Applications:** keep wire types (request and response bodies, DB rows, config files) separate from domain types once the two differ. A domain type with invariants deserialized straight from JSON skips its constructor. Convert DTO -> domain with `TryFrom` at the boundary. For small apps where they are identical, one type is fine.
- Marker types and handles (`LittleEndian`, a connection, a mutex) do not implement serde.

## 2. Naming and casing

- Pick the external casing once per format and apply it at the container: `#[serde(rename_all = "camelCase")]` for JSON APIs consumed by JavaScript, `snake_case` for config files. Do not rename field by field to get a convention.
- Enum variants: `#[serde(rename_all = "snake_case")]` (or `kebab-case` for config) so `Status::InProgress` is `"in_progress"`, not `"InProgress"`.
- Renaming a Rust field must not change the wire format silently. Keep the old name with `#[serde(alias = "old_name")]` while clients migrate.

## 3. Missing, unknown and optional fields

| Situation | Attribute |
|---|---|
| field may be absent, `Default` is the right value | `#[serde(default)]` on the field (or on the container for all fields) |
| absent means a specific non default value | `#[serde(default = "default_port")]` with `fn default_port() -> u16 { 8080 }` |
| optional in output | `Option<T>` with `#[serde(skip_serializing_if = "Option::is_none")]` |
| never on the wire | `#[serde(skip)]` (needs `Default` for deserialize) |
| typos in config must fail loudly | `#[serde(deny_unknown_fields)]` on config structs |
| forward compatible API payloads | do not deny unknown fields on data you receive from a newer peer |
| newtype should serialize as its inner value | `#[serde(transparent)]` |

- `deny_unknown_fields` does not work together with `#[serde(flatten)]` on the same struct or the flattened one. Choose one.
- `flatten` is convenient but slower (it buffers) and interacts badly with `deny_unknown_fields` and with non self describing formats. Avoid it in hot paths.
- `skip_serializing_if` changes the shape of the output; with non self describing binary formats (bincode, postcard) the reader can no longer tell which fields are present. Use it only for self describing formats (JSON, TOML, YAML).

## 4. Enums: pick the representation on purpose

| Representation | Attribute | JSON | Use when |
|---|---|---|---|
| externally tagged (default) | none | `{"Click": {"x": 1}}` | Rust to Rust, or the consumer does not care |
| internally tagged | `#[serde(tag = "type")]` | `{"type": "click", "x": 1}` | JSON APIs, events, messages. The usual choice for public JSON. Struct, unit and newtype-of-struct variants only; tuple variants fail to compile |
| adjacently tagged | `#[serde(tag = "t", content = "c")]` | `{"t": "click", "c": {...}}` | variants that hold non struct data, still self describing |
| untagged | `#[serde(untagged)]` | `{"x": 1}` | accepting "a number or a string" style inputs only. Tries each variant in order, error messages are useless unless you add `#[serde(expecting = "...")]`, and it is slow |

- Never use `untagged` for a message type where variants overlap in shape: the first variant that happens to match wins silently.
- Add `#[serde(rename_all = "snake_case")]` with the tag so tag values are stable strings.
- For forward compatibility of received enums, add a catch all: `#[serde(other)] Unknown` (unit variant, internally or adjacently tagged enums).

## 5. Validation on deserialize

Deserialization must not bypass a constructor. Route it through the validating constructor:

```rust
#[derive(Debug, Clone, serde::Deserialize)]
#[serde(try_from = "String")]
pub struct Email(String);

impl TryFrom<String> for Email {
    type Error = ParseEmailError; // must implement Display
    fn try_from(s: String) -> Result<Self, Self::Error> { Email::parse(s) }
}
```

- `#[serde(try_from = "T")]` / `from` / `into` route through your conversions. The error type of `try_from` must implement `Display`.
- Do not hand write `impl Deserialize` unless the format really needs a visitor; `try_from` plus a derived DTO covers almost everything.
- `#[serde(with = "module")]` for formats of foreign types (timestamps as RFC 3339, durations as `"5s"` with `humantime-serde`), instead of storing strings in your types.

## 6. Config files

- Config struct: `#[serde(deny_unknown_fields)]`, defaults via `#[serde(default)]` on fields, secrets typed as `secrecy::SecretString` so `Debug` never prints them.
- Load once at startup into a typed struct, validate (ports in range, URLs parse), and fail with context naming the file and the key. Do not read `std::env::var` deep inside business code; pass the config down.
- Layering (file, then env overrides) with `figment` or `config` crates; keep the layering in one module.

## 7. Untrusted input

- Bound the size before deserializing: limit request body bytes at the HTTP layer, and for binary formats set a size limit in the decoder options. Serde will happily allocate a `Vec` with a length taken from the input.
- `serde_json::from_slice` on a capped buffer, not `from_reader` on an unbounded stream.
- Deep nesting can overflow the stack; serde_json has a recursion limit (128) on by default, do not disable it (`unbounded_depth`) for untrusted data.
- `#[serde(borrow)]` and `&'de str` fields give zero copy deserialization but tie the value to the input buffer; use it for parsing hot paths, not for values you store.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Library serde feature named `serde` | feature exists and is named exactly that | `rg -n '^serde\s*=' Cargo.toml` under `[features]`; `rg -n 'cfg_attr\(feature = "serde"' src` |
| Domain invariants not bypassed | every `Deserialize` type with a private field and a `parse`/`new` uses `try_from` or a DTO | `rg -n -B3 'pub struct \w+\(String\)' src` near `derive(.*Deserialize` and inspect |
| Config rejects typos | config structs have `deny_unknown_fields` | `rg -n 'deny_unknown_fields' src` |
| No overlapping untagged enums | each `#[serde(untagged)]` reviewed | `rg -n 'serde\(untagged' src` |
| No flatten with deny_unknown_fields | none on the same type | `rg -n -A5 'deny_unknown_fields' src \| rg flatten` |
| Secrets not Debug printed | secret fields use `SecretString` or a manual `Debug` | `rg -n '(password|token|secret|api_key)\s*:\s*String' src` |
| Body size bounded | HTTP body limit set | `rg -n 'DefaultBodyLimit\|body_limit\|RequestBodyLimit' src` for axum/tower apps |
