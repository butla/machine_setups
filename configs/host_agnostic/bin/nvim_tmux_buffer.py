#!/usr/bin/env python3
"""AI-generated with brief review.

Check or reload files in the neovim instances that run in tmux session 0.

`check` exits with code 1 if a neovim instance has unsaved changes in one of the files
(or does not reply). `edit` reloads the files with `:edit` in the instances where they have no unsaved changes.

Usage: nvim_tmux_buffer.py {check,edit} <file>...
"""

import argparse
import json
import os
import subprocess
import sys

TMUX_SESSION = "0"
# Runs in neovim: for the buffer of the file `_A[1]`, `_A[2] == "edit"` reloads it. Returns the buffer state.
BUFFER_LUA = """(function()
for _, b in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_get_name(b) == _A[1] then
    if vim.bo[b].modified then return "modified" end
    if _A[2] == "edit" then vim.api.nvim_buf_call(b, function() vim.cmd("edit") end) end
    return "clean"
  end
end
return "not open"
end)()"""


def nvim_sockets() -> list[str]:
    """Return the RPC sockets of the neovim processes that run in the panes of the tmux session."""
    panes = subprocess.run(
        ["tmux", "list-panes", "-s", "-t", f"={TMUX_SESSION}", "-F", "#{pane_pid}"],
        check=False,
        capture_output=True,
        text=True,
    )
    pids = set(panes.stdout.split())
    children: dict[str, list[str]] = {}
    ps = subprocess.run(["ps", "-e", "-o", "pid=,ppid="], check=True, capture_output=True, text=True)
    for line in ps.stdout.splitlines():
        pid, ppid = line.split()
        children.setdefault(ppid, []).append(pid)
    to_visit = list(pids)
    while to_visit:
        for child in children.get(to_visit.pop(), []):
            pids.add(child)
            to_visit.append(child)
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    return [s for pid in sorted(pids) if os.path.exists(s := f"{runtime_dir}/nvim.{pid}.0")]


def buffer_states(command: str, paths: list[str]) -> list[tuple[str, str]]:
    """Run the command on the buffers of the files in all instances. Return (file, state) pairs."""
    states = []
    for socket in nvim_sockets():
        for path in paths:
            expression = f"luaeval({json.dumps(BUFFER_LUA)}, [{json.dumps(path)}, {json.dumps(command)}])"
            result = subprocess.run(
                ["nvim", "--server", socket, "--remote-expr", expression], check=False, capture_output=True, text=True
            )
            states.append((path, result.stdout.strip() or f"no reply: {result.stderr.strip()}"))
    return states


def all_clean(paths: list[str]) -> bool:
    return all(state in ("clean", "not open") for _, state in buffer_states("check", paths))


def reload(paths: list[str]) -> int:
    """Reload the files in neovim. Return the number of reloaded buffers."""
    return sum(state == "clean" for _, state in buffer_states("edit", paths))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["check", "edit"])
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    paths = [os.path.abspath(p) for p in args.paths]
    if args.command == "edit":
        print(f"Reloaded {reload(paths)} neovim buffers.")
    elif not all_clean(paths):
        sys.exit("A neovim instance in tmux has unsaved changes in the files (or did not reply).")


if __name__ == "__main__":
    main()
