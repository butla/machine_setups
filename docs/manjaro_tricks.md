Manjaro tricks
==============

## New Python version

Upgrade and rebuild python packages:
- Pipx - reinstall packages
- wipe ~/.virtualenvs (neovim one will get recreated when setup is run)
- rm -rf ~/.local/share/nvim/plugged
- run `make setup_machine`
