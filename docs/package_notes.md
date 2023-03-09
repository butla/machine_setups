Notes about certain packages and tools
======================================

## ZSH
Removing .zcompdump might be needed after installing oh-my-zsh (wasn't the last time I installed it)

## Python keyring integration
Removing keyring requirements for Python packages: https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u pylint: disable=line-too-long

## gthumb
the zoom-in keyboard shortcut problem (https://gitlab.gnome.org/GNOME/gthumb/-/issues/103)

## Timeshift
Emits errors on package updates on BTRFS. Not a real problem
https://forum.manjaro.org/t/btrfs-updating-leads-to-e-error-cant-list-qgroups-quotas-not-enabled/110375/8

## Syncthing
Syncs symbolic links, not their targets.
They might not sync correctly to the phone.
Don't have links in synced folders.

## Digikam

### Notes
Digikam can read tags from XMP sidecars made by F-stop, and vice versa.

Batch [fixes of creation time](https://www.reddit.com/r/kde/comments/qdlk14/comment/hlb35js/?utm_source=share&utm_medium=web2x&context=3)
(useful when the camera had the wrong time set):
- Select all the photos you want to adjust the time and date in the same manner.
- Go to Tools (right hand sight tab)
- Go to "Post-Processing" section and select Adjust Date and Time.

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

View/sort items -> by creation date

## F-Stop (Android app)

Syncing tags (https://www.fstopapp.com/forum/topic/how-do-i-force-a-rescan/#post-8022):
- General setting - Settings -> Main -> Check for Changed Images -> Compare Image’s Dates
- General setting - Settings -> Main -> Metadata -> Autosave
- General setting - Settings -> Main -> Metadata -> Sidecar filename format -> image.ext.xmp
- manual refresh: select files -> three dot menu -> “revert to metadata on disk

## Pix

Looks like .webp animations [don't work yet](https://github.com/linuxmint/pix/issues/151#issuecomment-1462024306).

## mbn

Initial info pull: `sudo mbn update` or `sudo mbn update -m` if repo is unavailable.

Check package version on a branch (e.g. unstable): `mbn info <package> --unstable`
