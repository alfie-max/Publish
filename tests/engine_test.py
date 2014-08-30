from ..modules import engine
from plugins import facebook as fb
from plugins import twitter as t
from plugins import mail

def test_get_plugins():
    plugins = engine.get_plugins()

def test_dispatch():
    fields = {'Message':'This is a test message'}
    plugin = fb.__plugin__()
    engine.dispatch(plugin, fields)

def test_dispatch_false_credentials():
    fields = {'Message':'This is a test message'}
    plugin = t.__plugin__()
    engine.dispatch(plugin, fields)

def test_dispatch_unauthorized():
    fields = {'Message':'This is a test message'}
    plugin = mail.__plugin__()
    try:
        engine.dispatch(plugin, fields)
    except Exception:
        pass
    
