// Everything savvy-progress draws as cells: the costumed crabs, the bars and
// the spinner. Each is a Raster's `cells` string, repainted by `$.ui.blit`.
//
// The crabs are half-block pixel art: a cell holds two square pixels, the top
// one as the foreground of `▀` and the bottom one as its background, so every
// pixel keeps its own true color. A crab is 16 by 12 pixels, 16 columns by 6 rows.

export const DEFAULT = 0x01000000

const CLAY = 0xd97757
const INK = 0x1f1e1d
const STEEL = 0x8e929a
const WHITE = 0xf8f6f1
const GOLD = 0xf5c542

// Each costume's own color: an agent's label and bars are drawn in it
export const COSTUME_COLOR: Record<string, number> = {
  astronaut: 0x7f77dd,
  detective: 0xd85a30,
  engineer: 0xba7517,
  chef: 0x378add,
  racer: 0x1d9e75,
  pirate: 0xc8679a,
  developer: 0x4fa3c7,
  designer: 0xd0435a,
  // Claude's own clay, for an agent nothing tells apart
  plain: CLAY,
}

export const hex = (c: number): string => '#' + c.toString(16).padStart(6, '0')

// Mixes `a` toward `b` by `k` (0 keeps a, 1 gives b)
export function mix(a: number, b: number, k: number): number {
  const ch = (s: number) => {
    const x = (a >> s) & 0xff
    const y = (b >> s) & 0xff
    return Math.round(x + (y - x) * k) << s
  }
  return ch(16) | ch(8) | ch(0)
}

// ---------------------------------------------------------------------------
// Cells

type Cell = [char: number, fg: number, bg: number]

export function encode(cells: Cell[]): string {
  const view = new DataView(new ArrayBuffer(cells.length * 12))
  cells.forEach(([c, fg, bg], i) => {
    view.setUint32(i * 12, c, true)
    view.setUint32(i * 12 + 4, fg, true)
    view.setUint32(i * 12 + 8, bg, true)
  })
  const bytes = new Uint8Array(view.buffer)
  let binary = ''
  for (let i = 0; i < bytes.length; i += 0x8000) binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000))
  return btoa(binary)
}

const cp = (s: string): number => s.codePointAt(0) ?? 0x20
const BLANK: Cell = [0x20, DEFAULT, DEFAULT]

// ---------------------------------------------------------------------------
// Crabs
//
// Clawd as the desktop app draws its crew: a body 10 wide and 6 tall with two
// square eyes, stubby arms out of its sides and four long legs, the outer pairs
// close together. It stands in columns 1 to 14 of a 16 by 12 grid: the rows
// above the body hold the hats, and the edge columns the props it holds out.
// Costumes are drawn a row down from where their numbers say (see crabPixels),
// so row -1 is the grid's top: the tallest hats and props reach it.

// 0 is an empty pixel; anything else a color
type Px = number[]
type Put = (x: number, y: number, c: number) => void

const rect = (put: Put, x: number, y: number, w: number, h: number, c: number) => {
  for (let dy = 0; dy < h; dy++) for (let dx = 0; dx < w; dx++) put(x + dx, y + dy, c)
}

// Stamps rows of palette letters at (x, y); '.' leaves a pixel alone
function stamp(put: Put, x: number, y: number, rows: string[], map: Record<string, number>) {
  rows.forEach((row, dy) => [...row].forEach((ch, dx) => map[ch] !== undefined && put(x + dx, y + dy, map[ch] ?? 0)))
}

type Pose = {
  // Walking: frames 1 and 3 lift one pair of legs each
  step: number
  // Arms raised a pixel (typing, holding something up)
  leftUp?: boolean
  rightUp?: boolean
}

function body(put: Put, { step, leftUp, rightUp }: Pose) {
  rect(put, 3, 2, 10, 6, CLAY)
  rect(put, 5, 4, 2, 2, INK)
  rect(put, 9, 4, 2, 2, INK)
  rect(put, 1, leftUp ? 4 : 5, 2, 2, CLAY)
  rect(put, 13, rightUp ? 4 : 5, 2, 2, CLAY)
  const lifted = step % 4 === 1 ? [3, 10] : step % 4 === 3 ? [5, 12] : []
  for (const x of [3, 5, 10, 12]) rect(put, x, 8, 1, lifted.includes(x) ? 2 : 3, CLAY)
}

