from .. import publish
import argparse
import tempfile
import os
from configobj import ConfigObj
import mock_engine
import mock_subprocess

publish.get_plugins = mock_engine.get_plugins
publish.subprocess = mock_subprocess

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

def test_main():
    publish.main(['--twitter'])
