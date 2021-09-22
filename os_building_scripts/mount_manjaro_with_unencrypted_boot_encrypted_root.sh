#!/bin/bash

# Requires partitions being retrieved to the new drive.

set -e

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

EFI_PARTITION=/dev/nvme0n1p1
BOOT_PARTITION=/dev/nvme0n1p2
# this will be encrypted
ROOT_PARTITION=/dev/nvme0n1p3

log "Opening the LUKS container..."
log 'it contains /boot and root (/) partition from the existing Manjaro install'
sudo cryptsetup luksOpen $ROOT_PARTITION crypt
log waiting for LVM modules to be loaded
sudo lvs > /dev/null

log setting up a directory enabling chroot into Manjaro
log mounting the existing Manjaro partitions

sudo mount /dev/vg0/manjaro /mnt
sudo mount $BOOT_PARTITION /mnt/boot
sudo mount $EFI_PARTITION /mnt/boot/efi

log mounting psuedo file systems

sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys /mnt/sys
sudo mount --bind /dev /mnt/dev
sudo mount --bind /dev/pts /mnt/dev/pts

log "Success! Stuff should be ready for chroot. Check out the mounts:"

lsblk | grep -v loop

# useful commands:
# =====================
#
# undo
# --------------------
# sudo umount /mnt/boot/efi /mnt/boot /mnt/proc /mnt/sys /mnt/dev/pts /mnt/dev /mnt; sudo vgchange -a n vg0 && sudo cryptsetup luksClose crypt
