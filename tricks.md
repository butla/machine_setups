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
**closing LVM and LUKS container**
sudo vgchange -a n vg0 && sudo cryptsetup close cryptdisk

**LVS: resize a filesystem**
- `sudo lvm lvscan` to get the volumes, let's say it's /dev/data/root
- sudo e2fsck -f /dev/data/root
- `sudo resize2fs -P /dev/data/root 75G` (last bit is the size)

**Shrink LVM container inside a LUKS container**
https://wiki.archlinux.org/title/Resizing_LVM-on-LUKS#Resize_LVM_physical_Volume

- [find $LV and $VG]
- sudo lvs
- # the units here are gibibytes!
- sudo lvresize -L 68G --resizefs $VG/$LV
- # [optionally] defragment the PV: https://unix.stackexchange.com/a/193971
- # TODO maybe a reload is needed here? sudo lvm pvscan shows nice values
- sudo pvdisplay <opened luks partition, e.g. "/dev/mapper/crypt_pop_os">
- NEW_VOLUME_BYTES = 4* PE_SIZE * TOTAL_PE + UNUSABLE_SIZE
- # if shrinking, calculate the size you want in mebibytes (this is safe, won't let you go below what's taken)
- sudo pvresize --setphysicalvolumesize 69619M <opened luks partition>
- # get luks sector size
- sudo cryptsetup status crypt_pop_os
- # figure out the bytes to give to cryptsetup
- sudo pvdisplay /dev/mapper/crypt_pop_os
- NEW_LUKS_SECTOR_COUNT = TOTAL PE * PE Size [BYTES] / LUKS_SECTOR_SIZE [BYTES]
- sudo cryptsetup -b $NEW_LUKS_SECTOR_COUNT resize crypt_pop_os
- # closing LVM
- sudo vgchange -a n data
- # closing the luks container
- sudo cryptsetup close crypt_pop_os
- # resize partition
- sudo parted /dev/nvme0n1
  > unit
  > s
  > p[rint]
  # sectors are NEW_LUKS_SECTOR_COUNT + offset sectors from "cryptsetup status"
  # NEW_PARTITION_SECTOR_END = PARTITION_SECTOR_START + NEW_LUKS_SECTOR_COUNT - 1
  > resizepart 3 NEW_PARTITION_SECTOR_END
