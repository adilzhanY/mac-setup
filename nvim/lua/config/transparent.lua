-- Universal transparent background.
--
-- kitty runs at `background_opacity 0.6` (+ blur) and Hyprland blurs behind it,
-- so the terminal is see-through. That transparency only shows through Neovim
-- cells that have NO background colour. Most colorschemes paint a solid Normal
-- background, which hides it. This autocmd clears the "page background" groups
-- after ANY colorscheme loads, so every theme gets the same transparent look as
-- kitty/Hyprland, including themes with no transparency option of their own
-- (solarized-osaka, pywal16, and the custom `uylag`).
--
-- Only background-fill groups are cleared. Functional highlights that NEED a
-- background to be usable (Visual, Search, CursorLine, Pmenu/completion menu)
-- are left untouched on purpose.

-- Groups whose background should become transparent. Using `guibg=NONE
-- ctermbg=NONE` (instead of nvim_set_hl) keeps each group's existing foreground.
local transparent_groups = {
  -- Core editor surfaces
  "Normal", "NormalNC", "EndOfBuffer", "NonText", "SignColumn", "FoldColumn",
  "LineNr", "LineNrAbove", "LineNrBelow", "CursorLineNr",
  "WinSeparator", "VertSplit",
  -- Floating windows (LSP hover, which-key, fzf-lua, diagnostics, etc.)
  "NormalFloat", "FloatBorder", "FloatTitle",
  -- nvim-tree file explorer
  "NvimTreeNormal", "NvimTreeNormalNC", "NvimTreeEndOfBuffer",
  "NvimTreeWinSeparator", "NvimTreeVertSplit", "NvimTreeOpenedFile",
  -- Telescope / which-key floats (harmless if the group doesn't exist)
  "TelescopeNormal", "TelescopeBorder", "WhichKeyFloat", "WhichKeyNormal", "WhichKeyBorder",
  -- Winbar, the strip above a split
  "WinBar", "WinBarNC",
  -- barbar tabline: the empty strip beside the tabs, and the nvim-tree offset
  -- block. The ACTIVE tab (BufferCurrent*) and the visible-but-not-current
  -- tabs (BufferVisible*) keep their background on purpose, since that shade
  -- is the only thing marking which buffer you are on. `ii` keeps them too.
  "BufferTabpageFill", "BufferTabpages", "BufferOffset",
  -- sticky context header at the top of a long function
  "TreesitterContext", "TreesitterContextLineNumber",
}

-- Whole families of groups, matched by name pattern. barbar alone defines
-- around fourteen BufferInactive* groups and Neovim four DiagnosticVirtualText
-- ones, so listing each by hand would go stale the moment either adds another.
local transparent_patterns = {
  "^BufferInactive",        -- barbar: the tabs you are not on
  "^DiagnosticVirtualText", -- the inline error/warning text at end of line
}

local function matches_pattern(name)
  for _, pattern in ipairs(transparent_patterns) do
    if name:match(pattern) then return true end
  end
  return false
end

local function make_transparent()
  for _, group in ipairs(transparent_groups) do
    -- pcall so a theme missing one of these groups can't break the others.
    pcall(vim.cmd, ("highlight %s guibg=NONE ctermbg=NONE"):format(group))
  end

  -- Linked groups are skipped: clearing a background on a link would sever it
  -- from whatever it points at. Groups with no background of their own are
  -- skipped too, so this does no work on a theme that is already transparent.
  for name, spec in pairs(vim.api.nvim_get_hl(0, {})) do
    if not spec.link and spec.bg and matches_pattern(name) then
      pcall(vim.cmd, ("highlight %s guibg=NONE ctermbg=NONE"):format(name))
    end
  end
end

vim.api.nvim_create_autocmd("ColorScheme", {
  group = vim.api.nvim_create_augroup("transparent_background", { clear = true }),
  pattern = "*",
  callback = make_transparent,
})

-- Apply immediately too, in case a colorscheme was set before this loaded.
make_transparent()
