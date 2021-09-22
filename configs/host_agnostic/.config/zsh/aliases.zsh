# we want the python from the current active virtualenv
alias vim='PYTHONPATH=$(pwd) vim'
alias r='ranger'
alias t='tmux -2'
alias vv='tmux_ide_panel'

# quick adding of untracked or changed files
alias ga='git add $(git ls-files --modified --others --exclude-standard | fzf) && git status'
alias gcf='git checkout -- $(git ls-files --modified --others --exclude-standard | fzf) && git status'
alias gs='git status'
alias gl='git log -3 --graph'
alias gdf='git difftool --dir-diff'
alias gd='git diff'
# can't have the status and needs to be an alias, so that I get completions for branches :(
alias gc='git checkout'
alias gco='git commit -a'
alias gcoo='git commit'
alias gm='git mergetool && echo ----------- && git status'
alias gpl='git pull'
alias gf='git fetch && echo ----------- && git status'
alias gr='git rebase -i'
# rebase the commits on the current branch
alias grb='git rebase -i $(git merge-base HEAD origin/master) && echo ----------- && git status'
# show the changes made on the current branch
alias gdfb='git difftool --dir-diff $(git merge-base HEAD origin/master)'
# show the log of the current branch
alias glb='git log $(git merge-base HEAD origin/master)..HEAD'
alias gclean='git reset --hard && git clean -f && echo ----------- && git status'

alias d='docker'
alias dk='docker-compose'

# get free disk space without the trash output from Snap. Also shows file system types.
alias dff='df -hT | grep -v "/snap"'
# get bulk devices without the trash output from Snap
alias lsblkk='lsblk | grep -v "/snap"'

# thorough finding
alias fdd='fd --hidden --follow --exclude .git'
#
# find everything
alias fde='fd --hidden --follow --exclude .git --no-ignore'

alias my_ip='http ipinfo.io'
alias ag='ag --hidden --ignore .git -f'

alias pudbtest='pudb3 $(which pytest) -s'
alias pudbtest2='pudb $(which pytest) -s'

alias dockerclean='docker ps -aq | xargs docker rm'
alias dockercomposeup='docker-compose up --build; docker-compose down -v'
alias dockerports='docker ps --format "{{.Image}} >>> {{.Ports}}\n"'

alias plasmarestart='killall plasmashell && kstart plasmashell'
# Restart bluetooth devices on my machines.
# Looks like they are being put to sleep and not waking.
# Should maybe change the tlp setup, so they aren't put to sleep.
alias bluetooth_restart_bl='sudo usb_modeswitch -R -v 8087 -p 0a2b'
alias bluetooth_restart_b3='sudo usb_modeswitch -R -v 0cf3 -p e300'

alias subs='subliminal download -l en .'

# I like this as the default font
alias toilet='toilet -f mono9'

# Create a safe password in Python and copy it into the clipboard.
# Good for fast generation of passwords.
alias genpass='python -c "import secrets; print(secrets.token_urlsafe());" | xclip -selection clipboard'

# Generate an RSA key
alias genkey='ssh-keygen -t rsa -b 4096'

# Show the JSON from a file in terminal. Does the nice render.
alias jsonv='python -m json.tool'

# TODO sync folder over Rsync from another machine. Show diffs of conflicts with git --no-index
# Or use Unison?
# TODO do dry run first and ask
# TODO should be a function
# -vv so that we see what files were skipped by update, so we can show alerts if something wasn't synced (cause it was changed in two places)
alias rrsync='rsync --archive --update --dry-run -vv'

# Corrects the overscan that I can't disable on this one Sony Bravia TV
# Source of the fix: https://wiki.archlinux.org/index.php/Xrandr#Correction_of_overscan_tv_resolutions_via_the_underscan_property
alias tv_sony_bravia_overscan_fix='xrandr --output HDMI-A-0 --set underscan on --set "underscan vborder" 50 --set "underscan hborder" 94'

alias tv_barcelo_santiago_overscan_fix='xrandr --output HDMI-A-0 --set underscan on --set "underscan vborder" 20 --set "underscan hborder" 40'
# Sends a ping every second, redirects the output of that into `tee` which saves output to a file and
# displays it on the screen as it flows in.
# Records the start-time in the file name.
#
# Should I be using Google's DNS as the target? Maybe they shouldn't get my IP?
alias ping_measure='ping -i 1 8.8.8.8 | tee ping_measurement_from_$(date --iso-8601=seconds).txt'

alias pia_download='brave https://www.privateinternetaccess.com/installer/x/download_installer_linux'

alias printers_list='lpstat -p -d'
alias printer_print_options='lpoptions -d Brother_DCP_J772DW -l'
alias print_pdf_black_and_white='lpr -P Brother_DCP_J772DW -o ColorModel=Gray'
