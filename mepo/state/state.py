import os
import sys
import yaml
import glob
import pickle

from pathlib import Path

from mepo.config.config_file import ConfigFile
from mepo.state.component import MepoComponent
from mepo.utilities import shellcmd
from mepo.state.exceptions import StateDoesNotExistError, StateAlreadyInitializedError

class MepoState(object):

    __state_dir_name = '.mepo'
    __state_fileptr_name = 'state.pkl'

    @staticmethod
    def get_parent_dirs():
        mypath = os.getcwd()
        parentdirs = [mypath]
        while mypath != '/':
            mypath = os.path.dirname(mypath)
            parentdirs.append(mypath)
        return parentdirs

    @classmethod
    def get_dir(cls):
        for mydir in cls.get_parent_dirs():
            state_dir = os.path.join(mydir, cls.__state_dir_name)
            if os.path.exists(state_dir):
                return state_dir
        raise OSError('mepo state dir [.mepo] does not exist')

    @classmethod
    def get_root_dir(cls):
        '''Return directory that contains .mepo'''
        return os.path.dirname(cls.get_dir())

    @classmethod
    def get_file(cls):
        state_file = os.path.join(cls.get_dir(), cls.__state_fileptr_name)
        if os.path.exists(state_file):
            return state_file
        raise OSError('mepo state file [%s] does not exist' % state_file)

    @classmethod
    def exists(cls):
        try:
            cls.get_file()
            return True
        except OSError:
            return False

    @classmethod
    def initialize(cls, project_config_file, directory_style):
        if cls.exists():
            raise StateAlreadyInitializedError('mepo state already exists')
        input_components = ConfigFile(project_config_file).read_file()

        num_fixture = 0
        complist = list()
        for name, comp in input_components.items():
            # We only allow one fixture
            if 'fixture' in comp:
                num_fixture += comp['fixture']
            if num_fixture > 1:
                raise Exception("Only one fixture allowed")

            complist.append(MepoComponent().to_component(name, comp, directory_style))
        cls.write_state(complist)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise StateDoesNotExistError('mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
            try:
                allcomps = pickle.load(fin)
            except ModuleNotFoundError:
                allcomps = renamed_load(fin)
        return allcomps

    @classmethod
    def write_state(cls, state_details):
        if cls.exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), 'state.*.pkl')
            states = [os.path.basename(x) for x in glob.glob(os.path.join(pattern))]
            new_state_id = max([int(x.split('.')[1]) for x in states]) + 1
            state_file_name = 'state.' + str(new_state_id) + '.pkl'
        else:
            state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
            os.mkdir(state_dir)
            state_file_name = 'state.0.pkl'
        new_state_file = os.path.join(state_dir, state_file_name)
        with open(new_state_file, 'wb') as fout:
            pickle.dump(state_details, fout, -1)
        state_fileptr = cls.__state_fileptr_name
        state_fileptr_fullpath = os.path.join(state_dir, state_fileptr)
        if os.path.isfile(state_fileptr_fullpath):
            os.remove(state_fileptr_fullpath)
        #os.symlink(new_state_file, state_fileptr_fullpath)
        curr_dir=os.getcwd()
        os.chdir(state_dir)
        os.symlink(state_file_name, state_fileptr)
        os.chdir(curr_dir)

class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = 'mepo.'+module

        return super(RenameUnpickler, self).find_class(renamed_module, name)

def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()

def renamed_loads(pickled_bytes):
    file_obj = io.BytesIO(pickled_bytes)
    return renamed_load(file_obj)
