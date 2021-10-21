#!/usr/bin/env python3
"""
This script installs software and applies configurations that I want in my Manjaro workstations.
"""

import logging
import os
import re
import shlex
import subprocess
from pathlib import Path

import workstation_setup


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
    upgrade_software()
    install_standard_packages()
    install_aur_packages()
    install_oh_my_zsh()
    ensure_configs_and_scripts()
    setup_tmux_plugins()
    setup_neovim()
    ensure_ntp()
    set_zsh_as_shell()
    set_qt_theme()
    enable_services()
    describe_manual_steps()

    log.info('All done.')


def _run_cmd(command: str, work_directory='.', is_check=False) -> subprocess.CompletedProcess:
    if is_check:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
        check = False
    else:
        stdout, stderr = None, None
        check = True
    return subprocess.run(
        shlex.split(command),
        check=check,
        cwd=work_directory,
        stdout=stdout,
        stderr=stderr,
    )


def _get_cmd_output(command: str) -> str:
    return subprocess.check_output(shlex.split(command)).decode()


def upgrade_software():
    log.info('Updating the package index and packages...')

    yay_is_installed = _run_cmd('which yay', is_check=True).returncode == 0

    if yay_is_installed:
        _run_cmd('yay -Syu')
    else:
        _run_cmd('sudo pacman -Syu')

    if _run_cmd('which flatpak', is_check=True).returncode == 0:
        _run_cmd('flatpak update')

    try:
        unused_packages = _get_cmd_output('pacman -Qdtq').splitlines()
    except subprocess.CalledProcessError:
        unused_packages = None

    if unused_packages:
        log.info('Removing unused packages...')
        _run_cmd(f'sudo pacman -R {" ".join(unused_packages)}')


def install_standard_packages():
    log.info('Installing the necessary packages...')
    packages_string = ' '.join(workstation_setup.packages.PACMAN_PACKAGES)
    _run_cmd(f'sudo pacman -S --needed --noconfirm {packages_string}')


def install_aur_packages():
    # yay doesn't have a method for skipping the installation of packages that are already installed,
    # so I have to implement that myself.
    # https://github.com/Jguer/yay/issues/1552
    installed_packages_output = subprocess.check_output('pacman -Q'.split())
    installed_packages = {line.split()[0].decode() for line in installed_packages_output.splitlines()}

    aur_packages_to_install = workstation_setup.packages.AUR_PACKAGES - installed_packages

    if not aur_packages_to_install:
        log.info('No AUR packages to install.')
        return

    log.info('Installing the necessary AUR packages...')
    packages_string = ' '.join(aur_packages_to_install)
    _run_cmd(f'yay -S --noconfirm {packages_string}')


def _clone_or_update_git_repo(repo_url: str, clone_location: Path):
    if clone_location.exists():
        log.info('Updating Git repo: %s', clone_location)
        _run_cmd('git pull', work_directory=clone_location)
    else:
        log.info('Pulling Git repo %s into %s', repo_url, clone_location)
        clone_location.parent.mkdir(parents=True, exist_ok=True)
        _run_cmd(f'git clone {repo_url} {clone_location}')


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
        _run_cmd(f'python3 -m venv {neovim_virtualenv_path}')
        _run_cmd(f'{neovim_virtualenv_path}/bin/pip install pynvim')
    else:
        log.info('Updating NeoVim Python integration virtualenv...')
        _run_cmd(f'{neovim_virtualenv_path}/bin/pip install --upgrade pynvim')

    vim_color_scheme_file = Path('~/.vim/colors/darcula.vim').expanduser()
    if not vim_color_scheme_file.exists():
        log.info('Pulling the colorsheme file for NeoVim...')
        vim_color_scheme_file.parent.mkdir(parents=True, exist_ok=True)
        color_scheme_url = 'https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim'
        _run_cmd(f'wget -O {vim_color_scheme_file} {color_scheme_url}')

    log.info('Synchronizing NeoVim plugins with vim-plug...')
    _run_cmd('nvim +PlugUpgrade +PlugClean +PlugUpdate +qall')

    regular_vim_binary = Path('/usr/bin/vim')
    if not regular_vim_binary.exists():
        log.info('Setting up link to NeoVim at %s', regular_vim_binary)
        regular_vim_binary.symlink_to('/usr/bin/nvim')


def ensure_ntp():
    log.info('Ensuring time is synced with NTP.')
    _run_cmd('sudo timedatectl set-ntp true')


def set_zsh_as_shell():
    if not os.environ['SHELL'].endswith('/zsh'):
        log.info('Setting up ZSH as the default shell...')
        _run_cmd('chsh -s /usr/bin/zsh')


def set_qt_theme():
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

    _run_cmd('sudo systemctl enable --now docker')
    subprocess.run('sudo usermod -a -G docker $(whoami)', shell=True, check=True)

    # needed so that yubico-authenticator can talk with the yubikey
    _run_cmd('sudo systemctl enable --now pcscd')


def describe_manual_steps():
    text = """There are some steps you need to do manually after an initial setup:
- KeePassXC: secret's service integration needs to be enabled manually
- Brave: enable sync (for everything); has to be done when KeePassXC secret's service integration is running
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: set it up - go to https://www.exodus.com/download/, restore the wallet
- Signal: sync with phone
- qbittorrent: enable search plugin -> View/search engine/search plugins, and configure it
- set up ~/.credentials/borg_key from KeePass
- clock widget: set time format to %Y-%m-%d %H:%M:%S
- restart so that XFCE configuration loads
- remove XFCE workspace switcher and set up favourites menu
"""
    log.info(text)


if __name__ == '__main__':
    main()


# notes for the future (maybe):
# - removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)
# - removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u pylint: disable=line-too-long
# - shortcuts for moving windows between screens:
#     https://github.com/calandoa/movescreen
#     https://github.com/jc00ke/move-to-next-monitor
# - gthumb - the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)

# TODOS
# - setup python tools with pipx packages (also update them?):
#   - ocrmypdf
# - (maybe needed) automatically fix pipx installs after Manjaro switches to a higher Python version.
#   They were getting broken.
# - alternative packages different hosts:
#   - bl: matebook-applet (AUR), for enabling/disabling fn-lock. It's not working right now
