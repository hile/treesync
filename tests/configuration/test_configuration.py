"""
Unit tests for treesync.configuration common loader methods
"""

import shutil
from pathlib import Path

import pytest

from pathlib_tree.tree import Tree, SKIPPED_PATHS
from treesync.configuration.sources import SourcesConfigurationSection
from treesync.configuration import Configuration
from treesync.constants import (
    DEFAULT_EXCLUDES,
    DEFAULT_FLAGS,
)
from treesync.target import ExcludesFile, Target, SyncError

from ..conftest import (
    EXCLUDES_FILE,
    EXCLUDES_CONFIG,
    EXPECTED_HOSTS_COUNT,
    EXPECTED_SOURCES_COUNT,
    EXPECTED_SYNC_TARGET_COUNT,
    HOST_SOURCES_CONFIG,
    OLD_FORMAT_ICONV_CONFIG,
    OLD_FORMAT_MINIMAL_CONFIG,
    OLD_FORMAT_SERVER_FLAGS_CONFIG,
    UNEXPECTED_HOST_NAME,
    VALID_HOST_NAME,
)
from ..utils import create_source_directory
from .validators import (
    validate_host_configuration,
    validate_source_configuration,
)


# pylint: disable=unused-argument
def test_configuration_empty(mock_no_user_sync_config) -> None:
    """
    Test loading empty sync configuration
    """
    config = Configuration()

    assert isinstance(config.__repr__(), str)

    assert config.defaults is not None

    # Ensure system / user paths are mocked out
    for path in config.__default_paths__:
        assert not path.exists()
        assert not path.is_file()

    sync_targets = config.sync_targets
    assert len(sync_targets) == 0


def test_configuration_hosts_properties() -> None:
    """
    Test properties of loaded minimal configuration file with hosts and sources sections
    """
    config = Configuration(HOST_SOURCES_CONFIG)
    assert isinstance(config.hosts.__sources_config__, SourcesConfigurationSection)

    assert len(config.hosts) == EXPECTED_HOSTS_COUNT
    assert config.hosts.get(UNEXPECTED_HOST_NAME) is None

    host = config.hosts.get(VALID_HOST_NAME)
    validate_host_configuration(host)
    assert host.server_config is None

    for host in config.hosts:  # pylint: disable=not-an-iterable
        validate_host_configuration(host)


def test_configuration_sources_properties() -> None:
    """
    Test properties of loaded minimal configuration file with hosts and sources sections
    """
    config = Configuration(HOST_SOURCES_CONFIG)
    assert len(config.sources) == EXPECTED_SOURCES_COUNT

    for source in config.sources:  # pylint: disable=not-an-iterable
        validate_source_configuration(source)


def test_configuration_old_format_minimal(mock_no_user_sync_config) -> None:
    """
    Tesst loading minimal old format test configuration
    """
    config = Configuration(OLD_FORMAT_MINIMAL_CONFIG)

    sync_targets = config.sync_targets
    assert len(sync_targets) == 1

    target = config.get_target('minimal')
    assert target.tree_excludes_file is None


def test_configuration_old_format_target_attributes_minimal(mock_no_user_sync_config) -> None:
    """
    Test basic attributes of minimal sync target
    """
    config = Configuration(OLD_FORMAT_MINIMAL_CONFIG)

    with pytest.raises(ValueError):
        config.get_target('default')

    target = config.get_target('minimal')
    assert isinstance(target, Target)
    assert target.default_settings == config.defaults

    assert target.__repr__() == target.name
    assert target.name == 'minimal'

    assert isinstance(target.settings.__repr__(), str)
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

    assert isinstance(target.source, Path)
    assert isinstance(target.destination, str)

    assert config.defaults.rsync_command in target.get_rsync_cmd_args()
    target_args = target.get_rsync_cmd_args()
    for flag in target.flags:
        assert flag in target_args


def test_configuration_old_format_target_attributes_excluded() -> None:
    """
    Test loading target with excluded attributes
    """
    config = Configuration(EXCLUDES_CONFIG)
    target = config.get_target('excludes')
    assert isinstance(target.settings.__repr__(), str)

    assert target.settings.ignore_default_flags is True
    assert target.settings.ignore_default_excludes is True

    assert isinstance(target.tree_excludes_file, ExcludesFile)

    expected_excludes = sorted(SKIPPED_PATHS + ['*.sqp', '*~'])
    # Never sync flags are always included
    assert target.excluded == expected_excludes

    with pytest.raises(ValueError):
        # pylint: disable=pointless-statement
        target.flags


def test_configuration_old_format_remote_server_config(mock_no_user_sync_config) -> None:
    """
    Test loading configuration with multiple servers and server specific flags
    """
    expected_target_count = 3
    config = Configuration(OLD_FORMAT_SERVER_FLAGS_CONFIG)
    assert len(config.targets.names) == expected_target_count

    # Check the __iter__ method as side effect
    targets = list(config.targets)
    assert len(targets) == expected_target_count

    no_flags_target = config.targets.get('data-remote')
    assert no_flags_target.settings.destination_server_settings is None
    assert no_flags_target.settings.destination_server_flags == []

    # Server with empty (but defined) configuration section settings
    dummy_target = config.targets.get('dummy')
    assert dummy_target.settings.destination_server_settings == {}
    assert dummy_target.settings.destination_server_flags == []

    # Server with iconv and rsync path flags
    flags_target = config.targets.get('data')
    assert flags_target.settings.destination_server_settings is not None
    expected_flags = [
        '--usermap=demo:dummy',
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


def test_configuration_old_format_sync_target_attributes_iconv() -> None:
    """
    Test loading target with excluded attributes
    """
    config = Configuration(OLD_FORMAT_ICONV_CONFIG)
    target = config.get_target('converted')

    assert target.settings.ignore_default_excludes is False
    assert target.settings.ignore_default_flags is True
    assert isinstance(target.settings.iconv, str)

    expected_flag = f'--iconv={target.settings.iconv}'
    assert expected_flag in target.flags


def test_configuration_old_format_sync_target_tmpdir(tmpdir) -> None:
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

    assert not Path(destination).exists()
    target.push()
    assert Path(destination).exists()
    target.pull()

    shutil.rmtree(source)
    with pytest.raises(SyncError):
        target.push()
    target.pull()


# pylint: disable=unused-argument
def test_host_configuration_sync_targets(mock_config_host_sources):
    """
    Test loading a host via configuration and listing
    """
    config = Configuration()
    host = config.hosts.get(VALID_HOST_NAME)
    assert len(host.sync_targets) == EXPECTED_SYNC_TARGET_COUNT
