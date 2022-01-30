"""
Unit tests for 'treesync list' command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args
from treesync.bin.treesync.main import Treesync


def test_cli_treesync_list_no_targets(monkeypatch):
    """
    Test running 'treesync list' without arguments
    """
    script = Treesync()
    testargs = ['treesync', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
