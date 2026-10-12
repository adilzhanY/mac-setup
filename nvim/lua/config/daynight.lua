-- Follow the end-4 (Quickshell) light/dark state for STATIC colorschemes.
--
-- Kitty's real background comes from the wallpaper-generated Material palette
-- (light or dark), and nvim is transparent (config/transparent.lua), so a
-- dark-flavoured scheme over a light terminal is unreadably pale. The "ii"
-- scheme tracks the palette itself and is left alone here; for every other
-- scheme this module sets 'background' from the palette's $darkmode. Schemes
-- with light variants (catppuccin flavour "auto" gives latte, gruvbox,
-- solarized) then pick readable colors. Live-reloads on a wallpaper or
-- dark-mode change. The "mono" scheme also tracks the palette itself.

local palette = require("ii.palette")

local M = {}

local function mode()
	local pal = palette.load()
	if not pal then
		return nil
	end
	return pal.darkmode and "dark" or "light"
end

-- Set 'background' to match the palette. Assigning 'background' makes nvim
-- re-source the active colorscheme, so ColorScheme autocmds (transparent.lua,
-- barbar, ibl) run again on a flip.
function M.sync()
	if vim.g.colors_name == "ii" or vim.g.colors_name == "mono" then
		return -- these schemes manage 'background' themselves
	end
	local m = mode()
	if m and vim.o.background ~= m then
		vim.o.background = m
	end
end

local watcher, debounce

local function refresh()
	local before = vim.o.background
	M.sync()
	if vim.o.background == before then
		return
	end
	-- lualine caches compiled theme colors; re-setup so it re-derives them
	local ok, lualine = pcall(require, "lualine")
	if ok then
		lualine.setup(lualine.get_config())
	end
	-- semantic-token extmarks keep stale colors through a plain redraw
	for _, buf in ipairs(vim.api.nvim_list_bufs()) do
		if vim.api.nvim_buf_is_loaded(buf) and #vim.lsp.get_clients({ bufnr = buf }) > 0 then
			pcall(vim.lsp.semantic_tokens.force_refresh, buf)
		end
	end
	vim.cmd("redraw!")
end

function M.setup()
	M.sync()
	if watcher then
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
	vim.api.nvim_create_autocmd("VimLeavePre", {
		group = vim.api.nvim_create_augroup("daynight_watcher", { clear = true }),
		callback = function()
			if watcher then watcher:stop(); watcher:close(); watcher = nil end
			if debounce then debounce:stop(); debounce:close(); debounce = nil end
		end,
	})
end

return M
