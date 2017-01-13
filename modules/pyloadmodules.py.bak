#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

# This script find all available modules and loads them that match a certain naming scheme.
# Each module must have a pre-cursor description which is as follow:

# NAME: name of the moduke
# DISPLAYNAME: What to display the module to user as
# FUNCTIONS: ADMIN
# AUTHOR: Who do we give credit to
# DESCRIPTION: What is the description of this module
# DISABLE: TRUE

# Note each class must return a dictionary which matches the standard format found in our github wiki

def find_modules(modpath):
    from os import walk
    import re
    if type(modpath) is not str:
        return
    modulelist = {}
    f = []
    # Read all the files in a directory are
    for (dirpath, dirnames, filenames) in walk(modpath):
        f.extend(filenames)
        break
    for xfile in f:
        # Validate the headers are in place exactly as we require.
        if re.match(r'^py[A-Za-z0-9]*.py',xfile):
            with open(xfile, 'r') as thefile:
                filelines = thefile.readlines()
                thefile.close()
            if xfile == "pyloadmodules.py":
                # Make sure we dont load ourselves
                continue
            elif not re.match(r'^\#\sNAME\:\s[A-Za-z0-9]*(\s)?$', filelines[2]):
                continue
            elif not re.match(r'^\#\sDISPLAYNAME\:\s[A-Za-z0-9 ]*(\s)?$', filelines[3]):
                continue
            elif not re.match(r'^\#\sFUNCTIONS\:\s((EXPORT|IMPORT|ADMIN|EXECUTE)(\,)?){1,4}$', filelines[4]):
                continue
            elif not re.match(r'^\#\sAUTHOR\:\s[\w\s]*$', filelines[5]):
                continue
            elif not re.match(r'^\#\sDESCRIPTION\:\s[\w\s]*$', filelines[6]):
                continue
            elif not re.match(r'^\#\sDISABLE\:\s(FALSE|TRUE)(\s)?$', filelines[7]):
                continue
            else:
                reg = re.search(r'^\#\sNAME\:\s([A-Za-z0-9]*)(\s)?$', filelines[2])
                modname = str(reg.group(0))
                modulelist[modname] = {}
                reg = re.search(r'^\#\sDISPLAYNAME\:\s[A-Za-z0-9 ]*(\s)?$', filelines[3])
                modulelist[modname]['DISPLAYNAME'] = str(reg.group(0))
                reg = re.search(r'^\#\sEND\:\s(FRONT|BACK)(\s)?$', filelines[4])
                modulelist[modname]['FUNCTIONS'] = str(reg.group(0)).split(',')
                reg = re.search(r'^\#\sAUTHOR\:\s[\w\s]*$', filelines[5])
                modulelist[modname]['AUTHOR'] = str(reg.group(0))
                reg = re.search(r'^\#\sDESCRIPTION\:\s[\w\s]*$', filelines[6])
                modulelist[modname]['DESCRIPTION'] = str(reg.group(0))
                reg = re.search(r'^\#\sDISABLE\:\s(FALSE|TRUE)(\s)?$', filelines[7])
                if str(reg.group(0)) == "FALSE":
                    modulelist[modname]['DISABLE'] = False
                else:
                    modulelist[modname]['DISABLE'] = True
    return modulelist

def load_modules(modulelist):
    import importlib
    if type(modulelist) is not dict:
        return
    for module,value in modulelist:
        importlib.import_module(module)
    return
