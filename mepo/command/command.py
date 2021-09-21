from importlib import import_module
from mepo.utilities import mepoconfig

def run(args):
    mepo_cmd = mepoconfig.get_alias_command(args.mepo_cmd)

    # Load the module containing the 'run' method of specified mepo command
    cmd_module = import_module('mepo.command.{}.{}'.format(mepo_cmd, mepo_cmd))

    # Execute 'run' method of the specified mepo command
    cmd_module.run(args)
