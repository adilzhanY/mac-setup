require("fzf-lua").setup{
	file_icon_padding = ' ',

-- Why the file list is built with ripgrep instead of fd.
--
-- ~/.config/git/ignore is git's GLOBAL ignore file, and it lists CLAUDE.md,
-- AGENTS.md, INFO.md and .claude/. That file keeps those out of every repo you
-- commit to, which is what you want. The side effect is that every file-listing
-- tool that honours gitignore also hides them, so <leader>f could never find
-- CLAUDE.md.
--
-- ripgrep's --no-ignore-global drops exactly that one layer: the global file
-- stops applying, while each project's own .gitignore still does, so
-- node_modules, dist and coverage stay out of the list. fd 10.5 has no
-- equivalent; its only comparable switch, --no-ignore-vcs, throws away the
-- project .gitignore too and floods the picker with node_modules.
--
-- fzf-lua reaches for fd first whenever it is installed, so naming the command
-- outright is the only way to choose rg. --hidden is deliberately absent: the
-- `hidden` option adds it, and alt-h toggles it from inside the picker.
files = {
	cmd = [[rg --color=never --files --no-ignore-global -g "!.git/" -g "!.jj/"]],
	-- alt-i, "also show ignored files", must NOT be spelled --no-ignore here.
	-- fzf-lua turns that toggle off with a plain gsub of the flag text, and
	-- "--no-ignore" is a prefix of "--no-ignore-global", so switching it back off
	-- chewed the command down to "rg --files-global", which rg rejects.
	-- --no-ignore-vcs means the same thing for this picker and shares no prefix.
	toggle_ignore_flag = "--no-ignore-vcs",
},

-- Same layer removed for content search, so <leader>g and <leader>G can grep
-- INSIDE CLAUDE.md as well. -e must stay last, it introduces the pattern.
grep = {
	rg_opts = "--column --line-number --no-heading --color=always --smart-case "
		.. "--max-columns=4096 --no-ignore-global -e",
},
--   -- MISC GLOBAL SETUP OPTIONS, SEE BELOW
--   -- fzf_bin = ...,
--   winopts = { ...  },     -- UI Options
--   keymap = { ...  },      -- Neovim keymaps / fzf binds
--   actions = { ...  },     -- Fzf "accept" binds
--   fzf_opts = { ...  },    -- Fzf CLI flags
--   fzf_colors = { ...  },  -- Fzf `--color` specification
--   hls = { ...  },         -- Highlights
--   previewers = { ...  },  -- Previewers options
--   -- SPECIFIC COMMAND/PICKER OPTIONS, SEE BELOW
--   -- files = { ... },

keymap = {
    -- Below are the default binds, setting any value in these tables will override
    -- the defaults, to inherit from the defaults change [1] from `false` to `true`
    builtin = {
      -- neovim `:tmap` mappings for the fzf win
      -- true,        -- uncomment to inherit all the below in your custom config
      ["<M-Esc>"]     = "hide",     -- hide fzf-lua, `:FzfLua resume` to continue
      ["<F1>"]        = "toggle-help",
      ["<F2>"]        = "toggle-fullscreen",
      -- Only valid with the 'builtin' previewer
      ["<F3>"]        = "toggle-preview-wrap",
      ["<F4>"]        = "toggle-preview",
      -- Rotate preview clockwise/counter-clockwise
      ["<F5>"]        = "toggle-preview-ccw",
      ["<F6>"]        = "toggle-preview-cw",
      -- `ts-ctx` binds require `nvim-treesitter-context`
      ["<F7>"]        = "toggle-preview-ts-ctx",
      ["<F8>"]        = "preview-ts-ctx-dec",
      ["<F9>"]        = "preview-ts-ctx-inc",
      ["<S-Left>"]    = "preview-reset",
      ["<S-down>"]    = "preview-page-down",
      ["<S-up>"]      = "preview-page-up",
      ["<M-S-down>"]  = "preview-down",
      ["<M-S-up>"]    = "preview-up",
    },
    fzf = {
      -- fzf '--bind=' options
      -- true,        -- uncomment to inherit all the below in your custom config
      ["ctrl-z"]      = "abort",
      ["ctrl-u"]      = "unix-line-discard",
      ["ctrl-f"]      = "half-page-down",
      ["ctrl-b"]      = "half-page-up",
      ["ctrl-a"]      = "beginning-of-line",
      ["ctrl-e"]      = "end-of-line",
      ["alt-a"]       = "toggle-all",
      ["alt-g"]       = "first",
      ["alt-G"]       = "last",
      -- Only valid with fzf previewers (bat/cat/git/etc)
      ["f3"]          = "toggle-preview-wrap",
      ["f4"]          = "toggle-preview",
      ["shift-down"]  = "preview-page-down",
      ["shift-up"]    = "preview-page-up",
    },
},
}