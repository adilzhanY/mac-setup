import type { EngineInterface, Register } from 'claude-code'

import { count, hour, modelName, mobyDick, tokens, type RangeKey, type Stats } from './format'

// The desktop app's usage card, in the terminal. A fresh session runs the
// /stats-card command, and the card draws in place of its output row, right
// under the logo; the command shows it again any time. The numbers come from
// scripts/stats.mjs, which reads the transcripts and Claude Code's own stats
// cache in a process of its own; the tabs and the ranges are buttons.

const SCRIPT = '/dev/claude-mods/stats-card/scripts/stats.mjs'
const COMMAND = 'stats-card'
// The heatmap's blues, light to dark, from the desktop card
const BLUES = ['#86acea', '#6394e3', '#407cdd', '#2566d0']
// The card's inside: 26 weeks of two-column days with a column between them
const MAX_INNER = 77
const MIN_INNER = 44
const RANGES: [RangeKey, string][] = [['all', 'All'], ['30d', '30d'], ['7d', '7d']]

let stats: Stats | undefined
let failure: string | undefined
let tab: 'overview' | 'models' = 'overview'
let range: RangeKey = 'all'

async function load($: EngineInterface) {
  try {
    const home = await $.env.get('HOME')
    // The first run reads every transcript, a few seconds; later runs only what changed
    const result = await $.process.run(['node', home + SCRIPT], { timeoutMs: 300_000 })
    if (result.exitCode !== 0) throw new Error(result.stderr.trim().split('\n').at(-1) || `exit ${result.exitCode}`)
    stats = JSON.parse(result.stdout) as Stats
  } catch (err) {
    failure = err instanceof Error ? err.message : String(err)
  }
  $.ui.invalidate('ui.render')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    try {
      await $.command.register({ name: 'stats-card', description: 'Show your Claude Code usage card', immediate: true })
    } catch {
      // A taken name leaves the card without its command
    }
    // Off the session's start: a fresh session prints the card, which fills in when the numbers are ready.
    // Only with a person at the prompt: in a `claude -p` run the card would become the run's output.
    if (!e.isInteractive) return next(e)
    $.clock.after(0, async () => {
      if ((await $.session.turns()) === 0) await $.command.run({ command: COMMAND }).catch(() => undefined)
      await load($)
    })
    return next(e)
  })

  // The command's row: a short line for the model, the card drawn in its place
  on('command.run', { command: 'stats-card' }, async $ => {
    if (!stats) void load($)
    return { text: 'Usage card shown.' }
  })

  on('ui.render', { component: 'CommandOutput' }, async ($, e, next) => {
    if (e.props.command !== COMMAND) return next(e)

    const inner = Math.min(MAX_INNER, (e.viewport?.columns ?? 100) - 6)
    if (inner < MIN_INNER) return next(e)

    const { Box, Button, Text } = $.ui.resolve(e)
    const redraw = () => $.ui.invalidate('ui.render')

    // A tab or a range: the chosen one on the tile color, the rest dim
    const choice = (key: string, label: string, isOn: boolean, onPress: () => void) => (
      <Box paddingX={1} {...(isOn ? { backgroundColor: 'subtle' } : {})}>
        <Button key={key} label={label} plain dimColor={!isOn} onPress={onPress} />
      </Box>
    )

    const header = (
      <Box flexDirection="row" justifyContent="space-between">
        <Box flexDirection="row">
          {choice('tab-overview', 'Overview', tab === 'overview', () => ((tab = 'overview'), redraw()))}
          {choice('tab-models', 'Models', tab === 'models', () => ((tab = 'models'), redraw()))}
        </Box>
        <Box flexDirection="row">
          {RANGES.map(([key, label]) => choice('range-' + key, label, range === key, () => ((range = key), redraw())))}
        </Box>
      </Box>
    )

    let body
    if (!stats) {
      body = <Text dimColor>{failure ? 'Stats unavailable: ' + failure : 'Reading your sessions...'}</Text>
    } else if (tab === 'overview') {
      const r = stats.ranges[range]
      const width = Math.floor((inner - 2) / 3)
      const tile = (label: string, value: string) => (
        <Box backgroundColor="subtle" paddingX={1} width={width} flexDirection="column">
          <Text color="inactive" wrap="truncate-end">{label}</Text>
          <Text bold wrap="truncate-end">{value}</Text>
        </Box>
      )
      const favorite = r.models[0]

      // The heatmap: as many of the last 26 weeks as fit, a column each, Monday on top
      const { weeks, levels } = stats.heatmap
      const shown = Math.min(weeks, Math.floor((inner + 1) / 3))
      const rows = Array.from({ length: 7 }, (_, day) => (
        <Text>
          {Array.from({ length: shown }, (_, i) => {
            const level = levels[(weeks - shown + i) * 7 + day] ?? -1
            const gap = i < shown - 1 ? ' ' : ''
            if (level < 0) return '  ' + gap
            return <Text color={level === 0 ? 'subtle' : (BLUES[level - 1] ?? 'subtle')}>{'▇▇' + gap}</Text>
          })}
        </Text>
      ))
      const footnote = mobyDick(r.tokens)

      body = (
        <Box flexDirection="column">
          <Box flexDirection="row" columnGap={1}>
            {tile('Sessions', count(r.sessions))}
            {tile('Messages', count(r.messages))}
            {tile('Total tokens', tokens(r.tokens))}
          </Box>
          <Box flexDirection="row" columnGap={1} marginTop={1}>
            {tile('Active days', count(r.activeDays))}
            {tile('Peak hour', hour(r.peakHour))}
            {tile('Favorite model', favorite ? modelName(favorite.model) : 'none yet')}
          </Box>
          <Box flexDirection="column" marginTop={1}>{rows}</Box>
          {footnote ? <Box marginTop={1}><Text dimColor>{footnote}</Text></Box> : null}
        </Box>
      )
    } else {
      // Models: each one's share of the range's tokens, as a bar
      const r = stats.ranges[range]
      const top = r.models.slice(0, 8)
      const bar = Math.max(10, inner - 14 - 8 - 6 - 3)
      body = top.length === 0 ? <Text dimColor>No model use in this range.</Text> : (
        <Box flexDirection="column">
          {top.map(m => {
            const share = r.tokens > 0 ? m.tokens / r.tokens : 0
            const filled = Math.max(1, Math.round(share * bar))
            return (
              <Box flexDirection="row" columnGap={1}>
                <Box width={14}><Text wrap="truncate-end">{modelName(m.model)}</Text></Box>
                <Text>
                  <Text color={BLUES[1]}>{'▆'.repeat(filled)}</Text>
                  <Text color="subtle">{'▆'.repeat(bar - filled)}</Text>
                </Text>
                <Box width={8} justifyContent="flex-end"><Text>{tokens(m.tokens)}</Text></Box>
                <Box width={6} justifyContent="flex-end"><Text dimColor>{Math.round(share * 100) + '%'}</Text></Box>
              </Box>
            )
          })}
        </Box>
      )
    }

    return (
      <Box width={inner + 4} borderStyle="round" borderDimColor paddingX={1} flexDirection="column">
        {header}
        <Box marginTop={1} flexDirection="column">{body}</Box>
      </Box>
    )
  })
}
