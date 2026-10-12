// Clawd, the Claude Code mascot, as pixel art and as Raster cells.
//
// Drawn in quadrants: a character cell holds 2 by 2 of them, so the front view
// is 12 by 4 quadrants, 6 columns by 2 rows. Its body is 8 quadrants wide and
// 3 tall, eyes on the middle row, arms on the bottom one, four feet under it.
// Moving by one quadrant is what lets the eyes glance.
//
// At work it turns side on, as the desktop app draws it: facing left, one eye,
// its front arm out over the keys of a laptop whose lid leans back to the upper
// left. That view is 16 quadrants wide. Both views keep every edge between two
// colors on a cell boundary, so no cell needs more than its two colors, and the
// body sits in the same columns in both, so turning does not move it.

export const SPRITE_COLUMNS = 6
export const SPRITE_ROWS = 2

// The views in quadrants
const QW = SPRITE_COLUMNS * 2
const QH = SPRITE_ROWS * 2
const SIDE_QW = 16
// How far left of the front view the side view starts, in quadrants
export const SIDE_SHIFT = 6

// "The terminal's own color", the clawd orange, and the rest of the palette
export const DEFAULT = 0x01000000
export const BODY = 0xd77757
export const NAP = 0x8b949e
export const LAPTOP = 0x8b8b8b
// A closed eye: a dark line across the orange
const LID = 0x3a1a10

// What a quadrant holds: nothing, Clawd, the laptop
const EMPTY = 0
const ORANGE = 1
const GREY = 2
const COLORS = [DEFAULT, BODY, LAPTOP]

export type Pose = {
  // 'side' is the working view, facing left
  view: 'front' | 'side'
  // Eyes shifted one quadrant left or right
  look: -1 | 0 | 1
  eyes: 'open' | 'closed'
  // Front view: 'wave' raises the right arm only, 'behind' hides both behind its back
  arms: 'down' | 'up' | 'wave' | 'behind'
  // Side view: the laptop shut or open, and the front arm down on the keys or lifted
  laptop: 'closed' | 'open'
  hand: 'down' | 'up'
}

export const STANDING: Pose = { view: 'front', look: 0, eyes: 'open', arms: 'down', laptop: 'closed', hand: 'down' }

// A character drawn over the cells, such as a nap letter
export type Glyph = { column: number; row: number; char: string; color: number; background?: number }

// The 16 quadrant blocks, indexed by upper left 1, upper right 2, lower left 4, lower right 8
const QUADRANTS = [
  0x20, 0x2598, 0x259d, 0x2580, 0x2596, 0x258c, 0x259e, 0x259b,
  0x2597, 0x259a, 0x2590, 0x259c, 0x2584, 0x2599, 0x259f, 0x2588,
]

type Art = { q: Uint8Array; width: number; eyes: number[] }

function canvas(width: number) {
  const q = new Uint8Array(width * QH)
  const set = (x: number, y: number, value: number = ORANGE) => {
    q[y * width + x] = value
  }
  return { q, set }
}

// The front view: body, arms, four feet, two eyes
function front(pose: Pose): Art {
  const { q, set } = canvas(QW)

  // Body: quadrant columns 2 to 9, rows 0 to 2
  for (let y = 0; y <= 2; y++) for (let x = 2; x <= 9; x++) set(x, y)

  // Arms: two quadrants out from each side on the bottom body row, or raised
  // diagonally to the top corner. `mirror` turns the left arm into the right one.
  const arm = (isRaised: boolean, mirror: (x: number) => number) => {
    const shape = isRaised ? [[1, 1], [0, 0]] : [[0, 2], [1, 2]]
    for (const [x, y] of shape) set(mirror(x ?? 0), y ?? 0)
  }
  if (pose.arms !== 'behind') {
    arm(pose.arms === 'up', (x) => x)
    arm(pose.arms !== 'down', (x) => QW - 1 - x)
  }

  // Feet on the bottom row
  for (const x of [2, 4, 7, 9]) set(x, 3)

  const eyes = [4 + pose.look, 7 + pose.look]
  if (pose.eyes === 'open') for (const x of eyes) set(x, 1, EMPTY)
  return { q, width: QW, eyes }
}

