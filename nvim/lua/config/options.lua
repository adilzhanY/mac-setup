local options = {
	laststatus = 3,
	ruler = false, --disable extra numbering
	showmode = false, --not needed due to lualine
	showcmd = false,
	wrap = true, --toggle bound to leader W
	mouse = "a", --enable mouse
	clipboard = "unnamedplus", --system clipboard integration
	history = 100, --command line history
	swapfile = false, --swap just gets in the way, usually
	backup = false,
	undofile = true, --undos are saved to file
	cursorline = true, --highlight line
	scrolloff = 8, --keep 8 lines above/below cursor (smoother scroll)
	ttyfast = true, --faster scrolling
	smoothscroll = true,
	title = true, --automatic window titlebar
	
	number = true, --numbering lines
	relativenumber = true, --toggle bound to leader nn
	numberwidth = 4,

	smarttab = true, --indentation stuff
	cindent = false,
	autoindent = true,
	tabstop = 2, --visual width of tab
	shiftwidth = 2, 

	foldmethod = "expr",
	foldlevel = 99, --disable folding, lower #s enable
	foldexpr = "v:lua.vim.treesitter.foldexpr()",
	
	termguicolors = true,

	ignorecase = true, --ignore case while searching
	smartcase = true, --but do not ignore if caps are used

	conceallevel = 2, --markdown conceal
	concealcursor = "nc",

	splitkeep = 'screen', --stablizie window open/close
}

for k, v in pairs(options) do
	vim.opt[k] = v
end

-- Diagnostics.
--
-- Neovim 0.12 ships with virtual_text OFF, and this config also had signs off,
-- so the only sign an error existed was a faint underline. Everything below is
-- what makes errors and warnings read like VSCode: a coloured gutter icon, the
-- message inline at the end of the line, and a bordered float on hover.
vim.diagnostic.config({
	underline = true,
	update_in_insert = false, -- do not churn while you are mid-word
	severity_sort = true,     -- errors win over warnings on the same line
	virtual_text = {
		spacing = 4,
		prefix = "●",
		source = "if_many", -- name the server when two disagree
		-- keep long messages from pushing the line off screen
		format = function(d)
			local msg = d.message:gsub("%s*\n%s*", " ")
			if #msg > 100 then msg = msg:sub(1, 100) .. "..." end
			return msg
		end,
	},
	signs = {
		text = {
			[vim.diagnostic.severity.ERROR] = "",
			[vim.diagnostic.severity.WARN]  = "",
			[vim.diagnostic.severity.INFO]  = "",
			[vim.diagnostic.severity.HINT]  = "",
		},
	},
	float = {
		border = "rounded",
		source = true,
		header = "",
		prefix = "",
	},
})

-- The full message for the line under the cursor, in a float, without moving:
-- <leader>k. Toggle the inline text off when it gets in the way.
vim.keymap.set("n", "<leader>dv", function()
	local shown = vim.diagnostic.config().virtual_text
	vim.diagnostic.config({ virtual_text = not shown and {
		spacing = 4, prefix = "●", source = "if_many",
	} or false })
end, { silent = true, desc = "Toggle inline diagnostic text" })

vim.o.shell = 'fish'
vim.o.tabstop = 2
vim.o.shiftwidth = 2
vim.o.expandtab = true
-- 100ms was too tight: any mapping sharing a prefix with a shorter one
-- (<leader>f vs <leader>fm, <leader>t vs <leader>tg, gc vs gcc) resolved to the
-- short one before the second key landed. 300ms still feels instant for jj/jk.
vim.opt.timeoutlen = 300
vim.opt.updatetime = 200 -- CursorHold delay, also how fast gitsigns refreshes

vim.opt.signcolumn = "yes"  -- reserve the gutter so text stops jumping when a
                            -- diagnostic sign appears and disappears
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.confirm = true      -- ask instead of failing on :q with unsaved changes
vim.opt.linebreak = true    -- wrap at words, not mid-identifier
vim.opt.breakindent = true
vim.opt.undolevels = 10000
