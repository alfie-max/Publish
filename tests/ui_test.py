import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-t','--twitter',
    action = 'store_true',
    help = 'Send to twitter')


args = parser.parse_args('--twitter'.split())

if args.twitter:
    print "Its twitter time :)"
