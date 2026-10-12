import { expect, test } from 'claude-code/testing'

import { blockColor, kindOf, labelOf, parseNumstat, statusOf, verbOf, type Call } from '../hooks/strip'

test('Tool calls sort into kinds, and read by their file, command or pattern', () => {
  expect(kindOf('Read')).toBe('read')
  expect(kindOf('Grep')).toBe('read')
  expect(kindOf('Edit')).toBe('edit')
  expect(kindOf('NotebookEdit')).toBe('edit')
  expect(kindOf('Bash')).toBe('run')
  expect(kindOf('TodoWrite')).toBe('other')

  expect(labelOf('Edit', { file_path: '/home/a/src/auth.ts' })).toBe('auth.ts')
  expect(labelOf('Bash', { command: '  git   status --short ' })).toBe('git')
  expect(labelOf('Grep', { pattern: 'useEffect' })).toBe('useEffect')
  expect(labelOf('TodoWrite', {})).toBe('TodoWrite')
  expect(verbOf('edit', 'Edit')).toBe('editing')
  expect(verbOf('other', 'Agent')).toBe('agent')
  expect(statusOf({ id: '1', tool: 'SubagentHandback', kind: 'other', label: 'SubagentHandback', state: 'running' })).toBe('subagent handback')
  expect(statusOf({ id: '2', tool: 'mcp__savvy-progress__step', kind: 'other', label: 'mcp__savvy-progress__step', state: 'running' })).toBe('savvy-progress step')
  expect(statusOf({ id: '3', tool: 'Bash', kind: 'run', label: 'git', state: 'running' })).toBe('running git')
})

test('Block colors: running yellow, a failure red, otherwise by kind', () => {
  const call = (kind: Call['kind'], state: Call['state']): Call => ({ id: '1', tool: 'x', kind, label: '', state })
  expect(blockColor(call('edit', 'running'))).toBe('warning')
  expect(blockColor(call('read', 'failed'))).toBe('error')
  expect(blockColor(call('edit', 'ok'))).toBe('claude')
  expect(blockColor(call('run', 'ok'))).toBe('success')
  expect(blockColor(call('other', 'ok'))).toBe('inactive')
})

test('git numstat adds up; a binary file counts as a file with no lines', () => {
  expect(parseNumstat('390\t8\tsrc/a.ts\n9\t2\tsrc/b.ts\n-\t-\tlogo.png\n')).toEqual({ added: 399, deleted: 10, files: 3 })
  expect(parseNumstat('')).toEqual({ added: 0, deleted: 0, files: 0 })
})
