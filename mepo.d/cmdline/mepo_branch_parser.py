import sys
import argparse

class MepoBranchParser(object):

    def __init__(self, branch):
        self.branch_subparsers = branch.add_subparsers(dest='mepo_branch_cmd')
        self.__create()
        self.__push()
        self.__pull()
        self.__switch()
        
    def __create(self):
        branch_create = self.branch_subparsers.add_parser(
            'create',
            description='Create branch <branch-name> in all repos with changes')
        branch_create.add_argument('branch_name', metavar='branch-name')

    def __push(self):
        branch_push = self.branch_subparsers.add_parser(
            'push',
            description='Push branch <branch-name> to origin')
        branch_push.add_argument('branch_name', metavar='branch-name')

    def __pull(self):
        branch_pull = self.branch_subparsers.add_parser(
            'pull',
            description='Pull branch <branch-name> from origin to sandbox')
        branch_pull.add_argument('branch_name', metavar='branch-name')

    def __switch(self):
        branch_switch = self.branch_subparsers.add_parser(
            'switch',
            description='switch repository <repo-name> to branch <branch-name>')
        branch_switch.add_argument('repo_name', metavar='repo-name')
        branch_switch.add_argument('branch_name', metavar='branch-name')
