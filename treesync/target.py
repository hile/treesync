"""
Tree sync target
"""

import os
import pathlib
import sys
import typing

from tempfile import NamedTemporaryFile
from subprocess import run, CalledProcessError

from sys_toolkit.textfile import LineTextFile

from .exceptions import SyncError

if typing.TYPE_CHECKING:  # pragma: no cover
    from treesync.configuration.targets import TargetConfiguration


class ExcludesFile(pathlib.Path):
    """
    Rsync excludes parser
    """
    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    @property
    def excludes(self):
        """
        Return excludes file items
        """
        if self.is_file():
            return list(LineTextFile(self))
        return []


# pylint: disable=too-few-public-methods
class TemporaryExcludesFile:
    """
    A temporary excludes file, merging excludes flags from various
    sources for rsync
    """
    def __init__(self, target):
        self.target = target
        # pylint: disable=consider-using-with
        self.__tempfile__ = NamedTemporaryFile(mode='w', prefix=f'treesync-{self.target.name}')
        for line in self.target.excluded:
            self.__tempfile__.write(f'{line}\n')
        self.__tempfile__.flush()

    def __repr__(self):
        """
        Return path to temporary file
        """
        return self.__tempfile__.name


class Target:
    """
    Tree sync target
    """
    def __init__(self, name, source: str, destination: str, settings: 'TargetConfiguration'):
        self.name = name
        self.source = pathlib.Path(source)
        self.destination = destination
        self.settings = settings if settings else {}
        self.__excludes_file__ = None

    def __repr__(self):
        return self.name

    @property
    def default_settings(self):
        """
        Configuration section for target settings
        """
        return self.settings.__config_root__.defaults

    @property
    def excluded(self):
        """
        Return list of excluded filenames applicable to target
        """
        excluded = list(self.default_settings.never_sync_paths)
        if not self.settings.ignore_default_excludes:
            excluded.extend(self.default_settings.excluded_paths)
        if self.settings.excludes:
            excluded.extend(self.settings.excludes)
        if self.tree_excludes_file is not None:
            excluded.extend(self.tree_excludes_file.excludes)
        return sorted(set(excluded))

    @property
    def tree_excludes_file(self):
        """
        Return tree specific excludes file
        """
        path = self.settings.excludes_file
        if path:
            return ExcludesFile(
                self.source.joinpath(self.settings.excludes_file)
            )
        if self.default_settings.tree_excludes_file:
            return ExcludesFile(
                self.source.joinpath(self.default_settings.tree_excludes_file)
            )
        return None

    @property
    def excludes_file(self):
        """
        Return temporary excludes file for commands
        """
        if self.__excludes_file__ is None:
            self.__excludes_file__ = TemporaryExcludesFile(self)
        return self.__excludes_file__

    @property
    def flags(self):
        """
        Return list of rsync flags for commands
        """
        flags = []
        if not self.settings.ignore_default_excludes:
            flags.extend(list(self.default_settings.flags))
        for flag in self.settings.flags:
            if flag not in flags:
                flags.append(flag)
        for flag in self.settings.destination_server_flags:
            if flag not in flags:
                flags.append(flag)
        if not flags:
            raise ValueError(f'Target defines no rsync flags: {self}')
        if self.settings.iconv:
            flags.append(f'--iconv={self.settings.iconv}')
        flags.append(f'--exclude-from={self.excludes_file}')
        return flags

    def get_rsync_cmd_args(self, dry_run=False):
        """
        Return rsync command and arguments excluding source and destination
        """
        args = [self.default_settings.rsync_command] + self.flags
        if dry_run:
            args.append('--dry-run')
        return args

    def get_pull_command_args(self, dry_run=False):
        """
        Return 'pull' command arguments
        """
        args = self.get_rsync_cmd_args(dry_run=dry_run)
        args.extend([
            f'{self.destination.rstrip("/")}/',
            f'{str(self.source).rstrip("/")}/',
        ])
        return args

    def get_push_command_args(self, dry_run=False):
        """
        Return 'push' command arguments
        """
        args = self.get_rsync_cmd_args(dry_run=dry_run)
        args.extend([
            f'{str(self.source).rstrip("/")}/',
            f'{self.destination.rstrip("/")}/',
        ])
        return args

    @staticmethod
    def run_sync_command(*args):
        """
        Run rsync command
        """
        try:
            return run(
                args,
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True
            )
        except CalledProcessError as error:
            raise SyncError(error) from error

    def pull(self, dry_run=False):
        """
        Pull data from destination to source with rsync
        """
        self.run_sync_command(*self.get_pull_command_args(dry_run))

    def push(self, dry_run=False):
        """
        Push data from source to destination with rsync
        """
        if not self.source.is_dir():
            raise SyncError(f'Source directory does not exist: {self.source}')
        return self.run_sync_command(*self.get_push_command_args(dry_run))
