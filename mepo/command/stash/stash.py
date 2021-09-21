import subprocess as sp

from mepo.state.state import MepoState

from mepo.command.stash.list  import list
from mepo.command.stash.pop   import pop
from mepo.command.stash.apply import apply
from mepo.command.stash.push  import push
from mepo.command.stash.show  import show

def run(args):
    d = {
        'list':  list,
        'pop':   pop,
        'apply': apply,
        'push':  push,
        'show':  show,
    }
    d[args.mepo_stash_cmd].run(args)
