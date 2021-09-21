import configparser
import os
import sys

config_file = os.path.expanduser('~/.mepoconfig')
config = configparser.ConfigParser()
config.read(config_file)

def split_entry(entry):
    entry_list = entry.split('.')
    if len(entry_list) != 2:
        raise Exception(f'Invalid entry [{entry}]. Must be of form section.option, e.g., "alias.st"')
    section = entry_list[0]
    option = entry_list[1]
    return section, option

def write():
    with open(config_file,'w') as fp:
        config.write(fp)

def print_sections():
    print(config.sections())

def print_options(section):
    print(config.options(section))

def print():
    config.write(sys.stdout)

def has_section(section):
    return config.has_section(section)

def has_option(section, option):
    return config.has_option(section, option)

def get(section, option):
    return config[section][option]

def remove_option(section, option):
    config.remove_option(section, option)
    if not config[section]:
        config.remove_section(section)

def set(section, option, value):
    if not has_section(section):
        config[section] = {}
    config[section][option] = value

def get_command_alias(command):
    output = []
    if has_section('alias'):
        for key,value in config.items('alias'):
            if value == command:
                output.append(key)
    return output

def get_alias_command(alias):
    command = alias
    if has_section('alias'):
        for key,value in config.items('alias'):
            if key == alias:
                command = value
    return command
