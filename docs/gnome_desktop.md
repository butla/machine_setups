Gnome desktop notes
===================

## Initial setup

Switch from Wayland to XServer: before logging in, check the cog icon in lower left corner, choose "Gnome on Xorg".
Ranger photo preview doesn't work on Wayland.
That can be fixed with https://github.com/jstkdng/ueberzugpp, but it gives a pixelated preview.

Remove touchegg (I don't use X11 gestures, and it spams the journal with connection failures unless I enable
touchegg.service):
`pamac remove touche touchegg gnome-shell-extension-x11gestures`

Baloo file indexer for KDE is just a nuisance. Disable it: `balooctl disable`

## Notes

Shutdown shortcut - ctrl+alt+delete

CLI gnome extensions installer: https://github.com/brunelli/gnome-shell-extension-installer
Might come in handy if I want to automatically set up some extensions.
Sadly, the audio swither extensions don't work on my (new) version of Gnome.
