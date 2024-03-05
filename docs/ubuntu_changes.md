# Packages
sudo add-apt-repository ppa:neovim-ppa/stable
sudo add-apt-repository ppa:aslatter/ppa   # alacritty
sudo add-apt-repository ppa:kelebek333/mint-tools  # pix
sudo add-apt-repository ppa:deadsnakes/ppa  # python
sudo apt-get update

## Command to install mostly everything

This is the command. Packages are documented below.

sudo apt install neovim httpie curl wget htop entr fd-find fzf silversearcher-ag git nmap sipcalc ranger tmux tree hunspell hunspell-en-us hunspell-pl pandoc whois nethogs iotop sshfs wavemon twine yamllint strace python3-virtualenvwrapper python3-poetry pipx zsh fonts-powerline zsh-autosuggestions lolcat cowsay asciinema sl mediainfo glances netcat yt-dlp bat zip unzip rsync python3.11-full python-is-python3 syncthing dos2unix odt2txt smartmontools toilet xsel xclip alacritty arandr brave-browser meld keepassxc pix cheese okular xournalpp simple-scan mpv vlc kolourpaint krita audacity xsensors psensor dconf-editor freeplane chromium-browser caffeine yubioath-desktop pix dbus-x11

## Get these from snap
Slack
signal
spotify
zoom
drawio

## Packages to get in alternative ways
ueberzug installed from pipx (it's not there, there's a fork ueberzug-bak, but it won't work on wayland anyway. Maybe should switch to Kitty)
Needs libxext-dev package

zsh-theme-powerlevel10k - git clone into oh my zsh
https://github.com/romkatv/powerlevel10k#oh-my-zsh
(does that get updates?)

awesome-terminal-fonts - fonts-hack-ttf should handle that

Docker - https://docs.docker.com/engine/install/ubuntu/

poetry - get from pipx

dbus-x11 - needed for dbus-launch

## Manjaro to Ubuntu packages
fd -> fd-find
the_silver_searcher -> silversearcher-ag
powerline-fonts -> fonts-powerline 
base-devel -> build-essential
gnu-netcat -> netcat
hunspell-en_us -> hunspell-en-us
zsh-completions -> zsh-autosuggestions (is this really that?)
python-virtualenvwrapper -> python3-virtualenvwrapper
python-pipx -> pipx
yubico-authenticator-bin -> yubioath-desktop
caffeine-ng -> caffeine
brave -> brave-browser
chromium -> chromium-browser
libnotify -> libnotify-bin

## Skipped packages
borg
yq
python-pudb
python-ipdb
python-tox
python-pylint
python-eyed3
lm_sensors
bluez-utils
dog
ldns
gendesk
cronie
hd-idle
"shotcut",  # a video editor
"obs-studio",  # video recording
"strawberry",  # music player, Clementine replacement
"discord",  # communicator / chat
"qbittorrent",
"qbittorrent-nox",  # non-GUI version of the torrent app
"virtualbox",
"libreoffice-still",
"adapta-maia-theme",  # a theme for XFCE that I like
"kvantum-manjaro",  # themes for QT apps
"asunder",  # audio CD ripper
"qt6ct",  # QT6 theme configurator, needed for new qbittorent
"gimp",  # image editor
"gnome-system-monitor",  # nice GUI to show resource usage charts
"system-config-printer",  # Manjaro or XFCE printer setup GUI
"digikam",  # a photo manager
"inkscape",  # vector graphics creator
libcanberra - present in Ubuntu
xorg-xinput
dbeaver

## For working psycopg2 builds
libpq-dev
python3.9-dev python3.8-dev

## AWS CLI setup
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#cliv2-linux-install

# Run `machine_setup` without some steps
Disable `sync_packages` and `set_java_version`

# Tweak fzf history
.local/share/nvim/plugged/fzf/shell/key-bindings.zsh -> remove "--scheme=history"

# Powerlevel10k setup
Run p10k configure once for a new system
And then merge it with the version from the repo.
