from mepo.cmdline.parser import MepoArgParser
from mepo.command import command

def main():
    args = MepoArgParser().parse()
    command.run(args)
