import type { EngineInterface, Register } from 'claude-code'

import { blockColor, kindOf, labelOf, parseNumstat, statusOf, type Call, type Stats } from './strip'

import { NAP, SPRITE_COLUMNS, SPRITE_ROWS, cells, type Glyph, type Pose } from './sprite'

// Clawd stands on the prompt, at the right end of the band above it. It blinks
// and glances around. When Claude starts working it reaches behind its back,
// turns side on with a laptop in front of it, opens the lid and types, as the
// desktop app draws it; when the turn ends it shuts the lid, puts the laptop
// away and cheers. After a while with nothing to do it naps.
// A button on the left of the band hides it, and the same spot shows it again.
// Between them, the work strip: a block per tool call this turn, what it is
// doing now, and the uncommitted changes in the session's repo (+added -deleted).

const KEY = 'clawd'
const TICK_MS = 100
// Columns left of the sprite: 3 for the side view's laptop, the rest for the nap
// letters and the code it types
const SIDE_COLUMNS = 6
const RASTER_COLUMNS = SPRITE_COLUMNS + SIDE_COLUMNS
// Ticks of no turns before it naps: 5 minutes
const NAP_AFTER = 3000
const CHEER_TICKS = 18
const GREET_TICKS = 14
// The steps of getting the laptop out and putting it away
const REACH_TICKS = 7
const UNPACK_TICKS = 5
const PACK_TICKS = 4
const STOW_TICKS = 4
// What floats up off the keys while it types
const CODE = ['{', '}', ';', '<', '>', '/', '=', '(', ')']

type Mode = 'greet' | 'idle' | 'reach' | 'unpack' | 'type' | 'pack' | 'stow' | 'cheer' | 'nap'

// What it says when the pointer rests on it
const SAYS: Record<Mode, string> = {
  greet: "hi, I'm Clawd",
  idle: "hi, I'm Clawd",
  reach: 'working...',
  unpack: 'working...',
  type: 'working...',
  pack: 'done!',
  stow: 'done!',
  cheer: 'done!',
  nap: 'zzz',
}

// Where the band is and how wide the Raster was drawn, for $.ui.blit
let site: string | undefined
let columns = RASTER_COLUMNS
let isWorking = false
let isHidden = false

let mode: Mode = 'greet'
let modeTicks = GREET_TICKS
let t = 0
let lastActive = 0
let blinkTicks = 0
let nextBlink = 30
let look: -1 | 0 | 1 = 0
let lookTicks = 0
let nextLook = 60
// Typing: whether the hand is down on the keys, how long until it moves, and a pause to read
let hand: Pose['hand'] = 'down'
let tapTicks = 0
let readTicks = 0
let lastCells = ''

// The work strip: this turn's tool calls, and the uncommitted changes of the repo
const MAX_CALLS = 200
let calls: Call[] = []
let stats: Stats | null = null
let statsPending = false

// Its blinks, glances and typing pauses come from a seeded generator: seeded by
// the clock at the session's start, so it differs between sessions and repeats
// exactly under a test's mocked clock
let seed = 1
function random(n: number): number {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0
  return Math.floor((seed / 2 ** 32) * n)
}

function setMode(next: Mode, ticks = 0) {
  mode = next
  modeTicks = ticks
}

// Glance one way for a moment, now and then
function glance() {
  if (lookTicks > 0 && --lookTicks === 0) look = 0
  if (lookTicks === 0 && t >= nextLook) {
    look = random(2) ? 1 : -1
    lookTicks = 10 + random(20)
    nextLook = t + 50 + random(90)
  }
}

// One step of its life, every TICK_MS
function advance() {
  t += 1
  if (isWorking) lastActive = t

  // Work starts: get the laptop out, or go back to it if it was being put away
  if (isWorking) {
    if (mode === 'idle' || mode === 'nap' || mode === 'greet' || mode === 'cheer') setMode('reach', REACH_TICKS)
    else if (mode === 'stow') setMode('unpack', UNPACK_TICKS)
    else if (mode === 'pack') setMode('type')
  } else if (mode === 'reach' || mode === 'unpack' || mode === 'type') {
    // Work ends: shut the lid
    hand = 'down'
    look = 0
    setMode('pack', PACK_TICKS)
  }

  switch (mode) {
    case 'reach':
      // A look over its shoulder at what it is reaching for
      look = modeTicks > 3 ? 1 : 0
      if (--modeTicks <= 0) setMode('unpack', UNPACK_TICKS)
      break
    case 'unpack':
      look = 0
      if (--modeTicks <= 0) setMode('type')
      break
    case 'type':
      if (readTicks > 0) {
        // Reading what it wrote, the hand lifted off the keys
        readTicks -= 1
        hand = 'up'
        glance()
        if (readTicks === 0) look = 0
      } else if (--tapTicks <= 0) {
        // A key: down for a moment, up for a moment, at an uneven pace
        hand = hand === 'down' ? 'up' : 'down'
        tapTicks = hand === 'down' ? 1 : 1 + random(2)
        if (random(40) === 0) readTicks = 8 + random(14)
      }
      break
    case 'pack':
      if (--modeTicks <= 0) setMode('stow', STOW_TICKS)
      break
    case 'stow':
      if (--modeTicks <= 0) setMode('cheer', CHEER_TICKS)
      break
    case 'cheer':
    case 'greet':
      if (--modeTicks <= 0) setMode('idle')
      break
    case 'idle':
      glance()
      if (t - lastActive > NAP_AFTER) {
        look = 0
        setMode('nap')
      }
      break
    case 'nap':
      break
  }

  // Blink every few seconds, now and then twice
  if (blinkTicks > 0) blinkTicks -= 1
  else if (t >= nextBlink && mode !== 'nap') {
    blinkTicks = 2
    nextBlink = t + (random(5) ? 30 + random(50) : 4)
  }
}

