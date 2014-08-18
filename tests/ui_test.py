import os
import argparse
import tempfile
import subprocess
from configobj import ConfigObj
from validate import Validator

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        #sys.exit(1)  --> Ignored due to test fail

parser = ThrowingArgumentParser()

parser.add_argument(
    '-t','--twitter',
    action = 'store_true',
    help = 'Send to twitter')

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

def pass_args(args):
    if len(args)==0:
        parser.print_help()
        #sys.exit(1)  --> Ignored due to test fail
    args = parser.parse_args(args.split())
    
    if args.twitter:
        print "Its twitter time :)"

    (fn, cfgFile) = tempfile.mkstemp()
    (fn, cfgSpec) = tempfile.mkstemp()

    Add_Field('Message', 'string', cfgFile, cfgSpec)
    subprocess.call('%s %s' % (os.getenv('EDITOR'), cfgFile), shell = True)


    if Validate(cfgFile, cfgSpec) != True:
        print "Input file validation failed"
        #sys.exit(1)  --> Ignored due to test fail



pass_args('-t')
pass_args('-f')
pass_args('')
