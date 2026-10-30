# Async and concurrency

Tokio based async code, locks, channels, cancellation and threads. The bugs here compile, pass tests on a laptop, and fail under production load: a blocked executor, a lock held across `.await`, a message lost by `select!`, a task nobody waits for. Sources: Tokio tutorial and API docs, Alice Ryhl "Async: What is blocking?", Rain (sunshowers) "Cancelling async Rust" (RustConf 2025), Effective Rust item 17, the Rust blog on async fn in traits.

## Contents

1. When to use async at all
2. Never block the executor
3. Locks in async code
4. Cancellation: the rules
5. `select!` correctly
6. Spawning and structured tasks
7. Graceful shutdown
8. Channels and backpressure
9. Async traits
10. Threads, Send and Sync
11. Deadlock rules
12. Tracing in async code
13. Checks

## 1. When to use async at all

- Async pays off for many concurrent IO bound operations: servers, crawlers, clients holding many sockets. For a CLI that does a few requests or for CPU work, plain threads (or `rayon`) are simpler and just as fast.
- One runtime per process. Never create a `Runtime` inside async code or call `block_on` from inside a runtime (it panics or deadlocks). Libraries do not start runtimes; they expose `async fn` and let the binary choose.
- `#[tokio::main]` in the binary; `#[tokio::test]` in tests. Use `flavor = "current_thread"` for small CLIs and most tests.

## 2. Never block the executor

**Rule of thumb: no more than 10 to 100 microseconds of work between two `.await` points** (Alice Ryhl). A blocked worker thread stalls every task scheduled on it; with the default one worker per core, a few blocked tasks freeze the whole server, and only under load.

Blocking calls that look harmless:

| Blocking | Async replacement |
|---|---|
| `std::thread::sleep` | `tokio::time::sleep(..).await` |
| `std::fs::*`, `File::read` | `tokio::fs::*` (which is `spawn_blocking` inside) or one `spawn_blocking` around a batch of std fs calls |
| `std::net`, `reqwest::blocking`, sync DB drivers (`postgres`, `rusqlite`) | async clients (`reqwest`, `sqlx`, `tokio-postgres`), or `spawn_blocking` |
| `std::sync::mpsc::Receiver::recv` | `tokio::sync::mpsc` |
| hashing passwords, compression, image work, big JSON (de)serialization | `spawn_blocking` for occasional calls, `rayon` + `oneshot` for sustained CPU work |
| `std::process::Command::output` | `tokio::process::Command` |

Where to move blocking work:

| Option | Blocking IO | CPU bound | Runs forever |
|---|---|---|---|
| `tokio::task::spawn_blocking` | yes | occasional only (pool has hundreds of threads, more than cores) | no |
| `rayon::spawn` + `tokio::sync::oneshot` | no | yes | no |
| `std::thread::spawn` | yes | yes | yes (a loop reading a channel) |

```rust
// CPU heavy work from async code
let (tx, rx) = tokio::sync::oneshot::channel();
rayon::spawn(move || {
    let _ = tx.send(expensive_hash(&input)); // receiver may be gone; that is fine
});
let digest = rx.await?;
```

- `spawn_blocking` tasks cannot be cancelled once started; `abort()` does nothing and runtime shutdown waits for them.
- Ban `std::thread::sleep` in async crates with `disallowed-methods` in `clippy.toml` (tooling-and-lints.md).
- `clippy::unused_async` (pedantic) finds `async fn` with no `.await`; such a function does not need to be async, and if it does blocking work it is a trap.

## 3. Locks in async code

- **Default to `std::sync::Mutex` (or `parking_lot::Mutex`) for data, held briefly, inside non async methods.** It is cheaper than the tokio mutex and fine as long as contention is low (Tokio tutorial, "Shared state").
- **Never hold any guard across `.await`.** With a std guard the future becomes `!Send` (compile error on `tokio::spawn`); with some third party mutexes whose guards are `Send` it compiles and deadlocks. With `tokio::sync::Mutex` it compiles and serializes every task behind the slowest await.
- Make it structurally impossible: wrap the lock in a type whose methods are sync and never return the guard.

