#!/usr/bin/python

# NAME: PYNESSUSASSET
# DISPLAYNAME: NESSUS
# FUNCTIONS: IMPORT
# AUTHOR: ShadeyShades
# DESCRIPTION: Import Nessus XML files into the standard format
# DISABLE: TRUE

# Contains the nessus import and function tests
# In general this plugin isn't done yet.
import re
import xml.etree.ElementTree as ET

class nessus(object):
    def __init__(self):
        pass
    def loadnessusxml(self,file):
        # Validate the file being passed to us matches our naming scheme
        if not re.match(r'^NESSUS\_(?:[0-9]{1,3}\.){3}[0-9]{1,3}_[0-9]{20}\.(xml|nessus)$',file):
            return
        if not type(file) is str:
            return
        #TODO: Once I get an actual nessus xml file to exam, do more input validation
        try:
            with open(file, r) as nessusfile:
                if len(nessusfile.readlines()) > 10000:
                    print("loadnessusxml: Critical: Nessus XML file has exceeded the maximum file size of the Nessus XML parser!")
                    return
        except Exception as err:
            print("loadnessusxml: Critical: Error while loading nessus xml file during input validation due to: %s" % err)
        try:
            nessusxml = ET.parse(file)
        except Exception as err:
            print("loadnessusxml:Error: %s" % err)
        return nessusxml

    def nessusxml2dict(self,nessusxml):
        if not "xml" in str(type(nessusxml)):
            print("nessusxml2dict:Critical: object received is not an xml object!")
        nessusobj = {}
        nessusobj['scan'] = {'type':'nessus'}
        top = nessusxml.getroot()
        # XML format pulled from https://static.tenable.com/documentation/nessus_v2_file_format.pdf
        for hosts in top.iter('ReportHost'):
            host = hosts.get('name')
            nessusobj[host] = {}
            nessusobj[host]["ip"] = host
            for tag in hosts.iter('tag'):
                if str(tag.get('name')) == "operating-system":
                    nessusobj[host]['os'] = str(tag.text)
                if str(tag.get('name')) == "mac-address":
                    nessusobj[host]['mac'] == st(tag.text)
                if str(tag.get('name')) == "netbios-name":
                    nessusobj[host]['nbname'] == str(tag.text)
        return nessusobj
