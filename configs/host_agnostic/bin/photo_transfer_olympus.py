# TODO check
# - configs/host_agnostic/bin/ostatnia_fota weź to, tylko dodaj parametryzację
# configs/host_agnostic/bin/phone_media_transfer.py

# sudo mount /dev/disk/by-id/usb-OLYMPUS_E-P7_BJKA03472-0:0 ~/urządzenia/olympus_filesystem
# can be automounted already?

# Implementation: Get last photo, take the ones alphabetically further, until the first one that's already downloaded
# (with check exists name - not the hash, we might have a newer hash.
# Or just do the rename immediately.
