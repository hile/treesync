#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for treesync.host module
"""
from treesync.host import Hosts, TargetHost

from .conftest import VALID_HOST_NAME


def test_target_host_attributes():
    """
    Test attributes of trivial TargetHost object
    """
    obj = TargetHost(VALID_HOST_NAME)
    assert isinstance(obj.__repr__(), str)


def test_hosts_object_attributes():
    """
    Test basic attributes of empty Hosts mapping object
    """
    hosts = Hosts()
    assert len(hosts) == 0


def test_hosts_get_create_delete():
    """
    Test getting non-existing named host entry from Hosts mapping

    The get() method will add new host to the mapping when no match exists
    """
    hosts = Hosts()

    host = hosts.get(VALID_HOST_NAME)
    assert isinstance(host, TargetHost)
    assert len(hosts) == 1

    other = hosts.get(VALID_HOST_NAME)
    assert other.__hash__() == host.__hash__()
    assert len(hosts) == 1

    for item in hosts:
        assert isinstance(item, str)
    for item in hosts.values():
        assert isinstance(item, TargetHost)

    del hosts[host.name]
    assert len(hosts) == 0
