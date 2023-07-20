Windows Setup
================

Tested on Windows 11

Find "Windows Features". Enable Hyper-V, virtualization, WSL

In Terminal: wsl --install Ubuntu-22.04

Install droid sans powerline fonts into Windows. Choose droid sans in Windows Terminal.

Install docker for windows (select WSL2 backend).
Enter Docker Desktop settings -> resources -> WSL integration -> "Enable integration with additional distros"/Ubuntu

sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt update
sudo apt install neovim tmux zsh python3.10-venv python3.10-full python3.10-dev make cmake fonts-powerline build-essential fonts-hack-ttf zsh-autosuggestions silversearcher-ag fd-find

sudo ln -s /usr/bin/fdfind /usr/bin/fd

Neovim as vim: sudo update-alternatives --config vim


Git pull machine_setups
Comment out most of the steps in `__main__`
run

Edit ~/.zshrc:
- source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
- source ~/.oh-my-zsh/custom/themes/powerlevel10k/powerlevel10k.zsh-theme

Install powerlevel10k into oh my zsh (https://github.com/romkatv/powerlevel10k#oh-my-zsh)
Run p10k configure

## Side notes

Checkout ubuntu_changes.md from the ubuntu setup branch
