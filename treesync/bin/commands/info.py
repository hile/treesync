
from .base import TreeSyncCommand


class InfoCommand(TreeSyncCommand):
    name = 'info'
    short_description = 'Show details for sync configurations'

    def __register_arguments__(self, parser):
        parser.add_argument('trees', nargs='*', help='Trees to show')

    def run(self, args):
        if not args.trees:
            self.exit(1, 'No configure tree matches arguments')

        for tree in args.trees:
            self.print_tree_details(tree)
