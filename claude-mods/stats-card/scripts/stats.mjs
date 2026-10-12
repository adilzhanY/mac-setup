#!/usr/bin/env node
// Usage stats for the stats card, printed as JSON.
//
// Claude Code keeps a cache of its /stats numbers (~/.claude/stats-cache.json)
// but only refreshes it when /stats runs, and its transcripts are cleaned up
// after a while. So: days up to the cache's date come from the cache, later
// days from the transcripts. Each transcript's summary is kept in
// ~/.cache/claude-stats/files.json by size and mtime, so a run only reads the
// files that changed since the last one.

import { createReadStream, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join } from 'node:path'
import { createInterface } from 'node:readline'

const HOME = homedir()
const PROJECTS = join(HOME, '.claude', 'projects')
const CLAUDE_CACHE = join(HOME, '.claude', 'stats-cache.json')
const OWN_CACHE = join(HOME, '.cache', 'claude-stats', 'files.json')
const SUMMARY_VERSION = 1
// The heatmap: 26 weeks, Monday first
const WEEKS = 26

const localDate = (ms) => {
  const d = new Date(ms)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function transcripts(dir) {
  const out = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) out.push(...transcripts(path))
    else if (entry.name.endsWith('.jsonl')) out.push(path)
  }
  return out
}

// One transcript: its session, when it started, and per day its messages and tokens by model
async function summarize(path) {
  const days = {}
  const seen = new Set()
  let sessionId = null
  let start = null
  let isSidechain = false
  const lines = createInterface({ input: createReadStream(path), crlfDelay: Infinity })
  for await (const line of lines) {
    if (!line.includes('"type":"user"') && !line.includes('"type":"assistant"')) continue
    let o
    try {
      o = JSON.parse(line)
    } catch {
      continue
    }
    if (o.type !== 'user' && o.type !== 'assistant') continue
    const ms = Date.parse(o.timestamp)
    if (Number.isNaN(ms)) continue
    sessionId ??= o.sessionId ?? null
    if (o.isSidechain) isSidechain = true
    if (start === null || ms < start) start = ms
    const day = (days[localDate(ms)] ??= { messages: 0, tokens: {} })
    day.messages += 1
    // A response is written one line per content block, each carrying the whole usage: count it once
    const usage = o.type === 'assistant' ? o.message?.usage : undefined
    const id = o.message?.id ?? o.requestId
    if (usage && o.message?.model && !o.message.model.startsWith('<') && !seen.has(id)) {
      seen.add(id)
      const n = (usage.input_tokens ?? 0) + (usage.output_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0)
      day.tokens[o.message.model] = (day.tokens[o.message.model] ?? 0) + n
    }
  }
  return { sessionId, start, isSidechain, days }
}

function readJson(path, fallback) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch {
    return fallback
  }
}

const cache = readJson(CLAUDE_CACHE, null)
const cutoff = cache?.lastComputedDate ?? '0000-00-00'

// Summarize what changed since the last run
const own = readJson(OWN_CACHE, { version: SUMMARY_VERSION, files: {} })
const previous = own.version === SUMMARY_VERSION ? own.files : {}
// A transcript Claude Code has cleaned up keeps its summary, so its days stay counted
const files = { ...previous }
for (const path of existsSync(PROJECTS) ? transcripts(PROJECTS) : []) {
  const { size, mtimeMs } = statSync(path)
  const hit = previous[path]
  files[path] = hit && hit.size === size && hit.mtimeMs === mtimeMs ? hit : { size, mtimeMs, ...(await summarize(path)) }
}
mkdirSync(dirname(OWN_CACHE), { recursive: true })
writeFileSync(OWN_CACHE, JSON.stringify({ version: SUMMARY_VERSION, files }))

// Days: the cache's up to its date, the transcripts' after it
const days = {}
const dayOf = (date) => (days[date] ??= { messages: 0, sessions: 0, tokens: {}, hours: new Array(24).fill(0) })
for (const a of cache?.dailyActivity ?? []) {
  const d = dayOf(a.date)
  d.messages += a.messageCount ?? 0
  d.sessions += a.sessionCount ?? 0
}
for (const t of cache?.dailyModelTokens ?? []) {
  const d = dayOf(t.date)
  for (const [model, n] of Object.entries(t.tokensByModel ?? {})) d.tokens[model] = (d.tokens[model] ?? 0) + n
}
for (const f of Object.values(files)) {
  for (const [date, day] of Object.entries(f.days)) {
    if (date <= cutoff) continue
    const d = dayOf(date)
    d.messages += day.messages
    for (const [model, n] of Object.entries(day.tokens)) d.tokens[model] = (d.tokens[model] ?? 0) + n
  }
  // A session counts on the day and hour it started; a subagent's transcript is part of its session
  if (f.start !== null && !f.isSidechain && localDate(f.start) > cutoff) {
    const d = dayOf(localDate(f.start))
    d.sessions += 1
    d.hours[new Date(f.start).getHours()] += 1
  }
}

const today = new Date()
today.setHours(0, 0, 0, 0)
const daysAgo = (n) => localDate(today.getTime() - n * 86_400_000)

function range(from) {
  const picked = Object.entries(days).filter(([date]) => date >= from)
  const sum = (f) => picked.reduce((s, [, d]) => s + f(d), 0)
  const byModel = {}
  for (const [, d] of picked) for (const [m, n] of Object.entries(d.tokens)) byModel[m] = (byModel[m] ?? 0) + n
  const hours = new Array(24).fill(0)
  for (const [, d] of picked) d.hours.forEach((n, h) => (hours[h] += n))
  // All time also counts the cache's session start hours
  if (from === '0000-00-00') Object.entries(cache?.hourCounts ?? {}).forEach(([h, n]) => (hours[Number(h)] += n))
  const peak = hours.some((n) => n > 0) ? hours.indexOf(Math.max(...hours)) : null
  const models = Object.entries(byModel)
    .map(([model, tokens]) => ({ model, tokens }))
    .sort((a, b) => b.tokens - a.tokens)
  return {
    sessions: sum((d) => d.sessions),
    messages: sum((d) => d.messages),
    tokens: models.reduce((s, m) => s + m.tokens, 0),
    activeDays: picked.filter(([, d]) => d.messages > 0).length,
    peakHour: peak,
    models,
  }
}

// The heatmap's days, column by column (a week each, Monday at the top), as levels 0 to 4
const monday = new Date(today)
monday.setDate(monday.getDate() - ((monday.getDay() + 6) % 7) - (WEEKS - 1) * 7)
const grid = []
for (let i = 0; i < WEEKS * 7; i++) {
  const date = new Date(monday)
  date.setDate(monday.getDate() + i)
  const key = localDate(date.getTime())
  grid.push(date > today ? null : (days[key]?.messages ?? 0))
}
const active = grid.filter((n) => n).sort((a, b) => a - b)
const quantile = (q) => active[Math.min(active.length - 1, Math.floor(q * active.length))] ?? 0
const steps = [quantile(0.25), quantile(0.5), quantile(0.75)]
const levels = grid.map((n) => (n === null ? -1 : n === 0 ? 0 : 1 + steps.filter((s) => n > s).length))

process.stdout.write(
  JSON.stringify({
    generatedAt: Date.now(),
    ranges: { all: range('0000-00-00'), '30d': range(daysAgo(29)), '7d': range(daysAgo(6)) },
    heatmap: { weeks: WEEKS, levels },
  }),
)
