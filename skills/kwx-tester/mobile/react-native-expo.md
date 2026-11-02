# React Native and Expo: tests in Jest

How to write fast, honest tests for a React Native or Expo app that run in Node, with no device: the jest-expo preset, React Native Testing Library (RNTL) v14, mocks for native and Expo modules, Expo Router tests, Reanimated and gesture handler, hooks and stores, local storage and Supabase clients, and the error messages you will meet. Every snippet marked "verified" ran on 2026-10-31 on a fresh `create-expo-app` with Expo SDK 58, React Native 0.88.1, React 19.3, Jest 30.5, jest-expo 58.0.13, RNTL 14.1.0, test-renderer 1.3.1, expo-router 58, Reanimated 4.7.1, gesture handler 3.3. Base rules for Testing Library are in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` section 9; this file adds what is specific to RN and to v14.

## Contents

1. What Jest can and cannot prove
2. Setup
3. RNTL v14: render, queries, user events, async utils, matchers
4. Mocking native modules and Expo modules
5. Expo Router
6. Reanimated and gesture handler
7. Hooks, stores and data fetching
8. Local storage: AsyncStorage, MMKV, SQLite
9. Supabase clients
10. Timers and time
11. Common errors and fixes
12. Checks

## 1. What Jest can and cannot prove

Jest with jest-expo runs your JS in Node with the native side replaced by mocks. React Native's docs say it plainly: component tests "are only JavaScript tests running in Node.js environment. They do not take into account any iOS, Android, or other platform code."

| Jest proves | Jest cannot prove |
|---|---|
| Logic, reducers, stores, hooks, validation | That a native module behaves as its mock does |
| What a screen shows in each state, and what each press does | Layout: overflow, clipping, keyboard covering an input, safe areas |
| Navigation decisions (Expo Router `renderRouter`) | Gestures and animations feel right on a device |
| That data is written to and read from storage APIs | Process death, permissions dialogs, push delivery, deep links from the OS |
| Accessibility names, roles and states | What TalkBack or VoiceOver actually reads in order |

Anything in the right column goes to a Maestro flow (`e2e-maestro-detox.md`) or to the user's checklist (`mobile-edge-cases.md`).

## 2. Setup

Verified:

```sh
npx expo install jest-expo jest @types/jest @testing-library/react-native test-renderer --dev
```

```json
{
  "scripts": { "test": "jest", "test:watch": "jest --watch" },
  "jest": {
    "preset": "jest-expo",
    "setupFilesAfterEnv": ["./jest-setup.ts"],
    "passWithNoTests": false
  }
}
```

Facts about the preset, read from `node_modules/jest-expo/jest-preset.js` (SDK 58):

- It mocks the native part of the Expo SDK and many third party native modules. You do not mock `expo-constants`, `expo-font` or `expo-linking` yourself.
- It maps `tsconfig.json` `paths` to Jest `moduleNameMapper`, so `@/components/...` imports work without extra config.
- It already sets `transformIgnorePatterns` for `react-native`, `@react-native`, `expo`, `@expo`, `@react-navigation`, `@sentry/react-native` and a few more. If you override `transformIgnorePatterns`, you replace the whole list: copy the preset's pattern and add your package to it, do not write a short one from memory.
- It sets `passWithNoTests: true`. A CI job with a wrong test path then passes with zero tests. Set it to `false` (above).
- Platform presets exist: `jest-expo/ios`, `jest-expo/android`, `jest-expo/web`, `jest-expo/node`, `jest-expo/universal` (runs every test once per platform). Use `jest-expo/universal` only when code branches on `Platform.OS`.
- SDK 58 and later need Jest 30. Upgrade `jest`, `@types/jest` and `jest-expo` together (Expo docs).
- `react-test-renderer` is deprecated and does not support React 19. RNTL v14 needs `test-renderer` instead. RNTL v14 needs React 19, React Native 0.78 or newer and Node 22.13 or newer; React 18 projects stay on RNTL v13.

Upgrading an old suite from v13: run the codemods `npx codemod@latest rntl-v14-update-deps` and `npx codemod@latest rntl-v14-async-functions --target ./src`, then read the diff (RNTL migration guide; the exact runner command is from the guide, not verified here).

Lint the tests: `eslint-plugin-testing-library` with the `react` config on test files catches missing `await`, `getBy` used for absence, and side effects in `waitFor`.

RNTL ships agent guidance inside the package: `node_modules/@testing-library/react-native/docs/guides/llm-guidelines.md`. Read it when unsure about a v14 rule.

## 3. RNTL v14: render, queries, user events, async utils, matchers

### 3.1 Everything is async

In v14 `render`, `renderHook`, `rerender`, `unmount`, `fireEvent.*` and `act` return promises. Every test that uses them is `async` and awaits them. A missing `await` on `render` fails with "`render` function has not been called" (verified). Do not wrap these calls in `act`; RNTL does it.

### 3.2 A complete screen test (verified)

```tsx
import { render, screen, userEvent } from '@testing-library/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { SaveName } from '../SaveName';

jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock'),
);

beforeEach(async () => {
  await AsyncStorage.clear();
});

test('save button is disabled until a name is typed', async () => {
  await render(<SaveName />);
  expect(await screen.findByText('Nothing saved')).toBeOnTheScreen();
  expect(screen.getByRole('button', { name: 'Save' })).toBeDisabled();
});

test('typing a name and pressing Save stores it and shows it', async () => {
  const user = userEvent.setup();
  await render(<SaveName />);
  await user.type(screen.getByLabelText('Name'), 'Aru');
  await user.press(screen.getByRole('button', { name: 'Save' }));
  expect(await screen.findByText('Saved: Aru')).toBeOnTheScreen();
  expect(await AsyncStorage.getItem('name')).toBe('Aru');
});

test('a name saved earlier is shown on start', async () => {
  await AsyncStorage.setItem('name', 'Old');
  await render(<SaveName />);
  expect(await screen.findByText('Saved: Old')).toBeOnTheScreen();
});
```

The component used `<TextInput aria-label="Name">` and `<Pressable role="button" aria-disabled={...} disabled={...}>`. The tests read like the spec: one behavior per test, state checked through what the user sees and through the storage API.

### 3.3 Query priority

Use `screen`, not destructured results. In order:

1. `getByRole('button', { name: 'Save' })`. Matches only accessibility elements: `Pressable`, `Button`, `TextInput` and `Text` are accessible by default; a `View` needs `accessible` plus a `role`. If `getByRole` cannot find your button, the screen reader cannot either. Fix the component, not the query.
2. `getByLabelText` (from `aria-label`, `accessibilityLabel` or `aria-labelledby`).
3. `getByPlaceholderText`, `getByText`, `getByDisplayValue`.
4. `getByTestId` last, for things with no user visible handle.

Variants: `getBy*` throws when not found (use for presence), `queryBy*` returns null (use only with `.not.toBeOnTheScreen()`), `findBy*` waits up to 1 second by default (use for anything that appears after async work). Scope with `within(screen.getByRole('list'))`.

Hidden content: v14 gives hidden Suspense and `<Activity mode="hidden">` content `display: 'none'`, so default queries skip it. Pass `{ includeHiddenElements: true }` only when you test hidden content on purpose.

### 3.4 User events over fireEvent

`const user = userEvent.setup()` then `await user.press`, `longPress`, `type`, `clear`, `paste`, `scrollTo`, `pullToRefresh` (14.1), `accessibilityAction` (14.1). User Event fires the full sequence a real touch fires (`pressIn`, `pressOut`, focus, `changeText`, `endEditing`, blur), so it catches bugs `fireEvent.press` misses, for example a handler on `onPressIn`. `type` works only on host `TextInput`s and appends to existing text.

`fireEvent` is for events User Event does not model, such as `fireEvent(element, 'layout', { nativeEvent: { layout: { width: 320 } } })` or custom props. In v14 `fireEvent.press` builds a default native event and merges yours into it, so assert handler arguments with `expect.objectContaining`.

A press takes at least 130 ms of simulated time. With fake timers pass `userEvent.setup({ advanceTimers: jest.advanceTimersByTime })` (verified).

### 3.5 Async utils

- `await screen.findByText('Saved')` to wait for something to appear.
- `await waitFor(() => expect(mockSubmit).toHaveBeenCalledTimes(1))` for a condition that is not an element. One assertion inside, no side effects inside, never empty.
- `await waitForElementToBeRemoved(() => screen.getByText('Loading'))` for a spinner going away.
- Never `await new Promise(r => setTimeout(r, 500))`.

### 3.6 Matchers

Built in, no import needed: `toBeOnTheScreen`, `toBeVisible`, `toBeEnabled`, `toBeDisabled`, `toBeChecked`, `toBePartiallyChecked`, `toBeSelected`, `toBeExpanded`, `toBeCollapsed`, `toBeBusy`, `toHaveTextContent`, `toHaveDisplayValue`, `toHaveAccessibleName`, `toHaveAccessibilityValue`, `toHaveStyle`, `toHaveProp`, `toContainElement`, `toBeEmptyElement`. Prefer state matchers (`toBeDisabled`) over prop checks (`toHaveProp('disabled', true)`), because the matcher also follows `aria-disabled` and ancestors.

### 3.7 Snapshots

Do not snapshot whole screens. Expo's docs recommend E2E (Maestro) over snapshot unit tests for UI, and React Native's docs warn that a snapshot "is considered to be correct, even in the case when the rendered output is actually wrong." Use `toMatchInlineSnapshot` for small serialized values only.

## 4. Mocking native modules and Expo modules

Order of preference:

1. **Nothing to mock.** jest-expo already mocks the Expo SDK native side. Try the test first.
2. **The library's own Jest mock.** Many native libraries ship one. Use it from `jest-setup.ts`:

```ts
// jest-setup.ts
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock'),
);
jest.mock('react-native-safe-area-context', () =>
  require('react-native-safe-area-context/jest/mock').default,
);
```

Both mock files exist in the installed packages (checked); the AsyncStorage one was run in the verified test.

3. **A root `__mocks__/<package>.ts` file** next to `node_modules` for a package used in many tests. Jest picks it up automatically for node modules.
4. **A per test `jest.mock` with a small fake** for behavior the test controls:

```ts
import * as Location from 'expo-location';

