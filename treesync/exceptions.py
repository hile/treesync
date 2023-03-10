#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Exceptions from treesync tool
"""


class ConfigurationError(Exception):
    """
    Exceptions caused by configuration file handling
    """


class SyncError(Exception):
    """
    Exceptions caused by rsync commands
    """
