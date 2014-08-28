#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import subprocess

from modules.engine import get_plugins
from configobj import ConfigObj
from validate import Validator
from termcolor import colored


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
        
    if len(args) == 0:
        parser.print_help()
        sys.exit()

    return parser.parse_args(args)


def main(args):
    plugins = get_plugins()
    channels = []
    fields = []
    args = parse_args(args)._get_kwargs()
    for arg in args:
        if arg[1] and arg[0] in plugins:
            fields.extend(plugins[arg[0]].__fields__)
            channels.append(arg[0])
    fields = list(set(fields))
    if 'Message' in fields:
        fields.remove('Message')
        fields.append('Message')

    print fields

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
