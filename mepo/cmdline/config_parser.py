import argparse
import textwrap

class MepoConfigArgParser(object):

    def __init__(self, config):
        self.config = config.add_subparsers()
        self.config.title = 'mepo config sub-commands'
        self.config.dest = 'mepo_config_cmd'
        self.config.required = True
        self.__get()
        self.__set()
        self.__delete()
        self.__print()

    def __get(self):
        get = self.config.add_parser(
            'get',
            description = ('Get config `entry` in `.mepoconfig`. '
            'Note this uses gitconfig style where `entry` is of the form `section.option`. '
            'So to get an `alias` `st` You would run `mepo config get alias.st`'))
        get.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to display.')

    def __set(self):
        set = self.config.add_parser(
            'set',
            description = ('Set config `entry` to `value` in `.mepoconfig`. '
            'Note this uses gitconfig style where `entry` is of the form `section.option`. '
            'So to set an `alias` for `status` of `st` You would run `mepo config set alias.st status`'))
        set.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to set.')
        set.add_argument(
            'value',
            metavar = 'value',
            help = 'Value to set entry to.')

    def __delete(self):
        delete = self.config.add_parser(
            'delete',
            description = ('Delete config `entry` in `.mepoconfig`. '
            'Note this uses gitconfig style where `entry` is of the form `section.option`. '
            'So to delete an `alias` `st` You would run `mepo config delete alias.st`'))
        delete.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to delete.')

    def __print(self):
        print = self.config.add_parser(
            'print',
            description = 'Print contents of `.mepoconfig`')
