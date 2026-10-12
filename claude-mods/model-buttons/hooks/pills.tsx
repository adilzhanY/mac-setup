import type { ClientModule } from 'claude-code'

import { EFFORT_COLORS as COLORS } from './colors'

// The effort pill's letters, drawn on the surface's own thread so High and Max
// can shimmer, a gradient moving through the letters, with no hook redraws.
//
// It draws and nothing else. A Client that listens to the pointer makes the
// terminal report the mouse in pixels, and in kitty with a window margin that
// puts every click in the session on the wrong cell. The hooks module lays a
// Button over this drawing on hover; that is what takes the click.

export type PillProps = { label: string; level: string }

type State = { phase: number }

// One frame of the shimmer, and how many frames it takes to cross the label
const FRAME_MS = 80
const SWEEP = 20

type Rgb = [number, number, number]
const rgb = (hex: string): Rgb => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)) as Rgb
const toHex = (c: Rgb) => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('')
const mix = (a: Rgb, b: Rgb, t: number): Rgb => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]

// The color of letter `i` of `n` at frame `phase`: a wave of the second color
// rolling left to right through the first
export function shimmer(pair: [string, string], i: number, n: number, phase: number): string {
  const wave = 0.5 + 0.5 * Math.cos(2 * Math.PI * (i / Math.max(n, 1) - phase / SWEEP))
  return toHex(mix(rgb(pair[1]), rgb(pair[0]), wave))
}

// The props of the last call, which the shimmer's clock reads
let latest: PillProps | undefined

const Pill: ClientModule<PillProps, State> = (props, surface) => {
  latest = props
  const { Box, Text } = surface.elements
  const state = surface.state ?? { phase: 0 }
  const color = COLORS[props.level]

  if (surface.state === undefined) {
    surface.setState(state)
    // The shimmer's clock; a level without one leaves the frame as it is
    surface.every(FRAME_MS, () => {
      if (Array.isArray(latest ? COLORS[latest.level] : undefined)) surface.setState({ phase: (surface.state ?? state).phase + 1 })
    })
  }

  return (
    <Box paddingX={1}>
      <Text>
        {props.label.split('').map((ch, i) => (
          <Text color={Array.isArray(color) ? shimmer(color, i, props.label.length, state.phase) : (color ?? 'text')}>{ch}</Text>
        ))}
      </Text>
    </Box>
  )
}

export default Pill
