#!/usr/bin/env python3
"""
A script that renames media files based on its metadata (EXIF and such).
"""

from pathlib import Path
from pprint import pprint

import exif
import ffmpeg

# TODO have an AUR package? Set the dependencies, don't rely on Poetry.


# TODO make this a generator
def find_media_files(folder_to_search: Path):
    # day, hour = photo.stem.split(' ')
    # new_name = f"{day.replace('-', '')}_{hour.replace('.', '')}{photo.suffix}"
    # return photo.with_name(new_name)
    pass


def new_media_file_name(media_file: Path) -> Path:
    with media_file.open('rb') as file_stream:
        exif_info = exif.Image(file_stream)
    pprint(exif_info.list_all())
    # on mp4 files
    pprint(ffmpeg.probe(media_file)["streams"])


if __name__ == '__main__':
    for photo in Path('/home/butla/Dropbox/Camera Uploads/').iterdir():
        new_path = to_samsung_photo_name(photo)
        print(f'Renaming {photo} to {new_path}')
        photo.rename(new_path)


photo_paths = Path('~/note_10_camera').expanduser().glob('*.mp4')
p(len(list(photo_paths)))

media_file_to_hash = {

}

