"""
Unit tests for 'treesync list' command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args
from treesync.bin.treesync.main import Treesync

from ..conftest import (
    INVALID_TARGET_NAME,
    VALID_TARGET_NAME,
)


# pylint: disable=unused-argument
def test_cli_treesync_list_no_targets(mock_no_user_sync_config, capsys, monkeypatch):
    """
    Test running 'treesync list' without arguments
    """
    script = Treesync()
    testargs = ['treesync', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''


# pylint: disable=unused-argument
def test_cli_treesync_list_host_sources_targets_no_targets(mock_config_old_format_minimal, capsys, monkeypatch):
    """
    Test running 'treesync list' without arguments with the minimal old format configuration
    """
    script = Treesync()
    testargs = ['treesync', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    # Contains 'minimal' as only output line
    assert len(lines) == 1
    assert lines == [VALID_TARGET_NAME]


# pylint: disable=unused-argument
def test_cli_treesync_list_host_sources_targets_valid_target(mock_config_old_format_minimal, capsys, monkeypatch):
    """
    Test running 'treesync list' without arguments
    """
    script = Treesync()
    testargs = ['treesync', 'list', VALID_TARGET_NAME]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    # Contains 'minimal' as only output line
    assert len(lines) == 1
    assert lines == [VALID_TARGET_NAME]


# pylint: disable=unused-argument
def test_cli_treesync_list_host_sources_targets_invalid_target(mock_config_old_format_minimal, capsys, monkeypatch):
    """
    Test running 'treesync list' without arguments
    """
    script = Treesync()
    testargs = ['treesync', 'list', INVALID_TARGET_NAME]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    errors = captured.err.splitlines()
    assert len(errors) == 1

    lines = captured.out.splitlines()
    # Contains 'minimal' as only output line
    assert len(lines) == 1
    assert lines == [VALID_TARGET_NAME]
