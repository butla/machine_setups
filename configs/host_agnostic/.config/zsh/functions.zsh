# TODO split this file into multiple categories

# log stuff in functions and scripts in a way that shows that the messages are from me and give me some info I want.
# I was tempted to call this function simply "log", but it is a shell builtin and it's hard to get it to work in scripts.
function log_info() {
    _BACKGROUND_GREEN="\x1b[42m"
    _BACKGROUND_RESET="\x1b[49m"

    echo $_BACKGROUND_GREEN $(date --iso-8601=seconds) INFO $_BACKGROUND_RESET $@
}


# Attach to a local Postgres container.
function pgclidocker()
{
    CONTAINER_PORT=$(docker ps | grep '\->5432' | python3 -c "import re; port = re.findall(r':(\d+)->5432', input())[0]; print(port)")
    pgcli -h localhost -p ${CONTAINER_PORT} -d postgres -U postgres
}

function toxac()
{
    for version in py36 py35 py34 py27; do
        if [ -d .tox/$version ]; then
            source .tox/$version/bin/activate
            break
        fi
    done
}

function virtualenv_for_folder_name()
{
    virtualenv_name=$(lsvirtualenv -b | grep $(basename $(pwd)))
    echo $virtualenv_name
}

# runs NeoVim with good Python completions
function v()
{
    log_info "Running neovim with Python stuff, and these arguments: $@"

    # Don't try to load anything if a venv is already activated
    if [[ -n $VIRTUAL_ENV ]]; then
        : # no-op
    elif [ -d .venv ]; then
        source .venv/bin/activate
    elif [[ $(virtualenv_for_folder_name) != "" ]]; then
        workon $(virtualenv_for_folder_name)
    else
        toxac
    fi

    PYTHON_PATH=$(pwd)
    # Some projects put the production code in an src directory.
    if [ -d src ]; then
        PYTHON_PATH=${PYTHON_PATH}:src
    fi
    PYTHONPATH=${PYTHON_PATH} nvim $@
    # leaving the virtualenv
    deactivate
}

function windows-1250-to-utf-8()
{
    TEMP_FILE=temp_convertion_file
    iconv \
        -f windows-1250 \
        -t utf-8 \
        "$1" > $TEMP_FILE
    mv $TEMP_FILE "$1"
}

function load_ssh_key()
{
    if ! ssh-add -l > /dev/null; then
        echo "Opening the private key and adding it to ssh-agent..."
        ssh-add
    fi
}

function upgrade()
{
    load_ssh_key

    (
        cd ~/development/machine_setups;
        echo "Git-pulling machine_setups repo...";
        git pull || exit;
        echo "Running make setup_machine..."
        make setup_machine;
    )
}

function upgrade_ognisko()
{
    load_ssh_key
    # TODO FIX! Crashes when on the remote we need to activate the SSH agent
    # (when pulling machine_setups on the RPI's side).
    ssh ognisko.local 'source ~/.zshrc; upgrade'
}

function record_voice()
{
    NAME=recording
    arecord -vv -fdat $NAME.wav
    ffmpeg -i $NAME.wav -acodec mp3 $NAME.mp3
    rm $NAME.wav
}

function say()
{
    clear
    echo "Say what you want to say."
    read the_thing_to_say
    clear
    # I know, it's a tortoise, ugh :) Upstream problems
    cowsay -f turtle "${the_thing_to_say}" | lolcat --freq 0.2 --seed 900 --speed 300 --animate
    # newline afterwards
    echo
}

# TODO do this with a param of the first function
function saysecret()
{
    clear
    echo "Say what you want to say."
    read -s the_thing_to_say
    # I know, it's a tortoise, ugh :) Upstream problems
    cowsay -f turtle $the_thing_to_say | lolcat --freq 0.2 --seed 900 --speed 300 --animate
}

function shrug()
{
    _SHRUG='¯\_(ツ)_/¯'
    echo "$_SHRUG copied to clipboard..."
    echo $_SHRUG | xclip -selection clipboard
}

function passwordgen()
{
    python3 -c "import secrets; print(secrets.token_urlsafe(16), end='')" | xclip -selection clipboard
    echo "Password created and copied to clipboard..."
}

