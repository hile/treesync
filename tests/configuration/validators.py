"""
Object validation utility functions
"""
from pathlib import Path

from treesync.configuration.hosts import HostConfiguration, HostTargetList, HostTargetConfiguration
from treesync.configuration.sources import SourcesConfigurationSection, SourceConfiguration


def validate_target_configuration(target: HostTargetConfiguration) -> None:
    """
    Validate attributes of a target configuration object
    """
    assert isinstance(target, HostTargetConfiguration)
    assert isinstance(target.__repr__(), str)
    assert isinstance(target.__host_config__, HostConfiguration)
    assert isinstance(target.__sources_config__, SourcesConfigurationSection)


def validate_host_configuration(host: HostConfiguration) -> None:
    """
    Validate attributes of a host configuration item
    """
    assert isinstance(host, HostConfiguration)
    assert isinstance(host.__sources_config__, SourcesConfigurationSection)

    assert isinstance(host.__repr__(), str)

    assert isinstance(host.targets, HostTargetList)
    assert isinstance(host.targets.__host_config__, HostConfiguration)
    assert isinstance(host.targets.__sources_config__, SourcesConfigurationSection)
    assert isinstance(host.targets.__repr__(), str)
    for target in host.targets:
        validate_target_configuration(target)


def validate_source_configuration(source: SourceConfiguration) -> None:
    """
    Validate attributes of a source configuration item
    """
    assert isinstance(source, SourceConfiguration)
    assert isinstance(source.__repr__(), str)
    assert isinstance(source.name, str)
    assert isinstance(source.path, Path)
