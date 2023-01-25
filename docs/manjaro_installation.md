Manjaro installation
====================

- prep partitions:
  - the EFI partition
  - LUKS partition with a btrfs partition inside
  - an ext4 boot partition (1024 MiB)
- mount partitions
- run the Manjaro installer
- manual partitioning
- [if calamares is unmounting the mounted partitions and can't install],
  [`cd` into dirs the partitions are mounted to](https://github.com/calamares/calamares/issues/1920#issuecomment-1101789100)
- TODO:
  - don't have a boot partition, chroot into the thing to setup systemd-boot?
    - maybe this needs a bind mount of /etc/resolv.conf
  - setup GRUB and kernel cmdline so we don't need a separate boot partition. Then boot into it and setup systemd-boot?
