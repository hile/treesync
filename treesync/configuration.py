
import fnmatch
import os
import sys

import ruamel.yaml

from .tree import Tree


if sys.platform == 'darwin':
    DEFAULT_CONFIG_PATH = os.path.expanduser('~/Library/Application Support/treesync/treesync.yaml')
elif sys.platform[:5] == 'linux' or fnmatch.fnmatch(sys.platform, '*bsd*'):
    DEFAULT_CONFIG_PATH = os.path.expanduser('~/.config/treesync.conf')


class ConfigurationError(Exception):
    pass


class Configuration:
    """
    Tree sync command configuration file handling
    """

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.path = path
        self.trees = []
        self.debug = False
        self.quiet = False
        self.load()

    def load(self):
        """
        Load tree sync configuration file
        """
        self.trees = []
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'r') as fd:
                    yaml = ruamel.yaml.YAML()
                    data = yaml.load(fd)
                if data:
                    for name in data:
                        self.trees.append(Tree(
                            config=self,
                            name=name,
                            src=data[name]['src'],
                            dest=data[name]['dest'],
                            flags=data[name].get('flags', {})
                        ))
            except Exception as e:
                raise ConfigurationError('Error loading {}: {}'.format(self.path, e))

    def save(self):
        """
        Save configuration file
        """
        dirname = os.path.dirname(self.path)
        if not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except Exception as e:
                raise ConfigurationError('Error creating directory {}: {}'.format(dirname, e))
