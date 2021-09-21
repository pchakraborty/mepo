from mepo.utilities import mepoconfig

def run(args):
    section, option = mepoconfig.split_entry(args.entry)
    if not mepoconfig.has_section(section):
        raise Exception(f'Section [{section}] does not exist in .mepoconfig')
    if not mepoconfig.has_option(section, option):
        raise Exception(f'Option [{option}] does not exist in section [{section}] in .mepoconfig')
    value = mepoconfig.get(section, option)
    print(f'''
    [{section}]
    {option} = {value}
    ''')
