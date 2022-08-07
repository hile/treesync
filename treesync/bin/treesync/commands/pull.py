"""
Treesync 'pull' subcommand
"""

from treesync.exceptions import SyncError
from .base import TreesyncCommand


class Pull(TreesyncCommand):
    """
    Tree pull subcommand
    """
    name = 'pull'

    def register_parser_arguments(self, parser):
        """
        Register arguments for 'pull' command
        """
        return super().register_rsync_arguments(parser)

    def run(self, args):
        targets = self.filter_targets(args.targets)
        if not targets:
            self.exit(1, 'No targets specified')
        errors = False
        for target in targets:
            self.message(f'pull {target.destination} -> {target.source}')
            try:
                target.pull(dry_run=args.dry_run)
            except SyncError as error:
                self.error(error)
                errors = True
        if errors:
            self.exit(1, 'Errors pulling targets')
