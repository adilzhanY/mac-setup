# Mac setup guide

This folder rebuilds the user's Linux (Arch + Hyprland) working setup on a MacBook. It is written for an AI agent (Claude Code) running on that Mac. The user copies this folder to the Mac and asks the agent to follow it.

The folder holds working configuration only. It has no names, emails, accounts, tokens, server addresses or profile links. Do not add any. Where personal data is needed (git name and email, logins), ask the user at that step.

## How to work through this guide

- Run every command from inside this folder (the copy commands use paths relative to it).
- Work top to bottom: **1. Must do**, then **2. Comfort**, then **3. Useful**. Finish and verify each step before the next one.
- This is a company MacBook. If Homebrew, a cask, an admin password prompt or a privacy permission is blocked by the company's device management, stop and tell the user to ask IT. Do not try to work around it.
- **Never click, type or move the mouse for the user** (no AppleScript keystrokes, no `cliclick`). Steps marked **[USER]** need the user's hands: a password, a login in the browser, or a switch in System Settings. Tell the user exactly where to click, then wait.
- Install with Homebrew wherever possible, so everything can be updated with `brew upgrade`.
- Copy files from this folder; do not symlink into it, so the folder can be deleted afterwards.
- After each section, run its **Check** and fix what fails before going on.
- Report at the end: what is installed, what was skipped and why, and what the user still has to do by hand.

### Ask the user first

Ask these before starting, in one message:

1. Full name and **work** email for git commits.
2. Which GitHub account to use on this Mac (work account, or none yet).
3. Which team chat app the team uses (Slack, Teams, Google Chat...). It goes on Super+A then S.
4. Docker: does the team use Docker Desktop (needs a company license), OrbStack, or nothing yet? With no answer, use Colima (free and open source).
5. Does the MacBook have a German (ISO) or US physical keyboard? The setup uses the US (ABC) input source either way.

## Folder contents

| Path | Goes to | What it is |
|---|---|---|
| `aerospace/aerospace.toml` | `~/.config/aerospace/aerospace.toml` | Window manager: all key bindings, the apps and websites modes |
| `aerospace/mode-hint.sh` | `~/.config/aerospace/mode-hint.sh` | Shows the letters of a mode while it is active |
| `kitty/kitty.conf`, `search.py`, `scroll_mark.py` | `~/.config/kitty/` | Terminal config and the scrollback search kitten |
| `fish/config.fish` | `~/.config/fish/config.fish` | Shell |
| `starship.toml` | `~/.config/starship.toml` | Prompt |
| `tmux/tmux.conf` | `~/.config/tmux/tmux.conf` | tmux |
| `nvim/` | `~/.config/nvim/` | The full Neovim config |
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Global rules for Claude Code |
| `claude/settings.json` | `~/.claude/settings.json` | Claude Code settings: model, effort, plugins, statusline, hooks |
| `claude/statusline.sh` | `~/.claude/statusline.sh` | Status line (works with GNU and BSD `date`) |
| `claude/hooks/notify.sh` | `~/.claude/hooks/notify.sh` | Notification and sound when Claude finishes |
| `claude-mods/` | `~/dev/claude-mods/` | Claude Code mods: Clawd, model buttons, stats card, savvy-progress |
| `skills/caveman/` | `~/.claude/skills/caveman/` | The caveman skill, with the user's own edits |
| `skills/mgpro/` | `~/.claude/skills/mgpro/` | mgpro: Apple-style motion graphics videos with Remotion, three.js and synthesized sound |
| `skills/kwx-designer/` | `~/.claude/skills/kwx-designer/` | kwx-designer: premium, intuitive UI design for web, mobile, desktop and editors, with custom SVG icons and a quality gate |
| `herdr/config.toml` | `~/.config/herdr/config.toml` | herdr, the terminal workspace for AI agents |

---

# 1. Must do

## 1.1 Base: Command Line Tools and Homebrew

