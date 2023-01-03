Spell book
==========

Various tricks, snippets, commands for doing things.

## Check what package a file belongs to
pacman -Qo <file>

## Adding a program to autostart

Find it's `.desktop` file (`pacman -Fl caffeine-ng | grep .desktop`) and copy it `~/.config/autostart`.

## Filesystem management
**setup LUKS1-type partition**
sudo cryptsetup luksFormat --type luks1 /dev/drive

**backup LUKS headers**
sudo cryptsetup luksHeaderBackup --header-backup-file backup-location /dev/nvme0n1p5

**closing LVM and LUKS container**
sudo vgchange -a n vg0 && sudo cryptsetup close cryptdisk

**LVM: resize a filesystem**
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
- # close the LVM
- sudo vgchange -a n data
- # change the LUKS sector count
- sudo cryptsetup -b $NEW_LUKS_SECTOR_COUNT resize crypt_pop_os
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

**Move a partition (100 MiB backwards)**
echo '+100M,' | sudo sfdisk --move-data /dev/nvme0n1 -N 3

**Grow partition to take up the unallocated space after it**
echo ", +" | ./sfdisk -N 1 /dev/sdc

## Convert a set of images into a PDF
`convert <image paths> output.pdf`
`convert` is part of imagemagick
