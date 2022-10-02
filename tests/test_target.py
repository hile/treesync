"""
Unit tests for treesync.target module
"""
from typing import List, Optional

from treesync.configuration import Configuration
from treesync.target import Target

from .conftest import (
    EXPECTED_HOSTS_TOTAL_TARGETS_COUNT,
    EXPECTED_HOST_TARGET_FLAGS,
    VALID_HOST_NAME
)


def get_first_sync_target(hostname: str, sync_targets: List) -> Optional[Target]:
    """
    Get first sync target matching hostname
    """
    for target in sync_targets:
        if target.hostname == hostname:
            return target
    return None


# pylint: disable=unused-argument
def test_configuration_sync_targets_no_hosts(mock_no_user_sync_config):
    """
    Test sync targets list with no host targets
    """
    config = Configuration()
    assert isinstance(config.sync_targets, list)
    assert len(config.sync_targets) == 0


# pylint: disable=unused-argument
def test_configuration_sync_targets_list(mock_config_host_sources):
    """
    Test sync targets list with default host targets list
    """
    config = Configuration()
    assert isinstance(config.sync_targets, list)
    assert len(config.sync_targets) == EXPECTED_HOSTS_TOTAL_TARGETS_COUNT


# pylint: disable=unused-argument
def test_configuration_target_flags(mock_config_host_sources):
    """
    Test loading flags for sync target with flags
    """
    config = Configuration()
    target = get_first_sync_target(VALID_HOST_NAME, config.sync_targets)
    assert isinstance(target, Target)
    for flag in EXPECTED_HOST_TARGET_FLAGS:
        assert flag in target.flags
