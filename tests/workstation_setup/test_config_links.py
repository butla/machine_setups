import os
from pathlib import Path

import pytest

from machine_setup.config_links import BACKUP_SUFFIX, set_up_links


@pytest.fixture
def source_dir(tmp_path: Path):
    path = tmp_path / 'source'
    path.mkdir()
    return path


@pytest.fixture
def target_dir(tmp_path: Path):
    path = tmp_path / 'target'
    path.mkdir()
    return path


def test_setup_links_creates_the_correct_links(source_dir: Path, target_dir: Path):
    # arrange
    # ===========
    source_file_that_should_have_links = [
        'aaa.py',
        'a_dir/bbb.py',
        'b_dir/c_dir/ccc.conf',
        'b_dir/c_dir/ddd',
    ]
    source_files_that_should_not_have_links = [
        'tests/eee.py',
        'd_dir/tests/fff.py',
    ]

    # create the source files
    for path_str in source_file_that_should_have_links + source_files_that_should_not_have_links:
        path = Path(source_dir) / path_str
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    # create a multi-level empty dir to make sure that it doesn't mess anything up
    (Path(source_dir) / 'e_dir/f_dir/g_dir').mkdir(parents=True)

    # act
    # ===========
    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    # assert
    # ===========
    target_dir_expected_dirs = {
        Path(target_dir) / 'a_dir',
        Path(target_dir) / 'b_dir',
        Path(target_dir) / 'b_dir/c_dir',
    }
    target_dir_expected_files = {Path(target_dir) / file for file in source_file_that_should_have_links}
    target_dir_contents = set(target_dir.glob('**/*'))

    # assert we have the expected folders and links created
    assert target_dir_contents == target_dir_expected_dirs | target_dir_expected_files

    # assert the created links have expected targets
    expected_link_targets = {str(Path(source_dir) / file) for file in source_file_that_should_have_links}
    created_links_targets = {os.readlink(item) for item in target_dir_contents if item.is_symlink()}
    assert created_links_targets == expected_link_targets


def test_setup_links_backs_up_and_replaces_existing_files(source_dir: Path, target_dir: Path):
    source_file_content = 'Just some file content'
    source_file = source_dir / 'bla/whatever.py'
    source_file.parent.mkdir(parents=True)
    source_file.write_text(source_file_content)

    old_system_file_content = "I'm the old thing"
    old_system_file = target_dir / 'bla/whatever.py'
    old_system_file.parent.mkdir(parents=True)
    old_system_file.write_text(old_system_file_content)

    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert old_system_file.with_name(f'whatever.py{BACKUP_SUFFIX}').read_text() == old_system_file_content


def test_setup_links_backs_up_and_replaces_existing_links(source_dir: Path, target_dir: Path, tmp_path: Path):
    source_file_name = 'bla'
    source_file = source_dir / source_file_name
    source_file.touch()

    old_link_target = tmp_path / 'old_link_target'
    old_link_target.touch()

    created_link_path = Path(target_dir / source_file_name)
    # Creating a link pointing to an existing file. This link should get backed up and replaced.
    created_link_path.symlink_to(old_link_target)

    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert os.readlink(created_link_path) == str(source_file)

    backed_up_link = created_link_path.with_suffix(BACKUP_SUFFIX)
    assert backed_up_link.exists()
    assert os.readlink(backed_up_link) == str(old_link_target)


def test_setup_links_replaces_broken_symlinks_without_backing_them_up(
        source_dir: Path,
        target_dir: Path,
        tmp_path: Path,
):
    source_file_name = 'bla'
    source_file = source_dir / source_file_name
    source_file.touch()

    created_link_path = Path(target_dir / source_file_name)
    # Creating a link pointing to a file that doesn't exist. The link should get replaced.
    created_link_path.symlink_to(tmp_path / "I_dont_exist")

    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert list(target_dir.glob('**/*')) == [created_link_path]
    assert os.readlink(created_link_path) == str(source_file)


def test_second_pass_of_setup_links_doesnt_change_anything(source_dir, target_dir):
    source_file = source_dir / 'aaa'
    source_file.write_text('some content')

    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    expected_link = target_dir / 'aaa'
    expected_target_dir_contents = [expected_link]
    assert list(target_dir.glob('**/*')) == expected_target_dir_contents
    assert os.readlink(expected_link) == str(source_file)

    # run again
    set_up_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert list(target_dir.glob('**/*')) == expected_target_dir_contents
    assert os.readlink(expected_link) == str(source_file)
