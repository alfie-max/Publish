from .. import publish
import argparse
import tempfile
import os
from configobj import ConfigObj
import mock_engine
import tempfile

publish.get_plugins = mock_engine.get_plugins

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

def test_install_plugin():
    try:
        publish.copyfile = copyfile
        (fn, tmpFile) = tempfile.mkstemp()
        publish.main(['--install-plugin', tmpFile])
    except SystemExit:
        os.unlink(tmpFile)

def test_install_plugin_fail():
    try:
        publish.main(['--install-plugin', 'path'])
    except SystemExit:
        pass

def copyfile(dir1, dir2):
    pass
