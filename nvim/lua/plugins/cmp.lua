-- Completion, snippets and the in-line hints that make this feel like VSCode.
--
-- What each piece gives you:
--   nvim_lsp      -> real, type-aware suggestions + auto-import
--   luasnip       -> snippet expansion (see lua/config/snippets.lua)
--   buffer / path -> words already in the file, and filesystem paths
--   lspkind       -> the little icon per kind, like VSCode's list
--
-- The parameter popup while you are inside foo(|) is not a cmp source. It
-- lives in lua/plugins/signature.lua, on top of vim.lsp.buf.signature_help().

local cmp = require('cmp')
local luasnip = require('luasnip')
local lspkind = require('lspkind')

-- friendly-snippets ships VSCode-format snippets for every language you use.
require("luasnip.loaders.from_vscode").lazy_load()

luasnip.setup({
  history = true,
  -- keep snippet jump points alive while you keep typing in the field
  updateevents = "TextChanged,TextChangedI",
  delete_check_events = "TextChanged",
  enable_autosnippets = false,
})

-- menuone: show the menu even for a single match, so you can read the docs.
-- noselect: nothing is preselected, so <CR> stays a plain newline until you
-- actually pick something with <Tab> or the arrows.
vim.opt.completeopt = { "menu", "menuone", "noselect" }
vim.opt.pumheight = 12 -- cap the popup so it never covers the whole file

-- How see-through the completion popup is, 0 opaque to 100 fully transparent.
-- This is the one number to change if you want more or less of it.
--
-- What it actually does, which is not quite what "transparency" suggests:
-- anywhere the popup draws a BLANK cell, the code underneath shows through, so
-- you read your own file in the gaps between "Function" and "futimes" and out
-- to the right of "[LSP]". The popup's own text always stays solid on top.
--
-- It also tints the popup with whatever sits behind it, but that part does
-- nothing here: blending needs a real colour to mix with, and Normal has no
-- background (that is what makes the editor see-through), so Neovim mixes
-- toward black instead and the popup just darkens a little. The text coming
-- through the gaps is the part you will actually notice.
local POPUP_BLEND = 20

-- cmp.config.window.bordered() does not forward winblend, so fold it in after.
--
-- The border is named explicitly because bordered() asks vim.o.winborder for
-- one, that option is empty here, and it then falls back to "none". So despite
-- the function name these popups have never actually had a border. With the
-- popup now see-through, the edge is worth drawing: it is the only thing
-- separating the suggestion list from the code showing through behind it.
local function glass(opts)
  return vim.tbl_extend("force",
    cmp.config.window.bordered(vim.tbl_extend("force", { border = "rounded" }, opts)),
    { winblend = POPUP_BLEND })
end

-- the built-in popup menu, used for cmdline completion, matches
vim.o.pumblend = POPUP_BLEND

local function has_words_before()
  local line, col = unpack(vim.api.nvim_win_get_cursor(0))
  if col == 0 then return false end
  return vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
end

cmp.setup({
  snippet = {
    expand = function(args) luasnip.lsp_expand(args.body) end,
  },

  -- bordered popups, and the documentation pane VSCode shows on the right
  window = {
    completion = glass({
      winhighlight = "Normal:Normal,FloatBorder:FloatBorder,CursorLine:PmenuSel,Search:None",
    }),
    documentation = glass({
      winhighlight = "Normal:Normal,FloatBorder:FloatBorder,Search:None",
    }),
  },

  formatting = {
    fields = { "kind", "abbr", "menu" },
    format = lspkind.cmp_format({
      mode = "symbol_text",
      maxwidth = 50,
      ellipsis_char = "...",
      show_labelDetails = true, -- the "(auto-import from ./foo)" hint
      menu = {
        nvim_lsp = "[LSP]",
        luasnip = "[snip]",
        buffer = "[buf]",
        path = "[path]",
      },
    }),
  },

  -- LSP results first, snippets next, dumb word matches last.
  sources = cmp.config.sources({
    { name = 'nvim_lsp', priority = 1000 },
    { name = 'luasnip', priority = 800 },
  }, {
    { name = 'buffer', priority = 500, keyword_length = 3 },
    { name = 'path', priority = 400 },
  }),

  mapping = cmp.mapping.preset.insert({
    ['<C-n>'] = cmp.mapping.select_next_item(),
    ['<C-p>'] = cmp.mapping.select_prev_item(),
    ['<C-d>'] = cmp.mapping.scroll_docs(4),
    ['<C-u>'] = cmp.mapping.scroll_docs(-4),
    ['<C-Space>'] = cmp.mapping.complete(),
    ['<C-e>'] = cmp.mapping.abort(),

    -- select = false is the important bit: <CR> only accepts something you
    -- deliberately selected. Before this, pressing Enter to break a line would
    -- silently paste whatever happened to be first in the menu.
    ['<CR>'] = cmp.mapping.confirm({ select = false }),

    -- Tab behaves like VSCode: accept/advance if there is something to accept,
    -- otherwise insert a real tab.
    ['<Tab>'] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      elseif luasnip.expand_or_locally_jumpable() then
        luasnip.expand_or_jump()
      elseif has_words_before() then
        cmp.complete()
      else
        fallback()
      end
    end, { 'i', 's' }),

    ['<S-Tab>'] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_prev_item()
      elseif luasnip.locally_jumpable(-1) then
        luasnip.jump(-1)
      else
        fallback()
      end
    end, { 'i', 's' }),
  }),

  experimental = {
    ghost_text = { hl_group = "Comment" }, -- greyed-out preview of the match
  },
})

-- Completion on the command line too: `:` completes commands, `/` completes
-- words from the buffer.
cmp.setup.cmdline({ '/', '?' }, {
  mapping = cmp.mapping.preset.cmdline(),
  sources = { { name = 'buffer' } },
})

cmp.setup.cmdline(':', {
  mapping = cmp.mapping.preset.cmdline(),
  sources = cmp.config.sources(
    { { name = 'path' } },
    { { name = 'cmdline' } }
  ),
})

-- Typing `(` after confirming a function should add the closing paren.
local ok, cmp_autopairs = pcall(require, 'nvim-autopairs.completion.cmp')
if ok then
  cmp.event:on('confirm_done', cmp_autopairs.on_confirm_done())
end

-- LSP progress in the corner, so a slow ts_ls start is visible instead of
-- looking like completion is broken.
require("fidget").setup({
  notification = { window = { winblend = 0 } },
})
