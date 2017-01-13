# -*- coding: utf-8 -*-
# try something like
def index(): 
    # Write an export page
    import importlib
    if type(modulelist) is not dict:
        return
    for module,attributes in modulelist:
        if "EXPORT" in attributes['FUNCTIONS'] and attributes['DISABLED'] == False:
            importlib.import_module(module)
    return dict(message="hello from export.py")
