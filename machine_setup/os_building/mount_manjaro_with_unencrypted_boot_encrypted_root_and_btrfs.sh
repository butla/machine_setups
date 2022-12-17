#!/bin/bash

# TODO setup correct btrfs mounts for everything that's in fstab
# https://fedoramagazine.org/os-chroot-101-covering-btrfs-subvolumes/
# UUID=28eb9094-4cba-4d0f-9d2d-22475a8b83a7 /boot          btrfs   defaults,discard=async,ssd 0 0
# UUID=1a0fa2f5-2f5d-46c2-b0ab-6aef6595ccdc /              btrfs   subvol=/@,defaults 0 0
# UUID=1a0fa2f5-2f5d-46c2-b0ab-6aef6595ccdc /home          btrfs   subvol=/@home,defaults 0 0
# UUID=1a0fa2f5-2f5d-46c2-b0ab-6aef6595ccdc /var/cache     btrfs   subvol=/@cache,defaults 0 0
# UUID=1a0fa2f5-2f5d-46c2-b0ab-6aef6595ccdc /var/log       btrfs   subvol=/@log,defaults 0 0

# TODO setup GRUB on lemur with console output to see what's wrong with the boot

set -e

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

# TODO parameterize this, move common code into a function in another (sourced) file in this directory,
# use values from hosts_configs.yml to fill the values
EFI_PARTITION=/dev/nvme0n1p1
BOOT_PARTITION=/dev/nvme0n1p7
# this will be encrypted
ROOT_PARTITION=/dev/nvme0n1p2
CRYPT_NAME=crypt_priv_systems
LVM_VG=priv_systems
LV=manjaro

log "Opening the LUKS container..."
sudo cryptsetup luksOpen $ROOT_PARTITION $CRYPT_NAME
log "Waiting for LVM modules to be loaded..."
sudo lvs > /dev/null

log "Mounting the existing OS partitions..."

sudo mount /dev/mapper/${LVM_VG}-${LV} /mnt
# TODO fix the mounts!
sudo mount $BOOT_PARTITION /mnt/@/boot
sudo mount $EFI_PARTITION /mnt/@/boot/efi

log "Mounting psuedo file systems..."

sudo mount --bind /proc /mnt/@/proc
sudo mount --bind /sys /mnt/@/sys
sudo mount --bind /dev /mnt/@/dev
sudo mount --bind /dev/pts /mnt/@/dev/pts

log "Success! Stuff should be ready for chroot. Check out the mounts:"

lsblk | grep -v loop

# useful commands:
# =====================
#
# undo
# --------------------
# sudo umount /mnt/boot/efi /mnt/boot /mnt/proc /mnt/sys /mnt/dev/pts /mnt/dev /mnt; sudo vgchange -a n vg0 && sudo cryptsetup luksClose crypt
