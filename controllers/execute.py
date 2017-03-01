@auth.requires_login()
@auth.requires_membership('execute')
def index():
    #TODO: Create new execute page
    import importlib
    if type(modulelist) is not dict:
        return
    scantypes = []
    for module,attributes in modulelist:
        if "EXECUTE" in attributes['FUNCTIONS'] and attributes['DISABLED'] == False:
            importlib.import_module(module)
            scantypes.append(attributes['DISPLAYNAME'])
    form = SQLFORM.factory(Field(" ", default=" ", writable=False),
                   Field("User_Name", 'string', required=True, default=auth.user.username, requires=IS_NOT_EMPTY(),writable=False),
                   Field('User_IP','string', required=True, writable=False, default=request.client,requires=IS_IPV4()),
                   Field('Scanner_IP','string', default='127.0.0.1', requires=IS_IPV4()),
                   Field('Scan_Type', required=True, requires=IS_IN_SET(scantypes, zero=T("Select Scan Type"), error_message=T('Not a valid option. Please see documentation.'))),
                   Field('Scan_Destinations','list:string',required=True,requires=IS_NOT_EMPTY()),
                   Field('Task_ID', 'string'),
                   Field('Approver', 'string'),
                   Field('Description','text'),                   
                   Field('Justification','text',required=True, requires=IS_NOT_EMPTY()),                           
                   submit_button='Execute'
                  )
    if form.process().accepted:
        response.flash = T('Scan is being executed and processed! Hold tight.')
        module2use = ''
        for module,attributes in modulelist:
            if attribute['DISPLAYNAME'] == form.vars.Scan_Type:
                module2use = module
        importmodule = __import__ (module2use)
        classmodule = getattr(importmodule,str(module2use))            
        standard_dict = classmodule.import_file(form.vars.Results_File)
        # TODO ADD DB function call.
        scan_type = str(form.vars.Scan_Type)
        scan_id = db.scans.id.max() + 1
        if scan_id < 10:
            scan_id = "000%s" % scan_id
        elif scan_id < 100:
            scan_id = "00%s" % scan_id
        elif scan_id < 1000:
            scan_id = "0%s" % scan_id
        else:
            scan_id = "%s" % scan_id
        scan_id = "%s-%s" % (scan_type,scan_id)
        db.scans.bulk_insert({"user_name":str(form.vars.User_Name), "scan_type": str(form.vars.Scan_Type), "user_ip": str(form.vars.User_IP), "scanner_ip":str(form.vars.Scanner_IP), "approver":str(form.vars.Approver), "description":str(form.vars.Description), "justification":str(form.vars.Justification), "task_id":str(form.vars.Task_ID), "date_timestamp":str(datetime.utcnow()), "network": form.vars.Scan_Destinations})
        if callable(getattr(classmodule, 'execute_root')):
            pass            
        db(db.scans.id == scan_id.split('-')[1]).update(command=scan_results['scan']['command'])
    elif form.errors:
        response.flash = T("Form has errors %s" % error_message)
    else:
        response.flash = T('Please fill out the required information.')
    return dict(form=form)
    return dict()
