#!/bin/bash
set -e

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

# Gotta repartition in GParted first. (You can also do it with fdisk if you're so inclined.)
# After repartition, I get a layout like this:
# [manjaro@manjaro Seagate Backup Plus Drive]$ lsblk
# NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
# # ...omitted lines...
# # manjaro live USB
# sda           8:0    1  28.7G  0 disk /run/miso/bootmnt
# ├─sda1        8:1    1   2.4G  0 part 
# └─sda2        8:2    1     4M  0 part 
# # my external drive
# sdb           8:16   0   1.8T  0 disk 
# └─sdb1        8:17   0   1.8T  0 part /run/media/manjaro/Seagate Backup Plus Drive
# # My new M2 drive, properly identified as NVME, while the previous was "sda" (so it was just SATA?)
# nvme0n1     259:0    0 953.9G  0 disk 
# ├─nvme0n1p1 259:4    0   200M  0 part  # will be /boot/efi
# ├─nvme0n1p2 259:5    0   512M  0 part  # will be /boot 
# └─nvme0n1p3 259:6    0 953.2G  0 part  # will be the LUKS container holding an LVM group

EFI_PARTITION=/dev/nvme0n1p1
BOOT_PARTITION=/dev/nvme0n1p2
PARTITION_FOR_LUKS=/dev/nvme0n1p3

log "creating the LUKS container in the chosen partition"
# Use luks1 - it looks like GRUB can't handle being loaded from LUKS2 partitions just yet.
# https://unix.stackexchange.com/questions/298068/system-unbootable-grub-error-disk-lvmid-not-found#420334
sudo cryptsetup luksFormat --type luks1 $PARTITION_FOR_LUKS

VG_NAME=vg0
OS_VOLUME_NAME=manjaro

log "opening the new LUKS container"
sudo cryptsetup luksOpen $PARTITION_FOR_LUKS crypt
log "making the LUKS container into an LVM partition"
sudo lvm pvcreate /dev/mapper/crypt
sudo vgcreate $VG_NAME /dev/mapper/crypt
log "creating a single logical volume for Manjaro"
# We'll leave some space for another operating system.
# That one can share /boot, which includes the GRUB.
sudo lvcreate -L 853G -n $OS_VOLUME_NAME $VG_NAME

# I'm expecting the drive to be manually mounted here
cd "/run/media/manjaro/Seagate Backup Plus Drive"

log "recreating the EFI partition"
sudo dd if=bl_efi_partition_image.bin of=$EFI_PARTITION bs=8M status=progress
log 'recreating the boot (GRUB and kernel) partition'
sudo dd if=bl_boot_partition_image.bin of=$BOOT_PARTITION bs=8M status=progress

MANJARO_VOLUME_PATH=/dev/${VG_NAME}/${OS_VOLUME_NAME}
MANJARO_IMAGE_SIZE=$(du -h '/run/media/manjaro/Seagate Backup Plus Drive/bl_root_partition_image.bin' | cut -f 1)
log "recreating the root Manjaro partition in ${MANJARO_VOLUME_PATH}"
log "data size to copy ${MANJARO_IMAGE_SIZE}"
sudo dd if=bl_root_partition_image.bin of=${MANJARO_VOLUME_PATH} bs=8M status=progress

log "Resizing the root filesystem so it takes all the space available to it in the volume..."
sudo resize2fs $MANJARO_VOLUME_PATH

log "presenting the current state of partitions"
lsblk | grep -v loop

# Mine looks like this:
# NAME              MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINTS
# sda                 8:0    1  28.7G  0 disk  /run/miso/bootmnt
# ├─sda1              8:1    1   2.4G  0 part
# └─sda2              8:2    1     4M  0 part
# sdb                 8:16   0   1.8T  0 disk
# └─sdb1              8:17   0   1.8T  0 part  /run/media/manjaro/Seagate Backup Plus Drive
# nvme0n1           259:0    0 953.9G  0 disk
# ├─nvme0n1p1       259:4    0   200M  0 part
# ├─nvme0n1p2       259:5    0   512M  0 part
# └─nvme0n1p3       259:6    0 953.2G  0 part
#   └─crypt         254:0    0 953.2G  0 crypt
#     └─vg0-manjaro 254:1    0   853G  0 lvm


# Useful snippets
# ===============
# # closing the LVM and LUKS container
# sudo vgchange -a n vg0 && sudo cryptsetup luksClose crypt
