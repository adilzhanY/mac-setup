# Property based testing

A property based test states a rule that must hold for every input in a described set, and a library generates many inputs, checks the rule, and shrinks any failure to a small counterexample. It finds the cases nobody thought to write: the empty list, the equal timestamps, the sequence of taps nobody tried. This file covers how to find properties (the hard part), how to write generators that reach the bugs, shrinking and replay, and stateful model based testing for things like timers, carts and sync engines.

kwx-developer lists the classic property kinds and library basics (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 6, `~/.claude/skills/kwx-developer/languages/rust/testing.md` section 5). This file adds the evidence on which kinds work best, the generator craft, and stateful testing.

## Contents

1. When to use it
2. Libraries
3. Finding properties: Hughes' five kinds and what the data says
4. Finding properties: Wlaschin's patterns as prompts
5. Generators that reach the bugs
6. Shrinking, seeds and replay
7. Stateful and model based testing
8. Worked example: a sync merge that does not converge
9. Pitfalls
10. Running in CI
11. Checks

## 1. When to use it

Use a property test when you can state a rule over many inputs and the input space is too large to enumerate:

- Parsers, serializers, encoders, formatters (round trips, never crash).
- Money, units, dates and time zone math (relations, invariants).
- Merges, sync and conflict resolution (commutative, idempotent, associative).
- Sorting, filtering, dedup, pagination (invariants, metamorphic relations).
- Anything with state: timers, carts, editors, undo stacks, caches, connection pools (model based).
- Permission rules (no user ever reads a row they do not own, for any generated set of users and rows).

Keep example tests too: they document the spec cases and the decision table rules (`test-design-techniques.md`). Properties cover the space between them. If the domain is small (all `u8`, all 3 letter strings, all 4 plans x 3 discounts), loop over it exhaustively instead.

David MacIver (Hypothesis author) defines property based testing as building tests such that, when they are fuzzed, failures reveal problems with the system that direct fuzzing could not. The human work is choosing the property; the library does the fuzzing.

## 2. Libraries

| Language | Library | Stateful support | Version checked |
|---|---|---|---|
| TypeScript / JS | fast-check | `fc.commands` + `fc.modelRun`, `asyncModelRun`, `scheduledModelRun`; `fc.scheduler()` for async races | 4.10.2 (verified) |
| Python | Hypothesis | `RuleBasedStateMachine` | 6.170.14 (verified) |
| Rust | proptest | `proptest-state-machine` crate | proptest-state-machine 0.9.0 (docs.rs) |
| Kotlin | Kotest property testing, or jqwik (JUnit 5) | jqwik `ActionChain` | docs only |

## 3. Finding properties: Hughes' five kinds and what the data says

John Hughes ("How to Specify It! A Guide to Writing Properties of Pure Functions", TFP 2019, LNCS 12053) wrote five kinds of properties for a binary search tree, planted eight bugs, and measured which properties found which bugs and how fast.

| Kind | Idea | Example for a workout log store |
|---|---|---|
| Invariant (validity) | Every operation keeps the data valid; generators and shrinkers produce valid data | After any insert or delete, entries are sorted by start time and ids are unique |
| Postcondition | The result of one call relates to its arguments | After `add(w)`, `get(w.id)` returns `w` |
| Metamorphic | Two related calls give related results | `add(a)` then `add(b)` gives the same log as `add(b)` then `add(a)` when ids differ |
| Inductive | Relate a call to calls on smaller inputs; together they specify the function completely | `total(log + w) == total(log) + w.seconds` and `total([]) == 0` |
| Model based | Map the real result to a simple model and compare with the model operation | The store, read as a sorted list, equals `sortBy(model ++ [w])` |

The measurements:

- Validity properties missed five of the eight bugs. Necessary, never enough.
- Every bug was found by at least one postcondition, one metamorphic property and one model based property.
- Model based properties found bugs fastest: on average 5.8 tests to fail, against 77 for postconditions and 56 for metamorphic properties. For one union bug, the postcondition needed about 50 tests and the logically equivalent model based property about 8, because the model check compares the whole result while the postcondition checks one key.
- Metamorphic properties are "less effective individually, but powerful in combination". Weak versions with preconditions that exclude tricky cases missed bugs.

