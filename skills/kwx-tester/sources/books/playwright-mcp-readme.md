# Playwright MCP README

- Author: Microsoft
- Year: 2026 (package 0.0.84)
- Legal URL: https://github.com/microsoft/playwright-mcp

## What I read

The README and the --help output of @playwright/mcp 0.0.84.

## Key lessons used in web/browser-automation-for-agents.md

- Uses the accessibility tree, not pixels; browser_snapshot 'is better than screenshot'; screenshots cannot be used for actions.
- Default profile is persistent under ~/.cache/ms-playwright/mcp-...; --isolated keeps it in memory; --extension attaches to the user's browser.
- 'Playwright MCP is not a security boundary'; origin allow lists are not a security boundary either.
- CLI with skills is more token efficient for coding agents; MCP for long exploratory loops.
