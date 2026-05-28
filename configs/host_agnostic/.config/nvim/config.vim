set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath

" vim-plug automatic download and setup
if empty(glob('~/.local/share/nvim/site/autoload/plug.vim'))
  silent !curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source ~/.config/nvim/init.vim
endif

call plug#begin(stdpath('data') . '/plugged')

" TODO remove it when not needed
Plug 'ycm-core/YouCompleteMe', { 'do': './install.py' }
" LSP client + language servers
Plug 'neovim/nvim-lspconfig'
" completions engine + LSP source (vim.snippet built-in handles snippet expansion on nvim 0.10+)
Plug 'hrsh7th/nvim-cmp'
Plug 'hrsh7th/cmp-nvim-lsp'
" treesitter-based syntax highlighting
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
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
" neovim-native darcula with treesitter highlight group support
Plug 'doums/darcula'
Plug 'junegunn/rainbow_parentheses.vim'
" close HTML tags
Plug 'alvan/vim-closetag'
" commenting out
Plug 'tpope/vim-commentary'
" Git integration
Plug 'tpope/vim-fugitive'
" I use this for renaming stuff in Python
" TODO remove when not needed anymore.
Plug 'davidhalter/jedi-vim'
Plug 'fisadev/vim-isort'
" highlighting Python test coverage
Plug 'mgedmin/coverage-highlight.vim'
" automatic Python imports
Plug 'relastle/vim-nayvy'
" unix file operations on open files
Plug 'tpope/vim-eunuch'
Plug 'hashivim/vim-terraform'

" Neotree - file explorer, with plugins.
Plug 'nvim-neo-tree/neo-tree.nvim', {'branch': 'v3.x'}
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-tree/nvim-web-devicons'
Plug 'MunifTanjim/nui.nvim'

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
" highlight Normal guibg=NONE ctermbg=NONE

" Orange markdown headers matching the darcula style (doums/darcula may define these differently)
highlight @markup.heading guifg=#c57825 ctermfg=222 gui=bold cterm=bold

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

" code analysis and refactoring (LSP)
nnoremap <leader>d <cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <leader>c <cmd>lua vim.lsp.buf.hover()<CR>
nnoremap <leader>r <cmd>lua vim.lsp.buf.references()<CR>
nnoremap <leader>R <cmd>lua vim.lsp.buf.rename()<CR>

" jumping around the quickfix list
nnoremap <leader>j :cn<CR>
nnoremap <leader>k :cp<CR>

" jumping around the location list
nnoremap <leader>J :lnext<CR>
nnoremap <leader>K :lprev<CR>

" open the errors / warnings list
nnoremap <leader>e :lopen<CR>

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
" open the quickfix list (cw). Fallback when LSP references don't find everything.
nnoremap <leader>F :execute "vimgrep /" . expand("<cword>") . "/j **/*.py"<Bar>cw<CR>

" Run Ale fixers, like ruff --format
nnoremap <leader>t :ALEFix<CR>

" map inserting a timestamp
nnoremap <leader>T "=strftime("%Y-%m-%d %H:%M:%S")<CR>P

" Open neotree on the location of current file
nnoremap <leader>n :Neotree reveal<CR>

" tweaking the preview display of open buffers for the FZF plugin
let g:fzf_preview_window = ['up:50%', 'ctrl-/']

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

" Rainbow parentheses config
let g:rainbow#pairs = [['(', ')'], ['[', ']']]
au VimEnter * RainbowParentheses

" This is needed if you're using virtualenvs (:help python-virtualenv)
let g:python3_host_prog = '~/.virtualenvs/neovim/bin/python'

" TODO Fix. NerdTree breaks after opening up a couple of buffers.
" Jump to a different window if I get automatically moved to NerdTree.
" This will make the cursor go to the code window instead of NerdTree after
" closing the quick-fix view.
" augroup NerdTreeFocusFix
"   autocmd!
"   " If focus moves into a nerdtree window automatically, bounce back
"   autocmd BufEnter * if winnr("$") > 1 && &filetype ==# 'nerdtree' && bufname('#') !~# 'NERD_tree' | wincmd p | endif
" augroup END
