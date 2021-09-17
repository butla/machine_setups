#!/usr/bin/env python3
"""
This script installs software and applies configurations that I want in my Manjaro workstations.
"""

import logging
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path

from . import packages


# colors taken from "colorama". I don't want to depend on it, though
_BACKGROUND_GREEN = '\x1b[42m'
_BACKGROUND_RESET = '\x1b[49m'
# using a color, so I can easily see my log message by glancing at the output
logging.basicConfig(
    level=logging.INFO,
    format=f'{_BACKGROUND_GREEN}--- %(asctime)s{_BACKGROUND_RESET} | %(levelname)s | %(message)s',
    datefmt='%Y-%d-%m %H:%M:%S',
)

log = logging.getLogger(__name__)


def main():
    upgrade_packages()
    install_standard_packages()
    install_aur_packages()
    install_oh_my_zsh()
    setup_tmux_plugins()
    setup_neovim()
    ensure_ntp()
    set_zsh_as_shell()
    ensure_configs_and_scripts()
    set_qt_theme()
    enable_services()
    describe_manual_steps()

    log.info('All done.')


def run_cmd(command: str, work_directory='.'):
    subprocess.run(shlex.split(command), check=True, cwd=work_directory)


def get_cmd_output(command: str):
    return subprocess.check_output(shlex.split(command))


def upgrade_packages():
    log.info('Updating the package index and packages...')
    run_cmd('sudo pacman -Syu --noconfirm')


def install_standard_packages():
    log.info('Installing the necessary packages...')
    packages_string = ' '.join(packages.PACMAN_PACKAGES)
    run_cmd(f'sudo pacman -S --needed --noconfirm {packages_string}')


def install_aur_packages():
    # yay doesn't have a method for skipping the installation of packages that are already installed,
    # so I have to implement that myself.
    # https://github.com/Jguer/yay/issues/1552
    installed_packages_output = subprocess.check_output('pacman -Q'.split())
    installed_packages = {line.split()[0].decode() for line in installed_packages_output.splitlines()}

    aur_packages_to_install = packages.AUR_PACKAGES - installed_packages

    if not aur_packages_to_install:
        log.info('No AUR packages to install.')
        return

    log.info('Installing the necessary AUR packages...')
    packages_string = ' '.join(aur_packages_to_install)
    run_cmd(f'yay -S --noconfirm {packages_string}')


def install_oh_my_zsh():
    oh_my_zsh_path = Path('~/.oh-my-zsh').expanduser()
    if oh_my_zsh_path.exists():
        return

    log.info('Installing oh-my-zsh into %s', oh_my_zsh_path)
    run_cmd(f'git clone https://github.com/ohmyzsh/ohmyzsh.git {oh_my_zsh_path}')


def setup_tmux_plugins():
    tmux_plugins = ['tpm', 'tmux-yank']
    tmux_plugins_dir = Path('~/.tmux/plugins').expanduser()

    for plugin in tmux_plugins:
        plugin_location = tmux_plugins_dir / plugin
        if not plugin_location.exists():
            tmux_plugins_dir.mkdir(parents=True, exist_ok=True)
            log.info('Pulling Tmux plugin: %s', plugin)
            run_cmd(f'git clone https://github.com/tmux-plugins/{plugin} {plugin_location}')


def setup_neovim():
    neovim_virtualenv_path = Path('~/.virtualenvs/neovim').expanduser()
    if not neovim_virtualenv_path.exists():
        log.info('Creating a virtualenv for NeoVim Python integration...')
        run_cmd(f'python3 -m venv {neovim_virtualenv_path}')
        run_cmd(f'{neovim_virtualenv_path}/bin/pip install pynvim')

    vim_color_scheme_file = Path('~/.vim/colors/darcula.vim').expanduser()
    if not vim_color_scheme_file.exists():
        log.info('Pulling the colorsheme file for NeoVim...')
        vim_color_scheme_file.parent.mkdir(parents=True, exist_ok=True)
        color_scheme_url = 'https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim'
        run_cmd(f'wget -O {vim_color_scheme_file} {color_scheme_url}')

    log.info('Synchronizing NeoVim plugins with vim-plug...')
    run_cmd('nvim +PlugClean +PlugInstall +qall')

    regular_vim_binary = Path('/usr/bin/vim')
    if not regular_vim_binary.exists():
        log.info(f'Setting up link to NeoVim at {regular_vim_binary}')
        regular_vim_binary.symlink_to('/usr/bin/nvim')


def ensure_ntp():
    log.info('Ensuring time is synced with NTP.')
    run_cmd('sudo timedatectl set-ntp true')


def set_zsh_as_shell():
    if not os.environ['SHELL'].endswith('/zsh'):
        log.info('Setting up ZSH as the default shell...')
        run_cmd('chsh -s /usr/bin/zsh')


def ensure_configs_and_scripts():
    configs_and_scripts_path = Path('~/development/configs_and_scripts').expanduser()
    if not configs_and_scripts_path.exists():
        log.info(f'Pulling configs_and_scripts repo into {configs_and_scripts_path}')
        configs_and_scripts_path.parent.mkdir(parents=True, exist_ok=True)
        # recursing into submodules for private configs
        run_cmd(
            f'git clone git@github.com:butla/configs_and_scripts.git {configs_and_scripts_path} --recurse-submodules'
        )

    log.info(f'Applying configs from {configs_and_scripts_path}...')
    run_cmd('make install_configs', work_directory=configs_and_scripts_path)


def set_qt_theme():
    theme_config = Path('~/.config/qt5ct/qt5ct.conf').expanduser()
    config_contents = theme_config.read_text()

    expected_theme_line = 'style=kvantum-dark'

    if re.findall(f'^{expected_theme_line}', config_contents, flags=re.MULTILINE):
        return

    log.info(f'Setting theme for QT in {theme_config}')
    new_config_contents = re.sub('^style=.*', expected_theme_line, config_contents, flags=re.MULTILINE)
    theme_config.write_text(new_config_contents)


def enable_services():
    log.info('Making sure certain services are enabled, running, and usable...')

    run_cmd('sudo systemctl enable --now docker')
    subprocess.run('sudo usermod -a -G docker $(whoami)', shell=True, check=True)

    # for yubikey
    run_cmd('sudo systemctl enable --now pcscd')


def describe_manual_steps():
    text = """There are some steps you need to do manually
- Brave: enable sync (for everything)
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: set it up - go to https://www.exodus.com/download/, restore the wallet
- Signal: sync with phone
- qbittorrent: enable search plugin -> View/search engine/search plugins, and configure it
- KeePassXC: secret's service integration needs to be enabled manually
- set up ~/.credentials/borg_key from KeePass
- restart so that XFCE configuration loads
- remove XFCE workspace switcher and set up favourites menu
- clock widget: set time format to %Y-%m-%d %H:%M:%S
"""
    log.info(text)


if __name__ == '__main__':
    main()


# notes for the future (maybe):
# - removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)
# - removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u
# - shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - gthumb - the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)

# TODOS
# - upload new version of bootstrap_my_tools
# - pipx packages:
#   - ocrmypdf
# - remove https://github.com/butla/utils. Move stuff from it around
# - compare installed packages on both machines - where is bh taking the awesome fonts from?
