import subprocess as sp

from mepo.state.state import MepoState

from mepo.command.config.get    import get
from mepo.command.config.set    import set
from mepo.command.config.delete import delete
from mepo.command.config.print  import print

def run(args):
    d = {
        'get': get,
        'set': set,
        'delete': delete,
        'print': print
    }
    d[args.mepo_config_cmd].run(args)
