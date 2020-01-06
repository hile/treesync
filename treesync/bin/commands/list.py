
from .base import TreeSyncCommand


class ListCommand(TreeSyncCommand):
    name = 'list'
    short_description = 'List configured trees'

    def run(self, args):
        for tree in self.config.trees:
            print(tree.name)
