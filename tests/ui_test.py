import argparse
import tempfile
import os
import mock_engine
import tempfile
from ..modules import ui
from configobj import ConfigObj

ui.get_plugins = mock_engine.get_plugins
ui.raw_input = mock_engine.raw_input
ui.getpass = mock_engine.getpass
ui.os.remove = mock_engine.remove

def test_known_args():
    ui.parse_args(['--twitter'])

def test_unknown_args():
    try:
        ui.parse_args(['--something'])
    except SystemExit:
        pass

def test_no_args():
    try:
        ui.parse_args([])
    except SystemExit:
        pass

def test_main():
    ui.main(['--twitter'])

def test_install_plugin():
    try:
        ui.copyfile = copyfile
        (fn, tmpFile) = tempfile.mkstemp()
        ui.main(['--install', tmpFile])
    except SystemExit:
        os.unlink(tmpFile)

def test_install_plugin_fail():
    try:
        ui.main(['--install', 'path'])
    except SystemExit:
        pass

def test_ui_print():
    ui.ui_print('Hello')

def test_ui_prompt():
    ui.ui_prompt('Hello')
    ui.ui_prompt('Hello', mask = True)
def copyfile(dir1, dir2):
    pass

def test_all():
    ui.main(['--all'])

def test_uninstall_plugin():
    try:
        ui.main(['--uninstall'])
    except SystemExit:
        pass

def test_list():
    try:
        ui.main(['--list'])
    except SystemExit:
        pass

def test_reset_plugin():
    try:
        ui.main(['--reset'])
    except SystemExit:
        pass
