import os.path
from pathlib import Path
import time

from machine_setup import shell


def test_creates_directories_when_needed(tmp_path: Path):
    file_path = tmp_path / "some_directory/another_level/the_file.txt"
    assert not file_path.parent.exists()
    file_contents = "blablabla"

    shell.ensure_file_contents(file_path, file_contents)

    assert file_path.exists()
    assert file_path.read_text() == file_contents


def test_when_directory_exists(tmp_path: Path):
    file_path = tmp_path / "the_file.txt"
    assert file_path.parent.exists()
    file_contents = "bleble"

    shell.ensure_file_contents(file_path, file_contents)

    assert file_path.exists()
    assert file_path.read_text() == file_contents


def test_when_the_file_exists(tmp_path: Path):
    file_path = tmp_path / "the_file.txt"
    file_path.write_text("the contents before")
    file_contents = "qwerttt"

    shell.ensure_file_contents(file_path, file_contents)

    assert file_path.read_text() == file_contents


def test_file_isnt_touched_if_theres_nothing_to_change(tmp_path: Path):
    file_path = tmp_path / "the_file.txt"
    file_contents = "the contents"
    file_path.write_text(file_contents)

    file_modification_time = os.path.getmtime(file_path)
    # this is needed so the test can fail
    time.sleep(0.01)

    shell.ensure_file_contents(file_path, file_contents)

    assert os.path.getmtime(file_path) == file_modification_time
