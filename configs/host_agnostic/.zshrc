# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/snap/bin:$HOME/.local/lib/node_modules/bin:$HOME/.cargo/bin:$HOME/go/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/butla/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
# ZSH_THEME="bira"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="yyyy-mm-dd"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  # TODO have something like globalias but that expands only after enter
  # and use it only when tutoring or presenting
  docker
  docker-compose
)

source $ZSH/oh-my-zsh.sh

export EDITOR='nvim'
#
# if less than one screen worth of output, just print it on stdout
# Without this Git on ZSH was trying to put everything through a pager.
export PAGER="less -F -X"

## Options section (listed under `man zshoptions`)
setopt always_to_end
setopt auto_cd
setopt auto_pushd
unsetopt case_glob
setopt complete_in_word
unsetopt extended_glob  # breaks using stuff like "HEAD^" with git
unsetopt flow_control   # prevents ctrl+s from freezing the terminal
setopt hist_ignore_dups
setopt hist_ignore_space
setopt hist_verify
unsetopt inc_append_history
setopt long_list_jobs
setopt numeric_glob_sort
setopt prompt_subst
setopt pushd_ignore_dups
setopt pushd_minus
setopt rc_expand_param
setopt share_history

HISTSIZE=50000
SAVEHIST=10000
HISTFILE=~/.zsh_history

# enable vim mode
bindkey -v

# normal delete and backspace with VIM mode
bindkey "^D" delete-char-or-list
bindkey "^?" backward-delete-char

# fzf for shell history
source ~/.local/share/nvim/plugged/fzf/shell/key-bindings.zsh

# bind cd with fzf to crtl+k in addition to esc+c (described as alt+c)
bindkey '^K' fzf-cd-widget

# virtualenvwrapper setup
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/development
source $(which virtualenvwrapper.sh)

# make python scripts use ipdb by default when debugging
export PYTHONBREAKPOINT=ipdb.set_trace

# fd configuration, mainly so that FZF works more to my liking
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'

source ~/.config/zsh/aliases.zsh
source ~/.config/zsh/functions.zsh

source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.config/zsh/p10k.zsh ]] || source ~/.config/zsh/p10k.zsh
