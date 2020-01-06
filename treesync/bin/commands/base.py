
from systematic.shell import ScriptCommand

from ...configuration import Configuration, ConfigurationError


class TreeSyncCommand(ScriptCommand):
    """
    Common base class for treesync commands
    """
    def parse_args(self, args):
        args = super().parse_args(args)

        try:
            self.config = Configuration(args.config)
        except ConfigurationError as e:
            self.exit(1, e)

        self.config.save()

        if 'debug' in args and args.debug:
            self.config.debug = True

        if 'quiet' in args and args.quiet:
            self.config.quiet = True

        trees = []
        if 'trees' in args:
            for name in self.config.trees:
                if name in args.trees:
                    trees.append(name)
            args.trees = trees

        if self.config.debug and not self.config.quiet:
            print('configuration: {}'.format(self.config.path))

        return args

    def print_tree_details(self, tree):
        """
        Print details for tree
        """
        print(tree.name)
        print('  source: {}'.format(tree.src))
        print('  target: {}'.format(tree.dest))
        print('   flags: {}'.format(' '.join(tree.flags)))
