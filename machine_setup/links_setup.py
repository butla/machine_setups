"""
Setting up links from this repository, to the broader filesystems.
Mainly used to ensure that any manual config changes will be caught by Git.
"""

from dataclasses import dataclass
import logging
import os
from pathlib import Path
import platform
import re
from typing import Iterable, List

from machine_setup import machine_info, shell

BACKUP_SUFFIX = ".bak"

log = logging.getLogger(__name__)


def setup_all_links():
    log.info("Ensuring up-to-date configurations and scripts...")
    set_up_links(
        source_dir=Path("configs/host_agnostic/"),
        target_dir=shell.home_path(),
    )
    current_host = platform.node()
    set_up_links(
        source_dir=Path(f"configs/host_specific/{current_host}/"),
        target_dir=shell.home_path(),
    )

    desktop_env = machine_info.get_desktop_environment()
    if desktop_env:
        set_up_links(
            source_dir=Path(f"configs/desktop_env_specific/{desktop_env}"),
            target_dir=shell.home_path(),
        )

    # TODO make sure the files here are chmod 600
    set_up_links(
        source_dir=Path("configs/configs_private/home/"),
        target_dir=shell.home_path(),
    )


def set_up_links(source_dir: Path, target_dir: Path) -> None:
    source_dir = source_dir.absolute()
    target_dir = target_dir.absolute()

    files_and_dirs_to_link = list(source_dir.glob("**/*"))
    files_to_link = [path for path in files_and_dirs_to_link if _should_set_up_link(path)]
    if not files_to_link:
        return

    links_to_create = _get_links_to_set_up(
        files_to_link=files_to_link,
        files_dir=source_dir,
        links_location=target_dir,
    )

    link_paths = [link.location for link in links_to_create]

    _ensure_parent_dirs(link_paths)
    _remove_broken_links(link_paths)
    _backup_and_remove_existing_targets(link_paths)

    for link_to_create in links_to_create:
        log.info("Creating the link at %s", link_to_create.location)
        # using run_cmd to not create the links as root
        shell.run_cmd(f"ln -s {link_to_create.target} {link_to_create.location}")


def _should_set_up_link(path) -> bool:
    """Given a path in a source directory, says whether a link for it should be created in the target directory."""
    return path.is_file() and path.suffix != ".pyc" and "tests/" not in str(path)


@dataclass
class _LinkToSetUp:
    target: Path
    location: Path


def _get_links_to_set_up(
    files_to_link: List[Path],
    files_dir: Path,
    links_location: Path,
) -> List[_LinkToSetUp]:
    file_path_strings = [str(path) for path in files_to_link]
    link_path_strings = [re.sub(f"^{files_dir}", str(links_location), path) for path in file_path_strings]
    link_paths = [Path(path) for path in link_path_strings]

    initial_links = [
        _LinkToSetUp(target=link_target, location=link_path)
        for link_target, link_path in zip(files_to_link, link_paths)
    ]
    return [link for link in initial_links if not _is_link_set_up(link)]


def _is_link_set_up(link: _LinkToSetUp):
    """Prevents us doing anything if the link is already set up correctly."""
    if link.location.exists() and link.location.is_symlink():
        if link.location.resolve() == link.target.absolute():
            return True
    return False


def _ensure_parent_dirs(paths: Iterable[Path]):
    for path in paths:
        if not path.parent.exists():
            log.info("Creating directory: %s", path.parent)
            shell.ensure_directory(path.parent)


def _backup_and_remove_existing_targets(paths: Iterable[Path]):
    for path in paths:
        if path.exists():
            log.info("Backing up %s", path)
            backup_path = path.with_name(path.name + BACKUP_SUFFIX)
            path.replace(backup_path)


def _remove_broken_links(paths: Iterable[Path]):
    for path in paths:
        if path.is_symlink() and not os.path.exists(os.readlink(path)):
            log.info("Will replace a broken link at %s", path)
            path.unlink()
