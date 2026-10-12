require("ibl").setup({
  indent = {
    char = "│", -- The character for indent lines
    tab_char = "│",
  },
  scope = {
    enabled = true, -- Highlight the current scope
    show_start = true, -- Show line at start of scope
    show_end = true, -- Show line at end of scope
    char = "│",
  },
  exclude = {
    filetypes = {
      "help",
      "alpha",
      "dashboard",
      "nvim-tree",
      "Trouble",
      "lazy",
      "mason",
    },
  },
})