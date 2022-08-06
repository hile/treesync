"""
Configuration section for treesync targets
"""


from sys_toolkit.configuration.base import ConfigurationSection

from ..target import Target


class TargetConfiguration(ConfigurationSection):
    """
    Loader for named targets in TargetSettings
    """
    source = ''
    destination = ''

    __default_settings__ = {
        'ignore_default_flags': False,
        'ignore_default_excludes': False,
        'excludes': [],
        'excludes_file': None,
        'flags': [],
        'iconv': None,
    }
    __required_settings__ = (
        'source',
        'destination',
    )

    @property
    def destination_server_settings(self):
        """
        Return settings for destination server
        """
        try:
            host, _path = str(self.destination).split(':', 1)
        except ValueError:
            return None
        return getattr(self.__config_root__.servers, host, None)  # pylint:disable=no-member

    @property
    def destination_server_flags(self):
        """
        Return flags specific to destination server
        """
        flags = []
        settings = self.destination_server_settings
        if settings is not None:
            server_flags = settings.get('flags', [])
            if server_flags:
                flags.extend(server_flags)
            iconv = settings.get('iconv', None)
            if iconv is not None:
                flags.append(f'--iconv={iconv}')
            rsync_path = settings.get('rsync_path', None)
            if rsync_path is not None:
                flags.append(f'--rsync-path={rsync_path}')
        return flags


class TargetsConfigurationSection(ConfigurationSection):
    """
    Tree sync targets by name
    """

    __name__ = 'targets'
    __dict_loader_class__ = TargetConfiguration

    @property
    def names(self):
        """
        Get configured target names
        """
        names = []
        for attr in vars(self):
            section = getattr(self, attr)
            if isinstance(section, self.__dict_loader_class__):
                names.append(attr)
        return names

    def __iter__(self):
        targets = [getattr(self, name) for name in self.names]
        return iter(targets)

    def get_target(self, name):
        """
        Get target by name
        """
        settings = getattr(self, name, None)
        if settings is None:
            raise ValueError(f'Invalid target name {name}')
        return Target(name, settings)
