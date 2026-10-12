import { expect, mock, test } from 'claude-code/testing'

import { hour, modelName, mobyDick, tokens } from '../hooks/format'

const range = (sessions: number, messages: number, total: number) => ({
  sessions,
  messages,
  tokens: total,
  activeDays: 3,
  peakHour: 2,
  models: [
    { model: 'claude-opus-5-5', tokens: total * 0.75 },
    { model: 'claude-haiku-4-5-20251001', tokens: total * 0.25 },
  ],
})

// What scripts/stats.mjs prints: a day active now and then, the rest quiet
const STATS = {
  generatedAt: 0,
  ranges: { all: range(724, 154039, 16_200_000_000), '30d': range(480, 91661, 1_000_000), '7d': range(41, 20245, 500_000) },
  heatmap: { weeks: 26, levels: Array.from({ length: 182 }, (_, i) => (i > 178 ? -1 : i % 5)) },
}

const ROW = (command: string) =>
  ({
    component: 'CommandOutput',
    viewport: { columns: 120, rows: 40 },
    props: { command, args: '', text: '', isErrored: false },
  }) as const

test('A claude -p run never prints the card, so its output stays the answer', async ($, on) => {
  const clock = mock.clock(on)
  on('session.turns', () => ({ value: 0 }))
  const commands: string[] = []
  on('command.run', ($, e) => {
    commands.push(e.command)
    return { text: '' }
  })
  on('session.start', ($, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: false })
  await clock.settle()
  expect(commands).toEqual([])
})

test('A fresh session prints the card, with the numbers and the heatmap', async ($, on) => {
  const clock = mock.clock(on)
  // Standing in for the engine: its own rows, HOME, the stats script and the command line
  on('ui.render', () => ({ type: 'engine', ref: 1 }))
  on('env.get', () => ({ value: '/home/test' }))
  on('session.turns', () => ({ value: 0 }))
  const commands: string[] = []
  on('command.run', ($, e) => {
    commands.push(e.command)
    return { text: '' }
  })
  const runs: string[][] = []
  on('process.run', ($, e) => {
    runs.push([...e.argv])
    return { value: { exitCode: 0, stdout: JSON.stringify(STATS), stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('session.start', ($, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await clock.settle()
  expect(commands).toEqual(['stats-card'])
  expect(runs).toEqual([['node', '/home/test/dev/claude-mods/stats-card/scripts/stats.mjs']])

  const ui = await $.ui.mount({ plugin: 'stats-card', surface: 'terminal', ...ROW('stats-card') })
  expect(await ui.find({ text: '724' })).toBeDefined()
  expect(await ui.find({ text: '154,039' })).toBeDefined()
  expect(await ui.find({ text: '16.2B' })).toBeDefined()
  expect(await ui.find({ text: '2 AM' })).toBeDefined()
  expect(await ui.find({ text: 'Opus 5.5' })).toBeDefined()
  expect(await ui.find({ text: /~60674× more tokens than Moby-Dick/ })).toBeDefined()
  // Seven rows of days, 26 weeks of them at this width, the future left blank
  expect((await ui.findAll({ type: 'Text', text: /^\u2587\u2587 ?$/ })).length).toBe(179)

  // A range button switches the numbers, a tab button the view
  await ui.press({ key: 'range-7d' })
  expect(await ui.find({ text: '20,245' })).toBeDefined()
  await ui.press({ key: 'tab-models' })
  expect(await ui.find({ text: 'Haiku 4.5' })).toBeDefined()
  expect(await ui.find({ text: '75%' })).toBeDefined()
  await ui.unmount()

  // Every other command's row is left as the engine draws it
  const other = await $.ui.mount({ plugin: 'stats-card', surface: 'terminal', ...ROW('cost') })
  expect(await other.drawn()).toMatchObject({ type: 'engine' })
  await other.unmount()
})

test('A resumed session does not print it again', async ($, on) => {
  const clock = mock.clock(on)
  on('env.get', () => ({ value: '/home/test' }))
  on('session.turns', () => ({ value: 12 }))
  const commands: string[] = []
  on('command.run', ($, e) => {
    commands.push(e.command)
    return { text: '' }
  })
  on('process.run', () => ({ value: { exitCode: 0, stdout: JSON.stringify(STATS), stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }))
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  await clock.settle()
  expect(commands).toEqual([])
})

test('The numbers are written the way the desktop card writes them', () => {
  expect(tokens(16_234_000_000)).toBe('16.2B')
  expect(tokens(18_000_000_000)).toBe('18.0B')
  expect(tokens(950_000_000)).toBe('950M')
  expect(tokens(12_400)).toBe('12.4K')
  expect(hour(0)).toBe('12 AM')
  expect(hour(2)).toBe('2 AM')
  expect(hour(13)).toBe('1 PM')
  expect(modelName('claude-opus-5-5')).toBe('Opus 5.5')
  expect(modelName('claude-fable-5')).toBe('Fable 5')
  expect(modelName('claude-haiku-4-5-20251001')).toBe('Haiku 4.5')
  expect(mobyDick(16_200_000_000)).toBe("You've used ~60674× more tokens than Moby-Dick.")
  expect(mobyDick(100_000)).toBeUndefined()
})
