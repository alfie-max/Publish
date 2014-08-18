#!/usr/bin/env python

import argparse

def parse_args():
    """ Parse arguments to the app """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t','--twitter',
        action = 'store_true',
        help = 'Send to twitter')
    
    return parser.parse_args()

args = parse_args()

if args.twitter:
    print "Its twitter time :)"
