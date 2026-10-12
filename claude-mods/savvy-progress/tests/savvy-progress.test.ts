import { expect, mock, test } from 'claude-code/testing'

import type { On } from 'claude-code'

import { costumeOf } from '../hooks/register'

const BAND = {
  component: 'AbovePrompt',
  requestId: 'band',
  props: { hasSurvey: false, isWorking: true, maxRows: 12, bodyColumns: 100, scroll: { offset: 0, bodyRows: 11 }, view: {} },
} as const

const PANE = {
  component: 'Pane',
  requestId: 'savvy-agents',
  props: { title: 'Agents', isFocused: false, bodyColumns: 60, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} },
} as const

const CLAY = 0xd97757

// The engine beneath the mod: a band of its own (Clawd stands in for it) and subagents that start
function engine(on: On) {
  const clock = mock.clock(on)
  mock.env(on, {})
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('settings.read', () => ({ value: {} }))
  // Registrations and opens the engine would take
  for (const op of ['tool.register', 'command.register'] as const) on(op, () => ({ value: undefined }) as never)
  // The panes the person has open
  const opened: string[] = []
  on('ui.open', ($, e) => {
    opened.push(e.id)
    return { value: undefined } as never
  })
  on('ui.panes', () => ({ value: opened.map(id => ({ id, isShown: true, isPlaced: true })) }) as never)
  on('ui.render', () => ({ type: 'engine', ref: 1 }))
  on('agent.spawn', ($, e) => ({ agentId: `agent-${e.description}`, model: 'claude-opus-5-5' }))
  // The blits that reach the terminal, by Raster key
  const blits = new Map<string, string[]>()
  on('ui.blit', ($, e) => {
    if ('cells' in e) blits.set(e.key, [...(blits.get(e.key) ?? []), e.cells])
    return { value: {} } as never
  })
  return { clock, blits, opened }
}

// Every foreground and background color of a Raster's cells
function colors(cells: string): Set<number> {
  const bytes = Uint8Array.from(atob(cells), c => c.charCodeAt(0))
  const view = new DataView(bytes.buffer)
  const out = new Set<number>()
  for (let i = 0; i < bytes.length; i += 12) {
    out.add(view.getUint32(i + 4, true))
    out.add(view.getUint32(i + 8, true))
  }
  return out
}

const report = ($: { tool: { call: (input: never) => Promise<unknown> } }, input: Record<string, unknown>) =>
  $.tool.call({ tool: 'mcp__savvy-progress__progress', ...input } as never)

test('The band stays out of the way until a flow reports', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  const band = await $.ui.mount({ plugin: 'savvy-progress', surface: 'terminal', ...BAND })
  expect(await band.drawn()).toMatchObject({ type: 'engine' })
  await band.unmount()
})

test('A reported flow draws its bar above the band beneath, and the cross dismisses it', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await report($, {
    title: 'Auth refactor',
    phase: 'delegate',
    done: 1,
    tasks: [
      { title: 'Token store', tier: 'medium' },
      { title: 'Refresh flow', tier: 'heavy' },
      { title: 'Tests', tier: 'light' },
    ],
  })

  const band = await $.ui.mount({ plugin: 'savvy-progress', surface: 'terminal', ...BAND })
  const bar = await band.find({ type: 'Raster', key: 'flow-bar' })
  expect(bar).toBeDefined()
  // The pill's white label and the track behind the fill
  expect(colors(String(bar?.props.cells)).has(0xffffff)).toBe(true)
  expect(colors(String(bar?.props.cells)).has(0x6b6b68)).toBe(true)
  expect(await band.find({ type: 'Text', text: / 33%/ })).toBeDefined()
  expect((await band.find({ key: 'savvy-agents' }))?.props.label).toBe('agents ×3')
  // What the mods beneath drew stays, under the bar
  expect(JSON.stringify(await band.drawn())).toContain('"type":"engine"')

  await band.press({ key: 'savvy-dismiss' })
  expect(await band.drawn()).toMatchObject({ type: 'engine' })
  await band.unmount()
})

test('Any running subagent gets a row with the button to the panel', async ($, on) => {
  const { opened } = engine(on)
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await $.agent.spawn({ subagentType: 'general-purpose', description: 'Designer: spec', prompt: 'go' } as never)
  const band = await $.ui.mount({ plugin: 'savvy-progress', surface: 'terminal', ...BAND })
  expect(await band.find({ type: 'Text', text: '1 agent working' })).toBeDefined()
  expect(await band.find({ type: 'Text', text: /Designer: spec/ })).toBeDefined()
  expect((await band.find({ key: 'savvy-agents' }))?.props.label).toBe('agents ×1')
  await band.press({ key: 'savvy-agents' })
  expect(opened).toEqual(['savvy-agents'])
  expect(JSON.stringify(await band.drawn())).toContain('"type":"engine"')
  await band.unmount()
})

test('The pane shows each subagent as a costumed crab that walks while it runs', async ($, on) => {
  const { clock, blits } = engine(on)
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await report($, { title: 'Auth refactor', tasks: [{ title: 'Refresh flow', tier: 'heavy' }, { title: 'Tests', tier: 'light' }] })
  await $.agent.spawn({ subagentType: 'savvy-heavy', description: 'Refresh flow', prompt: 'go' } as never)

  const pane = await $.ui.mount({ plugin: 'savvy-progress', surface: 'terminal', ...PANE })
  const crab = await pane.find({ type: 'Raster', key: 'crab-agent-Refresh flow' })
  expect(crab?.props.columns).toBe(16)
  expect(crab?.props.rows).toBe(6)
  const cells = String(crab?.props.cells)
  expect(colors(cells).has(CLAY)).toBe(true)
  // The detective's deerstalker
  expect(colors(cells).has(0x7a4a26)).toBe(true)

  // The planned task not started yet waits below, faded
  expect(await pane.find({ type: 'Raster', key: 'crab-plan-2' })).toBeDefined()
  expect(await pane.find({ type: 'Text', text: /2\. Tests/ })).toBeDefined()

  // A running crab is repainted by blits, not by redraws
  await clock.advance(1000)
  expect(new Set(blits.get('crab-agent-Refresh flow')).size).toBeGreaterThan(1)
  await pane.unmount()
})

test('The compact view lines the crew up', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await $.agent.spawn({ subagentType: 'Explore', description: 'Scout', prompt: 'go' } as never)
  const pane = await $.ui.mount({ plugin: 'savvy-progress', surface: 'terminal', ...PANE })
  await pane.press({ key: 'compact' })
  const crew = await pane.find({ type: 'Raster', key: 'crew-0' })
  expect(crew?.props.columns).toBe(17)
  // The pirate's gold trim
  expect(colors(String(crew?.props.cells)).has(0xf5c542)).toBe(true)
  await pane.unmount()
})

test('A subagent wears the costume of its job', () => {
  expect(costumeOf('general-purpose', 'Designer: spec for chess site')).toBe('designer')
  expect(costumeOf('general-purpose', 'Builder: static site pages')).toBe('developer')
  expect(costumeOf('general-purpose', 'Tester: check the forms')).toBe('detective')
  expect(costumeOf('general-purpose', 'Fix the deploy config')).toBe('engineer')
  expect(costumeOf('Explore', 'Scout auth')).toBe('pirate')
  expect(costumeOf('savvy-flow:savvy-heavy', 'Refresh flow')).toBe('detective')
  expect(costumeOf('general-purpose', 'Token store')).toBe('developer')
})
