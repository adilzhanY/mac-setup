import type { EngineInterface, Register, RenderChildren } from 'claude-code'

import { MODEL_COLOR, effortColor } from './colors'

// The desktop app's model and effort controls, in the terminal: two pills at
// the left of the footer, under the hint line (the status line is not a site a
// mod draws in), the model in Clawd's orange and the effort in its level's
// color, High and Max shimmering (pills.tsx). The model pill opens a dropdown
// and the effort pill a slider, both in the band above the prompt (a mod draws
// nowhere else that a popup fits), at its left; Clawd steps aside while one is
// open. A model is set the way the /config Model row sets it, an effort the way
// /effort does.
//
// A Button's label takes no color and colored Text over a Button takes its
// clicks, so each pill is colored text at rest, and the pointer resting on it
// reveals a Button over it that takes the click. Nothing here listens to the
// pointer itself: that switches the terminal to pixel mouse reports, which in
// kitty with a window margin puts every click in the session on the wrong cell.

type Option = { value: string; label: string }

const MODELS: Option[] = [
  { value: 'opus', label: 'Opus 5.5' },
  { value: 'fable', label: 'Fable 5.1' },
  { value: 'sonnet', label: 'Sonnet 5.5' },
  { value: 'haiku', label: 'Haiku 5.5' },
]
// What the rest of the Model row's choices are called under "More models"
const MORE_LABELS: Record<string, string> = {
  'opus[1m]': 'Opus 5.5, 1M context',
  'fable[1m]': 'Fable 5.1, 1M context',
  'sonnet[1m]': 'Sonnet 5.5, 1M context',
  opusplan: 'Opus plan mode',
  best: 'Best available',
  default: 'Default',
}
const EFFORTS: Option[] = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'xhigh', label: 'Extra high' },
  { value: 'max', label: 'Max' },
]
const DROPDOWN_WIDTH = 34
const SLIDER_WIDTH = 54
// One stop of the slider's track, in columns
const STOP = 10

// The Model row's value (`opus`, `opus[1m]`, `default`), its choices, the model
// running (`claude-opus-5-5`), and the session's effort: the saved one at the
// start and after a model switch, then what /effort and each request say
let chosen = ''
let options: readonly string[] = []
let running = ''
let effort: string | undefined
let open: 'none' | 'model' | 'effort' = 'none'
let showMore = false

async function refresh($: EngineInterface, isEffortSaved = false) {
  const row = (await $.config.list()).find(r => r.key === 'model')
  chosen = typeof row?.value === 'string' ? row.value : ''
  options = row && 'options' in row && Array.isArray(row.options) ? row.options : []
  running = (await $.session.model()).toLowerCase()
  if (isEffortSaved) {
    // A model's own saved effort, else the one for every model
    const settings = (await $.settings.read()) as { effortLevel?: unknown; modelSettings?: Record<string, { effortLevel?: unknown }> }
    const level = settings.modelSettings?.[running]?.effortLevel ?? settings.effortLevel
    effort = typeof level === 'string' ? level : undefined
  }
  $.ui.invalidate('ui.render')
}

function setEffort($: EngineInterface, level: string) {
  if (level === effort || !EFFORTS.some(x => x.value === level)) return
  effort = level
  $.ui.invalidate('ui.render')
}

// `claude-opus-5-5` is Opus 5.5
function modelName(id: string): string {
  const parts = id.replace(/^claude-/, '').replace(/-\d{8}$/, '').split('-')
  const family = parts.filter(p => !/^\d+$/.test(p)).map(p => p[0]?.toUpperCase() + p.slice(1)).join(' ')
  const version = parts.filter(p => /^\d+$/.test(p)).join('.')
  return [family, version].filter(Boolean).join(' ') || id
}

// The model in use, by the row's alias, or by the running model's id when the row says `default`
function active(): string | undefined {
  if (MORE_LABELS[chosen] && chosen !== 'default') return chosen
  const alias = chosen.replace('[1m]', '')
  return MODELS.find(m => m.value === alias)?.value ?? MODELS.find(m => running.includes(m.value))?.value
}

function modelLabel(): string {
  const current = active()
  return MODELS.find(m => m.value === current)?.label ?? (current && MORE_LABELS[current]) ?? modelName(running)
}

// The pill's shorter name: a 1M context window as a trailing "1M"
function pillLabel(): string {
  const base = MODELS.find(m => chosen.replace('[1m]', '') === m.value)
  return base && chosen.endsWith('[1m]') ? base.label + ' 1M' : modelLabel()
}

async function pickModel($: EngineInterface, value: string) {
  open = 'none'
  showMore = false
  const result = await $.config.set({ key: 'model', value })
  if ('deny' in result && result.deny) $.ui.toast('Model not switched: ' + result.deny)
  await refresh($)
}

function pickEffort($: EngineInterface, value: string) {
  open = 'none'
  effort = value
  $.ui.invalidate('ui.render')
  // Off the press: /effort sets it for the session and saves it for this model
  $.clock.after(0, () => $.command.run({ command: 'effort', args: value }).catch(() => undefined))
}

