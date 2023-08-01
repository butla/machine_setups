Manjaro tricks
==============

## New Python version

Upgrade and rebuild python packages:
- Pipx - remove ~/.local/pipx
- remove virtualenvs from ~/.virtualenvs (neovim one will get recreated when setup is run)
- rm -rf ~/.local/share/nvim/plugged
- run `make setup_machine`

## Providing system diagnostics for the forum

`inxi --full --admin --filter --width`

## Graphics card setup

Info is [here](https://wiki.manjaro.org/index.php/Configure_Graphics_Cards) may be beneficial
Intel Graphics card, should have the modesetting driver enabled

Nvidia card should use the proprietary driver (video-nvidia): `sudo mhwd -i pci video-nvidia`
But currently this makes the system freeze on Alien.

It's also work noting that after removal of the Nvidia driver,
the kernel might need to be rebuilt by reinstalling with `pacman`.