jest.mock('expo-location', () => ({
  requestForegroundPermissionsAsync: jest.fn(),
  getCurrentPositionAsync: jest.fn(),
  PermissionStatus: { GRANTED: 'granted', DENIED: 'denied' },
}));

test('shows the manual city field when location is denied', async () => {
  jest.mocked(Location.requestForegroundPermissionsAsync).mockResolvedValue({
    status: 'denied', granted: false, canAskAgain: false, expires: 'never',
  } as any);
  await render(<WeatherScreen />);
  expect(await screen.findByLabelText('City')).toBeOnTheScreen();
});
```

Rules:

- Mock the native boundary, never your own modules. A test that mocks `useProfile` proves only that the screen renders what the mock returns.
- Write a test for each result the native side can give: granted, denied, `canAskAgain: false`, throws. This is where permission bugs live.
- Keep mocks typed (`jest.mocked`) so a library update that changes a signature breaks the test, not production.
- Set `restoreMocks: true` (or `clearMocks`) in the Jest config so one test's mock setup does not leak into the next.
- For HTTP, prefer injecting a client or a repository and passing a fake. If you mock at the network layer, MSW's `msw/node` server is the usual choice; set `onUnhandledRequest: 'error'` so a forgotten request fails the test. (MSW in jest-expo is not verified here; it may need `fetch` and stream globals.)

## 5. Expo Router

Use `expo-router/testing-library`. It needs RNTL v14 on SDK 58 (v13 only on SDK 57). Verified:

```tsx
import { renderRouter, screen, testRouter } from 'expo-router/testing-library';
import { Link } from 'expo-router';
import { Text } from 'react-native';
import { userEvent } from '@testing-library/react-native';

