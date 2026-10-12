-- Hand-written snippets, on top of friendly-snippets.
--
-- The React ones reuse the prefixes from the VSCode extension
-- "ES7+ React/Redux/React-Native snippets", so the muscle memory carries over:
-- type `rafce` then <Tab>. Component snippets fill the name from the filename,
-- the same way that extension did.
--
-- <Tab> expands and jumps forward through the fields, <S-Tab> jumps back.
-- `<leader>sn` lists every snippet available in the current buffer.
--
-- Most snippets below are written in plain LSP snippet syntax ($1, ${1:default},
-- $0) through parse_snippet, which is the exact format VSCode uses. The ones
-- that need to compute something (the component name, a capitalised setter) are
-- built from nodes instead.

local ls = require("luasnip")
local s = ls.snippet
local t = ls.text_node
local i = ls.insert_node
local f = ls.function_node
local ps = ls.parser.parse_snippet

-- Component name from the filename: app/profile/page.tsx -> Page,
-- components/user-card.tsx -> UserCard, index.tsx -> the parent folder's name.
local function component_name()
  return f(function()
    local name = vim.fn.expand("%:t:r")
    if name == "" then return "Component" end
    if name == "index" then
      name = vim.fn.expand("%:p:h:t")
      if name == "" then return "Component" end
    end
    local parts = {}
    for word in name:gmatch("[^%-%_%.%s]+") do
      table.insert(parts, word:sub(1, 1):upper() .. word:sub(2))
    end
    local out = table.concat(parts)
    return out == "" and "Component" or out
  end, {})
end

-- Capitalise whatever was typed in insert node `idx`, for `setFoo` from `foo`.
local function capitalised(idx)
  return f(function(args)
    local v = (args[1] or {})[1] or ""
    return v:sub(1, 1):upper() .. v:sub(2)
  end, { idx })
end

-- ---------------------------------------------------------------------------
-- React components (name derived from the file)
-- ---------------------------------------------------------------------------
local components = {
  -- rafce: arrow component + default export. The common one.
  s("rafce", {
    t("const "), component_name(),
    t({ " = () => {", "  return (", "    <div>" }), i(1),
    t({ "</div>", "  )", "}", "", "export default " }), component_name(),
  }),

  -- rafc: arrow component, named export only
  s("rafc", {
    t("export const "), component_name(),
    t({ " = () => {", "  return (", "    <div>" }), i(1),
    t({ "</div>", "  )", "}" }),
  }),

  -- rafcp: arrow component that destructures props
  s("rafcp", {
    t("const "), component_name(), t(" = ({ "), i(1, "children"),
    t({ " }) => {", "  return (", "    <div>" }), i(2),
    t({ "</div>", "  )", "}", "", "export default " }), component_name(),
  }),

  -- rfc: function declaration + default export at the bottom
  s("rfc", {
    t("function "), component_name(),
    t({ "() {", "  return (", "    <div>" }), i(1),
    t({ "</div>", "  )", "}", "", "export default " }), component_name(),
  }),

  -- rfce: export default function, the Next.js App Router shape
  s("rfce", {
    t("export default function "), component_name(),
    t({ "() {", "  return (", "    <div>" }), i(1),
    t({ "</div>", "  )", "}" }),
  }),
}

-- Typed props version, only makes sense in .tsx
local components_ts = {
  s("tsrafce", {
    t("interface "), component_name(), t({ "Props {", "  " }), i(1),
    t({ "", "}", "", "const " }), component_name(), t(" = ({ "), i(2),
    t(" }: "), component_name(),
    t({ "Props) => {", "  return (", "    <div>" }), i(3),
    t({ "</div>", "  )", "}", "", "export default " }), component_name(),
  }),
}

-- ---------------------------------------------------------------------------
-- Hooks
-- ---------------------------------------------------------------------------
local function use_state(trigger)
  return s(trigger, {
    t("const ["), i(1, "state"), t(", set"), capitalised(1), t("] = useState("), i(2), t(")"),
  })
end

local hooks = {
  use_state("useState"),
  use_state("us"), -- short alias, same as the VSCode extension

  ps("useEffect", "useEffect(() => {\n  $1\n}, [$2])$0"),
  ps("ue", "useEffect(() => {\n  $1\n}, [$2])$0"),
  -- effect with a cleanup return, the shape that is easy to get wrong
  ps("uec", "useEffect(() => {\n  $1\n\n  return () => {\n    $2\n  }\n}, [$3])$0"),

  ps("useCallback", "const ${1:handler} = useCallback(() => {\n  $2\n}, [$3])$0"),
  ps("useMemo", "const ${1:value} = useMemo(() => {\n  return $2\n}, [$3])$0"),
  ps("useRef", "const ${1:ref} = useRef(${2:null})$0"),
  ps("useContext", "const ${1:value} = useContext(${2:Context})$0"),
  ps("useReducer", "const [${1:state}, dispatch] = useReducer(${2:reducer}, ${3:initialState})$0"),
}

