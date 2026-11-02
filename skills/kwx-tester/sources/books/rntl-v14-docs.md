# React Native Testing Library v14 documentation

- Authors: Callstack and contributors
- Year: v14.x docs, read 2026-10-31
- Legal URL: https://oss.callstack.com/react-native-testing-library/ (moved from callstack.github.io); LLM guidelines in the repo at docs/guides/llm-guidelines.md

## What I read

Quick start, the v14 migration guide, the Jest matchers page, the User Event page, and the LLM guidelines file.

## Key lessons used in mobile/react-native-expo.md (also mobile/mobile-accessibility-testing.md)

- v14 needs React 19+, React Native 0.78+, Node 22.13+; React Test Renderer replaced by the `test-renderer` package.
- render, renderHook, rerender, unmount, fireEvent and act are all async; codemods `rntl-v14-update-deps` and `rntl-v14-async-functions` exist.
- Removed: update, getQueriesForElement, UNSAFE_* queries, concurrentRoot, createNodeMock; strings outside Text always throw.
- Query priority: role, label, placeholder, text, display value, test id last; findBy for async, queryBy only for absence.
- User Event methods: press, longPress, type, clear, paste, scrollTo, pullToRefresh and accessibilityAction (14.1); a press takes at least 130 ms; advanceTimers option for fake timers.
- 18 built in matchers including toBeOnTheScreen, toHaveAccessibleName, toBeBusy, toBeExpanded.
- Prefer ARIA style props (role, aria-label) over accessibilityRole and accessibilityLabel.
