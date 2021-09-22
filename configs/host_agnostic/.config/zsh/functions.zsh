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
#
# runs Vim with good Python completions
function v()
{
    if [[ $(virtualenv_for_folder_name) != "" ]]; then
        workon $(virtualenv_for_folder_name)
    else
        toxac
    fi

    PYTHON_PATH=$(pwd)
    # Some projects put the production code in an src directory.
    if [ -d src ]; then
        PYTHON_PATH=${PYTHON_PATH}:src
    fi
    PYTHONPATH=${PYTHON_PATH} vim $@
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

function upgrade()
{
    echo "${bg[green]}---${reset_color}Looking for updates with yay${bg[green]}---${reset_color}"
    yay -Syu;
    echo "${bg[green]}---${reset_color}Removing unused pacman packages${bg[green]}---${reset_color}"
    sudo pacman -R $(pacman -Qdtq)

    echo "${bg[green]}---${reset_color}Looking for updates with flatpak${bg[green]}---${reset_color}"
    flatpak update;

    echo "${bg[green]}---${reset_color}Updating NeoVim plugins${bg[green]}---${reset_color}"
    nvim +PlugUpgrade +PlugClean +PlugUpdate +qall

    # TODO update Tmux plugins
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
    # I know, it's a tortoise, ugh :) Upstream problems
    cowsay -f turtle "$@" | lolcat --freq 0.2 --seed 900 --speed 300 --animate
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

function gp()
{
    git push $@
    echo "-----------"
    git status
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
    CHOSEN_FILE=$(fd --hidden --follow --exclude .git --no-ignore | fzf)
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

function subspl()
{
    subliminal download -l pl .
    if [[ $(file *.pl.srt) == *"Non-ISO"* ]]; then
        echo "Fixing a windows-1250 subtitle file..."
        windows-1250-to-utf-8 *.pl.srt
    fi
}