// The side view at the laptop, facing left
function side(pose: Pose): Art {
  const { q, set } = canvas(SIDE_QW)

  // Body: quadrant columns 8 to 15, rows 0 to 2, the feet in two pairs below
  for (let y = 0; y <= 2; y++) for (let x = 8; x <= 15; x++) set(x, y)
  for (const x of [8, 10, 13, 15]) set(x, 3)

  // The laptop's base on the floor in front of it, the hinge at its left end
  for (let x = 2; x <= 7; x++) set(x, 3, GREY)
  if (pose.laptop === 'open') {
    // The lid leans back to the upper left, two quadrants thick
    for (const [x, y] of [[1, 2], [2, 2], [0, 1], [1, 1]]) set(x ?? 0, y ?? 0, GREY)
    // The front arm reaches out over the keys: down on them, or lifted a quadrant
    const y = pose.hand === 'down' ? 2 : 1
    for (let x = 4; x <= 7; x++) set(x, y)
  } else {
    // Shut: the lid lies on the base
    for (let x = 2; x <= 7; x++) set(x, 2, GREY)
  }

  // One eye, looking at the screen; a glance moves it a quadrant
  const eyes = [12 + pose.look]
  if (pose.eyes === 'open') for (const x of eyes) set(x, 1, EMPTY)
  return { q, width: SIDE_QW, eyes }
}

// The cells of a Raster `columns` by `rows`. `left` is the front view's left
// edge in quadrants (2 per column) and its top is row 0; the side view starts
// SIDE_SHIFT quadrants further left. Clipped at the edges, then glyphs over it.
export function cells(columns: number, rows: number, left: number, pose: Pose, glyphs: Glyph[] = []): string {
  const art = pose.view === 'side' ? side(pose) : front(pose)
  const origin = pose.view === 'side' ? left - SIDE_SHIFT : left
  const at = (qx: number, qy: number) => {
    const sx = qx - origin
    if (sx < 0 || sx >= art.width || qy >= QH) return EMPTY
    return art.q[qy * art.width + sx] ?? EMPTY
  }

  const view = new DataView(new ArrayBuffer(columns * rows * 12))
  const put = (i: number, char: number, fg: number, bg: number) => {
    view.setUint32(i * 12, char, true)
    view.setUint32(i * 12 + 4, fg, true)
    view.setUint32(i * 12 + 8, bg, true)
  }

  for (let row = 0; row < rows; row++) {
    for (let column = 0; column < columns; column++) {
      const quads = [at(column * 2, row * 2), at(column * 2 + 1, row * 2), at(column * 2, row * 2 + 1), at(column * 2 + 1, row * 2 + 1)]
      put(row * columns + column, ...paint(quads))
    }
  }

  // Shut eyes: a heavy line across the half cell above where the eye was
  const lids: Glyph[] = pose.eyes === 'closed'
    ? art.eyes.map((x) => {
        const qx = origin + x
        return { column: Math.floor(qx / 2), row: 0, char: qx % 2 ? '╺' : '╸', color: LID, background: BODY }
      })
    : []

  for (const g of [...lids, ...glyphs]) {
    if (g.column < 0 || g.column >= columns || g.row < 0 || g.row >= rows) continue
    put(g.row * columns + g.column, g.char.codePointAt(0) ?? 0x20, g.color, g.background ?? DEFAULT)
  }

  return toBase64(new Uint8Array(view.buffer))
}

// One cell from its four quadrants: the glyph covers the quadrants of one color
// and the background is the other. A cell of three colors gives its rarest to
// the most common, which the art avoids.
function paint(quads: number[]): [number, number, number] {
  const counts = new Map<number, number>()
  for (const v of quads) counts.set(v, (counts.get(v) ?? 0) + 1)
  const ranked = [...counts.entries()].sort((a, b) => b[1] - a[1]).map(([v]) => v)
  const kept = ranked.slice(0, 2)
  const top = kept[0] ?? EMPTY
  const cell = quads.map((v) => (kept.includes(v) ? v : top))

  // Prefer the empty quadrants as the background, so the terminal shows through
  const fg = kept.find((v) => v !== EMPTY) ?? EMPTY
  if (fg === EMPTY) return [0x20, DEFAULT, DEFAULT]
  const bg = kept.find((v) => v !== fg) ?? EMPTY
  const bits = cell.reduce((sum, v, i) => sum | (v === fg ? 1 << i : 0), 0)
  return [QUADRANTS[bits] ?? 0x20, COLORS[fg] ?? DEFAULT, COLORS[bg] ?? DEFAULT]
}

// Standard padded base64, from the web API every host has
function toBase64(bytes: Uint8Array): string {
  let binary = ''
  for (let i = 0; i < bytes.length; i += 0x8000) {
    binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000))
  }
  return btoa(binary)
}