```rust
#[derive(Default)]
pub struct Counters {
    inner: std::sync::Mutex<HashMap<String, u64>>,
}

impl Counters {
    pub fn incr(&self, key: &str) {
        let mut map = self.inner.lock().expect("lock should not be poisoned");
        *map.entry(key.to_owned()).or_default() += 1;
    } // guard dropped here, no await possible inside

    pub fn get(&self, key: &str) -> u64 {
        self.inner.lock().expect("lock should not be poisoned").get(key).copied().unwrap_or(0)
    }
}
```

- `tokio::sync::Mutex` only when the critical section itself must await (for example, serializing writes to one connection). Even then, a task owning the resource and receiving messages (actor) is usually clearer.
- `match mutex.lock().unwrap().get(..) { .. }` keeps the lock for the whole `match` (the temporary lives to the end of the statement). Bind the value first. `clippy::significant_drop_in_scrutinee` and `significant_drop_tightening` (nursery) catch this.
- High contention on one map: shard it (N mutexes keyed by hash), use `dashmap`, or use an actor. Measure first.
- Read mostly config that changes rarely: `arc_swap::ArcSwap` or `tokio::sync::watch`, not a `RwLock` read on every request.

## 4. Cancellation: the rules

In async Rust any future can be cancelled at any `.await` by being dropped: by `select!` losing, by `timeout` firing, by `try_join!` failing fast, by a client disconnecting from an axum handler, by `JoinHandle::abort`. Code after that `.await` never runs.

- **Cancel safe** future: dropping it before completion and starting it again loses nothing (`mpsc::Receiver::recv`, `TcpListener::accept`, `AsyncReadExt::read`, `StreamExt::next`, `tokio::time::sleep`).
- **Not cancel safe** (Tokio docs list): `read_exact`, `read_to_end`, `read_to_string`, `write_all` (partial progress is lost), `Mutex::lock`, `RwLock::read/write`, `Semaphore::acquire`, `Notify::notified` (lose their place in the fair queue), `mpsc::Sender::send` (the message is dropped with the future).
- **Cancel correctness** is the system level property: a cancel unsafe future, actually cancelled, breaking an invariant. Look for multi step updates with an `.await` in the middle:

```rust
// Bug: if cancelled at the await, `state.data` stays None forever
let mut state = mutex.lock().await;
let data = state.data.take();
let new = process(data).await; // cancellation point
state.data = Some(new);
```

Mitigations, in order of preference:

1. **Move cancellation sensitive work into a spawned task.** Dropping a `JoinHandle` does not cancel the task, so the operation completes even if the caller goes away. Do this for anything that must finish: DB transactions that span several statements, writes to two systems, payment calls.
2. **Split into a cancel safe wait and an infallible commit.** `let permit = tx.reserve().await?; permit.send(msg);` instead of `tx.send(msg).await`.
3. **Use cursor based APIs** that record progress: `write_all_buf(&mut cursor)` instead of `write_all(&buf)`.
4. **Do not leave invariants broken across an await.** Compute the new value first, then mutate synchronously.
5. Never `let _ = some_async_fn();` (the future is never polled): `clippy::let_underscore_future` (default on).

## 5. `select!` correctly

- `select!` polls all branches, runs the first that completes and **drops the others**. Every branch must be cancel safe, or its future must be created once outside the loop and polled by `&mut` so it is resumed, not restarted:

```rust
let op = do_work();          // created once
tokio::pin!(op);
loop {
    tokio::select! {
        res = &mut op => break res,             // resumed each iteration
        Some(msg) = rx.recv() => handle(msg),   // recv is cancel safe
        () = token.cancelled() => return Err(Cancelled),
    }
}
```