function pose(): Pose {
  const flap = Math.floor(modeTicks / 3) % 2 === 0
  const arms =
    mode === 'cheer' ? (flap ? 'up' : 'down')
    : mode === 'greet' ? (flap ? 'wave' : 'down')
    : mode === 'reach' || mode === 'stow' ? 'behind'
    : 'down'
  return {
    // Side on at the laptop, as the desktop app draws it
    view: mode === 'unpack' || mode === 'type' || mode === 'pack' ? 'side' : 'front',
    look,
    eyes: mode === 'nap' || blinkTicks > 0 ? 'closed' : 'open',
    arms,
    laptop: mode === 'type' ? 'open' : 'closed',
    hand: mode === 'type' ? hand : 'down',
  }
}

// Letters drifting up and away from its head on the left: z's while it naps,
// a character of code now and then while it types
function sideGlyphs(spriteColumn: number): Glyph[] {
  const at = (dx: number, row: number, char: string): Glyph => ({ column: spriteColumn + dx, row, char, color: NAP })
  if (mode === 'nap') {
    const phases: Glyph[][] = [
      [at(-1, 1, 'z')],
      [at(-1, 1, 'z'), at(-2, 0, 'z')],
      [at(-2, 0, 'z'), at(-4, 0, 'Z')],
      [at(-4, 0, 'Z')],
      [],
    ]
    return phases[Math.floor(t / 7) % phases.length] ?? []
  }
  if (mode === 'type' && readTicks === 0) {
    const char = CODE[Math.floor(t / 30) % CODE.length] ?? ';'
    // Out of the top of the screen, which leans up 3 columns left of where it stands
    const phases: Glyph[][] = [[at(-4, 0, char)], [at(-5, 0, char)], [at(-6, 0, char)], [], [], []]
    return phases[Math.floor(t / 5) % phases.length] ?? []
  }
  return []
}

function frame(): string {
  const left = (columns - SPRITE_COLUMNS) * 2
  return cells(columns, SPRITE_ROWS, left, pose(), sideGlyphs(columns - SPRITE_COLUMNS))
}

// The uncommitted changes, from git: null where the session is not in a repo
async function refreshStats($: EngineInterface) {
  try {
    const result = await $.process.run(['git', 'diff', 'HEAD', '--numstat'], { timeoutMs: 15_000 })
    stats = result.exitCode === 0 ? parseNumstat(result.stdout) : null
  } catch {
    stats = null
  }
  $.ui.invalidate('ui.render')
}

// An edit changes the numbers: they are read again, at most once a second
function refreshStatsSoon($: EngineInterface) {
  if (statsPending) return
  statsPending = true
  $.clock.after(1000, async () => {
    statsPending = false
    await refreshStats($)
  })
}

