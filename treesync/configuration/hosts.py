"""
Hosts configuration section for treesync
"""
from typing import List, Optional

from sys_toolkit.configuration.base import ConfigurationSection, ConfigurationList

from ..exceptions import ConfigurationError
from ..host import Hosts

from .defaults import HOST_CONFIGURATION_DEFAULTS
from .targets import Target, TargetConfiguration


class HostTargetConfiguration(TargetConfiguration):
    """
    Configuration section for a single host sync target
    """
    def __repr__(self):
        return self.source

    @property
    def __host_config__(self):
        """
        Return parent host configuration item
        """
        return self.__parent__.__host_config__

    @property
    def __sources_config__(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member

    @property
    def hostname(self):
        """
        Name of host
        """
        return self.__host_config__.name

    @property
    def name(self):
        """
        Look up source name for this host target
        """
        source_config = self.__sources_config__.get_source_config(self.source)
        if not source_config:
            raise ConfigurationError(
                f'host {self.hostname} target {self} source does is not defined: {self.source}'
            )
        return f'{self.hostname}:{source_config.name}'

    @property
    def source_path(self):
        """
        Look up source path for this host target
        """
        source_config = self.__sources_config__.get_source_config(self.source)
        if not source_config:
            raise ConfigurationError(
                f'host {self.hostname} target {self} source does is not defined: {self.source}'
            )
        return source_config.path


class HostTargetList(ConfigurationList):
    """
    List of host sync target configurations
    """
    __name__ = 'targets'
    __dict_loader_class__ = HostTargetConfiguration

    @property
    def __host_config__(self) -> 'HostConfiguration':
        """
        Return parent host configuration item
        """
        return self.__parent__

    @property
    def __sources_config__(self):
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
    def __sources_config__(self):
        """
        Return sources configuration section
        """
        return self.__config_root__.sources  # pylint:disable=no-member

    @property
    def sync_targets(self):
        """
        Return sync targets for host
        """
        targets = []
        for target_config in self.targets:
            targets.append(
                Target(
                    target_config.name,
                    target_config.source_path,
                    target_config.destination,
                    target_config
                )
            )
        return targets


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
    def __sources_config__(self):
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
