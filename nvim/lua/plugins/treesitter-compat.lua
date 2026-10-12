-- nvim-treesitter `master` <-> Neovim 0.12 compatibility shim
-- ------------------------------------------------------------
-- The nvim-treesitter `master` branch is frozen and was never updated for the
-- treesitter query API change in Neovim 0.12: directive/predicate handlers now
-- receive `match[capture_id]` as a LIST of nodes (`TSNode[]`) instead of a single
-- `TSNode`. The frozen handlers in nvim-treesitter/query_predicates.lua still
-- treat it as one node, so they pass a plain table into get_node_text(), which
-- calls node:range() on it and throws:
--
--   Decoration provider "conceal_line" (ns=nvim.treesitter.highlighter):
--   .../vim/treesitter.lua:197: attempt to call method 'range' (a nil value)
--   ... query_predicates.lua:141: in function 'handler'
--
-- This fires on markdown/html code-fence injections (set-lang-from-info-string!),
-- which is why it pops up constantly while editing. Here we re-register the
-- affected handlers with `force = true`, normalizing match[id] to a single node
-- first (taking the last node in the list, matching Neovim's own handlers).
--
-- Remove this file (and its require in treesitter.lua) if you ever migrate to the
-- nvim-treesitter `main` branch, which handles the new API natively.

local query = require("vim.treesitter.query")

-- Make sure nvim-treesitter's own handlers are registered first, so our
-- force-registration below replaces them rather than the other way around.
pcall(require, "nvim-treesitter.query_predicates")

local opts = { force = true, all = false }

-- match[id] is `TSNode[]` on 0.12; older Neovim handed back a single TSNode.
-- Return the matched node in both cases (nil if the capture matched nothing).
local function node_of(match, id)
  local v = match[id]
  if type(v) == "table" and v.range == nil then
    return v[#v] -- list of nodes -> last matched node
  end
  return v -- already a single TSNode (older Neovim) or nil
end

local html_script_type_languages = {
  ["importmap"] = "json",
  ["module"] = "javascript",
  ["application/ecmascript"] = "javascript",
  ["text/ecmascript"] = "javascript",
}

local non_filetype_match_injection_language_aliases = {
  ex = "elixir",
  pl = "perl",
  sh = "bash",
  uxn = "uxntal",
  ts = "typescript",
}

local function get_parser_from_markdown_info_string(injection_alias)
  local match = vim.filetype.match({ filename = "a." .. injection_alias })
  return match or non_filetype_match_injection_language_aliases[injection_alias] or injection_alias
end

-- Directives (these are the ones that actually crash via get_node_text) --------

query.add_directive("set-lang-from-mimetype!", function(match, _, bufnr, pred, metadata)
  local node = node_of(match, pred[2])
  if not node then
    return
  end
  local type_attr_value = vim.treesitter.get_node_text(node, bufnr)
  local configured = html_script_type_languages[type_attr_value]
  if configured then
    metadata["injection.language"] = configured
  else
    local parts = vim.split(type_attr_value, "/", {})
    metadata["injection.language"] = parts[#parts]
  end
end, opts)

query.add_directive("set-lang-from-info-string!", function(match, _, bufnr, pred, metadata)
  local node = node_of(match, pred[2])
  if not node then
    return
  end
  local injection_alias = vim.treesitter.get_node_text(node, bufnr):lower()
  metadata["injection.language"] = get_parser_from_markdown_info_string(injection_alias)
end, opts)

query.add_directive("downcase!", function(match, _, bufnr, pred, metadata)
  local id = pred[2]
  local node = node_of(match, id)
  if not node then
    return
  end
  local text = vim.treesitter.get_node_text(node, bufnr, { metadata = metadata[id] }) or ""
  if not metadata[id] then
    metadata[id] = {}
  end
  metadata[id].text = string.lower(text)
end, opts)

-- Predicates (same list-vs-node hazard if these queries are ever exercised) ----

query.add_predicate("nth?", function(match, _pattern, _bufnr, pred)
  local node = node_of(match, pred[2])
  local n = tonumber(pred[3])
  if node and node:parent() and node:parent():named_child_count() > n then
    return node:parent():named_child(n) == node
  end
  return false
end, opts)

query.add_predicate("is?", function(match, _pattern, bufnr, pred)
  local locals = require("nvim-treesitter.locals")
  local node = node_of(match, pred[2])
  local types = { unpack(pred, 3) }
  if not node then
    return true
  end
  local _, _, kind = locals.find_definition(node, bufnr)
  return vim.tbl_contains(types, kind)
end, opts)

query.add_predicate("kind-eq?", function(match, _pattern, _bufnr, pred)
  local node = node_of(match, pred[2])
  local types = { unpack(pred, 3) }
  if not node then
    return true
  end
  return vim.tbl_contains(types, node:type())
end, opts)
