#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Utilities for treesync unit tests
"""
import pathlib
import shutil

from pathlib import Path

import yaml


def create_test_config(path, name, source, destination, **kwargs):
    """
    Create a test configuration file with one target
    """
    data = {
        name: {
            'source': str(source),
            'destination': str(destination)
        }
    }
    data[name].update(**kwargs)
    data = yaml.safe_dump({
        'targets': data
    })
    with open(path, 'w', encoding='utf-8') as filedescriptor:
        filedescriptor.write(f'{data}\n')


def create_source_directory(tmpdir, excludes_file=None):
    """
    Create temporary source directory for tests
    """
    source = pathlib.Path(tmpdir, 'src/path')
    destination = pathlib.Path(tmpdir, 'dst/path')
    config_file = pathlib.Path(tmpdir, 'test.yml')

    parent = Path(source.parent)
    if not parent.is_dir():
        parent.mkdir(parents=True)
    shutil.copytree(pathlib.Path(__file__).parent, source)

    if excludes_file is not None:
        tmpdir_excludes = pathlib.Path(source, excludes_file.name)
        shutil.copyfile(excludes_file, tmpdir_excludes)

    create_test_config(
        config_file,
        'test',
        source,
        destination,
        excludes_file=str(excludes_file.name)
    )

    return source, destination, config_file
