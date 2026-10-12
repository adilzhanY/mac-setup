-- "mono" colorscheme: no colors at all.
--
-- Pure black text on pure white in light mode, pure white text on pure black
-- in dark mode, and everything else a shade of grey. Nothing in the buffer is
-- ever tinted: keywords, strings, types, functions and variables all render in
-- the plain foreground, the way an editor with `syntax off` does.
--
-- Light/dark follows the same source as the rest of the desktop: the end-4
-- (Quickshell) palette file, which the day/night timer flips at 06:00 and
-- 19:00. It live-reloads when that file changes, so nvim flips with the shell.

local M = {}

-- ------------------------------------------------------------------ options

M.opts = {
	-- Paint a real background instead of letting kitty's translucency show
	-- through. Off by default because config/transparent.lua strips buffer
	-- backgrounds for every scheme, and kitty's window margin would stay
	-- translucent around an opaque buffer.
	opaque = false,
	-- Comments in a dimmer grey. The only "highlighting" that survives.
	dim_comments = true,
	italic_comments = true,
	-- Bold keywords and types. Off = completely flat code.
	emphasis = false,
	-- Grey out the :terminal ANSI palette too, so programs run inside nvim
	-- are colorless as well.
	terminal = true,
	-- Force nvim-web-devicons file icons to the plain foreground.
	flat_icons = true,
	-- After every colorscheme load, convert any color a plugin painted for
	-- itself into the grey of the same brightness. This is what makes the
	-- "no colors, ever" promise hold for plugins added later.
	sweep = true,
	-- Highlight groups the sweep must not touch. The statusline mode block is
	-- deliberately colored (see lua/lualine/themes/mono.lua) and lualine
	-- rebuilds those groups on every ColorScheme event, right before the sweep
	-- would run.
	sweep_ignore = { "^lualine_" },
}

function M.setup(opts)
	M.opts = vim.tbl_extend("force", M.opts, opts or {})
	if vim.g.colors_name == "mono" then
		M.apply()
	end
end

-- ------------------------------------------------------------------ palette

-- Greyscale ramps. Only `bg` and `fg` are absolute black/white; the rest are
-- chrome (line numbers, borders, selections) and stay strictly neutral.
local ramps = {
	dark = {
		bg = "#000000", -- editor background
		fg = "#FFFFFF", -- all buffer text
		bg1 = "#141414", -- cursor line, folds
		bg2 = "#1E1E1E", -- statusline, popup menu, tabs
		bg3 = "#2A2A2A", -- diff / quickfix wash
		sel = "#3A3A3A", -- visual selection, pmenu selection
		dim = "#8C8C8C", -- comments, secondary text
		faint = "#5A5A5A", -- line numbers, borders
		ghost = "#303030", -- indent guides, end of buffer
	},
	light = {
		bg = "#FFFFFF",
		fg = "#000000",
		bg1 = "#F1F1F1",
		bg2 = "#E9E9E9",
		bg3 = "#DEDEDE",
		sel = "#CFCFCF",
		dim = "#6B6B6B",
		faint = "#9A9A9A",
		ghost = "#C9C9C9",
	},
}

-- The desktop's light/dark state, from the end-4 palette; falls back to
-- whatever 'background' already says when that file isn't there.
local function is_dark()
	local ok, palette = pcall(require, "ii.palette")
	if ok then
		local pal = palette.load()
		if pal then
			return pal.darkmode
		end
	end
	return vim.o.background ~= "light"
end

-- ---------------------------------------------------------------- highlights

