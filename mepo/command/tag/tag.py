import subprocess as sp

from mepo.state.state import MepoState

from mepo.command.tag.list   import list
from mepo.command.tag.create import create
from mepo.command.tag.delete import delete
from mepo.command.tag.push   import push

def run(args):
    d = {
        'list': list,
        'create': create,
        'delete': delete,
        'push': push
    }
    d[args.mepo_tag_cmd].run(args)
