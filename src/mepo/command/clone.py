import os
import shutil
import pathlib
from urllib.parse import urlparse

try:
    from contextlib import chdir as contextlib_chdir
except ImportError:
    from ..utilities.chdir import chdir as contextlib_chdir

from ..state import MepoState
from ..state import StateDoesNotExistError
from ..git import GitRepository
from ..utilities import colors
from ..utilities import mepoconfig


DEFAULT_REGISTRY = "components.yaml"


def run(args):
    """
    Entry point of clone.

    Multiple ways to run clone
    1. After fixture has been cloned (via git clone)
       a. mepo init
          mepo clone
       b. mepo clone (initializes mepo)
    2. Clone fixture as well
       a. mepo clone <url> [<directory>]
       b. mepo clone -b <branch> <url> [<directory>]

    Steps -
    1. Clone fixture - if url is provided
    2. Read state - initialize mepo (write state) first, if needed
    3. Clone components
    4. Checkout all repos to the specified branch
    """
    arg_partial = handle_partial(args.partial)
    arg_style = handle_style(args.style)
    arg_registry = handle_registry(args.registry)

    fixture_dir = os.getcwd()
    if args.url is not None:
        fixture_dir = clone_fixture(args.url, args.branch, args.directory, arg_partial)

    with contextlib_chdir(fixture_dir):
        if arg_registry != DEFAULT_REGISTRY:
            shutil.copy(arg_registry, DEFAULT_REGISTRY)
        allcomps = read_state(arg_style)
        clone_components(allcomps, arg_partial)
        if args.allrepos:
            checkout_all_repos(allcomps, args.branch)


def handle_partial(partial_):
    """
    The `partial_` argument to clone can be set either via command line or
    via .mepoconfig. Non-default value set via command line takes precedence.
    The default value of `partial_` is None, and
    possible choices are None/blobless/treeless
    """
    allowed_non_default = ["blobless", "treeless"]
    if partial_ is None:  # default value from command line
        if mepoconfig.has_option("clone", "partial"):
            partial_ = mepoconfig.get("clone", "partial")
            if partial_ not in allowed_non_default:
                raise ValueError(f"Invalid partial type [{partial_}] in .mepoconfig")
            print(f"Found partial clone type [{partial_}] in .mepoconfig")
    return partial_


def handle_style(style):
    allowed_non_default = ["naked", "prefix", "postfix"]
    if style is None:  # default value from command line
        # For backward compatibility, we look for the "init" option as well
        # in .mepoconfig, provided "clone" does not contain style
        for option in ["clone", "init"]:
            if mepoconfig.has_option(option, "style"):
                style = mepoconfig.get(option, "style")
                if style not in allowed_non_default:
                    raise ValueError(f"Invalid style [{style}] in .mepoconfig")
                print(f"Found style [{style}] in .mepoconfig")
                break
    return style


def clone_fixture(url, branch=None, directory=None, partial=None):
    if directory is None:
        p = urlparse(url)
        last_url_node = p.path.rsplit("/")[-1]
        directory = pathlib.Path(last_url_node).stem
    git = GitRepository(url, directory)
    git.clone(branch, partial)
    return directory


def read_state(style):
    while True:
        try:
            # TODO: remove in v3
            # In case mepo has been initialized via `mepo init`
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            _ = MepoState.initialize(DEFAULT_REGISTRY, style)
            continue
        break
    return allcomps


def handle_registry(arg_registry):
    registry = DEFAULT_REGISTRY
    if arg_registry is not None:
        registry = arg_registry
    return registry


def clone_components(allcomps, partial_):
    max_namelen = max(len(comp.name) for comp in allcomps)
    for comp in allcomps:
        if comp.fixture:
            continue  # not cloning fixture
        recurse_submodules = comp.recurse_submodules
        # According to Git, treeless clones do not interact well with
        # submodules. So if any comp has the recurse option set to True,
        # we do a non-partial clone
        partial_ = None if partial_ == "treeless" and recurse_submodules else partial_
        version = comp.version.name
        version = version.replace("origin/", "")
        git = GitRepository(comp.remote, comp.local)
        git.clone(version, recurse_submodules, partial_)
        if comp.sparse:
            git.sparsify(comp.sparse)
        print_clone_info(comp.name, comp.version, max_namelen)


def print_clone_info(comp_name, comp_version, name_width):
    ver_name_type = f"({comp_version.type}) {comp_version.name}"
    print(f"{comp_name:<{name_width}} | {ver_name_type:<s}")


def checkout_all_repos(allcomps, branch):
    if branch is None:
        raise RuntimeError("`allrepos` option must be used with a branch/tag.")
    for comp in allcomps:
        branch_y = colors.YELLOW + branch + colors.RESET
        print(f"Checking out {branch_y} in {comp.name}")
        git = GitRepository(comp.remote, comp.local)
        git.checkout(branch)
