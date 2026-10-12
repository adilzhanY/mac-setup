#!/usr/bin/env bash
# Claude Code status line, compact:
#   ⚡ | dev/kadr | main* | wt:fix-x | C17% | 6%,0932,2h30 | 11%,Sat1902,6d12
# ⚡ shows only in fast mode. The model and the effort are the model-buttons
# mod's clickable pills under the footer (~/dev/claude-mods/model-buttons).
input=$(cat)

DIM='\033[2m'
RESET='\033[0m'
SEP=" ${DIM}|${RESET} "

j() { printf '%s' "$input" | jq -r "$1"; }

# green <50, yellow 50-79, red >=80
pct_col() {
  p=${1%%.*}
  if [ "$p" -ge 80 ]; then printf '\033[1;31m'
  elif [ "$p" -ge 50 ]; then printf '\033[1;33m'
  else printf '\033[1;32m'; fi
}

# format an epoch: GNU date (Linux) or BSD date (macOS)
fdate() { date -d "@$1" "$2" 2>/dev/null || date -r "$1" "$2"; }

# epoch -> "0950" today, "Sat1902" this week, "Aug1709" beyond
reset_at() {
  r=$1; [ -z "$r" ] && return
  if [ "$(date +%Y%m%d)" = "$(fdate "$r" +%Y%m%d)" ]; then
    fdate "$r" +%H%M
  elif [ $(( r - $(date +%s) )) -lt 604800 ]; then
    fdate "$r" '+%a%H%M'
  else
    fdate "$r" '+%b%d%H'
  fi
}

# epoch -> "6d12", "2h30", "45m"
remaining() {
  r=$1; [ -z "$r" ] && return
  d=$(( r - $(date +%s) )); [ "$d" -lt 0 ] && d=0
  if [ "$d" -ge 86400 ]; then printf '%dd%02d' $(( d / 86400 )) $(( (d % 86400) / 3600 ))
  elif [ "$d" -ge 3600 ]; then printf '%dh%02d' $(( d / 3600 )) $(( (d % 3600) / 60 ))
  else printf '%dm' $(( d / 60 )); fi
}

# path -> last three folders, with "../" when something was cut:
#   ~/dev/myapp/apps             -> dev/myapp/apps
#   ~/dev/myapp/apps/mobile/src  -> ../apps/mobile/src
short_dir() {
  d=$1
  [ -z "$d" ] && return
  case "$d" in "$HOME") printf '~'; return ;; "$HOME"/*) d="~/${d#"$HOME"/}" ;; esac
  [ "$d" = "/" ] && { printf '/'; return; }
  local abs=""
  case "$d" in /*) abs="/" ;; esac
  local IFS='/'
  local parts=($d)
  # a leading "/" leaves an empty first field; "~" is not a folder worth counting
  [ -z "${parts[0]}" ] && parts=("${parts[@]:1}")
  [ "${parts[0]}" = "~" ] && { parts=("${parts[@]:1}"); abs=""; }
  if [ "${#parts[@]}" -le 3 ]; then
    printf '%s%s' "$abs" "${parts[*]}"
  else
    printf '../%s' "${parts[*]: -3}"
  fi
}

out=""
add() { if [ -z "$out" ]; then out="$1"; else out="$out$SEP$1"; fi; }

# --- fast mode ---
[ "$(j '.fast_mode // false')" = "true" ] && add "$(printf '\033[1;33m⚡'"$RESET")"

# --- dir ---
dir=$(short_dir "$(j '.workspace.current_dir // .cwd // ""')")
[ -n "$dir" ] && add "$(printf '\033[38;2;122;162;247m%s'"$RESET" "$dir")"

# --- git branch (+ * when dirty) ---
gitdir=$(j '.workspace.current_dir // .cwd // ""')
if [ -n "$gitdir" ] && branch=$(git -C "$gitdir" rev-parse --abbrev-ref HEAD 2>/dev/null); then
  [ "$branch" = "HEAD" ] && branch=$(git -C "$gitdir" rev-parse --short HEAD 2>/dev/null)
  dirty=""
  [ -n "$(git -C "$gitdir" status --porcelain 2>/dev/null)" ] && dirty="*"
  add "$(printf '\033[38;2;158;206;106m%s%s'"$RESET" "$branch" "$dirty")"
fi

# --- worktree (only outside the main tree) ---
wt=$(j '.worktree.name // .workspace.git_worktree // empty')
[ -n "$wt" ] && add "$(printf '\033[1;38;2;187;154;247mwt:%s'"$RESET" "$wt")"

# --- context ---
ctx=$(j '.context_window.used_percentage // empty')
if [ -n "$ctx" ]; then
  ctx_i=$(printf '%.0f' "$ctx")
  add "$(printf "${DIM}C${RESET}%b%s%%${RESET}" "$(pct_col "$ctx_i")" "$ctx_i")"
fi

# --- rate limits: "9%,0950,2h45" (5h first, then 7d) ---
add_limit() {
  p=$(j ".rate_limits.$1.used_percentage // empty"); [ -z "$p" ] && return
  p_i=$(printf '%.0f' "$p")
  r=$(j ".rate_limits.$1.resets_at // empty")
  seg=$(printf '%b%s%%'"$RESET" "$(pct_col "$p_i")" "$p_i")
  [ -n "$r" ] && seg="$seg$(printf "${DIM},%s,%s${RESET}" "$(reset_at "$r")" "$(remaining "$r")")"
  add "$seg"
}
add_limit five_hour
add_limit seven_day

printf '%b\n' "$out"
