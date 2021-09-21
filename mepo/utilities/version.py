from collections import namedtuple

MepoVersion = namedtuple('MepoVersion', ['name', 'type', 'detached'])

def version_to_string(version):
    version_name     = version[0]
    version_type     = version[1]
    version_detached = version[2]

    if version_detached: # detached head
        # We remove the "origin/" from the internal detached branch name
        # for clarity in mepo status output
        version_name = version_name.replace('origin/','')
        s = f'({version_type}) {version_name} (DH)'
    else:
        s = f'({version_type}) {version_name}'
    return s

def sanitize_version_string(orig,curr,git):
    '''
    This routine tries to figure out if two tags are the same.

    The issue is that git sometimes returns the "wrong" tag in
    the mepo sense. mepo might have checked out tag v1.0.0 but
    if that commit is also tagged with foo, then sometimes mepo
    will say that things have changed because it thinks it's on
    foo.
    '''

    # The trick below only works on tags and hashes (I think), so
    # if not a tag or hash, just do nothing for now
    is_tag = '(t)'
    is_hash = '(h)'

    # For status, we pass in space-delimited strings that are:
    #  'type version dh'
    # So let's split into lists and pull the type
    # But for save, we are passing in one single string
    orig_list = orig.split()
    if (len(orig_list) > 1):
        # Pull out the type
        orig_type = orig_list[0]
        # Pull out the version string...
        orig_ver = orig_list[1]
    else:
        # Assume tag?
        orig_type = is_tag
        # version is the only element
        orig_ver = orig_list[0]

    curr_list = curr.split()
    if (len(curr_list) > 1):
        # Pull out the type
        curr_type = curr_list[0]
        # Pull out the version string...
        curr_ver = curr_list[1]
    else:
        # Assume tag?
        curr_type = is_tag
        # version is the only element
        curr_ver = curr_list[0]

    orig_type_is_tag_or_hash = (orig_type == is_tag or orig_type == is_hash)
    curr_type_is_tag_or_hash = (curr_type == is_tag or curr_type == is_hash)

    # Now if a type or hash...
    if orig_type_is_tag_or_hash and curr_type_is_tag_or_hash:

        # Use rev-list to get the hash of the tag...
        orig_rev = git.rev_list(orig_ver)
        curr_rev = git.rev_list(curr_ver)

        # If they are identical...
        if orig_rev == curr_rev:

            # Replace the curr version with the original to make
            # mepo happy...
            curr_list[curr_list.index(curr_ver)] = orig_ver
            if orig_type == is_hash:
                curr_list[curr_list.index(curr_type)] = orig_type

            # And then remake the curr string
            curr = ' '.join(curr_list)

    # And return curr
    return curr
