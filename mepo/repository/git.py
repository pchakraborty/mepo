import os
import shutil
import subprocess
import shlex

from urllib.parse import urljoin

from mepo.state.state import MepoState
from mepo.utilities import shellcmd
from mepo.utilities import colors

class GitRepository(object):
    """
    Class to consolidate git commands
    """
    __slots__ = ['__local', '__full_local_path', '__remote', '__git']

    def __init__(self, remote_url, local_path):
        self.__local = local_path

        if remote_url.startswith('..'):
            rel_remote = os.path.basename(remote_url)
            fixture_url = get_current_remote_url()
            self.__remote = urljoin(fixture_url,rel_remote)
        else:
            self.__remote = remote_url

        root_dir = MepoState.get_root_dir()
        full_local_path=os.path.join(root_dir,local_path)
        self.__full_local_path=full_local_path
        self.__git = 'git -C "{}"'.format(self.__full_local_path)

    def get_local_path(self):
        return self.__local

    def get_full_local_path(self):
        return self.__full_local_path

    def get_remote_url(self):
        return self.__remote

    def clone(self, version, recurse, type):
        cmd = 'git clone '
        if recurse:
            cmd += '--recurse-submodules '
        # You can't git clone -b hash, so we need to do different things
        if type == 'h':
            cmd += '--quiet {} {}'.format(self.__remote, self.__local)
            shellcmd.run(shlex.split(cmd))
            cmd2 = 'git -C {} checkout {}'.format(self.__local, version)
            shellcmd.run(shlex.split(cmd2))
        else:
            cmd += '--branch {} --quiet {} {}'.format(version, self.__remote, self.__local)
            shellcmd.run(shlex.split(cmd))

    def checkout(self, version):
        cmd = self.__git + ' checkout --quiet {}'.format(version)
        shellcmd.run(shlex.split(cmd))

    def sparsify(self, sparse_config):
        dst = os.path.join(self.__local, '.git', 'info', 'sparse-checkout')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(sparse_config, dst)
        cmd1 = self.__git + ' config core.sparseCheckout true'
        shellcmd.run(shlex.split(cmd1))
        cmd2 = self.__git + ' read-tree -mu HEAD'
        shellcmd.run(shlex.split(cmd2))

    def list_branch(self, all=False):
        cmd = self.__git + ' branch'
        if all:
            cmd += ' -a'
        return shellcmd.run(shlex.split(cmd), output=True)

    def list_tags(self):
        cmd = self.__git + ' tag'
        return shellcmd.run(shlex.split(cmd), output=True)

    def rev_list(self, tag):
        cmd = self.__git + ' rev-list -n 1 {}'.format(tag)
        return shellcmd.run(shlex.split(cmd), output=True)

    def list_stash(self):
        cmd = self.__git + ' stash list'
        return shellcmd.run(shlex.split(cmd), output=True)

    def pop_stash(self):
        cmd = self.__git + ' stash pop'
        return shellcmd.run(shlex.split(cmd), output=True)

    def apply_stash(self):
        cmd = self.__git + ' stash apply'
        return shellcmd.run(shlex.split(cmd), output=True)

    def push_stash(self, message):
        cmd = self.__git + ' stash push'
        if message:
            cmd += ' -m {}'.format(message)
        return shellcmd.run(shlex.split(cmd), output=True)

    def show_stash(self, patch):
        cmd = self.__git + ' stash show'
        if patch:
            cmd += ' -p --color'
        output = shellcmd.run(shlex.split(cmd),output=True)
        return output.rstrip()

    def run_diff(self, args=None):
        cmd = self.__git + ' diff --color'
        if args.name_only:
            cmd += ' --name-only'
        if args.staged:
            cmd += ' --staged'
        output = shellcmd.run(shlex.split(cmd),output=True)
        return output.rstrip()

    def fetch(self, args=None):
        cmd = self.__git + ' fetch'
        if args.all:
            cmd += ' --all'
        if args.prune:
            cmd += ' --prune'
        if args.tags:
            cmd += ' --tags'
        if args.force:
            cmd += ' --force'
        return shellcmd.run(shlex.split(cmd), output=True)

    def create_branch(self, branch_name):
        cmd = self.__git + ' branch {}'.format(branch_name)
        shellcmd.run(shlex.split(cmd))

    def create_tag(self, tag_name, annotate, message, tf_file=None):
        if annotate:
            if tf_file:
                cmd = ['git', '-C', self.__full_local_path, 'tag', '-a', '-F', tf_file, tag_name]
            elif message:
                cmd = ['git', '-C', self.__full_local_path, 'tag', '-a', '-m', message, tag_name]
            else:
                raise Exception("This should not happen")
        else:
            cmd = ['git', '-C', self.__full_local_path, 'tag', tag_name]
        shellcmd.run(cmd)

    def delete_branch(self, branch_name, force):
        delete = '-d'
        if force:
            delete = '-D'
        cmd = self.__git + ' branch {} {}'.format(delete, branch_name)
        shellcmd.run(shlex.split(cmd))

    def delete_tag(self, tag_name):
        cmd = self.__git + ' tag -d {}'.format(tag_name)
        shellcmd.run(shlex.split(cmd))

    def push_tag(self, tag_name, force):
        cmd = self.__git + ' push'
        if force:
            cmd += ' --force'
        cmd += ' origin {}'.format(tag_name)
        shellcmd.run(shlex.split(cmd))

    def verify_branch(self, branch_name):
        cmd = self.__git + ' show-branch remotes/origin/{}'.format(branch_name)
        status = shellcmd.run(shlex.split(cmd),status=True)
        return status

    def check_status(self):
        cmd = self.__git + ' status --porcelain=v2'
        output = shellcmd.run(shlex.split(cmd), output=True)
        if output.strip():
            output_list = output.splitlines()

            # Grab the file names first for pretty printing
            file_name_list = [item.split()[-1] for item in output_list]
            max_file_name_length = len(max(file_name_list, key=len))

            verbose_output_list = []
            for item in output_list:

                index_field = item.split()[0]
                if index_field == "2":
                    new_file_name = colors.YELLOW + item.split()[-2] + colors.RESET

                file_name = item.split()[-1]

                short_status = item.split()[1]

                if index_field == "?":
                    verbose_status = colors.RED   + "untracked file" + colors.RESET

                elif short_status == ".D":
                    verbose_status = colors.RED   + "deleted, not staged" + colors.RESET
                elif short_status == ".M":
                    verbose_status = colors.RED   + "modified, not staged" + colors.RESET
                elif short_status == ".A":
                    verbose_status = colors.RED   + "added, not staged" + colors.RESET

                elif short_status == "D.":
                    verbose_status = colors.GREEN + "deleted, staged" + colors.RESET
                elif short_status == "M.":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET
                elif short_status == "A.":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET

                elif short_status == "MM":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "MD":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "AM":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "AD":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "R.":
                    verbose_status = colors.GREEN + "renamed" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET
                elif short_status == "RM":
                    verbose_status = colors.GREEN + "renamed, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "RD":
                    verbose_status = colors.GREEN + "renamed, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "C.":
                    verbose_status = colors.GREEN + "copied" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET
                elif short_status == "CM":
                    verbose_status = colors.GREEN + "copied, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "CD":
                    verbose_status = colors.GREEN + "copied, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                else:
                    verbose_status = colors.CYAN + "unknown" + colors.RESET + " (please contact mepo maintainer)"

                verbose_status_string = "{file_name:>{file_name_length}}: {verbose_status}".format(
                        file_name=file_name, file_name_length=max_file_name_length,
                        verbose_status=verbose_status)
                verbose_output_list.append(verbose_status_string)

            output = "\n".join(verbose_output_list)

        return output.rstrip()

    def __get_modified_files(self):
        cmd = self.__git + ' diff --name-only'
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split('\n') if output else []

    def __get_untracked_files(self):
        cmd = self.__git + ' ls-files --others --exclude-standard'
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split('\n') if output else []

    def get_changed_files(self, untracked=False):
        changed_files = self.__get_modified_files()
        if untracked:
            changed_files += self.__get_untracked_files()
        return changed_files

    def stage_file(self, myfile):
        cmd = self.__git + ' add {}'.format(myfile)
        shellcmd.run(shlex.split(cmd))

    def get_staged_files(self):
        cmd = self.__git + ' diff --name-only --staged'
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split('\n') if output else []

    def unstage_file(self, myfile):
        cmd = self.__git + ' reset -- {}'.format(myfile)
        shellcmd.run(shlex.split(cmd))

    def commit_files(self, message, tf_file=None):
        if tf_file:
            cmd = ['git', '-C', self.__full_local_path, 'commit', '-F', tf_file]
        elif message:
            cmd = ['git', '-C', self.__full_local_path, 'commit', '-m', message]
        else:
            raise Exception("This should not happen")
        shellcmd.run(cmd)

    def push(self):
        cmd = self.__git + ' push -u {}'.format(self.__remote)
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def get_remote_latest_commit_id(self, branch, commit_type):
        if commit_type == 'h':
            cmd = self.__git + ' cat-file -e {}'.format(branch)
            status = shellcmd.run(shlex.split(cmd), status=True)
            if status != 0:
                msg = 'Hash {} does not exist on {}'.format(branch, self.__remote)
                msg += " Have you run 'mepo push'?"
                raise RuntimeError(msg)
            return branch
        else:
            # If we are a branch...
            if commit_type == 'b':
                msgtype = "Branch"
                reftype = 'heads'
            elif commit_type == 't':
                msgtype = 'Tag'
                reftype = 'tags'
            else:
                raise RuntimeError("Should not get here")
            cmd = self.__git + ' ls-remote {} refs/{}/{}'.format(self.__remote, reftype, branch)
            output = shellcmd.run(shlex.split(cmd), stdout=True).strip()
            if not output:
                #msg = '{} {} does not exist on {}'.format(msgtype, branch, self.__remote)
                #msg += " Have you run 'mepo push'?"
                #raise RuntimeError(msg)
                cmd = self.__git + ' rev-parse HEAD'
            output = shellcmd.run(shlex.split(cmd), output=True).strip()
            return output.split()[0]

    def get_local_latest_commit_id(self):
        cmd = self.__git + ' rev-parse HEAD'
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def pull(self):
        cmd = self.__git + ' pull'
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def get_version(self):
        cmd = self.__git + ' show -s --pretty=%D HEAD'
        output = shellcmd.run(shlex.split(cmd), output=True)
        if output.startswith('HEAD ->'): # an actual branch
            detached = False
            name = output.split(',')[0].split('->')[1].strip()
            tYpe = 'b'
        elif output.startswith('HEAD,'): # detached head
            detached = True
            tmp = output.split(',')[1].strip()
            if tmp.startswith('tag:'): # tag
                name = tmp[5:]
                tYpe = 't'
            else:
                cmd_for_branch = self.__git + ' reflog HEAD -n 1'
                reflog_output = shellcmd.run(cmd_for_branch.split(), output=True)
                name = reflog_output.split()[-1].strip()
                tYpe = 'b'
        elif output.startswith('HEAD'): # Assume hash
            cmd = self.__git + ' rev-parse HEAD'
            hash_out = shellcmd.run(shlex.split(cmd), output=True)
            detached = True
            name = hash_out.rstrip()
            tYpe = 'h'
        elif output.startswith('grafted'):
            cmd = self.__git + ' describe --always'
            hash_out = shellcmd.run(shlex.split(cmd), output=True)
            detached = True
            name = hash_out.rstrip()
            tYpe = 'h'
        return (name, tYpe, detached)

def get_current_remote_url():
    cmd = 'git remote get-url origin'
    output = shellcmd.run(shlex.split(cmd), output=True).strip()
    return output
