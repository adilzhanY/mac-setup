# Dialogs and overlays

The mechanics of modal dialogs on the web: which element, how it is named, every way it closes, light dismiss, and focus. Layout of creation modals lives in `patterns/saas-app-patterns.md` (section 6); when to confirm and when to offer undo lives in `patterns/states-feedback-and-failure.md` (section 9). Lessons from the ponytail plugin's modal example, including the defects in its own "lean" version.

## Contents

1. Which dialog to build on
2. Name and describe it
3. Every way it closes
4. Light dismiss
5. Focus
6. Checks

---

## 1. Which dialog to build on

1. The house dialog component, when the project has one.
2. Otherwise the native `<dialog>` opened with `showModal()`. It gives the top layer (no z-index fights, no portal), makes the rest of the page inert, closes on Escape, and styles its scrim with `::backdrop`. No overlay, portal, root or trigger wrappers are needed. `<dialog>` is Baseline widely available since March 2022 (MDN).
3. `show()` opens a non modal dialog: the page stays interactive, there is no backdrop and no inertness. Use it only for a deliberately non modal panel.
4. A dialog library only when the project already ships one. Ponytail's example: Radix Dialog (1 dependency and 30 lines) became `<dialog>` plus `showModal()` (8 lines). It then lost the accessible name, which section 2 restores.

## 2. Name and describe it

Every dialog has an accessible name: `aria-labelledby` pointing at its heading, and `aria-describedby` pointing at the consequence text. Without it a screen reader announces "dialog" and nothing else.

```html
<dialog id="delete-report" aria-labelledby="dr-title" aria-describedby="dr-desc">
  <form method="dialog">
    <h2 id="dr-title">Delete "Q3 report"?</h2>
    <p id="dr-desc">The report and its 12 charts are removed. This cannot be undone.</p>
    <button value="cancel" autofocus>Cancel</button>
    <button value="delete" class="danger">Delete</button>
  </form>
</dialog>
```

## 3. Every way it closes

- Buttons inside `<form method="dialog">` close the dialog and set `dialog.returnValue` to the button's `value`, with no click handlers.
- Read the answer in one `close` listener. Treat anything other than the confirming value as cancel, so Escape, the Cancel button and any later close path all run the same code.
- Escape fires `cancel` and then `close`. Ponytail's native version never told the caller on Escape: the parent kept waiting for an answer.
- Reset `dialog.returnValue = ""` before each `showModal()`, or a "delete" from the previous opening is read again when the next one closes by Escape.
- A dialog holding typed input that would be lost: handle `cancel` and ask, or keep the draft.

## 4. Light dismiss

- A modal opened with `showModal()` does not close on a backdrop click by default. Its default `closedby` behaviour is `closerequest`: Escape and the platform's back gesture only (MDN).
- Decide light dismiss on purpose. `closedby="any"` adds backdrop click and tap. Support per the MDN browser compat data (read 2026-10-29): Chrome 134, Firefox 141, Safari only in Technology Preview.
- For Safari, add a click handler that closes when `event.target === dialog`. A click on the backdrop lands on the dialog element itself; so does a click on the dialog's own padding, so give the dialog `padding: 0` and put the padding on an inner wrapper.
- Keep light dismiss off for destructive confirms and for forms with typed input. A stray click must not answer the question or throw away work.

## 5. Focus

- **Initial focus.** `showModal()` focuses the first focusable element inside, or the element with `autofocus` (MDN). On a destructive confirm put `autofocus` on Cancel; do not rely on source order.
- **Inert, not trapped.** The page behind is inert, but Tab can still leave the dialog to the browser's own interface (the address bar). That is expected; do not fight it with a script trap. (Observed behaviour reported by the ponytail examples; MDN states only the inertness.)
- **Focus return.** The HTML standard returns focus to the element that was focused before `showModal()` when the dialog closes; older browser versions did not. Not verified per browser version here. When older browsers matter, store `document.activeElement` before opening and focus it in the `close` handler.

## 6. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Right base | House dialog, else `<dialog>` with `showModal()` | No `show()` for a modal, no portal wrapper added next to a native dialog |
| Named | `aria-labelledby` on the heading, `aria-describedby` on the consequence | Read the dialog element's attributes |
| One close path | Escape, Cancel and the backdrop all reach one `close` handler | Find the `close` listener; `returnValue` reset before opening |
| Light dismiss decided | On for harmless panels, off for destructive confirms and typed input | Read `closedby` and any backdrop click handler |
| Safe focus | Cancel has `autofocus` on destructive confirms; focus returns to the trigger | Read `autofocus` and the close handler |