local function highlights(c)
	local o = M.opts
	local h = {}

	local fg = { fg = c.fg }
	local dim = { fg = o.dim_comments and c.dim or c.fg }
	local faint = { fg = c.faint }
	local ghost = { fg = c.ghost }
	local strong = o.emphasis and { fg = c.fg, bold = true } or fg
	local invert = { fg = c.bg, bg = c.fg, bold = true }

	local function flat(...)
		for _, group in ipairs({ ... }) do
			h[group] = fg
		end
	end

	-- editor chrome. The background is always defined; whether it survives is
	-- up to config/transparent.lua and the `opaque` option below.
	h.Normal = { fg = c.fg, bg = c.bg }
	h.NormalNC = { fg = c.fg, bg = c.bg }
	h.NormalFloat = { fg = c.fg, bg = c.bg1 }
	h.FloatBorder = faint
	h.FloatTitle = { fg = c.fg, bold = true }
	h.WinBar = { fg = c.fg, bold = true }
	h.WinBarNC = faint
	h.Cursor = { reverse = true }
	h.lCursor = { reverse = true }
	h.TermCursor = { reverse = true }
	h.CursorLine = { bg = c.bg1 }
	h.CursorColumn = { bg = c.bg1 }
	h.CursorLineNr = { fg = c.fg, bold = true }
	h.LineNr = faint
	h.LineNrAbove = faint
	h.LineNrBelow = faint
	h.SignColumn = {}
	h.FoldColumn = faint
	h.ColorColumn = { bg = c.bg1 }
	h.WinSeparator = { fg = c.ghost }
	h.VertSplit = { link = "WinSeparator" }
	h.StatusLine = { fg = c.fg, bg = c.bg2 }
	h.StatusLineNC = { fg = c.faint, bg = c.bg1 }
	h.TabLine = { fg = c.dim, bg = c.bg1 }
	h.TabLineFill = {}
	h.TabLineSel = { fg = c.fg, bg = c.bg2, bold = true }
	h.Visual = { bg = c.sel }
	h.VisualNOS = { link = "Visual" }
	h.Search = { fg = c.bg, bg = c.dim }
	h.IncSearch = invert
	h.CurSearch = invert
	h.Substitute = invert
	h.MatchParen = { bold = true, underline = true }
	h.Folded = { fg = c.dim, bg = c.bg1, italic = true }
	h.NonText = ghost
	h.Whitespace = ghost
	h.SpecialKey = ghost
	h.EndOfBuffer = ghost
	h.Conceal = faint
	h.Directory = { fg = c.fg, bold = true }
	h.Title = { fg = c.fg, bold = true }
	h.ErrorMsg = { fg = c.fg, bold = true }
	h.WarningMsg = { fg = c.fg }
	h.ModeMsg = { fg = c.fg, bold = true }
	h.MoreMsg = { fg = c.fg, bold = true }
	h.Question = fg
	h.QuickFixLine = { bg = c.bg3 }
	h.WildMenu = invert
	h.MsgArea = fg
	h.MsgSeparator = { fg = c.ghost }

	-- syntax: everything is plain text
	flat("Identifier", "Function", "String", "Character", "Number", "Boolean",
		"Float", "Constant", "Statement", "Conditional", "Repeat", "Label",
		"Operator", "Keyword", "Exception", "PreProc", "Include", "Define",
		"Macro", "PreCondit", "Type", "StorageClass", "Structure", "Typedef",
		"Special", "SpecialChar", "Tag", "Delimiter", "Debug")
	h.Comment = { fg = dim.fg, italic = o.italic_comments }
	h.SpecialComment = { link = "Comment" }
	h.Keyword = strong
	h.Statement = strong
	h.Conditional = strong
	h.Repeat = strong
	h.Type = strong
	h.Underlined = { fg = c.fg, underline = true }
	h.Ignore = ghost
	h.Error = { fg = c.fg, bold = true, undercurl = true, sp = c.fg }
	h.Todo = invert
	h.Added = fg
	h.Changed = fg
	h.Removed = fg
	h.healthSuccess = { fg = c.fg, bold = true }
	h.healthWarning = { fg = c.fg, bold = true }
	h.healthError = { fg = c.fg, bold = true }

	-- treesitter captures: link them all back to the flat groups so no
	-- language-specific query can sneak a color in
	for _, capture in ipairs({
		"@variable", "@variable.builtin", "@variable.parameter", "@variable.member",
		"@constant", "@constant.builtin", "@constant.macro",
		"@module", "@module.builtin", "@label",
		"@string", "@string.documentation", "@string.regexp", "@string.escape",
		"@string.special", "@string.special.symbol", "@string.special.path",
		"@string.special.url", "@character", "@character.special",
		"@boolean", "@number", "@number.float",
		"@type", "@type.builtin", "@type.definition", "@type.qualifier",
		"@attribute", "@attribute.builtin", "@property", "@field",
		"@function", "@function.builtin", "@function.call", "@function.macro",
		"@function.method", "@function.method.call", "@constructor", "@method",
		"@operator", "@keyword", "@keyword.coroutine", "@keyword.function",
		"@keyword.operator", "@keyword.import", "@keyword.type",
		"@keyword.modifier", "@keyword.repeat", "@keyword.return",
		"@keyword.debug", "@keyword.exception", "@keyword.conditional",
		"@keyword.conditional.ternary", "@keyword.directive",
		"@keyword.directive.define", "@keyword.storage",
		"@punctuation.delimiter", "@punctuation.bracket", "@punctuation.special",
		"@tag", "@tag.builtin", "@tag.attribute", "@tag.delimiter",
		"@namespace", "@none", "@text", "@parameter", "@preproc", "@define",
	}) do
		h[capture] = fg
	end
	h["@keyword"] = strong
	h["@keyword.function"] = strong
	h["@keyword.return"] = strong
	h["@keyword.conditional"] = strong
	h["@keyword.repeat"] = strong
	h["@keyword.import"] = strong
	h["@type"] = strong
	h["@type.builtin"] = strong
	h["@comment"] = { link = "Comment" }
	h["@comment.documentation"] = { link = "Comment" }
	h["@comment.todo"] = invert
	h["@comment.note"] = invert
	h["@comment.warning"] = invert
	h["@comment.error"] = invert
	h["@markup"] = fg
	h["@markup.heading"] = { fg = c.fg, bold = true }
	for i = 1, 6 do
		h["@markup.heading." .. i] = { fg = c.fg, bold = true }
		h["@markup.heading." .. i .. ".markdown"] = { fg = c.fg, bold = true }
		h["RenderMarkdownH" .. i] = { fg = c.fg, bold = true }
	end
	h["@markup.strong"] = { bold = true }
	h["@markup.italic"] = { italic = true }
	h["@markup.strikethrough"] = { strikethrough = true }
	h["@markup.underline"] = { underline = true }
	h["@markup.quote"] = { fg = c.dim, italic = true }
	h["@markup.math"] = fg
	h["@markup.link"] = { fg = c.fg, underline = true }
	h["@markup.link.url"] = { fg = c.dim, underline = true }
	h["@markup.link.label"] = fg
	h["@markup.raw"] = fg
	h["@markup.raw.block"] = fg
	h["@markup.list"] = fg
	h["@markup.list.checked"] = { fg = c.dim }
	h["@markup.list.unchecked"] = fg
	h["@diff.plus"] = fg
	h["@diff.minus"] = { fg = c.dim }
	h["@diff.delta"] = fg

	-- LSP semantic tokens: nvim links most of these to the treesitter groups
	-- above, but pin the common ones so a server can't reintroduce color
	for _, group in ipairs({
		"@lsp.type.class", "@lsp.type.comment", "@lsp.type.decorator",
		"@lsp.type.enum", "@lsp.type.enumMember", "@lsp.type.event",
		"@lsp.type.function", "@lsp.type.interface", "@lsp.type.keyword",
		"@lsp.type.macro", "@lsp.type.method", "@lsp.type.modifier",
		"@lsp.type.namespace", "@lsp.type.number", "@lsp.type.operator",
		"@lsp.type.parameter", "@lsp.type.property", "@lsp.type.regexp",
		"@lsp.type.string", "@lsp.type.struct", "@lsp.type.type",
		"@lsp.type.typeParameter", "@lsp.type.variable",
		"@lsp.mod.deprecated", "@lsp.mod.readonly", "@lsp.mod.defaultLibrary",
	}) do
		h[group] = fg
	end
	h["@lsp.type.comment"] = { link = "Comment" }
	h["@lsp.mod.deprecated"] = { fg = c.dim, strikethrough = true }

	-- diagnostics: severity shows through weight and underline, never hue
	h.DiagnosticError = { fg = c.fg, bold = true }
	h.DiagnosticWarn = { fg = c.fg }
	h.DiagnosticInfo = { fg = c.dim }
	h.DiagnosticHint = { fg = c.dim }
	h.DiagnosticOk = { fg = c.dim }
	h.DiagnosticVirtualTextError = { fg = c.dim, bold = true, italic = true }
	h.DiagnosticVirtualTextWarn = { fg = c.dim, italic = true }
	h.DiagnosticVirtualTextInfo = { fg = c.faint, italic = true }
	h.DiagnosticVirtualTextHint = { fg = c.faint, italic = true }
	h.DiagnosticUnderlineError = { undercurl = true, sp = c.fg }
	h.DiagnosticUnderlineWarn = { undercurl = true, sp = c.dim }
	h.DiagnosticUnderlineInfo = { underline = true, sp = c.faint }
	h.DiagnosticUnderlineHint = { underline = true, sp = c.faint }
	h.DiagnosticSignError = { fg = c.fg, bold = true }
	h.DiagnosticSignWarn = { fg = c.fg }
	h.DiagnosticSignInfo = { fg = c.dim }
	h.DiagnosticSignHint = { fg = c.dim }
	h.DiagnosticDeprecated = { strikethrough = true, sp = c.dim }
	h.DiagnosticUnnecessary = { fg = c.dim }
	h.LspReferenceText = { bg = c.bg3 }
	h.LspReferenceRead = { bg = c.bg3 }
	h.LspReferenceWrite = { bg = c.bg3, underline = true }
	h.LspInlayHint = { fg = c.faint, italic = true }
	h.LspSignatureActiveParameter = { bold = true, underline = true }
	h.LspCodeLens = { fg = c.faint, italic = true }

	-- diff / git: greys plus the signs' own +/~/- characters
	h.DiffAdd = { bg = c.bg2 }
	h.DiffChange = { bg = c.bg1 }
	h.DiffDelete = { fg = c.ghost, bg = c.bg1 }
	h.DiffText = { bg = c.sel, bold = true }
	h.diffAdded = fg
	h.diffRemoved = { fg = c.dim }
	h.diffChanged = fg
	h.diffFile = { fg = c.fg, bold = true }
	h.diffLine = { fg = c.dim }
	h.GitSignsAdd = { fg = c.dim }
	h.GitSignsChange = { fg = c.dim }
	h.GitSignsDelete = { fg = c.dim }
	h.GitSignsAddNr = { fg = c.faint }
	h.GitSignsChangeNr = { fg = c.faint }
	h.GitSignsDeleteNr = { fg = c.faint }
	h.GitSignsCurrentLineBlame = { fg = c.faint, italic = true }

	-- popup menu / nvim-cmp
	h.Pmenu = { fg = c.fg, bg = c.bg2 }
	h.PmenuSel = { fg = c.fg, bg = c.sel, bold = true }
	h.PmenuSbar = { bg = c.bg2 }
	h.PmenuThumb = { bg = c.faint }
	h.PmenuKind = { fg = c.dim, bg = c.bg2 }
	h.PmenuKindSel = { fg = c.fg, bg = c.sel }
	h.PmenuExtra = { fg = c.faint, bg = c.bg2 }
	h.PmenuExtraSel = { fg = c.dim, bg = c.sel }
	h.CmpItemAbbr = fg
	h.CmpItemAbbrDeprecated = { fg = c.faint, strikethrough = true }
	h.CmpItemAbbrMatch = { fg = c.fg, bold = true }
	h.CmpItemAbbrMatchFuzzy = { fg = c.fg, bold = true }
	h.CmpItemMenu = { fg = c.faint, italic = true }
	-- every completion kind renders in the same grey
	for _, kind in ipairs({
		"Text", "Method", "Function", "Constructor", "Field", "Variable",
		"Class", "Interface", "Module", "Property", "Unit", "Value", "Enum",
		"Keyword", "Snippet", "Color", "File", "Reference", "Folder",
		"EnumMember", "Constant", "Struct", "Event", "Operator", "TypeParameter",
	}) do
		h["CmpItemKind" .. kind] = { fg = c.dim }
	end

	-- indent-blankline v3
	h.IblIndent = ghost
	h.IblWhitespace = ghost
	h.IblScope = { fg = c.faint }

	-- barbar
	local barbar = {
		Current = { fg = c.fg, bg = c.bg2, bold = true },
		Visible = { fg = c.dim, bg = c.bg1 },
		Alternate = { fg = c.dim, bg = c.bg1 },
		Inactive = { fg = c.faint, bg = nil },
	}
	for state, s in pairs(barbar) do
		h["Buffer" .. state] = { fg = s.fg, bg = s.bg, bold = s.bold }
		for _, part in ipairs({ "Mod", "Sign", "SignRight", "Index", "Icon",
			"Btn", "Pin", "ERROR", "WARN", "INFO", "HINT" }) do
			h["Buffer" .. state .. part] = { fg = s.fg, bg = s.bg }
		end
		h["Buffer" .. state .. "Target"] = { fg = s.fg, bg = s.bg, bold = true, underline = true }
	end
	h.BufferTabpageFill = {}
	h.BufferTabpages = { fg = c.fg, bold = true }

	-- nvim-tree
	h.NvimTreeNormal = fg
	h.NvimTreeNormalNC = fg
	h.NvimTreeRootFolder = { fg = c.fg, bold = true }
	h.NvimTreeFolderIcon = { fg = c.dim }
	h.NvimTreeFolderName = fg
	h.NvimTreeOpenedFolderName = { fg = c.fg, bold = true }
	h.NvimTreeEmptyFolderName = { fg = c.dim }
	h.NvimTreeOpenedFile = { fg = c.fg, bold = true }
	h.NvimTreeSpecialFile = { fg = c.fg, underline = true }
	h.NvimTreeExecFile = { fg = c.fg, bold = true }
	h.NvimTreeSymlink = { fg = c.dim, italic = true }
	h.NvimTreeImageFile = fg
	h.NvimTreeGitNew = { fg = c.dim }
	h.NvimTreeGitDirty = { fg = c.dim }
	h.NvimTreeGitStaged = { fg = c.dim }
	h.NvimTreeGitDeleted = { fg = c.dim }
	h.NvimTreeGitRenamed = { fg = c.dim }
	h.NvimTreeGitIgnored = { fg = c.faint }
	h.NvimTreeIndentMarker = ghost
	h.NvimTreeWinSeparator = { fg = c.ghost }
	h.NvimTreeCursorLine = { bg = c.bg1 }

	-- telescope-style groups (fzf-lua reuses these)
	h.TelescopeNormal = fg
	h.TelescopeBorder = faint
	h.TelescopePromptBorder = faint
	h.TelescopeSelection = { bg = c.bg3 }
	h.TelescopeSelectionCaret = { fg = c.fg, bg = c.bg3 }
	h.TelescopeMatching = { fg = c.fg, bold = true, underline = true }
	h.TelescopePromptPrefix = fg
	h.TelescopePromptTitle = invert
	h.TelescopePreviewTitle = invert
	h.TelescopeResultsTitle = invert
	h.FzfLuaTitle = invert
	h.FzfLuaNormal = fg
	h.FzfLuaBorder = faint
	h.FzfLuaHeaderText = { fg = c.dim }
	h.FzfLuaHeaderBind = { fg = c.fg, bold = true }
	h.FzfLuaCursorLine = { bg = c.bg3 }
	h.FzfLuaFzfMatch = { fg = c.fg, bold = true }

	-- which-key
	h.WhichKey = { fg = c.fg, bold = true }
	h.WhichKeyGroup = { fg = c.dim }
	h.WhichKeyDesc = fg
	h.WhichKeySeparator = { fg = c.faint }
	h.WhichKeyFloat = { bg = c.bg1 }
	h.WhichKeyBorder = faint
	h.WhichKeyIcon = { fg = c.dim }
	h.WhichKeyIconAzure = { fg = c.dim }
	h.WhichKeyIconBlue = { fg = c.dim }
	h.WhichKeyIconCyan = { fg = c.dim }
	h.WhichKeyIconGreen = { fg = c.dim }
	h.WhichKeyIconGrey = { fg = c.dim }
	h.WhichKeyIconOrange = { fg = c.dim }
	h.WhichKeyIconPurple = { fg = c.dim }
	h.WhichKeyIconRed = { fg = c.dim }
	h.WhichKeyIconYellow = { fg = c.dim }

	-- alpha (start screen)
	h.AlphaHeader = { fg = c.dim }
	h.AlphaButtons = fg
	h.AlphaShortcut = { fg = c.fg, bold = true }
	h.AlphaFooter = { fg = c.faint, italic = true }

	-- twilight dims inactive code
	h.Twilight = { fg = c.faint }

	-- spell: shape only, no colored squiggles
	h.SpellBad = { undercurl = true, sp = c.dim }
	h.SpellCap = { undercurl = true, sp = c.faint }
	h.SpellLocal = { undercurl = true, sp = c.faint }
	h.SpellRare = { undercurl = true, sp = c.faint }

	return h
