#!/usr/bin/env python

import os
import argparse
import subprocess
import tempfile
import twitter

def parse_args():
    ''' Parse the arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t','--twitter',
        action = 'store_true',
        help = 'Send to twitter')
    parser.add_argument(
        '-fb','--facebook',
        action = 'store_true',
        help = 'Send to Facebook')
    
    return parser.parse_args()

def GetMsg(filePath):
    ''' Gets message from the User '''
    subprocess.call('%s %s' % (os.getenv('EDITOR'), filePath), shell = True)
    with open(filePath, 'r') as msgFile:
        msg = ''
        for line in msgFile.readlines():
            line = line.strip()
            if not line.startswith('#') and line != '':
                msg += line + '\n'
    return msg[:-1]


args = parse_args()
Messages = {}

if args.twitter:
    try:
        (fn, filePath) = tempfile.mkstemp()
        with open(filePath, 'w') as f:
            default = """\n# Please enter your Twitter message to be sent. Lines starting
# with '#' will be ignored, and an empty message skips this channel."""
            f.write(default)
        msg = GetMsg(filePath)
    finally:
        os.unlink(filePath)

    if msg:
        Messages['Twitter'] = msg
       
if args.facebook:
    try:
        (fn, filePath) = tempfile.mkstemp()
        with open(filePath, 'w') as f:
            default = """\n# Please enter your Facebook message to be sent. Lines starting
# with '#' will be ignored, and an empty message skips this channel."""
            f.write(default)
        msg = GetMsg(filePath)        
    finally:
        os.unlink(filePath)

    if msg:
        Messages['Facebook'] = msg

print Messages
