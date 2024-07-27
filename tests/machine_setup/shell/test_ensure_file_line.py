from pathlib import Path

import pytest

from machine_setup import shell


@pytest.fixture
def file_path(tmp_path: Path) -> Path:
    path = tmp_path / "blabla"
    assert not path.exists()
    return path


def test_works_on_nonexisting_file(file_path: Path):
    line_to_ensure = "blabla"
    line_matcher = line_to_ensure
    expected_file_contents = line_to_ensure

    shell.ensure_file_line(path=file_path, line_matcher=line_matcher, line_content=line_to_ensure)

    assert file_path.read_text() == expected_file_contents


def test_works_on_nonexistent_file_in_nonexistent_directories(tmp_path):
    path = tmp_path / "level_1" / "level_2" / "file_name"
    line_to_ensure = "flamingo"

    shell.ensure_file_line(path=path, line_matcher="whatever", line_content=line_to_ensure)

    assert path.read_text() == line_to_ensure


def test_works_on_existing_file_when_matcher_matches(file_path: Path):
    file_contents = """
xxxxxxxx
yyy = banana
zzzzzzzz
"""
    file_path.write_text(file_contents)
    line_to_ensure = "yyy = squirrel"
    line_matcher = r"yyy.*"

    shell.ensure_file_line(path=file_path, line_matcher=line_matcher, line_content=line_to_ensure)

    expected_file_contents = """
xxxxxxxx
yyy = squirrel
zzzzzzzz
"""
    assert file_path.read_text() == expected_file_contents


def test_works_on_existing_file_when_matcher_doesnt_match(file_path):
    file_contents = """
xxxxxxxx
zzzzzzzz
"""
    file_path.write_text(file_contents)
    line_to_ensure = "yyy = squirrel"
    line_matcher = r"yyy.*"

    shell.ensure_file_line(path=file_path, line_matcher=line_matcher, line_content=line_to_ensure)

    expected_file_contents = """
xxxxxxxx
zzzzzzzz
yyy = squirrel
"""
    assert file_path.read_text() == expected_file_contents


def test_works_when_path_is_str(file_path):
    file_contents = """
xxxxxxxx
"""
    file_path.write_text(file_contents)
    line_to_ensure = "yyy = squirrel"
    line_matcher = r"xxx.*"

    shell.ensure_file_line(path=str(file_path), line_matcher=line_matcher, line_content=line_to_ensure)

    expected_file_contents = """
yyy = squirrel
"""
    assert file_path.read_text() == expected_file_contents
