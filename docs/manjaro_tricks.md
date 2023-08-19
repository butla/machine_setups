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

Check the current running driver with `inxi -Gxx`.
i915 is Intel.

### Intel GPU
There's screen tearing on the lemur now.
Interestingly, Huawei on Gnome also had tearing on the vsync test.

Everything in this section is a "maybe".
Intel Graphics card, should have the modesetting driver enabled.

Or maybe just set this?
Set this file `/etc/X11/xorg.conf.d/20-intel.conf` to
```
Section "Device"
  Identifier "Intel Graphics"
  Driver "intel"
  Option "TearFree" "false"
  Option "DRI"  "iris"
EndSection
```

### Nvidia GPU
Nvidia card should use the proprietary driver (video-nvidia): `sudo mhwd -i pci video-nvidia`
But currently this makes the system freeze on Alien.

It's also work noting that after removal of the Nvidia driver,
the kernel might need to be rebuilt by reinstalling with `pacman`.
