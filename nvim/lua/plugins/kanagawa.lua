require('kanagawa').setup({
    compile = false,
    undercurl = true,
    commentStyle = { italic = true },
    functionStyle = {},
    keywordStyle = { italic = true },
    statementStyle = { bold = true },
    typeStyle = {},
    transparent = true,
    dimInactive = false,
    terminalColors = true,
    theme = "wave", -- "wave", "dragon", or "lotus"
    background = {
        dark = "wave", -- try "dragon" for late-night coding!
        light = "lotus"
    },
})