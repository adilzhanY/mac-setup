local lualine = require('lualine')

local diagnostics = {
	"diagnostics",
	sources = { "nvim_diagnostic" },
	sections = { "error", "warn" },
	symbols = { error = " ", warn = " " },
	colored = true,
	update_in_insert = false,
	always_visible = true,
	cond = function()
		return vim.bo.filetype ~= "markdown"
	end,
}

local diff = {
	"diff",
	colored = true,
	symbols = { added = " ", modified = " ", removed = " " },
}

local mode = {
	"mode",
	fmt = function(str)
		return "-- " .. str .. " --"
	end,
}

local branch = {
	"branch",
	icon = "",
}

-- Which colorscheme is active right now.
--
-- vim.g.colors_name on its own is not enough: kanagawa reports "kanagawa" for
-- all three of its variants and modus reports "modus" for both of its, so the
-- variant you actually picked would be invisible. config/theme.lua records the
-- exact name it selected in vim.g.theme_display, and this shows whichever of
-- the two is more specific. Running :colorscheme by hand sets colors_name to
-- something unrelated to the recorded pick, and then colors_name wins.
local theme_name = {
	function()
		local live = vim.g.colors_name or "none"
		local picked = vim.g.theme_display
		if type(picked) == "string" and picked ~= "" then
			if picked:sub(1, #live) == live then return "󰏘 " .. picked end
			if live:sub(1, #picked) == picked then return "󰏘 " .. live end
		end
		return "󰏘 " .. live
	end,
	-- the right-hand side is already busy, so drop this first on a narrow split
	cond = function() return vim.o.columns > 90 end,
}

local progress = function()
	local current_line = vim.fn.line(".")
	local total_lines = vim.fn.line("$")
	local chars = { "", "", "" } --adding more chars will still work
	local line_ratio = current_line / total_lines
	local index = math.ceil(line_ratio * #chars)
	return chars[index] .. " " .. math.floor(line_ratio * 100) .. "%%"
end

lualine.setup({
options = {
	icons_enabled = true,
	theme = "auto", --auto allows for theme switching
	component_separators = { left = "", right = "" },
	section_separators = { left = "", right = "" },
	disabled_filetypes = { "alpha", "dashboard" },
	always_divide_middle = true,
	},

sections = {
	lualine_a = { mode },
	lualine_b = { branch },
	lualine_c = { diagnostics, theme_name },
	lualine_x = { diff, "fileformat", "filetype" },
	lualine_y = { "location" },
	lualine_z = { progress },
	},
	extensions = { 'nvim-tree' },
})

-- transparency override if using old pywal, shouldn't be needed with 16
-- vim.api.nvim_set_hl(0, "lualine_c_normal", { bg = "none" })
-- vim.api.nvim_set_hl(0, "lualine_c_inactive", { bg = "none" })
-- vim.api.nvim_set_hl(0, "lualine_x_normal", { bg = "none" })
-- vim.api.nvim_set_hl(0, "lualine_x_inactive", { bg = "none" })
