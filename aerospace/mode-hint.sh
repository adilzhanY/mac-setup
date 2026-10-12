#!/bin/bash
# Called by AeroSpace on every mode change. Shows the letters of the apps and
# websites modes as a notification, the way the Linux shell drew a mode card.
# Keep the lists in step with aerospace.toml.

case "$(aerospace list-modes --current)" in
  apps)     title="Apps";     text="C Claude   V VS Code   O Obsidian   P 1Password" ;;
  websites) title="Websites"; text="G GitHub   M Gmail   Y YouTube   C Claude   H ChatGPT   I Gemini   T Translate" ;;
  *) exit 0 ;;
esac

osascript -e "display notification \"$text\" with title \"$title\""
