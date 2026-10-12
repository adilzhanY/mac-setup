import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderElement } from 'claude-code'

import type { AgentRun, Flow, Panel, Phase, PlannedTask } from '../types'

import {
  CRAB_COLUMNS,
  CRAB_ROWS,
  COSTUME_COLOR,
  crab,
  crabLine,
  flowBar,
  hex,
  lineBar,
  spinner,
  type CrabLook,
} from './pixels'

// savvy-progress for the terminal: the flow's bar above the prompt and a pane of
// subagents, each a costumed pixel crab that walks while it works. A terminal
// port of johnnyvizz's desktop mod (MIT), same tools and state, drawn in cells.

const flow = atom({ plugin: 'savvy-progress', key: 'flow' } as const, null)
const agents = atom({ plugin: 'savvy-progress', key: 'agents' } as const, [])
const panel = atom({ plugin: 'savvy-progress', key: 'panel' } as const, {
  isCompact: false,
  isDoneCollapsed: false,
  autoOpenedFor: '',
})
const now = atom({ plugin: 'savvy-progress', key: 'now' } as const, 0)

const TOOL = 'mcp__savvy-progress__progress'
const STEP_TOOL = 'mcp__savvy-progress__step'
const PANE = 'savvy-agents'
const PHASES: readonly Phase[] = ['plan', 'design', 'delegate', 'review', 'close']
const ACCENT = 0x8f8cf4
const DONE = 0x5fbf8f
const TICK_MS = 100

type ProgressInput = {
  title?: string
  total?: number
  done?: number
  phase?: Phase
  finished?: boolean
  tasks?: { title?: string; tier?: string; after?: number[] }[]
}

// ---------------------------------------------------------------------------
// Language: the `language` option, else Claude Code's `language` setting, else the
// process locale; English when nothing says Russian.

type Lang = 'en' | 'ru'

const STRINGS = {
  en: {
    pane: 'Agents',
    cost: 'Cost',
    tokens: 'Tokens',
    time: 'Time',
    collapse: 'compact',
    expand: 'expand',
    running: 'Running',
    finished: 'Finished',
    planned: 'Planned',
    empty: 'No subagents yet.',
    emptyHint: 'They show up here the moment one starts.',
    round: 'round',
    failed: 'error',
    after: 'after',
    opened: 'Agents panel opened.',
    closed: 'Agents panel closed.',
    done: 'Done',
    plan: 'Plan',
    design: 'Design',
    tasks: 'Tasks',
    review: 'Review',
    busy: 'running',
    agents: 'agents',
    working: (n: number) => `${n} ${n === 1 ? 'agent' : 'agents'} working`,
    phases: { plan: 'plan', design: 'design', delegate: 'delegate', review: 'review', close: 'close' },
  },
  ru: {
    pane: 'Агенты',
    cost: 'Стоимость',
    tokens: 'Токены',
    time: 'Время',
    collapse: 'свернуть',
    expand: 'развернуть',
    running: 'Работают',
    finished: 'Завершены',
    planned: 'Запланированы',
    empty: 'Субагентов пока нет.',
    emptyHint: 'Они появятся здесь, как только один запустится.',
    round: 'раунд',
    failed: 'ошибка',
    after: 'после',
    opened: 'Панель агентов открыта.',
    closed: 'Панель агентов закрыта.',
    done: 'Готово',
    plan: 'План',
    design: 'Дизайн',
    tasks: 'Задачи',
    review: 'Ревью',
    busy: 'в работе',
    agents: 'агенты',
    working: (n: number) => `В работе: ${n}`,
    phases: { plan: 'план', design: 'дизайн', delegate: 'задачи', review: 'ревью', close: 'итог' },
  },
} as const

// Module scope is fine here: session.start sets it again on every (re)load.
let lang: Lang = 'en'
const tr = () => STRINGS[lang]

const isRussian = (v: unknown): boolean => typeof v === 'string' && /^(ru|russian|рус)/i.test(v.trim())

async function detectLang($: EngineInterface, option: unknown): Promise<Lang> {
  if (option === 'en' || option === 'ru') return option
  try {
    const settings = (await $.settings.read()) as Record<string, unknown>
    if (typeof settings.language === 'string' && settings.language.trim()) return isRussian(settings.language) ? 'ru' : 'en'
  } catch {
    // No settings: fall through to the locale.
  }
  const locale = (await $.env.get('LC_ALL')) || (await $.env.get('LC_MESSAGES')) || (await $.env.get('LANG'))
  return isRussian(locale) ? 'ru' : 'en'
}

// ---------------------------------------------------------------------------
// The flow

