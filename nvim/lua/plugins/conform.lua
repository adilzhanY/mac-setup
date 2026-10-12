-- Formatting.
--
-- prettierd is a daemon version of prettier: same output, but it keeps the
-- process warm so a format is instant instead of a ~400ms node start. prettier
-- is the fallback when a project pins its own version.
local js = { "prettierd", "prettier", stop_after_first = true }

require("conform").setup({
  formatters_by_ft = {
    javascript = js,
    javascriptreact = js,
    typescript = js,
    typescriptreact = js,
    css = js,
    scss = js,
    less = js,
    html = js,
    json = js,
    jsonc = js,
    yaml = js,
    markdown = js,
    graphql = js,
    lua = { "stylua" },
    -- ruff replaces black here: it is already installed, and it is the same
    -- tool that lints, so the two cannot disagree about a line.
    python = { "ruff_organize_imports", "ruff_format" },
    -- rustfmt comes from rustup, same toolchain as rust-analyzer
    rust = { "rustfmt" },
    toml = { "taplo" },
    sh = { "shfmt" },
    ["_"] = { "trim_whitespace" }, -- anything with no formatter of its own
  },

  -- Format when you save, like VSCode's formatOnSave.
  --
  -- The guard matters: init.lua autosaves the buffer once a second while you
  -- type, and reformatting mid-keystroke would move the cursor out from under
  -- you. vim.g.autosaving is set only around those timer writes, so formatting
  -- happens on a deliberate :w (or <leader>w) and never on an autosave.
  format_on_save = function(bufnr)
    if vim.g.autosaving then return nil end
    if vim.g.disable_autoformat or vim.b[bufnr].disable_autoformat then return nil end
    return { timeout_ms = 2000, lsp_format = "fallback" }
  end,

  notify_on_error = true,
})

-- :FormatDisable / :FormatEnable, for the file you do not want touched.
vim.api.nvim_create_user_command("FormatDisable", function(args)
  if args.bang then
    vim.b.disable_autoformat = true
  else
    vim.g.disable_autoformat = true
  end
end, { desc = "Turn off format on save (! for this buffer only)", bang = true })

vim.api.nvim_create_user_command("FormatEnable", function()
  vim.b.disable_autoformat = false
  vim.g.disable_autoformat = false
end, { desc = "Turn format on save back on" })
