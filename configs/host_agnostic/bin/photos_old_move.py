#!/usr/bin/python3
"""
Move old photos to a different dir.
"""

# TODO have bindings for all devices
# HOST_TO_DIRS = {}

import argparse
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser(
        description='Move photos and videos older than a given date from source to destination directory.'
    )
    parser.add_argument('cutoff', help='Cutoff date in the format YYYYMMDD. Files with names earlier than this will be moved.')
    parser.add_argument('src', help='Source directory containing media files.')
    parser.add_argument('dest', help='Destination directory to move the older files into.')
    parser.add_argument('--dry-run', action='store_true', help='List files that would be moved without actually moving them.')

    args = parser.parse_args()

    cutoff = args.cutoff
    src = Path(args.src)
    dest = Path(args.dest)

    if not src.is_dir():
        print(f"Source directory '{src}' does not exist or is not a directory.")
        return
    if not dest.exists():
        dest.mkdir(parents=True)

    older = sorted([
        p for p in src.iterdir()
        if (p.suffix.lower() in ('.mp4', '.jpg', '.xmp')) and p.name < cutoff
    ])

    print(f"Moving files to {dest} ...")
    for older_media_file in older:
        file_move_message = f"Moving {older_media_file}..."
        if args.dry_run:
            file_move_message = f"DRY RUN! {file_move_message}"

        print(file_move_message)
        if not args.dry_run:
            shutil.move(older_media_file, dest)


if __name__ == '__main__':
    main()
