require'nvim-treesitter.configs'.setup {
	ensure_installed = {
		-- web
		"javascript", "typescript", "tsx", "jsdoc", "html", "css", "scss", "graphql",
		-- config formats you open constantly in these projects
		"json", "jsonc", "yaml", "toml", "dockerfile",
		-- backend / systems
		"python", "rust", "go", "c", "cpp", "java", "bash", "sql",
		-- editing this config, and git
		"lua", "vim", "vimdoc", "query", "regex", "diff", "gitcommit", "gitignore",
		-- prose
		"markdown", "markdown_inline",
	},
	sync_install = false,
	auto_install = true,
	highlight = {
		enable = true,
    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
		additional_vim_regex_highlighting = false,
	},
	-- NOTE: treesitter's indent module is DISABLED on purpose.
	-- The nvim-treesitter `master` branch is incompatible with Neovim 0.12:
	-- nvim_treesitter#indent() throws in query_predicates.lua and returns 0,
	-- which made <CR>/o drop the cursor to column 0 inside functions/JSX.
	-- With it off, Neovim's native (filetype) indentexpr handles JS/TS/JSX/
	-- HTML/CSS/Python/Lua correctly. Highlighting/folding still use treesitter.
	indent = {
		enable = false,
	},
	incremental_selection = {
		enable = true,
		keymaps = {
		init_selection = "gnn", -- set to `false` to disable one of the mappings
		node_incremental = "grn",
		scope_incremental = "grc",
		node_decremental = "grm",
		},
	},
}

-- Patch the frozen master-branch query handlers so they stop throwing
-- "attempt to call method 'range' (a nil value)" on Neovim 0.12. See the file
-- for the full explanation.
require("plugins.treesitter-compat")
