import os

from mepo.state.state import MepoState
from mepo.utilities import verify

def run(args):
    root_dir = MepoState.get_root_dir()
    allcomps = MepoState.read_state()
    if args.comp_name: # single comp name is specified, print relpath
        if args.comp_name == "_root":
            # _root is a "hidden" allowed argument for whereis to return
            # the root dir of the project. Mainly used by mepo-cd
            print(root_dir)
        else:
            verify.valid_components([args.comp_name], allcomps)
            for comp in allcomps:
                if comp.name == args.comp_name:
                    full_local_path=os.path.join(root_dir,comp.local)
                    print(_get_relative_path(full_local_path))
    else: # print relpaths of all comps
        max_namelen = len(max([x.name for x in allcomps], key=len))
        FMT = '{:<%s.%ss} | {:<s}' % (max_namelen, max_namelen)
        for comp in allcomps:
            full_local_path=os.path.join(root_dir,comp.local)
            print(FMT.format(comp.name, _get_relative_path(full_local_path)))

def _get_relative_path(path):
    return os.path.relpath(path, os.getcwd())
