"""
Unit tests for 'treesync list' command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args
from treesync.bin.treesync.main import Treesync

from ..conftest import SERVERS_TARGET_NAME

EXPECTED_OUTPUT_LINES_VALID_TARGET = 8
EXPECTED_OUTPUT_LINES_ALL_TARGETS = 24


# pylint: disable=unused-argument
def test_cli_treesync_show_no_targets(mock_no_user_sync_config, capsys, monkeypatch):
    """
    Test running 'treesync show' without specifying a target and with no targets to show
    """
    script = Treesync()
    testargs = ['treesync', 'show']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


# pylint: disable=unused-argument
def test_cli_treesync_show_no_arguments(mock_config_old_format_server_flags, capsys, monkeypatch):
    """
    Test running 'treesync show' without specifying a target, listing all default targets
    """
    script = Treesync()
    testargs = ['treesync', 'show']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) == EXPECTED_OUTPUT_LINES_ALL_TARGETS


# pylint: disable=unused-argument
def test_cli_treesync_show_valid_target(mock_config_old_format_server_flags, capsys, monkeypatch):
    """
    Test running 'treesync show' with a single valid target name
    """
    script = Treesync()
    testargs = ['treesync', 'show', SERVERS_TARGET_NAME]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) == EXPECTED_OUTPUT_LINES_VALID_TARGET