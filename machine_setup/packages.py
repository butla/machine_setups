import socket


def get_packages_for_host():
    return HOSTS_TO_PACKAGES.get(socket.gethostname(), FULL_PACKAGES)


PACMAN_NO_GUI_PACKAGES = {
    # =========================
    # lightweight CLI programs
    # =========================
    "neovim",  # text editor
    "httpie",  # nice HTTP calling tool
    "curl",  # traditional HTTP calling tool
    "wget",  # download files from the web
    "htop",  # see system resource usage
    "base-devel",  # basic compilers, etc
    "make",
    "cmake",
    "entr",  # rerunning commands on file changes
    "fd",  # file finder
    "fzf",  # fuzzy search
    "the_silver_searcher",  # text search in code files
    "git",
    "nmap",  # network scanner
    "sipcalc",  # network/IP address calculator
    "ranger",  # file manager
    "tmux",  # terminal multiplexer
    "tree",  # shows file trees
    "hunspell",  # CLI spellchecker
    "hunspell-en_us",
    "hunspell-pl",
    "pandoc",  # universal document converter
    "whois",  # looks up information about Internet domains
    "nethogs",  # "top"-like thing for showing network transfers
    "iotop",  # "top"-like thing for showing disk IO
    "sshfs",  # mounting remote filesystems with SSH
    "borg",  # backup solution
    "wavemon",  # WiFi monitor
    "twine",  # PyPI package release helper
    "yamllint",
    "yq",  # utility for getting stuff from YAMLs
    "strace",  # monitoring process's syscalls
    "python-pudb",  # TUI python debugger
    "python-ipdb",  # python debugger with completions and color
    "python-virtualenvwrapper",  # Python virtualenv manager
    "python-tox",  # test runner for multiple Python versions
    "python-pylint",  # python linters
    "flake8",
    "python-poetry",  # python dependency manager
    "python-pipx",  # managing Python apps in isolated virtualenvs
    "python-eyed3",  # mp3 metadata viewer
    "lm_sensors",  # provides "sensors" for reading temperature readings
    "bluez-utils",  # provides "bluetoothctl"
    "tesseract",  # OCR
    "tesseract-data-pol",
    "tesseract-data-eng",
    "zsh",  # my preferred shell
    "zsh-theme-powerlevel10k",  # a ZSH theme
    "powerline-fonts",  # needed for powerlevel10k theme
    "awesome-terminal-fonts",  # needed for powerlevel10k theme
    "zsh-autosuggestions",  # ZSH plugin for suggestions of past commands
    "zsh-completions",  # additional completions for ZSH
    "lolcat",  # colorful printing in the terminal
    "cowsay",  # ASCII talking animals
    "asciinema",  # recording terminal sessions
    "sl",  # steam locomotive
    "mediainfo",  # CLI for getting info about media files, used by ranger
    "glances",  # single view of multiple system load metrics
    "dog",  # DNS lookup.
    "ldns",  # another DNS lookup. Provides "drill", which gives more info than "dog".
    "gnu-netcat",  # TCP client/listener
    "gendesk",  # desktop file generator for apps, used while building some AUR packages
    "yt-dlp",  # download video and audio from YouTube
    "bat",  # cat with syntax highlighting
    "zip",
    "unzip",
    "rsync",
    # Convert USB drives, so that you make bootable USBs by copying over an (Linux/Windows) ISO file.
    # woeusb from AUR can be an alternative.
    "ventoy",
    "syncthing",  # file synchronization
    "dos2unix",  # convert Windows line endings to Unix ones
    "cronie",  # anacron implementation
    "odt2txt",  # for preview of OpenDocument in ranger
    "hd-idle",  # tool for spinning down hard disks after inactivity or immediately
    "smartmontools",  # has smartctl - utility for getting drive diagnostics
    "manjaro-check-repos",  # has mbn tool for comparing packages across different Manjaro branches
    "toilet",  # printing large letters in terminal
    "pre-commit",  # running pre-commit hooks for development
    "yubikey-manager",  # CLI Yubikey usage. Backup in case yubico-authenticator-bin doesn't work.
    # =========================
    # CLI programs for GUIs
    # =========================
    "libnotify",  # desktop notifications
    "xsel",  # working with the desktop clipboard from the CLI
    "xclip",  # as above
    "ueberzug",  # needed for ranger's image previews
    "libcanberra",  # needed for "canberra-gtk-play -i bell" for testing that sound is on
    "xorg-xinput",  # can be used to manage input devices (keyboards, touchpads)
    "jre17-openjdk",  # Java runtime for programs like freeplane
    "swh-plugins",  # some audio plugins for shotcut
    "libva-intel-driver",  # for OBS
    "sndio",  # for OBS
    "v4l2loopback-dkms",  # for OBS
    # =========================
    # heavy CLI programs for development
    # =========================
    "terraform",  # infrastructure management
    "docker",
    "docker-compose",
    "rust",  # Rust programming language tools
    "go",  # Go programming language tools
    "npm",  # NodeJS package manager. Useful for some tools.
    "nvm",  # NodeJS version management
    "texlive-binextra",  # for generating HTML from Markdown with Pandoc
    "aws-cli",  # AWS and Digital Ocean CLI
    "ollama",  # running LLM AI models locally
}

