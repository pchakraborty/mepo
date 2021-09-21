from mepo.state.state    import MepoState, StateDoesNotExistError
from mepo.repository.git import GitRepository
from mepo.command.init   import init as mepo_init
from mepo.utilities      import shellcmd, colors
from urllib.parse   import urlparse

import os
import pathlib
import shutil
import shlex

def run(args):

    # This protects against someone using branch without a URL
    if args.branch and not args.repo_url:
        raise RuntimeError("The branch argument can only be used with a URL")

    if args.allrepos and not args.branch:
        raise RuntimeError("The allrepos option must be used with a branch/tag.")

    # If you pass in a config, with clone, it could be outside the repo.
    # So use the full path
    passed_in_config = False
    if args.config:
        passed_in_config = True
        args.config = os.path.abspath(args.config)
    else:
        # If we don't pass in a config, we need to "reset" the arg to the
        # default name because we pass args to mepo_init
        args.config = 'components.yaml'

    if args.repo_url:
        p = urlparse(args.repo_url)
        last_url_node = p.path.rsplit('/')[-1]
        url_suffix = pathlib.Path(last_url_node).suffix
        if args.directory:
            local_clone(args.repo_url,args.branch,args.directory)
            os.chdir(args.directory)
        else:
            if url_suffix == '.git':
                git_url_directory = pathlib.Path(last_url_node).stem
            else:
                git_url_directory = last_url_node

            local_clone(args.repo_url,args.branch)
            os.chdir(git_url_directory)

    # Copy the new file into the repo only if we pass it in
    if passed_in_config:
        try:
            shutil.copy(args.config,os.getcwd())
        except shutil.SameFileError as e:
            pass

    # This tries to read the state and if not, calls init,
    # loops back, and reads the state
    while True:
        try:
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            mepo_init.run(args)
            continue
        break

    max_namelen = len(max([comp.name for comp in allcomps], key=len))
    for comp in allcomps:
        if not comp.fixture:
            git = GitRepository(comp.remote, comp.local)
            version = comp.version.name
            version = version.replace('origin/','')
            recurse = comp.recurse_submodules
            # We need the type to handle hashes in components.yaml
            type = comp.version.type
            git.clone(version,recurse,type)
            if comp.sparse:
                git.sparsify(comp.sparse)
            print_clone_info(comp, max_namelen)

    if args.allrepos:
        for comp in allcomps:
            if not comp.fixture:
                git = GitRepository(comp.remote, comp.local)
                print("Checking out %s in %s" %
                        (colors.YELLOW + args.branch + colors.RESET,
                        colors.RESET + comp.name + colors.RESET))
                git.checkout(args.branch)

def print_clone_info(comp, name_width):
    ver_name_type = '({}) {}'.format(comp.version.type, comp.version.name)
    print('{:<{width}} | {:<s}'.format(comp.name, ver_name_type, width = name_width))

def local_clone(url,branch=None,directory=None):
    cmd = 'git clone '
    if branch:
        cmd += '--branch {} '.format(branch)
    cmd += '--quiet {}'.format(url)
    if directory:
        cmd += ' "{}"'.format(directory)
    shellcmd.run(shlex.split(cmd))
