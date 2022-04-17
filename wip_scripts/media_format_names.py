#!/usr/bin/env python3
"""
A script that renames media files based on its metadata (EXIF and such).
"""

from pathlib import Path


def to_samsung_photo_name(photo: Path):
    day, hour = photo.stem.split(' ')
    new_name = f"{day.replace('-', '')}_{hour.replace('.', '')}{photo.suffix}"
    return photo.with_name(new_name)


if __name__ == '__main__':
    for photo in Path('/home/butla/Dropbox/Camera Uploads/').iterdir():
        new_path = to_samsung_photo_name(photo)
        print(f'Renaming {photo} to {new_path}')
        photo.rename(new_path)


photo_paths = Path('~/note_10_camera').expanduser().glob('*.mp4')
p(len(list(photo_paths)))

media_file_to_hash = {

}

