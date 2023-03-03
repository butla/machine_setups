import socket


def get_packages_for_host():
    return HOSTS_TO_PACKAGES.get(socket.gethostname(), FULL_PACKAGES)


PACMAN_NO_GUI_PACKAGES = {
    # =========================
    # lightweight CLI programs
    # =========================
    'neovim',  # text editor
    'httpie',  # nice HTTP calling tool
    'curl',  # traditional HTTP calling tool
    'wget',  # download files from the web
    'htop',  # see system resource usage
    'base-devel',  # basic compilers, etc
    'make',
    'cmake',
    'entr', # rerunning commands on file changes
    'fd',  # file finder
    'fzf',  # fuzzy search
    'the_silver_searcher',  # text search in code files
    'git',
    'nmap',  # network scanner
    'sipcalc',  # network/IP address calculator
    'ranger',  # file manager
    'tmux',  # terminal multiplexer
    'tree',  # shows file trees
    'hunspell',  # CLI spellchecker
    'hunspell-en_us',
    'hunspell-pl',
    'pandoc',  # universal document converter
    'whois',  # looks up information about Internet domains
    'nethogs',  # "top"-like thing for showing network transfers
    'iotop',  # "top"-like thing for showing disk IO
    'sshfs',  # mounting remote filesystems with SSH
    'borg',  # backup solution
    'wavemon',  # WiFi monitor
    'twine',  # PyPI package release helper
    'yamllint',
    'yq',  # utility for getting stuff from YAMLs
    'strace',  # monitoring process's syscalls
    'python-pudb',  # TUI python debugger
    'python-ipdb',  # python debugger with completions and color
    'python-virtualenvwrapper',  # Python virtualenv manager
    'python-tox',  # test runner for multiple Python versions
    'python-pylint',  # python linters
    'flake8',
    'python-poetry',  # python dependency manager
    'python-pipx',  # managing Python apps in isolated virtualenvs
    'python-eyed3',  # mp3 metadata viewer
    'lm_sensors',  # provides "sensors" for reading temperature readings
    'bluez-utils',  # provides "bluetoothctl"
    'tesseract',  # OCR
    'tesseract-data-pol',
    'tesseract-data-eng',
    'zsh',  # my preferred shell
    'zsh-theme-powerlevel10k',  # a ZSH theme
    'powerline-fonts',  # needed for powerlevel10k theme
    'awesome-terminal-fonts',  # needed for powerlevel10k theme
    'zsh-autosuggestions',  # ZSH plugin for suggestions of past commands
    'zsh-completions',  # additional completions for ZSH
    'lolcat',  # colorful printing in the terminal
    'cowsay',  # ASCII talking animals
    'asciinema',  # recording terminal sessions
    'sl',  # steam locomotive
    'mediainfo',  # CLI for getting info about media files, used by ranger
    'glances',  # single view of multiple system load metrics
    'dog',  # DNS lookup.
    'ldns',  # another DNS lookup. Provides "drill", which gives more info than "dog".
    'gnu-netcat',  # TCP client/listener
    'gendesk',  # desktop file generator for apps, used while building some AUR packages
    'youtube-dl',  # download video and audio from YouTube
    # Convert USB drives, so that you make bootable USBs by copying over an (Linux/Windows) ISO file.
    # woeusb from AUR can be an alternative.
    'ventoy',
    'syncthing',  # file synchronization
    'dos2unix',  # convert Windows line endings to Unix ones
    'cronie',  # anacron implementation
    'odt2txt',  # for preview of OpenDocument in ranger
    'hd-idle',  # tool for spinning down hard disks after inactivity or immediately
    'smartmontools',  # has smartctl - utility for getting drive diagnostics
    # =========================
    # CLI programs for GUIs
    # =========================
    'libnotify',  # desktop notifications
    'xsel',  # working with the desktop clipboard from the CLI
    'xclip',  # as above
    'ueberzug',  # needed for ranger's image previews
    'libcanberra',  # needed for "canberra-gtk-play -i bell" for testing that sound is on
    'xorg-xinput',  # can be used to manage input devices (keyboards, touchpads)
    # =========================
    # heavy CLI programs for development
    # =========================
    'terraform',  # infrastructure management
    'docker',
    'docker-compose',
    'rust',  # Rust programming language tools
    'go',  # Go programming language tools
}

