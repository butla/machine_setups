import logging
import shlex
import subprocess
import sys

log = logging.getLogger(__name__)


def run_cmd(command: str, work_directory='.', allow_fail=False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        shlex.split(command),
        check=False,
        cwd=work_directory,
        stdout=None,
        stderr=None,
    )

    command_failed = result.returncode != 0
    if not allow_fail and command_failed:
        log.error(f"Command: '{command}' failed with status {result.returncode}.\n")
        sys.exit("ERROR! Shell command failed!")

    return result


def check_command_exists(command: str) -> str:
    return subprocess.run(
        f'command -v {command}',
        shell=True,
        stdout=subprocess.DEVNULL
    ).returncode == 0


def replace_in_file(match: str, replacement: str, file: str):
    run_cmd(f"sudo sed -i -E 's|{match}|{replacement}|' {file}")
