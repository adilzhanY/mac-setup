# Naming

Names are the most read part of an interface. A name is good when a reader who sees only the name, at the call site, forms the right picture of the thing, and when the same thing has the same name everywhere. Models already pick reasonable names in isolation; what they get wrong is consistency with the codebase's vocabulary, precision, and renaming when meaning changes.

## Contents

1. The rules
2. Vocabulary consistency (the part agents miss)
3. Names that signal a design problem
4. TypeScript conventions
5. Rust conventions
6. Files and folders
7. Checks

## 1. The rules

1. **Use the codebase's word for the concept.** Before naming, grep for the concept's existing name. If the code says `workspace`, do not introduce `project` for the same thing. One term per concept across code, UI copy, database columns, API fields and docs.
2. **Precise over generic.** Ousterhout's red flag "vague name": `data`, `info`, `item`, `result`, `value`, `obj`, `temp`, `handle`, `process`, `manager`, `stuff`. A name should rule out wrong interpretations: `count` of what? `cancelledOrderCount`.
3. **Carry the unit and the kind.** `timeoutMs`, `sizeBytes`, `priceCents`, `durationSecs`, `createdAt` (timestamp) vs `createdOn` (date). Units in names prevent the most common class of numeric bug. In Rust prefer a type (`Duration`, a `Cents(u64)` newtype) over a unit suffix.
4. **Length follows scope.** One letter is fine for a 3 line lambda or loop index; module level and exported names are full words. Google TS: short names only for variables in scope for 10 lines or less.
5. **Booleans read as predicates.** `isLoading`, `hasAccess`, `canEdit`, `shouldRetry`. Never negative (`isNotValid`, `disableX` toggles produce double negatives). Rust: `is_empty()`, `has_children()`.
6. **Functions are verbs, values are nouns.** `fetchInvoices()` returns invoices; `invoices` is the value. Do not name a function a noun (`userData()`), or a value a verb.
7. **No type encoding.** No Hungarian notation, no `I` prefix on interfaces unless the codebase does it, no `strName`, no `userArray` (use plural `users`), no `Impl` suffix unless there is a real interface and the codebase uses it.
8. **No implementation details in interface names.** `getUsersFromRedis()` leaks the storage; `getUsers()` hides it.
9. **Same verb, same meaning.** Pick one verb per kind of operation and keep it (section 2).
10. **Hard to name means hard to understand.** If you cannot find a short precise name, the thing probably does two jobs or has no clear job (Ousterhout: "hard to pick name" is a design red flag). Fix the design, not the name.
11. **Rename when meaning shifts.** Pragmatic Programmer tip 74: "Name to express your intent to readers, and rename as soon as that intent shifts." A function called `validateEmail` that now also normalises and saves is lying. Rename it in a structure-only commit.
12. **Consistent word order.** Rust API Guidelines C-WORD-ORDER: the standard library uses verb-object-error (`ParseIntError`), so a new error is `ParseAddrError`, not `AddrParseError`. In TS pick `UserCreateInput` or `CreateUserInput` and keep it.

## 2. Vocabulary consistency

Agents introduce synonyms because each file is written in isolation. In audits, look for these synonym sets and report any concept with more than one name.

| Concept | Synonym set to grep |
|---|---|
| Getting data | `get`, `fetch`, `load`, `retrieve`, `read`, `find`, `query`, `lookup` |
| Creating | `create`, `add`, `new`, `make`, `build`, `insert`, `register` |
| Removing | `delete`, `remove`, `destroy`, `drop`, `clear`, `purge` |
| Changing | `update`, `edit`, `modify`, `set`, `patch`, `change`, `save` |
| Checking | `validate`, `check`, `verify`, `ensure`, `assert`, `is` |
| Converting | `to`, `convert`, `transform`, `map`, `serialize`, `format`, `parse` |
| Domain nouns | `user`/`account`/`member`/`profile`; `org`/`team`/`workspace`/`company`; `item`/`product`/`sku`; `order`/`purchase`/`checkout` |

A useful default vocabulary (adopt it only where the codebase has none):

- `get` is cheap and local (memory, a field); `fetch` goes over the network; `load` reads from disk or storage; `find` may return nothing (`T | undefined`, `Option<T>`); `list` returns many.
- `create` makes a new persisted thing; `build`/`make` construct an in-memory value.
- `parse` turns text into a typed value and can fail; `format` turns a value into display text; `serialize` turns a value into a wire format.
- `validate` returns errors without throwing; `assert`/`ensure` throws or panics.

Detect:

```
# How many verbs does this codebase use for network reads?
rg -o "\b(get|fetch|load|retrieve)[A-Z]\w+\(" src --no-filename | sed 's/[A-Z].*//' | sort | uniq -c
# Synonyms for one domain noun
rg -o -i "\b(workspace|project|space|org)s?\b" src --no-filename | tr A-Z a-z | sort | uniq -c
```

When the domain has more than a handful of nouns, keep a glossary (Pragmatic Programmer tip 80, "Use a Project Glossary") in ARCHITECTURE.md or `docs/glossary.md`, and use the glossary word in code, UI and database alike.

## 3. Names that signal a design problem

