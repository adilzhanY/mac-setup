// The pills' colors, shared by the hooks module and the pill's drawing.

// The model's name: Clawd's orange
export const MODEL_COLOR = '#d77757'

// An effort level's color, or two colors its letters shimmer between
export const EFFORT_COLORS: Record<string, string | [string, string]> = {
  low: '#8fb4ff',
  medium: '#b8c4e0',
  high: ['#ffffff', '#8e9ab0'],
  xhigh: '#ffb27a',
  max: ['#e2d0ff', '#9a6cff'],
}

// One color for a level, the first of a shimmering pair
export function effortColor(level: string): string {
  const color = EFFORT_COLORS[level]
  return Array.isArray(color) ? color[0] : (color ?? 'text')
}
