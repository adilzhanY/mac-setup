local npairs = require('nvim-autopairs')

npairs.setup({
    disable_in_macro = true, -- disable when recording or executing a macro
    disable_in_visualblock = false, -- disable when insert after visual block mode
    disable_in_replace_mode = true,
    ignored_next_char = [=[[%w%%%'%[%"%.%`%$]]=],
    enable_moveright = true,
    enable_afterquote = true, -- add bracket pairs after quote
    enable_check_bracket_line = true, --- check bracket in same line
    enable_bracket_in_quote = true, --
    enable_abbr = false, -- trigger abbreviation
    break_undo = true, -- switch for basic rule break undo sequence
    check_ts = true,
    ts_config = {
        lua = { 'string' },
        javascript = { 'template_string' },
        java = false,
    },
    disable_filetype = { "TelescopePrompt", "spectre_panel" },
    map_cr = true,
    map_bs = true, -- map the <BS> key
    map_c_h = false, -- Map the <C-h> key to delete a pair
    map_c_w = false, -- map <c-w> to delete a pair if possible
})

-- It prevents nvim-autopairs from creating a closing ">" when you type "<"
local Rule = require('nvim-autopairs.rule')
npairs.add_rules({
    Rule("<", ">"):with_pair(function(opts)
        local pair = opts.line:sub(opts.col - 1, opts.col)
        -- Only auto-close if it's not a JSX/TSX file, letting autotag handle it
        if vim.bo.filetype == 'javascriptreact' or vim.bo.filetype == 'typescriptreact' then
            return false
        end
        return pair == '<>'
    end)
})
