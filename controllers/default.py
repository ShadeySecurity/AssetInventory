# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from nmapscanner import *


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Please sign up.")
    return dict(message=T('Welcome to our scripting server!'))


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

@auth.requires_login()
@auth.requires_membership('auditor')
def audit():
    grid = SQLFORM.smartgrid(db.auditexecute, headers={'auditexecute.execoptions':'Standard Options Selected','auditexecute.advancedCMDS':'Advanced Options Selected','auditexecute.Identifier':'Task Identifier'}, deletable=False, create=False, csv=True, editable=False)
    return locals()
    return dict(form=form)
@auth.requires_login()
def results():
    grid = SQLFORM.grid(db.results, editable=False, deletable=False, headers={'results.ip':'IP','results.netbios':'NetBIOS Hostname','results.first_timestamp':'First Seen','results.last_timestamp':'Last Seen','results.dns':'DNS Hostname','results.os':'Operating System'})
    return locals()
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('editor')
def editresults():
    grid = SQLFORM.smartgrid(db.results, headers={'results.ip':'IP','results.netbios':'NetBIOS Hostname','results.first_timestamp':'First Seen','results.last_timestamp':'Last Seen','results.dns':'DNS Hostname','results.os':'Operating System'})
    return locals()
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('execute')
def execute():
    from  datetime import datetime
    try:
        form = SQLFORM(db.auditexecute, record=None,
            deletable=False, linkto=None,
            upload=None, fields = None, labels = {'network':'Your network address or IP','execoptions':'Options','advancedCMDS':"Advanced Commands",'Identifier':'Task Identifier'},
            col3={}, submit_button='Submit',
            delete_label='Check to delete:',
            showid=True, readonly=False,
            comments=True, keepopts=[],
            ignore_rw=False, record_id=None,
            formstyle='table3cols',
            buttons=['submit'], separator=': ')
        if form.process().accepted:
            if len(form.vars.network) > 0 and len(form.vars.speed) > 0 and len(form.vars.justification) > 0:
                speedopts = ["1","2","3","4","5"]
                if form.vars.speed in speedopts:
                    response.flash = T('Thanks! The form has been submitted.')
                    options = ""
                    speed = " -T %s" % (form.vars.speed)
                    if "Get Hostname" in form.vars.execoptions:
                        options += "--script nbstat.nse"
                    elif "Get OS" in form.vars.execoptions:
                        options += " -O"
                    elif "Get ALL" in form.vars.execoptions:
                        options += " -A"
                    else:
                        response.flash = "You selected no standard options! Welcome to 1337 land. You selected %s" % form.vars.execoptions
                    if len(options) < 3:
                        response.flash = "Missing your options!"
                        return 
                    options += " "
                    options += str(form.vars.advancedCMDS)
                    network =  str(form.vars.network)
                    fileopts = str(form.vars.results_location)
                    scan = SuperScan()
                    # If we need root, use custom scan
                    if "-O" in options or "-sS" in options or "-i" in options or "-A" in options:
                        scanresults = scan.customscan(network,speed,options)
                        # Pull each host object out of the scan object
                        for hosts in scanresults.hosts:
                            # Make sure the host is up
                            if scanresults.hosts.isup()
                            # Get all open ports for this host
                            resultports = hosts.get_open_ports()
                            # Merge the tuples in the format we want
                            for tuples in resultports:
                                # Combine tuples with a slash
                                ports = "/".join(tuples)
                                # Add a semi-colon for CSV compatible merged list
                                ports += ";"
                            # Simplify output of results if we can
                            if "Windows" in hosts.os_match_probabilities():
                                osmatches = "Windows"
                            elif "Linux" in hosts.os_match_probabilities():
                                osmatches = "Linux"
                            else:
                                osmatches = ";",.join(hosts.os_match_probabilities())
                            # Grab and merge in a csv friendly manner the hostnames
                            hostnames = ";".join(hosts.hostnames)
                            #Grab out nbstat data
                            for scriptDict in hosts.scripts_results:
                                # check for nbstat scriptname id
                                if scriptDict.get('id') == "nbstat":
                                    # get the nbstat script result dictionary
                                    nbresults= scriptDict
                            # Write to DB
                            success = db(db.results.ip == hosts.address).update(ports=ports, os=osmatches,
                                                                               dns=hostnames,
                                                                               netbios=nbresults,
                                                                               last_timestamp=str(datetime.now()))
                            if success:
                                response.flash = "Data has been updated!"
                            else:
                                success = db.results.insert(ip=hosts.address,ports=ports, os=osmatches,dns=hostnames,netbios=nbresults,,first_timestamp=str(datetime.now()),last_timestamp=str(datetime.now()))

                    else:
                        options += speed
                        scan.scan(network,options)
                        scanresults = scan.out_struct()
                        for result in scanresults:
                            scanports = ''.join(result['ports'])
                            success = db(db.results.ip == result['ip']).update(ports=result['ports'],os=result['os'],dns=result['dns'],netbios=result['netbios'],last_timestamp=str(datetime.now()))
                            if success:
                                response.flash = "Data has been updated!"
                            else:
                                success = db.results.insert(ip=result['ip'],ports=result['ports'],os=result['os'],dns=result['dns'],netbios=result['netbios'],first_timestamp=str(datetime.now()),last_timestamp=str(datetime.now()))
                else:
                    response.flash = T('Thanks, but you gave us a bad speed! 0-5 please!')
            else:
                response.flash = T('Try again - no fields can be empty.')
            response.flash = "Thanks for scanning! Your results are now in the results database!"
        else:
            helloworld = 1
        return dict(form=form)
    except Exception as err:
        response.flash = "Critical Error: %s" % err
    return dict(form=form)