| Name | Usually means | Do |
|---|---|---|
| `Manager`, `Handler`, `Processor`, `Helper`, `Util`, `Service` with no domain word | A class with no single responsibility, or a bag of functions | Name the responsibility (`InvoiceNumbering`, `RetryPolicy`) or split |
| `doX`, `handleX`, `processX` for non-event code | The function's purpose is unclear | Name the outcome: `chargeCard`, `applyDiscount` |
| `X2`, `XNew`, `XV2`, `XOld`, `XFixed` | A parallel change was never contracted | Finish the migration; delete the old one (`evolving-a-codebase.md`) |
| `and` in a name (`validateAndSave`) | Two jobs in one function | Split, or name the higher level outcome |
| Long name with many qualifiers (`getActiveNonDeletedUsersForCurrentOrgSortedByName`) | The function is too specific, or parameters are hiding in the name | Generalise the interface (`listUsers({ status, sort })`) or rely on the module name for context |
| Name repeats the module (`user::UserService::get_user_by_user_id`) | Stutter; the context is already given | `users::get(id)`; clippy `module_name_repetitions` (pedantic) |
| Boolean parameter `doX(true)` | Flag argument selecting behaviour | Two functions or an options object with named field (Fowler: Remove Flag Argument) |

## 4. TypeScript conventions

From Google's TypeScript style guide, adapted. Codebase convention overrides.

- `UpperCamelCase` for classes, interfaces, types, enums, React components and type parameters with words; `lowerCamelCase` for variables, functions, methods, properties, parameters; `CONSTANT_CASE` for module level constants that are truly immutable configuration values (not every `const`).
- Acronyms as words: `loadHttpUrl`, `userId`, `apiKey`, not `loadHTTPURL`, `userID`. Exception: platform names like `XMLHttpRequest`.
- No `_` prefix for private members (use `private` or `#`), no `opt_` prefix, no `I` prefix for interfaces unless the codebase already uses it everywhere.
- React: components `PascalCase`; hooks `useThing`; event props `onThing`; handlers inside components `handleThing`. Boolean props `isOpen`, not `open` if the codebase uses `is`.
- Enforce: `@typescript-eslint/naming-convention` with the codebase's rules.

## 5. Rust conventions

From the Rust API Guidelines (naming chapter). These are ecosystem wide, so follow them even when the codebase drifts.

- Types, traits, enum variants: `UpperCamelCase`; acronyms as one word (`Uuid`, `HttpClient`). Functions, methods, modules, locals: `snake_case`. Constants and statics: `SCREAMING_SNAKE_CASE`. Lifetimes short (`'a`, `'de`).
- Constructors: `new`, `with_capacity`/`with_x` for variants, `from_x` for conversion constructors, and `From`/`TryFrom` impls where natural.
- Conversions by cost: `as_x` is free and borrows (`as_bytes`), `to_x` is expensive or produces an owned copy (`to_string`, `to_lowercase`), `into_x` consumes `self` (`into_inner`). `mut` goes where it appears in the return type: `as_mut_slice`, not `as_slice_mut`.
- Getters: `name()` and `name_mut()`, no `get_` prefix. `get` alone only when there is one obvious thing to get (`Cell::get`), or for fallible lookups by key (`map.get(k)`).
- Iterators: `iter`, `iter_mut`, `into_iter`; iterator types named after the method (`Keys`, `IntoIter`).
- Cargo features: no `use-` or `with-` prefixes; `std` for std support; features are additive, so no `no-x` features.
- Errors: verb-object-error order (`ParseConfigError`); crate level `Error` and `Result` aliases are common and fine.
- No `-rs` or `-rust` in crate names.

## 6. Files and folders

- One case per file kind across the repo. Common TS defaults: components `PascalCase.tsx`, everything else `camelCase.ts` or `kebab-case.ts`; pick what the repo uses. Google's TS guide uses `snake_case` file names; many web codebases use kebab. Consistency is what matters.
- Rust files and modules are `snake_case`, always.
- File named after its main export: `InvoiceTable.tsx` exports `InvoiceTable`; `currency.ts` holds currency functions.
- Test files mirror the source name: `currency.test.ts`.
- Folder names: plural for collections of similar things (`components`, `hooks`), singular for a domain (`billing`, `auth`). Keep the choice consistent.
- Enforce with `unicorn/filename-case` (eslint) or Biome `useFilenamingConvention`.

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One term per concept | No domain concept has two names in code | synonym greps in section 2; compare with the glossary |
| One verb per operation kind | Network reads use one verb, disk reads one verb, etc. | verb count grep in section 2 |
| No vague names in new exports | No exported `data`, `info`, `manager`, `helper`, `utils`, `handleX` outside event handlers | `rg -n "export (const\|function\|class) (data\|info\|item\|result\|\w*(Manager\|Helper\|Util))\b" src` |
| Units present | Numeric durations, sizes and money carry a unit or a type | `rg -n "(timeout\|delay\|interval\|duration\|size\|price\|amount)\s*[:=]" src` and read |
| No stale names | No `V2`, `New`, `Old`, `2` suffixed parallel names left after a migration | `rg -n "(function\|const\|class\|fn\|struct\|enum) \w+(V2\|New\|Old\|Legacy)\b" src` plus `rg --files \| rg "(V2\|New\|Old\|Legacy\|Copy)\.\w+$"` (declarations only, so `isNew` fields do not match) |
| Boolean params | No exported function takes a positional boolean that switches behaviour | `rg -n "\(\w+: boolean[,)]" src`; clippy `fn_params_excessive_bools` |
| Rust guidelines | No `get_` getters, conversions named by cost | `rg -n "pub fn get_\w+\(&self\)" ` ; read conversions |
| File case consistent | One case per file kind | `scan_conventions.py` "file naming"; `unicorn/filename-case` |
