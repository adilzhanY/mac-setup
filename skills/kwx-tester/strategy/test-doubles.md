# Test doubles: fakes, stubs, mocks and spies

A test double stands in for a real collaborator in a test. Used well, it makes a test fast and deterministic. Used badly, it makes the test check its own setup, break on every refactor, and pass while production fails. This file gives the vocabulary, the two schools and where the evidence points, a decision procedure for each dependency, what never to double, and how to keep a double honest with a contract test.

kwx-developer already has the default table of what to mock per dependency (`~/.claude/skills/kwx-developer/reliability/testing-strategy.md` section 6). Use that table for the quick answer; use this file to reason about a case the table does not cover, to review a test suite that over mocks, and to write contract tests for fakes.

## Contents

1. Vocabulary
2. The two schools and where the evidence points
3. Commands, queries and what to assert
4. Decision procedure for one dependency
5. What never to double
6. Fakes: when and how
7. Contract tests: keeping a double honest
8. Per stack notes
9. Smells in a suite that over mocks
10. Checks

## 1. Vocabulary

Gerard Meszaros named the kinds of doubles in xUnit Test Patterns (2007); Fowler's "Mocks Aren't Stubs" made the names common.

| Double | What it does | Example |
|---|---|---|
| Dummy | Passed to fill a parameter, never used | A logger nobody reads in this test |
| Stub | Returns canned answers to calls made during the test | `getExchangeRate()` always returns 1.1 |
| Spy | A stub that also records how it was called | An email sender that stores sent messages in an array |
| Mock | Pre programmed with expectations about the calls it should receive, fails if they do not happen | `expect(payment.charge).toHaveBeenCalledWith(...)` |
| Fake | A working implementation with a shortcut that makes it unfit for production | An in memory repository; a fake clock you can advance |

Library names blur this: `vi.fn()` and `jest.fn()` create objects that can act as stub, spy or mock depending on how the test uses them. Classify by use: do you feed answers in (stub), or check calls coming out (mock or spy)?

Verification styles (Fowler): **state verification** checks the result and the resulting state; **behaviour verification** checks which calls were made. Mocks always use behaviour verification.

## 2. The two schools and where the evidence points

| | Classical (Detroit, Chicago) | London (mockist) |
|---|---|---|
| Unit means | A unit of behaviour, can span several classes | One class |
| Doubles | Only when the real thing is awkward: shared, slow, out of process | For every collaborator with interesting behaviour |
| Verification | Mostly state | Mostly behaviour (interactions) |
| Strength | Tests survive refactoring; fail only when behaviour changes | Failures point at one class; drives interface design outside in |
| Weakness | A bug can turn many tests red at once | Tests coupled to implementation; break on refactor; can pass with wrong expectations |

Where the sources land:

- **Fowler** calls himself "a convinced classicist", mainly because mockist tests couple to the implementation.
- **Software Engineering at Google** (ch. 13): prefer the real implementation, then a fake, then stubbing or interaction testing. "Overuse of stubbing leads to tests that are unclear and brittle." Interaction testing is for cases where no real or fake implementation is feasible, or where the number or order of calls is the behaviour (for example, a cache must cut database calls).
- **Khorikov** (Unit Testing Principles, Practices, and Patterns, 2020) says "both schools are wrong in their treatment of mocks": the London school mocks internal collaborators, the classical school mocks its own database. His rule: mock only **unmanaged out of process dependencies**, the ones other systems can observe (SMTP, a message bus, a payment provider). Use real instances of **managed** dependencies (your own database that only your app talks to), because talking to them is an implementation detail.
- **Freeman and Pryce** (GOOS; "Mock Roles, not Objects", OOPSLA 2004) are the London school's authors, and their own guidelines limit mocks: "only mock types you own", write thin wrappers around third party code, do not mock value objects, "specify as little as possible in a test", do not add behaviour to mocks, and treat many mocks in one test as a design smell.

The common ground, which this skill follows: real collaborators inside your process; real managed dependencies (your database) in medium tests; doubles only at the edge of your system, behind an interface you own; assert interactions only for outgoing commands that other systems can see. Evidence: moderate (practitioner consensus across schools).

## 3. Commands, queries and what to assert

Split each call to a dependency into a query (reads, returns data, no side effect) or a command (changes something, the side effect is the point). This is Meyer's command query separation, applied to doubles by Khorikov.

| Call | Double | Assert on it? |
|---|---|---|
| Query (get rate, read user, fetch weather) | Stub | No. Asserting that a stub was called is an anti pattern: it tests how the code gets its data, not what it does with it |
| Command to your own managed dependency (insert row) | Do not double; use the real database | Assert the resulting state (the row) |
| Command to an unmanaged dependency (send email, charge card, push notification, publish event other systems read) | Mock or spy at your adapter | Yes: assert the call and the arguments that matter, and that it happened exactly as often as the spec says |

