import subprocess as sp

from mepo.state.state import MepoState

from mepo.command.branch.list   import list
from mepo.command.branch.create import create
from mepo.command.branch.delete import delete

def run(args):
    d = {
        'list': list,
        'create': create,
        'delete': delete,
    }
    d[args.mepo_branch_cmd].run(args)
