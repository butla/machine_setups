set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

" This is needed if you're using virtualenvs (:help python-virtualenv)
let g:python3_host_prog = '~/.virtualenvs/neovim/bin/python'
