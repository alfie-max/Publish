#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import subprocess

from configobj import ConfigObj
from validate import Validator
from termcolor import colored
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
        help = 'Post message on Twitter')
    parser.add_argument(
        '-fb','--facebook',
        action = 'store_true',
        help = 'Post message on Facebook')
    parser.add_argument(
        '-b','--blog',
        action = 'store_true',
        help = 'Post message on Blog')
    parser.add_argument(
        '-e','--email',
        action = 'store_true',
        help = 'Sent message via Email')
    parser.add_argument(
        '-tauth','--twitter-auth',
        action = 'store_true',
        help = 'Authenticate twitter account')
    parser.add_argument(
        '-fauth','--facebook-auth',
        action = 'store_true',
        help = 'Authenticate facebook account')
    parser.add_argument(
        '-bauth','--blog-auth',
        action = 'store_true',
        help = 'Authenticate blog account')
    parser.add_argument(
        '-eauth','--email-auth',
        action = 'store_true',
        help = 'Authenticate email account')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def Add_Field(field, value, fieldType, cfgFile, cfgSpec):
    """ Adds a field into config file """
    config = ConfigObj(cfgFile, write_empty_values = True)
    config[field] = value
    config.write()

    spec = ConfigObj(cfgSpec)
    spec[field] = fieldType
    spec.write()

def Validate_ConfigFile(cfgFile, cfgSpec):
    """ Validates the config file content types """
    try:
        config = ConfigObj(cfgFile, configspec = cfgSpec)
    except:
        return False
    validator = Validator()
    result = config.validate(validator)
    os.unlink(cfgSpec)
    return result


""" Here program starts execution """

channels = [] # stores channel list
(fn, cfgFile) = tempfile.mkstemp() # File to hold the message details
(fn, cfgSpec) = tempfile.mkstemp() # File to hold the message specs
args = Parse_Args()

""" Check for authentication request """
auth = False
if args.twitter_auth:
    reply = Authenticate('Twitter')
    print reply
    auth = True
if args.facebook_auth:
    reply = Authenticate('Facebook')
    print reply
    auth = True
if args.blog_auth:
    reply = Authenticate('Blog')
    print reply
    auth = True
if args.email_auth:
    reply = Authenticate('Email')
    print reply
    auth = True

""" Exit if any auth took place """
if auth:
    sys.exit(0)


""" Check for message publish request """
if args.twitter:
    channels.append('Twitter')
if args.facebook:
    channels.append('Facebook')
if args.blog:
    channels.append('Blog')
    Add_Field('Topic', '', 'string', cfgFile, cfgSpec)
if args.email:
    channels.append('Email')
    Add_Field('Subject', '', 'string', cfgFile, cfgSpec)
    Add_Field('To_Email', '', 'string', cfgFile, cfgSpec)
    
""" Ask user input """
if len(channels) != 0 :
    Add_Field('Message', '', 'string', cfgFile, cfgSpec)
    subprocess.call('%s %s' % (os.getenv('EDITOR'), cfgFile), shell = True)
    if Validate_ConfigFile(cfgFile, cfgSpec) != True:
        print colored('Input file validation failed','red')
        os.unlink(cfgFile)
        sys.exit(1)
    else:
        reply = {}
        msgConfig = ConfigObj(cfgFile)
        Message = msgConfig['Message']
        if len(Message.strip()) == 0:
            print colored('Empty message field', 'red')
            exit(1)
        if args.blog:
            Topic = msgConfig['Topic']
            if len(Topic.strip()) == 0:
                reply['Blog'] = colored('Empty topic field', 'red')
                channels.remove('Blog')

        reply.update(Dispatch(channels, cfgFile))
        print "          Message sent Summary          "
        print "----------------------------------------"
        for key in reply:
            print " %s : %s"%(key, reply[key])