# fuzzy finding a file/directory and then going to its location (jumping)
# TODO maybe should go into the directory if it's selected?
function fj()
{
    CHOSEN_PATH=$(fzf)
    if [ $? != 0 ]; then
        echo '[[Jump cancelled]]'
        return
    fi
    JUMP_TARGET=$(dirname ${CHOSEN_PATH})
    cd $JUMP_TARGET
}

# Fuzzily find a file and open it with the current editor (which should be neovim, of course :) )
function vf()
{
    _find_file_and_edit --hidden --follow --exclude .git --no-ignore
}

# like vf(), but searches all over the system, in the usual locations I want to change stuff in.
function ve()
{
    _find_file_and_edit \
        --hidden --follow --no-ignore \
        --exclude .git --exclude .PlayOnLinux --exclude .steam \
        --exclude .wine --exclude '.local/share/Steam/**' \
        --search-path ~ --search-path /etc
}

function _find_file_and_edit()
{
    FD_FILTER=$@
    CHOSEN_FILE=$(fd $@ | fzf)
    if [ $? != 0 ]; then
        echo '[[Edit cancelled]]'
        return
    fi
    $EDITOR $CHOSEN_FILE
}

# Gets the name of the current directory.
# I couldn't find a satisfactorily readable method for doing that with just the shell.
function current_directory()
{
    echo $(python3 -c "from pathlib import Path; print(Path('.').absolute().name)")
}

# create a virtualenv for the current directory, which should be a python project
function mkvirt()
{
    # uses mkvirtualenv from https://pypi.org/project/virtualenvwrapper/
    mkvirtualenv $(current_directory)
}

# Enters a virtualenv for the current project.
# Assumes that the virtualenv is created by virtualenvwrapper
# and is called the same as the current directory/project.
function workonc()
{
    workon $(current_directory)
}

function subs()
{
    OPENSUBTITLES_USER=$(cat ~/.credentials/opensubtitles_creds.json | jq .username)
    OPENSUBTITLES_PASS=$(cat ~/.credentials/opensubtitles_creds.json | jq .password)

    subliminal --opensubtitles $OPENSUBTITLES_USER $OPENSUBTITLES_PASS download -l en .
}

function subspl()
{
    OPENSUBTITLES_USER=$(cat ~/.credentials/opensubtitles_creds.json | jq .username)
    OPENSUBTITLES_PASS=$(cat ~/.credentials/opensubtitles_creds.json | jq .password)

    subliminal --opensubtitles $OPENSUBTITLES_USER $OPENSUBTITLES_PASS download -l pl .
    if [[ $(file *.pl.srt) == *"Non-ISO"* ]]; then
        echo "Fixing a windows-1250 subtitle file..."
        windows-1250-to-utf-8 *.pl.srt
    fi
}

# TODO make this say exactly what program modified what file in the audited directories
# Right now the it produces a lot of spam that needs to be grepped.
#
# Something like `aureport -i -k THE_KEY` should say that, but it says they're not implemented.
#
# Potential inspiration: https://kifarunix.com/find-out-who-edited-files-in-linux/
function configs_audit()
{
    AUDIT_KEY=configs_audit
    log_info "Gonna trace programs that write potential configs - directories like: ~/.config, ~/.local, /etc"

    log_info "Starting auditd service for tracing..."
    sudo systemctl start auditd.service

    log_info "Adding trace to certain directories..."
    audit_paths=("$HOME/.config" "$HOME/.local" "/etc")
    for audit_path in "${audit_paths[@]}"; do
        sudo auditctl -w $audit_path -p wa -k $AUDIT_KEY
    done

    log_info "You can now do the thing in some program, that you want to trace... Press \"enter\" here once you're done"
    read

    # TODO this line alone produces something, but if ran in this script it doesn't
    # filter out (grep -v) things that spam .config the most
    sudo ausearch --start recent --format interpret -k $AUDIT_KEY | grep name | grep -v spotify | grep -v Slack | grep -v Brave | grep -E 'type=PROCTITLE|type=PATH'

    log_info "Removing directories from trace..."
    for audit_path in "${audit_paths[@]}"; do
        sudo auditctl -W $audit_path -p wa -k $AUDIT_KEY
    done

    # TODO doesn't want to stop
    # log "Stopping auditd service after tracing..."
    # sudo systemctl stop auditd.service
}

function nmap_local()
{
    sudo nmap -sn 192.168.50.0/24 | awk '/Nmap scan report/{if (NR!=1) print ""; print} !/Nmap scan report/'
}
