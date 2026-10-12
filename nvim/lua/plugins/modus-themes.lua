require('modus-themes').setup({
  -- Style: "auto", "modus_operandi", "modus_vivendi"
  style = 'modus_vivendi',  -- Dark theme (this is what you want!)
  
  -- Variant per style (new API; replaces the deprecated `variant` string).
  -- Options: "default", "tinted", "deuteranopia", "tritanopia"
  variants = {
    modus_operandi = 'default',
    modus_vivendi = 'default',
  },
  
  -- High contrast for better readability
  styles = {
    comments = { italic = true },
    keywords = { italic = true },
    functions = {},
    variables = {},
  },
  
  -- Transparency options
  transparent = true,  -- transparent background (matches kitty/Hyprland)
  
  -- Darker background for better contrast
  dim_inactive = false,
  
  -- Hide end-of-buffer filler lines for cleaner look
  hide_end_of_buffer = true,
  
  -- Highlight line numbers for active line
  hide_inactive_statusline = false,
})