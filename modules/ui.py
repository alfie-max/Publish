import os
import sys
import argparse
import tempfile
import importlib
import subprocess

from getpass import getpass
from shutil import copyfile
from termcolor import colored
from validate import Validator
from modules.exception import *
from os.path import split, splitext, exists
from configobj import ConfigObj, ConfigObjError
from modules.engine import get_plugins, dispatch


class ThrowingArgumentParser(argparse.ArgumentParser):
    '''Overrides argparse error function and Handles conditions 
    like invalid arguments.
    '''
    def error(self, message):
        self.print_help()
        sys.exit()

def parse_args(args):
    '''(list) -> object

    Returns an argument parser object with given arguments.
    '''
    parser = ThrowingArgumentParser()
    try:
        plugins = get_plugins()
    except Failed, e:
        ui_print(colored(e.message, 'red'))
        sys.exit(1)
    for plugin in plugins:
        parser.add_argument(
            '-{}'.format(plugin[0]), '--{}'.format(plugin),
            action = 'store_true',
            help = 'Post message via {}'.format(plugin).title())
    parser.add_argument(
        '-a', '--all',
        action = 'store_true',
        help = 'Send via all installed plugins')
    parser.add_argument(
        '-l', '--list',
        action = 'store_true',
        help = 'List all installed plugins')
    parser.add_argument(
        '-r', '--reset-plugin',
        action = 'store_true',
        help = "Reset plugin's saved config")
    parser.add_argument(
        '--install-plugin', type = str,
        nargs = 1, metavar='',
        help = 'Install new plugin')
    parser.add_argument(
        '--uninstall-plugin',
        action = 'store_true',
        help = 'Uninstall plugin')
        
    if len(args) == 0:
        parser.print_help()
        sys.exit()

    return parser.parse_args(args)

def add_field(field, fieldType, cfgFile, cfgSpec):
    '''(string, string, file, file)
    
    Writes into first file empty fields and writes specification
    details of the file in the second file.
    '''
    config = ConfigObj(cfgFile, write_empty_values = True)
    config[field] = ''
    config.write()

    spec = ConfigObj(cfgSpec)
    spec[field] = fieldType
    spec.write()

def validate_configfile(cfgFile, cfgSpec):
    '''(file, file) => bool

    Verifies whether the first file contents are met with its specification
    Returns the verification result as True/False.
    '''
    try:
        config = ConfigObj(cfgFile, configspec = cfgSpec)
    except ConfigObjError:
        return False
    validator = Validator()
    result = config.validate(validator)
    os.unlink(cfgSpec)
    return result

def get_fields_channels(plugins, args):
    '''(dict, object) -> (list, list)

    Takes in a dict with plugin name and corresponding object and arguments.
    Returns fields required by channels and channels passed in arguments.
    '''
    channels = []
    field_list = []
    if args.all:
        for channel in plugins:
            try:
                field_list.extend(plugins[channel].__fields__)
            except AttributeError:
                raise Failed("Channel '{}' has no attribute '__fields__'".format(channel))
            channels.append(channel)
    else:
        args = args._get_kwargs()
        for arg in args:
            if arg[1] and arg[0] in plugins:
                try:
                    field_list.extend(plugins[arg[0]].__fields__)
                except AttributeError:
                    raise Failed("Channel '{}' has no attribute '__fields__'".format(arg[0]))
                channels.append(arg[0])

    field_list = list(set(field_list))
    if 'Message' in field_list:
        field_list.remove('Message')
        field_list.append('Message')
        
    return field_list, channels

