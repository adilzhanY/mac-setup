import { expect, mock, test } from 'claude-code/testing'

import type { On } from 'claude-code'

// 6 columns of sprite and 6 beside it for the side view's laptop and the letters it gives off
const COLUMNS = 12
const BODY = 0xd77757
const LAPTOP = 0x8b8b8b

const band = (isWorking: boolean, hasSurvey = false) =>
  ({
    component: 'AbovePrompt',
    requestId: 'band',
    props: { hasSurvey, isWorking, maxRows: 12, bodyColumns: 100, scroll: { offset: 0, bodyRows: 11 }, view: {} },
  }) as const

type Cell = { char: string; fg: number; bg: number }

// A Raster's cells, one array per row
function grid(cells: string): Cell[][] {
  const bytes = Uint8Array.from(atob(cells), c => c.charCodeAt(0))
  const view = new DataView(bytes.buffer)
  const out: Cell[][] = []
  for (let r = 0; r < bytes.length / 12 / COLUMNS; r++) {
    const row: Cell[] = []
    for (let c = 0; c < COLUMNS; c++) {
      const i = (r * COLUMNS + c) * 12
      row.push({ char: String.fromCodePoint(view.getUint32(i, true)), fg: view.getUint32(i + 4, true), bg: view.getUint32(i + 8, true) })
    }
    out.push(row)
  }
  return out
}

const text = (cells: string, row: number) => (grid(cells)[row] ?? []).map(c => c.char).join('')
const colors = (cells: string, row: number) => new Set((grid(cells)[row] ?? []).flatMap(c => [c.fg, c.bg]))

// Standing in for the engine's band beneath the mods, which draws nothing of its own
const engineBand = (on: On) => on('ui.render', () => ({ type: 'engine', ref: 1 }))

test('Clawd stands on the prompt at the right end of the band', async ($, on) => {
  mock.store(on)
  engineBand(on)
  const ui = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  const raster = await ui.find({ type: 'Raster', key: 'clawd' })
  expect(raster?.props.columns).toBe(COLUMNS)
  expect(raster?.props.rows).toBe(2)

  // Its body and four feet in the last columns; the arms depend on the greeting wave
  const cells = String(raster?.props.cells)
  expect(text(cells, 1).slice(-5, -1)).toBe('▛▛▜▜')
  expect(text(cells, 0).slice(-5, -1)).toBe('█▜▛█')
  await ui.unmount()
})

test('The band button hides Clawd and brings it back', async ($, on) => {
  mock.store(on)
  engineBand(on)
  const ui = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  expect((await ui.find({ key: 'hide' }))?.props.label).toBe('hide Clawd')

  await ui.press({ key: 'hide' })
  expect(await ui.find({ type: 'Raster' })).toBeUndefined()
  expect((await ui.find({ key: 'show' }))?.props.label).toBe('show Clawd')

  await ui.press({ key: 'show' })
  expect(await ui.find({ type: 'Raster', key: 'clawd' })).toBeDefined()
  expect(await ui.find({ key: 'hide' })).toBeDefined()
  await ui.unmount()
})

test('Clawd steps aside while another mod draws in the band', async ($, on) => {
  mock.store(on)
  // Beneath Clawd, another mod's popup: a tree of its own, not the engine's empty band
  on('ui.render', ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    return Box({ children: [Text({ children: ['model picker'] })] })
  })
  const ui = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  expect(await ui.find({ type: 'Raster' })).toBeUndefined()
  expect(await ui.find({ text: 'model picker' })).toBeDefined()
  await ui.unmount()
})

test('Clawd leaves the band to the desktop app and to surveys', async ($, on) => {
  // Standing in for the engine's own band: one line of text
  on('ui.render', ($, e) => {
    const { Text } = $.ui.resolve(e)
    return Text({ children: ['engine band'] })
  })

  const desktop = await $.ui.mount({ plugin: 'clawd', surface: 'desktop', ...band(false) })
  expect(await desktop.find({ type: 'Raster' })).toBeUndefined()
  expect(await desktop.find({ text: 'engine band' })).toBeDefined()
  await desktop.unmount()

  const survey = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false, true) })
  expect(await survey.find({ type: 'Raster' })).toBeUndefined()
  expect(await survey.find({ text: 'engine band' })).toBeDefined()
  await survey.unmount()
})

