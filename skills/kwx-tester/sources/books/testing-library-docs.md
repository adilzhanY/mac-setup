# Testing Library docs: guiding principles, queries, user-event

- Author: Kent C. Dodds and contributors
- Year: 2026
- Legal URL: https://testing-library.com/docs/guiding-principles ; https://testing-library.com/docs/queries/about/ ; https://testing-library.com/docs/user-event/intro

## What I read

The three pages.

## Key lessons used in web/component-and-unit-tests.md

- Core principle: tests that resemble use give more confidence; DOM nodes, not component instances.
- Query priority with quotes (getByRole 'top preference for just about everything', placeholder 'not a substitute for a label', test ids only when nothing else works).
- getBy / queryBy / findBy behaviour table; use screen.
- user-event simulates full interactions and checks visibility and interactability; call userEvent.setup() in the test, not in hooks.
