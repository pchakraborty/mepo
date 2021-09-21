from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository

# Popping up an EDITOR is based on https://stackoverflow.com/a/39989442
import os, tempfile, subprocess

def run(args):
    allcomps = MepoState.read_state()
    comps2crttg = _get_comps_to_list(args.comp_name, allcomps)

    tf_file = None

    if args.annotate:
        create_annotated_tag = True
    elif args.message:
        create_annotated_tag = True
    else:
        create_annotated_tag = False

    if create_annotated_tag:
        # Pop up an editor if a message is not provided
        if not args.message:
            EDITOR = git_var('GIT_EDITOR')
            initial_message = b"" # set up the file

            # Use delete=False to keep the file around as we send the file name to git commit -F
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf_file = tf.name
            tf.write(initial_message)
            tf.flush()
            subprocess.call([EDITOR, tf.name])

    for comp in comps2crttg:
        git = GitRepository(comp.remote, comp.local)
        git.create_tag(args.tag_name,create_annotated_tag,args.message,tf_file)
        print('+ {}: {}'.format(comp.name, args.tag_name))

    if create_annotated_tag:
        # Now close and by-hand delete the temp file
        if not args.message:
            tf.close()
            os.unlink(tf.name)

def git_var(what):
    '''
    return GIT_EDITOR or GIT_PAGER, for instance

    Found at https://stackoverflow.com/a/44174750/1876449

    '''
    proc = subprocess.Popen(['git', 'var', what], shell=False,
        stdout=subprocess.PIPE)
    output = proc.stdout.read()
    status = proc.wait()
    if status != 0:
        raise Exception("git_var failed with [%]" % what)
    output = output.rstrip(b'\n')
    output = output.decode('utf8', errors='ignore') # or similar for py3k
    return output

def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list
