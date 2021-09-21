from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository
from mepo.state.component import MepoVersion

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2stg = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2stg:
        git = GitRepository(comp.remote, comp.local)
        stage_files(git, comp, args.untracked)

def stage_files(git, comp, untracked=False, commit=False):
    curr_ver = MepoVersion(*git.get_version())
    if curr_ver.detached: # detached head
        raise Exception(f"{comp.name} has detached head! Cannot stage.")
    for myfile in git.get_changed_files(untracked):
        git.stage_file(myfile)
        print_output = f"{comp.name}: {myfile}"
        if commit:
            print(f"Staged: {print_output}")
        else:
            print(f"+ {print_output}")

