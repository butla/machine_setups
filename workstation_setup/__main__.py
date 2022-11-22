#!/usr/bin/env python3
"""
This script installs software and applies configurations that I want in my Manjaro workstations.
"""

from functools import partial
import logging
import os
from pathlib import Path
import platform
import re
import socket
import subprocess

import workstation_setup
from workstation_setup import shell

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
    ensure_configs_and_scripts()
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
    log.info('Making sure pamac can install from AUR...')
    # uncommenting some lines
    # TODO add a "replace line in file" function
    shell.run_cmd(r"sudo sed -i -E 's|^.*EnableAUR|EnableAUR|' /etc/pamac.conf")
    shell.run_cmd(r"sudo sed -i -E 's|^.*CheckAURUpdates|CheckAURUpdates|' /etc/pamac.conf")

    log.info('Updating the package index and packages...')
    shell.run_cmd('sudo pamac upgrade --no-confirm')
    if shell.check_command_exists('flatpak'):
        log.info('Updating flatpak packages...')
        shell.run_cmd('flatpak update')

    log.info('Installing the necessary packages...')
    packages_string = ' '.join(workstation_setup.packages.get_packages_for_host())

    _add_package_keys()
    shell.run_cmd(f'sudo pamac install --no-confirm {packages_string}')

    log.info('Removing unused packages...')
    shell.run_cmd('sudo pamac remove --orphans --no-confirm', allow_fail=True)


def _add_package_keys():
    run_key_cmd = partial(subprocess.run, shell=True, check=True)
    keys_from_web = [
        'https://download.spotify.com/debian/pubkey_5E3C45D7B312C643.gpg',
    ]
    for key_url in keys_from_web:
        run_key_cmd(f'curl -sS {key_url} | sudo gpg --import -')

    # TODO this key should be only added for hosts that install Dropbox
    gpg_keys = [
        # dropbox
        '1C61A2656FB57B7E4DE0F4C1FC918B335044912E',
    ]
    for key in gpg_keys:
        run_key_cmd(f'sudo gpg --recv-keys {key}')

    # TODO tor-browser upgrade is causing PGP signature errors when run with
    # sudo pamac install tor-browser
    run_key_cmd('sudo gpg --auto-key-locate nodefault,wkd --locate-keys torbrowser@torproject.org')


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


def ensure_configs_and_scripts():
    workstation_setup.config_links.setup_all_links()


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

    # We'll run anacron through cron. Check out https://serverfault.com/a/172994/499078
    crontab_contents = f'@hourly anacron -t ${{HOME}}/.local/etc/anacrontab -S {users_anacron_spool_dir}\n'
    subprocess.run(
        ['crontab', '-'],
        input=crontab_contents,
        text=True,
        check=True,
    )


def describe_manual_steps():
    text = """There are some steps you need to do manually after an initial setup:
- Syncthing: "Actions" / Show ID; share secrets and documents (at ~/Documents); set up GUI creds
- add id_rsa to ~/.ssh
- KeePassXC: secret's service integration needs to be enabled manually
- Brave: enable sync (for everything); has to be done when KeePassXC secret's service integration is running
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: set it up - go to https://www.exodus.com/download/, restore the wallet
- Signal: sync with phone
- qbittorrent: enable search plugin -> View/search engine/search plugins, and configure it
- set up ~/.credentials/borg_key from KeePass
- pix: set sorting by filename in "view/sort by"
- clock widget: set time format to %Y-%m-%d %H:%M:%S
- remove XFCE workspace switcher and set up favourites menu
- restart so that XFCE configuration loads
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
# - shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - gthumb - the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)

# TODOs
# - install spotify on bp
# - XFCE: dark theme for the login widget?
# - touchpad taps as clicks
# - sort out the secret's service one way or the other
#   (maybe sharing the keepass DB that's used by Brave on different machines causes issues?):
#   - make gnome keyring run as secrets service keyring
#     https://itnext.io/linux-gnome-keyring-setup-as-freedesktop-secretservice-99521a20e9c4
#     (it looks to be running, really. And brave is creating "Brave safe storage",
#     visible with seahorse in the "login" under "passwords")
#   - disable gnomekeyring
#     https://www.chucknemeth.com/linux/security/keyring/keepassxc-keyring
# - run this as sudo, impersonating the user where it's necessary; upgrade script added for root
# - All commands without confirmation. Get logs for everything. Async status display of all.
#   Have a graph of tasks? (check if preconditions for working are met - mark dependencies)
#   Do everything possible in parallel.
# - open any image / copy to clipboard with FZF.
#   Or better - bemenu, with meta+m (for media) (maybe upper case, lower is move)
#   check "grafika" and whatever photo folders are available
# - setup python tools with pipx packages (also update them?):
#   - ocrmypdf
#   - ptpython (nice python interactive shell), with sympy and others (through pipx inject)
#   - pgcli (nice Postgres CLI client)
#   - litecli (nice SQLite CLI client)
#   - isort
#   - subliminal
# - On failed steps ask whether to restart or skip them. Or maybe cancel the whole run.
# - (maybe needed) automatically fix pipx installs and virtualenvs after Manjaro switches to a higher Python version.
#   Currently, they're all getting broken.
#   My current process is recreating all virtualenvs and all pipx installs.
#   ~/.local/pipx/ might need to get deleted as well.
# - Alternative packages different hosts:
#   - bl: matebook-applet (AUR), for enabling/disabling fn-lock. It's not working right now
# - GRUB setup for machines (/etc/grub.d/40_custom, other necessary ones)
#   https://wiki.archlinux.org/title/GRUB#Custom_grub.cfg
