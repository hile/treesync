#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for 'treesync push' command
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args
from treesync.bin.treesync.main import Treesync


def test_cli_treesync_push_no_targets(monkeypatch) -> None:
    """
    Test running 'treesync push' without targets
    """
    script = Treesync()
    testargs = ['treesync', 'push']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_treesync_push_invalid_targets(monkeypatch) -> None:
    """
    Test running 'treesync push' with invalid targets
    """
    script = Treesync()
    testargs = ['treesync', 'push', 'invalid-target-name']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)
