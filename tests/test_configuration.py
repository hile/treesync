"""
Test cases for pathlib_tree.sync.configuration classes
"""

import pathlib
import shutil

import pytest

from pathlib_tree.tree import Tree, SKIPPED_PATHS
from treesync.configuration import Configuration
from treesync.constants import (
    DEFAULT_EXCLUDES,
    DEFAULT_FLAGS,
)
from treesync.target import ExcludesFile, Target, SyncError

from . import TEST_DATA
from .utils import create_source_directory

EXCLUDES_FILE = TEST_DATA.joinpath('rsync.exclude')
EXCLUDES_CONFIG = TEST_DATA.joinpath('excludes.yml')
ICONV_CONFIG = TEST_DATA.joinpath('iconv.yml')
MINIMAL_CONFIG = TEST_DATA.joinpath('minimal.yml')
SERVER_FLAGS_CONFIG = TEST_DATA.joinpath('servers.yml')


def test_sync_configuration_empty():
    """
    Test loading empty sync configuration
    """
    config = Configuration()

    assert isinstance(config.__repr__(), str)

    # pylint: disable=no-member
    assert config.defaults is not None

    # Ensure system / user paths are mocked out
    for path in config.__default_paths__:
        assert not path.exists()
        assert not path.is_file()

    # pylint: disable=no-member
    sync_targets = config.sync_targets
    assert len(sync_targets) == 0


def test_sync_configuration_minimal():
    """
    Tesst loading minimal.yml test configuration
    """
    config = Configuration(MINIMAL_CONFIG)

    # pylint: disable=no-member
    sync_targets = config.sync_targets
    assert len(sync_targets) == 1

    target = config.get_target('minimal')
    assert target.tree_excludes_file is None


def test_sync_target_attributes_minimal():
    """
    Test basic attributes of minimal sync target
    """
    config = Configuration(MINIMAL_CONFIG)

    with pytest.raises(ValueError):
        config.get_target('default')

    target = config.get_target('minimal')
    assert isinstance(target, Target)
    # pylint: disable=no-member
    assert target.default_settings == config.defaults

    assert target.__repr__() == target.name
    assert target.name == 'minimal'

    assert target.settings.ignore_default_flags is False
    assert target.settings.ignore_default_excludes is False
    assert target.settings.excludes_file is None
    assert target.settings.iconv is None
    assert target.settings.excludes.__values__ == []
    assert target.settings.flags.__values__ == []

    expected_excludes = SKIPPED_PATHS + DEFAULT_EXCLUDES
    assert target.excluded == sorted(set(expected_excludes))

    for flag in DEFAULT_FLAGS:
        assert flag in target.flags

    assert isinstance(target.source, pathlib.Path)
    assert isinstance(target.destination, str)

    # pylint: disable=no-member
    assert config.defaults.rsync_command in target.get_rsync_cmd_args()
    target_args = target.get_rsync_cmd_args()
    for flag in target.flags:
        assert flag in target_args


def test_sync_target_attributes_excluded():
    """
    Test loading target with excluded attributes
    """
    config = Configuration(EXCLUDES_CONFIG)
    target = config.get_target('excludes')

    assert target.settings.ignore_default_flags is True
    assert target.settings.ignore_default_excludes is True

    assert isinstance(target.tree_excludes_file, ExcludesFile)

    expected_excludes = sorted(SKIPPED_PATHS + ['*.sqp', '*~'])
    # Never sync flags are always included
    assert target.excluded == expected_excludes

    with pytest.raises(ValueError):
        # pylint: disable=pointless-statement
        target.flags


def test_sync_configuration_remote_servers():
    """
    Test loading configuration with multiple servers and server specific flags
    """
    expected_target_count = 3
    config = Configuration(SERVER_FLAGS_CONFIG)
    # pylint: disable=no-member
    assert len(config.targets.names) == expected_target_count

    # Check the __iter__ method as side effect
    # pylint: disable=no-member
    targets = list(config.targets)
    assert len(targets) == expected_target_count

    # pylint: disable=no-member
    no_flags_target = config.targets.get_target('data-remote')
    assert no_flags_target.settings.destination_server_settings is None
    assert no_flags_target.settings.destination_server_flags == []

    # Server with empty (but defined) configuration section settings
    # pylint: disable=no-member
    dummy_target = config.targets.get_target('dummy')
    assert dummy_target.settings.destination_server_settings == {}
    assert dummy_target.settings.destination_server_flags == []

    # Server with iconv and rsync path flags
    # pylint: disable=no-member
    flags_target = config.targets.get_target('data')
    assert flags_target.settings.destination_server_settings is not None
    expected_flags = [
        '--iconv=UTF-8-MAC,UTF-8',
        '--rsync-path=/usr/local/bin/rsync'
    ]
    assert flags_target.settings.destination_server_flags == expected_flags

    # Target flags include expected flags and defaults
    target_flags = flags_target.flags
    for flag in expected_flags:
        assert flag in target_flags

    command = flags_target.get_rsync_cmd_args()
    assert '--dry-run' not in command

    command = flags_target.get_rsync_cmd_args(dry_run=True)
    assert '--dry-run' in command


def test_sync_target_attributes_iconv():
    """
    Test loading target with excluded attributes
    """
    config = Configuration(ICONV_CONFIG)
    target = config.get_target('converted')

    assert target.settings.ignore_default_excludes is False
    assert target.settings.ignore_default_flags is True
    assert isinstance(target.settings.iconv, str)

    expected_flag = f'--iconv={target.settings.iconv}'
    assert expected_flag in target.flags


def test_sync_target_tmpdir(tmpdir):
    """
    Test loading target for temporary directory
    """
    source, destination, config_file = create_source_directory(tmpdir, EXCLUDES_FILE)

    assert source.exists()
    assert not destination.exists()

    config = Configuration(config_file)
    target = config.get_target('test')
    assert target.source == source
    assert target.destination == str(destination)

    assert target.tree_excludes_file.exists()

    expected_excludes = ['.*.progress', '*.tmp']
    for value in expected_excludes:
        assert value in target.excluded

    Tree(destination.parent).create()

    assert not pathlib.Path(destination).exists()
    target.push()
    assert pathlib.Path(destination).exists()
    target.pull()

    shutil.rmtree(source)
    with pytest.raises(SyncError):
        target.push()
    target.pull()
