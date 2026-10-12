-- craftzdog's Solarized Osaka.
--
-- `transparent = true` is already the theme's default, which is why the main
-- editor background was see-through before this file existed. What was still
-- solid were the sidebar and float backgrounds: the theme paints those from
-- bg_sidebar / bg_float, two colours that the `transparent` flag deliberately
-- does not touch. Setting both styles to "transparent" makes it compute those
-- as `none` instead, so nvim-tree, the quickfix list, :help and every LSP
-- float show the terminal through them the way `ii` does.
--
-- The barbar tabline and the inline diagnostic text are painted from yet more
-- colours that no option covers. config/transparent.lua clears those.
require('solarized-osaka').setup({
  transparent = true,
  terminal_colors = true,
  styles = {
    comments = { italic = true },
    keywords = { italic = true },
    functions = {},
    variables = {},
    sidebars = "transparent", -- nvim-tree, quickfix, :help
    floats = "transparent",   -- LSP hover, signature help, which-key
  },
  sidebars = { "qf", "help" },
  hide_inactive_statusline = false,
  dim_inactive = false,
})
