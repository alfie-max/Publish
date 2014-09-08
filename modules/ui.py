import os
import sys
import argparse
import tempfile
import subprocess

from termcolor import colored
from shutil import copyfile
from modules.exception import *
from modules.engine import get_plugins, dispatch
from configobj import ConfigObj, ConfigObjError
from validate import Validator


class ThrowingArgumentParser(argparse.ArgumentParser):
    """ Overrides argparse error function and
    Handles conditions like invalid arguments"""
    def error(self, message):
        self.print_help()
        sys.exit()

def parse_args(args):
    """ Parse arguments to the app """
    parser = ThrowingArgumentParser()
    plugins = get_plugins()
    for plugin in plugins:
        parser.add_argument(
            '-{}'.format(plugin[0]), '--{}'.format(plugin),
            action = 'store_true',
            help = 'Post message via {}'.format(plugin).title())
    parser.add_argument(
        '--install-plugin', type = str,
        nargs = 1, metavar='',
        help = 'Install new plugin')
        
    if len(args) == 0:
        parser.print_help()
        sys.exit()

    return parser.parse_args(args)

def add_field(field, fieldType, cfgFile, cfgSpec):
    """ Adds a field into config file """
    config = ConfigObj(cfgFile, write_empty_values = True)
    config[field] = ''
    config.write()

    spec = ConfigObj(cfgSpec)
    spec[field] = fieldType
    spec.write()

def validate_configfile(cfgFile, cfgSpec):
    """ Validates the config file content types """
    try:
        config = ConfigObj(cfgFile, configspec = cfgSpec)
    except ConfigObjError:
        return False
    validator = Validator()
    result = config.validate(validator)
    os.unlink(cfgSpec)
    return result

def get_fields_channels(plugins, args):
    channels = []
    field_list = []
    args = args._get_kwargs()
    for arg in args:
        if arg[1] and arg[0] in plugins:
            field_list.extend(plugins[arg[0]].__fields__)
            channels.append(arg[0])
    field_list = list(set(field_list))
    if 'Message' in field_list:
        field_list.remove('Message')
        field_list.append('Message')
        
    return field_list, channels

def check_common_args(args):
    status = False
    if args.install_plugin:
        status = True
        plugin_path =  args.install_plugin[0]
        if os.path.isfile(plugin_path):
            plugin = os.path.basename(plugin_path)
            plugins_dir = os.getcwd() + '/plugins/' + plugin
            copyfile(plugin_path ,plugins_dir)
        else:
            ui_print (colored('File Not Found', 'red'))
    if status:
        sys.exit()
        
def ui_print(msg):
    print msg

def main(args):
    fields = {}
    plugins = get_plugins()
    args = parse_args(args)
    check_common_args(args)

    field_list, channels = get_fields_channels(plugins, args)

    (fn, cfgFile) = tempfile.mkstemp() # File to hold the message details
    (fn, cfgSpec) = tempfile.mkstemp() # File to hold the message specs

    for field in field_list:
        add_field(field, 'string', cfgFile, cfgSpec)

    subprocess.call('%s %s' % (os.getenv('EDITOR'), cfgFile), shell = True)
    if validate_configfile(cfgFile, cfgSpec):
        config = ConfigObj(cfgFile)
        for field in field_list:
            fields[field] = config[field]
        responses = {}
        os.unlink(cfgFile)
        for channel in plugins:
            if channel in channels:
                plugin = plugins[channel]
                ui_print(colored(channel.title(), 'cyan', attrs=['underline']))
                try:
                    dispatch(plugin, fields)
                except Failed, e:
                    ui_print(colored(e.message, 'red'))
    else:
        ui_print (clored('Input file validation failed'), 'red')
        os.unlink(cfgFile)
        sys.exit(1)
