#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for 'treesync' utility
"""
from pathlib import Path

#: Default paths to look for configuration files
DEFAULT_CONFIGURATION_PATHS = (
    Path('~/.config/treesync.yml').expanduser(),
)

SKIPPED_PATHS = [
    '.DocumentRevisions-V100',
    '.Spotlight-V100',
    '.TemporaryItems',
    '.Trashes',
    '.fseventsd',
    '.metadata_never_index',
    'TheVolumeSettingsFolder',
]

#: Filename in source directory automatically added as rsync exclude
DEFAULT_EXCLUDES_FILE = '.rsync.exclude'

MACOS_META_EXCLUDES = [
    '.fseventsd',
    '.Trashes',
    '.TemporaryItems',
    '.Spotlight-V100',
]
#: Default excluded filenames and directories
DEFAULT_EXCLUDES = [
    '.pytest_cache/',
    '__pycache__/',
    '*.egg-info/',
    '*.pyc',
    '.*.swp',
    '*~',
] + MACOS_META_EXCLUDES

#: Default flags for rsync
DEFAULT_FLAGS = [
    '--archive',
    '--delete',
    '--protect-args',
    '--verbose',
]

#: Tree specific automatically loaded configuration file in source tree
TREE_CONFIG_FILE = '.treesync.yml'
