"""
Ensuring proper configuration is set up for various programs in the host system.
"""

import logging
import os
from pathlib import Path
import re
import subprocess

from machine_setup import machine_info, shell

log = logging.getLogger(__name__)


def set_gsettings():
    """Sets settings with gsettings. These are used by Gnome/GTK apps."""
    log.info('Setting up GTK app settings with GSettings...')
    shell.run_cmd('gsettings set org.x.pix.browser sort-type file::name')

    if machine_info.get_desktop_environment() != 'gnome':
        return

    log.info('Setting up Gnome settings with GSettings...')

    # touchpad scroll
    shell.run_cmd('gsettings set org.gnome.desktop.peripherals.mouse natural-scroll false')
    shell.run_cmd('gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll false')

    # show battery percentage
    shell.run_cmd('gsettings set org.gnome.desktop.interface show-battery-percentage true')

    # desktop zoom
    shell.run_cmd('gsettings set org.gnome.desktop.interface toolkit-accessibility true')
    shell.run_cmd('gsettings set org.gnome.desktop.a11y.applications screen-magnifier-enabled true')
    shell.run_cmd('gsettings set org.gnome.desktop.a11y.magnifier mag-factor 1.0')

    # automatically remove old trash and temp files
    shell.run_cmd('gsettings set org.gnome.desktop.privacy old-files-age 30')
    shell.run_cmd('gsettings set org.gnome.desktop.privacy remove-old-trash-files true')
    shell.run_cmd('gsettings set org.gnome.desktop.privacy remove-old-temp-files true')

    # keybindings
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings maximize "[\'<Super>Up\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings minimize "[\'<Super>Down\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings close "[\'<Alt>F4\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings show-desktop "[\'<Super>d\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings begin-move "[\'<Super>m\']"')
    shell.run_cmd('gsettings set org.gnome.settings-daemon.plugins.media-keys magnifier-zoom-out "[\'<Super>minus\']"')
    shell.run_cmd('gsettings set org.gnome.settings-daemon.plugins.media-keys magnifier-zoom-in "[\'<Super>equal\']"')
    # this makes sure alt-tab doesn't group stuff together
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings switch-windows "[\'<Alt>Tab\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings switch-windows-backward "[\'<Shift><Alt>Tab\']"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings switch-applications "[]"')
    shell.run_cmd('gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward "[]"')

    # clear bindings for switching workspaces, so that they don't conflict with the custom ones
    for index in range(1, 10):
        shell.run_cmd(f'gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-{index} "[]"')

    # Custom keybindings, based on https://askubuntu.com/a/597414
    # Gnome restart is required for these to start working.
    custom_keybindings = [
        ('brave', '<Super>1', 'brave'),
        ('clementine', '<Super>2', 'clementine'),
        ('keepassxc', '<Super>3', 'keepassxc'),
        ('calculator', '<Super>4', 'gnome-calculator'),
        ('terminal with tmux', '<Super>t', 'alacritty --command tmux'),
        ('file explorer', '<Super>f', 'nautilus'),
        ('sleep', '<Shift><Super>l', 'systemctl suspend'),
    ]
    keybinding_entry_paths = [f'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{index}/'
                              for index in range(len(custom_keybindings))]
    # create a number of entries that will be filled with values below
    shell.run_cmd('gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings '
                  f'"{str(keybinding_entry_paths)}"')
    for index, custom_keybinding in enumerate(custom_keybindings):
        set_command_base = ('gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding'
                            ':/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{index}/ '
                            '{field_name} "{value}"')
        for field_name, value in zip(['name', 'binding', 'command'], custom_keybinding):
            shell.run_cmd(set_command_base.format(index=index, field_name=field_name, value=value))


def setup_tmux_plugins():
    log.info('Setting up Tmux pluggins...')

    tmux_plugins = ['tpm', 'tmux-yank']
    tmux_plugins_dir = Path('~/.tmux/plugins').expanduser()

    for plugin in tmux_plugins:
        plugin_location = tmux_plugins_dir / plugin
        shell.clone_or_update_git_repo(f'https://github.com/tmux-plugins/{plugin}', plugin_location)


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
    # UpdateRemotePlugins shouldn't be necessary, because vim-plug is supposed to run it for semshi, but it doesn't.
    # TODO this looks to be messing something up in the output
    shell.run_cmd('nvim +PlugUpgrade +PlugClean +PlugUpdate +UpdateRemotePlugins +qall')

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
    if not machine_info.check_gui_present():
        return

    theme_config = Path('~/.config/qt5ct/qt5ct.conf').expanduser()
    log.info('Setting theme for QT in %s', theme_config)
    config_contents = theme_config.read_text()

    expected_theme_line = 'style=kvantum-dark'

    if re.findall(f'^{expected_theme_line}', config_contents, flags=re.MULTILINE):
        return

    new_config_contents = re.sub('^style=.*', expected_theme_line, config_contents, flags=re.MULTILINE)
    theme_config.write_text(new_config_contents)


def enable_services():
    log.info('Making sure certain services are enabled, running, and usable...')

    # No working docker on ARM? Something errors out if I try to enable Docker...
    if not machine_info.check_is_arm_cpu():
        # TODO looks like this might fail during the run on a clean system
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

    # TODO this doesn't work as expected. If the day is skipped, then the action doesn't happen.
    # It has to be set up with anacrontab with manipulation of the spool file, so that the action is run on first
    # day of the month. Or maybe there's some other way to do it.
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


def set_java_version():
    """
    Has to be done for freeplane:
    https://forum.manjaro.org/t/freeplane-refuse-to-start-after-update/116595/2
    """
    java_version = 'java-17-openjdk'
    log.info(f'Ensuring Java runtime being used is {java_version}')
    shell.run_cmd(f'sudo archlinux-java set {java_version}')
