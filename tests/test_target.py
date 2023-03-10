#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for treesync.target module
"""
from typing import List, Optional

from treesync.configuration import Configuration
from treesync.target import Target, TargetList

from .conftest import (
    EXPECTED_HOSTS_TOTAL_TARGETS_COUNT,
    EXPECTED_HOST_TARGET_FLAGS,
    HOST_TARGET_NAME,
    VALID_HOST_NAME,
    VALID_TARGET_NAME,
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
    assert isinstance(config.sync_targets, TargetList)
    assert len(config.sync_targets) == 0


# pylint: disable=unused-argument
def test_configuration_sync_targets_list(mock_config_host_sources):
    """
    Test sync targets list with default host targets list
    """
    config = Configuration()
    assert isinstance(config.sync_targets, TargetList)
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


def test_target_list_empty(mock_config_host_sources):
    """
    Test attributes of an empty target list object
    """
    obj = TargetList()
    obj.sort()
    assert len(obj) == 0
    assert list(obj) == []

    assert obj.get(VALID_TARGET_NAME) is None


# pylint: disable=unused-argument
def test_sync_targets_delete_and_set(mock_config_host_sources):
    """
    Test getting a target by name
    """
    config = Configuration()
    target = config.sync_targets[0]
    assert isinstance(target, Target)

    del config.sync_targets[0]
    assert len(config.sync_targets) == EXPECTED_HOSTS_TOTAL_TARGETS_COUNT - 1

    # This replaces item, not appends
    config.sync_targets[0] = target
    assert len(config.sync_targets) == EXPECTED_HOSTS_TOTAL_TARGETS_COUNT - 1


# pylint: disable=unused-argument
def test_sync_targets_get_target(mock_config_host_sources):
    """
    Test getting a target by name
    """
    config = Configuration()
    target = config.sync_targets.get(HOST_TARGET_NAME)
    assert isinstance(target, Target)