// Hide or show it, remembered across sessions; it waves hello when it comes back
async function setHidden($: EngineInterface, hidden: boolean) {
  isHidden = hidden
  if (!hidden) setMode('greet', GREET_TICKS)
  $.ui.invalidate('ui.render')
  await $.store.set('isHidden', hidden)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    seed = (await $.clock.now()) >>> 0 || 1
    isHidden = (await $.store.get('isHidden')) === true

    $.clock.every(TICK_MS, () => {
      if (isHidden || site === undefined) return
      const before = SAYS[mode]
      advance()
      // What it says on hover is part of the tree, so a change redraws it
      if (SAYS[mode] !== before) {
        $.ui.invalidate('ui.render')
        return
      }
      const drawn = frame()
      if (drawn === lastCells) return
      lastCells = drawn
      // A blit with the band collapsed or mid redraw is refused; the next render draws the frame
      $.ui.blit({ requestId: site, key: KEY, cells: drawn }).catch(() => {
        lastCells = ''
      })
    })

    try {
      await $.command.register({ name: 'clawd', description: 'Show or hide Clawd on the prompt', immediate: true })
    } catch {
      // A taken name leaves Clawd without its command, and nothing else
    }
    $.clock.after(0, () => refreshStats($))
    return next(e)
  })

  on('command.run', { command: 'clawd' }, async $ => {
    await setHidden($, !isHidden)
    return {}
  })

  // A prompt wakes it, and it looks over at what you typed
  on('prompt.submit', ($, e, next) => {
    lastActive = t
    if (mode === 'nap') {
      setMode('idle')
      look = -1
      lookTicks = 12
    }
    return next(e)
  })

  // A new turn starts the strip over
  on('turn.start', ($, e, next) => {
    calls = []
    $.ui.invalidate('ui.render')
    return next(e)
  })

  // A tool call is a block in the strip: running until its result, then ok or failed
  on('tool.call', async ($, e, next) => {
    const input = e as unknown as Record<string, unknown>
    const call: Call = {
      id: e.tool_use_id ?? `call-${calls.length}-${Date.now()}`,
      tool: e.tool,
      kind: kindOf(e.tool),
      label: labelOf(e.tool, input),
      state: 'running',
    }
    calls = [...calls, call].slice(-MAX_CALLS)
    $.ui.invalidate('ui.render')

    const result = await next(e)
    const failed = Boolean(result.deny) || result.isError === true
    call.state = failed ? 'failed' : 'ok'
    if (call.kind === 'edit' && !failed) refreshStatsSoon($)
    $.ui.invalidate('ui.render')
    return result
  }).catch(($, e, next) => next(e))

  on('turn.complete', ($, e, next) => {
    isWorking = false
    // A call still running when the turn ends was cut short
    for (const call of calls) if (call.state === 'running') call.state = 'failed'
    $.clock.after(0, () => refreshStats($))
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    // The desktop app draws its own Clawd; a survey has the band to itself
    if (e.surface !== 'terminal' || e.props.hasSurvey || e.props.maxRows < SPRITE_ROWS) {
      return next(e)
    }

    isWorking = e.props.isWorking
    // Another mod drawing in the band (the model picker's popup) has it while it does
    const theirs = await next(e)
    if (theirs !== null && typeof theirs === 'object' && 'type' in theirs && theirs.type !== 'engine') return theirs

    const { Box, Button, Raster, Text } = $.ui.resolve(e)

    site = e.requestId
    columns = Math.max(SPRITE_COLUMNS, Math.min(e.props.bodyColumns - 15, RASTER_COLUMNS))
    lastCells = frame()
    const says = SAYS[mode]

    // The strip takes what the button and Clawd leave: a column per block, the rest for the status
    const beside = 14 + 4 + (isHidden ? 0 : columns)
    const stripWidth = Math.max(0, e.props.bodyColumns - beside)
    const running = calls.findLast(c => c.state === 'running')
    const shown = stripWidth > 0 ? calls.slice(-stripWidth) : []
    const files = stats?.files ?? 0
    const strip = (
      <Box flexGrow={1} flexDirection="column" paddingX={2} height={SPRITE_ROWS} justifyContent="space-between">
        <Text>{shown.length ? shown.map(c => <Text color={blockColor(c)}>{'\u25ae'}</Text>) : ' '}</Text>
        {running ? (
          <Text dimColor wrap="truncate-end">{statusOf(running)}</Text>
        ) : isWorking ? (
          <Text dimColor>thinking</Text>
        ) : stats && files > 0 ? (
          <Box flexDirection="row" columnGap={1}>
            <Text color="success">{'+' + stats.added}</Text>
            <Text color="error">{'-' + stats.deleted}</Text>
            <Text dimColor>{`in ${files} ${files === 1 ? 'file' : 'files'}`}</Text>
          </Box>
        ) : stats ? (
          <Text dimColor>no uncommitted changes</Text>
        ) : (
          ' '
        )}
      </Box>
    )

    if (isHidden) {
      return (
        <Box width={e.props.bodyColumns} alignItems="flex-end">
          <Box height={SPRITE_ROWS} flexDirection="column" justifyContent="flex-end">
            <Button key="show" label="show Clawd" dimColor onPress={() => setHidden($, false)} />
          </Box>
          {strip}
        </Box>
      )
    }

    return (
      <Box width={e.props.bodyColumns} alignItems="flex-end">
        <Box height={SPRITE_ROWS} flexDirection="column" justifyContent="flex-end">
          <Button key="hide" label="hide Clawd" dimColor onPress={() => setHidden($, true)} />
        </Box>
        {strip}
        <Box key="clawd-hover" width={columns} height={SPRITE_ROWS}>
          <Raster key={KEY} columns={columns} rows={SPRITE_ROWS} cells={lastCells} />
          <Box
            position="absolute"
            top={0}
            right={columns}
            display="none"
            hover={{ display: 'flex' }}
            borderStyle="round"
            borderDimColor
            paddingX={1}
          >
            <Text dimColor>{says}</Text>
          </Box>
        </Box>
      </Box>
    )
  })
}
