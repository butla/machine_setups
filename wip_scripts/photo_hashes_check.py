from pathlib import Path
from pprint import pprint as p

photo_paths = Path("~/note_10_camera").expanduser().glob("*.mp4")
p(len(list(photo_paths)))

media_file_to_hash = {}