- Branch order is random by default for fairness. Add `biased;` when order matters (shutdown signal first), knowing you now own fairness.
- A branch whose pattern does not match is disabled for the rest of that `select!`; with all branches disabled and no `else` the macro panics. Handle channel close (`None`) explicitly.
- Prefer simpler tools when they fit: `tokio::time::timeout` for one deadline (same cancellation caveat), `JoinSet` for N tasks, `futures::stream` combinators for streams.
- `try_join!` drops the remaining futures on the first error. When every operation must finish (stopping several services, flushing several sinks), use `join!` and combine the results afterwards.

## 6. Spawning and structured tasks

- **Every spawned task has an owner who awaits it or aborts it.** A bare `tokio::spawn(fut);` with the handle dropped is fire and forget: its panic is silently swallowed and shutdown cannot wait for it.
- Spawn a known set of tasks with `tokio::task::JoinSet` (aborts all on drop, `join_next()` surfaces panics and errors) or `tokio_util::task::TaskTracker` (waits for all at shutdown).
- Check the `JoinHandle` result: `Err(JoinError)` means the task panicked or was cancelled; log it or propagate it.
- A task's future must be `Send + 'static`: move owned data or `Arc`s in, never borrow from the spawner. Clone the `Arc` into a new binding just before the `async move`.
- Spawn per unit of independent work (per connection, per job), not per tiny step; spawning costs an allocation and scheduling, and a long chain of `spawn` + `await` is just slower sequential code.
- Concurrency limits: unbounded `spawn` per incoming item is a memory and file descriptor bomb. Bound it with a `Semaphore` (acquire before spawning, move the permit into the task), `buffer_unordered(n)` on a stream, or a fixed worker pool reading from a bounded channel.
- `clippy::future_not_send` (nursery) flags public `async fn`s whose futures are not `Send`, which users would discover only when spawning them.

## 7. Graceful shutdown

1. Detect: `tokio::signal::ctrl_c()` and, on Unix, `signal(SignalKind::terminate())` (SIGTERM is what container orchestrators send).
2. Tell: a `tokio_util::sync::CancellationToken`, cloned into each task, which `select!`s on `token.cancelled()` next to its work.
3. Wait: spawn through a `TaskTracker`, then `tracker.close(); tracker.wait().await;` with an overall `timeout` so a stuck task cannot block exit forever.
4. HTTP servers: axum's `serve(..).with_graceful_shutdown(signal)` stops accepting and drains in flight requests.

```rust
let token = CancellationToken::new();
let tracker = TaskTracker::new();
for job in jobs {
    let token = token.clone();
    tracker.spawn(async move {
        tokio::select! {
            () = token.cancelled() => {}
            () = run(job) => {}
        }
    });
}
shutdown_signal().await;
token.cancel();
tracker.close();
if tokio::time::timeout(Duration::from_secs(30), tracker.wait()).await.is_err() {
    tracing::warn!("tasks did not stop within 30s");
}
```

## 8. Channels and backpressure

| Need | Channel |
|---|---|
| many producers, one consumer | `tokio::sync::mpsc` (bounded) |
| one reply to one request | `tokio::sync::oneshot` |
| every subscriber sees every message | `tokio::sync::broadcast` (slow receivers get `Lagged` and lose messages) |
| only the latest value matters (config, status) | `tokio::sync::watch` |
| sync threads | `std::sync::mpsc` or `crossbeam-channel` |

- **Bounded by default.** `unbounded_channel` turns a slow consumer into unbounded memory growth. Pick a capacity and let producers wait (backpressure) or use `try_send` and shed load explicitly.
- The actor pattern (a task owning state, receiving `enum Command { Get { key, reply: oneshot::Sender<..> }, .. }`) replaces most `Arc<tokio::Mutex<_>>` designs and has no lock to hold across awaits.
- When the receiver is dropped, `send` returns `Err`; treat it as "the other side shut down", usually a clean exit, not a panic.

## 9. Async traits

- `async fn` in traits is stable (Rust 1.75), but such traits are not dyn compatible and callers cannot require the future to be `Send`.
- Internal traits: write `async fn` freely.
- Public traits used with multithreaded runtimes: `#[trait_variant::make(Service: Send)]`, or desugar to `fn call(&self, req: Request) -> impl Future<Output = Response> + Send;`.
- Need `dyn Trait`: `#[async_trait::async_trait]`, or methods returning `Pin<Box<dyn Future<Output = T> + Send + '_>>`.

