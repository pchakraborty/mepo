from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2deltg = _get_comps_to_list(args.comp_name, allcomps)
    for comp in comps2deltg:
        git = GitRepository(comp.remote, comp.local)
        git.delete_tag(args.tag_name)
        print('- {}: {}'.format(comp.name, args.tag_name))

def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list