end

-- ------------------------------------------------------------- terminal sync

-- nvim renders inside kitty, whose background comes from the desktop palette.
-- Assert pure black/white directly (OSC 11/10) so the visible background is
-- the one this scheme asks for even when the wallpaper palette is tinted.
local function sync_terminal(c)
	local ui = vim.api.nvim_list_uis()[1]
	if not (ui and ui.stdout_tty) then
		return
	end
	io.write(string.format("\027]11;%s\027\\\027]10;%s\027\\", c.bg, c.fg))
end

-- Icon plugins ship hardcoded per-filetype colors; flatten whatever they
-- defined to the plain foreground.
local function flatten_icon_groups(c)
	for _, group in ipairs(vim.fn.getcompletion("DevIcon", "highlight")) do
		pcall(vim.api.nvim_set_hl, 0, group, { fg = c.fg })
	end
	for _, group in ipairs(vim.fn.getcompletion("MiniIcons", "highlight")) do
		pcall(vim.api.nvim_set_hl, 0, group, { fg = c.fg })
	end
end

-- Last resort: any color a plugin defines for itself (barbar's pick letters,
-- a linter's own groups, anything installed later) gets converted to the grey
-- of the same brightness, then pushed into a band that stays readable against
-- the background. Groups that are already grey are left untouched.
local function grey_of(value, dark, is_bg)
	local r = math.floor(value / 65536) % 256
	local g = math.floor(value / 256) % 256
	local b = value % 256
	if r == g and g == b then
		return nil -- already neutral
	end
	local y = math.floor(0.2126 * r + 0.7152 * g + 0.0722 * b + 0.5)
	if is_bg then
		-- backgrounds stay close to the editor background
		y = dark and math.min(y, 0x4A) or math.max(y, 0xC0)
	else
		-- foregrounds stay legible on it
		y = dark and math.max(y, 0x8C) or math.min(y, 0x6B)
	end
	return y * 65536 + y * 256 + y
end

local function sweep_exempt(name)
	for _, pattern in ipairs(M.opts.sweep_ignore or {}) do
		if name:match(pattern) then
			return true
		end
	end
	return false
end

local function sweep_colors(dark)
	for name, spec in pairs(vim.api.nvim_get_hl(0, {})) do
		if not spec.link and not sweep_exempt(name) then
			local changed = false
			for _, key in ipairs({ "fg", "sp" }) do
				local grey = type(spec[key]) == "number" and grey_of(spec[key], dark, false)
				if grey then
					spec[key] = grey
					changed = true
				end
			end
			local grey_bg = type(spec.bg) == "number" and grey_of(spec.bg, dark, true)
			if grey_bg then
				spec.bg = grey_bg
				changed = true
			end
			if changed then
				pcall(vim.api.nvim_set_hl, 0, name, spec)
			end
		end
	end
end

-- Runs last on every ColorScheme event, after the plugins that repaint their
-- own groups there: nvim-web-devicons recreates its per-filetype colors from
-- scratch (a `highlight clear` wipes them, so flattening during apply() would
-- be undone), and config/transparent.lua strips buffer backgrounds.
local function ensure_post_hook()
	local group = vim.api.nvim_create_augroup("mono_post", { clear = true })
	vim.api.nvim_create_autocmd("ColorScheme", {
		group = group,
		callback = function()
			if vim.g.colors_name ~= "mono" or not M._colors then
				return
			end
			local c = M._colors
			if M.opts.flat_icons then
				flatten_icon_groups(c)
			end
			if M.opts.sweep then
				sweep_colors(c.bg == "#000000")
			end
			if M.opts.opaque then
				for _, g in ipairs({ "Normal", "NormalNC" }) do
					local hl = vim.api.nvim_get_hl(0, { name = g })
					hl.bg = tonumber(c.bg:sub(2), 16)
					vim.api.nvim_set_hl(0, g, hl)
				end
			end
		end,
	})
end

-- ---------------------------------------------------------------------- apply

function M.apply()
	local dark = is_dark()
	local c = dark and ramps.dark or ramps.light

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
	vim.g.colors_name = "mono"

	for group, spec in pairs(highlights(c)) do
		vim.api.nvim_set_hl(0, group, spec)
	end

	if M.opts.flat_icons then
		flatten_icon_groups(c)
	end

	if M.opts.terminal then
		-- a greyscale ANSI ramp: programs run in :terminal stay colorless but
		-- keep enough contrast steps to remain readable
		local shades = dark
			and { c.bg, "#4D4D4D", "#666666", "#808080", "#999999", "#B3B3B3", "#CCCCCC", "#E6E6E6" }
			or { c.bg, "#C4C4C4", "#AEAEAE", "#989898", "#828282", "#6C6C6C", "#565656", "#404040" }
		for i = 0, 7 do
			vim.g["terminal_color_" .. i] = shades[i + 1]
		end
		for i = 8, 15 do
			vim.g["terminal_color_" .. i] = shades[i - 7]
		end
		vim.g.terminal_color_0 = c.bg
		vim.g.terminal_color_7 = c.fg
		vim.g.terminal_color_15 = c.fg
	end

	M._colors = c
	ensure_post_hook()
	sync_terminal(c)
	M._ensure_watcher()
end

-- -------------------------------------------------------------------- watcher

local watcher, debounce

local function refresh()
	if vim.g.colors_name ~= "mono" then
		return -- another theme is active; stay dormant
	end
	-- full colorscheme command so ColorScheme autocmds run again
	-- (transparent.lua re-strips backgrounds, barbar/ibl re-derive groups)
	vim.cmd.colorscheme("mono")
	package.loaded["lualine.themes.mono"] = nil
	local ok, lualine = pcall(require, "lualine")
	if ok then
		local cfg = lualine.get_config()
		cfg.options.theme = "mono"
		lualine.setup(cfg)
	end
	-- semantic-token extmarks keep stale colors through a plain redraw
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
	local ok, palette = pcall(require, "ii.palette")
	if not ok then
		return
	end
	local dir = vim.fn.fnamemodify(palette.path, ":h")
	if vim.fn.isdirectory(dir) == 0 then
		return
	end
	watcher = vim.uv.new_fs_event()
	debounce = vim.uv.new_timer()
	-- watch the directory: the scss file is truncate-rewritten and could be
	-- inode-replaced, which would orphan a direct file watch
	watcher:start(dir, {}, function(werr, filename)
		if werr or filename ~= "material_colors.scss" then
			return
		end
		debounce:stop()
		debounce:start(300, 0, vim.schedule_wrap(refresh))
	end)
	local group = vim.api.nvim_create_augroup("mono_palette_watcher", { clear = true })
	vim.api.nvim_create_autocmd("VimLeavePre", {
		group = group,
		callback = function()
			if watcher then watcher:stop(); watcher:close(); watcher = nil end
			if debounce then debounce:stop(); debounce:close(); debounce = nil end
		end,
	})
	-- at startup apply() runs before the TUI attaches; assert the terminal
	-- background once the UI is really up
	vim.api.nvim_create_autocmd("UIEnter", {
		group = group,
		callback = function()
			if vim.g.colors_name == "mono" and M._colors then
				sync_terminal(M._colors)
			end
		end,
	})
end

return M
