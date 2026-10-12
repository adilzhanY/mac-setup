-- Automatic signature help: the parameter popup that appears while the cursor
-- is inside a call, foo(|), and follows you from argument to argument.
--
-- This replaces cmp-nvim-lsp-signature-help, which called the dot form
-- `client.request(method, ...)`. Neovim 0.11 deprecated that in favour of
-- `client:request(method, ...)`, so every keystroke inside a call printed
--   client.request is deprecated. Run ":checkhealth vim.deprecated"
-- across the bottom of the screen. The function below uses
-- vim.lsp.buf.signature_help(), which is the supported path and also renders a
-- real float with the active parameter highlighted, rather than stuffing the
-- signature into the completion menu as list entries.

local M = {}

local group = vim.api.nvim_create_augroup("AutoSignatureHelp", { clear = true })
local timer = assert(vim.uv.new_timer())
local DEBOUNCE_MS = 100

-- Is the cursor inside an unclosed call on this line?
--
-- A cheap paren count is enough here and costs nothing per keystroke. It walks
-- the text to the left of the cursor and skips anything inside a string, so a
-- literal "(" in `t("(")` does not keep the popup open forever.
-- M._inside_call at the bottom of this file exposes this for the config test
local function inside_call(line, col)
  local depth = 0
  local quote = nil
  local n = 1
  while n <= col do
    local ch = line:sub(n, n)
    if quote then
      if ch == "\\" then
        n = n + 1 -- skip the escaped character
      elseif ch == quote then
        quote = nil
      end
    elseif ch == '"' or ch == "'" or ch == "`" then
      quote = ch
    elseif ch == "(" then
      depth = depth + 1
    elseif ch == ")" then
      depth = depth - 1
    end
    n = n + 1
  end
  return depth > 0
end

local function has_signature_client(buf)
  for _, client in ipairs(vim.lsp.get_clients({ bufnr = buf })) do
    if client:supports_method("textDocument/signatureHelp") then
      return true
    end
  end
  return false
end

local function update()
  if vim.api.nvim_get_mode().mode:sub(1, 1) ~= "i" then return end

  local buf = vim.api.nvim_get_current_buf()
  if not has_signature_client(buf) then return end

  -- The completion menu and the signature float fight for the same space, and
  -- cmp wins on usefulness while you are picking a name.
  local ok, cmp = pcall(require, "cmp")
  if ok and cmp.visible() then return end

  local row, col = unpack(vim.api.nvim_win_get_cursor(0))
  local line = vim.api.nvim_buf_get_lines(buf, row - 1, row, false)[1] or ""
  if not inside_call(line, col) then return end

  vim.lsp.buf.signature_help({
    border = "rounded",
    focusable = false, -- never steal the cursor out of insert mode
    silent = true,     -- no "no signature help available" spam
    close_events = { "InsertLeave", "BufHidden", "WinLeave" },
    max_width = 80,
    max_height = 12,
  })
end

function M.setup()
  vim.api.nvim_create_autocmd({ "TextChangedI", "CursorMovedI" }, {
    group = group,
    callback = function()
      timer:stop()
      timer:start(DEBOUNCE_MS, 0, vim.schedule_wrap(function()
        pcall(update)
      end))
    end,
  })

  vim.api.nvim_create_autocmd("InsertLeave", {
    group = group,
    callback = function() timer:stop() end,
  })
end

M.setup()

-- Exposed only so the paren logic above can be unit tested.
M._inside_call = inside_call

return M
