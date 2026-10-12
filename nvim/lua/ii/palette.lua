-- Parses the Material You palette that end-4 (Quickshell "ii") regenerates
-- on every wallpaper change / light-dark toggle.

local M = {}

M.path = vim.fn.expand("~/.local/state/quickshell/user/generated/material_colors.scss")

-- keys that must be present and valid, otherwise the file is missing/torn
local sentinels = { "onSurface", "primary", "error", "surfaceContainer", "term0", "term15" }

---@return {colors: table<string,string>, darkmode: boolean}|nil, string|nil
function M.load()
	local f = io.open(M.path, "r")
	if not f then
		return nil, "ii: cannot read palette file: " .. M.path
	end

	local colors = {}
	local darkmode = true
	for line in f:lines() do
		local key, value = line:match("^%$([%w_]+):%s*(.-)%s*;")
		if key == "darkmode" then
			darkmode = value == "True"
		elseif key and value:match("^#%x%x%x%x%x%x$") then
			colors[key] = value
		end
	end
	f:close()

	for _, key in ipairs(sentinels) do
		if not colors[key] then
			return nil, "ii: palette file incomplete (missing $" .. key .. ")"
		end
	end

	return { colors = colors, darkmode = darkmode }
end

return M
