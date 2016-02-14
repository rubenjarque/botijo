import os, importlib

actions = {}

for name in os.listdir("plugins"):
    if name.endswith(".py") & ("__init__.py" != name) & ('_config' not in name):
        module = "plugins." + name[:-3]
        m = importlib.import_module(module)
        initMethod = getattr(m, 'init')
        initMethod(actions)
