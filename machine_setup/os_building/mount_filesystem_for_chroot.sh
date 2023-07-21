#!/bin/bash
set -e

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

HOST_TO_MOUNT=$1

if [ -z $HOST_TO_MOUNT ]; then
    echo "Specify the host for which to mount the drives."
    exit 1
fi

function get_host_value() {
    echo $(yq -r .${HOST_TO_MOUNT}.$1 $HOSTS_CONFIG_FILE)
}

PROJECT_ROOT_PATH=$(dirname $(dirname $(dirname $(readlink -f $0))))
HOSTS_CONFIG_FILE=$PROJECT_ROOT_PATH/machine_setup/hosts_config.yml

EFI_PARTITION=$(get_host_value efi_partition)
BOOT_PARTITION=$(get_host_value boot_partition)
CRYPT_PARTITION=$(get_host_value crypt_partition)
CRYPT_NAME=crypt_mounted
LVM_VG=$(get_host_value lvm.vg)
LV=$(get_host_value lvm.lv)

log "Opening the LUKS container..."
sudo cryptsetup luksOpen /dev/disk/by-uuid/$CRYPT_PARTITION $CRYPT_NAME

log "Mounting the existing OS partitions..."

if [ $LV != "null" ]; then
    log "Waiting for LVM modules to be loaded..."
    sudo lvs > /dev/null
    sudo mount /dev/mapper/${LVM_VG}-${LV} /mnt
else
    sudo mount /dev/mapper/${CRYPT_NAME} /mnt
fi

if [ $BOOT_PARTITION != "null" ]; then
    sudo mount /dev/disk/by-uuid/$BOOT_PARTITION /mnt/boot
    sudo mount /dev/disk/by-uuid/$EFI_PARTITION /mnt/boot/efi
else
    # TODO this should be migrated to /mnt/efi
    sudo mount /dev/disk/by-uuid/$EFI_PARTITION /mnt/boot/efi
fi

# TODO mount differently depending on whether it's BTRFS or EXT4
# The code below returns too much.
# sudo blkid /dev/mapper/crypt_priv_systems | grep -Eo 'TYPE="(.*)"'

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
