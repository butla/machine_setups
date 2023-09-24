1. Make both drives into LUKS containers
```
sudo cryptsetup luksFormat /dev/sda
sudo cryptsetup luksFormat /dev/sdb
```
2. Mount LUKS containers
```
sudo cryptsetup open /dev/sda crypt_data_1
sudo cryptsetup open /dev/sdb crypt_data_2
```
3. Format LUKS containers into one BTRFS volume.
```
sudo mkfs.btrfs -d raid0 /dev/mapper/crypt_data_1 /dev/mapper/crypt_data_2
```
4. Mount the BTRFS volume
```
sudo mount -t btrfs /dev/mapper/crypt_data_1 ~/data
```
