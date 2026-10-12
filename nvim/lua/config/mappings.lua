-- mappings, including plugins

local function map(m, k, v)
	vim.keymap.set(m, k, v, { noremap = true, silent = true })
end

-- set leader
map("", "<Space>", "<Nop>")
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- buffers
map("n", "<S-l>", ":bnext<CR>")
map("n", "<S-h>", ":bprevious<CR>")
map("n", "<leader>q", ":BufferClose<CR>")
map("n", "<leader>Q", ":BufferClose!<CR>")
map("n", "<leader>U", ":bufdo bd<CR>") --close all
map('n', '<leader>vs', ':vsplit<CR>:bnext<CR>') --ver split + open next buffer

-- move lines
map("n", "<A-j>", ":m .+1<CR>==")  -- Alt+j: Move line down
map("n", "<A-k>", ":m .-2<CR>==")  -- Alt+k: Move line up
map("v", "<A-j>", ":m '>+1<CR>gv=gv")  -- Alt+j in visual: Move block down
map("v", "<A-k>", ":m '<-2<CR>gv=gv")  -- Alt+k in visual: Move block up

-- buffer position nav + reorder
map('n', '<A-S-h>', '<Cmd>BufferMovePrevious<CR>')
map('n', '<A-S-l>', '<Cmd>BufferMoveNext<CR>')
map('n', '<A-1>', '<Cmd>BufferGoto 1<CR>')
map('n', '<A-2>', '<Cmd>BufferGoto 2<CR>')
map('n', '<A-3>', '<Cmd>BufferGoto 3<CR>')
map('n', '<A-4>', '<Cmd>BufferGoto 4<CR>')
map('n', '<A-5>', '<Cmd>BufferGoto 5<CR>')
map('n', '<A-6>', '<Cmd>BufferGoto 6<CR>')
map('n', '<A-7>', '<Cmd>BufferGoto 7<CR>')
map('n', '<A-8>', '<Cmd>BufferGoto 8<CR>')
map('n', '<A-9>', '<Cmd>BufferGoto 9<CR>')
map('n', '<A-0>', '<Cmd>BufferLast<CR>')
map('n', '<A-p>', '<Cmd>BufferPin<CR>')

-- windows - ctrl nav, fn resize
map("n", "<C-h>", "<C-w>h")
map("n", "<C-j>", "<C-w>j")
map("n", "<C-k>", "<C-w>k")
map("n", "<C-l>", "<C-w>l")
map("n", "<F5>", ":resize +2<CR>")
map("n", "<F6>", ":resize -2<CR>")
map("n", "<F7>", ":vertical resize +2<CR>")
map("n", "<F8>", ":vertical resize -2<CR>")

-- fzf and grep
map("n", "<leader>b", ":lua require('fzf-lua').buffers()<CR>") -- search buffers
map("n", "<leader>f", ":lua require('fzf-lua').files()<CR>") --search cwd
map("n", "<leader>Fh", ":lua require('fzf-lua').files({ cwd = '~/' })<CR>") --search home
map("n", "<leader>Fc", ":lua require('fzf-lua').files({ cwd = '~/.config' })<CR>") --search .config
map("n", "<leader>Fl", ":lua require('fzf-lua').files({ cwd = '~/.local/src' })<CR>") --search .local/src
map("n", "<leader>Ff", ":lua require('fzf-lua').files({ cwd = '..' })<CR>") --search above
map("n", "<leader>Fr", ":lua require('fzf-lua').resume()<CR>") --last search
map("n", "<leader>g", ":lua require('fzf-lua').grep()<CR>") --grep
map("n", "<leader>G", ":lua require('fzf-lua').grep_cword()<CR>") --grep word under cursor
map("n", "<leader>sn", ":lua require('fzf-lua').luasnip()<CR>") --search snippets

vim.keymap.set('t', 'jj', '<C-\\><C-n>', { noremap = true, silent = true }) -- jj exits terminal mode
vim.keymap.set('t', 'jk', '<C-\\><C-n>', { noremap = true, silent = true }) -- jk exits terminal mode

map("n", "<leader>fm", function() require("conform").format({ lsp_fallback = true }) end) -- format file
map("n", "<leader>sf", function() require("conform").format({ lsp_fallback = true }) end) -- format file (alternative)

-- misc
map("n", "<leader>s", ":%s//g<Left><Left>") --replace all
map("n", "<leader>t", ":NvimTreeToggle<CR>") --open file explorer
map("n", "<leader>p", function()
	if type(switch_theme) == "function" then switch_theme() end
end) --cycle themes
map("n", "<leader>P", ":PlugInstall<CR>") --vim-plug
map('n', '<leader>z', ":lua require('FTerm').open()<CR>") --open term
map("n", "<leader>w", ":w<CR>") --write but one less key
map("n", "<leader>d", ":w ") --duplicate to new name
map("n", "<leader>x", "<cmd>!chmod +x %<CR>") --make a file executable
map("n", "<leader>mv", ":!mv % ") --move a file to a new dir
map("n", "<leader>R", ":so %<CR>") --reload neovim config
map("n", "<leader>u", function() vim.ui.open(vim.fn.expand("<cWORD>")) end) --open a url under cursor
map("v", "<leader>i", "=gv") --auto indent
map("n", "<leader>W", ":set wrap!<CR>") --toggle wrap
map("n", "<leader>l", ":Twilight<CR>") --surrounding dim

-- decisive csv
map("n", "<leader>csa", ":lua require('decisive').align_csv({})<cr>")
map("n", "<leader>csA", ":lua require('decisive').align_csv_clear({})<cr>")
map("n", "[c", ":lua require('decisive').align_csv_prev_col()<cr>")
map("n", "]c", ":lua require('decisive').align_csv_next_col()<cr>")

-- commenting
map("n", "gcc", "<Plug>(comment_toggle_linewise_current)")
map("n", "gc", "<Plug>(comment_toggle_linewise)")
map("n", "gbc", "<Plug>(comment_toggle_blockwise_current)") -- Add this line
map("v", "gc", "<Plug>(comment_toggle_blockwise)")

-- Quick terminal launchers
map("n", "<leader>tg", ":term<CR>:file git<CR>i") -- Open git terminal
map("n", "<leader>tf", ":term<CR>:file fish<CR>i") -- Open fish terminal
map("n", "<leader>tt", ":term<CR>i") -- Open unnamed terminal


map("n", "<leader>H", function() --toggle htop in term
    _G.htop:toggle()
end)


map("n", "<leader>ma", function() --quick make in dir of buffer
	local bufdir = vim.fn.expand("%:p:h")
	vim.cmd("lcd " .. bufdir)
	vim.cmd("!sudo make uninstall && sudo make clean install %")
end)


map("n", "<leader>nn", function() --toggle relative vs absolute line numbers
	if vim.wo.relativenumber then
		vim.wo.relativenumber = false
		vim.wo.number = true
	else
		vim.wo.relativenumber = true
	end
end)

vim.keymap.set('i', 'jj', '<Esc>', { noremap = true, silent = true })
vim.keymap.set('i', 'jk', '<Esc>', { noremap = true, silent = true })


-- ---------------------------------------------------------------------------
-- Diagnostics and problems (LSP keys are buffer-local, see plugins/lsp.lua)
-- ---------------------------------------------------------------------------
map("n", "<leader>dd", function() vim.diagnostic.setloclist() end) --diagnostics for this file
