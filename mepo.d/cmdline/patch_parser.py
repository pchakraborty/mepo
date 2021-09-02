import argparse

class MepoPatchArgParser(object):

    def __init__(self, patch):
        self.patch = patch.add_subparsers()
        self.patch.title = 'mepo patch sub-commands'
        self.patch.dest = 'mepo_patch_cmd'
        self.patch.required = True
        self.__apply()
        self.__create()

    def __apply(self):
        ptapply = self.patch.add_parser(
            'apply',
            description = 'apply patch')
        ptapply.add_argument(
            'patch_file',
            metavar = 'patch-file',
            nargs = '?',
            default = 'patch.diff',
            help = 'default patch file: %(default)s')
        ptapply.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component to apply patch in')

    def __create(self):
        ptcreate = self.patch.add_parser(
            'create',
            description = 'create patch')
        ptcreate.add_argument(
            'patch_file',
            metavar = 'patch-file',
            nargs = '?',
            default = 'patch.diff',
            help = 'default patch file: %(default)s')
        ptcreate.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component to create patch in')
