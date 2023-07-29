Switching from GRUB to systemd-boot
===================================

Based on [this article](https://forum.manjaro.org/t/how-to-convert-to-systemd-boot/128946).

## Procedure
- boot into the system, don't chroot
- make sure /etc/mkinitcpio.conf FILES doesn't contain the key to the LUKS partition
- sudo cryptsetup luksRemoveKey <luks partition> /crypto_keyfile.bin
- sudo rm /crypto_keyfile.bin
- fixup crypttab - set "none" instead of crypto_keyfile
- unmount ESP
- unmount /boot partition or remove /boot folder (back it up first)
- sudo mkdir /efi (following the [mountpoint recommendation from systemd author](https://github.com/systemd/systemd/pull/3757#issuecomment-234290236))
- fixup fstab: change ESP to /efi, don't mount /boot
- mount ESP to /efi
- sudo bootctl install
- sudo pacman -S systemd-kernel-maintenance
  - looks like the above may be buggy. `pamac build kernel-install-mkinitcpio` seems to work well.
    [More info](https://forum.manjaro.org/t/systemd-kernel-maintenance-stopped-producing-initrd-after-2023-06-04-update/145257)
- sudo pacman -Rn grub-btrfs grub-theme-manjaro grub
- reinstall the current kernels, so that their systemd-boot entries get generated, e.g. sudo pacman -S linux515 linux419
- make sure /etc/kernel/cmdline is fine, e.g.
  `root=/dev/mapper/crypt_priv_systems rw rootflags=subvol=@ cryptdevice=UUID=<uuid>:crypt_priv_systems apparmor=1 security=apparmor udev.log_priority=3`
- remove /efi/EFI/Manjaro
- copy files_to_copy/common/efi/loader/loader.conf to /efi/loader/loader.conf

## Notes
- kernel cmdline gets saved automagically, based on the current /proc/cmdline, probably
