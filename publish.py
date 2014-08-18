#!/usr/bin/env python

import argparse
import sys

class ThrowingArgumentParser(argparse.ArgumentParser):
    """ Overrides argparse error function and
    Handles conditions like invalid arguments"""
    def error(self, message):
        self.print_help()

def parse_args():
    """ Parse arguments to the app """
    parser = ThrowingArgumentParser()
    parser.add_argument(
        '-t','--twitter',
        action = 'store_true',
        help = 'Send to twitter')

    if len(sys.argv)==1:
        parser.print_help()

    return parser.parse_args()

args = parse_args()

if args.twitter:
    print "Its twitter time :)"