const blank = (): Flow => ({
  title: 'savvy-flow',
  total: 0,
  done: 0,
  running: 0,
  phase: 'plan',
  isFinished: false,
  tasks: [],
})

const isNewFlow = (prev: Flow | null, input: ProgressInput): boolean =>
  !prev || prev.isFinished || (input.title !== undefined && input.title.trim() !== prev.title)

const cleanTasks = (tasks: ProgressInput['tasks']): PlannedTask[] | undefined =>
  tasks
    ?.filter(t => t.title?.trim())
    .map(t => ({
      title: (t.title ?? '').trim(),
      tier: (t.tier ?? '').replace(/^savvy-/, '').trim().toLowerCase(),
      after: (t.after ?? []).filter(n => Number.isInteger(n) && n > 0),
    }))

export const merge = (prev: Flow | null, input: ProgressInput): Flow => {
  // A new title means a new flow: never carry counters over from an earlier one.
  const base = isNewFlow(prev, input) || !prev ? blank() : { ...blank(), ...prev }
  const tasks = cleanTasks(input.tasks) ?? base.tasks
  const total = Math.max(0, Math.round(input.total ?? (input.tasks ? tasks.length : base.total)))
  const done = Math.min(total || Infinity, Math.max(0, Math.round(input.done ?? base.done)))
  const phase = input.phase && PHASES.includes(input.phase) ? input.phase : base.phase
  return {
    ...base,
    title: input.title?.trim() || base.title,
    total,
    done,
    phase: input.finished ? 'close' : phase,
    isFinished: input.finished === true,
    tasks,
  }
}

const label = (f: Flow): string => {
  const s = tr()
  if (f.isFinished) return s.done
  if (f.phase === 'plan') return s.plan
  if (f.phase === 'design') return s.design
  const count = f.total ? `${f.done}/${f.total}` : `${f.running} ${s.busy}`
  return `${f.phase === 'review' ? s.review : s.tasks} ${count}`
}

const ratio = (f: Flow): number => (f.isFinished ? 1 : f.total ? f.done / f.total : 0)

// ---------------------------------------------------------------------------
// Agents

// What each savvy tier runs on, for planned tasks that have no run yet.
const TIER_MODEL: Record<string, string> = {
  fable: 'Fable · high',
  heavy: 'Opus · xhigh',
  careful: 'Opus · high',
  medium: 'Opus · medium',
  light: 'Opus · low',
}

// USD per million tokens: input, output, cache read, cache write (5-minute TTL).
// The engine reports tokens, not money, so the panel's cost is an estimate.
const PRICES: [RegExp, [number, number, number, number]][] = [
  [/fable|mythos/, [10, 50, 0.25, 12.5]],
  [/opus-5-5/, [4, 20, 0.2, 5]],
  [/opus/, [5, 25, 0.5, 6.25]],
  [/sonnet/, [2, 10, 0.2, 2.5]],
  [/haiku/, [1, 5, 0.1, 1.25]],
]

type Usage = {
  input_tokens: number
  output_tokens: number
  cache_read_input_tokens: number
  cache_creation_input_tokens: number
}

const priceOf = (model: string): [number, number, number, number] =>
  PRICES.find(([re]) => re.test(model.toLowerCase()))?.[1] ?? [4, 20, 0.2, 5]

const costOf = (model: string, u: Usage): number => {
  const [i, o, r, w] = priceOf(model)
  return (
    ((u.input_tokens || 0) * i +
      (u.output_tokens || 0) * o +
      (u.cache_read_input_tokens || 0) * r +
      (u.cache_creation_input_tokens || 0) * w) /
    1e6
  )
}

const sumTokens = (u: Usage): number =>
  (u.input_tokens || 0) + (u.output_tokens || 0) + (u.cache_read_input_tokens || 0) + (u.cache_creation_input_tokens || 0)

const windowOf = (model: string): number => (/haiku/i.test(model) ? 200_000 : 1_000_000)

// `savvy-careful`, or `savvy-flow:savvy-careful` when the agents ship in a plugin.
const tierOf = (type: string): string => {
  const bare = type.replace(/^[^:]*:/, '')
  const t = bare.replace(/^savvy-/, '').toLowerCase()
  return t in TIER_MODEL && bare.startsWith('savvy-') ? t : 'other'
}

// Which crab an agent is: a savvy tier wears its own costume, any other agent the
// one its job reads as, from its description ("Designer: icons", "Run the tests")
const TIER_COSTUME: Record<string, string> = {
  fable: 'astronaut',
  heavy: 'detective',
  careful: 'engineer',
  medium: 'chef',
  light: 'racer',
}

