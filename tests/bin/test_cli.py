#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for 'treesync' command main class
"""
import pytest

from cli_toolkit.tests.script import validate_script_attributes

from treesync.bin.treesync.main import main, Treesync

DEFAULT_ARGS = {
    'debug': False,
    'quiet': False
}


def test_cli_treesync_run_main() -> None:
    """
    Run main() for treesync command without arguments
    """
    with pytest.raises(SystemExit):
        main()


def test_cli_treesync_attributes() -> None:
    """
    Validate basic attributes of treesync script
    """
    expected_args = DEFAULT_ARGS.copy()
    expected_args['test-cli_command'] = None
    validate_script_attributes(Treesync(), expected_args=expected_args)
