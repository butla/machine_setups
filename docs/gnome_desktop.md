Gnome desktop notes
===================

## Initial setup

Switch from Wayland to XServer: before logging in, check the cog icon in lower left corner, choose "Gnome on Xorg".

Enable touchegg service, so that gnome-shell doesn't constantly spam that it can't connect to it: `sudo systemctl enable --now touchegg`.

## Notes

Shutdown shortcut - ctrl+alt+delete

CLI gnome extensions installer: https://github.com/brunelli/gnome-shell-extension-installer
Might come in handy if I want to automatically set up some extensions.
Sadly, the audio swither extensions don't work on my (new) version of Gnome.
