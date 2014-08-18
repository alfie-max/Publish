import argparse

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.parse_args('--help'.split())

parser = ThrowingArgumentParser()

parser.add_argument(
    '-t','--twitter',
    action = 'store_true',
    help = 'Send to twitter')

args = parser.parse_args('--twitter'.split())
if args.twitter:
    print "Its twitter time :)"