-- ---------------------------------------------------------------------------
-- Imports and exports
-- ---------------------------------------------------------------------------
local imports = {
  ps("imr", 'import React from "react"$0'),
  ps("imrs", 'import React, { useState } from "react"$0'),
  ps("imrse", 'import React, { useState, useEffect } from "react"$0'),
  ps("imp", 'import ${1:name} from "${2:module}"$0'),
  ps("imd", 'import { ${1:name} } from "${2:module}"$0'),
  ps("ime", 'import * as ${1:name} from "${2:module}"$0'),
  ps("exp", "export default ${1:name}$0"),
  ps("exd", "export const ${1:name} = $2$0"),
}

-- ---------------------------------------------------------------------------
-- Everyday JS/TS
-- ---------------------------------------------------------------------------
local everyday = {
  ps("clg", "console.log($1)$0"),
  -- clo logs a variable alongside its own name, so the output is readable
  s("clo", { t('console.log("'), i(1), t('", '), f(function(args)
    return (args[1] or {})[1] or ""
  end, { 1 }), t(")") }),
  ps("cer", "console.error($1)$0"),
  ps("cwa", "console.warn($1)$0"),
  ps("ctm", 'console.time("${1:label}")$0'),
  ps("anfn", "const ${1:name} = (${2:args}) => {\n  $3\n}$0"),
  ps("aafn", "const ${1:name} = async (${2:args}) => {\n  $3\n}$0"),
  ps("tryc", "try {\n  $1\n} catch (error) {\n  ${2:console.error(error)}\n}$0"),
  ps("fetch", 'const res = await fetch(${1:url})\nif (!res.ok) throw new Error("Request failed: " + res.status)\nconst ${2:data} = await res.json()$0'),
  ps("map", "${1:items}.map((${2:item}) => (\n  $3\n))$0"),
  ps("cln", 'className="$1"$0'),
}

-- ---------------------------------------------------------------------------
-- TypeScript types
-- ---------------------------------------------------------------------------
local types = {
  ps("int", "interface ${1:Name} {\n  $2\n}$0"),
  ps("typ", "type ${1:Name} = $2$0"),
  ps("enm", "enum ${1:Name} {\n  $2\n}$0"),
}

-- ---------------------------------------------------------------------------
-- Next.js, App Router
-- ---------------------------------------------------------------------------
local nextjs = {
  -- a page.tsx server component
  s("npage", {
    t("export default function "), component_name(),
    t({ "() {", "  return (", "    <main>" }), i(1),
    t({ "</main>", "  )", "}" }),
  }),

  -- a client component, with the directive people forget
  s("nclient", {
    t({ '"use client"', "", 'import { useState } from "react"', "", "export default function " }),
    component_name(),
    t({ "() {", "  " }), i(1),
    t({ "", "", "  return (", "    <div>" }), i(2),
    t({ "</div>", "  )", "}" }),
  }),

  s("nlayout", {
    t("export default function "), component_name(),
    t({ "({", "  children,", "}: {", "  children: React.ReactNode", "}) {", "  return (", "    <section>" }),
    i(1),
    t({ "</section>", "  )", "}" }),
  }),

  -- app/api/.../route.ts handler
  ps("nroute", 'import { NextResponse } from "next/server"\n\nexport async function ${1:GET}(request: Request) {\n  $2\n\n  return NextResponse.json({ $3 })\n}$0'),
  ps("nmeta", 'export const metadata = {\n  title: "$1",\n  description: "$2",\n}$0'),
  ps("nimg", '<Image src={$1} alt="$2" width={$3} height={$4} />$0'),
  ps("nlink", '<Link href="$1">$2</Link>$0'),
}

-- ---------------------------------------------------------------------------
-- Registration
-- ---------------------------------------------------------------------------
local function merge(...)
  local out = {}
  for _, list in ipairs({ ... }) do
    for _, snip in ipairs(list) do table.insert(out, snip) end
  end
  return out
end

ls.add_snippets("javascript", merge(components, hooks, imports, everyday))
ls.add_snippets("javascriptreact", merge(components, hooks, imports, everyday, nextjs))
ls.add_snippets("typescript", merge(components, hooks, imports, everyday, types))
ls.add_snippets("typescriptreact", merge(components, components_ts, hooks, imports, everyday, types, nextjs))
