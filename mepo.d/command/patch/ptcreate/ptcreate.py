from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):

    allcomps = MepoState.read_state()
    comps2crtpt = _get_comps_to_patch(args.comp_name, allcomps)

    for comp in comps2crtpt:
        git = GitRepository(comp.remote, comp.local)
        output = git.create_patch()
        print(output)
        #with open(args.patch_file, 'a') as f:
            #f.write(output)
        #print('+ {}: {}'.format(comp.name, args.branch_name))

def _get_comps_to_patch(specified_comps, allcomps):
    comps_to_patch = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_patch = [x for x in allcomps if x.name in specified_comps]
    return comps_to_patch