test('Clawd turns side on and types on its laptop while Claude works, packs up, cheers, then naps', async ($, on) => {
  const clock = mock.clock(on)
  mock.store(on)
  engineBand(on)
  const blits: string[] = []
  on('ui.blit', ($, e) => {
    if ('cells' in e) blits.push(e.cells)
    return { value: {} }
  })

  on('session.start', ($, e) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(true) })

  await clock.advance(6000)
  // Side on, the laptop shut on the floor in front of it first, then the lid up
  const isOpen = (cells: string) => colors(cells, 0).has(LAPTOP)
  const shut = blits.findIndex(cells => colors(cells, 1).has(LAPTOP) && !isOpen(cells))
  const open = blits.findIndex(isOpen)
  expect(shut).toBeGreaterThan(-1)
  expect(open).toBeGreaterThan(shut)
  // Its arm comes down on the keys and lifts again: the drawing takes more than one shape
  const keys = new Set(blits.slice(open).filter(isOpen).map(cells => text(cells, 0) + text(cells, 1)))
  expect(keys.size).toBeGreaterThan(1)
  expect(colors(blits.at(-1) ?? '', 0).has(BODY)).toBe(true)
  await ui.unmount()

  // The turn ends: the laptop goes away and it cheers with both arms up
  const idle = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  blits.length = 0
  await clock.advance(5000)
  expect(blits.some(cells => text(cells, 0).endsWith('▚█▜▛█▞'))).toBe(true)
  expect(text(blits.at(-1) ?? '', 1).slice(-6)).toBe('▀▛▛▜▜▀')
  expect(colors(blits.at(-1) ?? '', 1).has(LAPTOP)).toBe(false)

  // Five quiet minutes later it naps: eyes shut as two lines, letters drifting off its head
  blits.length = 0
  await clock.advance(5 * 60_000 + 5000)
  expect(blits.some(cells => /[zZ]/.test(text(cells, 0) + text(cells, 1)))).toBe(true)
  const asleep = text(blits.at(-1) ?? '', 0)
  expect(asleep).toContain('╺')
  expect(asleep).toContain('╸')
  await idle.unmount()
})

test('The work strip shows this turn\'s calls and the uncommitted changes, in green and red', async ($, on) => {
  const clock = mock.clock(on)
  mock.store(on)
  engineBand(on)
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('process.run', () => ({
    value: { exitCode: 0, stdout: '390\t8\tsrc/cache/lookup.ts\n9\t2\tsrc/cache/lookup.test.ts\n-\t-\tlogo.png\n', stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
  }))
  on('tool.call', (_$, e) => (e.tool === 'Bash' ? { ref: 2, result: {}, text: 'failed', isError: true } : { ref: 1, result: {}, text: 'ok' }))

  await $.session.start({ cwd: '/tmp/repo', surface: 'terminal', isInteractive: true })
  await clock.settle()
  await $.tool.call({ tool: 'Read', file_path: '/repo/src/cache/lookup.ts' } as never)
  await $.tool.call({ tool: 'Bash', command: 'npm test' } as never)

  const ui = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  expect((await ui.find({ type: 'Text', text: '+399' }))?.props.color).toBe('success')
  expect((await ui.find({ type: 'Text', text: '-10' }))?.props.color).toBe('error')
  expect(await ui.find({ type: 'Text', text: 'in 3 files' })).toBeDefined()
  // A read is a blue block, a failed command a red one
  const blocks = (await ui.findAll({ type: 'Text', text: '▮' })).filter(b => b.text === '▮')
  expect(blocks.map(b => b.props.color)).toEqual(['suggestion', 'error'])
  await ui.unmount()
})

test('While a call runs the strip names it; a new turn starts it over', async ($, on) => {
  const clock = mock.clock(on)
  mock.store(on)
  engineBand(on)
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('turn.start', ($, e) => ({ turnId: e.turnId }))
  // Not a repository: no counts, and no line for them
  on('process.run', () => ({ value: { exitCode: 128, stdout: '', stderr: 'not a git repository', isStdoutTruncated: false, isStderrTruncated: false } }))
  on('tool.call', async () => {
    await clock.sleep(500)
    return { ref: 1, result: {}, text: 'ok' }
  })

  await $.session.start({ cwd: '/tmp/scratch', surface: 'terminal', isInteractive: true })
  await clock.settle()
  const pending = $.tool.call({ tool: 'Bash', command: 'git status' } as never)
  await clock.settle()
  const running = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(true) })
  expect(await running.find({ type: 'Text', text: 'running git' })).toBeDefined()
  await running.unmount()

  await clock.advance(600)
  await pending
  const done = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  expect(await done.find({ type: 'Text', text: 'running git' })).toBeUndefined()
  expect(await done.find({ type: 'Text', text: 'in 0 files' })).toBeUndefined()
  await done.unmount()

  await $.turn.start({ text: 'next', turnId: 'turn-2' })
  const fresh = await $.ui.mount({ plugin: 'clawd', surface: 'terminal', ...band(false) })
  expect((await fresh.findAll({ type: 'Text', text: '▮' })).filter(b => b.text === '▮')).toHaveLength(0)
  await fresh.unmount()
})
