#!/bin/bash

set -e

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

# TODO parameterize this, move common code into a function in another (sourced) file in this directory,
# use values from hosts_configs.yml to fill the values
EFI_PARTITION=/dev/nvme0n1p1
BOOT_PARTITION=/dev/nvme0n1p2
# this will be encrypted
ROOT_PARTITION=/dev/nvme0n1p3
CRYPT_NAME=crypt
LVM_VG=vg0
LV=manjaro

log "Opening the LUKS container..."
sudo cryptsetup luksOpen $ROOT_PARTITION $CRYPT_NAME
log "Waiting for LVM modules to be loaded..."
sudo lvs > /dev/null

log "Mounting the existing OS partitions..."

sudo mount /dev/mapper/${LVM_VG}-${LV} /mnt
sudo mount $BOOT_PARTITION /mnt/boot
sudo mount $EFI_PARTITION /mnt/boot/efi

log "Mounting psuedo file systems..."

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
