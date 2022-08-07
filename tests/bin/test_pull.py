"""
Unit tests for 'treesync pull' command
"""

import sys

from pathlib import Path

import pytest

from cli_toolkit.tests.script import validate_script_run_exception_with_args
from pathlib_tree.tree import Tree

from treesync.bin.treesync.main import Treesync

from ..conftest import TEST_DATA
from ..utils import create_source_directory

EXCLUDES_FILE = TEST_DATA.joinpath('rsync.exclude')


def test_cli_treesync_pull_no_targets(monkeypatch):
    """
    Test running 'treesync pull' without targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_treesync_pull_invalid_targets(monkeypatch):
    """
    Test running 'treesync push' with invalid targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull', 'invalid-target-name']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_push_pull_tmpdir(tmpdir, monkeypatch):
    """
    Test pull and push with tmpdir
    """
    source, destination, config_file = create_source_directory(tmpdir, EXCLUDES_FILE)

    assert source.exists()
    assert not destination.exists()

    Tree(destination.parent).create()
    script = Treesync()

    testargs = ['treesync', 'push', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        with pytest.raises(SystemExit) as exit_status:
            script.run()
        assert exit_status.value.code == 0
    assert Path(destination).exists()

    testargs = ['treesync', 'pull', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        with pytest.raises(SystemExit) as exit_status:
            script.run()
        assert exit_status.value.code == 0