// Each costume draws the whole crab for animation frame `f` in its color `t`.
// The frames are what a running crab cycles through; a still one shows frame 0.
const COSTUMES: Record<string, (put: Put, f: number, t: number) => void> = {
  // Magnifier held up on the right, a deerstalker with a red band; the lens
  // sweeps across and glints
  detective: (put, f) => {
    body(put, { step: f, rightUp: true })
    stamp(put, 4, -1, ['..bbbb..', '.bcbbcb.', 'bbcbbcbb'], { b: 0x7a4a26, c: 0xb08050 })
    rect(put, 2, 2, 12, 1, 0xc8452c)
    const dx = [0, 0, -1, -1][f % 4] ?? 0
    stamp(put, 13 + dx, -1, ['kkk', 'kgk', 'kkk'], { k: 0x4a4e57, g: f % 4 === 2 ? 0xe6f4ff : 0x9cc8e8 })
    put(14 + dx, 2, 0x7a4a26)
  },
  // Headphones on, typing on a laptop held in front; the hands tap and the
  // logo on the lid pulses
  developer: (put, f) => {
    const tap = f % 2 === 1
    body(put, { step: 0, leftUp: tap, rightUp: !tap })
    rect(put, 4, 0, 8, 1, 0x3a3d45)
    rect(put, 3, 1, 1, 1, 0x3a3d45)
    rect(put, 12, 1, 1, 1, 0x3a3d45)
    stamp(put, 2, 2, ['kk', 'kp', 'kk'], { k: 0x3a3d45, p: 0x6b6f7a })
    stamp(put, 12, 2, ['kk', 'pk', 'kk'], { k: 0x3a3d45, p: 0x6b6f7a })
    rect(put, 4, 6, 8, 2, 0xc9ccd4)
    rect(put, 4, 8, 8, 1, 0x8e929a)
    const logo = [0x8f8cf4, 0xb3b0ff, 0x8f8cf4, 0x6b68d0][f % 4] ?? 0x8f8cf4
    rect(put, 7, 6, 2, 1, logo)
  },
  // A red beret, a paintbrush held up on the right and a palette on the left;
  // the brush paints and dips into a new color
  designer: (put, f) => {
    body(put, { step: f, rightUp: true })
    stamp(put, 3, -1, ['....bb....', '..rrrrrr..', '.rrrrrrrrr', 'dddddddddd'], { b: 0x8e2a3b, r: 0xd0435a, d: 0x8e2a3b })
    const tip = [0x4aa3e8, 0x4aa3e8, 0xe25a5a, 0xf5c542][f % 4] ?? 0x4aa3e8
    const lean = f % 2
    rect(put, 15 - lean, -1, 1, 2, tip)
    rect(put, 15, 1, 1, 4, 0xc9a26b)
    stamp(put, 0, 5, ['www', 'rbw', 'wyw'], { w: 0xe8cf9f, r: 0xe25a5a, b: 0x4aa3e8, y: f % 4 === 3 ? 0xffffff : 0xf5c542 })
  },
  // A yellow hard hat with an orange badge; the wrench in the left hand turns a bolt
  engineer: (put, f) => {
    body(put, { step: f, leftUp: true })
    stamp(put, 4, -1, ['..yyyy..', '.yyooyyy', 'yyyooyyy'], { y: GOLD, o: 0xe0782a })
    rect(put, 2, 2, 12, 1, 0xc99a1e)
    const wrench = [
      ['s.s', 'sss', '.s.'],
      ['s..', '.ss', '.s.'],
      ['...', 'sss', '.s.'],
      ['s..', '.ss', '.s.'],
    ][f % 4] ?? []
    stamp(put, 0, -1, wrench, { s: STEEL })
  },
  // Astronaut in a glass dome: its legs dangle as if afloat, a glint runs over
  // the glass and a star blinks
  astronaut: (put, f, t) => {
    body(put, { step: 0 })
    if (f % 2) for (const x of [5, 10]) put(x, 10, 0)
    stamp(put, 2, -1, ['...wwwwww...', '.ww......ww.', 'w..........w'], { w: 0xe6e8ee })
    rect(put, 2, 2, 1, 3, 0xe6e8ee)
    rect(put, 13, 2, 1, 3, 0xe6e8ee)
    const glint = [[3, 1], [4, 0], [5, 0], [4, 0]][f % 4] ?? [3, 1]
    put(glint[0] ?? 3, glint[1] ?? 1, 0xffffff)
    rect(put, 7, 7, 2, 1, t)
    if (f % 2 === 0) stamp(put, 14, -1, ['.y', 'yy'], { y: GOLD })
  },
  // Chef in a toque: tosses the omelette out of the pan
  chef: (put, f, t) => {
    body(put, { step: f, rightUp: true })
    stamp(put, 4, -1, ['.ww..ww.', 'wwwwwwww', 'wwgwwgww', 'tttttttt'], { w: 0xf4f3ee, g: 0xd2d1c8, t })
    rect(put, 13, 4, 3, 1, 0x4a4a48)
    const egg = [3, 1, 0, 1][f % 4] ?? 3
    put(14, egg, 0xf5b731)
  },
  // Racer in a helmet: runs at double pace, the checkered flag flutters
  racer: (put, f, t) => {
    body(put, { step: f, leftUp: true })
    stamp(put, 3, -1, ['...tttt...', '.tttwwttt.', 'ttttwwtttt', 'vvvvvvvvvv'], { t, w: WHITE, v: 0x3b4a5e })
    rect(put, 0, -1, 1, 5, STEEL)
    stamp(put, 1, -1, f % 2 ? ['kw', 'wk'] : ['wk', 'kw'], { w: WHITE, k: INK })
  },
  // Pirate scouting the code: an eye patch, and the cutlass fences
  pirate: (put, f) => {
    body(put, { step: f, rightUp: true })
    stamp(put, 3, -1, ['k........k', 'kk......kk', 'kkkkwwkkkk', '.gggggggg.'], { k: 0x55514c, w: WHITE, g: GOLD })
    rect(put, 9, 4, 2, 2, INK)
    put(8, 3, INK)
    const blade = f % 2 ? [[14, 0], [14, 1], [15, 2], [15, 3]] : [[15, 0], [15, 1], [15, 2], [15, 3]]
    for (const [x, y] of blade) put(x ?? 0, y ?? 0, 0xc9ccd2)
    rect(put, 14, 4, 2, 1, 0x7a4a26)
  },
  plain: (put, f) => body(put, { step: f }),
}

