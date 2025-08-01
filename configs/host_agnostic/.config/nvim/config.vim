set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath

" vim-plug automatic download and setup
if empty(glob('~/.local/share/nvim/site/autoload/plug.vim'))
  silent !curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source ~/.config/nvim/init.vim
endif

call plug#begin(stdpath('data') . '/plugged')

" code completions
Plug 'ycm-core/YouCompleteMe', { 'do': './install.py' }
" async linting and syntax checking
Plug 'dense-analysis/ale'
" text searching
Plug 'mileszs/ack.vim'
" auto-close brackets, quotes, code structures, etc.
Plug 'Raimondi/delimitMate'
Plug 'tpope/vim-endwise'
" fast jumping around the visible text
Plug 'easymotion/vim-easymotion'
" fuzzy file search
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'flazz/vim-colorschemes'
Plug 'junegunn/rainbow_parentheses.vim'
" close HTML tags
Plug 'alvan/vim-closetag'
" commenting out
Plug 'tpope/vim-commentary'
" Git integration
Plug 'tpope/vim-fugitive'
" Python semantic coloring - currently disabled, because it's too error prone.
" :UpdateRemotePlugins doesn't seem to be called automatically.
" Maybe the upgrade script needs to run PlugUpdate! (with the bang on the end)
" https://github.com/junegunn/vim-plug/issues/1119#issuecomment-1066479981
" Plug 'numirias/semshi', { 'do': ':UpdateRemotePlugins' }

" I use this for renaming stuff in Python
Plug 'davidhalter/jedi-vim'
Plug 'fisadev/vim-isort'
" highlighting Python test coverage
Plug 'mgedmin/coverage-highlight.vim'
" automatic Python imports
Plug 'relastle/vim-nayvy'
" unix file operations on open files
Plug 'tpope/vim-eunuch'
Plug 'hashivim/vim-terraform'

" Nerdtree - file explorer. With plugins
Plug 'preservim/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'ryanoasis/vim-devicons'
Plug 'PhilRunninger/nerdtree-visual-selection'

call plug#end()

" Cheat sheet with commands I don't use often:
" gq+MOVE or gqq for single line - format line, insert line breaks

" My settings follow
if &term =~ '^screen'
    " tmux will send xterm-style keys when its xterm-keys option is on
    execute "set <xUp>=\e[1;*A"
    execute "set <xDown>=\e[1;*B"
    execute "set <xRight>=\e[1;*C"
    execute "set <xLeft>=\e[1;*D"
endif

set rtp+=~/bin/fzf

set expandtab
set tabstop=4
set shiftwidth=4

let g:markdown_folding = 1
set foldlevelstart=2

" I usually want my text and code at up to 120 characters. Formatting done with gq
" set textwidth=120
" Disabling this for the time being.
set textwidth=0

" working with the system clipboard (requires vim-gtk3)
set clipboard=unnamedplus

" Markdown syntax highlighting
autocmd BufNewFile,BufFilePre,BufRead *.md set filetype=markdown

" Bash syntax highlighting
autocmd BufNewFile,BufFilePre,BufRead .bash_functions set filetype=sh

" YML editing options
autocmd FileType yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2

" Terraform editing options
autocmd BufNewFile,BufFilePre,BufRead *.tfvars set filetype=tf
autocmd FileType tf setlocal tabstop=2 softtabstop=2 shiftwidth=2

" SQL editing options
autocmd FileType sql setlocal tabstop=2 softtabstop=2 shiftwidth=2

" HTML/CSS editing options
autocmd FileType css,html* setlocal tabstop=2 softtabstop=2 shiftwidth=2
" prevent delimitMate from closing tags by not using <>, so that vim-closetag can do it's job
" TODO not working
autocmd FileType html let b:delimitMate_matchpairs = "(:),[:],{:}"

autocmd FileType toml setlocal commentstring=#\ %s

set ignorecase
set hlsearch
set incsearch
set smartcase
set nowrap

" line number shown at cursor, relative numbers on other lines
set number
set relativenumber
" highlight only the line number, not the whole line
set cursorlineopt=number
" enable highlight
set cursorline

" showing whitespace
set listchars=trail:¬,tab:>-,extends:>,precedes:<
set list

" buffers are hidden, not closed when switching to a different one; preserves undo history
set hidden

" show commands as they are being typed
set showcmd

" always display the status line
set laststatus=2

colorscheme darcula
syntax enable

" disable background color settings, so it can be transparent
highlight Normal guibg=NONE ctermbg=NONE

" Coloring syntax on long lines was slow in Vim, though it seems to be better in NeoVim.
" This limits the number of columns to be colored.
" set synmaxcol=200

" Unbind space from doing anything in normal mode, make it the leader key.
noremap <Space> <NOP>
let mapleader = " "

" spell-checking
set spell spelllang=en_us
set spellfile=~/.vim/en.utf-8.add

" toggle between English and Polish spell-checking
nmap <leader>l :call ToggleSpellingLanguage()<CR>