def check_common_args(args):
    ''' (list)

    Checks if any common arguments were passed as arguments.
    (common arguments being all arguments other than sending a message)
    '''
    status = False
    if args.reset_plugin:
        if status:
            sys.exit()
        status = True
        try:
            plugins = get_plugins()
        except Failed, e:
            ui_print(colored(e.message, 'red'))
            sys,exit(1)
        if len(plugins) != 0:
            ch = {}
            ui_print(colored('Installed Plugins :', 'blue'))
            for i,channel in enumerate(plugins):
                ui_print(colored(' '*20 + '{}. '.format(i+1) + channel.title(), 'blue'))
                ch[i+1] = channel
            choices = ui_prompt('Select plugin[s] to reset (separate with spaces) : ').split()
            for i, choice in enumerate(choices):
                try:
                    choices[i] = int(choice)
                    if choices[i] in ch:
                        plugin = plugins[ch[choices[i]]]
                        plugin.Reset()
                    else:
                        raise ValueError
                except AttributeError:
                    ui_print(colored("Plugin does't have reset function", 'red'))
                    sys.exit(1)
                except ValueError:
                    ui_print(colored('Invalid Entry', 'red'))
                    sys.exit(1)
        else:
            ui_print(colored('No Plugins Installed', 'blue'))

    if args.list:
        if status:
            sys.exit()
        status = True
        try:
            plugins = get_plugins()
        except Failed, e:
            ui_print(colored(e.message, 'red'))
            sys,exit(1)
        if len(plugins) != 0:
            ui_print(colored('Installed Plugins :', 'blue'))
            for channel in plugins:
                ui_print(colored(' '*20 + channel.title(), 'blue'))
        else:
            ui_print(colored('No Plugins Installed', 'blue'))

    if args.install_plugin:
        if status:
            sys.exit()
        status = True
        plugin_path =  args.install_plugin[0]
        if os.path.isfile(plugin_path):
            plugin = os.path.basename(plugin_path)
            plugins_dir = os.getcwd() + '/plugins/' + plugin
            copyfile(plugin_path ,plugins_dir)
        else:
            ui_print (colored('File Not Found', 'red'))

    if args.uninstall_plugin:
        if status:
            sys.exit()
        status = True
        try:
            plugins = get_plugins()
        except Failed, e:
            ui_print(colored(e.message, 'red'))
            sys,exit(1)
        if len(plugins) != 0:
            ch = {}
            ui_print(colored('Installed Plugins :', 'blue'))
            for i,channel in enumerate(plugins):
                ui_print(colored(' '*20 + '{}. '.format(i+1) + channel.title(), 'blue'))
                ch[i+1] = channel
            choices = ui_prompt('Select plugin[s] to uninstall (separate with spaces) : ').split()
            for i, choice in enumerate(choices):
                try:
                    choices[i] = int(choice)
                    if choices[i] in ch:
                        paths = []
                        plugin = plugins[ch[choices[i]]]
                        module = importlib.import_module(plugin.__module__)
                        path, filename = split(module.__file__)
                        filename, ext = splitext(filename)
                        paths.append(path + os.sep + filename + '.{}'.format('py'))
                        paths.append(path + os.sep + filename + '.{}'.format('pyc'))
                        for path in paths:
                            if exists(path):
                                os.remove(path)
                    else:
                        raise ValueError
                except ValueError:
                    ui_print(colored('Invalid Entry', 'red'))
                    sys.exit(1)
        else:
            ui_print(colored('No Plugins Installed', 'blue'))

    if status:
        sys.exit()
        
def ui_print(msg):
    '''(string)

    Prints given string to UI.
    '''
    print msg

def ui_prompt(msg, mask=False):
    ''' (string, bool)
    
    Function to prompt user for input via UI.
    '''
    try:
        if mask:
            return getpass(colored(msg, 'yellow'))
        else:
            return raw_input(colored(msg, 'yellow'))
    except KeyboardInterrupt:
        print '\r'
        sys.exit(1)

def main(args):
    '''(list)
    
    Main function
    '''
    fields = {}
    args = parse_args(args)
    check_common_args(args)

    try:
        plugins = get_plugins()
        field_list, channels = get_fields_channels(plugins, args)
        if len(channels) == 0:
            raise Failed('No Plugins Installed')
    except Failed, e:
        ui_print(colored(e.message, 'red'))
        sys.exit(1)

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
                ui_print(colored('\n' + channel.title(), 'cyan', attrs=['underline']))
                try:
                    dispatch(plugin, fields)
                except Failed, e:
                    ui_print(colored(e.message, 'red'))
    else:
        ui_print (colored('Input file validation failed', 'red'))
        os.unlink(cfgFile)
        sys.exit(1)
