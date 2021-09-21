import sys
import time
import multiprocessing as mp
import atexit

from mepo.state.state import MepoState
from mepo.repository.git import GitRepository
from mepo.utilities.version import version_to_string
from mepo.utilities import colors

def run(args):
    print('Checking status...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    atexit.register(pool.close)
    result = pool.map(check_component_status, allcomps)
    restore_state(allcomps, result)

def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)
    curr_ver = version_to_string(git.get_version())
    return (curr_ver, git.check_status())

def restore_state(allcomps, result):
    for index, comp in enumerate(allcomps):
        git = GitRepository(comp.remote, comp.local)
        current_version = result[index][0].split(' ')[1]
        orig_version = comp.version.name
        if current_version != orig_version:
            print(colors.YELLOW + "Restoring " + colors.RESET + "{} to {} from {}.".format(comp.name, colors.GREEN + orig_version + colors.RESET, colors.RED + current_version + colors.RESET))
            git.checkout(comp.version.name)
