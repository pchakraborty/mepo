from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    comps2list = _get_comps_to_list(args.comp_name, allcomps)
    max_namelen = len(max([x.name for x in comps2list], key=len))
    FMT = '{:<%s.%ss} | {:<s}' % (max_namelen, max_namelen)
    for comp in comps2list:
        git = GitRepository(comp.remote, comp.local)
        output = git.list_branch(args.all).rstrip().split('\n')
        print(FMT.format(comp.name, output[0]))
        for line in output[1:]:
            print(FMT.format('', line))

def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list
