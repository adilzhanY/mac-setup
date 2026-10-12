local devicons_setup_ok, devicons = pcall(require, "nvim-web-devicons")
if not devicons_setup_ok then
  return
end

-- Your devicons setup - E-ink style (all icons white)
devicons.setup({
  color_icons = true,
  default = true,
  strict = true,
  override = {
    -- Default icon for unknown files
    default_icon = {
      icon = "",
      color = "#FFFFFF",
      name = "Default"
    }
  },
  override_by_extension = {
    -- Override ALL file extensions to use white color
    ["lua"] = { icon = "", color = "#FFFFFF", name = "Lua" },
    ["py"] = { icon = "", color = "#FFFFFF", name = "Py" },
    ["vim"] = { icon = "", color = "#FFFFFF", name = "Vim" },
    ["md"] = { icon = "", color = "#FFFFFF", name = "Markdown" },
    ["txt"] = { icon = "", color = "#FFFFFF", name = "Text" },
    ["sh"] = { icon = "", color = "#FFFFFF", name = "Shell" },
    ["fish"] = { icon = "", color = "#FFFFFF", name = "Fish" },
    ["yaml"] = { icon = "", color = "#FFFFFF", name = "Yaml" },
    ["yml"] = { icon = "", color = "#FFFFFF", name = "Yaml" },
    ["toml"] = { icon = "", color = "#FFFFFF", name = "Toml" },
    ["conf"] = { icon = "", color = "#FFFFFF", name = "Conf" },
    ["ini"] = { icon = "󰮮", color = "#FFFFFF", name = "Ini" },
    ["git"] = { icon = "", color = "#FFFFFF", name = "Git" },
    ["gitignore"] = { icon = "", color = "#FFFFFF", name = "GitIgnore" },
  }
})

-- Custom icon overrides - ALL WHITE
devicons.set_icon({
  js = {
    icon = "",
    color = "#FFFFFF",
    name = "Js"
  },
  tsx = {
      icon = "",
      color = "#FFFFFF",
      name = "Tsx"
  },
  css = {
      icon = "",
      color = "#FFFFFF",
      name = "Css"
  },
  rust = {
      icon = "󱘗",
      color = "#FFFFFF",
      name = "Rust"
  },
  jsx = {
      icon = "",
      color = "#FFFFFF",
      name = "Jsx"
  },
  json = {
      icon = "",
      color = "#FFFFFF",
      name = "Json"
  },
  jsonc = {
      icon = "",
      color = "#FFFFFF",
      name = "Jsonc"
  },
  ts = {
      icon = "",
      color = "#FFFFFF",
      name = "Ts"
  },
  html = {
      icon = "",
      color = "#FFFFFF",
      name = "Html"
  },
  go = {
      icon = "󰟓",
      color = "#FFFFFF",
      name = "Go"
  },
  java = {
      icon = "",
      color = "#FFFFFF",
      name = "Java"
  },
  c = {
      icon = "",
      color = "#FFFFFF",
      name = "C"
  },
  cpp = {
      icon = "",
      color = "#FFFFFF",
      name = "Cpp"
  },
})

-- devicons.refresh() is not strictly necessary here since we are setting up
-- before nvim-tree loads, but it doesn't hurt.


-- =================================================================
-- NOW CONFIGURE NVIM-TREE
-- =================================================================

local nvim_tree_setup_ok, nvim_tree = pcall(require, "nvim-tree")
if not nvim_tree_setup_ok then
  return
end

nvim_tree.setup({
  filters ={
    dotfiles = false,
    custom = {}
  },
  git = {
    ignore = false,
  },
  -- Tells nvim-tree to use the icons setup above
  renderer = {
    icons = {
      show = {
        file = true,
        folder = true,
        folder_arrow = true,
        git = true,
      },
      glyphs = {
        folder = {
          arrow_closed = "", -- Using a simple arrow for better compatibility
          arrow_open = "",
          default = "",
          open = "",
          empty = "",
          empty_open = "",
          symlink = "",
          symlink_open = "",
        },
        git = {
          unstaged = "✗",
          staged = "✓",
          unmerged = "",
          renamed = "➜",
          untracked = "★",
          deleted = "",
          ignored = "◌",
        },
      },
    },
  },
  -- It's generally better to let devicons handle all file icons.
  -- The `web_devicons` key inside `renderer.icons` is deprecated.
  -- The default behavior is to use nvim-web-devicons if it's available.
  -- So we can remove the explicit `web_devicons` table.

  view = {
    width = 25,
    side = 'left',
  },
  sync_root_with_cwd = false,
  respect_buf_cwd = false,
  update_cwd = false,
  update_focused_file = {
    enable = true,
    update_cwd = false,
    update_root = false,
  },
})
