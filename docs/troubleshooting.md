Troubleshooting tips
====================

## System error diagnostics
sudo journalctl -xe -b 0 -p err
sudo journalctl -xe -b 0 -p warning
sudo dmesg

## Restart Gnome
killall -HUP gnome-shell

## New version of a package messed something up
sudo downgrade <package>

## Dealing with pacman / pamac invalid GPG signatures

Looks like this:

```
Refreshing multilib.db...
Error: multilib.db: GPGME error: No data
```

**Solution**
- sudo rm -rf /var/lib/pacman/sync /var/tmp/pamac/dbs/sync/ /var/cache/pkgfile
- have good mirrors.
- sudo pamac upgrade

or [this solution](https://forum.manjaro.org/t/root-tip-how-to-mitigate-and-prevent-gpgme-error-when-syncing-your-system/84700)

**Root cause**
Looks like the sig files in /var/lib/pacman/sync (and other similar folders) that get downloaded by pacman
sometimes contain error HTTP responses from the mirror instead of signatures.

## Test anacrontab
anacron -d -t ${HOME}/.local/etc/anacrontab -S /home/butla/.local/var/spool/anacron

## Syncthing showing folders up-to-date but out-of-sync with devices
sudo systemctl stop syncthing@butla
syncthing --reset-database
sudo systemctl start syncthing@butla

## KeepassXC doesn't remember the last open database
Open the database, then do really shutdown keepass (ctrl+q).

## Dropbox trey icon not showing on Gnome
- enable app indicator extension
- dropbox-cli stop && dropbox-cli start

## Nautilus crashing after start (Gnome file explorer)
Copy something to clipboard. [More context.](https://gitlab.gnome.org/GNOME/nautilus/-/issues/2539)
