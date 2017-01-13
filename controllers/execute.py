@auth.requires_login()
@auth.requires_membership('execute')
def index():
    #TODO: Create new execute page
    import importlib
    if type(modulelist) is not dict:
        return
    for module,attributes in modulelist:
        if "EXECUTE" in attributes['FUNCTIONS'] and attributes['DISABLED'] == False:
            importlib.import_module(module)
    return dict()
