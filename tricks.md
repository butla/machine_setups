Spell book
==========

Various tricks, snippets, commands for doing things.

## Check what package a file belongs to
pacman -Qo <file>

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

## Filesystem management
**LVS: resize a filesystem**
- `sudo lvm lvscan` to get the volumes, let's say it's /dev/data/root
- sudo e2fsck -f /dev/data/root
- `sudo resize2fs -P /dev/data/root 75G` (last bit is the size)

**Shrink LVM container inside a LUKS container**
https://wiki.archlinux.org/title/Resizing_LVM-on-LUKS#Resize_LVM_physical_Volume

- sudo lvs [find lv and vg]
- sudo lvresize -L 68G [!these are gibibytes!] --resizefs $VG/$LV
- # organize space in the PV?: https://unix.stackexchange.com/a/193971
- # TODO reload? sudo lvm pvscan shows nice values
- sudo pvdisplay <opened luks partition, e.g. "/dev/mapper/crypt_pop_os">
- NEW_VOLUME_BYTES = 4* PE_SIZE * TOTAL_PE + UNUSABLE_SIZE
- # if shrinking, calculate the size you want in mebibytes (this is safe, won't let you go below what's taken)
- sudo pvresize --setphysicalvolumesize 69619M <opened luks partition>
- # TODO resize luks

**closing LVM and LUKS container**
sudo vgchange -a n vg0 && sudo cryptsetup luksClose crypt
