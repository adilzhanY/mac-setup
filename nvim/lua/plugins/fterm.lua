local fterm = require("FTerm")

fterm.setup({
	cmd = 'fish'
})

_G.htop = fterm:new({
	ft = 'fterm_htop',
	cmd = "htop"
})
