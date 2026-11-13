#!/usr/bin/env bash
# Keeps one marker file per open interactive Claude Code session in ~/.claude/open-sessions/.
# SessionStart writes the marker. SessionEnd removes it only when the user ended the session
# (/exit, Ctrl-D, /clear, /logout). After a crash or a reboot, the markers that are left
# show the sessions to resume with `claude --resume <session_id>` in their `cwd`.
# Headless sessions (`claude -p`, entrypoint `sdk-cli`) end with the same reason as a kill,
# so they are not tracked.
set -euo pipefail

[ "${CLAUDE_CODE_ENTRYPOINT:-}" = cli ] || exit 0

dir="$HOME/.claude/open-sessions"
input=$(cat)
marker="$dir/$(jq -r .session_id <<<"$input").json"

case $(jq -r .hook_event_name <<<"$input") in
  SessionStart)
    window=""
    [ -n "${TMUX:-}" ] && window=$(tmux display-message -p -t "$TMUX_PANE" '#S:#W')
    mkdir -p "$dir"
    jq -c --arg window "$window" --arg started "$(date -Is)" \
      '{session_id, cwd, tmux_window: $window, started: $started}' <<<"$input" >"$marker"
    ;;
  SessionEnd)
    case $(jq -r .reason <<<"$input") in
      prompt_input_exit | clear | logout) rm -f "$marker" ;;
    esac
    ;;
esac
