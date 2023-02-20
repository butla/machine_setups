Manjaro installation
====================

## Initial system install
- boot from live USB
- if there are invalid installs on some drives - wipe old boot info from EFI partitions and EFI vars (efibootmgr)
- prep partitions:
  - the EFI partition: 2GB (systemd-boot uses more space there)
  - LUKS partition with a btrfs partition inside (create with luks2?)
- run the Manjaro installer
- [when root partition is directly in LUKS]
  - select manual partitioning
  - choose an empty partition for root, edit it, format to BTRFS, select encryption
  - mount ESP to /boot/efi for now
- [when root partition is in LVM in LUKS]
  - select manual partitioning
  - when adding mountpoints always "keep" content so it doesn't try to format anything
  - mount ESP to /boot/efi for now
  - if calamares is unmounting the mounted partitions and can't install,
    `cd` into dirs the partitions are mounted to
    https://github.com/calamares/calamares/issues/1920#issuecomment-1101789100
- reboot

## System configuration after boot
- `mkdir -p ~/development`
- `git clone https://github.com/butla/machine_setups ~/development/machine_setups`
- `cd ~/development/machine_setups && ./run_setup_first_time.sh`
- pull `machine_setups` from Git and run `make setup_machine`
- follow `docs/switching_from_grub_to_systemd-boot.md`
