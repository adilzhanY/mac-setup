-- "ii" colorscheme: follows the end-4 (Quickshell) wallpaper-generated
-- Material You palette, including light/dark, and live-reloads when the
-- palette file changes (wallpaper switch or dark mode toggle).

local palette = require("ii.palette")

local M = {}

-- ---------------------------------------------------------------- color math

local function rgb(hex)
	return tonumber(hex:sub(2, 3), 16), tonumber(hex:sub(4, 5), 16), tonumber(hex:sub(6, 7), 16)
end

local function is_dark(hex)
	local r, g, b = rgb(hex)
	return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.5
end

-- mix `a` toward `b` by t (0 = a, 1 = b)
local function blend(a, b, t)
	local ar, ag, ab = rgb(a)
	local br, bg, bb = rgb(b)
	return string.format("#%02X%02X%02X",
		math.floor(ar + (br - ar) * t + 0.5),
		math.floor(ag + (bg - ag) * t + 0.5),
		math.floor(ab + (bb - ab) * t + 0.5))
end

-- nvim renders inside kitty, whose background is term0. If the terminal is
-- forced dark while the shell palette went light (forceDarkMode), the M3
-- roles would be unreadable, so rebuild the critical roles from term colors.
local function effective(pal)
	local c = vim.tbl_extend("force", {}, pal.colors)
	local dark = pal.darkmode
	if is_dark(c.term0) ~= dark then
		dark = is_dark(c.term0)
		local base, on = c.term0, c.term15
		c.surface, c.onSurface = base, on
		c.background, c.onBackground = base, on
		c.onSurfaceVariant, c.outline = c.term7, c.term8
		c.outlineVariant = blend(c.term8, base, 0.5)
		c.surfaceContainerLowest = blend(base, on, 0.02)
		c.surfaceContainerLow = blend(base, on, 0.05)
		c.surfaceContainer = blend(base, on, 0.08)
		c.surfaceContainerHigh = blend(base, on, 0.12)
		c.surfaceContainerHighest = blend(base, on, 0.16)
		local accents = { primary = "term4", secondary = "term6", tertiary = "term5",
			error = "term1", success = "term2" }
		for role, term in pairs(accents) do
			local up = role:sub(1, 1):upper() .. role:sub(2)
			c[role], c["on" .. up] = c[term], base
			c[role .. "Container"], c["on" .. up .. "Container"] = blend(c[term], base, 0.6), on
		end
	end
	return c, dark
end

-- ---------------------------------------------------------------- highlights

