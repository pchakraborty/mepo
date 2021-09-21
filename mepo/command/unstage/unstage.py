from mepo.state.state import MepoState
from mepo.utilities import shellcmd
from mepo.utilities import verify
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    comps2unstg = _get_comps_to_unstage(args.comp_name, allcomps)
    for comp in comps2unstg:
        git = GitRepository(comp.remote, comp.local)
        staged_files = git.get_staged_files()
        for myfile in staged_files:
            git.unstage_file(myfile)
            print('- {}: {}'.format(comp.name, myfile))

def _get_comps_to_unstage(specified_comps, allcomps):
    comps_to_unstage = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_unstage = [x for x in allcomps if x.name in specified_comps]
    return comps_to_unstage
