from mepo.state.state import MepoState
from mepo.state.component import MepoVersion
from mepo.repository.git import GitRepository
from mepo.config.config_file import ConfigFile
from mepo.utilities.version import sanitize_version_string

import os

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        _update_comp(comp)

    MepoState.write_state(allcomps)

    complist = dict()
    relpath_start = MepoState.get_root_dir()
    for comp in allcomps:
        complist.update(comp.to_dict(relpath_start))
    config_file_root_dir=os.path.join(relpath_start,args.config_file)
    ConfigFile(config_file_root_dir).write_yaml(complist)
    print(f"Components written to '{config_file_root_dir}'")

def _update_comp(comp):
    git = GitRepository(comp.remote, comp.local)
    orig_ver = comp.version
    curr_ver = MepoVersion(*git.get_version())

    orig_ver_is_tag_or_hash = (orig_ver.type == 't' or orig_ver.type == 'h')
    curr_ver_is_tag_or_hash = (curr_ver.type == 't' or curr_ver.type == 'h')

    if orig_ver_is_tag_or_hash and curr_ver_is_tag_or_hash:
        # This command is to try and work with git tag oddities
        curr_ver_to_use = sanitize_version_string(orig_ver.name,curr_ver.name,git)
        if curr_ver_to_use == orig_ver.name:
            comp.version = orig_ver
        else:
            _verify_local_and_remote_commit_ids_match(git, curr_ver_to_use, comp.name, curr_ver.type)
            comp.version = curr_ver
    else:
        if _version_has_changed(curr_ver, orig_ver, comp.name):
            _verify_local_and_remote_commit_ids_match(git, curr_ver.name, comp.name, curr_ver.type)
            comp.version = curr_ver

def _version_has_changed(curr_ver, orig_ver, name):
    result = False
    if curr_ver != orig_ver:
        if curr_ver.type == 'b':
            assert curr_ver.detached is False, f'You cannot save a detached branch, have you committed your code in {name}?\n {curr_ver}'
            result = True
        elif curr_ver.type == 't':
            result = True
        elif curr_ver.type == 'h':
            result = True
        else:
            raise Exception("This should not happen")
    return result

def _verify_local_and_remote_commit_ids_match(git, curr_ver_name, comp_name, curr_ver_type):
    remote_id = git.get_remote_latest_commit_id(curr_ver_name, curr_ver_type)
    local_id = git.get_local_latest_commit_id()
    failmsg = "{} (remote commit) != {} (local commit) for {}:{}. Did you try 'mepo push'?"
    if remote_id != local_id:
        msg = failmsg.format(remote_id, local_id, comp_name, curr_ver_name)
        raise Exception(msg)
