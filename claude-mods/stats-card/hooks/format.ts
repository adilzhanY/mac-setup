// How the card writes its numbers: the stats script's JSON in, short labels out.

export type Range = {
  sessions: number
  messages: number
  tokens: number
  activeDays: number
  peakHour: number | null
  models: { model: string; tokens: number }[]
}

export type Stats = {
  generatedAt: number
  ranges: Record<RangeKey, Range>
  heatmap: { weeks: number; levels: number[] }
}

export type RangeKey = 'all' | '30d' | '7d'

// Moby-Dick in tokens: about 206,000 words
export const MOBY_DICK_TOKENS = 267_000

export const count = (n: number) => n.toLocaleString('en-US')

// One decimal under 100 of a unit (`16.2B`, `18.0B`), none above (`950M`)
export function tokens(n: number): string {
  for (const [size, unit] of [[1e9, 'B'], [1e6, 'M'], [1e3, 'K']] as const) {
    if (n >= size) return (n / size).toFixed(n / size < 100 ? 1 : 0) + unit
  }
  return String(n)
}

export function hour(h: number | null): string {
  if (h === null) return 'none yet'
  const twelve = h % 12 === 0 ? 12 : h % 12
  return `${twelve} ${h < 12 ? 'AM' : 'PM'}`
}

// `claude-opus-5-5` is Opus 5.5, `claude-haiku-4-5-20251001` is Haiku 4.5
export function modelName(id: string): string {
  const parts = id.replace(/^claude-/, '').replace(/-\d{8}$/, '').split('-')
  const family = parts.filter((p) => !/^\d+$/.test(p)).map((p) => p[0]?.toUpperCase() + p.slice(1)).join(' ')
  const version = parts.filter((p) => /^\d+$/.test(p)).join('.')
  return [family, version].filter(Boolean).join(' ') || id
}

export function mobyDick(n: number): string | undefined {
  const times = Math.round(n / MOBY_DICK_TOKENS)
  return times >= 2 ? `You've used ~${times}× more tokens than Moby-Dick.` : undefined
}
