
Treesync rsync wrapper
======================

This repository contains a wrapper for rsync to pull and push trees between computers
using rsync with well known flags.

The command does nothing fancy, just takes out the burden of ensuring repeated flags
to 'rsync tree to other host' and 'rsync local copy of tree from other host' commands
are not messed up somehow on command line.

Installing
----------

This command can be installed currently only from github, not pip:

    pip install git+https://github.com/hile/treesync.git#egg=treesync

Commands
--------

    treesync list

        Lists configured sync targets

    treesync pull <target>

        Pulls changes in named target from dest to src

    treesync push <target>

        Pushes changes in named target from src to dest

Debug and quiet flags
---------------------

Flags `--debug` and `--quiet` can be specified before command to be run (pull/push).

The 'pull' and 'push' target argument is name of the configured tree. These commands also accept
flag '--dry-run' to avoid making changes.

By default 'pull' and 'push print rsync command output to screen. This can be avoided with '--quiet' flag.
If '--debug' is given, the rsync command to be executed is also printed unless '--quiet' is set.

Configuration
-------------

You can see file for configuration appropriate for your OS by running following command:

    treesync --debug list

Configuration file is yaml and contains dictionaries for each sync target.

Example:

    code:
        src: /Volumes/Code/
        dest: other:/code/
        flags:
        - '--delete'
        - '-av'
        - '--exclude-from=/Volumes/Code/hile/.rsync.exclude'

    music:
        src: /Volumes/Music
        dest: mediaserver:/music/m4a
        flags:
        - '--delete'
        - '-av'
        - '--exclude-from=/Volumes/Music/.rsync.exclude'
        - '--iconv=UTF-8-MAC,UTF-8'
