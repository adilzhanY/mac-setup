--useful stuff

-- close nvim-tree if it's last buffer open
vim.api.nvim_create_autocmd("BufEnter", {
	pattern = "*",
	callback = function()
		if #vim.api.nvim_list_bufs() == 1 and vim.bo.filetype == "NvimTree" then
	vim.cmd("quit")
	end
	end,
})


-- auto-create missing dirs when saving a file
--vim.api.nvim_create_autocmd("BufWritePre", {
--	pattern = "*",
--	callback = function()
--	local dir = vim.fn.expand("<afile>:p:h")
--	if vim.fn.isdirectory(dir) == 0 then
--		vim.fn.mkdir(dir, "p")
--	end
--end,
--})


-- linting when file is written to
--
-- try_lint() without arguments runs every linter that linters_by_ft lists for
-- the current filetype. If one of those binaries is not installed it raises
-- ENOENT on every single write, and autosave writes once a second, so the
-- error banner never goes away. Filter the list down to linters whose command
-- actually exists on PATH before calling try_lint.
local function available_linters()
  local ok, lint = pcall(require, "lint")
  if not ok then
    return {}
  end
  local names = lint.linters_by_ft[vim.bo.filetype] or {}
  local runnable = {}
  for _, name in ipairs(names) do
    local linter = lint.linters[name]
    local cmd = type(linter) == "table" and linter.cmd or nil
    if type(cmd) == "function" then
      cmd = cmd()
    end
    -- no resolvable cmd means nvim-lint handles it itself, so let it try
    if cmd == nil or vim.fn.executable(cmd) == 1 then
      table.insert(runnable, name)
    end
  end
  return runnable
end

vim.api.nvim_create_autocmd("BufWritePost", {
  callback = function()
    local names = available_linters()
    if #names > 0 then
      require("lint").try_lint(names)
    end
  end,
})


-- spellcheck in md
vim.api.nvim_create_autocmd("FileType", {
	pattern = "markdown",
	command = "setlocal spell wrap",
})


-- disable automatic comment on newline
vim.api.nvim_create_autocmd("FileType", {
		pattern = "*",
		callback = function()
		vim.opt_local.formatoptions:remove({ "c", "r", "o" })
		end,
})


-- highlight text on yank
vim.api.nvim_create_autocmd("TextYankPost", {
	pattern = "*",
	callback = function()
	vim.hl.on_yank({ timeout = 300 })
	end,
})


-- reload files on external change
--vim.api.nvim_create_autocmd("FocusGained", {
--	pattern = "*",
--	command = "checktime",
--})


-- restore cursor pos on file open
vim.api.nvim_create_autocmd("BufReadPost", {
	pattern = "*",
	callback = function()
	local line = vim.fn.line("'\"")
	if line > 1 and line <= vim.fn.line("$") then
		vim.cmd("normal! g'\"")
	end
end,
})

vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    local startuptime = vim.fn.reltimefloat(vim.fn.reltime(vim.g.start_time))
    vim.g.startup_time_ms = string.format("%.2f ms", startuptime * 1000)
  end,
})

vim.api.nvim_create_augroup("alpha_on_empty", { clear = true })
vim.api.nvim_create_autocmd("User", {
	pattern = "BDeletePre *",
	group = "alpha_on_empty",
	callback = function()
		local bufnr = vim.api.nvim_get_current_buf()
		local name = vim.api.nvim_buf_get_name(bufnr)
		if name == "" then
      vim.cmd([[:Alpha | bd#]])
		end
	end,
})


vim.api.nvim_create_autocmd({ "BufEnter", "FocusGained", "InsertLeave", "CmdlineLeave", "WinEnter" }, {
   pattern = "*",
   group = augroup,
   callback = function()
      if vim.o.nu and vim.api.nvim_get_mode().mode ~= "i" then
         vim.opt.relativenumber = true
      end
   end,
})

vim.api.nvim_create_autocmd({ "BufLeave", "FocusLost", "InsertEnter", "CmdlineEnter", "WinLeave" }, {
   pattern = "*",
   group = augroup,
   callback = function()
      if vim.o.nu then
         vim.opt.relativenumber = false
         -- Conditional taken from https://github.com/rockyzhang24/dotfiles/commit/03dd14b5d43f812661b88c4660c03d714132abcf
         -- Workaround for https://github.com/neovim/neovim/issues/32068
         if not vim.tbl_contains({"@", "-"}, vim.v.event.cmdtype) then
            vim.cmd "redraw"
         end
      end
   end,
})

-- Auto-restore terminal buffers that were saved in sessions
vim.api.nvim_create_autocmd("BufReadPost", {
  pattern = "*",
  callback = function()
    local bufname = vim.api.nvim_buf_get_name(0)
    -- Check if the buffer has a custom name (like "git" or "fish")
    -- and if it's empty (meaning it was saved but not a real file)
    if bufname ~= "" and vim.fn.filereadable(bufname) == 0 and vim.bo.buftype == "" then
      -- Check if the buffer name looks like a terminal name (doesn't have a path)
      if not bufname:match("/") then
        -- Convert it back to a terminal
        vim.cmd("terminal")
        vim.cmd("file " .. bufname)
      end
    end
  end,
})
