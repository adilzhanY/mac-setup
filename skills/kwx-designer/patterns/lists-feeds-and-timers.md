# Lists, feeds, search and timers

Interface pieces whose data keeps changing: paged lists and feeds, search as you type, countdowns and live durations. Each one has a happy path that looks finished and a set of states and timing traps that make it break. Lessons from the ponytail plugin's infinite scroll, debounce and countdown examples, mostly from the defects of its own short versions.

## Contents

1. Paged lists and feeds
2. Volume
3. Search as you type
4. Timers and live durations
5. Checks

---

## 1. Paged lists and feeds

1. Load the next page with an `IntersectionObserver` watching a sentinel element after the last item, not a scroll listener. Disconnect it in cleanup.
2. Prefetch: give the observer a `rootMargin` of a few hundred pixels (`"600px 0px"` for rows about 60 px tall) so the next page arrives before the user reaches the end.
3. One request at a time. The observer fires again while a page is still loading, so keep an in flight flag and skip while it is set. Keep the load function stable so the observer is not rebuilt on every render.
4. A row for every state:
   - loading more: a spinner row at the end while the page fetches;
   - end of list: a calm row with the total ("You have seen all 248 orders");
   - error: the reason and a Retry that refetches only the failed page;
   - first page empty: the empty state, not an endless spinner.
5. Keyboard and screen reader users: endless loading pushes the footer out of reach and loses their place. Prefer a "Load more" button, or switch to one after two or three automatic loads. Announce "20 more orders loaded" in an `aria-live="polite"` region, keep focus where it was (move it to the first new item only when the button was used), and restore the scroll position on Back.

## 2. Volume

- Decide the realistic size before building: 3 rows or 30,000, one user or a team of 200. Write the size you designed for in the reply.
- No request per row (an avatar, a price or a status fetched per item). Fetch the page in one request.
- A list that only grows in memory gets pagination or windowing (render only the visible rows) once it reaches thousands of rows.
- A change to one row re-renders that row, not the whole list.

## 3. Search as you type

1. Local filtering stays instant (no debounce over about 50 ms, `platforms/desktop/keyboard-and-command-palette.md`). Remote search waits about 300 ms after the last keystroke.
2. Write the debounce inline with `clearTimeout` and `setTimeout`. Make a shared utility only once three or more inputs need it.
3. Debounce does not stop stale results: a slow earlier response can land after a newer one and overwrite it. Abort the previous request with an `AbortController`, or drop any response whose query is no longer the current one.
4. States: an empty query clears the results without a request; a loading indicator sits inside the field; an error shows the reason and Retry; no results gets the designed empty state with the filters still visible.
5. Markup: `<input type="search">` with a real label, inside a `<search>` element (or `role="search"` on a wrapper for older browsers). The placeholder "Search..." is not a label.

## 4. Timers and live durations

1. Compute the remaining time from a fixed end timestamp on every tick (`end - Date.now()`). Never decrement a counter once per `setInterval` call: intervals drift, and browsers throttle timers in background tabs to once a second or less, so a decrementing timer runs slow.
2. One interval for the timer's lifetime. Restart it only when the end time changes. In React the effect depends on the end time, never on the remaining value (ponytail's version depended on `[remaining]` and tore the interval down every second).
3. Define zero: what is shown, what happens next, and the interval is cleared.
4. Durations over a minute read as m:ss or h:mm:ss, never "245s". `Intl.DurationFormat` with `style: "digital"` gives `0:04:05` (Baseline 2025, newly available since March 2025, per MDN); pad by hand where the target is older.
5. Accessibility: `role="timer"` on the display (its live setting is off by default), so a screen reader is not interrupted every second. Announce only milestones ("1 minute left", "Time is up") in a separate polite live region. Give readable text ("45 seconds") or `<time datetime="PT45S">`.
6. The deadline itself comes from the server or a stored value, never from page load (`psychology/psychology.md`, honesty rules).

## 5. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Observer, not scroll | Next page loads from an `IntersectionObserver` with a `rootMargin`, disconnected in cleanup | Read the effect or setup code |
| No double load | An in flight flag guards the load function | Find the flag check before the fetch |
| Feed states | Loading more, end of list, error with retry and empty rows all exist | Read the list's render branches |
| Reachable footer | A Load more button exists, or auto loading stops; new items announced politely | Find the button and the live region |
| Sized | The designed volume is stated; no fetch per row | Read the row component for fetch calls |
| Fresh results | The previous search request is aborted or its late response dropped | Find the `AbortController` or the query comparison |
| Timer correct | Remaining time computed from an end timestamp; one interval | Read the tick function and the effect dependencies |
| Timer readable | m:ss or h:mm:ss; `role="timer"`; milestone announcements only | Read the formatter and the markup |
