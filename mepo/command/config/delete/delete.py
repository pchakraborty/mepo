from mepo.utilities import mepoconfig

def run(args):
    section, option = mepoconfig.split_entry(args.entry)
    mepoconfig.remove_option(section, option)
    mepoconfig.write()
