#!/usr/bin/env python3
import logging
import shlex
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
    setup_tmux_plugins()
    setup_neovim()

    log.info('All done.')

def run_cmd(command: str):
    subprocess.run(shlex.split(command), check=True)


def upgrade_packages():
    log.info('Updating the package index and packages...')
    run_cmd('sudo pacman -Syu --noconfirm')


def install_standard_packages():
    log.info('Installing the necessary packages...')
    packages_string = ' '.join(packages.PACMAN_PACKAGES)
    run_cmd(f'sudo pacman -S --needed {packages_string}')


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

    packages_string = ' '.join(aur_packages_to_install)
    run_cmd(f'yay -S --noconfirm {packages_string}')


def setup_tmux_plugins():
    tmux_plugins = ['tpm', 'tmux-yank']
    tmux_plugins_dir = Path('~/.tmux/plugins').expanduser()

    tmux_plugins_dir.mkdir(parents=True, exist_ok=True)
    for plugin in tmux_plugins:
        plugin_location = tmux_plugins_dir / plugin
        if not plugin_location.exists():
            log.info('Pulling Tmux plugin: %s', plugin)
            run_cmd(f'git clone https://github.com/tmux-plugins/{plugin} {plugin_location}')


def setup_neovim():
    vim_color_scheme_file = Path('~/.vim/colors/darcula.vim').expanduser()
    if not vim_color_scheme_file.exists():
        log.info('Pulling the colorsheme file for NeoVim...')
        vim_color_scheme_file.parent.mkdir(parents=True, exist_ok=True)
        color_scheme_url = 'https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim'
        run_cmd(f'wget -O {vim_color_scheme_file} {color_scheme_url}')

    log.info('Synchronizing NeoVim plugins with vim-plug...')
    run_cmd('nvim +PlugClean +PlugInstall +qall')

if __name__ == '__main__':
    main()


# TODOS
# - commit configs_and_scripts as well, check on the other laptop (remove that neovim venv)
# - https://github.com/ohmyzsh/ohmyzsh/issues/449
# - TODO solve python keyring
#     https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u
#     maybe make keepass into the keyring thing?
# - TODO_arch_setup_todos.txt
# - set up neovim alias for vim
# - add docker permissions for user? make docker work
# - other python versions from AUR
# - todo separate this code out into functions
# - fork and tweak darcula for better colors with .sh and HTML? compare with benokai, or some popular VS code colors?
# - use `let g:python3_host_prog = 'blablabla'` for working with virtualenvs?
# - zeal for documentation? Is there some config file for it?
# - set SSHD config link from manually_linked in configs_and_scripts? Only for bh
#     sudo systemctl enable sshd
#     sudo systemctl start sshd
# - autostart programs, including signal
# - automounting USB (removable drives and media settings, I didn't find any vulnerabilities in just mounting)
# - try deoplete?
# - pia install
