-- Smooth animated scrolling
-- Animates <C-u> <C-d> <C-b> <C-f> <C-y> <C-e> zt zz zb by default.

require("neoscroll").setup({
	hide_cursor = true,          -- hide cursor while scrolling
	stop_eof = true,             -- stop at <EOF> when scrolling downwards
	respect_scrolloff = false,   -- let the cursor reach the edge despite scrolloff
	cursor_scrolls_alone = true, -- scroll the window even if the cursor can't move further
	easing = "sine",             -- easing curve for the animation
	duration_multiplier = 1.0,   -- lower = faster animation (e.g. 0.7), higher = slower
})
