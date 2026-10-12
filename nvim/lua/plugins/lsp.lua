-- Language servers.
--
-- Completion itself lives in lua/plugins/cmp.lua. This file only decides which
-- servers run, how each one is configured, and what keys they bind.
--
-- mason-lspconfig v2 removed the old `handlers`/per-server `setup()` mechanism.
-- Servers in `ensure_installed` are installed and auto-enabled through
-- vim.lsp.enable(), so per-server options go through vim.lsp.config() and
-- keymaps through an LspAttach autocmd.

require('mason').setup({
  ui = { border = 'rounded' },
})

local capabilities = require('cmp_nvim_lsp').default_capabilities()
-- Ask servers for the extra fields VSCode gets: snippet-style function
-- signatures, auto-import edits, and folding ranges.
capabilities.textDocument.completion.completionItem.snippetSupport = true
capabilities.textDocument.completion.completionItem.resolveSupport = {
  properties = { 'documentation', 'detail', 'additionalTextEdits' },
}
capabilities.textDocument.foldingRange = { dynamicRegistration = false, lineFoldingOnly = true }

-- ---------------------------------------------------------------------------
-- Keymaps, bound once per buffer whenever any server attaches
-- ---------------------------------------------------------------------------
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(args)
    local bufnr = args.buf
    local function map(m, k, v, desc)
      vim.keymap.set(m, k, v, { noremap = true, silent = true, buffer = bufnr, desc = desc })
    end

    map('n', 'gd', vim.lsp.buf.definition, 'Go to definition')
    map('n', 'gD', vim.lsp.buf.declaration, 'Go to declaration')
    map('n', 'gi', vim.lsp.buf.implementation, 'Go to implementation')
    map('n', 'gy', vim.lsp.buf.type_definition, 'Go to type definition')
    map('n', 'K', function() vim.lsp.buf.hover({ border = 'rounded' }) end, 'Hover docs')
    map('n', '<leader>rr', vim.lsp.buf.references, 'References')
    map('n', '<leader>rn', vim.lsp.buf.rename, 'Rename symbol')
    map({ 'n', 'v' }, '<leader>ca', vim.lsp.buf.code_action, 'Code action')

    -- The signature popup also appears automatically while typing arguments
    -- (cmp-nvim-lsp-signature-help); this is the on-demand version.
    map({ 'i', 'n' }, '<C-k>', function() vim.lsp.buf.signature_help({ border = 'rounded' }) end, 'Signature help')

    -- vim.diagnostic.goto_prev/goto_next are deprecated on 0.11+ and print a
    -- warning every time. jump() is the supported replacement.
    map('n', '[d', function() vim.diagnostic.jump({ count = -1, float = true }) end, 'Previous diagnostic')
    map('n', ']d', function() vim.diagnostic.jump({ count = 1, float = true }) end, 'Next diagnostic')
    map('n', '[e', function() vim.diagnostic.jump({ count = -1, float = true, severity = vim.diagnostic.severity.ERROR }) end, 'Previous error')
    map('n', ']e', function() vim.diagnostic.jump({ count = 1, float = true, severity = vim.diagnostic.severity.ERROR }) end, 'Next error')
    map('n', '<leader>k', vim.diagnostic.open_float, 'Show diagnostic under cursor')
  end,
})

-- Inlay hints (inferred types, parameter names) are most of the value of
-- rust-analyzer and ts_ls. <leader>ih toggles them per buffer.
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(args)
    local client = vim.lsp.get_client_by_id(args.data.client_id)
    if client and client:supports_method('textDocument/inlayHint') then
      vim.lsp.inlay_hint.enable(true, { bufnr = args.buf })
      vim.keymap.set('n', '<leader>ih', function()
        vim.lsp.inlay_hint.enable(
          not vim.lsp.inlay_hint.is_enabled({ bufnr = args.buf }),
          { bufnr = args.buf }
        )
      end, { buffer = args.buf, silent = true, desc = 'Toggle inlay hints' })
    end
  end,
})

-- ---------------------------------------------------------------------------
-- Shared defaults
-- ---------------------------------------------------------------------------
vim.lsp.config('*', { capabilities = capabilities })

-- ---------------------------------------------------------------------------
-- TypeScript / JavaScript / React / Next.js
-- ---------------------------------------------------------------------------
-- The inlayHints blocks are what produce the greyed-out `: string` and
-- `paramName:` annotations VSCode shows without you asking.
local ts_inlay_hints = {
  includeInlayParameterNameHints = 'literals',
  includeInlayParameterNameHintsWhenArgumentMatchesName = false,
  includeInlayFunctionParameterTypeHints = true,
  includeInlayVariableTypeHints = false,
  includeInlayPropertyDeclarationTypeHints = true,
  includeInlayFunctionLikeReturnTypeHints = true,
  includeInlayEnumMemberValueHints = true,
}

vim.lsp.config('ts_ls', {
  settings = {
    typescript = {
      inlayHints = ts_inlay_hints,
      -- prefer `import { x } from "./y"` over long relative chains
      preferences = { importModuleSpecifier = 'shortest' },
      updateImportsOnFileMove = { enabled = 'always' },
      suggest = { completeFunctionCalls = true },
    },
    javascript = {
      inlayHints = ts_inlay_hints,
      preferences = { importModuleSpecifier = 'shortest' },
      updateImportsOnFileMove = { enabled = 'always' },
      suggest = { completeFunctionCalls = true },
    },
    -- show every diagnostic, including the ones VSCode calls "suggestions"
    -- (unused variables, unreachable code)
    completions = { completeFunctionCalls = true },
  },
})