PACMAN_GUI_PACKAGES = {
    # =========================
    # GUI programs
    # =========================
    "alacritty",  # my preferred terminal emulator
    "arandr",  # displays' manager
    "brave-browser",  # my preferred browser
    "meld",  # visual diff tool
    "keepassxc",  # a password manager
    "pix",  # a good image viewer
    "gimp",  # image editor
    "digikam",  # a photo manager
    "inkscape",  # vector graphics creator
    "cheese",  # taking photos and videos with the camera/webcam
    "okular",  # my preferred PDF viewer
    "xournalpp",  # PDF editor
    "simple-scan",  # simple scanner operation
    "mpv",  # a nice video player with fast jumping and subtitle adjustment
    "vlc",  # an alternative video player
    "kolourpaint",  # Microsoft Paint clone
    "signal-desktop",  # private communicator
    "discord",  # communicator / chat
    "qbittorrent",
    "qbittorrent-nox",  # non-GUI version of the torrent app
    "virtualbox",
    "libreoffice-still",
    "adapta-maia-theme",  # a theme for XFCE that I like
    "kvantum-manjaro",  # themes for QT apps
    "asunder",  # audio CD ripper
    "krita",  # drawing program with tablet support
    "audacity",  # sound editor
    "system-config-printer",  # Manjaro or XFCE printer setup GUI
    "qt6ct",  # QT6 theme configurator, needed for new qbittorent
    "xsensors",  # shows hardware sensor info, like temperatures
    "psensor",  # temperature sensors chart
    "gnome-system-monitor",  # nice GUI to show resource usage charts
    "dconf-editor",  # find and edit Gnome/GTK app settings
    "strawberry",  # music player, Clementine replacement
    "freeplane",  # mind-mapping tool, successor to freemind
    "shotcut",  # a video editor
    "obs-studio",  # video recording
    "chromium",  # browser used by automations with Playwright
    "caffeine-ng",  # prevent system from sleeping
    "dbeaver",  # universal DB client. Supports SQL Server
    "drawio-desktop",  # diagramming tool
}

AUR_NO_GUI_PACKAGES = {
    "wrk",  # HTTP application benchmarking tool
    "hollywood",  # "Fill your console with Hollywood melodrama technobabble"
    "qbittorrent-cli-bin",  # CLI for the non-GUI torrent client, TODO, make it work
    "battop",  # battery stats
    "dstask",  # task/note manager, git-based
    # DISABLING keybase because I don't use it too much and it holds a mount that freezes `ls /`
    # "keybase-bin",  # for encrypted Git repositories. AUR is fresher than regular Manjaro repo version
    "mactelnet",  # connec to to MikroTik routers with with their MAC
}

AUR_GUI_PACKAGES = {
    "slack-desktop",
    "spotify",
    "tor-browser-bin",
    "zoom",  # video conferencing
    # OTP with a Yubikey connected over USB, replaces faulty "yubioath-desktop"
    # https://bugs.archlinux.org/task/76325
    "yubico-authenticator-bin",
}

PACMAN_WORK_PACKAGES: set[str] = set()

AUR_WORK_PACKAGES: set[str] = set()
# {
#     # Package stopped working
#     # "rambox-pro-bin"  # Client for multiple Microsoft Suite accounts.
# }

WORK_PACKAGES = PACMAN_WORK_PACKAGES | AUR_WORK_PACKAGES

NO_GUI_PACKAGES = PACMAN_NO_GUI_PACKAGES | AUR_NO_GUI_PACKAGES
FULL_PACKAGES = NO_GUI_PACKAGES | PACMAN_GUI_PACKAGES | AUR_GUI_PACKAGES

NOT_PRESENT_IN_MANJARO_ARM_PACKAGES = {
    "pandoc",
    "hollywood",
    "manjaro-check-repos",
    "battop",
    "libva-intel-driver",
    "keybase-bin",
}
_arm_exclusions_not_present_in_list_of_all = NOT_PRESENT_IN_MANJARO_ARM_PACKAGES - FULL_PACKAGES
_arm_excluded_packages_are_in_list_of_all = not bool(_arm_exclusions_not_present_in_list_of_all)
if not _arm_excluded_packages_are_in_list_of_all:
    raise Exception(
        f"Some of the packages excluded on ARM aren't in the list of all packages. Remove outdated exclusions!: {_arm_exclusions_not_present_in_list_of_all}"
    )

MAIN_MACHINE_ADDITIONAL_AUR_PACKAGES = {"dropbox", "dropbox-cli", "exodus"}
MAIN_MACHINE_PACKAGES = FULL_PACKAGES | MAIN_MACHINE_ADDITIONAL_AUR_PACKAGES

HOSTS_TO_PACKAGES = {
    "ognisko": NO_GUI_PACKAGES - NOT_PRESENT_IN_MANJARO_ARM_PACKAGES,
    "alien": MAIN_MACHINE_PACKAGES,
    "lemur": MAIN_MACHINE_PACKAGES | WORK_PACKAGES,
}
