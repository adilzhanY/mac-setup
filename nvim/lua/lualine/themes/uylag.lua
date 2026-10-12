local M_palette = {
  bg = "#0b0a12",
  bg2 = "#12101f",
  panel = "#1a1530",
  sel_bg = "#2a1f4d",
  fg = "#ebe6ff",
  fg_dim = "#c4bddf",
  comment = "#8f87b2",
  purple = "#9d72ff",
  purple2 = "#c3a6ff",
  purple3 = "#6f4ec2",
  violet = "#4b347f",
  magenta = "#d58aff",
  rose = "#e6b0ff",
  error = "#ff7ab3",
  warn = "#caa2ff",
  info = "#9d72ff",
  hint = "#7a60c8"
}

return {
  normal = {
    a = { bg = M_palette.purple3, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  insert = {
    a = { bg = M_palette.purple, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  visual = {
    a = { bg = M_palette.magenta, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  replace = {
    a = { bg = M_palette.error, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  command = {
    a = { bg = M_palette.warn, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  terminal = {
    a = { bg = M_palette.purple, fg = M_palette.bg, gui = 'bold' },
    b = { bg = M_palette.panel, fg = M_palette.fg },
    c = { bg = M_palette.bg2, fg = M_palette.fg_dim },
  },
  inactive = {
    a = { bg = M_palette.bg, fg = M_palette.comment },
    b = { bg = M_palette.bg, fg = M_palette.comment },
    c = { bg = M_palette.bg, fg = M_palette.comment },
  },
}