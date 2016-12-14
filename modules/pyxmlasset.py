#!/usr/bin/python

# A Class which allows us to take dictionaries and export them as xml

class pyxmlasset(object):
    def __init__(self):
        pass
    def dict2xml(self,obj):
        # We may be passing to this 2 different types of objects
        if not type(obj) is dict:
            return
        #TODO: Create looping here to create
        return xmlobj
    def xml2file(self,xmlobj,file):
        if not "xml" in str(type(xmlobj)):
            print("xml2dict: Critical: Object received is not an xml object!")
            return
        if not type(file) is str:
            print("xml2dict: Critical: File object was not a string!")
            return
        try:
            success = xmlobj.write(file)
        except Exception as err:
            print("xml2dict: Error: %s" % err)
            success = False
        if not success:
            print("xml2dict: Error: Unable to write to xml file! ")
        return success