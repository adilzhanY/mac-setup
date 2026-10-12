-- Statusline for the "mono" colorscheme: greyscale everywhere except the mode
-- block, which keeps the colors muscle memory expects (green in INSERT, purple
-- in VISUAL, and so on). The buffer itself stays colorless; this is the one
-- place a glance at color tells you something the text cannot.
--
-- Two families, one per background: bright accents carrying black text on the
-- dark theme, deep accents carrying white text on the light theme. Both sets
-- sit at roughly equal brightness, so the bar never jumps when the mode
-- changes. Re-required (cache cleared) by mono's palette watcher on a flip.

local dark = true
local ok, palette = pcall(require, "ii.palette")
if ok then
	local pal = palette.load()
	dark = pal and pal.darkmode or (not pal and vim.o.background ~= "light")
else
	dark = vim.o.background ~= "light"
end

local grey = dark
	and { bg = "#000000", fg = "#FFFFFF", b = "#1E1E1E", cbg = "#141414", cfg = "#8C8C8C", ifg = "#5A5A5A" }
	or { bg = "#FFFFFF", fg = "#000000", b = "#E9E9E9", cbg = "#F1F1F1", cfg = "#6B6B6B", ifg = "#9A9A9A" }

-- mode accents. NORMAL is blue, INSERT green, VISUAL purple, REPLACE red,
-- COMMAND amber, TERMINAL teal: the mapping nearly every vim statusline uses.
local accents = dark
	and {
		normal = "#61AFEF", -- blue
		insert = "#98C379", -- green
		visual = "#C678DD", -- purple
		replace = "#E06C75", -- red
		command = "#E5C07B", -- amber
		terminal = "#56B6C2", -- teal
	}
	or {
		normal = "#2C6FB5",
		insert = "#2E7D32",
		visual = "#7B1FA2",
		replace = "#C62828",
		command = "#B26A00",
		terminal = "#00707A",
	}

-- text on the accent block: black on the bright set, white on the deep set
local on_accent = dark and "#000000" or "#FFFFFF"

local b = { bg = grey.b, fg = grey.fg }
local c = { bg = grey.cbg, fg = grey.cfg }

local function section(accent)
	return {
		a = { bg = accent, fg = on_accent, gui = "bold" },
		b = b,
		c = c,
	}
end

local inactive = { bg = grey.cbg, fg = grey.ifg }

return {
	normal = section(accents.normal),
	insert = section(accents.insert),
	visual = section(accents.visual),
	replace = section(accents.replace),
	command = section(accents.command),
	terminal = section(accents.terminal),
	inactive = { a = inactive, b = inactive, c = inactive },
}
