import plugins.twitter as t
import plugins.facebook as fb
from ..modules.exception import Failed

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
