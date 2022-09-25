"""
Treesync 'list' subcommand
"""

from .base import TreesyncCommand


class List(TreesyncCommand):
    """
    Tree pull subcommand
    """
    name = 'list'

    def register_parser_arguments(self, parser):
        """
        Register only common base arguments
        """
        return super().register_common_arguments(parser)

    def run(self, args):
        """
        List configured sync targets
        """
        for target in self.filter_targets(args.targets):
            self.message(f'{target.name}')
