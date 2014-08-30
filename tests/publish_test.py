from .. import publish
import argparse
import tempfile
import os
from configobj import ConfigObj
import mock_engine

def test_known_args():
    publish.parse_args(['--twitter'])

def test_unknown_args():
    try:
        publish.parse_args(['--something'])
    except SystemExit:
        pass

def test_no_args():
    try:
        publish.parse_args([])
    except SystemExit:
        pass

def test_validate_config():
    (fn, cfgFile) = tempfile.mkstemp() # File to hold the message details 
    (fn, cfgSpec) = tempfile.mkstemp() # File to hold the message specs
    publish.add_field('Message', 'string', cfgFile, cfgSpec)
    publish.validate_configfile(cfgFile, cfgSpec)

def test_get_fields_channels():
    plugins = mock_engine.get_plugins()
    args = [('twitter', True),('facebook', True)]
    publish.get_fields_channels(plugins, args)
