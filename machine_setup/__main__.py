#!/usr/bin/env python3
"""
This script installs software and applies configuration that I want in any of my Manjaro computers (machines).

"Computer" sounds weird here, even though it would be an accurate name :)
So I prefer to use "machine" ¯\_(ツ)_/¯
"""

from functools import partial
import logging
import os
from pathlib import Path
import platform
import re
import socket
import subprocess

import machine_setup
from machine_setup import shell

# Colors taken from "colorama". I don't want to depend on it, though.
# I'll be using a color, so I can easily see my log message by glancing at the output
_BACKGROUND_GREEN = '\x1b[42m'
_BACKGROUND_RESET = '\x1b[49m'

logging.basicConfig(
    level=logging.INFO,
    format=f'{_BACKGROUND_GREEN}--- %(asctime)s{_BACKGROUND_RESET} | %(levelname)s | %(message)s',
    datefmt='%Y-%d-%m %H:%M:%S',
)

log = logging.getLogger(__name__)


def main():
    log.info('Starting upgrade system...')

    sync_packages()
    install_oh_my_zsh()
    setup_file_links()
    setup_tmux_plugins()
    setup_neovim()
    ensure_ntp()
    set_zsh_as_shell()
    set_qt_theme()
    enable_services()
    setup_crontab()
    describe_manual_steps()

    log.info('All done.')


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
        shell.run_cmd('flatpak update')

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
        'https://download.spotify.com/debian/pubkey_5E3C45D7B312C643.gpg',
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


def _clone_or_update_git_repo(repo_url: str, clone_location: Path):
    if clone_location.exists():
        log.info('Updating Git repo: %s', clone_location)
        shell.run_cmd('git pull', work_directory=clone_location)
    else:
        log.info('Pulling Git repo %s into %s', repo_url, clone_location)
        clone_location.parent.mkdir(parents=True, exist_ok=True)
        shell.run_cmd(f'git clone {repo_url} {clone_location}')


def install_oh_my_zsh():
    oh_my_zsh_path = Path('~/.oh-my-zsh').expanduser()
    _clone_or_update_git_repo('https://github.com/ohmyzsh/ohmyzsh.git', oh_my_zsh_path)


def setup_file_links():
    machine_setup.config_links.setup_all_links()


def setup_tmux_plugins():
    tmux_plugins = ['tpm', 'tmux-yank']
    tmux_plugins_dir = Path('~/.tmux/plugins').expanduser()

    for plugin in tmux_plugins:
        plugin_location = tmux_plugins_dir / plugin
        _clone_or_update_git_repo(f'https://github.com/tmux-plugins/{plugin}', plugin_location)


def setup_neovim():
    neovim_virtualenv_path = Path('~/.virtualenvs/neovim').expanduser()
    if not neovim_virtualenv_path.exists():
        log.info('Creating a virtualenv for NeoVim Python integration...')
        shell.run_cmd(f'python3 -m venv {neovim_virtualenv_path}')
        shell.run_cmd(f'{neovim_virtualenv_path}/bin/pip install pynvim')
    else:
        log.info('Updating NeoVim Python integration virtualenv...')
        shell.run_cmd(f'{neovim_virtualenv_path}/bin/pip install --upgrade pynvim')

    vim_color_scheme_file = Path('~/.vim/colors/darcula.vim').expanduser()
    if not vim_color_scheme_file.exists():
        log.info('Pulling the colorsheme file for NeoVim...')
        vim_color_scheme_file.parent.mkdir(parents=True, exist_ok=True)
        color_scheme_url = 'https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim'
        shell.run_cmd(f'wget -O {vim_color_scheme_file} {color_scheme_url}')

    log.info('Synchronizing NeoVim plugins with vim-plug...')
    shell.run_cmd('nvim +PlugUpgrade +PlugClean +PlugUpdate +qall')

    regular_vim_binary = Path('/usr/bin/vim')
    if not regular_vim_binary.exists():
        log.info('Setting up link to NeoVim at %s', regular_vim_binary)
        shell.run_cmd(f'sudo ln -s /usr/bin/nvim {regular_vim_binary}')


def ensure_ntp():
    log.info('Ensuring time is synced with NTP.')
    shell.run_cmd('sudo timedatectl set-ntp true')


def set_zsh_as_shell():
    if not os.environ['SHELL'].endswith('/zsh'):
        log.info('Setting up ZSH as the default shell...')
        # TODO this messes up the script's output. Fix it.
        shell.run_cmd('chsh -s /usr/bin/zsh')


def set_qt_theme():
    if socket.gethostname() in ['ognisko']:
        # non-GUI machines don't have QT, so there's no need for settings
        return
    theme_config = Path('~/.config/qt5ct/qt5ct.conf').expanduser()
    config_contents = theme_config.read_text()

    expected_theme_line = 'style=kvantum-dark'

    if re.findall(f'^{expected_theme_line}', config_contents, flags=re.MULTILINE):
        return

    log.info('Setting theme for QT in %s', theme_config)
    new_config_contents = re.sub('^style=.*', expected_theme_line, config_contents, flags=re.MULTILINE)
    theme_config.write_text(new_config_contents)


def enable_services():
    log.info('Making sure certain services are enabled, running, and usable...')

    # No working docker on ARM? Something errors out if I try to enable Docker...
    if not _is_arm_cpu():
        shell.run_cmd('sudo systemctl enable --now docker')
        subprocess.run('sudo usermod -a -G docker $(whoami)', shell=True, check=True)

    # needed so that yubico-authenticator can talk with the yubikey
    shell.run_cmd('sudo systemctl enable --now pcscd')

    shell.run_cmd('sudo systemctl enable --now syncthing@butla')

    # so that the hosts get DNS entries like <hostname>.local in the local subnet
    shell.run_cmd('sudo systemctl enable --now avahi-daemon.service')



