#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for 'treesync pull' command
"""
import sys

from subprocess import CalledProcessError
from pathlib_tree.tree import Tree

import pytest

from cli_toolkit.tests.script import validate_script_run_exception_with_args
from sys_toolkit.tests.mock import MockException

from treesync.bin.treesync.main import Treesync

from ..conftest import TEST_DATA
from ..utils import create_source_directory

EXCLUDES_FILE = TEST_DATA.joinpath('rsync.exclude')


# pylint: disable=unused-argument
def test_cli_treesync_pull_no_targets(mock_no_user_sync_config, monkeypatch) -> None:
    """
    Test running 'treesync pull' without targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_cli_treesync_pull_invalid_targets(mock_no_user_sync_config, monkeypatch) -> None:
    """
    Test running 'treesync push' with invalid targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull', 'invalid-target-name']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_cli_push_pull_tmpdir(mock_no_user_sync_config, tmpdir, monkeypatch) -> None:
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
    assert destination.exists()

    testargs = ['treesync', 'pull', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        with pytest.raises(SystemExit) as exit_status:
            script.run()
        assert exit_status.value.code == 0


# pylint: disable=unused-argument
def test_cli_push_pull_tmpdir_error(mock_no_user_sync_config, tmpdir, monkeypatch) -> None:
    """
    Test pull and push with tmpdir and errors in running the commands
    """
    mock_called_process_error = MockException(CalledProcessError, cmd='mock command', returncode=1)
    monkeypatch.setattr('treesync.target.run', mock_called_process_error)
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
        assert exit_status.value.code == 1
    assert not destination.exists()

    testargs = ['treesync', 'pull', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        with pytest.raises(SystemExit) as exit_status:
            script.run()
        assert exit_status.value.code == 1
