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
    ensure_ntp()

    log.info('All done.')

def run_cmd(command: str):
    subprocess.run(shlex.split(command), check=True)


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


if __name__ == '__main__':
    main()


# TODOS
# - neovim needs that python variable defined, so that it works in virtual envs without pynvim?
#   - following ":help python-virtualenv" from vim, there should be a pynvim virtualenv
#        let g:python3_host_prog = '/path/to/py3nvim/bin/python'
# - ZSH as default user shell
# - set up ZSH (.zshrc)
#   - keep powerline with process times and status
#   - co jest potrzebne, żeby zainstalować powerline na huwaweiu?
#   - vim/zshrc config - wyświetlanie trybu VIMa działa z powerlinem. Nie spodziewałem się, że Powerline'owe prompty tak ładnie się chowają jeśli trzeba
# - https://github.com/ohmyzsh/ohmyzsh/issues/449
# - TODO solve python keyring
#     https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u
#     maybe make keepass into the keyring thing?
# - add docker permissions for user? make docker work
# - other python versions from AUR
# - todo separate this code out into functions
# - fork and tweak darcula for better colors with .sh and HTML? compare with benokai, or some popular VS code colors?
# - use `let g:python3_host_prog = 'blablabla'` for working with virtualenvs?
# - zeal for documentation? Is there some config file for it?
# - autostart programs, including signal
# - automounting USB (removable drives and media settings, I didn't find any vulnerabilities in just mounting)
# - try deoplete?
# - pia install
# - check slack channels on the old Ubuntu
# - display a list of things to do manually:
#   - slack - set up the workspaces
#   - log into spotify
#   - log into dropbox
#   - sync signal
#   - set up ~/.credentials/borg_key from KeePass
#   - add qbittorrent search plugin -> View/search engine/search plugins (can I move settings from the other laptop?)
#   - Brave - enable sync for everything
# - pipx packages:
#   - ocrmypdf
# - save launcher menu
# - sudo systemctl enable --now pcscd (for yubikey?)
# - shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - todo install oh my zsh: sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
#     TODO remove ~/.zcompdump after installing oh my zsh
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
# - autostart signal, (maybe slack, and discord?)
# - xfce panel - get rid of workplace switcher?
# - go through TODOs in machine_configs
# - mention manual steps if the respective packages has been installed
# - keepassxc roaming config file kept in git https://github.com/keepassxreboot/keepassxc/issues/2666
# - image viewer solution:
#   - gthumb - solve zoom in problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)
#     - sprawdź ``man gthumb``, może tam jest o pliku konfiguracyjnym
#   - use gwenview but fix video playback to start immediately. How to skip to next if there's a video?
# - remove https://github.com/butla/utils. Move stuff from it around
