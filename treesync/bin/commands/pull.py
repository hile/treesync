
from .base import TreeSyncCommand


class PullCommand(TreeSyncCommand):
    name = 'pull'
    short_description = 'Pull trees from target'

    def __register_arguments__(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Pass rsync --dry-run flag to command')
        parser.add_argument('trees', nargs='*', help='Trees to pull')

    def run(self, args):

        for tree in args.trees:
            try:
                tree.pull(dry_run=args.dry_run)
            except Exception as e:
                self.error(e)
