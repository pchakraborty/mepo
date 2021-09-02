import subprocess as sp

from state.state import MepoState

from command.patch.ptapply  import ptapply
from command.patch.ptcreate import ptcreate

def run(args):
    d = {
        'apply':  ptapply,
        'create': ptcreate,
    }
    d[args.mepo_patch_cmd].run(args)