```bash
xcode-select --install          # [USER] confirms the dialog
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"   # [USER] types the Mac password
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Check: `brew doctor` has no errors, `clang --version` works.

## 1.2 Command line tools

```bash
brew install git gh fish bash jq yq ripgrep fd fzf bat eza zoxide atuin starship \
  tmux lazygit btop neovim poppler uv go deno coreutils terminal-notifier
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env
rustup component add rust-analyzer clippy rustfmt
```

`bash` from Homebrew matters: macOS ships bash 3.2, and the status line script needs bash 4+ (it runs with `#!/usr/bin/env bash`, so Homebrew's bash must come first in PATH, which `brew shellenv` does).

Check: `bash --version` shows 5.x, `rg`, `fd`, `eza`, `zoxide`, `atuin`, `starship`, `lazygit`, `nvim --version` (0.11 or newer) all run.

## 1.3 Shell: fish, starship, zoxide, atuin

```bash
echo /opt/homebrew/bin/fish | sudo tee -a /etc/shells   # [USER] password
chsh -s /opt/homebrew/bin/fish                           # [USER] password
mkdir -p ~/.config/fish
cp fish/config.fish ~/.config/fish/config.fish
cp starship.toml ~/.config/starship.toml
```

Then inside fish, install the plugin manager and Node:

```fish
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
fisher install jorgebucaran/nvm.fish
nvm install 24
set --universal nvm_default_version 24
corepack enable            # pnpm and yarn on demand
npm install -g pnpm
atuin import auto          # imports any existing shell history
```

