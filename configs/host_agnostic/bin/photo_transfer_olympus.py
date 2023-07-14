# TODO check
# - configs/host_agnostic/bin/ostatnia_fota weź to, tylko dodaj parametryzację
# configs/host_agnostic/bin/phone_media_transfer.py

# sudo mount /dev/disk/by-id/usb-OLYMPUS_E-P7_BJKA03472-0:0 ~/urządzenia/olympus_filesystem
# can be automounted already?

# Implementation: Get last photo, take the ones alphabetically further, until the first one that's already downloaded
# (with check exists name - not the hash, we might have a newer hash.
# Or just do the rename immediately.

import sys
import shutil
from pathlib import Path
from typing import Generator

OLYMPUS_MEDIA_DEST_DIR = Path("~/zdjęcia_i_filmiki/olympus_photos/").expanduser()
OLYMPUS_MEDIA_SOURCE_DIR = Path("/run/media/butla/54C9-B006/DCIM/100OLYMP")


# TODO this won't work. I should change the file names to be timestamps (up to hundreth's of a second for uniqueness?).
# It's hard to figure out the new photos because of old names repeating. I'll have to remove older photos from the camera,
# so they don't loop.
def sync_olympus_media():
    if not OLYMPUS_MEDIA_SOURCE_DIR.exists():
        sys.exit(f"Looks like the camera isn't mounted - there's no {OLYMPUS_MEDIA_SOURCE_DIR}")

    last_synced_media = _get_last_synced_media_name()
    print("Syncing media newer than", OLYMPUS_MEDIA_SOURCE_DIR / last_synced_media)

    synced_media_counter = 0
    for media in _get_newer_camera_media_than(last_synced_media):
        if OLYMPUS_MEDIA_DEST_DIR.with_name(media.name).exists():
            print("Found", media.name, "in the destination folder. Ending the sync.")
            break
        print('dry run:', media)
        # shutil.copy(media, OLYMPUS_MEDIA_DEST_DIR)
        synced_media_counter += 1
    print("Synced", synced_media_counter, "media files.")
    if synced_media_counter > 0:
        print("Last synced file:", media)


def _get_last_synced_media_name() -> str:
    last_media_file = OLYMPUS_MEDIA_DEST_DIR / "last_pulled_media.txt"
    return last_media_file.read_text().splitlines()[0].strip()


def _get_newer_camera_media_than(start_name: str) -> Generator[Path, None, None]:
    all_source_media = OLYMPUS_MEDIA_SOURCE_DIR.iterdir()

    def reject_older_names():
        for media in all_source_media:
            if media.name > start_name:
                return
        # while media := next(all_source_media):
        #     if media.name > start_name:
        #         return
    reject_older_names()

    for media in all_source_media:
        yield media


if __name__ == "__main__":
    sync_olympus_media()
