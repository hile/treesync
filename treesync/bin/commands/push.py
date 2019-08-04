
from .base import TreeSyncCommand


class PushCommand(TreeSyncCommand):
    name = 'push'
    short_description = 'Push trees to target'

    def __register_arguments__(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Pass rsync --dry-run flag to command')
        parser.add_argument('trees', nargs='*', help='Trees to push2')

    def run(self, args):
        for tree in args.trees:
            try:
                tree.push(dry_run=args.dry_run)
            except Exception as e:
                self.error(e)