def setup_crontab():
    log.info('Ensuring periodic operations with cron and anacron.')

    users_anacron_spool_dir = Path('~/.local/var/spool/anacron').expanduser()
    users_anacron_spool_dir.mkdir(parents=True, exist_ok=True)

    crontab_contents = f"""
# We'll run anacron through cron. Check out https://serverfault.com/a/172994/499078
@hourly anacron -t ${{HOME}}/.local/etc/anacrontab -S {users_anacron_spool_dir}

# first day of the month
* * 1 * * ${{HOME}}/bin/new_accounting_month
"""
    subprocess.run(
        ['crontab', '-'],
        input=crontab_contents,
        text=True,
        check=True,
    )


# TODO move the below to docs, mention checking that out, separate ones for XFCE
def describe_manual_steps():
    text = """There are some steps you need to do manually after an initial setup:
- Syncthing:
  - http://localhost:8384
  - "Actions" / Show ID
  - share documents (at ~/Documents)
  - set up GUI creds
- add id_rsa to ~/.ssh
- Brave: enable sync (everything but passwords and open tabs)
- Signal: sync with phone
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: set it up - go to https://www.exodus.com/download/, restore the wallet
- qbittorrent: enable search plugin -> View/search engine/search plugins, and configure it
- set up ~/.credentials/borg_key from KeePass
- XFCE:
  - clock widget: set time format to %Y-%m-%d %H:%M:%S
  - remove XFCE workspace switcher and set up favourites menu
  - restart so that XFCE configuration loads
  - battery level widget
  - dark theme for the login screen
"""
    log.info(text)


def _is_arm_cpu():
    # This will work for the ognisko, which is an RPI4,
    # but can be expanded in the future.
    return platform.machine() == 'aarch64'


if __name__ == '__main__':
    main()


# notes for the future (maybe):
# - removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)
# - removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u pylint: disable=line-too-long
# - XFCE shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - gthumb - the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)
# - timeshift emits errors on package updates on BTRFS
#   https://forum.manjaro.org/t/btrfs-updating-leads-to-e-error-cant-list-qgroups-quotas-not-enabled/110375/8?u=butla

# TODOs
# - setup Manjaro on Gnome (detect if we have gnome running)
#   - dconf: keybindings, normal scroll direction (check if all of this can be safely set on XFCE)
#     - https://askubuntu.com/questions/597395/how-to-set-custom-keyboard-shortcuts-from-terminal
#     - https://unix.stackexchange.com/questions/323160/gnome3-adding-keyboard-custom-shortcuts-using-dconf-without-need-of-logging
#       - maximize window: super+up
#       - hide window: super+down
#       - move window: super+m
#       - zoom in / zoom out -> super and = and -
#       - custom: brave, alacritty + tmux, keepassxc, gnome-calculator
#   - gnome extensions installer https://github.com/brunelli/gnome-shell-extension-installer
#   - audio switcher
#   - delete trash and temp data after 30 days
#   - battery show percentage
#   - gsettings set org.gnome.desktop.peripherals.mouse natural-scroll false
#   - gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll false
#   - /org/gnome/desktop/wm/keybindings/close = alt+f4
#   - accessibility: zoom: on, magnification: 1.00
#   - keybindings:
#      - sleep
#      - hide all normal windows: super+d
#      - super+f for file explorer (nautilus)
#   - pix set config value: dconf -> /org/x/pix/browser/sort-type -> file::name
#   - dropbox trey icon: https://superuser.com/questions/1037769/dropbox-system-tray-icon-missing-not-working
# - Rename "configs" to "files_to_link"
#   dedicated dir: files_to_link|files_to_copy/{gnome, xfce, common}.
#   files_to_copy from current "manually_linked". Set them up with root.
# - link setup DE detection needs to work over SSH
# - don't use `sudo pamac`
#   - use pacman for installing regular packages
#   - sync AUR packages with Git to a directory (~/.cache/aur_packages)
#   - install AUR package dependencies (gather them from packages) with "sudo pacman -S --asdeps <packages>"
#   - build as regular user: `makepkg`
#   - install with `sudo pacman -U <package file>`
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
# - KeyboardInterrupt handling.
# - setup syncthing shares between hosts automatically?
# - touchpad turning off on bp - something about sleeping USB that I fixed on bl?
# - touchpad taps as clicks
# - replacement to pix that doesn't glitch when going through photo videos
# - run this as sudo, impersonating the user where it's necessary; upgrade script runs python with sudo.
# - make package update faster: can we skip pamac scan for updates? Can that be done periodically in the background?
# - All commands without confirmation. Get logs for everything. Async status display of all.
#   Have a graph of tasks? (check if preconditions for working are met - mark dependencies)
#   Do everything possible in parallel.
# - open any image / copy to clipboard with FZF.
#   Or better - bemenu, with meta+m (for media) (maybe upper case, lower is move)
#   check "grafika" and whatever photo folders are available
# - On failed steps ask whether to restart or skip them. Or maybe cancel the whole run.
# - (maybe needed) automatically fix pipx installs and virtualenvs after Manjaro switches to a higher Python version.
#   Currently, they're all getting broken.
#   My current process is recreating all virtualenvs and all pipx installs.
#   ~/.local/pipx/ might need to get deleted as well.
# - a single widget with reboot/poweroff/suspend options for Gnome (like in XFCE), opened with a hotkey
# - GRUB setup for machines (/etc/grub.d/40_custom, other necessary ones)
#   https://wiki.archlinux.org/title/GRUB#Custom_grub.cfg