```ts
// Good: stub the query, assert the outcome and the one outgoing command.
const rates = { get: async () => 1.1 };          // stub, never asserted
const mailer = new RecordingMailer();             // spy at our own adapter
await checkout({ cart, rates, mailer, db });
expect(await db.orders.byUser(user.id)).toHaveLength(1);       // state
expect(mailer.sent).toEqual([expect.objectContaining({ to: user.email, template: "receipt" })]);
```

## 4. Decision procedure for one dependency

Ask in order and stop at the first yes:

1. **Is it your own code in the same process?** Use the real thing. If it is hard to construct, that is a design signal (too many dependencies), not a reason to mock.
2. **Is it a value or a pure function?** Real. Never double values.
3. **Is it nondeterministic: time, randomness, ids?** Inject it and use a fake (a clock you set and advance, a seeded random source). This is a double, and the right one.
4. **Is it a managed out of process dependency (your database, your own file storage, your local Supabase)?** Real, in a medium test, isolated per test.
5. **Is it unmanaged (third party API, email, SMS, payments, push, OS services you cannot run in tests)?** Wrap it in a small adapter you own. In tests of your logic, use a fake or spy of the adapter. Test the adapter itself against a network level double (MSW, wiremock) built from recorded real responses, and once in a while against the real sandbox.
6. **Is it a native module or OS API that cannot run in the test runtime** (a React Native native module under Jest, Android system services under JVM unit tests)? Double it at the thinnest boundary, and cover the real one in device or instrumented tests.

## 5. What never to double

| Never double | Why | Instead |
|---|---|---|
| The system under test, or part of it (partial mocks, `vi.spyOn(sut, "helper")`) | You test a different program | Test through the public API |
| Your own domain logic and helpers | Tests break on refactor and miss integration bugs | Real objects |
| Value objects, DTOs, plain data | Nothing to isolate | Construct them (builders in `test-data-and-fixtures.md`) |
| Your database or ORM in tests of data access | Constraints, transactions, RLS, triggers and SQL are where the bugs live | Real Postgres or local Supabase per test |
| Types you do not own (SDK classes, `fetch` internals, framework objects) | Your mock encodes your assumptions about their behaviour, which may be wrong; upgrades go unnoticed | Wrap in an adapter you own; mock the network, not the library |
| The thing whose behaviour the test is about | The test checks the mock | Use the real one, or test at a different boundary |
| Logging, metrics (with assertions) | Implementation detail, unless a log line is a product requirement | Let them run; assert only required audit events |

## 6. Fakes: when and how

A fake is the best double when the real thing cannot be used, because it behaves like the real thing across many tests, where a stub only answers one call (SWE at Google ch. 13).

- **Who writes it:** ideally whoever owns the real implementation, next to it, so it changes with it. For a third party service, you own the fake of your adapter.
- **Fidelity:** match the contract the tests rely on (results, errors, ordering, uniqueness), not latency or storage format.
- **Errors too:** a fake that never fails trains the code to assume success. Give it switches for the failures the real thing has: `fakePayments.failNext("card_declined")`, timeouts, rate limits, duplicate keys.
- **A fake has its own tests,** the same contract suite the real implementation passes (section 7). Without them it drifts silently.
- **Keep it boring.** No logic beyond the contract. Freeman and Pryce: a mock or fake that needs real behaviour is a sign of misplaced responsibilities.

```ts
// A fake of our own adapter around the payment provider.
export class FakePayments implements Payments {
  charges: Charge[] = [];
  private nextError: PaymentError | null = null;
  failNext(code: PaymentError["code"]) { this.nextError = { code }; }
  async charge(input: ChargeInput): Promise<Result<Charge, PaymentError>> {
    if (this.nextError) { const e = this.nextError; this.nextError = null; return err(e); }
    if (this.charges.some((c) => c.idempotencyKey === input.idempotencyKey)) {
      return ok(this.charges.find((c) => c.idempotencyKey === input.idempotencyKey)!); // same as provider
    }
    const charge = { id: `ch_${this.charges.length + 1}`, ...input };
    this.charges.push(charge);
    return ok(charge);
  }
}
```

## 7. Contract tests: keeping a double honest

A double is a claim about how the real thing behaves. A contract test checks the claim. Without it, the double and the real thing drift, and tests stay green while production breaks. Fowler ("Eradicating Non-Determinism in Tests") suggests running contract tests against remote services periodically rather than on every push.

### One suite, two implementations

Write the behaviour the code relies on as a test suite parameterized by implementation. Run it against the fake on every push and against the real thing (local container, sandbox) nightly or before release.

```ts
// payments.contract.ts
export function paymentsContract(name: string, make: () => Promise<Payments>) {
  describe(`Payments contract: ${name}`, () => {
    it("returns the same charge for a repeated idempotency key", async () => {
      const p = await make();
      const a = await p.charge({ amount: 500, currency: "EUR", idempotencyKey: "k1", card: TEST_CARD_OK });
      const b = await p.charge({ amount: 500, currency: "EUR", idempotencyKey: "k1", card: TEST_CARD_OK });
      expect(unwrap(b).id).toBe(unwrap(a).id);
    });
    it("reports a declined card as card_declined", async () => {
      const p = await make();
      const r = await p.charge({ amount: 500, currency: "EUR", idempotencyKey: "k2", card: TEST_CARD_DECLINED });
      expect(r).toEqual(err({ code: "card_declined" }));
    });
  });
}

// payments.fake.test.ts (every push)
paymentsContract("fake", async () => new FakePayments({ declineCards: [TEST_CARD_DECLINED] }));

// payments.real.test.ts (nightly, needs sandbox keys)
describe.runIf(process.env.PAYMENTS_SANDBOX_KEY)("sandbox", () => {
  paymentsContract("sandbox", async () => new ProviderPayments(process.env.PAYMENTS_SANDBOX_KEY!));
});
```

