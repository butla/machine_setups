import contextlib
import os
from pathlib import Path

from machine_setup import constants, shell

override_file_contents = f"""
polkit.addRule(function(action, subject) {{
    if (action.id == "org.manjaro.pamac.commit" && subject.isInGroup("{constants.USER}")) {{
        return polkit.Result.YES;
    }}

}})
"""


@contextlib.contextmanager
def override_pamac_password():
    pamac_file_path = "/etc/polkit-1/rules.d/99-pamac-override.rules"
    try:
        shell.ensure_file_contents(
            path=pamac_file_path, contents=override_file_contents
        )
        yield
    finally:
        os.remove(pamac_file_path)
