import argparse
import warnings

from .branch_parser import MepoBranchArgParser
from .stash_parser import MepoStashArgParser
from .tag_parser import MepoTagArgParser
from .config_parser import MepoConfigArgParser

from ..utilities import mepoconfig


def get_version():
    from importlib import metadata

    return metadata.version("mepo")


class LocationAction(argparse._StoreTrueAction):

    def __init__(self, option_strings, dest, const=True, help=None):
        super().__init__(option_strings, dest, const, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        import os, sys
        import mepo

        print(os.path.dirname(mepo.__file__))
        sys.exit(0)


class MepoArgParser:

    __slots__ = ["parser", "subparsers"]

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Tool to manage (m)ultiple r(epo)s"
        )
        self.parser.add_argument("--version", action="version", version=get_version())
        self.parser.add_argument(
            "--location", action=LocationAction, help=argparse.SUPPRESS
        )
        self.subparsers = self.parser.add_subparsers()
        self.subparsers.title = "mepo commands"
        self.subparsers.required = True
        self.subparsers.dest = "mepo_cmd"

    def parse(self):
        self.__init()
        self.__clone()
        self.__list()
        self.__status()
        self.__restore_state()
        self.__diff()
        self.__fetch()
        self.__checkout()
        self.__checkout_if_exists()
        self.__changed_files()
        self.__branch()
        self.__tag()
        self.__stash()
        self.__develop()
        self.__pull()
        self.__pull_all()
        self.__compare()
        self.__reset()
        self.__whereis()
        self.__stage()
        self.__unstage()
        self.__commit()
        self.__push()
        self.__save()
        self.__config()
        self.__update_state()
        return self.parser.parse_args()

    def __init(self):
        init = self.subparsers.add_parser(
            "init",
            description="Initialize mepo based on `config-file`",
            aliases=mepoconfig.get_command_alias("init"),
        )
        init.add_argument(
            "--registry",
            nargs="?",
            default="components.yaml",
            help="default: %(default)s",
        )
        init.add_argument(
            "--style",
            metavar="style-type",
            nargs="?",
            default=None,
            choices=["naked", "prefix", "postfix"],
            help="Style of directory file, default: prefix, allowed options: %(choices)s",
        )

    def __clone(self):
        clone = self.subparsers.add_parser(
            "clone",
            description="Clone repositories.",
            aliases=mepoconfig.get_command_alias("clone"),
        )
        clone.add_argument(
            "url", metavar="URL", nargs="?", default=None, help="URL to clone"
        )
        clone.add_argument(
            "directory",
            nargs="?",
            default=None,
            help="Directory to clone into (Only allowed with URL!)",
        )
        clone.add_argument(
            "--branch",
            "-b",
            metavar="name",
            nargs="?",
            default=None,
            help="Branch/tag of URL to initially clone (Only allowed with URL!)",
        )
        clone.add_argument(
            "--registry",
            metavar="registry",
            nargs="?",
            default=None,
            help="Registry (default: %(default)s)",
        )
        clone.add_argument(
            "--style",
            metavar="style-type",
            nargs="?",
            default=None,
            choices=["naked", "prefix", "postfix"],
            help="Style of directory file, default: prefix, allowed options: %(choices)s (ignored if init already called)",
        )
        clone.add_argument(
            "--allrepos",
            action="store_true",
            help="Must be passed with -b/--branch. When set, it not only checkouts out the branch/tag for the fixture, but for all the subrepositories as well.",
        )
        clone.add_argument(
            "--partial",
            metavar="partial-type",
            nargs="?",
            default=None,
            choices=[None, "blobless", "treeless"],
            help=(
                """
                Style of partial clone, default: %(default)s.
                Allowed options: %(choices)s.
                None: normal full git clone,
                blobless: cloning with "--filter=blob:none",
                treeless: cloning with "--filter=tree:0".
                NOTE: We do *not* recommend using "treeless" as it is very
                aggressive and will cause problems with many git commands.
                """
            ),
        )

    def __list(self):
        listcomps = self.subparsers.add_parser(
            "list",
            description="List all components that are being tracked",
            aliases=mepoconfig.get_command_alias("list"),
        )
        listcomps.add_argument(
            "-1", "--one-per-line", action="store_true", help="one component per line"
        )

    def __status(self):
        status = self.subparsers.add_parser(
            "status",
            description="Check current status of all components",
            aliases=mepoconfig.get_command_alias("status"),
        )
        status.add_argument(
            "--ignore-permissions",
            action="store_true",
            help="Tells command to ignore changes in file permissions.",
        )
        status.add_argument(
            "--nocolor", action="store_true", help="Tells status to not display colors."
        )
        status.add_argument(
            "--hashes", action="store_true", help="Print the exact hash of the HEAD."
        )
        status.add_argument(
            "--parallel", action="store_true", help="Run the parallel version."
        )

    def __restore_state(self):
        restore_state = self.subparsers.add_parser(
            "restore-state",
            description="Restores all components to the last saved state.",
            aliases=mepoconfig.get_command_alias("restore-state"),
        )
        restore_state.add_argument(
            "--parallel", action="store_true", help="Run the parallel version."
        )

    def __diff(self):
        diff = self.subparsers.add_parser(
            "diff",
            description="Diff all components",
            aliases=mepoconfig.get_command_alias("diff"),
        )
        diff.add_argument(
            "--name-only", action="store_true", help="Show only names of changed files"
        )
        diff.add_argument(
            "--name-status",
            action="store_true",
            help="Show name-status of changed files",
        )
        diff.add_argument(
            "--ignore-permissions",
            action="store_true",
            help="Tells command to ignore changes in file permissions.",
        )
        diff.add_argument(
            "--staged", action="store_true", help="Show diff of staged changes"
        )
        diff.add_argument(
            "-b",
            "--ignore-space-change",
            action="store_true",
            help="Ignore changes in amount of whitespace",
        )
        diff.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="*",
            help="Component to list branches in",
        )

    def __checkout(self):
        checkout = self.subparsers.add_parser(
            "checkout",
            description="Switch to branch/tag `branch-name` in component `comp-name`. "
            "If no components listed, checkout from all. "
            "Specifying `-b` causes the branch `branch-name` to be created and checked out.",
            aliases=mepoconfig.get_command_alias("checkout"),
        )
        checkout.add_argument(
            "branch_name", metavar="branch-name", help="Name of branch"
        )
        checkout.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="*",
            help="Components to checkout branch in",
        )
        checkout.add_argument("-b", action="store_true", help="create the branch")
        checkout.add_argument(
            "-q", "--quiet", action="store_true", help="Suppress prints"
        )
        checkout.add_argument(
            "--detach", action="store_true", help="Detach upon checkout"
        )

    def __checkout_if_exists(self):
        checkout_if_exists = self.subparsers.add_parser(
            "checkout-if-exists",
            description="Switch to branch or tag `ref-name` in any component where it is present. ",
            aliases=mepoconfig.get_command_alias("checkout-if-exists"),
        )
        checkout_if_exists.add_argument(
            "ref_name", metavar="ref-name", help="Name of branch or tag"
        )
        checkout_if_exists.add_argument(
            "-q", "--quiet", action="store_true", help="Suppress prints"
        )
        checkout_if_exists.add_argument(
            "--detach", action="store_true", help="Detach on checkout"
        )
        checkout_if_exists.add_argument(
            "-n",
            "--dry-run",
            action="store_true",
            help="Dry-run only (lists repos where branch exists)",
        )

    def __changed_files(self):
        changed_files = self.subparsers.add_parser(
            "changed-files",
            description="List files that have changes versus the state. By default runs against all components.",
            aliases=mepoconfig.get_command_alias("changed-files"),
        )
        changed_files.add_argument(
            "--full-path", action="store_true", help="Print with full path"
        )
        changed_files.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="*",
            help="Component to list branches in",
        )

    def __fetch(self):
        fetch = self.subparsers.add_parser(
            "fetch",
            description="Download objects and refs from in component `comp-name`. "
            "If no components listed, fetches from all",
            aliases=mepoconfig.get_command_alias("fetch"),
        )
        fetch.add_argument(
            "comp_name", metavar="comp-name", nargs="*", help="Components to fetch in"
        )
        fetch.add_argument("--all", action="store_true", help="Fetch all remotes.")
        fetch.add_argument(
            "-p", "--prune", action="store_true", help="Prune remote branches."
        )
        fetch.add_argument("-t", "--tags", action="store_true", help="Fetch tags.")
        fetch.add_argument("-f", "--force", action="store_true", help="Force action.")

    def __branch(self):
        branch = self.subparsers.add_parser(
            "branch",
            description="Runs branch commands.",
            aliases=mepoconfig.get_command_alias("branch"),
        )
        MepoBranchArgParser(branch)

    def __stash(self):
        stash = self.subparsers.add_parser(
            "stash",
            description="Runs stash commands.",
            aliases=mepoconfig.get_command_alias("stash"),
        )
        MepoStashArgParser(stash)

    def __tag(self):
        tag = self.subparsers.add_parser(
            "tag",
            description="Runs tag commands.",
            aliases=mepoconfig.get_command_alias("tag"),
        )
        MepoTagArgParser(tag)

    def __develop(self):
        develop = self.subparsers.add_parser(
            "develop",
            description="Checkout current version of 'develop' branches of specified components",
            aliases=mepoconfig.get_command_alias("develop"),
        )
        develop.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            default=None,
            help="Component(s) to checkout development branches",
        )
        develop.add_argument(
            "-q", "--quiet", action="store_true", help="Suppress prints"
        )

    def __pull(self):
        pull = self.subparsers.add_parser(
            "pull",
            description="Pull branches of specified components",
            aliases=mepoconfig.get_command_alias("pull"),
        )
        pull.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            default=None,
            help="Components to pull in",
        )
        pull.add_argument("-q", "--quiet", action="store_true", help="Suppress prints")

    def __pull_all(self):
        pull_all = self.subparsers.add_parser(
            "pull-all",
            description="Pull branches of all components (only those in non-detached HEAD state)",
            aliases=mepoconfig.get_command_alias("pull-all"),
        )
        pull_all.add_argument(
            "-q", "--quiet", action="store_true", help="Suppress prints"
        )

    def __compare(self):
        compare = self.subparsers.add_parser(
            "compare",
            description="Compare current and original states of all components. "
            "Will only show differing repos unless --all is passed in",
            aliases=mepoconfig.get_command_alias("compare"),
        )
        compare.add_argument(
            "--all",
            action="store_true",
            help="Show all repos, not only differing repos",
        )
        compare.add_argument(
            "--nocolor",
            action="store_true",
            help="Tells command to not display colors.",
        )
        compare.add_argument(
            "--wrap",
            action="store_true",
            help="Tells command to ignore terminal size and wrap",
        )

    def __reset(self):
        reset = self.subparsers.add_parser(
            "reset",
            description="Reset the current mepo clone to the original state. "
            "This will delete all subrepos and does not check for uncommitted changes! "
            "Must be run in the root of the mepo clone.",
            aliases=mepoconfig.get_command_alias("reset"),
        )
        reset.add_argument("-f", "--force", action="store_true", help="Force action.")
        reset.add_argument(
            "--reclone", action="store_true", help="Reclone repos after reset."
        )
        reset.add_argument("-n", "--dry-run", action="store_true", help="Dry-run only")

    def __whereis(self):
        whereis = self.subparsers.add_parser(
            "whereis",
            description="Get the location of component `comp-name` "
            "relative to my current location. If `comp-name` is not present, "
            "get the relative locations of ALL components.",
            aliases=mepoconfig.get_command_alias("whereis"),
        )
        whereis.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="?",
            default=None,
            help="Component to get location of",
        )
        whereis.add_argument(
            "-i", "--ignore-case", action="store_true", help="Ignore case for whereis"
        )

    def __stage(self):
        stage = self.subparsers.add_parser(
            "stage",
            description="Stage modified & untracked files in the specified component(s)",
            aliases=mepoconfig.get_command_alias("stage"),
        )
        stage.add_argument(
            "--untracked", action="store_true", help="Stage untracked files as well"
        )
        stage.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            help="Component to stage file in",
        )

    def __unstage(self):
        unstage = self.subparsers.add_parser(
            "unstage",
            description="Un-stage staged files. "
            "If a component is specified, files are un-staged only for that component.",
            aliases=mepoconfig.get_command_alias("unstage"),
        )
        unstage.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="*",
            help="Component to unstage in",
            default=None,
        )

    def __commit(self):
        commit = self.subparsers.add_parser(
            "commit",
            description="Commit staged files in the specified components",
            aliases=mepoconfig.get_command_alias("commit"),
        )
        commit.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Stage all tracked files and then commit",
        )
        commit.add_argument(
            "-m",
            "--message",
            type=str,
            metavar="message",
            default=None,
            help="Message to commit with",
        )
        commit.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            help="Component to commit file in",
        )

    def __push(self):
        push = self.subparsers.add_parser(
            "push",
            description="Push local commits to remote for specified component. "
            "Use mepo tag push to push tags",
            aliases=mepoconfig.get_command_alias("push"),
        )
        push.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            help="Component to push to remote",
        )

    def __save(self):
        save = self.subparsers.add_parser(
            "save",
            description="Save current state in a yaml registry",
            aliases=mepoconfig.get_command_alias("save"),
        )
        save.add_argument(
            "registry",
            metavar="registry",
            nargs="?",
            default="components-new.yaml",
            help="default: %(default)s",
        )

    def __config(self):
        config = self.subparsers.add_parser(
            "config",
            description="Runs config commands.",
            aliases=mepoconfig.get_command_alias("config"),
        )
        MepoConfigArgParser(config)

    def __update_state(self):
        _ = self.subparsers.add_parser(
            "update-state",
            description="Permanently update mepo1 state to current",
            aliases=mepoconfig.get_command_alias("update-state"),
        )