export const costumes = Object.keys(COSTUMES)

export const CRAB_COLUMNS = 16
export const CRAB_ROWS = 6
const W = CRAB_COLUMNS
const H = CRAB_ROWS * 2

export type CrabLook = {
  costume: string
  // Animation frame; a crab that is not running stays on 0
  frame?: number
  // Planned crabs are drawn faded toward grey
  isDim?: boolean
}

export function crabPixels({ costume, frame = 0, isDim }: CrabLook): Px {
  const px: Px = new Array(W * H).fill(0)
  // A row down: the costumes' row -1 is the grid's top
  const put: Put = (x, y, c) => {
    if (x >= 0 && x < W && y + 1 >= 0 && y + 1 < H) px[(y + 1) * W + x] = c
  }
  const draw = COSTUMES[costume] ?? COSTUMES.plain
  draw?.(put, frame, COSTUME_COLOR[costume] ?? CLAY)
  return isDim ? px.map(c => (c ? mix(c, 0x808080, 0.62) : 0)) : px
}

// Two pixels a cell: the upper one `▀`'s foreground, the lower one its background
export function halfBlocks(px: Px, columns: number, rows: number): Cell[] {
  const cells: Cell[] = []
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < columns; c++) {
      const top = px[r * 2 * columns + c] ?? 0
      const low = px[(r * 2 + 1) * columns + c] ?? 0
      if (!top && !low) cells.push(BLANK)
      else if (!low) cells.push([0x2580, top, DEFAULT])
      else if (!top) cells.push([0x2584, low, DEFAULT])
      else if (top === low) cells.push([0x2588, top, DEFAULT])
      else cells.push([0x2580, top, low])
    }
  }
  return cells
}

export const crab = (look: CrabLook): string => encode(halfBlocks(crabPixels(look), W, CRAB_ROWS))

// A line of crabs side by side, a column apart: the compact panel
export function crabLine(looks: CrabLook[]): string {
  const columns = looks.length * (W + 1)
  const out: Cell[] = new Array(columns * CRAB_ROWS).fill(BLANK)
  looks.forEach((look, i) => {
    halfBlocks(crabPixels(look), W, CRAB_ROWS).forEach((cell, j) => {
      out[Math.floor(j / W) * columns + i * (W + 1) + (j % W)] = cell
    })
  })
  return encode(out)
}

