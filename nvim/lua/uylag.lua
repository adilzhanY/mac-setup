local M = {}

M.setup = function()
  vim.cmd('highlight clear')
  if vim.fn.exists('syntax_on') then
    vim.cmd('syntax reset')
  end

  vim.g.colors_name = 'uylag'
  vim.o.termguicolors = true

  local M_palette = {}
  M_palette.bg = "#0b0a12"
  M_palette.bg2 = "#12101f"
  M_palette.panel = "#1a1530"
  M_palette.sel_bg = "#2a1f4d"
  M_palette.fg = "#ebe6ff"
  M_palette.fg_dim = "#c4bddf"
  M_palette.comment = "#8f87b2"
  M_palette.purple = "#9d72ff"
  M_palette.purple2 = "#c3a6ff"
  M_palette.purple3 = "#6f4ec2"
  M_palette.violet = "#4b347f"
  M_palette.magenta = "#d58aff"
  M_palette.rose = "#e6b0ff"
  M_palette.error = "#ff7ab3"
  M_palette.warn = "#caa2ff"
  M_palette.info = "#9d72ff"
  M_palette.hint = "#7a60c8"

  local function hi(group, opts)
    local cmd = 'highlight ' .. group
    if opts.fg then cmd = cmd .. ' guifg=' .. opts.fg end
    if opts.bg then cmd = cmd .. ' guibg=' .. opts.bg end
    if opts.style then cmd = cmd .. ' gui=' .. opts.style end
    if opts.sp then cmd = cmd .. ' guisp=' .. opts.sp end
    vim.cmd(cmd)
  end

  hi('Normal', { fg = M_palette.fg, bg = M_palette.bg })
  hi('NormalFloat', { fg = M_palette.fg, bg = M_palette.bg2 })
  hi('FloatBorder', { fg = M_palette.purple3, bg = M_palette.bg2 })
  hi('NormalNC', { fg = M_palette.fg, bg = M_palette.bg })
  
  hi('Cursor', { fg = M_palette.bg, bg = M_palette.fg })
  hi('CursorLine', { bg = M_palette.bg2 })
  hi('CursorLineNr', { fg = M_palette.purple, bg = M_palette.bg2, style = 'bold' })
  hi('LineNr', { fg = M_palette.comment, bg = M_palette.bg })
  hi('SignColumn', { bg = M_palette.bg })
  hi('ColorColumn', { bg = M_palette.bg2 })
  hi('VertSplit', { fg = M_palette.sel_bg, bg = M_palette.bg })
  hi('StatusLine', { fg = M_palette.fg, bg = M_palette.panel })
  hi('StatusLineNC', { fg = M_palette.fg_dim, bg = M_palette.bg2 })
  hi('TabLine', { fg = M_palette.fg_dim, bg = M_palette.bg2 })
  hi('TabLineFill', { bg = M_palette.bg })
  hi('TabLineSel', { fg = M_palette.fg, bg = M_palette.panel, style = 'bold' })
  
  hi('Visual', { bg = M_palette.sel_bg })
  hi('VisualNOS', { bg = M_palette.sel_bg })
  hi('Search', { fg = M_palette.bg, bg = M_palette.purple })
  hi('IncSearch', { fg = M_palette.bg, bg = M_palette.magenta })
  hi('CurSearch', { fg = M_palette.bg, bg = M_palette.magenta })
  
  hi('Pmenu', { fg = M_palette.fg, bg = M_palette.panel })
  hi('PmenuSel', { fg = M_palette.fg, bg = M_palette.sel_bg })
  hi('PmenuSbar', { bg = M_palette.bg2 })
  hi('PmenuThumb', { bg = M_palette.comment })
  
  hi('ErrorMsg', { fg = M_palette.error, bg = M_palette.bg, style = 'bold' })
  hi('WarningMsg', { fg = M_palette.warn, bg = M_palette.bg })
  hi('ModeMsg', { fg = M_palette.purple, bg = M_palette.bg, style = 'bold' })
  hi('MoreMsg', { fg = M_palette.purple, bg = M_palette.bg })
  hi('Question', { fg = M_palette.fg, bg = M_palette.bg })
  
  hi('DiffAdd', { fg = M_palette.fg, bg = M_palette.violet })
  hi('DiffChange', { fg = M_palette.fg, bg = M_palette.sel_bg })
  hi('DiffDelete', { fg = M_palette.comment, bg = M_palette.bg })
  hi('DiffText', { fg = M_palette.bg, bg = M_palette.fg })
  
  hi('SpellBad', { sp = M_palette.error, style = 'undercurl' })
  hi('SpellCap', { sp = M_palette.warn, style = 'undercurl' })
  hi('SpellLocal', { sp = M_palette.info, style = 'undercurl' })
  hi('SpellRare', { sp = M_palette.info, style = 'undercurl' })
  
  hi('Comment', { fg = M_palette.comment, style = 'italic' })
  hi('Constant', { fg = M_palette.purple2 })
  hi('String', { fg = M_palette.rose })
  hi('Character', { fg = M_palette.rose })
  hi('Number', { fg = M_palette.magenta })
  hi('Boolean', { fg = M_palette.magenta })
  hi('Float', { fg = M_palette.magenta })
  
  hi('Identifier', { fg = M_palette.fg })
  hi('Function', { fg = M_palette.purple, style = 'bold' })
  hi('Statement', { fg = M_palette.purple, style = 'bold' })
  hi('Conditional', { fg = M_palette.purple, style = 'bold' })
  hi('Repeat', { fg = M_palette.purple, style = 'bold' })
  hi('Label', { fg = M_palette.purple3 })
  hi('Operator', { fg = M_palette.purple3 })
  hi('Keyword', { fg = M_palette.purple, style = 'bold' })
  hi('Exception', { fg = M_palette.error, style = 'bold' })
  
  hi('PreProc', { fg = M_palette.magenta })
  hi('Include', { fg = M_palette.purple, style = 'bold' })
  hi('Define', { fg = M_palette.magenta })
  hi('Macro', { fg = M_palette.magenta })
  hi('PreCondit', { fg = M_palette.magenta })
  
  hi('Type', { fg = M_palette.purple2, style = 'bold' })
  hi('StorageClass', { fg = M_palette.purple2 })
  hi('Structure', { fg = M_palette.purple2 })
  hi('Typedef', { fg = M_palette.purple2 })
  
  hi('Special', { fg = M_palette.purple2 })
  hi('SpecialChar', { fg = M_palette.purple2 })
  hi('Tag', { fg = M_palette.purple2, style = 'bold' })
  hi('Delimiter', { fg = M_palette.fg_dim })
  hi('SpecialComment', { fg = M_palette.comment, style = 'italic' })
  hi('Debug', { fg = M_palette.fg })
  
  hi('Underlined', { fg = M_palette.fg, style = 'underline' })
  hi('Ignore', { fg = M_palette.comment })
  hi('Error', { fg = M_palette.error, bg = M_palette.sel_bg, style = 'bold' })
  hi('Todo', { fg = M_palette.bg, bg = M_palette.warn, style = 'bold' })
  
  hi('@variable', { fg = M_palette.fg })
  hi('@variable.builtin', { fg = M_palette.fg_dim, style = 'italic' })
  hi('@variable.parameter', { fg = M_palette.fg_dim })
  hi('@variable.member', { fg = M_palette.fg_dim })
  hi('@constant', { fg = M_palette.purple2 })
  hi('@string', { fg = M_palette.rose })
  hi('@number', { fg = M_palette.magenta })
  hi('@function', { fg = M_palette.purple, style = 'bold' })
  hi('@method', { fg = M_palette.purple, style = 'bold' })
  hi('@keyword', { fg = M_palette.purple, style = 'bold' })
  hi('@type', { fg = M_palette.purple2, style = 'bold' })
  hi('@property', { fg = M_palette.fg_dim })
  hi('@comment', { fg = M_palette.comment, style = 'italic' })
  hi('@punctuation.delimiter', { fg = M_palette.fg_dim })
  
  hi('LspReferenceText', { bg = M_palette.bg2 })
  hi('LspReferenceRead', { bg = M_palette.bg2 })
  hi('LspReferenceWrite', { bg = M_palette.bg2 })
  hi('DiagnosticError', { fg = M_palette.error })
  hi('DiagnosticWarn', { fg = M_palette.warn })
  hi('DiagnosticInfo', { fg = M_palette.info })
  hi('DiagnosticHint', { fg = M_palette.hint })
  
  hi('GitSignsAdd', { fg = M_palette.purple, bg = M_palette.bg })
  hi('GitSignsChange', { fg = M_palette.warn, bg = M_palette.bg })
  hi('GitSignsDelete', { fg = M_palette.error, bg = M_palette.bg })
  
  hi('NvimTreeNormal', { fg = M_palette.fg, bg = M_palette.bg })
  hi('TelescopeNormal', { fg = M_palette.fg, bg = M_palette.bg })
  
  -- Render Markdown
  hi('RenderMarkdownH1', { fg = M_palette.fg, style = 'bold' })
  hi('RenderMarkdownH2', { fg = M_palette.fg, style = 'bold' })
  hi('RenderMarkdownH3', { fg = M_palette.fg, style = 'bold' })
  hi('RenderMarkdownH4', { fg = M_palette.fg, style = 'bold' })
  hi('RenderMarkdownH5', { fg = M_palette.fg, style = 'bold' })
  hi('RenderMarkdownH6', { fg = M_palette.fg, style = 'bold' })
end

M.colors = {
  bg = "#0b0a12",
  fg = "#ebe6ff",
  normal = {
    a = { bg = "#6f4ec2", fg = "#0b0a12", gui = "bold" },
    b = { bg = "#1a1530", fg = "#ebe6ff" },
    c = { bg = "#12101f", fg = "#c4bddf" }
  },
  insert = {
    a = { bg = "#9d72ff", fg = "#0b0a12", gui = "bold" },
    b = { bg = "#1a1530", fg = "#ebe6ff" },
    c = { bg = "#12101f", fg = "#c4bddf" }
  },
  visual = {
    a = { bg = "#d58aff", fg = "#0b0a12", gui = "bold" },
    b = { bg = "#1a1530", fg = "#ebe6ff" },
    c = { bg = "#12101f", fg = "#c4bddf" }
  }
}

return M