PACMAN_GUI_PACKAGES = {
    # =========================
    # GUI programs
    # =========================
    'alacritty',  # my preferred terminal emulator
    'arandr',  # displays' manager
    'brave-browser',  # my preferred browser
    'meld',  # visual diff tool
    'keepassxc',  # a password manager
    'pix',  # a good image viewer
    'gimp',  # image editor
    'digikam',  # a photo manager
    'inkscape',  # vector graphics creator
    'cheese',  # taking photos and videos with the camera/webcam
    'okular',  # my preferred PDF viewer
    'pdfmod',  # PDF editor
    'xournalpp',  # writing on PDFs
    'simple-scan',  # simple scanner operation
    'mpv',  # a nice video player with fast jumping and subtitle adjustment
    'vlc',  # an alternative video player
    'kolourpaint',  # Microsoft Paint clone
    'signal-desktop', # private communicator
    'discord',  # communicator / chat
    'yubioath-desktop',  # OTP with a Yubikey connected over USB
    'qbittorrent',
    'qbittorrent-nox',  # non-GUI version of the torrent app
    'virtualbox',
    'libreoffice-still',
    'adapta-maia-theme',  # a theme for XFCE that I like
    'kvantum-manjaro',  # themes for QT apps
    'asunder',  # audio CD ripper
    'krita',  # drawing program with tablet support
    'audacity',  # sound editor
    'system-config-printer',  # Manjaro or XFCE printer setup GUI
    'qt6ct',  # QT6 theme configurator, needed for new qbittorent
    'xsensors',  # shows hardware sensor info, like temperatures
    'psensor',  # temperature sensors chart
    'gnome-system-monitor',  # nice GUI to show resource usage charts
    'dconf-editor',  # find and edit Gnome/GTK app settings
    'clementine',  # music player
    'freeplane',  # mind-mapping tool, successor to freemind
}

AUR_NO_GUI_PACKAGES = {
    'wrk',  # HTTP application benchmarking tool
    'toilet',  # printing large letters in terminal
    'hollywood',  # "Fill your console with Hollywood melodrama technobabble"
    'qbittorrent-cli-bin',  # CLI for the non-GUI torrent client, TODO, make it work
    'battop',  # battery stats
    'dstask',  # task/note manager, git-based
}

AUR_GUI_PACKAGES = {
    'slack-desktop',
    'spotify',
    'tor-browser',
    'zoom',  # video conferencing
    'losslesscut-bin',  # fast and simple video editor
    # TODO get something good for recording videos - OBS? Figure out a good video editor
    # 'olive',  # video editor. Alternatives: https://github.com/nschloe/stargraph#video-editors
    # Simple/crude screencasting / desktop recording.
    # 'screenstudio',
    # Kazam looks nicer but is broken without a fix:
    # https://aur.archlinux.org/packages/kazam/
}

NO_GUI_PACKAGES = PACMAN_NO_GUI_PACKAGES | AUR_NO_GUI_PACKAGES
FULL_PACKAGES = NO_GUI_PACKAGES | PACMAN_GUI_PACKAGES | AUR_GUI_PACKAGES

NOT_PRESENT_ON_RPI_MANJARO_PACKAGES = {'pandoc', 'hollywood'}
MAIN_MACHINE_ADDITIONAL_AUR_PACKAGES = {'dropbox', 'dropbox-cli', 'exodus'}
MAIN_MACHINE_PACKAGES = FULL_PACKAGES | MAIN_MACHINE_ADDITIONAL_AUR_PACKAGES

HOSTS_TO_PACKAGES = {
    'ognisko': NO_GUI_PACKAGES - NOT_PRESENT_ON_RPI_MANJARO_PACKAGES,
    'alien': MAIN_MACHINE_PACKAGES,
    'bl': MAIN_MACHINE_PACKAGES,
}
