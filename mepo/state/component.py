import os
import shlex
import textwrap
from collections import namedtuple
from mepo.utilities.version import MepoVersion
from mepo.utilities import shellcmd, mepoconfig
from urllib.parse import urlparse

# This will be used to store the "final nodes" from each subrepo
original_final_node_list = []

class MepoComponent(object):

    __slots__ = ['name', 'local', 'remote', 'version', 'sparse', 'develop', 'recurse_submodules', 'fixture']

    def __init__(self):
        self.name = None
        self.local = None
        self.remote = None
        self.version = None
        self.sparse = None
        self.develop = None
        self.recurse_submodules = None
        self.fixture = None

    def __repr__(self):
        return '{} - local: {}, remote: {}, version: {}, sparse: {}, develop: {}, recurse_submodules: {}, fixture: {}'.format(
            self.name, self.local, self.remote, self.version, self.sparse, self.develop, self.recurse_submodules, self.fixture)

    def __set_original_version(self, comp_details):
        if self.fixture:
            cmd_if_branch = 'git symbolic-ref HEAD'
            # Have to use 'if not' since 0 is a good status
            if not shellcmd.run(cmd_if_branch.split(),status=True):
                output = shellcmd.run(cmd_if_branch.split(),output=True).rstrip()
                ver_name = output.replace('refs/heads/','')
                ver_type = 'b'
                is_detached = False
            else:
                # On some CI systems, git is handled oddly. As such, sometimes
                # tags aren't found due to shallow clones
                cmd_for_tag = 'git describe --tags'
                # Have to use 'if not' since 0 is a good status
                if not shellcmd.run(cmd_for_tag.split(),status=True):
                    ver_name = shellcmd.run(cmd_for_tag.split(),output=True).rstrip()
                    ver_type = 't'
                    is_detached = True
                else:
                    # Per internet, describe always should always work, though mepo
                    # will return weirdness (a grafted branch, probably a hash)
                    cmd_for_always = 'git describe --always'
                    ver_name = shellcmd.run(cmd_for_always.split(),output=True).rstrip()
                    ver_type = 'h'
                    is_detached = True
        else:
            if comp_details.get('branch', None):
                # SPECIAL HANDLING of 'detached head' branches
                ver_name = 'origin/' + comp_details['branch']
                ver_type = 'b'
                # we always detach branches from components.yaml
                is_detached = True
            elif comp_details.get('hash', None):
                # Hashes don't have to exist
                ver_name = comp_details['hash']
                ver_type = 'h'
                is_detached = True
            else:
                ver_name = comp_details['tag'] # 'tag' key has to exist
                ver_type = 't'
                is_detached = True
        self.version = MepoVersion(ver_name, ver_type, is_detached)

    def __validate_fixture(self, comp_details):
        unallowed_keys = ['remote', 'local', 'branch', 'hash', 'tag', 'sparse', 'recurse_submodules']
        if any([comp_details.get(key) for key in unallowed_keys]):
            raise Exception("Fixtures are only allowed fixture and develop")

    def __validate_component(self, comp_name, comp_details):
        types_of_git_tags = ['branch', 'tag', 'hash']
        git_tag_intersection = set(types_of_git_tags).intersection(set(comp_details.keys()))
        if len(git_tag_intersection) == 0:
            raise Exception(textwrap.fill(textwrap.dedent(f'''
                Component {comp_name} has none of {types_of_git_tags}. mepo
                requires one of them.''')))
        elif len(git_tag_intersection) != 1:
            raise Exception(textwrap.fill(textwrap.dedent(f'''
                Component {comp_name} has {git_tag_intersection} and only one of
                {types_of_git_tags} are allowed.''')))

    def to_component(self, comp_name, comp_details, comp_style):
        self.name = comp_name
        self.fixture = comp_details.get('fixture', False)
        if self.fixture:
            self.__validate_fixture(comp_details)

            self.local = '.'
            repo_url = get_current_remote_url()
            p = urlparse(repo_url)
            last_url_node = p.path.rsplit('/')[-1]
            self.remote = "../"+last_url_node
        else:
            self.__validate_component(comp_name, comp_details)
            #print(f"original self.local: {comp_details['local']}")

            # Assume the flag for repostories is commercial-at
            repo_flag = '@'

            # To make it easier to loop over the local path, split into a list
            local_list = splitall(comp_details['local'])

            # The last node of the path is what we will decorate
            last_node = local_list[-1]

            # Add that final node to a list
            original_final_node_list.append(last_node)

            # Now we need to decorate all the final nodes since we can have
            # nested repos with mepo
            for item in original_final_node_list:
                try:
                    # Find the index of every "final node" in a local path
                    # for nesting
                    index = local_list.index(item)

                    # Decorate all final nodes
                    local_list[index] = decorate_node(item, repo_flag, comp_style)
                except ValueError:
                    pass

            # Now pull the list of nodes back into a path
            self.local = os.path.join(*local_list)
            #print(f'final self.local: {self.local}')

            self.remote = comp_details['remote']
        self.sparse = comp_details.get('sparse', None) # sparse is optional
        self.develop = comp_details.get('develop', None) # develop is optional
        self.recurse_submodules = comp_details.get('recurse_submodules', None) # recurse_submodules is optional
        self.__set_original_version(comp_details)
        return self

    def to_dict(self, start):
        details = dict()
        # Fixtures are allowed exactly two entries
        if self.fixture:
            details['fixture'] = self.fixture
            if self.develop:
                details['develop'] = self.develop
        else:
            details['local'] = self.local
            details['remote'] = self.remote
            if self.version.type == 't':
                details['tag'] = self.version.name
            elif self.version.type == 'h':
                details['hash'] = self.version.name
            else: # if not tag or hash, version has to be a branch
                if self.version.detached: # SPECIAL HANDLING of 'detached head' branches
                    details['branch'] = self.version.name.replace('origin/', '')
                else:
                    details['branch'] = self.version.name
            if self.sparse:
                details['sparse'] = self.sparse
            if self.develop:
                details['develop'] = self.develop
            if self.recurse_submodules:
                details['recurse_submodules'] = self.recurse_submodules
        return {self.name: details}

def get_current_remote_url():
    cmd = 'git remote get-url origin'
    output = shellcmd.run(shlex.split(cmd), output=True).strip()
    return output

def decorate_node(item, flag, style):
    # If we do not pass in a style...
    if not style:
        # Just use what's in components.yaml
        return item
    # else use the style
    else:
        item = item.replace(flag,'')
        if style == 'naked':
            output = item
        elif style == 'prefix':
            output = flag + item
        elif style == 'postfix':
            output = item + flag
        return output

# From https://learning.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
