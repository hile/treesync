
from systematic.shell import Script

from ..configuration import DEFAULT_CONFIG_PATH
from .commands.list import ListCommand
from .commands.pull import PullCommand
from .commands.push import PushCommand


def main():
    script = Script()

    script.add_argument('-d', '--debug', action='store_true', help='Show debug messages')
    script.add_argument('-q', '--quiet', action='store_true', help='Do not show any messages')
    script.add_argument('-c', '--config', default=DEFAULT_CONFIG_PATH, help='Path to configuration file')
    script.add_subcommand(ListCommand())
    script.add_subcommand(PullCommand())
    script.add_subcommand(PushCommand())

    script.run()
