-- The Problems panel: every diagnostic in the workspace in one list, rather
-- than only the ones in the file you happen to have open.
require("trouble").setup({
  focus = true,
  warn_no_results = false,
  open_no_results = true,
  modes = {
    diagnostics = { auto_open = false },
  },
})

local map = function(k, cmd, desc)
  vim.keymap.set("n", k, cmd, { silent = true, desc = desc })
end

map("<leader>xx", "<cmd>Trouble diagnostics toggle<cr>", "Problems (workspace)")
map("<leader>xb", "<cmd>Trouble diagnostics toggle filter.buf=0<cr>", "Problems (this file)")
map("<leader>xs", "<cmd>Trouble symbols toggle<cr>", "Symbol outline")
map("<leader>xr", "<cmd>Trouble lsp toggle<cr>", "References / definitions")
map("<leader>xq", "<cmd>Trouble qflist toggle<cr>", "Quickfix list")