const ROLES: [RegExp, string][] = [
  [/design|illustrat|artist|visual|icon|\bui\b|\bux\b|styl|brand|logo|layout|mockup/i, 'designer'],
  [/test|review|\bqa\b|verif|audit|inspect|debug|investigat|check/i, 'detective'],
  [/fix|infra|deploy|devops|setup|install|config|migrat|refactor|engineer|\bops\b|perf|optimi/i, 'engineer'],
  [/explor|scout|research|search|find|survey|map|read/i, 'pirate'],
  [/plan|architect|strateg|spec\b|roadmap/i, 'astronaut'],
]

export const costumeOf = (type: string, description = ''): string => {
  const tier = tierOf(type)
  if (tier !== 'other') return TIER_COSTUME[tier] ?? 'plain'
  if (type === 'Explore') return 'pirate'
  if (type === 'Plan') return 'astronaut'
  // Building, writing code and anything unnamed: the developer at a laptop
  return ROLES.find(([re]) => re.test(`${description} ${type}`))?.[1] ?? 'developer'
}

const plannedCostume = (pl: PlannedTask): string => TIER_COSTUME[pl.tier] ?? costumeOf('', pl.title)

const colorOf = (costume: string): number => COSTUME_COLOR[costume] ?? COSTUME_COLOR.plain ?? 0xd97757

export const modelName = (id: string): string => {
  const m = /(fable|mythos|opus|sonnet|haiku)-(\d+)(?:-(\d{1,2})(?!\d))?/i.exec(id)
  const [, family = '', major = '', minor] = m ?? []
  if (!family) return id.replace(/^claude-/, '').replace(/\[.*\]$/, '') || '?'
  return `${family.charAt(0).toUpperCase()}${family.slice(1).toLowerCase()} ${major}${minor ? '.' + minor : ''}`
}

const norm = (s: string): string => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim()