// ---------------------------------------------------------------------------
// The flow's bar above the prompt: a solid fill with a pill at its head, a
// twinkling layer for tasks handed out and not yet accepted, then the track,
// one segment per planned task.

const EIGHTHS = [0x20, 0x258f, 0x258e, 0x258d, 0x258c, 0x258b, 0x258a, 0x2589, 0x2588]
const TWINKLE = ['⠂', '⠄', '⠐', '⠠', '⠈', '⠁', '⡀', '⢀'].map(cp)
export const TRACK = 0x6b6b68

// Deterministic noise, so a still frame is the same frame every time
const noise = (x: number, y: number): number => {
  const s = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453
  return s - Math.floor(s)
}

export type FlowBar = {
  columns: number
  ratio: number
  // Accepted plus handed to workers, as a share of the plan
  inFlight: number
  segments: number
  color: number
  label: string
  // Animation tick, or null for a still bar
  tick: number | null
}

export function flowBar({ columns, ratio, inFlight, segments, color, label, tick }: FlowBar): string {
  const fillAt = Math.max(0, Math.min(columns, ratio * columns))
  const full = Math.floor(fillAt)
  const flightEnd = Math.min(columns, Math.round(Math.max(inFlight, ratio) * columns))
  const pill = ` ${label} `
  // The pill rides the head of the fill, held inside the bar
  const pillEnd = Math.max(pill.length, Math.min(columns, Math.round(fillAt)))
  const pillStart = pillEnd - pill.length
  // The shimmer: a soft band of light sweeping along the fill
  const sweep = tick === null ? -99 : ((tick * 0.8) % (Math.max(full, 1) + 16)) - 8
  const cells: Cell[] = []

  for (let x = 0; x < columns; x++) {
    const inPill = x >= pillStart && x < pillEnd
    // Darker at the tail, full color at the head
    let c = mix(color, 0x000000, 0.32 * (1 - x / Math.max(1, full)))
    const glow = Math.max(0, 1 - Math.abs(x - sweep) / 4)
    if (glow) c = mix(c, 0xffffff, 0.38 * glow)

    if (inPill) {
      const ch = cp(pill[x - pillStart] ?? ' ')
      cells.push([ch, 0xffffff, x < full ? mix(color, 0xffffff, 0.12) : mix(color, 0x000000, 0.1)])
    } else if (x < full) {
      cells.push([0x20, DEFAULT, c])
    } else if (x === full && fillAt > full) {
      cells.push([EIGHTHS[Math.round((fillAt - full) * 8)] ?? 0x20, color, DEFAULT])
    } else if (x < flightEnd) {
      // Handed out: braille sparks that twinkle while a turn runs
      const n = noise(x, tick === null ? 0 : Math.floor(tick / 2))
      cells.push([TWINKLE[Math.floor(n * TWINKLE.length)] ?? 0x2802, mix(color, 0xffffff, n * 0.3), DEFAULT])
    } else {
      // The track, with a gap where one task ends and the next begins
      const isGap = segments > 1 && segments < columns / 3 && [...Array(segments - 1)].some((_, i) => Math.round(((i + 1) * columns) / segments) === x)
      cells.push(isGap ? BLANK : [0x2501, TRACK, DEFAULT])
    }
  }
  return encode(cells)
}

// ---------------------------------------------------------------------------
// An agent's own bar: a thin heavy line, with eighths of a cell at its head

export type LineBar = {
  columns: number
  ratio: number
  color: number
  tick: number | null
}

export function lineBar({ columns, ratio, color, tick }: LineBar): string {
  const at = Math.max(0, Math.min(columns, ratio * columns))
  const full = Math.floor(at)
  const sweep = tick === null ? -99 : ((tick * 0.6) % (Math.max(full, 1) + 12)) - 6
  const cells: Cell[] = []
  for (let x = 0; x < columns; x++) {
    if (x < full || (x === full && at - full >= 0.5)) {
      const glow = Math.max(0, 1 - Math.abs(x - sweep) / 3)
      const c = mix(color, 0xffffff, 0.45 * glow)
      cells.push([x === full ? 0x2578 : 0x2501, c, DEFAULT])
    } else {
      cells.push([0x2500, TRACK, DEFAULT])
    }
  }
  return encode(cells)
}

// ---------------------------------------------------------------------------
// A one-cell spinner for a running agent

const SPIN = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'].map(cp)

export const spinner = (color: number, tick: number): string =>
  encode([[SPIN[tick % SPIN.length] ?? 0x280b, color, DEFAULT]])
