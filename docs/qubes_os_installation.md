QubesOS installation
====================

Prep partitions:
- the EFI partition
- an ext4 boot partition (1024 MiB)
- LUKS partition with an ext4 partition inside

During setup:
- choose custom/advanced partitioning.
- Setup /boot/efi on the EFI partition.
- /boot on the boot partition.
- Decrypt the LUKS containers
- format the partition inside LUKS to btrfs, set it to "/" mountpoint

If the partition inside LUKS is BTRFS I get an error "You must create a new file system on root device" after
setting up the mount points, even if the file systems are empty.
Looks like the [setup might be bugged around BTRFS](https://groups.google.com/g/qubes-users/c/bN4KmHA5sxA?pli=1).
