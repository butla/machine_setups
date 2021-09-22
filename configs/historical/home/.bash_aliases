alias subs='subliminal download -l en .'
alias subspl='subliminal download -l pl .'
alias vim='PYTHONPATH=$(pwd) vim'
alias r='ranger'
alias t='tmux -2'
alias g='git'
alias my_ip='http ipinfo.io'

alias pudbtest='pudb3 $(which pytest) -s'
alias pudbtest2='pudb $(which pytest) -s'

alias gitdiff='git difftool --dir-diff'
# completions for the alias
source /usr/share/bash-completion/completions/git
__git_complete gitdiff _git_diff

alias dockerclean='docker ps -aq | xargs docker rm'
alias dockercomposeup='docker-compose up --build; docker-compose down -v'
alias dockerports='docker ps --format "{{.Image}} >>> {{.Ports}}\n"'

alias plasmarestart='killall plasmashell && kstart plasmashell'
