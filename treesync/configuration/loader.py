"""
Configuration loader for treesync
"""
from typing import Optional

from sys_toolkit.configuration.yaml import YamlConfiguration

from ..constants import DEFAULT_CONFIGURATION_PATHS

from .defaults import Defaults
from .hosts import HostsSettings
from .servers import ServersConfigurationSection
from .sources import SourcesConfigurationSection
from .targets import TargetsConfigurationSection


class Configuration(YamlConfiguration):
    """
    Yaml configuration file for 'treesync' CLI
    """
    defaults: Optional[Defaults] = None
    hosts: Optional[HostsSettings] = None
    servers: Optional[ServersConfigurationSection] = None
    sources: Optional[SourcesConfigurationSection] = None
    targets: Optional[TargetsConfigurationSection] = None

    __default_paths__ = DEFAULT_CONFIGURATION_PATHS
    __section_loaders__ = (
        Defaults,
        HostsSettings,
        ServersConfigurationSection,
        SourcesConfigurationSection,
        TargetsConfigurationSection,
    )

    def __repr__(self):
        return 'treesync config'

    @property
    def sync_targets(self):
        """
        Get configured sync targets
        """
        targets = []
        # pylint: disable=no-member
        for name in self.targets.names:
            targets.append(self.get_target(name))
        return targets

    def get_target(self, name):
        """
        Get target by name
        """
        # pylint: disable=no-member
        return self.targets.get_target(name)
