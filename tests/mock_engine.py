import importlib
import glob
from os.path import basename, splitext
import plugins.twitter as t
import plugins.facebook as fb

PLUGINS_DIR = "./plugins"

def get_plugins(plugins_dir = PLUGINS_DIR):
    plugins = {}
    plugin = t.__plugin__()
    plugins[t.__cname__] = plugin
    plugin = fb.__plugin__()
    plugins[fb.__cname__] = plugin

    return plugins

def raw_input(msg):
    return '1'

def getpass(msg):
    return ''

def remove(path):
    pass

class Failed(Exception):
    pass

