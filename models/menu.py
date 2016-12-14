# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = "/SimpleAssetInventory/static/images/favicon.png"
response.title = T("Simple Asset Inventory")
response.subtitle = T('Powered by Python')

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = "ShadeyShades, Special K, and the rest of the SimpleAssetInventory team"
response.meta.source = "https://github.com/ShadeySecurity/AssetInventory"
response.meta.description = T("Simple Inventory System")
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Execute'), False, URL('default','execute'),[]),
    (T('Results'), False, URL('default','results'), []),
    (T('Audit'), False, URL('default','audit'), []),
    (T('Edit Results'), False, URL('default','editresults'),[])
]

DEVELOPMENT_MENU = False


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and scripts resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