In Rust, the same idea is a generic function `fn contract<S: Store>(make: impl Fn() -> S)` called from two `#[test]` functions, the real one behind `#[ignore = "needs sandbox"]` or an env check.

### Schema bound stubs

For HTTP doubles (MSW handlers, wiremock stubs, recorded fixtures), validate every stubbed response against the same schema the real API publishes (OpenAPI, zod, JSON Schema). A stub that returns a field the real API does not have fails at test time, not in production.

```ts
const handler = http.get("/api/forecast", () => HttpResponse.json(ForecastSchema.parse(recordedForecast)));
```

Re-record fixtures from the real API (sandbox) when the provider announces a change, and diff them.

### Consumer driven contracts

When the consumer and provider are deployed separately (a mobile app and its API), a consumer driven contract tool (Pact) records what the consumer expects and makes the provider verify it in CI. In a single repo with shared types it adds little; a shared schema is enough (kwx-developer section 10).

## 8. Per stack notes

- **TypeScript (Vitest, Jest):** `vi.fn()` for spies at your adapters; `vi.spyOn` only on boundaries you own; MSW for HTTP with `onUnhandledRequest: "error"`; `vi.useFakeTimers()` plus `vi.setSystemTime()` for time. Set `restoreMocks: true`. Avoid `vi.mock("./myModule")` of your own relative modules.
- **React Native:** native modules (`expo-haptics`, `expo-notifications`, secure storage) do not run under Jest, so mock them at the module boundary (often the library ships a mock, for example `jest-expo` presets). Keep app logic out of those mocks, and cover the real modules in device flows.
- **Rust:** do not create a trait only so a mock can implement it (kwx-developer Rust testing). Use traits at true boundaries (a `Clock`, a `Mailer`, an HTTP client), with hand written fakes; `wiremock` for HTTP; `mockall` only for a boundary trait whose fake would be larger than the test.
- **Kotlin / Android:** prefer hand written fakes of repositories and data sources over MockK mocks of your own classes; use MockK `verify` only for outgoing commands at the edge. Room has an in memory database for medium tests of DAOs, which is the real engine, not a fake.
- **Supabase:** never mock `supabase-js` in backend or RLS tests; run the local stack (`supabase start`). In frontend component tests, mock at HTTP with MSW, and validate stubbed rows against the generated database types.
- **QML / Quickshell:** move logic into plain JS functions or C++ classes that take their services as parameters; give services fake implementations with the same properties and signals for headless Qt Quick tests. Visual behaviour goes to the user's hand checks.

## 9. Smells in a suite that over mocks

| Smell | What it means | Fix |
|---|---|---|
| Test asserts a stub was called (`expect(repo.get).toHaveBeenCalled()`) | Checks how data is fetched, not the result | Remove the assertion; assert the output |
| More lines of mock setup than of test | The unit has too many collaborators, or the test is at the wrong level | Test at a higher level with real collaborators; split the unit |
| Mock returns a mock that returns a mock | Testing a chain of calls (Law of Demeter breach) | Only mock immediate neighbours (Freeman et al.); introduce a role |
| Refactor without behaviour change turns tests red | Tests coupled to implementation | Assert state and outgoing commands only |
| Everything green, production broken on an SDK upgrade | Mocked a type you do not own | Adapter plus contract test against the real SDK |
| `vi.mock` of the module under test's siblings | Partial isolation of your own code | Use the real modules |
| Mock verifies call order of unrelated calls | Overspecified | Assert only what the spec requires |
| Fake has no tests | Silent drift | Contract suite run against fake and real |

When auditing, count interaction assertions per test file (`rg -c "toHaveBeenCalled|verify\(" src tests`) and read the files at the top of the list first.

## 10. Checks

| Check | Pass condition |
|---|---|
| Only boundaries doubled | Doubles sit at adapters to unmanaged dependencies, time, randomness, or native modules |
| No assertions on stubs | Queries are stubbed and never verified |
| Commands verified | Outgoing commands to unmanaged systems are asserted with the arguments that matter |
| Managed dependencies real | Database, local Supabase and file system are real in medium tests |
| No types you do not own mocked | Third party SDKs sit behind an adapter you own |
| Fakes have failure modes | Each fake can simulate the real errors the code must handle |
| Contract tests | Each fake and recorded stub has a contract suite or schema check against the real thing, run on a schedule |
| Over mock audit | Files with the most interaction assertions reviewed; partial mocks of the SUT removed |
