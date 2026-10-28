#!/usr/bin/env python3
"""AI-generated with brief review.

Move the items of the previous work day from the DONE section of todo.md to done.md.

The items of the previous work day are the first group of `- ` lines in the DONE section (until an empty line).
A second group of items is from today, and stays in todo.md.
done.md gets the items under a `## <date>` heading for the previous work day (Monday to Friday),
at the top of the file, or at the end of the section if the heading is already there.

The script changes the files only when no neovim instance in tmux session 0 has unsaved changes in them.
It checks again every minute until there are none. Then it reloads the files in neovim.

Usage: todo_done_move.py <todo.md> <done.md>
"""

import argparse
import datetime
import os
import time

import nvim_tmux_buffer

DONE_HEADER = ["DONE", "===="]
RETRY_SECONDS = 60


def previous_work_day(today: datetime.date) -> datetime.date:
    day = today - datetime.timedelta(days=1)
    while day.weekday() >= 5:
        day -= datetime.timedelta(days=1)
    return day


def take_done_items(todo_lines: list[str]) -> list[str]:
    """Remove the first group of DONE items (and the empty line after it) from the todo lines. Return the group."""
    header = next(i for i in range(len(todo_lines)) if todo_lines[i : i + 2] == DONE_HEADER)
    start = header + 2
    while start < len(todo_lines) and not todo_lines[start].strip():
        start += 1
    if start == len(todo_lines) or not todo_lines[start].startswith("- "):
        return []
    end = start
    while end < len(todo_lines) and todo_lines[end].strip():
        end += 1
    items = todo_lines[start:end]
    del todo_lines[start : end + 1]
    return items


def add_done_items(done_lines: list[str], day: datetime.date, items: list[str]) -> None:
    heading = f"## {day.isoformat()}"
    if heading in done_lines:
        end = done_lines.index(heading) + 1
        while end < len(done_lines) and done_lines[end].strip():
            end += 1
        done_lines[end:end] = items
    else:
        # Line 0 is the title of the file, line 1 is empty.
        done_lines[2:2] = [heading, *items, ""]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("todo")
    parser.add_argument("done")
    args = parser.parse_args()
    paths = [os.path.abspath(args.todo), os.path.abspath(args.done)]

    if not nvim_tmux_buffer.all_clean(paths):
        print(f"Unsaved changes in neovim. Checking again every {RETRY_SECONDS} seconds.", flush=True)
        while not nvim_tmux_buffer.all_clean(paths):
            time.sleep(RETRY_SECONDS)

    with open(args.todo) as file:
        todo_lines = file.read().split("\n")
    items = take_done_items(todo_lines)
    if not items:
        print("No DONE items to move.")
        return
    with open(args.done) as file:
        done_lines = file.read().split("\n")
    day = previous_work_day(datetime.date.today())
    add_done_items(done_lines, day, items)

    # done.md first: if the script stops between the writes, the items are in both files, not in neither.
    with open(args.done, "w") as file:
        file.write("\n".join(done_lines))
    with open(args.todo, "w") as file:
        file.write("\n".join(todo_lines))
    print(f"Moved {len(items)} lines to {day.isoformat()} in {args.done}:")
    print("\n".join(items))
    print(f"Reloaded {nvim_tmux_buffer.reload(paths)} neovim buffers.")


if __name__ == "__main__":
    main()