const fmtTokens = (n: number): string =>
  n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${Math.round(n / 1e3)}k` : `${Math.round(n)}`

const fmtCost = (usd: number): string => `$${usd < 10 ? usd.toFixed(2) : usd.toFixed(1)}`

export const fmtTime = (ms: number): string => {
  const s = Math.max(0, Math.round(ms / 1000))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const ss = String(s % 60).padStart(2, '0')
  return h ? `${h}:${String(m).padStart(2, '0')}:${ss}` : `${m}:${ss}`
}

const elapsed = (a: AgentRun, at: number): number => (a.endedAt ?? Math.max(at, a.startedAt)) - a.startedAt

type Planned = PlannedTask & { n: number }

const plannedOf = (f: Flow | null, list: AgentRun[]): Planned[] => {
  if (!f || f.isFinished) return []
  const started = new Set(list.map(a => norm(a.description)))
  return (f.tasks ?? []).map((t, i) => ({ ...t, n: i + 1 })).filter(t => !started.has(norm(t.title)))
}

const totals = (list: AgentRun[], at: number) => {
  const cost = list.reduce((s, a) => s + a.costUsd, 0)
  const tokens = list.reduce((s, a) => s + a.tokens, 0)
  const start = Math.min(...list.map(a => a.startedAt))
  const end = Math.max(...list.map(a => a.endedAt ?? Math.max(at, a.startedAt)))
  return { cost, tokens, time: list.length ? end - start : 0 }
}

// The task's own progress when the worker reports steps; a finished run is full.
const progressOf = (a: AgentRun): number | null => {
  if (a.status === 'done') return 1
  if (a.stepTotal) return Math.min(1, (a.stepDone ?? 0) / a.stepTotal)
  return null
}

const ctxOf = (a: AgentRun): number => (a.contextMax ? Math.min(100, Math.round((a.contextTokens / a.contextMax) * 100)) : 0)

// ---------------------------------------------------------------------------
// Animation. Each render records how to draw every Raster it mounts; one clock
// repaints the ones whose cells changed with $.ui.blit, so a frame never costs a
// render pass. Still Rasters are recorded too, so a blit of a moving frame that
// lands after the redraw that stopped it is put right on the next tick. A blit
// the surface refuses (the pane closed, the band redrawn without it) drops the
// entry until the next render records it again.

type Live = Map<string, (tick: number) => string>

let tick = 0
const paneLive: Live = new Map()
const bandLive: Live = new Map()
let bandSite: string | undefined
const sent = new Map<string, string>()

// Crabs step about three times a second; the racer twice as fast.
const frameOf = (costume: string, t: number): number => Math.floor(t / (costume === 'racer' ? 1.5 : 3))

function repaint($: EngineInterface, site: string | undefined, live: Live) {
  if (site === undefined) return
  for (const [key, draw] of live) {
    const cells = draw(tick)
    const id = `${site}/${key}`
    if (sent.get(id) === cells) continue
    sent.set(id, cells)
    $.ui
      .blit({ requestId: site, key, cells })
      .then(r => {
        if (r.deny !== undefined) live.delete(key)
      })
      .catch(() => live.delete(key))
  }
}

// ---------------------------------------------------------------------------
// The pane

// Opens the agents pane, or closes it when it is up; true when it ends up open.
// A pane opened unasked on a narrow terminal waits undrawn, or sits behind another
// pane's tab: that counts as closed, so the press brings it up instead.
// Callers await this inside the press or command, so the open counts as asked.
async function togglePane($: EngineInterface): Promise<boolean> {
  const isOpen = (await $.ui.panes()).some(p => p.id === PANE && p.isShown && p.isPlaced)
  if (isOpen) {
    // Our own close skips our ui.close hook, so its rasters are dropped here
    paneLive.clear()
    await $.ui.close({ id: PANE })
    return false
  }
  const at = await $.clock.now()
  await update($, now, () => at)
  await $.ui.open({ id: PANE, title: tr().pane, columns: 64 })
  return true
}

async function autoOpen($: EngineInterface, key: string): Promise<void> {
  const p = await read($, panel)
  if (p.autoOpenedFor === key) return
  await update($, panel, prev => ({ ...prev, autoOpenedFor: key }))
  void $.ui.open({ id: PANE, title: tr().pane, columns: 64 })
}

export const register: Register = (on, options) => {
  on('session.start', async ($, e, next) => {
    const started = await next(e)
    lang = await detectLang($, options.language)
    await $.tool.register({
      name: 'progress',
      description:
        'Report /savvy-flow progress to the progress bar above the prompt and the agents panel. ' +
        'Call it after presenting the plan (title, total, tasks, phase "delegate"), each time a task is accepted (done), ' +
        'when switching phase or re-planning (tasks), and once at the end with finished: true. Fields left out keep their previous value.',
      inputSchema: {
        type: 'object',
        properties: {
          title: { type: 'string', description: 'Short name of the overall task, a few words.' },
          total: { type: 'integer', minimum: 0, description: 'Number of planned worker tasks.' },
          done: { type: 'integer', minimum: 0, description: 'Number of tasks accepted after review.' },
          phase: { type: 'string', enum: [...PHASES] },
          finished: { type: 'boolean', description: 'True once the flow is closed.' },
          tasks: {
            type: 'array',
            description:
              'The planned worker tasks in order, numbered from 1. Each title must equal the Agent tool `description` the task will be delegated with, so the panel can match runs to tasks.',
            items: {
              type: 'object',
              properties: {
                title: { type: 'string', description: 'A few words; reused verbatim as the Agent description.' },
                tier: { type: 'string', enum: ['fable', 'heavy', 'careful', 'medium', 'light'] },
                after: { type: 'array', items: { type: 'integer' }, description: 'Numbers of the tasks this one waits for.' },
              },
              required: ['title', 'tier'],
            },
          },
        },
      },
    })
    await $.tool.register({
      name: 'step',
      description:
        'For savvy-flow workers: report progress on your own task to the agents panel. ' +
        'Right after reading the brief, call it with `total` (your plan in 3-8 steps) and `done: 0`; ' +
        'call it again as each step finishes. Cheap and silent: it only draws a bar.',
      inputSchema: {
        type: 'object',
        properties: {
          done: { type: 'integer', minimum: 0, description: 'Steps finished so far.' },
          total: { type: 'integer', minimum: 1, description: 'Steps planned; may change if the plan changes.' },
          note: { type: 'string', description: 'The step in progress, a few words.' },
        },
        required: ['done'],
      },
    })
    await $.command.register({
      name: 'agents-info',
      description: 'Show or hide the panel of subagents: running, finished and planned, with model, context, cost and time',
      immediate: true,
    })

    $.clock.every(TICK_MS, () => {
      tick += 1
      repaint($, PANE, paneLive)
      repaint($, bandSite, bandLive)
    })

    // Ticks the running agents' clocks once a second; quiet when nothing runs.
    $.clock.every(1000, () => {
      void (async () => {
        const list = await read($, agents)
        if (!list.some(a => a.status === 'running')) return
        const at = await $.clock.now()
        await update($, now, () => at)
      })()
    })
    return started
  })

  on('command.run', { command: 'agents-info' }, async $ => {
    const isOpen = await togglePane($)
    return { text: isOpen ? tr().opened : tr().closed }
  })

  on('ui.close', { id: PANE }, ($, e, next) => {
    paneLive.clear()
    return next(e)
  })

  on('tool.call', { tool: TOOL }, async ($, e) => {
    const input = e as unknown as ProgressInput
    const prev = await read($, flow)
    if (isNewFlow(prev, input) && input.title !== undefined) {
      // A new flow starts with a clean list; agents still running stay.
      await update($, agents, list => list.filter(a => a.status === 'running'))
    }
    const merged = await update($, flow, p => merge(p, input))
    if (merged && input.tasks?.length) await autoOpen($, merged.title)
    return { result: `ok: ${label(merged ?? blank())}` }
  })

  // A worker's own progress: the call runs in the worker's loop, so agentId names it.
  on('tool.call', { tool: STEP_TOOL }, async ($, e) => {
    const input = e as unknown as { done?: number; total?: number; note?: string }
    const agentId = e.agentId
    if (!agentId) return { result: 'ignored: only subagents report steps' }
    await update($, agents, list =>
      list.map(a => {
        if (a.agentId !== agentId) return a
        const total = Math.max(0, Math.round(input.total ?? a.stepTotal ?? 0))
        const done = Math.max(0, Math.round(input.done ?? a.stepDone ?? 0))
        return { ...a, stepTotal: total, stepDone: total ? Math.min(total, done) : done, stepNote: input.note?.trim() || undefined }
      }),
    )
    return { result: 'ok' }
  })

  // Safety net: worker launches move the twinkling layer even if the orchestrator forgets to report.
  on('tool.call', { tool: 'Agent' }, async ($, e, next) => {
    const type = String(e.subagent_type ?? '')
    if (!type.replace(/^[^:]*:/, '').startsWith('savvy-')) return next(e)

    await update($, flow, prev => {
      const base = prev && !prev.isFinished ? { ...blank(), ...prev } : blank()
      return { ...base, running: base.running + 1, phase: base.phase === 'plan' ? 'delegate' : base.phase }
    })
    try {
      return await next(e)
    } finally {
      await update($, flow, prev => (prev ? { ...prev, running: Math.max(0, prev.running - 1) } : prev))
    }
  })

  on('agent.spawn', async ($, e, next) => {
    const started = await next(e)
    if (started.deny !== undefined) return started

    const at = await $.clock.now()
    await update($, agents, list => {
      const round = 1 + list.filter(a => norm(a.description) === norm(e.description) && e.description).length
      const run: AgentRun = {
        id: started.agentId ?? e.tool_use_id,
        agentId: started.agentId,
        type: e.subagentType,
        description: e.description,
        model: started.model,
        status: 'running',
        startedAt: at,
        contextTokens: 0,
        contextMax: windowOf(started.model),
        tokens: 0,
        costUsd: 0,
        steps: 0,
        round,
      }
      return [...list.filter(a => a.id !== run.id), run].slice(-200)
    })
    await update($, now, () => at)
    if (e.subagentType.replace(/^[^:]*:/, '').startsWith('savvy-')) {
      const f = await read($, flow)
      await autoOpen($, f && !f.isFinished ? f.title : 'savvy-flow')
    }
    return started
  })

  // Each model request of a subagent: live context, tokens and cost.
  on('turn.step', async function* ($, e, next) {
    const result = yield* next(e)
    const agentId = e.agentId
    const usage = result.usage
    if (!agentId || !usage) return result

    const model = usage.model || e.model
    await update($, agents, list =>
      list.map(a =>
        a.agentId !== agentId
          ? a
          : {
              ...a,
              model,
              effort: typeof e.effort === 'string' ? e.effort : a.effort,
              status: 'running',
              endedAt: undefined,
              contextTokens: sumTokens(usage),
              contextMax: windowOf(model),
              tokens: a.tokens + sumTokens(usage),
              costUsd: a.costUsd + costOf(model, usage),
              steps: a.steps + 1,
            },
      ),
    )
    return result
  })

  on('turn.complete', async ($, e, next) => {
    const agentId = e.agentId
    if (agentId) {
      const at = await $.clock.now()
      await update($, agents, list =>
        list.map(a => {
          if (a.agentId !== agentId) return a
          // A run whose steps went unseen still gets the turn's own sum.
          const usage = a.steps === 0 ? e.usage : undefined
          return {
            ...a,
            status: e.reason === 'answer' ? 'done' : 'failed',
            endedAt: at,
            ...(usage
              ? { model: usage.model || a.model, tokens: sumTokens(usage), costUsd: costOf(usage.model || a.model, usage) }
              : {}),
          }
        }),
      )
      await update($, now, () => at)
    }
    return next(e)
  })

  // -------------------------------------------------------------------------
  // The pane

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e, next) => {
    if (e.surface !== 'terminal') return next(e)
    const s = tr()
    const { Box, Text, Button, Raster } = $.ui.resolve(e)
    const list = await read($, agents)
    const f = await read($, flow)
    const p: Panel = await read($, panel)
    const at = Math.max(await read($, now), ...list.map(a => a.startedAt), 0)

    const running = list.filter(a => a.status === 'running').reverse()
    const finished = list.filter(a => a.status !== 'running').reverse()
    const planned = plannedOf(f, list)
    const t = totals(list, at)
    const title = f && !f.isFinished ? f.title : ''
    // A column of margin at each side, so the frame and the transcript beside it stay clear
    const cols = Math.max(30, e.props.bodyColumns - 2)
    // Right of the crab: its 12 columns and a gap of 2
    const textW = Math.max(12, cols - CRAB_COLUMNS - 2)

    paneLive.clear()
    const crabRaster = (key: string, look: CrabLook, isRunning: boolean) => {
      const still = crab(look)
      paneLive.set(key, isRunning ? n => crab({ ...look, frame: frameOf(look.costume, n) }) : () => still)
      return <Raster key={key} columns={CRAB_COLUMNS} rows={CRAB_ROWS} cells={crab({ ...look, frame: isRunning ? frameOf(look.costume, tick) : 0 })} />
    }

    const rule = (text: string) => (
      <Text key={`h-${text}`} dimColor wrap="truncate-end">
        {text + ' ' + '─'.repeat(Math.max(0, cols - text.length - 1))}
      </Text>
    )

    const agentCard = (a: AgentRun) => {
      const costume = costumeOf(a.type, a.description)
      const tier = tierOf(a.type)
      const color = colorOf(costume)
      const isRunning = a.status === 'running'
      const ctx = ctxOf(a)
      const progress = progressOf(a)
      const meta = [a.effort ? `${modelName(a.model)} · ${a.effort}` : modelName(a.model)]
      if (a.round > 1) meta.push(`${s.round} ${a.round}`)
      if (a.status === 'failed') meta.push(s.failed)
      const steps = a.stepTotal ? `${a.stepDone ?? 0}/${a.stepTotal}${a.stepNote ? '  ' + a.stepNote : ''}` : ''
      const stats = `ctx ${ctx}% · ${fmtTokens(a.contextTokens)}  ≈${fmtCost(a.costUsd)}  ${fmtTime(elapsed(a, at))}`
      // Without reported steps the bar shows the context fill, in grey.
      const barColor = progress === null ? 0x8a8a86 : a.status === 'failed' ? 0xd0453f : color
      const bar = (n: number | null) => lineBar({ columns: textW, ratio: progress ?? ctx / 100, color: barColor, tick: n })
      const stillBar = bar(null)
      paneLive.set(`bar-${a.id}`, isRunning ? bar : () => stillBar)
      if (isRunning) paneLive.set(`spin-${a.id}`, n => spinner(color, n))

      return (
        <Box key={a.id} flexDirection="row" columnGap={2} marginBottom={1}>
          {crabRaster(`crab-${a.id}`, { costume }, isRunning)}
          <Box flexDirection="column" flexGrow={1} paddingTop={1}>
            <Box flexDirection="row" justifyContent="space-between" columnGap={1}>
              <Text bold wrap="truncate-end">
                {a.description || a.type}
              </Text>
              {isRunning ? (
                <Raster key={`spin-${a.id}`} columns={1} rows={1} cells={spinner(color, tick)} />
              ) : a.status === 'done' ? (
                <Text color="success">✓</Text>
              ) : (
                <Text color="error">✗</Text>
              )}
            </Box>
            <Text wrap="truncate-end">
              <Text color={hex(color)}>{tier === 'other' ? a.type : tier}</Text>
              <Text dimColor>{'  ' + meta.join(' · ')}</Text>
            </Text>
            <Box flexDirection="row" justifyContent="space-between" columnGap={2} marginTop={1}>
              <Text wrap="truncate-end">{steps}</Text>
              <Text dimColor wrap="truncate-start">
                {stats}
              </Text>
            </Box>
            <Raster key={`bar-${a.id}`} columns={textW} rows={1} cells={bar(isRunning ? tick : null)} />
          </Box>
        </Box>
      )
    }

    const plannedCard = (pl: Planned) => {
      const tier = pl.tier in TIER_MODEL ? pl.tier : 'other'
      const costume = plannedCostume(pl)
      const meta = [TIER_MODEL[tier] ?? '']
      if (pl.after.length) meta.push(`${s.after} ${pl.after.join(', ')}`)
      return (
        <Box key={`plan-${pl.n}`} flexDirection="row" columnGap={2} marginBottom={1}>
          {crabRaster(`crab-plan-${pl.n}`, { costume, isDim: true }, false)}
          <Box flexDirection="column" flexGrow={1} paddingTop={1}>
            <Box flexDirection="row" justifyContent="space-between" columnGap={1}>
              <Text dimColor wrap="truncate-end">
                {`${pl.n}. ${pl.title}`}
              </Text>
              <Text dimColor>◷</Text>
            </Box>
            <Text wrap="truncate-end">
              <Text color={hex(colorOf(costume))} dimColor>
                {tier}
              </Text>
              <Text dimColor>{'  ' + meta.filter(Boolean).join(' · ')}</Text>
            </Text>
          </Box>
        </Box>
      )
    }

    // The flow's phases, the current one lit
    const phaseIndex = f ? PHASES.indexOf(f.phase) : -1
    const stepper = f && !f.isFinished && (
      <Text wrap="truncate-end">
        {PHASES.map((ph, i) => (
          <Text key={ph}>
            {i > 0 && <Text dimColor>{' › '}</Text>}
            {i === phaseIndex ? (
              <Text bold color={hex(ACCENT)}>
                {s.phases[ph]}
              </Text>
            ) : (
              <Text dimColor={i > phaseIndex}>{s.phases[ph]}</Text>
            )}
          </Text>
        ))}
      </Text>
    )

    const tileW = Math.floor((cols - 2) / 3)
    const tile = (k: string, v: string) => (
      <Box key={k} flexDirection="column" width={tileW} borderStyle="round" borderDimColor paddingX={1}>
        <Text dimColor wrap="truncate-end">
          {k}
        </Text>
        <Text bold wrap="truncate-end">
          {v}
        </Text>
      </Box>
    )

    const header = (
      <Box flexDirection="column" marginBottom={1}>
        <Box flexDirection="row" justifyContent="space-between" columnGap={1}>
          <Text bold wrap="truncate-end">
            <Text color={hex(f?.isFinished ? DONE : ACCENT)}>● </Text>
            {title || s.pane}
          </Text>
          <Button
            key="compact"
            label={p.isCompact ? s.expand : s.collapse}
            plain
            dimColor
            onPress={() => update($, panel, prev => ({ ...prev, isCompact: !prev.isCompact }))}
          />
        </Box>
        {stepper}
        <Box flexDirection="row" columnGap={1}>
          {tile(s.cost, '≈' + fmtCost(t.cost))}
          {tile(s.tokens, fmtTokens(t.tokens))}
          {tile(s.time, fmtTime(t.time))}
        </Box>
      </Box>
    )

    if (list.length === 0 && planned.length === 0) {
      return (
        <Box flexDirection="column" paddingX={1}>
          {header}
          <Box flexDirection="row" columnGap={2}>
            {crabRaster('crab-empty', { costume: 'plain', isDim: true }, false)}
            <Box flexDirection="column" justifyContent="center">
              <Text>{s.empty}</Text>
              <Text dimColor>{s.emptyHint}</Text>
            </Box>
          </Box>
        </Box>
      )
    }

    if (p.isCompact) {
      // The whole crew in lines of as many as fit, walking while they work
      type Member = { look: CrabLook; isRunning: boolean }
      const crew: Member[] = [
        ...running.map(a => ({ look: { costume: costumeOf(a.type, a.description) }, isRunning: true })),
        ...finished.map(a => ({ look: { costume: costumeOf(a.type, a.description) }, isRunning: false })),
        ...planned.map(pl => ({ look: { costume: plannedCostume(pl), isDim: true }, isRunning: false })),
      ]
      const fit = Math.max(1, Math.floor((cols + 1) / (CRAB_COLUMNS + 1)))
      // ponytail: four lines of crabs at most, the rest counted; scroll them if crews grow past that
      const lines = Array.from({ length: Math.min(4, Math.ceil(crew.length / fit)) }, (_, i) => crew.slice(i * fit, (i + 1) * fit))
      const hidden = crew.length - lines.flat().length
      const counts = [
        running.length && `${running.length} ${s.running.toLowerCase()}`,
        finished.length && `${finished.length} ${s.finished.toLowerCase()}`,
        planned.length && `${planned.length} ${s.planned.toLowerCase()}`,
      ].filter(Boolean)
      return (
        <Box flexDirection="column" paddingX={1}>
          {header}
          {lines.map((members, i) => {
            const draw = (n: number | null) =>
              crabLine(members.map(c => ({ ...c.look, frame: c.isRunning && n !== null ? frameOf(c.look.costume, n) : 0 })))
            paneLive.set(`crew-${i}`, draw)
            return <Raster key={`crew-${i}`} columns={members.length * (CRAB_COLUMNS + 1)} rows={CRAB_ROWS} cells={draw(tick)} />
          })}
          <Text dimColor>
            {counts.join(' · ')}
            {hidden > 0 ? `  +${hidden}` : ''}
          </Text>
        </Box>
      )
    }

    return (
      <Box flexDirection="column" paddingX={1}>
        {header}
        {running.length > 0 && rule(`${s.running} · ${running.length}`)}
        {running.map(agentCard)}
        {finished.length > 0 && (
          <Box key="h-done" flexDirection="row">
            <Button
              key="done"
              label={`${p.isDoneCollapsed ? '▸' : '▾'} ${s.finished} · ${finished.length}`}
              plain
              dimColor
              onPress={() => update($, panel, prev => ({ ...prev, isDoneCollapsed: !prev.isDoneCollapsed }))}
            />
            <Text dimColor>{' ' + '─'.repeat(Math.max(0, cols - `▾ ${s.finished} · ${finished.length}`.length - 1))}</Text>
          </Box>
        )}
        {!p.isDoneCollapsed && finished.map(agentCard)}
        {planned.length > 0 && rule(`${s.planned} · ${planned.length}`)}
        {planned.map(plannedCard)}
      </Box>
    )
  })

  // -------------------------------------------------------------------------
  // The band: one row above whatever the mods beneath draw there (Clawd).

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey || e.surface !== 'terminal') return next(e)
    const f = await read($, flow)
    const list = await read($, agents)
    const running = list.filter(a => a.status === 'running')
    // No flow: a row only while some subagent works
    if (f === null && running.length === 0) return next(e)

    const below = await next(e)
    const { Box, Text, Button, Raster } = $.ui.resolve(e)
    const stack = (row: RenderElement): RenderElement =>
      below ? (
        <Box flexDirection="column">
          {row}
          {below}
        </Box>
      ) : (
        row
      )
    bandSite = e.requestId
    bandLive.clear()

    if (f === null) {
      // Who is working, for how long, and the button to the panel
      const at = Math.max(await read($, now), ...running.map(a => a.startedAt))
      const lead = running[running.length - 1]
      const color = colorOf(costumeOf(lead?.type ?? '', lead?.description))
      bandLive.set('band-spin', n => spinner(color, n))
      return stack(
        <Box key="savvy-row" flexDirection="row" columnGap={1}>
          <Raster key="band-spin" columns={1} rows={1} cells={spinner(color, tick)} />
          <Text bold>{tr().working(running.length)}</Text>
          <Box flexGrow={1} flexShrink={1}>
            <Text dimColor wrap="truncate-end">
              {running.map(a => a.description || a.type).join(' · ')}
            </Text>
          </Box>
          <Text dimColor>{fmtTime(Math.max(...running.map(a => elapsed(a, at))))}</Text>
          <Button key="savvy-agents" label={`${tr().agents} ×${list.length}`} onPress={() => togglePane($)} />
        </Box>,
      )
    }

    const crew = list.length + plannedOf(f, list).length
    const color = f.isFinished ? DONE : ACCENT
    const percent = `${Math.round(ratio(f) * 100)}%`.padStart(4)
    const crewLabel = `[ ${tr().agents} ×${crew} ]`

    // ● title  [bar]  pct  ×n ✕, a column between each
    const cols = e.props.bodyColumns
    const titleW = Math.max(6, Math.min(f.title.length, 32, Math.floor(cols * 0.3)))
    const barW = Math.max(8, cols - (2 + titleW) - percent.length - crewLabel.length - 1 - 5)
    // Moving while a turn runs or a subagent works in the background
    const isAnimated = !f.isFinished && (e.props.isWorking || list.some(a => a.status === 'running'))
    const bar = (n: number | null) =>
      flowBar({
        columns: barW,
        ratio: ratio(f),
        inFlight: f.total ? Math.min(1, (f.done + f.running) / f.total) : 0,
        segments: f.total,
        color,
        label: label(f),
        tick: n,
      })

    const stillBar = bar(null)
    bandLive.set('flow-bar', isAnimated ? bar : () => stillBar)

    const row = (
      <Box key="savvy-row" flexDirection="row" columnGap={1}>
        <Box width={2 + titleW} flexShrink={0}>
          <Text wrap="truncate-end">
            <Text color={hex(color)}>● </Text>
            <Text bold>{f.title}</Text>
          </Text>
        </Box>
        <Raster key="flow-bar" columns={barW} rows={1} cells={bar(isAnimated ? tick : null)} />
        <Text dimColor>{percent}</Text>
        <Button key="savvy-agents" label={crewLabel.slice(2, -2)} onPress={() => togglePane($)} />
        <Button key="savvy-dismiss" label="✕" plain dimColor role="dismiss" onPress={() => update($, flow, () => null)} />
      </Box>
    )
    return stack(row)
  })
}
