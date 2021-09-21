from mepo.utilities import mepoconfig

def run(args):
    section, option = mepoconfig.split_entry(args.entry)
    value = args.value
    mepoconfig.set(section, option, value)
    mepoconfig.write()
