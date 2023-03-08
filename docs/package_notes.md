Notes about certain packages and tools
======================================

Removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)

Removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u pylint: disable=line-too-long

gthumb - the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)

Timeshift emits errors on package updates on BTRFS. Not a real problem
https://forum.manjaro.org/t/btrfs-updating-leads-to-e-error-cant-list-qgroups-quotas-not-enabled/110375/8

Syncthing syncs symbolic links, not their targets. They might not sync correctly to the phone.
Don't have links in synced folders.

## Digikam

### Notes
Restarting digikam rereads tags from files, doesn't remove the ones that disappeared

### Settings to set
Settings/Configure/Metadata/Behavior (makes it play nicer with syncing files with Syncthing):
- update file modification timestamps
- rescan file when files are modified
- clean up metadata from the database when rescan files

Settings/Configure/Metadata/Sidecars (this ensures that video files have metadata saved in the filesystem):
- read from sidecar files
- write to sidecar files
- write to xmp sidecar for read-only item only

Settings/Configure/Miscellaneous/Appearance:
- Widget style: Adwaita-Dark
- Icon theme: Use Icon Theme From System

## F-Stop (Android app)

Syncing tags (https://www.fstopapp.com/forum/topic/how-do-i-force-a-rescan/#post-8022):
- General setting - Settings -> Main -> Check for Changed Images -> Compare Image’s Dates
- single file - select it, choose “revert to metadata on disk