-- eslint: its code actions are what "Fix all auto-fixable problems" does.
vim.lsp.config('eslint', {
  settings = {
    workingDirectories = { mode = 'auto' },
    format = false, -- prettier formats, eslint only reports
  },
})

-- tailwindcss: also complete classes written inside clsx/cva/tw helpers, which
-- plain tailwindcss-language-server does not look at by default.
vim.lsp.config('tailwindcss', {
  filetypes = {
    'html', 'css', 'scss', 'javascript', 'javascriptreact',
    'typescript', 'typescriptreact', 'svelte', 'vue', 'astro',
  },
  settings = {
    tailwindCSS = {
      experimental = {
        classRegex = {
          { 'cva\\(([^)]*)\\)', '["\'`]([^"\'`]*).*?["\'`]' },
          { 'cx\\(([^)]*)\\)', '["\'`]([^"\'`]*).*?["\'`]' },
          { 'clsx\\(([^)]*)\\)', '["\'`]([^"\'`]*).*?["\'`]' },
          { 'cn\\(([^)]*)\\)', '["\'`]([^"\'`]*).*?["\'`]' },
          'class:\\s*?["\'`]([^"\'`]*).*?["\'`]',
        },
      },
      validate = true,
    },
  },
})

-- emmet: `div.card>p*3` then <C-y>, expands. Off by default in JSX, so list the
-- React filetypes explicitly.
vim.lsp.config('emmet_language_server', {
  filetypes = {
    'html', 'css', 'scss', 'sass', 'less',
    'javascriptreact', 'typescriptreact', 'vue', 'svelte',
  },
})

-- ---------------------------------------------------------------------------
-- JSON / YAML with real schemas
-- ---------------------------------------------------------------------------
-- schemastore turns package.json, tsconfig.json, .eslintrc, next.config,
-- GitHub workflows and so on into validated, auto-completing files.
local schemastore = require('schemastore')

vim.lsp.config('jsonls', {
  settings = {
    json = {
      schemas = schemastore.json.schemas(),
      validate = { enable = true },
    },
  },
})

vim.lsp.config('yamlls', {
  settings = {
    yaml = {
      schemaStore = { enable = false, url = '' }, -- schemastore.nvim supplies these
      schemas = schemastore.yaml.schemas(),
      validate = true,
      keyOrdering = false, -- otherwise every unsorted key is flagged
    },
  },
})

-- ---------------------------------------------------------------------------
-- Python
-- ---------------------------------------------------------------------------
vim.lsp.config('pyright', {
  settings = {
    python = {
      analysis = {
        typeCheckingMode = 'basic',
        autoSearchPaths = true,
        useLibraryCodeForTypes = true,
        diagnosticMode = 'openFilesOnly', -- workspace-wide is slow on big repos
        inlayHints = {
          variableTypes = true,
          functionReturnTypes = true,
          callArgumentNames = true,
        },
      },
    },
  },
})

-- ---------------------------------------------------------------------------
-- Lua (this config)
-- ---------------------------------------------------------------------------
vim.lsp.config('lua_ls', {
  settings = {
    Lua = {
      runtime = { version = 'LuaJIT' },
      diagnostics = { globals = { 'vim', 'load_theme', 'switch_theme' } },
      workspace = {
        library = vim.api.nvim_get_runtime_file('', true),
        checkThirdParty = false,
      },
      hint = { enable = true, arrayIndex = 'Disable' },
      telemetry = { enable = false },
    },
  },
})

-- ---------------------------------------------------------------------------
-- Rust
-- ---------------------------------------------------------------------------
-- rust_analyzer is deliberately NOT installed through Mason. It ships as a
-- rustup component, so this way its version always matches the toolchain that
-- compiles the code, and it finds rust-src through the same rustup install. A
-- separate Mason copy drifts out of sync with rustc and then fails to load the
-- standard library ("can't find crate for `std`"). It is picked up from
-- ~/.cargo/bin, which fish puts on PATH via ~/.config/fish/conf.d/rustup.fish.
vim.lsp.config('rust_analyzer', {
  settings = {
    ['rust-analyzer'] = {
      check = { command = 'clippy' },
      cargo = { allFeatures = true },
      procMacro = { enable = true },
      inlayHints = {
        bindingModeHints = { enable = false },
        closureReturnTypeHints = { enable = 'with_block' },
        parameterHints = { enable = true },
        typeHints = { enable = true },
      },
    },
  },
})
vim.lsp.enable('rust_analyzer')

-- ---------------------------------------------------------------------------
-- Install + auto-enable
-- ---------------------------------------------------------------------------
require('mason-lspconfig').setup({
  ensure_installed = {
    -- Frontend / React / Next.js / React Native (all TS/JS share ts_ls)
    "ts_ls", "cssls", "html", "tailwindcss", "emmet_language_server", "eslint",
    -- Config files you hit in every JS/TS or Rust project
    "jsonls", "yamlls", "taplo", "dockerls",
    -- Backend / scripting / docs / editing this very config
    "pyright", "lua_ls", "bashls", "marksman",
  },
})

-- Organize imports / remove unused imports, the VSCode "Organize Imports"
-- command. ts_ls exposes it as a source action.
vim.keymap.set('n', '<leader>co', function()
  vim.lsp.buf.code_action({
    context = { only = { 'source.organizeImports' }, diagnostics = {} },
    apply = true,
  })
end, { silent = true, desc = 'Organize imports' })

vim.keymap.set('n', '<leader>cF', function()
  vim.lsp.buf.code_action({
    context = { only = { 'source.fixAll' }, diagnostics = {} },
    apply = true,
  })
end, { silent = true, desc = 'Fix all auto-fixable problems' })
