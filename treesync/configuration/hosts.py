"""
Hosts configuration section for treesync
"""
from typing import List, Optional

from sys_toolkit.configuration.base import ConfigurationSection, ConfigurationList

from ..host import Hosts

from .defaults import HOST_CONFIGURATION_DEFAULTS


class HostTarget(ConfigurationSection):
    """
    Configuration section for a single host sync target
    """
    source: str = ''
    destination: str = ''
    __required_settings__ = (
        'source',
        'destination',
    )

    def __repr__(self):
        return self.source

    @property
    def host_config(self):
        """
        Return parent host configuration item
        """
        return self.__parent__.host_config

    @property
    def sources_config(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member


class HostTargetList(ConfigurationList):
    """
    List of host sync target configurations
    """
    __name__ = 'targets'
    __dict_loader_class__ = HostTarget

    @property
    def host_config(self) -> 'HostConfiguration':
        """
        Return parent host configuration item
        """
        return self.__parent__

    @property
    def sources_config(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member


class HostConfiguration(ConfigurationSection):
    """
    Configuration for a single host
    """
    name: str = ''
    rsync_path: Optional[str] = None
    iconv: Optional[str] = None
    flags: List[str] = []
    targets: List[HostTargetList] = []

    __section_loaders__ = (
        HostTargetList,
    )
    __default_settings__ = HOST_CONFIGURATION_DEFAULTS
    __required_settings__ = (
        'name',
    )

    def __repr__(self) -> str:
        return self.name

    @property
    def server_config(self) -> Optional[ConfigurationSection]:
        """
        Return host settings from old servers config section
        """
        config = self.__config_root__.servers  # pylint:disable=no-member
        return getattr(config, self.name, None)

    @property
    def sources_config(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member


class HostsSettings(ConfigurationList):
    """
    Configuration for target hosts
    """
    __name__ = 'hosts'
    __dict_loader_class__ = HostConfiguration

    def __init__(self, setting=None, data=None, parent=None):
        super().__init__(setting, data, parent)
        self.hosts = Hosts()

    @property
    def sources_config(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member

    def get(self, name: str) -> Optional[HostConfiguration]:
        """
        Get specified host by name
        """
        for host in self:
            if host.name == name:
                return host
        return None
