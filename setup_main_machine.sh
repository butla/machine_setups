#!/bin/bash
function log() {
    echo '---' $(date --iso-8601=seconds) '---' $@ '---'
}

log "Updating the package index and packages"
sudo pacman -Syu --noconfirm

log "Installing the necessary packages"
PACKAGES_TO_INSTALL=$(cat packages_to_install.txt | grep -v '#')
sudo pacman -S --noconfirm --needed $PACKAGES_TO_INSTALL

# - name: setup tmux plugins
#   git:
#     repo: https://github.com/tmux-plugins/{{ item }}
#     dest: '{{ ansible_user_dir }}/.tmux/plugins/{{ item }}'
#   with_items:
#     - tpm
#     - tmux-yank
# 
# 
# - name: create the development folder
#   file: path={{ item }} state=directory
#   with_items:
#   - "{{ ansible_user_dir }}/development"
# 
# # TODO is there something built into nvim?
# - name: install vim plugin manager
#   git:
#     repo: https://github.com/VundleVim/Vundle.vim.git
#     dest: "{{ ansible_user_dir }}/.vim/bundle/Vundle.vim"
# 
# - name: download darcula colorsheme for vim
#   get_url:
#     url: https://raw.githubusercontent.com/blueshirts/darcula/master/colors/darcula.vim
#     dest: "{{ ansible_user_dir }}/.vim/colors/darcula.vim"
#     mode: 0644
# 
# # TODO check when this changes
# - name: install vim plugins
#   command: nvim +PluginInstall +qall
# 
# # TODO run this only when plugin install did something, or after a plugin update
# - name: compile and install YouComplete me for Vim
#   command: ./install.py --clang-completer
#   args:
#     chdir: "{{ ansible_user_dir }}/.vim/bundle/YouCompleteMe"

# TODOS
# - install AUR packages
# - set up neovim alias for vim
# - add docker permissions for user? make docker work
# - other python versions from AUR
# - try installing python cryptography, or building some package from source (to check libssl and python-dev)

# Install Pylint globally (pip3 install --user) for checking of Python files outside of
# virtualenvs.
#
# Install yamllint with Python 2 and add the config to ~/.config/yamllint
#
# Get freemind from zip, put it in opt, link in ~/bin
#
# Poetry i jego completions.
#
# installing ptpython so that it's in 3.7 (from deadsnakes) by default
# python3.7 -m pip install --user ptpython

# python packages:
# - twine
# - yamllint
# - ueberzug (normal package)
# - subliminal
# - pudb
# - httpie
# - pgcli
# - virtualenvwrapper
# - ptpython
# - tox
