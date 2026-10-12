-- lualine theme computed from the end-4 wallpaper palette; re-required
-- (cache cleared) by ii's palette watcher on every wallpaper change

local ok, pal = pcall(function()
	local p = require("ii.palette").load()
	assert(p, "no palette")
	return p.colors
end)

if not ok then
	-- palette unavailable: neutral fallback so require() never explodes
	local gray = {
		a = { bg = "#888888", fg = "#1a1a1a", gui = "bold" },
		b = { bg = "#3a3a3a", fg = "#dddddd" },
		c = { bg = "#2a2a2a", fg = "#aaaaaa" },
	}
	return { normal = gray, insert = gray, visual = gray, replace = gray,
		command = gray, terminal = gray, inactive = gray }
end

local b = { bg = pal.surfaceContainerHigh, fg = pal.onSurface }
local c = { bg = pal.surfaceContainer, fg = pal.onSurfaceVariant }

local function mode(bg, fg)
	return { a = { bg = bg, fg = fg, gui = "bold" }, b = b, c = c }
end

local inactive_section = { bg = pal.surfaceContainerLow, fg = pal.outline }

return {
	normal = mode(pal.primary, pal.onPrimary),
	insert = mode(pal.success, pal.onSuccess),
	visual = mode(pal.tertiary, pal.onTertiary),
	replace = mode(pal.error, pal.onError),
	command = mode(pal.secondary, pal.onSecondary),
	terminal = mode(pal.primaryContainer, pal.onPrimaryContainer),
	inactive = { a = inactive_section, b = inactive_section, c = inactive_section },
}
