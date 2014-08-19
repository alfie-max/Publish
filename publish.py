#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import subprocess

from configobj import ConfigObj
from validate import Validator
from modules.dispatcher import Dispatch, Authenticate

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
    parser.add_argument(
        '-tauth','--twitter-auth',
        action = 'store_true',
        help = 'Authenticate twitter account')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def Add_Field(field, fieldType, cfgFile, cfgSpec):
    """ Adds a field into config file """
    config = ConfigObj(cfgFile)
    config[field] = ''
    config.write()

    spec = ConfigObj(cfgSpec)
    spec[field] = fieldType
    spec.write()

def Validate_ConfigFile(cfgFile, cfgSpec):
    """ Validates the config file content types """
    config = ConfigObj(cfgFile, configspec = cfgSpec)
    validator = Validator()
    result = config.validate(validator)
    os.unlink(cfgSpec)
    return result


""" Here program starts execution """

channels = [] # stores channel list
(fn, cfgFile) = tempfile.mkstemp() # File to hold the message details
(fn, cfgSpec) = tempfile.mkstemp() # File to hold the message specs
args = Parse_Args()

""" Check each args """
if args.twitter_auth:
    reply = Authenticate('Twitter')
    print reply
    sys.exit(0)
if args.twitter:
    channels.append('Twitter')
    

""" Ask user input """
if len(channels) != 0 :
    Add_Field('Topic', 'string', cfgFile, cfgSpec)
    Add_Field('To_Email', 'string_list', cfgFile, cfgSpec)
    Add_Field('Message', 'string', cfgFile, cfgSpec)
    subprocess.call('%s %s' % (os.getenv('EDITOR'), cfgFile), shell = True)
    if Validate_ConfigFile(cfgFile, cfgSpec) != True:
        print "Input file validation failed"
        os.unlink(cfgFile)
        sys.exit(1)
    else:
        reply = Dispatch(channels, cfgFile)
