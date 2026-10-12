require('auto-session').setup({
  log_level = 'error',
  auto_session_enable_last_session = false,
  auto_session_root_dir = vim.fn.stdpath('data')..'/sessions/',
  auto_session_enabled = true,
  auto_save_enabled = true,
  auto_restore_enabled = true,
  auto_session_suppress_dirs = { '~/', '~/Downloads', '/' },
  auto_session_use_git_branch = false,
  bypass_session_save_file_types = { 'terminal' },
  pre_save_cmds = {
    function()
      for _, buf in ipairs(vim.api.nvim_list_bufs()) do
        if vim.bo[buf].buftype == 'terminal' then
          vim.api.nvim_buf_delete(buf, { force = true })
        end
      end
    end
  }
})