function toggle($: EngineInterface, which: 'model' | 'effort') {
  open = open === which ? 'none' : which
  showMore = false
  $.ui.invalidate('ui.render')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await refresh($, true)
    return next(e)
  })

  // A switch made elsewhere, with /model or the menu, moves the selection and
  // brings that model's saved effort
  on('classic.PostModelSwitch', async ($, e, next) => {
    const result = await next(e)
    await refresh($, true)
    return result
  }).catch(($, e, next) => next(e))

  // An /effort typed by hand, for the session only or saved
  // (whatever goes wrong here, the command itself runs as it would without the mod)
  on('command.run', { command: 'effort' }, async ($, e, next) => {
    const result = await next(e)
    setEffort($, e.args.trim().split(/\s+/)[0] ?? '')
    return result
  }).catch(($, e, next) => next(e))

  // What each request of the main loop really asks for: the session's effort
  on('turn.step', async function* ($, e, next) {
    if (e.agentId === undefined && typeof e.effort === 'string') setEffort($, e.effort)
    return yield* next(e)
  })

  // Sending a prompt closes an open popup
  on('prompt.submit', ($, e, next) => {
    if (open !== 'none') {
      open = 'none'
      $.ui.invalidate('ui.render')
    }
    return next(e)
  }).catch(($, e, next) => next(e))

  // The pills, at the left of their own row under the engine's hint line
  on('ui.render', { component: 'PromptHint' }, async ($, e, next) => {
    if (e.surface !== 'terminal') return next(e)
    const { Box, Button, Client, Text } = $.ui.resolve(e)
    const theirs = await next(e)
    const level = EFFORTS.find(x => x.value === effort)

    // A pill: its colored drawing, and over it, while the pointer rests on it,
    // a Button with the same label on the highlight color that takes the click
    const pill = (which: 'model' | 'effort', label: string, color: string, drawing: RenderChildren) => (
      <Box key={'pill-' + which} {...(open === which ? { backgroundColor: 'subtle' } : {})}>
        {drawing}
        <Box position="absolute" top={0} left={0} display="none" hover={{ display: 'flex' }}>
          <Box paddingX={1} backgroundColor="subtle">
            <Button key={'open-' + which} label={label} plain hover={{ color, bold: which === 'model' }} onPress={() => toggle($, which)} />
          </Box>
        </Box>
      </Box>
    )

    const model = pillLabel()
    return (
      <Box flexDirection="column">
        {theirs}
        <Box flexDirection="row" columnGap={1}>
          {pill('model', model, MODEL_COLOR, (
            <Box paddingX={1}>
              <Text bold color={MODEL_COLOR}>{model}</Text>
            </Box>
          ))}
          {level ? pill('effort', level.label, effortColor(level.value), (
            <Client key="effort" module="./pills.tsx" props={{ label: level.label, level: level.value }} />
          )) : null}
        </Box>
      </Box>
    )
  })

  // The open popup, at the left of the band, over the pills
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.surface !== 'terminal' || open === 'none' || e.props.hasSurvey) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const width = open === 'model' ? DROPDOWN_WIDTH : SLIDER_WIDTH
    const frame = (children: RenderChildren) => (
      <Box width={e.props.bodyColumns} justifyContent="flex-start">
        <Box width={width} borderStyle="round" borderDimColor paddingX={1} flexDirection="column">
          {children}
        </Box>
      </Box>
    )

    if (open === 'model') {
      const current = active()
      // A row: the number key, the name, a tick on the one in use
      const row = (o: Option, hotkey?: string) => (
        <Button
          key={'model-' + o.value}
          label={o.label + (o.value === current ? '  ✓' : '')}
          plain
          dimColor={o.value !== current}
          {...(hotkey ? { hotkey } : {})}
          onPress={() => pickModel($, o.value)}
        />
      )
      const more = options.filter(v => !MODELS.some(m => m.value === v)).map(v => ({ value: v, label: MORE_LABELS[v] ?? v }))
      return frame([
        ...MODELS.map((m, i) => row(m, String(i + 1))),
        <Text dimColor>{'─'.repeat(width - 4)}</Text>,
        <Button
          key="more"
          label={showMore ? 'Fewer models' : 'More models  ›'}
          plain
          dimColor
          onPress={() => ((showMore = !showMore), $.ui.invalidate('ui.render'))}
        />,
        ...(showMore ? more.map(o => row(o)) : []),
      ])
    }

    // The slider: a track of five stops, filled up to the knob, the levels under it
    const at = Math.max(0, EFFORTS.findIndex(x => x.value === effort))
    return frame([
      <Box flexDirection="row" justifyContent="space-between">
        <Text>
          <Text dimColor>Effort </Text>
          {EFFORTS[at]?.label ?? ''}
        </Text>
      </Box>,
      <Box flexDirection="row" justifyContent="space-between" marginTop={1}>
        <Text dimColor>Faster</Text>
        <Text dimColor>Smarter</Text>
      </Box>,
      <Box flexDirection="row">
        {EFFORTS.map((x, i) => (
          <Box width={STOP} justifyContent="center" backgroundColor={i <= at ? 'inactive' : 'subtle'}>
            <Button key={'stop-' + x.value} label={i === at ? '██' : '·'} plain dimColor={i !== at} onPress={() => pickEffort($, x.value)} />
          </Box>
        ))}
      </Box>,
      <Box flexDirection="row">
        {EFFORTS.map((x, i) => (
          <Box width={STOP} justifyContent="center">
            <Button key={'level-' + x.value} label={x.value} plain dimColor={i !== at} hotkey={String(i + 1)} onPress={() => pickEffort($, x.value)} />
          </Box>
        ))}
      </Box>,
    ])
  })
}