" Set the initial value of the variable.
autocmd BufNewFile,BufFilePre,BufRead * let g:polish_spellcheck_enabled=0

function! ToggleSpellingLanguage()
    if g:polish_spellcheck_enabled
        let g:polish_spellcheck_enabled=0
        setlocal spelllang=en_us
    else
        let g:polish_spellcheck_enabled=1
        setlocal spelllang=pl
    endif
endfunction

" TODO bind a shortcut to type :%s:<CURSOR>:gc so that I can search and replace faster

" copy the current file's path
nmap cp :let @+ = expand("%")<CR>

" jumping around method level code blocks with a nicer binding
nmap <leader>[ [m
nmap <leader>] ]m

" code analysis and refactoring
nnoremap <leader>d :YcmCompleter GoToDefinition<CR>
nnoremap <leader>c :YcmCompleter GetDoc<CR>
nnoremap <leader>r :YcmCompleter GoToReferences<CR>
" nnoremap <leader>R :Semshi rename<CR>
let g:jedi#rename_command = "<leader>R"

" jumping around the quickfix list
nnoremap <leader>j :cn<CR>
nnoremap <leader>k :cp<CR>

" jumping around the location list
nnoremap <leader>J :lnext<CR>
nnoremap <leader>K :lprev<CR>

" keybindings for fuzzy file finding and search
nnoremap <leader>. :FZF<CR>
nnoremap <leader>, :Buffers<CR>
nnoremap <leader>/ :Ag<CR>
nnoremap ? :Ack ""<Left>
" find a file in the Virtualenv
nnoremap <leader>> :FZF $VIRTUAL_ENV/lib<CR>
" find text in the Virtualenv
nnoremap <leader>? :Ack "" $VIRTUAL_ENV/lib<C-Left><Left><Left>

" useful keybindings for basic operations
nnoremap <leader>q :bd<CR>
nnoremap <leader>s :w<CR>

" easymotion configuration, only explicit mappings
let g:EasyMotion_do_mapping=0
map <leader>w <Plug>(easymotion-w)
map <leader>W <Plug>(easymotion-W)
map <leader>b <Plug>(easymotion-b)
map <leader>B <Plug>(easymotion-B)

" Useful when you want to paste one thing over a couple of things without Vim
" replacing the default register after the initial replace.
vnoremap <leader>p "0p

" Search for occurrences of a word in code files.
nnoremap <leader>f :execute "Ack " . expand("<cword>")<CR>

" Search for occurrences of a word in python files, don't jump to first found immediately (j), but
" open the quickfix list (cw).
" Should use that when YouCompleteMe fails to find references.
nnoremap <leader>F :execute "vimgrep /" . expand("<cword>") . "/j **/*.py"<Bar>cw<CR>

" Run Ale fixers, like ruff --format
nnoremap <leader>t :ALEFix<CR>

" map inserting a timestamp
nnoremap <leader>T "=strftime("%Y-%m-%d %H:%M:%S")<CR>P

" Open nerdtree on the location of current file
nnoremap <leader>n :NERDTreeFind<CR>

" nerdtree size
let g:NERDTreeWinSize=70

" tweaking the preview display of open buffers for the FZF plugin
let g:fzf_preview_window = ['up:50%', 'ctrl-/']

" making YouCompleteMe work nicely with virtualenv
let g:ycm_python_binary_path = 'python'

" automatically close the doc preview window after completion
let g:ycm_autoclose_preview_window_after_completion = 1

" ack.vim should use silver searcher under the hood
" It will search in hidden files, but will ignore git stuff
let g:ackprg = 'ag --vimgrep --hidden --ignore .git'

" ALE configuration =====================

" Set the linter depending on what's available in the current environment.
" for linter in ['ruff', 'pylint', 'flake8', 'pycodestyle']
"     if system("python3 -c 'import " . linter . "'") == ""
"         let g:ale_linters = { 'python': [linter] }
"         break
"     endif
" endfor
let g:ale_linters = { 'python': ['ruff', 'mypy'] }

let g:ale_fixers = { 'python': ['ruff_format'] }

let g:ale_lint_on_text_changed = 'never'
let g:ale_fix_on_save = 0

" ======================================

" disable jedi-vim completions and unused commands - something else will be taking care of that
let g:jedi#completions_enabled = 0
" only bind the needed jedi-vim commands
let g:jedi#goto_command = ""
let g:jedi#goto_assignments_command = ""
let g:jedi#goto_stubs_command = ""
let g:jedi#goto_definitions_command = ""
let g:jedi#documentation_command = ""
let g:jedi#usages_command = ""
let g:jedi#completions_command = ""

" Rainbow parentheses config
let g:rainbow#pairs = [['(', ')'], ['[', ']']]
au VimEnter * RainbowParentheses

" This is needed if you're using virtualenvs (:help python-virtualenv)
let g:python3_host_prog = '~/.virtualenvs/neovim/bin/python'