## 10. Threads, Send and Sync

- `std::thread::scope` lets threads borrow from the stack without `Arc`; prefer it for fork-join work that ends before the function returns.
- Data parallel loops: `rayon` (`par_iter()`), not hand rolled thread pools.
- `Rc`, `RefCell`, `Cell` are not thread safe; the compiler stops you. Do not "fix" a `!Send` error with `unsafe impl Send`; find the `Rc` or the guard held across an await.
- Atomics: use `Ordering::SeqCst` unless you can explain why a weaker ordering is correct, or use `Relaxed` only for independent counters and statistics. Anything more clever belongs in a reviewed, tested module (and `loom` tests).
- Thread pools and runtimes are created once at startup, not per request.

## 11. Deadlock rules

From Effective Rust item 17:

- Data that must stay consistent goes under **one** lock (one `Mutex<State>`, not `Mutex<Players>` + `Mutex<Games>`).
- When you must take two locks, **always in the same order** everywhere; document the order next to the fields.
- **Never call a callback, closure, trait object method or channel send while holding a lock.** The callee may take the same lock or block.
- **Never return a `MutexGuard`** to a caller.
- Keep the guard's scope as small as a block: `let value = { let g = m.lock()?; g.get(k).cloned() };`.
- Prefer message passing where a lock design needs a diagram to explain.
- Detect deadlocks in tests with `parking_lot`'s `deadlock_detection` feature or a timeout around the test.

## 12. Tracing in async code

- Use `tracing`, not `log`, and `#[tracing::instrument(skip(pool, body), fields(user_id = %id))]` on async functions. `skip` large or secret arguments; `skip_all` and opt fields in is safer for handlers.
- Never hold `span.enter()` across an `.await` (the span stays entered on whatever task runs next on that thread). Use `.instrument(span)` on the future or `#[instrument]`.
- Request ids come from a middleware (tower-http `TraceLayer`, `SetRequestIdLayer`), once per request, not generated again in handlers.
- Initialise the subscriber once in `main`; tests guard initialisation with `std::sync::Once` / `LazyLock` and only print when an env var such as `TEST_LOG` is set.

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No blocking sleep in async crates | zero | `clippy.toml` `disallowed-methods = [{ path = "std::thread::sleep", reason = "..." }]`; `rg -n 'thread::sleep' src` |
| No std fs/net in async fns | each hit inside `spawn_blocking` | `rg -n 'std::fs::\|std::net::\|reqwest::blocking' src` and check the enclosing fn is not `async` |
| No guard across await | compiles with `tokio::spawn`; zero lint hits | `clippy::await_holding_lock`, `clippy::await_holding_refcell_ref` (default on) |
| No lock in match scrutinee | zero warnings | `clippy::significant_drop_in_scrutinee` (nursery) |
| No dropped futures | zero warnings | `clippy::let_underscore_future` (default on) |
| No fire and forget spawns | every `tokio::spawn` result is stored, joined, or the task is in a `JoinSet`/`TaskTracker` | `rg -n '^\s*tokio::spawn\(' src` (statement position = handle dropped) |
| No unbounded channels without a reason | each `unbounded_channel` has a comment | `rg -n 'unbounded_channel' src` |
| `select!` loops are cancel safe | no `read_exact`, `write_all`, `send(`, `lock(` directly in a branch inside a loop | `rg -n -A8 'select!' src` and inspect |
| Public futures are Send | zero warnings | `clippy::future_not_send` (nursery) in libraries |
| Shutdown handled | SIGTERM and ctrl_c handled, tasks awaited with a deadline | `rg -n 'ctrl_c\|SignalKind::terminate\|with_graceful_shutdown' src` |
| No nested runtimes | zero `Runtime::new`/`block_on` inside async code | `rg -n 'Runtime::new\|block_on' src` |
