#!/usr/bin/env python

import argparse


def parse_args(description='Post tweets on twitter'):
    '''
    
    Parse the arguments

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--message',
        type = str,
        required = True,
        help = 'Message to be Published')
    parser.add_argument(
        '-t','--twitter',
        action = 'store_true',
        help = 'Send to twitter')
    parser.add_argument(
        '-fb','--facebook',
        action = 'store_true',
        help = 'Send to Facebook')
    
    return parser.parse_args()

args = parse_args()

if args.twitter :
    print args.message, ": Will be tweeted soon"
if args.facebook :
    print "%s : This message will be posted to facebook after the api is designed" %args.message
