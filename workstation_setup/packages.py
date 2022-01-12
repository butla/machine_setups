PACMAN_PACKAGES = [
    # =========================
    # lightweight CLI programs
    # =========================
    'neovim',  # text editor
    'httpie',  # nice HTTP calling tool
    'curl',
    'base-devel',  # basic compilers, etc
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
    # =========================
    # heavy CLI programs for development
    # =========================
    'terraform',  # infrastructure management
    'docker',
    'docker-compose',
    'rust',  # Rust programming language tools
    'go',  # Go programming language tools
    # =========================
    # CLI programs for GUIs
    # =========================
    'libnotify',  # desktop notifications
    'xsel',  # working with the desktop clipboard from the CLI
    'xclip',  # as above
    'ueberzug',  # needed for ranger's image previews
    'libcanberra',  # needed for "canberra-gtk-play -i bell" for testing that sound is on
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
    'mpv',  # a nice video player
    'vlc',  # an alternative video player
    'kolourpaint',  # Microsoft Paint clone
    'signal-desktop', # private communicator
    'discord',  # communicator / chat
    'freemind',  # mindmapping tool
    'yubioath-desktop',  # OTP with a Yubikey connected over USB
    'qbittorrent',
    'virtualbox',
    'libreoffice-still',
    'adapta-maia-theme',  # a theme for XFCE that I like
    'kvantum-manjaro',  # themes for QT apps
    'asunder',  # audio CD ripper
    'mplayer',  # video player with fast jumping and subtitle adjustment
    'krita',  # drawing program with tablet support
    'audacity',  # sound editor
    'syncthing',  # file synchronization
    'system-config-printer',  # Manjaro or XFCE printer setup GUI
]

AUR_PACKAGES = {
    'dropbox',
    'dropbox-cli',
    'slack-desktop',
    'wrk',  # HTTP application benchmarking tool
    'spotify',
    'tor-browser',
    'zoom',  # video conferencing
    'toilet',  # printing large letters in terminal
    'hollywood',  # "Fill your console with Hollywood melodrama technobabble"
    # TODO get something good for recording videos.
    # Simple/crude screencasting / desktop recording.
    # 'screenstudio',
    # Kazam looks nicer but is broken without a fix:
    # https://aur.archlinux.org/packages/kazam/
}
