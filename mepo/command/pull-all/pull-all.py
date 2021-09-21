from mepo.state.state import MepoState
from mepo.repository.git import GitRepository
from mepo.state.component import MepoVersion
from mepo.utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    detached_comps=[]
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        name, tYpe, detached = MepoVersion(*git.get_version())
        if detached:
            detached_comps.append(comp.name)
        else:
            print("Pulling branch %s in %s " %
                    (colors.YELLOW + name + colors.RESET,
                     colors.RESET + comp.name + colors.RESET))
            output = git.pull()
            if not args.quiet: print(output)
    if len(detached_comps) > 0:
        print("The following repos were not pulled (detached HEAD): %s" % (', '.join(map(str, detached_comps))))

