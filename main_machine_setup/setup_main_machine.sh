#!/bin/bash
set -e

function log() {
    echo '---' $(date --iso-8601=seconds) '---' $@ '---'
}


log "Updating the package index and packages"
sudo pacman -Syu --noconfirm

log "Installing the necessary packages"
PACKAGES_TO_INSTALL=$(cat packages_to_install.txt | grep -v '#')
sudo pacman -S --noconfirm --needed $PACKAGES_TO_INSTALL

ALL_INSTALLED_PACKAGES=$(pacman -Q | cut -d " " -f 1 | sort)

# TODO only install packages that aren't installed yet (subtract the installed packages list)
log "Installing the necessary AUR packages"
AUR_PACKAGES=$(cat packages_to_install_from_AUR.txt | grep -v '#' | sort)
# TODO fix!
# post workaround to https://github.com/Jguer/yay/issues/1552
AUR_PACKAGES_TO_INSTALL=$(comm -23 <(echo $AUR_PACKAGES) <(echo $ALL_INSTALLED_PACKAGES))
# yay -S --noconfirm $AUR_PACKAGES_TO_INSTALL


log "Setting up tmux plugins"

TMUX_PLUGINS_DIR=~/.tmux/plugins
TMUX_PLUGINS="tpm tmux-yank"

mkdir -p $TMUX_PLUGINS_DIR

for plugin in $TMUX_PLUGINS; do
    plugin_location=$TMUX_PLUGINS_DIR/${plugin}
    if [ ! -d $plugin_location ]; then
	log pulling Tmux plugin $plugin
	git clone https://github.com/tmux-plugins/${plugin} $plugin_location
    else
	log Tmux plugin $plugin already pulled
    fi
done


VIM_COLOR_SCHEME_FILE=~/.vim/colors/darcula.vim
if [ ! -e $VIM_COLOR_SCHEME_FILE ]; then
    log "Pulling Vim colorsheme file"
    mkdir -p $(dirname $VIM_COLOR_SCHEME_FILE)
    wget -O $VIM_COLOR_SCHEME_FILE https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim
fi


# vim-plug sets up the plugins automatically on running Vim.
# TODO run it manually

# TODO solve python keyring
# https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u
# maybe make keepass into the keyring thing?

# TODOS
# - set up neovim alias for vim
# - add docker permissions for user? make docker work
# - other python versions from AUR
# - try installing python cryptography, or building some package from source (to check libssl and python-dev)
# - fork and tweak darcula for better colors with .sh and HTML? compare with benokai, or some popular VS code colors?
# - use `let g:python3_host_prog = 'blablabla'` for working with virtualenvs?
# - try deoplete?

