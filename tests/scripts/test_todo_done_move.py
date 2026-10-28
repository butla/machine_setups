"""AI-generated with brief review."""

import datetime
from pathlib import Path
import subprocess

SATURDAY = 5
SCRIPT = Path(__file__).parents[2] / "configs/host_agnostic/bin/todo_done_move.py"


def _previous_work_day() -> str:
    # The script uses the local date too.
    day = datetime.date.today() - datetime.timedelta(days=1)  # noqa: DTZ011
    while day.weekday() >= SATURDAY:
        day -= datetime.timedelta(days=1)
    return day.isoformat()


def _run(tmp_path: Path, todo: str, done: str) -> tuple[str, str]:
    todo_path, done_path = tmp_path / "todo.md", tmp_path / "done.md"
    todo_path.write_text(todo)
    done_path.write_text(done)
    subprocess.run([SCRIPT, todo_path, done_path], check=True)  # noqa: S603
    return todo_path.read_text(), done_path.read_text()


def test_moves_first_group_and_keeps_todays_group(tmp_path: Path) -> None:
    yesterday_items = "- review MR\n    - details\n- doc done\n"
    today_items = "- started a new thing\n"
    other_sections = "PULL REQUESTS\n=============\n\nkafka MR\n"
    old_done = "## 2026-10-20\n- old item\n"

    todo, done = _run(
        tmp_path,
        todo=f"Rituals\n\nDONE\n====\n\n{yesterday_items}\n{today_items}\n{other_sections}",
        done=f"# Things done by the day\n\n{old_done}",
    )

    assert todo == f"Rituals\n\nDONE\n====\n\n{today_items}\n{other_sections}"
    assert done == f"# Things done by the day\n\n## {_previous_work_day()}\n{yesterday_items}\n{old_done}"


def test_adds_to_existing_day_section(tmp_path: Path) -> None:
    day_heading = f"## {_previous_work_day()}"
    new_item = "- doc done\n"
    old_items = "- review MR\n"

    todo, done = _run(
        tmp_path,
        todo=f"DONE\n====\n\n{new_item}\nPULL REQUESTS\n",
        done=f"# Things done by the day\n\n{day_heading}\n{old_items}\n## 2026-10-20\n",
    )

    assert todo == "DONE\n====\n\nPULL REQUESTS\n"
    assert done == f"# Things done by the day\n\n{day_heading}\n{old_items}{new_item}\n## 2026-10-20\n"


def test_no_items_changes_nothing(tmp_path: Path) -> None:
    todo_text = "DONE\n====\n\nPULL REQUESTS\n"
    done_text = "# Things done by the day\n\n## 2026-10-20\n- old item\n"

    assert _run(tmp_path, todo=todo_text, done=done_text) == (todo_text, done_text)
