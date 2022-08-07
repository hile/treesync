"""
Pytest configuration for all tests
"""

import os
from pathlib import Path

import pytest

from treesync.constants import DEFAULT_CONFIGURATION_PATHS

TEST_DATA = Path(__file__).parent.joinpath('mock')

EXCLUDES_FILE = TEST_DATA.joinpath('rsync.exclude')
EXCLUDES_CONFIG = TEST_DATA.joinpath('excludes.yml')

# Configuration file with hosts and sources
HOST_SOURCES_CONFIG = TEST_DATA.joinpath('host_sources.yml')

SERVERS_TARGET_NAME = 'dummy'
VALID_TARGET_NAME = 'minimal'
INVALID_TARGET_NAME = 'no-such-target'
VALID_HOST_NAME = 'server1'
UNEXPECTED_HOST_NAME = 'no-such-host'

# These constants match data in HOST_SOURCES_CONFIG file
EXPECTED_HOSTS_COUNT = 3
EXPECTED_SOURCES_COUNT = 2

# test configuration files for old configuration sections
OLD_FORMAT_ICONV_CONFIG = TEST_DATA.joinpath('old_format_iconv_flags.yml')
OLD_FORMAT_MINIMAL_CONFIG = TEST_DATA.joinpath('old_format_minimal.yml')
OLD_FORMAT_SERVER_FLAGS_CONFIG = TEST_DATA.joinpath('old_format_servers.yml')


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv):
    """
    Wrap cli_mock_argv to be used in all tests
    """
    print('mock CLI argv', cli_mock_argv)


@pytest.fixture
def mock_no_user_sync_config():
    """
    Mock user configuration path
    """

    def exists(self):
        if self in DEFAULT_CONFIGURATION_PATHS:
            return False
        return os.path.exists(str(self))

    def is_file(self):
        if self in DEFAULT_CONFIGURATION_PATHS:
            return False
        return os.path.isfile(str(self))

    # pylint: disable=import-outside-toplevel
    from _pytest.monkeypatch import MonkeyPatch
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(Path, 'exists', exists)
    monkeypatch.setattr(Path, 'is_file', is_file)

    yield monkeypatch
    monkeypatch.undo()


@pytest.fixture
def mock_config_old_format_minimal(monkeypatch):
    """
    Mock a treesync setup using the OLD_FORMAT_MINIMAL_CONFIG configuration file
    """
    monkeypatch.setattr('treesync.configuration.loader.DEFAULT_CONFIGURATION_PATHS', [OLD_FORMAT_MINIMAL_CONFIG])
    return OLD_FORMAT_MINIMAL_CONFIG


@pytest.fixture
def mock_config_old_format_server_flags(monkeypatch):
    """
    Mock a treesync setup using the OLD_FORMAT_SERVER_FLAGS_CONFIG configuration file
    """
    monkeypatch.setattr('treesync.configuration.loader.DEFAULT_CONFIGURATION_PATHS', [OLD_FORMAT_SERVER_FLAGS_CONFIG])
    return OLD_FORMAT_SERVER_FLAGS_CONFIG


@pytest.fixture
def mock_config_host_sources(monkeypatch):
    """
    Mock a treesync setup using the HOST_SOURCES_CONFIG configuration file
    """
    monkeypatch.setattr('treesync.configuration.loader.DEFAULT_CONFIGURATION_PATHS', [HOST_SOURCES_CONFIG])
    return HOST_SOURCES_CONFIG
