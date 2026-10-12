-- PicVim: view images (png/jpg/gif/bmp/ico) inside Neovim via the kitty
-- graphics protocol. Keys in an image buffer:
--   =/+ zoom in   -/_ zoom out   hjkl/arrows pan   t/T rotate   o reset   r redraw

-- PicVim opens the tty at require-time, so skip it when stdout is not a
-- terminal (headless runs like `nvim --headless +PlugInstall`).
if vim.uv.guess_handle(1) ~= "tty" then
  return
end

require("picvim").setup()
