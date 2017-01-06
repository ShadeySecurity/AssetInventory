def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def import_results():
    #TODO: Create a results page for importing csv, nessus, openvas, and nmap
    form = SQLFORM.factory(Field(" ", default=" ", writable=False),
                           Field("User_Name", 'string', required=True, default=auth.user.username, requires=IS_NOT_EMPTY(),writable=False),
                           Field('User_IP','string', required=True, writable=False, default=request.client,requires=IS_IPV4()),
                           Field('Scan_Type', required=True, requires=IS_IN_SET(['NMAP','CSV','NESSUS'], zero=T("Select Scan Type"), error_message=T('Not a valid option. Please see documentation.'))),
                           Field('Task_ID', 'string'),
                           Field('Approver', 'string'),
                           Field('Description','text'),
                           Field('Scanner_IP','string',requires=IS_IPV4()),
                           Field('Justification','text',required=True, requires=IS_NOT_EMPTY()),
                           Field('Results_File','upload',uploadfolder="/tmp",authorize="upload",required=True),
                           submit_button='Import'
                          )
    if form.process().accepted:
        response.flash = T('Import is being processed! Hold tight.')
        if not form.vars.Scan_Type in ['NMAP','CSV','NESSUS']:
            print("Import Results: Critical: Invalid scan type received!!!")
            return dict(form=form)
        else:
            results = {}
            results['user_name'] = auth.user.username
            results['scan_type'] = form.vars.Scan_Type
            results['user_ip'] = request.client
            results['task_id'] = form.vars.Task_ID
            results['approver'] = form.vars.Approver
            results['desc'] = form.vars.Description
            
    elif form.errors:
        response.flash = T('form has errors %s' % error_message)
    else:
        response.flash = T('Please fill out the required information.')
    return dict(form=form)
@auth.requires_login()
@auth.requires_membership('execute')
def scan_nmap():
    #TODO: Create new execute page for nmap scans
    pass
