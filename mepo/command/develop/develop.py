from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository
from mepo.utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2dev = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2dev:
        git = GitRepository(comp.remote, comp.local)
        if comp.develop is None:
            raise Exception("'develop' branch not specified for {}".format(comp.name))
        if not args.quiet:
            print("Checking out development branch %s in %s" %
                    (colors.YELLOW + comp.develop + colors.RESET,
                    colors.RESET + comp.name + colors.RESET))
        git.checkout(comp.develop)
        output = git.pull()
