#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import subprocess

from configobj import ConfigObj
from validate import Validator

class ThrowingArgumentParser(argparse.ArgumentParser):
    """ Overrides argparse error function and
    Handles conditions like invalid arguments"""
    def error(self, message):
        self.print_help()
        sys.exit(1)

def Parse_Args():
    """ Parse arguments to the app """
    parser = ThrowingArgumentParser()
    parser.add_argument(
        '-t','--twitter',
        action = 'store_true',
        help = 'Send to twitter')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def Add_Field(field, fieldType, cfgFile, cfgSpec):
    config = ConfigObj(cfgFile)
    config[field] = ''
    config.write()

    spec = ConfigObj(cfgSpec)
    spec[field] = fieldType
    spec.write()

def Validate(cfgFile, cfgSpec):
    config = ConfigObj(cfgFile, configspec = cfgSpec)
    validator = Validator()
    result = config.validate(validator)
    return result


""" Here program starts execution """
args = Parse_Args()
(fn, cfgFile) = tempfile.mkstemp()
(fn, cfgSpec) = tempfile.mkstemp()

if args.twitter:
    print "Its twitter time :)"

Add_Field('Message', 'string', cfgFile, cfgSpec)
subprocess.call('%s %s' % (os.getenv('EDITOR'), cfgFile), shell = True)


if Validate(cfgFile, cfgSpec) != True:
    print "Input file validation failed"
    sys.exit(1)
