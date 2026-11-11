import contextlib
from pathlib import Path
from typing import TYPE_CHECKING

from machine_setup import constants, shell

if TYPE_CHECKING:
    from collections.abc import Iterator

override_file_contents = f"""
polkit.addRule(function(action, subject) {{
    if (action.id == "org.manjaro.pamac.commit" && subject.isInGroup("{constants.USER}")) {{
        return polkit.Result.YES;
    }}

}})
"""


@contextlib.contextmanager
def override_pamac_password() -> Iterator[None]:
    pamac_file_path = Path("/etc/polkit-1/rules.d/99-pamac-override.rules")
    try:
        shell.ensure_file_contents(path=pamac_file_path, contents=override_file_contents)
        yield
    finally:
        pamac_file_path.unlink()
