from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository
from mepo.command.stage.stage import stage_files

# Popping up an EDITOR is based on https://stackoverflow.com/a/39989442
import os, tempfile, subprocess

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2commit = [x for x in allcomps if x.name in args.comp_name]

    tf_file = None

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

    for comp in comps2commit:
        git = GitRepository(comp.remote, comp.local)
        if args.all:
            stage_files(git, comp, commit=True)

        staged_files = git.get_staged_files()
        if staged_files:
            git.commit_files(args.message,tf_file)

        for myfile in staged_files:
            print('+ {}: {}'.format(comp.name, myfile))

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

