import argparse

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()

parser = ThrowingArgumentParser()

parser.add_argument(
    '-t','--twitter',
    action = 'store_true',
    help = 'Send to twitter')

def pass_args(args):
    if len(args)==0:
        parser.print_help()
    args = parser.parse_args(args.split())
    if args.twitter:
        print "Its twitter time :)"

pass_args('-f')
pass_args('-t')
pass_args('')
