require('lint').linters_by_ft = { --some of these need to be installed from package manager
  lua = {'luac'},
  python = {'ruff'},
  sh = {'bash'},
  c = {'cppcheck'},
  -- rust: intentionally left out. rust-analyzer is configured with
  -- check.command = "clippy", so clippy diagnostics already arrive through the
  -- LSP. Running it here too would compile the crate a second time on every
  -- write, which autosave makes expensive.
  -- css/html/eslint diagnostics already arrive over LSP (cssls, html, eslint),
  -- so no second tool is listed for them. config/autocmd.lua skips any linter
  -- whose binary is not on PATH, so adding one here is safe even before you
  -- install it.
}

-- Some linters require a file to be saved to disk, others support linting stdin input.
-- For such linters you could also define a more aggressive autocmd,
-- for example on the InsertLeave or TextChanged events.
-- To get the filetype of a buffer you can run := vim.bo.filetype.

-- lints on close, see autocmd
