import importlib
import glob
from os.path import basename, splitext

PLUGINS_DIR = "./tests/plugins"

def get_plugins(plugins_dir = PLUGINS_DIR):
    plugins = []
    plugin_files = glob.glob("{}/*.py".format(plugins_dir))
    for plugin_file in plugin_files:
        if plugin_file.endswith("__init__.py"):
            continue
        name, ext = splitext(basename(plugin_file))
        module_name = "publish.tests.plugins.{}".format(name)
        module = importlib.import_module(module_name)
        plugins.append(module.__plugin__)

    return plugins


if __name__ == '__main__':
    main()
