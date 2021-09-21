from mepo.utilities import verify
from mepo.state.state import MepoState
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2push = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2push:
        git = GitRepository(comp.remote, comp.local)
        output = git.push()
        print('----------\nPushed: {}\n----------'.format(comp.name))
        print(output)
