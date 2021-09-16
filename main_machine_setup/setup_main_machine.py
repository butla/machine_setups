#!/usr/bin/env python3
import logging
import os
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
        run_cmd(f'git clone git@github.com:butla/configs_and_scripts.git {configs_and_scripts_path}')

    log.info('Applying the configs...')
    run_cmd('make install_configs', work_directory=configs_and_scripts_path)


def describe_manual_steps():
    text = """There are some steps you need to do manually
- Brave: enable sync (for everything)
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: set it up - go to https://www.exodus.com/download/, restore the wallet
- Spotify: log inslack - set up the workspaces
- Signal: sync with phone
- set up ~/.credentials/borg_key from KeePass
- qbittorrent: enable search plugin -> View/search engine/search plugins
- KeePassXC: secret's service integration needs to be enabled manually
"""
    log.info(text)


if __name__ == '__main__':
    main()


# notes for the future (maybe):
# - removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)
# - removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u

# TODOS
# - keepassxc roaming config file kept in git https://github.com/keepassxreboot/keepassxc/issues/2666
# - qbittorent setting into configs_and_scripts?
# - add docker permissions for user? make docker work
# - zeal for documentation? Is there some config file for it?
# - automounting USB (removable drives and media settings, I didn't find any vulnerabilities in just mounting)
# - upload new version of bootstrap_my_tools
# - try deoplete?
# - check slack channels on the old Ubuntu
# - pipx packages:
#   - ocrmypdf
# - save launcher menu
# - sudo systemctl enable --now pcscd (for yubikey?)
# - shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - signal settings

# Docker install on arch:
# pacman -S docker
# systemctl enable docker
# add user to group

# qt5 setting -> kvantum-dark theme (for KDE apps to look properly)
# - change XFCE theme while looking at what a config window is changing with strace, add those config to ``configs_and_scripts`` (blog post out of that)
#   - hide window headings
# - skrypt datee dający mi datę w formacie jaki lubię (i wrzucający do schowka), do zapisków
# - xfce favourites menu
# - clock style
# - xfce panel - get rid of workplace switcher?
# - image viewer solution:
#   - gthumb - solve zoom in problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)
#     - sprawdź ``man gthumb``, może tam jest o pliku konfiguracyjnym
#   - use gwenview but fix video playback to start immediately. How to skip to next if there's a video?
# - remove https://github.com/butla/utils. Move stuff from it around
# - compare installed packages on both machines - where is bh taking the awesome fonts from?
