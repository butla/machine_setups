import functools
import logging
from pathlib import Path
import re
import shlex
import subprocess
import sys
from typing import Union

from machine_setup import constants

log = logging.getLogger(__name__)


@functools.cache
def home_path() -> Path:
    return Path(f"/home/{constants.USER}")


def run_cmd(
    command: str,
    work_directory: str = ".",
    allow_fail: bool = False,
    as_root: bool = False,
) -> subprocess.CompletedProcess:
    """
    Args:
        as_root: the script assumes running as root, so specifying this parameter to False will add sudo as the regular
            user.
    """
    parsed_command = shlex.split(command)
    if not as_root:
        parsed_command = shlex.split(f"sudo -u {constants.USER}") + parsed_command

    result = subprocess.run(
        parsed_command,
        check=False,
        cwd=work_directory,
        stdout=None,
        stderr=None,
    )

    command_failed = result.returncode != 0
    if not allow_fail and command_failed:
        message = (
            f"Command: '{parsed_command}' failed with status {result.returncode}.\n"
        )
        log.error(message)
        raise Exception(message)

    return result


def check_command_exists(command: str) -> str:
    return (
        subprocess.run(
            f"command -v {command}",
            shell=True,
            stdout=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def replace_in_file(match: str, replacement: str, file: str):
    run_cmd(f"sed -i -E 's|{match}|{replacement}|' {file}", as_root=True)


def ensure_file_line(
    path: Union[str, Path], line_matcher: str, line_content: str, as_root: bool = False
):
    """Ensures a given line exists in the file.
    If the file doesn't exist it'll be created.

    Args:
        line_matcher: regex used to match the line that'll be set.
            If it doesn't match anything, the line will be added at the end of the file.
        as_root: the script assumes running as root, so specifying this parameter to False will add sudo as the regular
            user.
    """
    # TODO!!!!
    # Also replace usages
    path = Path(path)
    change_message = f"File {path} - ensured line {line_content}"

    if not path.exists():
        ensure_directory(path.parent)
        run_cmd(f"touch {path}")
        path.write_text(line_content)
        log.info(change_message)
        return

    file_contents = path.read_text()

    any_lines_match = bool(re.findall(line_matcher, file_contents, flags=re.M))
    if not any_lines_match:
        with path.open(mode="a") as file_handle:
            file_handle.write(line_content + "\n")
        log.info(change_message)
        return

    contents_after_change = re.sub(
        line_matcher, line_content, file_contents, flags=re.M
    )

    if file_contents == contents_after_change:
        log.info(f"File {path} already has line: {line_content}")
    else:
        path.write_text(contents_after_change)
        log.info(change_message)


def ensure_file_contents(path: Union[str, Path], contents: str):
    path = Path(path)

    if path.exists() and path.read_text() == contents:
        return

    log.info(f"Ensuring file {path} is set up.")
    ensure_directory(path.parent)
    path.write_text(contents)


def ensure_directory(path: Path):
    # Using run_cmd to ensure these get created as the regular user and not root, which is running this script.
    run_cmd(f"mkdir -p {path}")


def clone_or_update_git_repo(repo_url: str, clone_location: Path):
    if clone_location.exists():
        log.info("Updating Git repo: %s", clone_location)
        run_cmd("git pull", work_directory=clone_location)
    else:
        log.info("Pulling Git repo %s into %s", repo_url, clone_location)
        ensure_directory(clone_location.parent)
        run_cmd(f"git clone {repo_url} {clone_location}")
