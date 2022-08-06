"""
Configuration defaults for hosts
"""
from sys_toolkit.configuration.base import ConfigurationSection
from pathlib_tree.tree import SKIPPED_PATHS

from ..constants import (
    DEFAULT_EXCLUDES,
    DEFAULT_EXCLUDES_FILE,
    DEFAULT_FLAGS,
    TREE_CONFIG_FILE
)


class Defaults(ConfigurationSection):
    """
    Tree sync default settings
    """
    __name__ = 'defaults'
    __default_settings__ = {
        'rsync_command': 'rsync',
        'flags': DEFAULT_FLAGS,
        'never_sync_paths': SKIPPED_PATHS,
        'excluded_paths': DEFAULT_EXCLUDES,
        'tree_config_file': TREE_CONFIG_FILE,
        'tree_excludes_file': DEFAULT_EXCLUDES_FILE,
    }