local function highlights(c)
	local h = {}

	-- editor chrome (transparent.lua strips bgs of the page groups afterwards;
	-- they are still set here so the scheme works outside kitty too)
	h.Normal = { fg = c.onSurface, bg = c.surface }
	h.NormalNC = { fg = c.onSurface, bg = c.surface }
	h.NormalFloat = { fg = c.onSurface, bg = c.surfaceContainerLow }
	h.FloatBorder = { fg = c.outline }
	h.FloatTitle = { fg = c.primary, bold = true }
	h.WinBar = { fg = c.onSurface, bold = true }
	h.WinBarNC = { fg = c.outline }
	h.Cursor = { reverse = true }
	h.CursorLine = { bg = c.surfaceContainer }
	h.CursorColumn = { bg = c.surfaceContainer }
	h.CursorLineNr = { fg = c.primary, bold = true }
	h.LineNr = { fg = c.outline }
	h.SignColumn = {}
	h.FoldColumn = { fg = c.outline }
	h.ColorColumn = { bg = c.surfaceContainerLow }
	h.WinSeparator = { fg = c.outlineVariant }
	h.VertSplit = { link = "WinSeparator" }
	h.StatusLine = { fg = c.onSurface, bg = c.surfaceContainer }
	h.StatusLineNC = { fg = c.outline, bg = c.surfaceContainerLow }
	h.TabLine = { fg = c.onSurfaceVariant, bg = c.surfaceContainerLow }
	h.TabLineFill = {}
	h.TabLineSel = { fg = c.onSurface, bg = c.surfaceContainerHigh, bold = true }
	h.Visual = { bg = c.secondaryContainer }
	h.VisualNOS = { link = "Visual" }
	h.Search = { fg = c.onTertiaryContainer, bg = c.tertiaryContainer }
	h.IncSearch = { fg = c.onPrimary, bg = c.primary, bold = true }
	h.CurSearch = { link = "IncSearch" }
	h.Substitute = { link = "IncSearch" }
	h.MatchParen = { fg = c.primary, bg = c.surfaceContainerHighest, bold = true }
	h.Folded = { fg = c.onSurfaceVariant, bg = c.surfaceContainerLow, italic = true }
	h.NonText = { fg = c.outlineVariant }
	h.Whitespace = { fg = c.outlineVariant }
	h.SpecialKey = { fg = c.outlineVariant }
	h.EndOfBuffer = { fg = c.outlineVariant }
	h.Conceal = { fg = c.outline }
	h.Directory = { fg = c.primary }
	h.Title = { fg = c.primary, bold = true }
	h.ErrorMsg = { fg = c.error, bold = true }
	h.WarningMsg = { fg = c.tertiary }
	h.ModeMsg = { fg = c.primary, bold = true }
	h.MoreMsg = { fg = c.primary, bold = true }
	h.Question = { fg = c.primary }
	h.QuickFixLine = { bg = c.secondaryContainer }
	h.WildMenu = { fg = c.onPrimary, bg = c.primary }

	-- syntax (legacy groups; treesitter/@lsp link into these or get their own)
	h.Comment = { fg = c.outline, italic = true }
	h.SpecialComment = { link = "Comment" }
	h.Keyword = { fg = c.primary, bold = true }
	h.Statement = { link = "Keyword" }
	h.Conditional = { link = "Keyword" }
	h.Repeat = { link = "Keyword" }
	h.Include = { link = "Keyword" }
	h.Label = { link = "Keyword" }
	h.Exception = { fg = c.error, bold = true }
	h.Function = { fg = c.tertiary }
	h.String = { fg = c.success }
	h.Character = { link = "String" }
	h.Type = { fg = c.secondary, bold = true }
	h.StorageClass = { fg = c.secondary }
	h.Structure = { fg = c.secondary }
	h.Typedef = { fg = c.secondary }
	h.Constant = { fg = c.term5 }
	h.Number = { fg = c.term5 }
	h.Boolean = { fg = c.term5 }
	h.Float = { fg = c.term5 }
	h.PreProc = { fg = c.term1 }
	h.Define = { link = "PreProc" }
	h.Macro = { link = "PreProc" }
	h.PreCondit = { link = "PreProc" }
	h.Operator = { fg = c.onSurfaceVariant }
	h.Delimiter = { fg = c.onSurfaceVariant }
	h.Identifier = { fg = c.onSurface }
	h.Special = { fg = c.term2 }
	h.SpecialChar = { fg = c.term2 }
	h.Debug = { fg = c.term2 }
	h.Tag = { fg = c.primary }
	h.Underlined = { fg = c.primary, underline = true }
	h.Ignore = { fg = c.outlineVariant }
	h.Error = { fg = c.error, bold = true }
	h.Todo = { fg = c.onTertiary, bg = c.tertiary, bold = true }
	h.Added = { fg = c.success }
	h.Changed = { fg = c.primary }
	h.Removed = { fg = c.error }
	h.healthSuccess = { fg = c.success, bold = true }
	h.healthWarning = { fg = c.tertiary, bold = true }
	h.healthError = { fg = c.error, bold = true }

	-- treesitter captures
	h["@comment"] = { link = "Comment" }
	h["@comment.todo"] = { link = "Todo" }
	h["@comment.note"] = { fg = c.onPrimaryContainer, bg = c.primaryContainer, bold = true }
	h["@comment.warning"] = { fg = c.onTertiaryContainer, bg = c.tertiaryContainer, bold = true }
	h["@comment.error"] = { fg = c.onErrorContainer, bg = c.errorContainer, bold = true }
	h["@keyword"] = { link = "Keyword" }
	h["@keyword.function"] = { link = "Keyword" }
	h["@keyword.return"] = { link = "Keyword" }
	h["@keyword.operator"] = { link = "Keyword" }
	h["@keyword.conditional"] = { link = "Keyword" }
	h["@keyword.repeat"] = { link = "Keyword" }
	h["@keyword.import"] = { link = "Keyword" }
	h["@keyword.directive"] = { link = "PreProc" }
	h["@keyword.exception"] = { link = "Exception" }
	h["@function"] = { link = "Function" }
	h["@function.builtin"] = { fg = c.tertiary, italic = true }
	h["@function.method"] = { link = "Function" }
	h["@function.macro"] = { link = "PreProc" }
	h["@method"] = { link = "Function" }
	h["@constructor"] = { link = "Function" }
	h["@string"] = { link = "String" }
	h["@string.escape"] = { fg = c.term2 }
	h["@string.special"] = { fg = c.term2 }
	h["@string.regexp"] = { fg = c.term2 }
	h["@character"] = { link = "String" }
	h["@type"] = { link = "Type" }
	h["@type.builtin"] = { fg = c.secondary, bold = true, italic = true }
	h["@type.definition"] = { link = "Type" }
	h["@constant"] = { link = "Constant" }
	h["@constant.builtin"] = { fg = c.term5, bold = true }
	h["@constant.macro"] = { link = "PreProc" }
	h["@number"] = { link = "Number" }
	h["@boolean"] = { link = "Boolean" }
	h["@number.float"] = { link = "Float" }
	h["@operator"] = { link = "Operator" }
	h["@punctuation.delimiter"] = { link = "Delimiter" }
	h["@punctuation.bracket"] = { link = "Delimiter" }
	h["@punctuation.special"] = { fg = c.term2 }
	h["@variable"] = { fg = c.onSurface }
	h["@variable.builtin"] = { fg = c.tertiary, italic = true }
	h["@variable.parameter"] = { fg = c.onSurfaceVariant, italic = true }
	h["@variable.member"] = { fg = c.term6 }
	h["@field"] = { fg = c.term6 }
	h["@property"] = { fg = c.term6 }
	h["@attribute"] = { fg = c.term5 }
	h["@module"] = { fg = c.secondary }
	h["@namespace"] = { fg = c.secondary }
	h["@label"] = { link = "Keyword" }
	h["@tag"] = { link = "Tag" }
	h["@tag.attribute"] = { fg = c.term5 }
	h["@tag.delimiter"] = { link = "Delimiter" }
	h["@markup.heading"] = { fg = c.primary, bold = true }
	h["@markup.strong"] = { bold = true }
	h["@markup.italic"] = { italic = true }
	h["@markup.strikethrough"] = { strikethrough = true }
	h["@markup.underline"] = { underline = true }
	h["@markup.link"] = { fg = c.primary }
	h["@markup.link.url"] = { fg = c.primary, underline = true }
	h["@markup.link.label"] = { fg = c.secondary }
	h["@markup.raw"] = { fg = c.success }
	h["@markup.list"] = { fg = c.primary }
	h["@markup.quote"] = { fg = c.onSurfaceVariant, italic = true }
	h["@diff.plus"] = { link = "Added" }
	h["@diff.minus"] = { link = "Removed" }
	h["@diff.delta"] = { link = "Changed" }

	-- markdown headings (render-markdown style groups, harmless if unused)
	for i = 1, 6 do
		h["RenderMarkdownH" .. i] = { fg = c.primary, bold = true }
	end

	-- diagnostics / LSP
	h.DiagnosticError = { fg = c.error }
	h.DiagnosticWarn = { fg = c.tertiary }
	h.DiagnosticInfo = { fg = c.primary }
	h.DiagnosticHint = { fg = c.onSurfaceVariant }
	h.DiagnosticOk = { fg = c.success }
	h.DiagnosticVirtualTextError = { fg = c.error, italic = true }
	h.DiagnosticVirtualTextWarn = { fg = c.tertiary, italic = true }
	h.DiagnosticVirtualTextInfo = { fg = c.primary, italic = true }
	h.DiagnosticVirtualTextHint = { fg = c.onSurfaceVariant, italic = true }
	h.DiagnosticUnderlineError = { undercurl = true, sp = c.error }
	h.DiagnosticUnderlineWarn = { undercurl = true, sp = c.tertiary }
	h.DiagnosticUnderlineInfo = { undercurl = true, sp = c.primary }
	h.DiagnosticUnderlineHint = { undercurl = true, sp = c.onSurfaceVariant }
	h.DiagnosticSignError = { fg = c.error }
	h.DiagnosticSignWarn = { fg = c.tertiary }
	h.DiagnosticSignInfo = { fg = c.primary }
	h.DiagnosticSignHint = { fg = c.onSurfaceVariant }
	h.LspReferenceText = { bg = c.surfaceContainerHigh }
	h.LspReferenceRead = { bg = c.surfaceContainerHigh }
	h.LspReferenceWrite = { bg = c.surfaceContainerHigh }
	h.LspInlayHint = { fg = c.outline, italic = true }
	h.LspSignatureActiveParameter = { bg = c.secondaryContainer, bold = true }

	-- diff / git
	h.DiffAdd = { bg = c.successContainer }
	h.DiffChange = { bg = c.surfaceContainerHigh }
	h.DiffDelete = { fg = c.outline, bg = c.errorContainer }
	h.DiffText = { bg = c.secondaryContainer, bold = true }
	h.GitSignsAdd = { fg = c.success }
	h.GitSignsChange = { fg = c.primary }
	h.GitSignsDelete = { fg = c.error }
	h.GitSignsCurrentLineBlame = { fg = c.outline, italic = true }

	-- popup menu / nvim-cmp (kept opaque on purpose, see transparent.lua)
	h.Pmenu = { fg = c.onSurface, bg = c.surfaceContainerHigh }
	h.PmenuSel = { fg = c.onSecondaryContainer, bg = c.secondaryContainer, bold = true }
	h.PmenuSbar = { bg = c.surfaceContainerHigh }
	h.PmenuThumb = { bg = c.outline }
	h.CmpItemAbbr = { fg = c.onSurface }
	h.CmpItemAbbrDeprecated = { fg = c.outline, strikethrough = true }
	h.CmpItemAbbrMatch = { fg = c.primary, bold = true }
	h.CmpItemAbbrMatchFuzzy = { fg = c.primary }
	h.CmpItemMenu = { fg = c.outline, italic = true }
	h.CmpItemKindFunction = { fg = c.tertiary }
	h.CmpItemKindMethod = { fg = c.tertiary }
	h.CmpItemKindConstructor = { fg = c.tertiary }
	h.CmpItemKindVariable = { fg = c.term6 }
	h.CmpItemKindField = { fg = c.term6 }
	h.CmpItemKindProperty = { fg = c.term6 }
	h.CmpItemKindKeyword = { fg = c.primary }
	h.CmpItemKindOperator = { fg = c.primary }
	h.CmpItemKindClass = { fg = c.secondary }
	h.CmpItemKindInterface = { fg = c.secondary }
	h.CmpItemKindStruct = { fg = c.secondary }
	h.CmpItemKindModule = { fg = c.secondary }
	h.CmpItemKindText = { fg = c.onSurfaceVariant }
	h.CmpItemKindSnippet = { fg = c.success }
	h.CmpItemKindConstant = { fg = c.term5 }
	h.CmpItemKindValue = { fg = c.term5 }
	h.CmpItemKindEnum = { fg = c.term5 }
	h.CmpItemKindEnumMember = { fg = c.term5 }
	h.CmpItemKindUnit = { fg = c.term5 }
	h.CmpItemKindFile = { fg = c.primary }
	h.CmpItemKindFolder = { fg = c.primary }
	h.CmpItemKindReference = { fg = c.onSurfaceVariant }

	-- indent-blankline v3 (always defined so ibl's ColorScheme hook never fails)
	h.IblIndent = { fg = c.outlineVariant }
	h.IblWhitespace = { fg = c.outlineVariant }
	h.IblScope = { fg = c.primary }

	-- barbar
	local barbar = {
		Current = { fg = c.onSurface, bg = c.surfaceContainerHigh, accent = c.primary, bold = true },
		Visible = { fg = c.onSurfaceVariant, bg = c.surfaceContainerLow, accent = c.primary },
		Alternate = { fg = c.onSurfaceVariant, bg = c.surfaceContainerLow, accent = c.primary },
		Inactive = { fg = c.outline, bg = nil, accent = c.outlineVariant },
	}
	for state, s in pairs(barbar) do
		h["Buffer" .. state] = { fg = s.fg, bg = s.bg, bold = s.bold }
		h["Buffer" .. state .. "Mod"] = { fg = c.tertiary, bg = s.bg, bold = s.bold }
		h["Buffer" .. state .. "Sign"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "SignRight"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "Index"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "Icon"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "Btn"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "Pin"] = { fg = s.accent, bg = s.bg }
		h["Buffer" .. state .. "Target"] = { fg = c.error, bg = s.bg, bold = true }
		h["Buffer" .. state .. "ERROR"] = { fg = c.error, bg = s.bg }
		h["Buffer" .. state .. "WARN"] = { fg = c.tertiary, bg = s.bg }
		h["Buffer" .. state .. "INFO"] = { fg = c.primary, bg = s.bg }
		h["Buffer" .. state .. "HINT"] = { fg = c.outline, bg = s.bg }
	end
	h.BufferTabpageFill = {}
	h.BufferTabpages = { fg = c.primary, bold = true }

	-- nvim-tree
	h.NvimTreeNormal = { fg = c.onSurface }
	h.NvimTreeNormalNC = { fg = c.onSurface }
	h.NvimTreeRootFolder = { fg = c.tertiary, bold = true }
	h.NvimTreeFolderIcon = { fg = c.primary }
	h.NvimTreeFolderName = { fg = c.primary }
	h.NvimTreeOpenedFolderName = { fg = c.primary, bold = true }
	h.NvimTreeEmptyFolderName = { fg = c.primary }
	h.NvimTreeSpecialFile = { fg = c.tertiary, underline = true }
	h.NvimTreeExecFile = { fg = c.success }
	h.NvimTreeSymlink = { fg = c.term6 }
	h.NvimTreeImageFile = { fg = c.term5 }
	h.NvimTreeGitNew = { fg = c.success }
	h.NvimTreeGitDirty = { fg = c.primary }
	h.NvimTreeGitStaged = { fg = c.success }
	h.NvimTreeGitDeleted = { fg = c.error }
	h.NvimTreeGitRenamed = { fg = c.tertiary }
	h.NvimTreeIndentMarker = { fg = c.outlineVariant }
	h.NvimTreeWinSeparator = { fg = c.outlineVariant }

	-- telescope-style groups (fzf-lua reuses these + NormalFloat/FloatBorder)
	h.TelescopeNormal = { fg = c.onSurface }
	h.TelescopeBorder = { fg = c.outline }
	h.TelescopePromptBorder = { fg = c.outline }
	h.TelescopeSelection = { bg = c.surfaceContainerHigh }
	h.TelescopeSelectionCaret = { fg = c.primary, bg = c.surfaceContainerHigh }
	h.TelescopeMatching = { fg = c.primary, bold = true }
	h.TelescopePromptPrefix = { fg = c.primary }
	h.TelescopePromptTitle = { fg = c.onPrimary, bg = c.primary, bold = true }
	h.TelescopePreviewTitle = { fg = c.onPrimary, bg = c.primary, bold = true }
	h.TelescopeResultsTitle = { fg = c.onPrimary, bg = c.primary, bold = true }
	h.FzfLuaTitle = { fg = c.onPrimary, bg = c.primary, bold = true }
	h.FzfLuaHeaderText = { fg = c.tertiary }
	h.FzfLuaHeaderBind = { fg = c.primary }

	-- which-key
	h.WhichKey = { fg = c.primary, bold = true }
	h.WhichKeyGroup = { fg = c.tertiary }
	h.WhichKeyDesc = { fg = c.onSurface }
	h.WhichKeySeparator = { fg = c.outline }
	h.WhichKeyFloat = { bg = c.surfaceContainerLow }
	h.WhichKeyBorder = { fg = c.outline }

	-- alpha (start screen)
	h.AlphaHeader = { fg = c.primary }
	h.AlphaButtons = { fg = c.onSurface }
	h.AlphaShortcut = { fg = c.tertiary, bold = true }
	h.AlphaFooter = { fg = c.outline, italic = true }

	-- twilight dims inactive code
	h.Twilight = { fg = c.outline }

	-- spell
	h.SpellBad = { undercurl = true, sp = c.error }
	h.SpellCap = { undercurl = true, sp = c.tertiary }
	h.SpellLocal = { undercurl = true, sp = c.success }
	h.SpellRare = { undercurl = true, sp = c.secondary }

	return h
end

-- ---------------------------------------------------------------- terminal sync

-- end-4 recolors running kitties with a config-reload signal that sometimes
-- doesn't land; since nvim sits inside the terminal, assert the terminal's
-- default bg/fg itself (OSC 11/10) so text is always readable on the real bg
local function sync_terminal()
	local t = M._term
	local ui = vim.api.nvim_list_uis()[1]
	if not t or not (ui and ui.stdout_tty) then
		return
	end
	io.write(string.format("\027]11;%s\027\\\027]10;%s\027\\", t.bg, t.fg))
end

-- ---------------------------------------------------------------- apply

function M.apply()
	local pal, err = palette.load()
	if not pal then
		error(err)
	end
	local c, dark = effective(pal)

	-- clear colors_name BEFORE touching 'background': changing bg while a
	-- colorscheme is set makes nvim re-source it (recursion on live reload)
	vim.g.colors_name = nil
	local mode = dark and "dark" or "light"
	if vim.o.background ~= mode then
		vim.o.background = mode
	end

	vim.cmd("highlight clear")
	if vim.fn.exists("syntax_on") == 1 then
		vim.cmd("syntax reset")
	end
	vim.o.termguicolors = true
	vim.g.colors_name = "ii"

	for group, spec in pairs(highlights(c)) do
		vim.api.nvim_set_hl(0, group, spec)
	end

	for i = 0, 15 do
		vim.g["terminal_color_" .. i] = c["term" .. i]
	end

	M._term = { bg = c.term0, fg = c.term7 }
	sync_terminal()

	M._ensure_watcher()
end

-- ---------------------------------------------------------------- watcher

local watcher, debounce, retries

local function refresh()
	if vim.g.colors_name ~= "ii" then
		return -- another theme is active; stay dormant
	end
	local pal = palette.load()
	if not pal then
		-- partial write; retry a few times
		if retries < 3 then
			retries = retries + 1
			debounce:start(300, 0, vim.schedule_wrap(refresh))
		end
		return
	end
	retries = 0
	-- full colorscheme command so ColorScheme autocmds run again
	-- (transparent.lua re-strips backgrounds, barbar/ibl re-derive groups)
	vim.cmd.colorscheme("ii")
	package.loaded["lualine.themes.ii"] = nil
	local ok, lualine = pcall(require, "lualine")
	if ok then
		local cfg = lualine.get_config()
		cfg.options.theme = "ii"
		lualine.setup(cfg)
	end
	-- semantic-token extmarks keep stale colors through a plain redraw;
	-- re-request them so LSP-highlighted text picks up the new palette
	for _, buf in ipairs(vim.api.nvim_list_bufs()) do
		if vim.api.nvim_buf_is_loaded(buf) and #vim.lsp.get_clients({ bufnr = buf }) > 0 then
			pcall(vim.lsp.semantic_tokens.force_refresh, buf)
		end
	end
	vim.cmd("redraw!")
end

function M._ensure_watcher()
	if watcher then
		return
	end
	local dir = vim.fn.fnamemodify(palette.path, ":h")
	if vim.fn.isdirectory(dir) == 0 then
		return
	end
	watcher = vim.uv.new_fs_event()
	debounce = vim.uv.new_timer()
	retries = 0
	-- watch the directory: the scss file is truncate-rewritten and could be
	-- inode-replaced, which would orphan a direct file watch
	watcher:start(dir, {}, function(werr, filename)
		if werr or filename ~= "material_colors.scss" then
			return
		end
		retries = 0
		debounce:stop()
		debounce:start(300, 0, vim.schedule_wrap(refresh))
	end)
	local group = vim.api.nvim_create_augroup("ii_palette_watcher", { clear = true })
	vim.api.nvim_create_autocmd("VimLeavePre", {
		group = group,
		callback = function()
			if watcher then watcher:stop(); watcher:close(); watcher = nil end
			if debounce then debounce:stop(); debounce:close(); debounce = nil end
		end,
	})
	-- at startup apply() runs before the TUI attaches; sync the terminal
	-- once the UI is up (covers a kitty that missed end-4's reload signal)
	vim.api.nvim_create_autocmd("UIEnter", {
		group = group,
		callback = function()
			if vim.g.colors_name == "ii" then
				sync_terminal()
			end
		end,
	})
end

return M
