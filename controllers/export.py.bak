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
            scantypes.append(attributes['DISPLAYNAME'])
    form = SQLFORM.factory(Field(" ", default=" ", writable=False),
                           Field("User_Name", 'string', required=True, default=auth.user.username, requires=IS_NOT_EMPTY(),writable=False),
                           Field('User_IP','string', required=True, writable=False, default=request.client,requires=IS_IPV4()),
                           Field('File_Type', required=True, requires=IS_IN_SET(scantypes, zero=T("Select File Type"), error_message=T('Not a valid option. Please see documentation.'))),
                           Field('Task_ID', 'string'),
                           Field('Approver', 'string'),
                           Field('Description','text'),
                           Field('Scanner_IP','string',requires=IS_IPV4()),
                           Field('Justification','text',required=True, requires=IS_NOT_EMPTY()),                           
                           submit_button='Export'
                          )
    if form.process().accepted:
        response.flash = T('Emport is being processed! Hold tight.')
        if not form.vars.File_Type in scantype:
            print("Import Results: Critical: Invalid export file type received!!!")
        else:
            module2use = ''
            for module,attributes in modulelist:
                if attribute['DISPLAYNAME'] == form.vars.File_Type:
                    module2use = module
            importmodule = __import__ (module2use)
            classmodule = getattr(importmodule,str(module2use))
            standard_dict = classmodule.import_file(form.vars.Results_File)
            # TODO ADD DB function call.
    elif form.errors:
        response.flash = T("Form has errors %s" % error_message)
    else:
        response.flash = T('Please fill out the required information.')
    return dict(form=form)
    return dict(message="hello from export.py")
