#!/usr/bin/env python3
"""
This script installs software and applies configuration that I want in any of my Manjaro computers (machines).

"Computer" sounds weird here, even though it would be an accurate name :)
So I prefer to use "machine".
"""

from functools import partial
import logging
from pathlib import Path
import subprocess
import sys
from typing import Callable, List

import machine_setup
from machine_setup import os_configuration, shell

# Colors taken from "colorama". I don't want to depend on it, though.
# I'll be using a color, so I can easily see my log message by glancing at the output
_BACKGROUND_GREEN = '\x1b[42m'
_BACKGROUND_RESET = '\x1b[49m'

logging.basicConfig(
    level=logging.INFO,
    format=f'{_BACKGROUND_GREEN}--- %(asctime)s{_BACKGROUND_RESET} | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)


# TODO use stop_on_errors in run_setup_first_time!
def main(stop_on_errors=False):
    log.info('Starting upgrade system...')

    upgrade_steps: List[Callable] = [
        sync_packages,
        install_oh_my_zsh,
        machine_setup.links_setup.setup_all_links,
        os_configuration.setup_tmux_plugins,
        os_configuration.set_zsh_as_shell,
        os_configuration.set_gsettings,
        os_configuration.enable_services,
        os_configuration.ensure_ntp,
        os_configuration.setup_crontab,
        os_configuration.set_java_version,
        os_configuration.apply_app_specific_config_patches,
        os_configuration.setup_neovim,
        describe_manual_steps,
    ]
    steps_succeeded = True
    for upgrade_step_function in upgrade_steps:
        try:
            upgrade_step_function()
        # we don't want to skip next steps if any step fails, usually
        except Exception:
            log.exception("ERROR! One of the steps has failed!")
            steps_succeeded = False

            if stop_on_errors:
                log.error('Stopping execution of further steps...')
                break

    if steps_succeeded:
        log.info('All done.')
    else:
        # TODO why is this not ending the process with a non-zero code?
        sys.exit('ERROR! Some steps have failed!')


def sync_packages():
    # TODO list the packages getting installed, updated.
    # Pipe the command output somewhere else. Log file.
    # Say "updating packages, log location /var/log/bobr_machine_setup
    log.info('Making sure pamac can install from AUR...')
    # uncommenting some lines
    shell.replace_in_file('^.*EnableAUR', 'EnableAUR', '/etc/pamac.conf')
    shell.replace_in_file('^.*CheckAURUpdates', 'CheckAURUpdates', '/etc/pamac.conf')
    # TODO set the line that disables database signatures in pacman.conf
    # first SigLevel, from [options] section. Can an ini reader get that?
    # Capture group after [options] before next [
    # Or just copy the whole config file.

    log.info('Updating the package index and packages...')
    shell.run_cmd('pamac upgrade --no-confirm')
    if shell.check_command_exists('flatpak'):
        log.info('Updating flatpak packages...')
        shell.run_cmd('flatpak update --assumeyes')

    log.info('Adding GPG keys for some packages...')
    _add_package_keys()

    log.info('Installing the necessary packages...')
    packages_string = ' '.join(machine_setup.packages.get_packages_for_host())
    shell.run_cmd(f'pamac install --no-confirm {packages_string}')

    log.info('Removing unused packages...')
    shell.run_cmd('sudo pamac remove --orphans --no-confirm', allow_fail=True)


def _add_package_keys():
    run_key_cmd = partial(subprocess.run, shell=True, check=True)
    keys_from_web = [
        'https://download.spotify.com/debian/pubkey_7A3A762FAFD4A51F.gpg',
    ]
    for key_url in keys_from_web:
        run_key_cmd(f'curl -sS {key_url} | gpg --import -')

    # TODO this key should be only added for hosts that install Dropbox
    gpg_keys = [
        # dropbox
        '1C61A2656FB57B7E4DE0F4C1FC918B335044912E',
    ]
    for key in gpg_keys:
        run_key_cmd(f'gpg --recv-keys {key}')

    run_key_cmd('gpg --auto-key-locate nodefault,wkd --locate-keys torbrowser@torproject.org')


def install_oh_my_zsh():
    oh_my_zsh_path = Path('~/.oh-my-zsh').expanduser()
    shell.clone_or_update_git_repo('https://github.com/ohmyzsh/ohmyzsh.git', oh_my_zsh_path)


def describe_manual_steps():
    log.info("Check out docs/initial_setup.md to check the steps you need to do manually "
            "after running the initial setup.")


if __name__ == '__main__':
    main()


# TODOs
# - run this as sudo, without requiring confirmations. Solid logs needed.
#   - impersonate the user where necessary
#   - have a user for `pamac upgrade` with paswordless sudo?
# - add precommit: mypy, black, isort
# - make package update faster: if the last "synchronizing package lists" in /var/log/pacman.log is no older than 8 hours
# - make neovim plugin update not mess up the script's output
# - Rename "configs" to "files_to_link"
#   - dedicated dir: files_to_link|files_to_copy/{gnome, xfce, common}.
#   - Pull "manually_linked" into files_to_copy from current "manually_linked". Set them up with root.
#   - files are copied only when they are different
# - desktop detection needs to work over SSH - use inxi --system?
# - digikam settings sync:
#   - /home/butla/.config/digikamrc
#   - set only some sections/options, create a file if empty (implement ensure_line_in_ini_file)
# - signal settings - allow access to mic and cam / autostart / notifications should only contain the name
# - see TODOs from sync packages
# - setup my GPG secret keys in the keychain and gpg config
# - add the method of getting keys with the packages. Ones with keys should be a dict.
#   There needs to be an intermediate step that wraps the simple string or dict into a Package representation,
#   that's hashable on the name.
# - setup python tools with pipx packages (also update them?):
#   - ocrmypdf
#   - ptpython (nice python interactive shell), with sympy and others (through pipx inject)
#   - pgcli (nice Postgres CLI client)
#   - litecli (nice SQLite CLI client)
#   - isort
#   - subliminal
# - extract code and tests into an "src" directory?
# - qbittorrent settings (~/.config/qBittorrent); settings/behavior/"prevent sleep"
# - KeyboardInterrupt handling.
#   Check if commands get interrupted when exiting with ctrl+c. If I kill the script, pamac should exit as well.
# - setup syncthing shares between hosts automatically?
# - replacement to pix that doesn't glitch/hang for a few seconds when opening a heavy video
# - Graph of tasks. Async status display of all.
#   Have a graph of tasks? (check if preconditions for working are met - mark dependencies)
#   Do everything possible in parallel.
# - open any image / copy to clipboard with FZF.
#   Or better - bemenu, with meta+m (for media) (maybe upper case, lower is move)
#   check "grafika" and whatever photo folders are available
# - On failed steps ask whether to restart or skip them. Or maybe cancel the whole run.
# - font configs in alacritty that switch when a monitor is attached? Have configs for alien, lemur, iiyama (monitor)
