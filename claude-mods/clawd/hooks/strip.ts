// The work strip's data: what each tool call is, what to call it, what the
// uncommitted changes add up to. Nothing here draws; register.tsx does.

export type Kind = 'read' | 'edit' | 'run' | 'other'

export type Call = {
  id: string
  tool: string
  kind: Kind
  label: string
  state: 'running' | 'ok' | 'failed'
}

export type Stats = { added: number; deleted: number; files: number }

const READ = new Set(['Read', 'Grep', 'Glob', 'WebFetch', 'WebSearch', 'ListMcpResourcesTool', 'ReadMcpResourceTool'])
const EDIT = new Set(['Edit', 'Write', 'NotebookEdit'])

export function kindOf(tool: string): Kind {
  if (tool === 'Bash') return 'run'
  if (EDIT.has(tool)) return 'edit'
  if (READ.has(tool)) return 'read'
  return 'other'
}

// The word that says what a call is doing: a file's name, a command's program,
// a search's pattern, or the tool's own name
export function labelOf(tool: string, input: Record<string, unknown>): string {
  const path = input.file_path ?? input.notebook_path
  if (typeof path === 'string' && path) return path.split('/').pop() ?? path
  if (typeof input.command === 'string' && input.command.trim()) return input.command.trim().split(/\s+/)[0] ?? tool
  for (const key of ['pattern', 'query', 'url'] as const) {
    const value = input[key]
    if (typeof value === 'string' && value) return value.length > 40 ? value.slice(0, 39) + '…' : value
  }
  return tool
}

// What the status line says while a call runs: "reading lookup.ts", "running git"
export function verbOf(kind: Kind, tool: string): string {
  switch (kind) {
    case 'read':
      return 'reading'
    case 'edit':
      return 'editing'
    case 'run':
      return 'running'
    default:
      return wordsOf(tool)
  }
}

// A tool's name as words: "SubagentHandback" is "subagent handback",
// "mcp__savvy-progress__step" is "savvy-progress step"
export function wordsOf(tool: string): string {
  return tool
    .replace(/^mcp__/, '')
    .replace(/__/g, ' ')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .toLowerCase()
}

// The status line for a running call: the verb, then the label unless it only repeats the tool
export const statusOf = (call: Call): string =>
  call.label === call.tool ? verbOf(call.kind, call.tool) : `${verbOf(call.kind, call.tool)} ${call.label}`

// The color of a call's block: running is yellow, a failure red, otherwise by kind
export function blockColor(call: Call): string {
  if (call.state === 'running') return 'warning'
  if (call.state === 'failed') return 'error'
  switch (call.kind) {
    case 'read':
      return 'suggestion'
    case 'edit':
      return 'claude'
    case 'run':
      return 'success'
    default:
      return 'inactive'
  }
}

// `git diff --numstat`: one line per file, "added<TAB>deleted<TAB>path", a
// binary file's counts are "-"
export function parseNumstat(text: string): Stats {
  const stats: Stats = { added: 0, deleted: 0, files: 0 }
  for (const line of text.split('\n')) {
    const [added, deleted, path] = line.split('\t')
    if (!path) continue
    stats.files += 1
    if (added !== '-') stats.added += Number(added) || 0
    if (deleted !== '-') stats.deleted += Number(deleted) || 0
  }
  return stats
}
