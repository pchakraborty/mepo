from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2popst = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2popst:
        git = GitRepository(comp.remote, comp.local)
        git.pop_stash()
        #print('+ {}'.format(comp.name))
