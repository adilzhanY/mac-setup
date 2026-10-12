import { expect, mock, test } from 'claude-code/testing'

import type { On } from 'claude-code'

const HINT = {
  component: 'PromptHint',
  requestId: 'hint',
  props: { isDraft: false, isWorking: false, hint: '? for shortcuts' },
} as const
const BAND = {
  component: 'AbovePrompt',
  requestId: 'band',
  props: { hasSurvey: false, isWorking: false, maxRows: 20, bodyColumns: 120, scroll: { offset: 0, bodyRows: 19 }, view: {} },
} as const
const OPTIONS = ['default', 'sonnet', 'opus', 'haiku', 'fable', 'best', 'sonnet[1m]', 'opus[1m]', 'fable[1m]', 'opusplan']
const ORANGE = '#d77757'

// Standing in for the engine: the Model row, the running model, the settings,
// the command line and its own drawings. Records what the mod sets.
function engine(on: On, start: string, saved = 'high') {
  const state = { model: start, sets: [] as string[], commands: [] as string[] }
  on('config.list', () => ({
    value: [{ key: 'model', label: 'Model', kind: 'choice', value: state.model, options: OPTIONS, provider: { plugin: 'engine', tier: 'core' }, isLocked: false }],
  }))
  on('config.set', ($, e) => {
    state.sets.push(String(e.value))
    state.model = String(e.value)
    return { value: e.value }
  })
  on('session.model', () => ({ value: 'claude-' + state.model.replace('[1m]', '') + '-5-5' }))
  on('settings.read', () => ({ value: { effortLevel: 'medium', modelSettings: { 'claude-opus-5-5': { effortLevel: saved } } } }))
  on('command.run', ($, e) => {
    state.commands.push(`/${e.command} ${e.args}`)
    return { text: '' }
  })
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('ui.render', () => ({ type: 'engine', ref: 1 }))
  return state
}

// The letters of the effort pill and their colors, as its drawing drew them
async function effortLetters(ui: { findAll: (q: { in?: string; type?: string }) => Promise<{ text: string; props: Record<string, unknown> }[]> }) {
  const texts = await ui.findAll({ in: 'effort', type: 'Text' })
  return texts.filter(t => t.text.length === 1).map(t => t.props.color)
}

test('The pills sit under the hint line: the model in orange, the effort in its color', async ($, on) => {
  engine(on, 'opus')
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })

  const hint = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...HINT })
  const drawn = await hint.drawn()
  // The engine's own line first, the pills after it
  expect('children' in drawn ? drawn.children?.[0] : undefined).toMatchObject({ type: 'engine' })
  expect((await hint.find({ type: 'Text', text: 'Opus 5.5' }))?.props.color).toBe(ORANGE)
  expect((await hint.find({ type: 'Client', key: 'effort' }))?.props.props).toEqual({ label: 'High', level: 'high' })
  expect(await effortLetters(hint)).toHaveLength(4)
  // Over each pill, a Button with the same label, shown while the pointer rests there
  expect((await hint.find({ key: 'open-model' }))?.props.label).toBe('Opus 5.5')
  expect((await hint.find({ key: 'open-effort' }))?.props.label).toBe('High')
  await hint.unmount()
})

test('High and Max shimmer, the other levels hold still', async ($, on) => {
  engine(on, 'opus', 'max')
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  const hint = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...HINT })
  const before = await effortLetters(hint)
  await hint.advance(400)
  const after = await effortLetters(hint)
  expect(before).toHaveLength(3)
  expect(after).not.toEqual(before)

  // An /effort typed by hand moves the pill: low is one light blue, frame after frame
  await $.command.run({ command: 'effort', args: 'low', origin: { kind: 'composer' }, presentation: { isFullscreen: true, columns: 120 } })
  const low = await effortLetters(hint)
  await hint.advance(400)
  expect(await effortLetters(hint)).toEqual(low)
  expect(new Set(low)).toEqual(new Set(['#8fb4ff']))
  await hint.unmount()
})

test('The model pill opens the dropdown, a pick switches the model', async ($, on) => {
  const clock = mock.clock(on)
  const state = engine(on, 'opus')
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  const hint = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...HINT })

  // Closed, the band is left to whoever draws there
  const closed = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...BAND })
  expect(await closed.drawn()).toMatchObject({ type: 'engine' })
  await closed.unmount()

  await hint.press({ key: 'open-model' })
  const band = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...BAND })
  expect((await band.find({ key: 'model-opus' }))?.props.label).toBe('Opus 5.5  ✓')
  expect((await band.find({ key: 'model-fable' }))?.props.hotkey).toBe('2')
  await band.press({ key: 'more' })
  expect((await band.find({ key: 'model-opus[1m]' }))?.props.label).toBe('Opus 5.5, 1M context')

  await band.press({ key: 'model-fable' })
  await clock.settle()
  expect(state.sets).toEqual(['fable'])
  expect(await band.drawn()).toMatchObject({ type: 'engine' })
  expect((await hint.find({ key: 'open-model' }))?.props.label).toBe('Fable 5.1')
  await band.unmount()
  await hint.unmount()
})

test('The effort pill opens the slider, a pick runs /effort', async ($, on) => {
  const clock = mock.clock(on)
  const state = engine(on, 'opus')
  await $.session.start({ cwd: '/tmp', surface: 'terminal', isInteractive: true })
  const hint = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...HINT })

  await hint.press({ key: 'open-effort' })
  const band = await $.ui.mount({ plugin: 'model-buttons', surface: 'terminal', ...BAND })
  expect((await band.find({ key: 'stop-high' }))?.props.label).toBe('██')
  expect((await band.find({ key: 'level-medium' }))?.props.hotkey).toBe('2')

  await band.press({ key: 'level-medium' })
  await clock.settle()
  expect(state.commands).toEqual(['/effort medium'])
  expect(await band.drawn()).toMatchObject({ type: 'engine' })
  expect((await hint.find({ type: 'Client', key: 'effort' }))?.props.props).toEqual({ label: 'Medium', level: 'medium' })
  await band.unmount()
  await hint.unmount()
})

test('The desktop app keeps its own controls', async ($, on) => {
  engine(on, 'opus')
  const ui = await $.ui.mount({ plugin: 'model-buttons', surface: 'desktop', ...HINT })
  expect(await ui.find({ type: 'Client' })).toBeUndefined()
  await ui.unmount()
})