Hughes' advice, which this skill follows: when time is short, write model based properties plus validity properties (so invalid test data does not cause confusing failures). When a model is expensive or would mirror the implementation closely enough to share its bugs, write several metamorphic properties instead. Evidence: moderate (one careful study on one data structure, from the author of QuickCheck).

## 4. Finding properties: Wlaschin's patterns as prompts

Scott Wlaschin ("Choosing properties for property based testing") gives names that work as a checklist. Go through them for each function:

| Pattern | Ask | Example |
|---|---|---|
| Different paths, same destination | Can two orders of operations give the same result? | Apply discount then tax equals tax then discount (if the spec says so) |
| There and back again | Is there an inverse? | `parse(format(x)) == x`; export then import |
| Some things never change | What is preserved? | Number of sets in a workout after reordering |
| The more things change, the more they stay the same | Is it idempotent? | `normalize(normalize(s)) == normalize(s)`; replaying a sync batch |
| Solve a smaller problem first | Does it hold for parts? | Total of a log equals the sum of totals of its halves |
| Hard to prove, easy to verify | Is checking easier than computing? | A route is valid if consecutive points are connected; a sort output is ordered and a permutation |
| The test oracle | Is there a slower, obvious version? | Optimized search vs linear scan |

Also try: "never crashes on any input" for anything parsing external data, and "no information leak" for permission code (no generated user ever sees another user's rows).

## 5. Generators that reach the bugs

A property is only as good as its inputs. Most weak property tests fail here, not in the property.

- **Generate domain values, not raw types.** Build a `workout` arbitrary from valid parts (positive seconds, real dates, titles with realistic Unicode) instead of filtering random objects. Filtering throws most inputs away and libraries complain or slow down.
- **Make collisions likely.** Hughes measured that with independent random keys, the looked up key was absent from the tree in about 80% of tests, so most tests checked the trivial case. Drawing keys from a smaller range brought it to about 55% present. Use small ranges for ids, timestamps and names when equality matters: `fc.integer({ min: 0, max: 5 })` for timestamps finds equal timestamp bugs; a full 64 bit range never does.
- **Measure the distribution.** Before trusting a property, look at what it generates. Verified with fast-check 4.10.2:

```ts
fc.statistics(
  fc.tuple(fc.integer({ min: 0, max: 100 }), fc.array(fc.integer({ min: 0, max: 100 }))),
  ([k, xs]) => (xs.includes(k) ? "present" : "absent"),
  { numRuns: 1000 },
);
// absent...94.20%  present...5.80%   -> the "found" branch is barely tested; shrink the range
```

In Hypothesis, call `event("present")` inside the test and run `pytest --hypothesis-show-statistics`.

- **Test your generators.** Hughes recommends a property that every generated value is valid, and the same for shrunk values, because a generator or shrinker that produces invalid data makes unrelated properties fail with confusing counterexamples.
- **Bias toward edges.** The libraries already favour small and boundary values (0, empty, max). Add your domain's edges explicitly with `fc.oneof` or `st.one_of`: DST days, 23:59:59, the page size, Unicode look alikes.

## 6. Shrinking, seeds and replay

When a property fails, the library shrinks the input to a smaller one that still fails. Hypothesis, fast-check and proptest shrink "integrated" with generation, so shrunk values still respect the generator's rules (a shrunk workout is still a valid workout). Hughes notes a custom shrinker can break invariants, which is another reason to test validity of shrunk values.

Replay a failure exactly:

- **fast-check:** the report prints `seed`, `path` and, for commands, a `replayPath`. Re-run with `fc.assert(prop, { seed, path, endOnFailure: true })`. Pin a global seed in CI if runs must be reproducible: `fc.configureGlobal({ seed: Number(process.env.FC_SEED ?? Date.now()) })` and print it.
- **Hypothesis:** failing examples are saved in `.hypothesis/` and tried first next run; pin one with `@example(...)`.
- **proptest:** failures go to `proptest-regressions/`; commit the folder.

Always copy an important shrunk counterexample into a plain example test with a name that says what it shows. The property may later change; the regression must stay.

## 7. Stateful and model based testing

For code with state, the input is a sequence of operations. The library generates sequences, runs them against the real system and a simple model, checks the results after every step, and shrinks a failing sequence to the shortest one. Hughes and Quviq use this heavily for industrial systems.

The recipe:

1. Write the model: the simplest thing that behaves correctly (a plain object, a list, a map).
2. Write one command per operation: a precondition (when it is allowed), the call on the real system, the same change on the model, and the assertions comparing them.
3. Check invariants after every command.
4. Let the library generate and shrink sequences.

### fast-check: the workout timer

Verified with fast-check 4.10.2 and Vitest 5.0.5 (the run used plain JavaScript; types added here for reading). The model is the state table from `test-design-techniques.md` section 8.

```ts
class Cmd implements fc.Command<Model, Timer> {
  constructor(readonly name: "start" | "pause" | "resume" | "tick" | "reset") {}
  check() { return true; }        // also try invalid events: they must be rejected
  run(m: Model, r: Timer) {
    const ok = r[this.name]();
    const next = { start: { idle: "running" }, pause: { running: "paused" }, resume: { paused: "running" } }[this.name];
    if (this.name === "reset") { m.state = "idle"; m.left = m.total; }
    else if (this.name === "tick") {
      expect(ok).toBe(m.state === "running");
      if (ok && --m.left <= 0) { m.left = 0; m.state = "finished"; }
    } else {
      expect(ok).toBe(next?.[m.state] !== undefined);
      if (ok) m.state = next[m.state];
    }
    expect(r.state).toBe(m.state);   // compare after every step
    expect(r.left).toBe(m.left);
  }
  toString() { return this.name; }
}

it("timer matches its state model for any event sequence", () => {
  const cmds = (["start", "pause", "resume", "tick", "reset"] as const).map((n) => fc.constant(new Cmd(n)));
  fc.assert(fc.property(fc.integer({ min: 1, max: 5 }), fc.commands(cmds, { maxCommands: 40 }), (total, c) =>
    fc.modelRun(() => ({ model: { state: "idle", left: total, total }, real: createTimer(total) }), c)));
});
```

With a planted bug (resume allowed from idle) the run failed and shrank to `Counterexample: [1,resume /*replayPath="AI:B"*/]`: the shortest sequence that shows it.

### fast-check: async races

`fc.scheduler()` controls the order in which promises resolve, so a property can explore orderings that happen in the field once a week. Verified:

```ts
// The settings screen shows what the server echoed back after each save.
it("shows the last value typed whatever order the server answers in", async () => {
  await fc.assert(fc.asyncProperty(fc.scheduler(), async (s) => {
    const api = { save: s.scheduleFunction(async (v: string) => v) };
    const screen = makeScreen(api);
    screen.save("a"); screen.save("b");
    await s.waitAll();
    expect(screen.shown).toBe("b");
  }));
});
// Fails: [task 2] save("b") resolved, then [task 1] save("a") resolved -> screen shows "a"
```

The fix is in the code (ignore responses older than the latest request), and the property stays as the regression.

### Hypothesis

```python
class TimerMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.real, self.model = Timer(3), {"state": "idle", "left": 3}

    @rule()
    def start(self):
        ok = self.real.start()
        assert ok == (self.model["state"] == "idle")
        if ok: self.model["state"] = "running"

    # ... pause, resume, tick, reset as rules ...

    @invariant()
    def matches_model(self):
        assert (self.real.state, self.real.left) == (self.model["state"], self.model["left"])

TestTimer = TimerMachine.TestCase
```

`@precondition(lambda self: ...)` restricts when a rule runs; `Bundle` passes values produced by one rule (created ids) to others; `settings(max_examples=..., stateful_step_count=...)` controls size (Hypothesis docs).

### proptest

`proptest-state-machine` splits the same idea into a `ReferenceStateMachine` (the model: `init_state`, `transitions`, `apply`, `preconditions`) and a `StateMachineTest` (the real system: `init_test`, `apply`, `check_invariants`), run with `prop_state_machine! { #[test] fn timer(sequential 1..40 => TimerTest); }` (proptest book, State Machine testing chapter; not verified here).

## 8. Worked example: a sync merge that does not converge

An offline first app merges two versions of a record: the later `updated_at` wins, ties broken by device id. Three properties every merge in a sync system needs, so that devices converge whatever order they receive updates in:

```python
from hypothesis import given, strategies as st

def merge(a, b):  # version = (updated_at_ms, device_id, value)
    return max(a, b, key=lambda v: (v[0], v[1]))

# Small timestamp range on purpose: equal timestamps must be common.
versions = st.tuples(st.integers(0, 5), st.sampled_from(["phone", "laptop"]), st.text(max_size=3))

@given(versions, versions)
def test_merge_is_commutative(a, b):
    assert merge(a, b) == merge(b, a)

@given(versions)
def test_merge_is_idempotent(a):
    assert merge(a, a) == a

@given(versions, versions, versions)
def test_merge_is_associative(a, b, c):
    assert merge(merge(a, b), c) == merge(a, merge(b, c))
```

Verified with Hypothesis 6.170.14: commutativity failed with `a=(0, 'phone', ''), b=(0, 'phone', '0')`. Two edits from the same device in the same millisecond tie on the key, `max` returns its first argument, and so the phone and the laptop would each keep a different value forever. A decision table built from the spec (`test-design-techniques.md` section 11) shows the same gap as "equal timestamps: not specified"; the property turned it into a concrete failing case in one second. Comparing the whole tuple (`max(a, b)`) makes every tie resolve the same way on every device, and all three properties pass. A production fix would usually add a per edit counter or a hybrid logical clock; ask the owner.

## 9. Pitfalls

| Pitfall | Why it hurts | Fix |
|---|---|---|
| The property re-implements the code | Shares its bugs; Hughes warns against replicating the implementation in the test | Use relations, invariants or a much simpler model |
| Heavy `filter` / `assume` / preconditions | Most inputs discarded; tricky cases excluded (Hughes' "Weak" properties missed bugs) | Build valid values in the generator |
| Inputs too wide to collide | The interesting branch is almost never hit | Small ranges; measure with statistics |
| Only a validity property | Misses most bugs (5 of 8 in Hughes' study) | Add model, postcondition or metamorphic properties |
| Time or randomness inside the code under test | Non reproducible failures | Inject clock and random source |
| Failure "fixed" by narrowing the generator | Hides the bug | Fix the code, keep the generator, add the counterexample as an example test |
| Huge numRuns on every push | Slow suite | Default runs on push, many more nightly |
| Assertions with `==` on floats | Spurious failures | Integer minor units for money; tolerance stated by the spec |

## 10. Running in CI

- Default run counts on every push (fast-check 100, Hypothesis 100, proptest 256). A nightly job with 10 to 100 times more (`fc.configureGlobal({ numRuns })`, Hypothesis `settings` profiles, `PROPTEST_CASES`).
- Print the seed in CI logs; keep the Hypothesis database and `proptest-regressions/` in a place the next run sees (commit regressions; cache `.hypothesis/` or rely on `@example`).
- A property that fails only sometimes is not flaky by nature: it found a rare input. Treat it as a bug with a seed, not as a flaky test.

## 11. Checks

| Check | Pass condition |
|---|---|
| Right targets | Parsers, money, dates, merges, permissions and stateful components have properties |
| Strong kinds | Beyond validity: at least one model based, postcondition or metamorphic property per function under test |
| No re-implementation | Properties do not copy the code's logic |
| Generators | Domain values built, not filtered; collision prone ranges where equality matters; distribution measured once |
| Generator validity | A property checks generated (and shrunk) values are valid |
| Stateful code | Model based test with invariants checked after every step |
| Replay | Seeds printed; regression folders committed; key counterexamples copied into example tests |
| CI budget | Default runs on push, more nightly |
