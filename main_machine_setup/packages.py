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
    'pandoc',  # universal document converter
    'whois',  # looks up information about Internet domains
    'nethogs',  # "top"-like thing for showing network transfers
    'iotop',  # "top"-like thing for showing disk IO
    'borg',  # backup solution
    'wavemon',  # WiFi monitor
    'twine',  # PyPI package release helper
    'yamllint',
    'yq',  # utility for getting stuff from YAMLs
    'python-pudb',  # TUI python debugger
    'python-ipdb',  # python debugger with completions and color
    'python-virtualenvwrapper',  # Python virtualenv manager
    'python-tox',  # test runner for multiple Python versions
    'python-pylint',  # python linters
    'flake8',
    'python-poetry',  # python dependency manager
    'python-pipx',  # managing Python apps in isolated virtualenvs
    'python-pynvim',  # python-integration for NeoVim
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
    # =========================
    # GUI programs
    # =========================
    'alacritty',  # my preferred terminal emulator
    'brave',  # my preferred browser
    'meld',  # visual diff tool
    'keepassxc',  # a password manager
    'gthumb',  # a good image viewer
    'gimp',  # image editor
    'inkscape',  # vector graphics creator
    'cheese',  # taking photos with the camera
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
    'qbittorrent',
    'virtualbox',
]

AUR_PACKAGES = {
    'dropbox',
    'dropbox-cli',
    'slack-desktop',
    'wrk',  # HTTP application benchmarking tool
    'subliminal',  # movie subtitles downloader
    'ptpython',  # nice python interactive shell
    'pgcli',  # Postgres CLI client
    'spotify',
}
