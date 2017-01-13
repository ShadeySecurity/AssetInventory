#!/usr/bin/python

# NAME: PYNMAPASSET
# DISPLAYNAME: NMAP
# FUNCTIONS: IMPORT,EXECUTE
# AUTHOR: ShadeyShades
# DESCRIPTION: Import nmap xml and execute nmap scans into standard format
# DISABLE: FALSE

######################
# Name: pynmap.py
# Description:  A helper class which allows us to ingest, read, and convert NMap XML files/objects.
# Authors: ShadeyShades
######################

import re
import xml.etree.ElementTree as ET


class nmap(object):
    def __init__(self):
        # Dont have anything for here yet.
        pass
    ######################
    # Name:         loadnmapxml
    # Description:  A script which loads an NMAP XML into an object
    # Requires:     xml, re
    # Input:        file - NMap XML File to be read
    # Output:       nmapxml - Object of the NMap XML file
    ######################

    def loadnmapxml(self, filename):
        # Validate the file being passed to us matches our naming scheme
        if not re.match(r'^NMAP\_(?:[0-9]{1,3}\.){3}[0-9]{1,3}_[0-9]{20}\.(xml|nmap)$',file):
            return
        # Validate the file headers are what we expect and that the file isn't too long.
        try:
            with open(filename,'r') as nmapfile:
                counter = 0
                nmaplist = nmapfile.readlines()
                for line in nmaplist:
                    counter += 1
                    if not line == '<?xml version="1.0" encoding="UTF-8"?>' and counter == 1:
                        return
                    elif not line == "<!DOCTYPE nmaprun>" and counter == 2:
                        return
                    elif not line == '<?xml-stylesheet href="file:///usr/bin/../share/nmap/nmap.xsl" type="text/xsl"?>' and counter == 3:
                        return
                    elif not re.match(r'^^<\!\-\-\ Nmap\s[0-9]{1}\.[0-9]{1,2}\sscan\sinitiated\s[MTWFS]{1}[aneduitohr]{2}\s[JFMASOND]{1}[nbryalgptvoceu]{2}\s[0-3]{1}[0-9]{1}\s[0-2]{2}\:[0-5]{1}[0-9]{1}\:[0-6]{1}[0-9]{1}\s[1-2][09][129][0-9]\sas\:\snmap\s.*\-\->$',line)  and counter == 4:
                        return
                    elif not re.match(r'^<nmaprun\sscanner\=\"nmap\"\sargs\=\"nmap[-&#A-Za-z0-9\=\;\\\/ \.]*\"\sstart\=\"[0-9]{10}\"\sstartstr=\"[MTWFS]{1}[aneduitohr]{2}\s[JFMASOND]{1}[nbryalgptvoceu]{2}\s[0-3]{1}[0-9]{1}\s[0-2]{2}\:[0-5]{1}[0-9]{1}\:[0-6]{1}[0-9]{1}\s[1-2][09][129][0-9]\"\sversion\=\"[0-9]{1,2}\.[0-9]{0,4}\"\sxmloutputversion\=\"[0-9]{1,2}\.[0-9]{0,4}\">$',line) and counter==5:
                        return
                    elif counter > 10000:
                        print("ImportNmapXML: Critical: Too many results in file!")
                        break
                nmapfile.close()
        except Exception as err:
            print("loadnmapxml: ERROR: While validating XML file, following error happened: %s" % err)
            return
        try:
            # Parse xml file into object
            nmapxml = ET.parse(file)
        except Exception as err:
            print("loadnmapxml: Error: Unable to load XML file to be parsed due to: %s" % err )
        return nmapxml

    ###########################
    # Name:         nmapxml2dict
    # Description:  Takes the nmap object and converts to nested dictionary object
    # Requires:     csv
    # Input:        nmapxml - nmap xml object
    # Ouput:        nmapobj - nmap nested dict object
    # Sample result: {'127.0.0.1' : { 'ip':'127.0.0.1', 'hostnames':['localhost'],'os':'Linux','os_version':'2.6.x','22':{'state':'open','protocol':'tcp','name':'ssh'}}}
    ############################
    def nmapxml2dict(self, nmapxmlobj):
        if not "xml" in str(type(nmapxmlobj)):
            return
        top = nmapxmlobj.getroot()
        nmapdict = {}
        for host in top.iter('host'):
            for status in host.iter('status'):
                state = status.get('state')
            if state == 'down':
                continue
            for address in host.iter('address'):
                addrtype = address.get('addrtype')
                if "ip" in addrtype:
                    ip = str(address.get("addr"))
                    nmapdict[ip] = {}
                    nmapdict[ip]['ip'] = ip
                elif addrtype == "mac":
                    nmapdict[ip]['mac'] = str(address.get('addr'))
                    nmapdict[ip]['vendor'] = str(address.get('vendor'))
            for port in host.iter('port'):
                portid = str(port.get('portid'))
                nmapdict[ip]['port'] = {}
                nmapdict[ip]['port'][portid] = {}
                nmapdict[ip]['port'][portid]['protocol'] = str(port.get("protocol"))
                for state in port.iter('state'):
                    nmapdict[ip]['port'][portid]['state'] = str(state.get('state'))
                for service in port.iter('service'):
                    nmapdict[ip]['port'][portid]['name'] = str(service.get('name'))
                    nmapdict[ip]['port'][portid]['product'] = str(service.get('product'))
                    nmapdict[ip]['port'][portid]['version'] = str(service.get('version'))
                for script in port.iter('script'):
                    nmapdict[ip]['port'][portid]['banner'] = str(script.get('output'))
                    nmapdict[ip]['port'][portid]['banner_src'] = str(script.get('id'))
            for os in host.iter('os'):
                for osmatch in os.iter('osmatch'):
                    if "Linux" in str(osmatch.get('osfamily')):
                        nmapdict[ip]['os'] = str(osmatch.get('osfamily'))
                        nmapdict[ip]['os_version'] = str(osmatch.get('osgen'))
            for hostnames in host.iter('hostnames'):
                nmapdict[ip]['hostnames'] = []
                for hostname in hostnames.iter('hostname'):
                    nmapdict[ip]['hostnames'].append(str(hostname.get('name')))
            for distance in host.iter('distance'):
                nmapdict[ip]['distance'] = str(distance.get('value'))
            for hop in host.iter('hop'):
                nmapdict[ip]['hops'] = {}
                ttl = str(hop.get("ttl"))
                nmapdict[ip]['hops'][ttl] = {}
                nmapdict[ip]['hops'][ttl]['hostname'] = str(hop.get('host'))
                nmapdict[ip]['hops'][ttl]['rtt'] = str(hop.get('rtt'))
                nmapdict[ip]['hops'][ttl]['ip'] = str(hop.get('ipaddr'))
            for status in host.iter('status'):
                if "echo-reply" in str(status.get('reason')):
                    nmapdict[ip]['pingable'] = True
            for script in host.iter('script'):
                # Not sure at all if this is the correct way of grabbing this... but I cannot find an xml with nbstat
                if "nbstat" in script.get('name'):
                    nmapdict[ip]['nbname'] = script.get('name')
        nmapdict['scan'] = {"type":"nmap"}
        for nmaprun in top.iter('nmaprun'):
            nmapdict['scan']['command'] = str(nmaprun.get('args'))
            nmapdict['scan']['start_time'] = str(nmaprun.get('startstr'))
            nmapdict['scan']['nmap_version'] = str(nmaprun.get('version'))
        for services in top.iter('scaninfo'):
            nmapdict['scan']['ports_scanned'] = str(services.get('services'))
        for endtime in top.iter('finished'):
            nmapdict['scan']['end_time'] = str(endtime.get('timestr'))
        return nmapdict
