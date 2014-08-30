import importlib
import glob
from modules.exception import *
from os.path import basename, splitext

PLUGINS_DIR = "./plugins"

def get_plugins(plugins_dir = PLUGINS_DIR):
    plugins = {}
    plugin_files = glob.glob("{}/*.py".format(plugins_dir))
    for plugin_file in plugin_files:
        if plugin_file.endswith("__init__.py"):
            continue
        name, ext = splitext(basename(plugin_file))
        module_name = "plugins.{}".format(name)
        module = importlib.import_module(module_name)
        plugin = module.__plugin__()
        plugins[module.__cname__] = plugin

    return plugins

def dispatch(plugin, fields):
    if not plugin.VerifyCredentials():
        try:
            plugin.Authorize()
        except (AuthorizarionError, Failed), e:
            return e.message

    req_fields_list = plugin.__fields__
    req_fields = {}
    for field in fields:
        if field in req_fields_list:
            req_fields[field] = fields[field]
    try:
        return plugin.SendMsg(req_fields)
    except Exception, e:
        raise UnhandledException(e.message)

if __name__ == '__main__':
    main()
