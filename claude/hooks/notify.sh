#!/usr/bin/env bash
# Desktop notification with a sound when Claude Code finishes a turn.
# Wired to the Stop hook event in ~/.claude/settings.json.

input=$(cat)
cwd=$(jq -r '.cwd // ""' <<<"$input")
project=$(basename "${cwd:-$PWD}")

# terminal-notifier shows Claude's icon when one is given; osascript is the fallback
if command -v terminal-notifier >/dev/null 2>&1; then
  terminal-notifier -title "Claude Code finished" -message "Done in ${project}" \
    -group claude-code -sound Glass >/dev/null 2>&1 &
else
  osascript -e "display notification \"Done in ${project}\" with title \"Claude Code finished\" sound name \"Glass\"" >/dev/null 2>&1 &
fi

exit 0
