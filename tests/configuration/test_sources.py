"""
Unit tests for treesync.configuration.sources module
"""

from treesync.configuration import Configuration
from treesync.configuration.sources import SourceConfiguration

from ..conftest import HOST_SOURCES_CONFIG, DUMMY_TARGET_NAME, INVALID_TARGET_NAME


# pylint: disable=unused-argument
def test_configuration_sources_get_source_invalid(mock_config_host_sources) -> None:
    """
    Test looking up a valid source by name
    """
    config = Configuration(HOST_SOURCES_CONFIG)
    assert config.sources.get(INVALID_TARGET_NAME) is None


# pylint: disable=unused-argument
def test_configuration_sources_get_source_valid(mock_config_host_sources) -> None:
    """
    Test looking up a valid source by name
    """
    config = Configuration(HOST_SOURCES_CONFIG)
    source = config.sources.get(DUMMY_TARGET_NAME)
    assert isinstance(source, SourceConfiguration)