What the config does: no greeting, starship prompt with transient prompt, `z <folder>` jumps to visited folders, Ctrl+R searches history with atuin (Up arrow stays fish's own), `ls` is `eza --icons`, `c` starts Claude Code, `clear` really clears in kitty.

Check: open a new fish, `node -v` prints v24, `z`, `atuin`, `starship` work, the prompt shows the folder and git branch.

## 1.4 Terminal: kitty and fonts

```bash
brew install --cask kitty font-jetbrains-mono-nerd-font
```

The terminal font is **Paper Mono** (open font license). It is not in Homebrew: download the OTF files from `https://github.com/paper-design/paper-mono` (folder `fonts`, or the latest release) and copy them to `~/Library/Fonts/`.

```bash
mkdir -p ~/.config/kitty
cp kitty/kitty.conf kitty/search.py kitty/scroll_mark.py ~/.config/kitty/
```

Then run `kitty +kitten themes` once and let the user pick a light and a dark theme (it can save `light-theme.auto.conf` and `dark-theme.auto.conf`, which then follow macOS appearance). On Linux the colors came from the wallpaper, so there is no theme file to copy.

What the config does: Paper Mono 16 with the Nerd Font for icons and Cyrillic, beam cursor with a trail, wide window margin, Ctrl+C copies a selection or interrupts, Ctrl+F searches the scrollback in a split, Ctrl+Shift+M and Ctrl+Shift+U widen and reset the side margins, fast smooth scrolling, Ctrl+plus, minus, 0 for font size, slight transparency. Left Option works as Alt inside the terminal; right Option still types special characters.

Check: kitty starts fish, icons in `eza --icons` render, Cyrillic text renders, Ctrl+F opens the search split.

## 1.5 Window manager: AeroSpace (the Hyprland replacement)

AeroSpace is a tiling window manager like Hyprland and i3. It needs no System Integrity Protection changes.

```bash
brew install --cask nikitabobko/tap/aerospace
mkdir -p ~/.config/aerospace
cp aerospace/aerospace.toml aerospace/mode-hint.sh ~/.config/aerospace/
chmod +x ~/.config/aerospace/mode-hint.sh
```

**[USER]** Open AeroSpace once, then allow it in System Settings, Privacy & Security, **Accessibility**. For Super+Shift+S screenshots also allow **Screen & System Audio Recording**. The first mode hint asks for notification permission (allow it).

Put the team chat app the user named on `s` in `[mode.apps.binding]` and in `mode-hint.sh`, for example `s = ['exec-and-forget open -a Slack', 'mode main']`.

Recommended macOS settings for AeroSpace (ask the user, both need a log out):

```bash
defaults write com.apple.spaces spans-displays -bool true    # turns off "Displays have separate Spaces"
defaults write com.apple.dock expose-group-apps -bool true   # Mission Control groups windows by app
killall Dock
```

### The key bindings

**Option is the Super key.** Counted from the space bar, Option sits where Super sits on a PC keyboard (two keys away), so the hand position stays the same, and Cmd keeps copy, paste, find and quit. Linux `CTRL + SUPER + X` is `Ctrl+Option+X` here, and `SUPER + ALT + X` is `Option+Cmd+X`.

| Linux | Mac | What it does |
|---|---|---|
| Super+Q | Option+Q | New terminal (kitty) |
| Super+B | Option+B | New browser window (Brave) |
| Super+D | Option+D | App launcher (Raycast, set in Raycast, see 1.6) |
| Super+E | Option+E | File manager (Finder, home folder) |
| Super+M | Option+M | System monitor (Activity Monitor) |
| Super+I | Option+I | Settings |
| Super+Alt+H | Option+Cmd+H | herdr in a floating terminal |
| Super+C | Option+C | Close window |
| Super+V | Option+V | Float or tile the window |
| Super+F | Option+F | Maximize, toggle (fills the workspace) |
| Super+Shift+F | Option+Shift+F | Real fullscreen (macOS native) |
| Super+H J K L | Option+H J K L | Focus left, down, up, right |
| Super+Shift+H J K L | Option+Shift+H J K L | Move window left, down, up, right |
| Ctrl+Super+H J K L | Ctrl+Option+H J K L | Resize by 40 px |
| Super+1 ... 0 | Option+1 ... 0 | Go to workspace 1 to 10 |
| Super+Shift+1 ... 0 | Option+Shift+1 ... 0 | Send window to workspace (focus stays) |
| Super+Tab | Option+Tab | Overview (Mission Control) |
| Super+Shift+V | Option+Shift+V | Clipboard history (Maccy, see 2.1) |
| Super+Shift+S | Option+Shift+S | Screen snip to clipboard |
| Super+Alt+L | Option+Cmd+L | Lock (screen off; macOS also has Ctrl+Cmd+Q) |
| Super+A, then a letter | Option+A, then a letter | **Apps mode** |
| Super+W, then a letter | Option+W, then a letter | **Websites mode** |
| | Option+Shift+; | AeroSpace service mode (Esc reloads the config, R resets the layout) |
| | Option+/ and Option+, | Tiles or accordion layout, switch orientation |

**Modes.** A mode is a state you enter with one shortcut. Inside it a single letter opens something and drops straight back out. Esc or Enter leaves without doing anything. While a mode is active, a notification lists its letters.

- Apps mode (Option+A): C Claude, V VS Code, O Obsidian, P 1Password, S the team chat.
- Websites mode (Option+W): G GitHub, M Gmail, Y YouTube, C Claude, H ChatGPT, I Gemini, T Translate.

To add an entry, add one line to the mode in `aerospace.toml` and the same letter to `mode-hint.sh`.

**Typing special letters.** Option+U then a, o or u types ä ö ü, and Option+S types ß. Those keys are left unbound for that reason. Option+E is taken (Finder), so é and similar accents need the right Option key inside kitty, or the character viewer.

**Not possible on macOS**, leave these out: Hyprland pseudo tiling (Super+P), pinning a window to all workspaces, the scratchpad workspace (Super+S), centering a floating window (Super+Alt+V), and the Linux-only desktop shell (sidebars, wallpaper picker, widgets, on-screen drawing).

**Known overlap:** herdr's own Ctrl+Alt+H J K L pane focus keys are taken by the resize binds above. Inside herdr use its prefix instead (Ctrl+A, then H J K L).

Check: Option+Q opens kitty, Option+C closes it, Option+V floats and unfloats, Option+F maximizes, Option+H J K L moves focus between two kitty windows, Option+2 and Option+Shift+2 work, Option+A shows the apps hint and C opens Claude, Option+W then G opens GitHub. **[USER]** has to press the keys: ask them to try the list and report what fails.

## 1.6 Launcher: Raycast

```bash
brew install --cask raycast
```

**[USER]** In Raycast settings set the hotkey to **Option+D** (the Linux Super+D launcher). Then in System Settings, Keyboard, Keyboard Shortcuts, Spotlight, turn off Cmd+Space for Spotlight, and in Input Sources set "Select the previous input source" to **Cmd+Space**. On Linux the layout switch was Alt+Space, and the PC Alt key sits where Cmd sits on a Mac keyboard (right next to the space bar).

## 1.7 Keyboard layouts

**[USER]** System Settings, Keyboard, Input Sources: add **ABC** (US), **Russian, PC** and **Kazakh**. Keep ABC first. On Linux the layouts were US international and Kazakh, switched with Alt+Space (now Cmd+Space, see 1.6).

Key repeat as on Linux (250 ms delay, fast repeat), needs a log out:

```bash
defaults write -g InitialKeyRepeat -int 15
defaults write -g KeyRepeat -int 2
defaults write -g ApplePressAndHoldEnabled -bool false   # holding a key repeats it instead of showing accents
```

## 1.8 Git and GitHub

```bash
git config --global user.name "<name from the user>"
git config --global user.email "<work email from the user>"
git config --global init.defaultBranch main
gh auth login          # [USER] logs in in the browser
gh auth setup-git      # git uses gh for GitHub credentials
npm install -g gh-axi  # token-efficient GitHub CLI for agents (see CLAUDE.md)
```

Commit habits the user follows (also in CLAUDE.md): one short line per commit message, no body, no attribution or Co-Authored-By lines, no dashes.

Check: `gh auth status` is logged in, `gh-axi` prints a dashboard inside any repo.

## 1.9 Docker

Use what the user answered. Without an answer, Colima:

```bash
brew install colima docker docker-compose docker-buildx
mkdir -p ~/.docker/cli-plugins
ln -sfn /opt/homebrew/opt/docker-compose/bin/docker-compose ~/.docker/cli-plugins/docker-compose
ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
colima start --cpu 4 --memory 8 --disk 60 --vm-type vz --vz-rosetta
brew services start colima        # starts at login
```

With Docker Desktop instead: `brew install --cask docker`, open it once, **[USER]** accepts the terms.

Check: `docker run --rm hello-world` and `docker compose version` work.

## 1.10 Neovim

```bash
cp -R nvim ~/.config/nvim
npm install -g @fsouza/prettierd prettier
uv tool install ruff
brew install lua cppcheck
nvim    # first start installs vim-plug and every plugin, then restart nvim
```

What it is: vim-plug, nvim-tree, fzf-lua, barbar tabs, lualine, which-key, treesitter, gitsigns, conform (prettierd, prettier) and nvim-lint, nvim-cmp with LuaSnip, trouble, FTerm floating terminal, auto-session, autosave after one second, PicVim images and PDFs in the editor (kitty graphics plus poppler), several themes with a saved choice. Keymaps are in `lua/config/mappings.lua`, LSP keys in `lua/plugins/lsp.lua` (gd, gD, gi, gy, K, leader rr, rn, ca, ih, [d ]d [e ]e).

LSPs: Mason installs `ts_ls`, `cssls`, `html`, `tailwindcss`, `emmet_language_server`, `eslint`, `jsonls`, `yamlls`, `taplo`, `dockerls`, `pyright`, `lua_ls`, `bashls`, `marksman` on first start. `rust_analyzer` comes from rustup (1.2), not Mason, on purpose.

Mac notes:
- The `ii` and `mono` themes and `config/daynight.lua` read a palette file written by the Linux desktop shell. On the Mac that file does not exist, so they fall back quietly and the saved theme (solarized-osaka) loads. Optional: make `daynight.lua` follow macOS appearance (`defaults read -g AppleInterfaceStyle` prints `Dark` in dark mode) instead of the missing palette.
- `<leader>u` opens the URL under the cursor with `vim.ui.open`, which works on macOS.

Check: `nvim` opens with no errors, `:checkhealth` has no red errors for lsp, treesitter, conform and mason, a `.ts` file shows diagnostics and `K` hover, `:Mason` lists the servers as installed.

## 1.11 Claude Code

Install and log in:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude      # [USER] logs in with the account the company provides
```

Copy the config:

```bash
mkdir -p ~/.claude/hooks ~/.claude/skills ~/dev
cp claude/CLAUDE.md claude/settings.json claude/statusline.sh ~/.claude/
cp claude/hooks/notify.sh ~/.claude/hooks/
chmod +x ~/.claude/statusline.sh ~/.claude/hooks/notify.sh
cp -R claude-mods ~/dev/claude-mods
cp -R skills/caveman skills/mgpro skills/kwx-designer ~/.claude/skills/
```

The mods must live at exactly `~/dev/claude-mods`: `settings.json` loads them from there through `CLAUDE_CODE_PLUGIN_DIRS`, and the stats card runs `~/dev/claude-mods/stats-card/scripts/stats.mjs`. Make `~/dev/claude-mods` a git repo with a first commit so later edits are tracked (`git init && git add -A && git commit -m "Claude Code mods"`), and ask the user before pushing it anywhere.

What `settings.json` sets: Opus as the model, effort medium by default and high for Opus 5.5, fullscreen TUI, hold-to-talk voice, auto theme, the status line, the Stop notification hook, the four mods, the LSP plugins and the ponytail plugin.

The status line reads: fast-mode bolt, the last three folders, branch with `*` when dirty, `wt:<name>` in a worktree, context use `C42%`, then the 5 hour and 7 day limits as `12%,2015,2h00` (used, reset time, time left), green under 50, yellow under 80, red above.

The mods (they draw inside Claude Code's TUI):
- **clawd**: the pixel Clawd mascot above the prompt, with a strip of this turn's tool calls and the `git diff` line counts. `/clawd` hides and shows it.
- **model-buttons**: clickable model and effort pills under the footer, with a dropdown and a slider.
- **stats-card**: the desktop app's usage card on a fresh session (`/stats-card`).
- **savvy-progress**: a progress bar for multi-agent work and an `/agents-info` pane with a card per subagent.

They use Claude Code's mod engine. Check them with `claude plugin test ~/dev/claude-mods/<name>` for each of the four. If the installed Claude Code does not load them, report it and leave them out. Do not patch Claude Code.

### Plugins

```bash
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
claude plugin install typescript-lsp@claude-plugins-official
claude plugin install pyright-lsp@claude-plugins-official
claude plugin install lua-lsp@claude-plugins-official
claude plugin install rust-analyzer-lsp@claude-plugins-official
npm install -g typescript typescript-language-server pyright
brew install lua-language-server
```

**ponytail** makes the agent work like a lazy senior developer: the smallest complete change, no code nobody asked for, a one-line note of what was skipped. Its modes: `/ponytail lite|full|ultra`, "stop ponytail" to turn it off.

The LSP plugins need their servers on PATH: the npm and brew lines above, plus rust-analyzer from 1.2.

### Skills

```bash
npx -y skills add kunchenguid/lavish-axi -g          # lavish: visual HTML pages for plans, comparisons, diagrams
npx -y skills add vercel-labs/skills --skill find-skills -g
npx -y skills add leonxlnx/taste-skill -g            # design-taste-frontend: anti-template frontend design
curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh
uv tool install graphifyy && graphify install          # /graphify: codebase to knowledge graph
```

Pick Claude Code as the target when `skills add` asks. `caveman` was copied above (it holds the user's own edits, so do not reinstall it from upstream). no-mistakes is a local git gate (review, test, lint, push, PR, CI) with its own skill. Install its skill too if the installer does not; its README says how.

Do not install the user's personal skills (language learning, logo and their own Linux apps). They are not in this folder on purpose.

Check, in a fresh `claude` session:
- The status line shows folder, branch and percentages.
- `/` lists caveman, lavish, find-skills, design-taste-frontend, graphify, no-mistakes and the ponytail commands.
- `/plugin` shows ponytail and the four LSP plugins enabled.
- The mods draw (Clawd above the prompt, pills under the footer).
- When a turn ends, a notification with a sound appears.

---

# 2. Comfort

## 2.1 Clipboard history: Maccy

```bash
brew install --cask maccy
```

**[USER]** Maccy settings: hotkey **Option+Shift+V** (Linux Super+Shift+V), launch at login.

## 2.2 herdr

A terminal workspace manager for running several AI agents side by side, opened with Option+Cmd+H as a floating window.

```bash
brew install herdr
mkdir -p ~/.config/herdr
cp herdr/config.toml ~/.config/herdr/config.toml
```

Then install herdr's Claude Code integration (see `herdr --help` and its docs at herdr.dev). It adds its own SessionStart hook to `~/.claude/settings.json`, so let herdr do that rather than writing it by hand. The config uses prefix Ctrl+A with H J K L, P N for tabs, C new tab, V and minus for splits, Z zoom, X close, the kanagawa theme switching to catppuccin-latte in light mode, fish as the shell, kitty graphics.

Check: Option+Cmd+H opens herdr floating, `claude` inside a pane shows up in herdr's agent panel.

## 2.3 macOS comfort settings

Ask before applying; some need `killall Dock` or a log out.

```bash
defaults write com.apple.dock autohide -bool true                 # Dock hides
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock mru-spaces -bool false              # Spaces keep their order
defaults write -g NSWindowShouldDragOnGesture -bool true          # Ctrl+Cmd+drag moves a window from anywhere (Linux Super+drag)
defaults write -g AppleShowAllExtensions -bool true
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write com.apple.screencapture location ~/Pictures/Screenshots && mkdir -p ~/Pictures/Screenshots
killall Dock Finder
```

Trackpad: tap to click and natural scrolling on (as on Linux), in System Settings, Trackpad. **[USER]**

## 2.4 tmux

```bash
mkdir -p ~/.config/tmux && cp tmux/tmux.conf ~/.config/tmux/tmux.conf
```

Mouse on, windows and panes start at 1, `|` and `-` split in the current folder, 50,000 lines of history.

---

# 3. Useful

Install when the user wants them; ask in one go.

```bash
brew install --cask brave-browser visual-studio-code obsidian 1password claude
```

- **Brave** is the browser on Option+B. Make it the default browser if the user agrees (**[USER]** confirms the macOS dialog).
- **Claude desktop app**, **VS Code**, **Obsidian**, **1Password** are the apps mode entries.
- **Python**: `uv` is the tool for Python projects and tools (`uv tool install`, `uv run`).
- **Rust, Go, Deno** are installed in 1.2.
- **lazygit** (`lazygit` in a repo) and **btop** are installed in 1.2.
- **Android**: only when the team builds mobile apps. Then install Android Studio (`brew install --cask android-studio`) and create exactly one emulator named `universal` (Pixel 6, arm64 image, hardware keyboard on), as CLAUDE.md says.

---

# 4. Final report

End with a short report to the user:

1. What is installed and checked.
2. What was skipped, and why (blocked by device management, failed check, not wanted).
3. Everything still marked **[USER]** that is not done yet, as a list of exact clicks.
4. A reminder that this folder can be deleted, since every file was copied.
