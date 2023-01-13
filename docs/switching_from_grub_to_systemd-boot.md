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
- sudo pacman -S systemd-kernel-maintenance (TODO: maybe use the kernel-install automation?)
- sudo pacman -Rn grub-btrfs grub-theme-manjaro grub
- reinstall the current kernels, so that their systemd-boot entries get generated, e.g. sudo pacman -S linux515 linux419

## Notes
- kernel cmdline (e.g. "root=/dev/mapper/priv_systems-manjaro rw rootflags=subvol=@ cryptdevice=UUID=5e1bd4b3-0260-42bf-9afb-aec5f29a31a9:crypt_priv_systems apparmor=1 security=apparmor udev.log_priority=3
") gets saved automagically, based on the current /proc/cmdline, probably
TODO
