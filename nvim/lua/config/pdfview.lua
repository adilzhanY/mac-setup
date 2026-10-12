-- View PDFs inside Neovim: pages are rendered to PNG on demand with pdftoppm
-- (poppler) and displayed by PicVim (kitty graphics), so each page gets
-- PicVim's zoom/pan/rotate. Extra keys in a PDF page buffer:
--   J / <PageDown>  next page        K / <PageUp>  previous page
--   gg first page                    G  last page
-- :PdfViewClearCache wipes the rendered-page cache.

local M = {}

local cache_root = vim.fn.stdpath("cache") .. "/pdfview"
local render_dpi = 150

-- page png path -> { pdf, dir, total, page }
local docs = {}

local function notify(msg, level)
  vim.notify("[pdfview] " .. msg, level or vim.log.levels.INFO)
end

local function page_png(dir, page)
  return string.format("%s/page-%04d.png", dir, page)
end

local function render_page(doc, page)
  local png = page_png(doc.dir, page)
  if vim.fn.filereadable(png) == 1 then
    return png
  end
  vim.fn.system({
    "pdftoppm", "-png", "-r", tostring(render_dpi),
    "-f", tostring(page), "-l", tostring(page),
    "-singlefile", doc.pdf, (png:gsub("%.png$", "")),
  })
  return vim.fn.filereadable(png) == 1 and png or nil
end

local function open_page(doc, page)
  page = math.max(1, math.min(page, doc.total))
  local png = render_page(doc, page)
  if not png then
    notify(("could not render page %d of %s"):format(page, doc.pdf), vim.log.levels.ERROR)
    return
  end
  docs[png] = { pdf = doc.pdf, dir = doc.dir, total = doc.total, page = page }
  vim.cmd.edit(vim.fn.fnameescape(png))
  vim.api.nvim_echo({ {
    string.format("%s  page %d/%d   [J/K pages  gg/G ends  +/- zoom  hjkl pan  o reset]",
      vim.fn.fnamemodify(doc.pdf, ":t"), page, doc.total),
    "MoreMsg",
  } }, false, {})
end

local function current_doc()
  return docs[vim.api.nvim_buf_get_name(0)]
end

function M.next_page()
  local doc = current_doc()
  if doc then open_page(doc, doc.page + 1) end
end

function M.prev_page()
  local doc = current_doc()
  if doc then open_page(doc, doc.page - 1) end
end

function M.first_page()
  local doc = current_doc()
  if doc then open_page(doc, 1) end
end

function M.last_page()
  local doc = current_doc()
  if doc then open_page(doc, doc.total) end
end

-- Intercept *.pdf before Neovim reads the binary into a buffer.
vim.api.nvim_create_autocmd("BufReadCmd", {
  pattern = "*.pdf",
  callback = function(ev)
    local pdf = vim.fn.fnamemodify(ev.file, ":p")
    vim.bo[ev.buf].buftype = "nofile"
    vim.bo[ev.buf].bufhidden = "wipe"
    for _, tool in ipairs({ "pdftoppm", "pdfinfo" }) do
      if vim.fn.executable(tool) == 0 then
        notify(tool .. " not found, install poppler", vim.log.levels.ERROR)
        return
      end
    end
    local info = vim.fn.system({ "pdfinfo", pdf })
    local total = tonumber(info:match("Pages:%s*(%d+)"))
    if not total then
      notify("could not read " .. pdf, vim.log.levels.ERROR)
      return
    end
    -- Cache keyed by path+mtime so an updated PDF re-renders.
    local dir = cache_root .. "/" .. vim.fn.sha256(pdf .. ":" .. vim.fn.getftime(pdf)):sub(1, 16)
    vim.fn.mkdir(dir, "p")
    local doc = { pdf = pdf, dir = dir, total = total }
    vim.schedule(function()
      open_page(doc, 1)
    end)
  end,
})

-- Page-navigation keys on rendered page buffers (PicVim adds zoom/pan itself).
vim.api.nvim_create_autocmd("BufEnter", {
  pattern = cache_root .. "/*.png",
  callback = function(ev)
    if not docs[vim.api.nvim_buf_get_name(ev.buf)] then
      return
    end
    vim.bo[ev.buf].bufhidden = "wipe"
    local function map(lhs, fn, desc)
      vim.keymap.set("n", lhs, fn, { buffer = ev.buf, silent = true, desc = desc })
    end
    map("J", M.next_page, "PDF: next page")
    map("<PageDown>", M.next_page, "PDF: next page")
    map("K", M.prev_page, "PDF: previous page")
    map("<PageUp>", M.prev_page, "PDF: previous page")
    map("gg", M.first_page, "PDF: first page")
    map("G", M.last_page, "PDF: last page")
  end,
})

vim.api.nvim_create_user_command("PdfViewClearCache", function()
  vim.fn.delete(cache_root, "rf")
  notify("cache cleared")
end, { desc = "Delete all rendered PDF pages" })

return M