test('deep link opens the profile screen with its id', async () => {
  await renderRouter(
    {
      index: () => <Text>Home</Text>,
      'profile/[id]': () => <Text>Profile</Text>,
    },
    { initialUrl: '/profile/42' },
  );
  expect(screen).toHavePathname('/profile/42');
  expect(screen).toHaveSegments(['profile', '[id]']);
  expect(await screen.findByText('Profile')).toBeOnTheScreen();
});

test('tapping a link navigates, back returns', async () => {
  const user = userEvent.setup();
  await renderRouter({
    index: () => <Link href="/settings">Open settings</Link>,
    settings: () => <Text>Settings</Text>,
  });
  await user.press(screen.getByText('Open settings'));
  expect(await screen.findByText('Settings')).toBeOnTheScreen();
  await testRouter.back();
  expect(screen).toHavePathname('/');
});
```

- Mock file system keys have no leading `./` or `/` and no extension. A string array (`['index', 'profile']`) gives routes that render `null`.
- To test your real layouts, pass a fixture folder: `renderRouter({ appDir: './__fixtures__/app', overrides: { '(auth)/_layout': MockLayout } })`. Paths resolve from the folder Jest runs in.
- Matchers: `toHavePathname`, `toHavePathnameWithParams('/a?x=1')`, `toHaveSegments`, `toHaveSearchParams`, `toHaveRouterState`.
- `testRouter.push / replace / navigate / back / setParams / dismissAll` are async; await them.
- Good targets: auth redirects (signed out user opening `/settings` lands on `/sign-in`), deep link params parsed into the screen, a protected group's layout, `+not-found`.

Write one `renderRouter` test per session state: signed out lands on the login header, signed in lands on home, expired session lands on login. With `Stack.Protected`, the screens the guard switches to must be direct screens of that stack. Tests and helpers live outside `src/app` (every file there is a route and gets bundled). Check: `find src/app -path "*__tests__*" -o -name "*.test.*"` is empty (mistakes M18 in `~/.claude/ui-designer/mistakes.md`: a signed-out start showed "Unmatched Route").

## 6. Reanimated and gesture handler

Reanimated 4 (verified):

```json
"jest": {
  "preset": "jest-expo",
  "resolver": "react-native-reanimated/jest/resolver",
  "setupFilesAfterEnv": ["./jest-setup.ts"]
}
```

```ts
// jest-setup.ts
require('react-native-reanimated').setUpTests();
```

```tsx
test('pressing Hide fades the box out', async () => {
  jest.useFakeTimers();
  const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
  await render(<Fader />);
  await user.press(screen.getByRole('button', { name: 'Hide' }));
  jest.advanceTimersByTime(400);
  expect(screen.getByTestId('box')).toHaveAnimatedStyle({ opacity: 0 });
  jest.useRealTimers();
});
```

Without the resolver the suite fails at import with "TypeError: Cannot read properties of undefined (reading 'loadUnpackersWithCode')" (verified). Mocking `react-native-worklets` with its `src/mock` instead failed with "`setCSSEventHandler` is not available in JSReanimated" (verified), so use the resolver.

Gesture handler: the docs say to add `"setupFiles": ["react-native-gesture-handler/jestSetup.js"]` and to use `fireGestureHandler` and `getByGestureTestId` from `react-native-gesture-handler/jest-utils`. On gesture handler 3.3 with worklets 0.13 and the Reanimated resolver, any suite that imports `react-native-gesture-handler` failed after its tests passed with "[Worklets] `getUIRuntimeHolder` is not supported on web" (verified 2026-10-31; the worklets resolver gave "`runOnUISync` is not supported on web"). What worked: keep `GestureHandlerRootView` in the root layout only, and in suites that do not test gestures stub the module:

```ts
// shortcut: stubs gesture handler entirely, remove when the upstream Jest setup works with your versions
jest.mock('react-native-gesture-handler', () => {
  const { View } = require('react-native');
  return { GestureHandlerRootView: View };
});
```

Test gesture logic (thresholds, snap points) as pure functions, and leave the feel of a swipe to a Maestro flow or the user's checklist. Re-check this section after each Reanimated, worklets or gesture handler upgrade.

## 7. Hooks, stores and data fetching

- Test a custom hook through a component that uses it, unless the hook is a reusable library. Then `const { result } = await renderHook(() => useCounter())` and `await act(() => result.current.increment())`.
- **Zustand:** stores are module singletons and leak state between tests. Reset in `beforeEach` with the store's initial state (`useStore.setState(initialState, true)`), or follow Zustand's documented `__mocks__/zustand.ts` that resets every store after each test.
- **TanStack Query:** new `QueryClient` per test, `retry: false` so an error state appears at once, and a wrapper:

```tsx
function renderWithClient(ui: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: Infinity } } });
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}
```

- **Redux Toolkit:** build a real store per test with `configureStore({ reducer, preloadedState })`; do not mock `useSelector`.
- Test the store's logic directly (actions in, state out) and the screen with the real store. Both are fast.

### Offline: the minimum rendered tests

For an app with a persisted query cache, mock `@react-native-community/netinfo` to `isConnected: false` and seed a QueryClient from a persisted cache fixture. Then render the real screens and assert:

1. The offline banner shows, with the data timestamp.
2. The cached primary data renders (e.g. a gym app's schedule and bookings).
3. Every action that needs the network is disabled or refused with a message, and the fetch mock has 0 calls (e.g. book and cancel).
4. Anything the spec promises offline renders from the cache (e.g. the membership QR).
5. Offline with no cache shows the empty offline view ("offline, nothing saved yet"), not the error view.

A test of a pure viewState function or reducer does not replace these. Why: android A had 13 app tests and none rendered offline.

## 8. Local storage: AsyncStorage, MMKV, SQLite

- **AsyncStorage:** use the package mock (section 4). Clear it in `beforeEach`. Test that the app reads data written by the previous app version: seed the old key and shape, render, assert the screen. That is the cheapest upgrade test you can write.
- **MMKV:** recent `react-native-mmkv` versions ship an in memory implementation for Jest; check the package's testing docs for your version.
- **expo-sqlite:** its native module does not run in Node, and there is no official Jest mock. Put all SQL behind a small repository interface. Test screens with a fake repository. Test the SQL itself in Node with `better-sqlite3` (same SQLite engine, synchronous API) by running the same migration and query strings through a thin adapter, and test the real `expo-sqlite` path once in a device E2E flow that upgrades with old data. Evidence: opinion (no official guidance exists; community packages such as `expo-sqlite-mock` take the same approach).
- **Migrations:** keep a fixture database or SQL dump for every released schema version. A test opens each one, runs the migrations, and checks the data, not only the schema. See `mobile-edge-cases.md` "App update with old data".

## 9. Supabase clients

- The app should create one Supabase client in one module and pass it (or a repository built on it) to features. Screens never call `supabase.from(...)` directly; that keeps them testable with a fake repository.
- **Unit and screen tests:** fake the repository. Do not stub the chained query builder (`from().select().eq()`); such stubs break on every refactor and prove nothing.
- **Integration tests:** run in Node against a local stack (`supabase start`), with the real client and real RLS policies, a fresh user per test. No device needed. Never point tests at the production project. Backend testing details live in `../backend/`.
- The client stores its session in AsyncStorage on mobile; the AsyncStorage mock covers it. Turn off `autoRefreshToken` in tests, and call `supabase.removeAllChannels()` in `afterAll` if a test opened Realtime, or Jest reports open handles.
- Test the signed out, expired session and network error paths, not only the happy path.

## 10. Timers and time

- Use `jest.useFakeTimers()` for debounce, polling, toasts and animations; pass `advanceTimers` to `userEvent.setup`.
- Pin the clock with `jest.setSystemTime(new Date('2026-03-29T01:30:00Z'))` for date logic, and pick dates that hit edge cases: DST change, month end, leap day, the user's time zone different from UTC.
- Pin the zone for the whole run: `"test": "TZ=UTC jest"` (and add one test that sets another zone through your injected formatter).
- Restore real timers in `afterEach` if a test switched them on.

## 11. Common errors and fixes

| Error message | Cause | Fix |
|---|---|---|
| "`render` function has not been called" (verified) | `render` not awaited in v14 | `await render(...)`, make the test `async` |
| "Invariant Violation: Text strings must be rendered within a <Text> component" (verified) | A bare string inside a `View`; v14 always checks this | Wrap it in `<Text>`; it is a real bug on device too |
| "[@RNC/AsyncStorage]: NativeModule: AsyncStorage is null" (verified) | No Jest mock for AsyncStorage | Add the package mock in `jest-setup.ts` |
| "Cannot read properties of undefined (reading 'loadUnpackersWithCode')" (verified) | Reanimated or worklets loaded without the Jest resolver | `"resolver": "react-native-reanimated/jest/resolver"` and `setUpTests()` |
| "[Worklets] `getUIRuntimeHolder` is not supported on web" (verified) | Gesture handler 3.x imported under the web resolver | Stub gesture handler in that suite (section 6) |
| "SyntaxError: Cannot use import statement outside a module" | A package in `node_modules` ships untranspiled ESM and is not in `transformIgnorePatterns` | Copy the preset's pattern and add the package name inside the `(?!...)` group |
| "TurboModuleRegistry.getEnforcing(...): 'X' could not be found" | A native module with no Jest mock | Library mock, `__mocks__` file, or `jest.mock` with a fake (section 4) |
| "An update to X inside a test was not wrapped in act(...)" | State changes after the test stopped waiting | Wait for the final UI with `findBy*`; await every RNTL call; do not wrap in `act` by hand |
| "You are trying to import a file after the Jest environment has been torn down" | Async work (timers, promises, Realtime) still running after the test | Await the work, clear timers, close channels in `afterAll` |
| "Jest did not exit one second after the test run has completed" | Open handles: sockets, intervals, Supabase Realtime | `npx jest --detectOpenHandles`, then close what it reports |
| `getByRole` finds nothing, but the element is visible | The element is not an accessibility element (`View` without `accessible`, or `accessible={false}` on a parent) | Make it accessible with a role; that also fixes TalkBack |
| Test files in `app/` break routing | Expo Router treats every file in `app/` as a route | Move tests to `__tests__/` |
| Unknown option warning from `render` or `userEvent.setup` | v14 warns on unknown options (for example the removed `concurrentRoot`) | Remove the option |

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Suite runs in Node | `npx jest` green, no device | Run it; paste the `Tests:` line |
| No silent empty run | `passWithNoTests` is `false` | `rg -n passWithNoTests package.json jest.config.*` |
| v14 async discipline | Every `render`, `fireEvent`, `renderHook`, `act` awaited | `rg -n "^\s*(render|fireEvent(\.\w+)?|renderHook|act)\(" --glob '*test*'` returns nothing |
| No `react-test-renderer` | Removed from `package.json` | `rg -n react-test-renderer package.json` |
| Queries user facing | `getByTestId` used only where no role, label or text exists | `rg -c ByTestId` compared with `rg -c "ByRole|ByLabelText|ByText"` |
| Mocks at the boundary only | No `jest.mock` of relative paths into your own code | `rg -n "jest\.mock\(['\"]\.\.?/" --glob '*test*'` and review each |
| Mocks restored | `restoreMocks` or `clearMocks` set | `rg -n "restoreMocks|clearMocks" package.json jest.config.*` |
| Stores reset between tests | Each store has a reset in `beforeEach` or a reset mock | Read setup files |
| Every native result tested | Granted, denied, blocked, error for each permission or native call the screen uses | Read the test names |
| No tests in `app/` | None | `fd -e tsx -e ts . app | rg -i test`; `find src/app -path "*__tests__*" -o -name "*.test.*"` prints nothing |
| Router per session state | one `renderRouter` test each for signed out, signed in, expired | Read the test names |
| Offline set | the 5 rendered offline tests of section 7 exist with netinfo mocked offline and a seeded cache | Read the test file |
| No fixed sleeps | None | `rg -n "setTimeout\(r|new Promise\(.*setTimeout" --glob '*test*'` |
| Upgrade data covered | A test seeds old storage keys or an old DB and reads them | Read test names for "old", "migrat", "upgrade" |
