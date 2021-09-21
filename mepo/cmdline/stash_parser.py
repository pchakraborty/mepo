import argparse

class MepoStashArgParser(object):

    def __init__(self, stash):
        self.stash = stash.add_subparsers()
        self.stash.title = 'mepo stash sub-commands'
        self.stash.dest = 'mepo_stash_cmd'
        self.stash.required = True
        self.__push()
        self.__list()
        self.__pop()
        self.__apply()
        self.__show()
        
    def __push(self):
        stpush = self.stash.add_parser(
            'push',
            description = 'Push (create) stash in component <comp-name>')
        stpush.add_argument(
            '-m', '--message', 
            type=str, 
            metavar = 'message', 
            default=None,
            help = 'Message for the stash')
        stpush.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to push stash in')

    def __show(self):
        stshow = self.stash.add_parser(
            'show',
            description = 'show stash in component <comp-name>')
        stshow.add_argument(
                '-p', '--patch',
                action = 'store_true',
                help = 'Message for the stash')
        stshow.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to show stash in')

    def __list(self):
        stlist = self.stash.add_parser(
            'list',
            description = 'List local stashes of all components')

    def __pop(self):
        stpop = self.stash.add_parser(
            'pop',
            description = 'Pop stash in component <comp-name>')
        stpop.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to pop stash in')

    def __apply(self):
        stapply = self.stash.add_parser(
            'apply',
            description = 'apply stash in component <comp-name>')
        stapply.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to apply stash in')
