#!/usr/bin/python

# NAME: PYCISCOASSET
# DISPLAYNAME: Cisco
# FUNCTIONS: IMPORT
# AUTHOR: ShadeyShades
# DESCRIPTION: Load a cisco config file into standard format.
# DISABLE: FALSE

import re

accesslistreg = re.compile(r'^access\-list\s(?P<name>([\d]*)|(.*))(\s)?(?P<acltype>extended|standard)\s'
                           r'(?P<action>[a-z]{4,6})\s'
                           r'(?P<proto>[a-z]{2,4})\s((?P<src_netany>any)|host\s'
                           r'(?P<src_host>(?:[0-9]{1,3}\.){3}[0-9]{1,3})|(?P<src_net>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))\s'
                           r'((?P<dst_netany>any)|host\s(?P<dst_host>(?:[0-9]{1,3}\.){3}[0-9]{1,3})|'
                           r'(?P<src_sub>(?:[0-9]{1,3}\.){3}255)|(?P<dst_net>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?'
                           r'(\s)?((?P<src_sub2>(?:[0-9]{1,3}\.){3}255)|(?P<dst_net2>(?:[0-9]{1,3}\.){3}[0-9]{1,3})|'
                           r'(host\s(?P<dst_host2>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))|(?P<dst_any2>any)|(eq\s(?P<port>.*))|'
                           r'(?P<log>log))?(\s)?((?P<dst_sub3>(?:[0-9]{1,3}\.){3}255)|(eq\s(?P<port2>.*)))?')
class cisco(object):
    def __init__(self):
        # TODO: build the field here once abstraction layer is done
        self.executefields = {}
    def import_ciscoconfig(self,file):
        if not type(file) is str:
            return
        if not re.match(r'^CISCO\_(?:[0-9]{1,3}\.){3}[0-9]{1,3}_[0-9]{20}\.(conf|txt)?$',file):
            return
        with open(file,'r') as ciscofile:
            if len(ciscofile.readlines()) > 4000:
                    print("loadciscoconfig:Critical: File length of provided file is too long.")
                    return
                #TODO: Add more whitelisting checks here when I get time
            ciscolist = ciscofile.readlines()
        return  ciscolist

    def ciscoobj2dict(self,ciscoobj):
        if not type(ciscoobj) is list:
            print("ciscoobj:Critical: The cisco object expected is a list of the line of a cisco config.")
            return
        ciscodict = {'127.0.0.1':{'hosts':{'vendor':'cisco'}, 'fw_acl':{}, 'hostnames':{}, 'host_users':{}, 'vlans':{}, 'routes':{}, 'interfaces':{}}}
        counter = 0
        for line in ciscoobj:
            counter += 1
            if re.match(r'^access-list',line):
                results = accesslistreg.search(line)
                name = results.group('name')
                ciscodict['127.0.0.1']['fwl_acl'].update({'rule_name': name})
                acltype = results.group('acltype')
                ciscodict['127.0.0.1']['fwl_acl'].update({'rule_type': acltype})
                action = results.group('action')
                ciscodict['127.0.0.1']['fwl_acl'].update({'action': action})
                # Unlike above, there are multiple possible names for the same thing due to the weird regex needed for cisco acls
                ciscodict['127.0.0.1']['fwl_acl'].update({'src_net': results.group('src_host')+"/32"})                  
                if results.group('src_netany') == "any":
                    ciscodict['127.0.0.1']['fwl_acl'].update({'src_net': '0.0.0.0/0'})
                
                ciscodict['127.0.0.1']['fwl_acl'].update({'src_net': results.group('
                                                                                   : srcnet, 'dst_net': dstnet, 'args': args})
                child = ""
                childcounter = counter
                while not child == "!":
                    childcounter += 1
                    child = ciscoobj[childcounter]
            elif re.match(r'^ssid',line):
                results = re.search(r'^ssid\s(?P<ssid>.*)$',line)
                ssid = results.group('ssid')
                ciscodict['ssids'][ssid] = {}
                ciscodict['ssids'][ssid]['vlans'] = []
                ciscodict['ssids'][ssid]['auth_args'] = []
                child = ""
                childcounter = counter
                while not child == "!":
                    childcounter += 1
                    child = ciscoobj[childcounter]
                    results = re.search(r'^vlan\s(?P<vlan>[0-9]{1,3})$',child)
                    vlan = str(results.group('vlan'))
                    ciscodict['ssids'][ssid]['vlans'].append(vlan)
                    results = re.search(r'^authentication\s(?P<args>.*)$', child)
                    arg = str(results.group('args'))
                    ciscodict['ssids'][ssid]['auth_args'].append(arg)
            elif re.match(r'^version'):
                results = re.search(r'^version\s(?P<version>[0-9]{1,2}\.[0-9A-Z]{1,3}([0-9A-Za-z]{1,4})?)$',line)
                ciscodict['os_version'] = results.group('version')
            elif re.match(r'^hostname', line):
                reg = re.search(r'^hostname\s([A-Za-z0-9\.\-\_\:]{0,30})$',line)
                hostname = str(reg.group(1))
                ciscodict['hostname'] = hostname
            elif re.match(r'^aaa\sgroup\sserver\sradius',line):
                child = ""
                ciscodict['radius'] = {}
                childcounter = counter
                while not child == "!":
                    childcounter += 1
                    child = ciscoobj[childcounter]
                    reg = re.compile(r'^server\s(?P<server>((?:[0-9]{1,3}\.){3}[0-9]{1,3}))\s(auth\-port\s(?P<authport>[0-9]{1,4})\s|acct\-port\s(?P<acctport>[0-9]{1,4})){1,3}$')
                    results = reg.search(child)
                    server = str(results.group('server'))
                    acct = str(results.group('acctport'))
                    auth = str(results.group('authport'))
                    ciscodict['radius'][server] = {}
                    ciscodict['radius'][server]['acct-port'] = acct
                    ciscodict['radius'][server]['auth-port'] = auth
            elif re.match(r'^interface',line):
                ciscodict['interfaces'] = {}
                childcounter = counter
                child = ciscoobj[childcounter]
                reg = re.compile(r'^interface\s([A-Za-z]{5,19}[0-9\/]{1,8})$')
                results = reg.search(child)
                interface = str(results.group(1))
                ciscodict['interfaces'][interface] = {}
                ciscodict['interfaces'][interface]['active'] = True
                ciscodict['interfaces'][interface]['bridge_args'] = []
                ciscodict['interfaces'][interface]['switch_mode_args'] = []
                while not child == "!":
                    childcounter += 1
                    child = ciscoobj[childcounter]
                    reg = re.compile(r'^ip\saddress\s(?P<ip>((?:[0-9]{1,3}\.){3}[0-9]{1,3})|(([A-Fa-f0-9]{0,4}\:){1,8}[A-Fa-f0-9]{0,4}))((?P<cidr>\/[0-9]{1,2})|\s(?P<subnet>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))?$')
                    results = reg.search(child)
                    ciscodict['interfaces'][interface]['ip'] = str(results.group('ip'))
                    ciscodict['interfaces'][interface]['cidr'] = str(results.group('cidr'))
                    ciscodict['interfaces'][interface]['subnet'] = str(results.group('subnet'))
                    if child == "shutdown":
                        ciscodict['interfaces'][interface]['active'] = False
                    results = re.search(r'^description\s(.*)$',child)
                    ciscodict['interfaces'][interface]['description'] = str(results.group(1))
                    results = re.search(r'^speed\s(.*)$', child)
                    ciscodict['interfaces'][interface]['speed'] = str(results.group(1))
                    results = re.search(r'^duplex\s(.*)$', child)
                    ciscodict['interfaces'][interface]['duplex'] = str(results.group(1))
                    results = re.search(r'^encapsulation\s(?P<encap>[a-zA-Z0-9]*)\s(?P<vlan>[0-9]{1,3})\s(?P<mode>[a-zA-Z]*)$', child)
                    ciscodict['interfaces'][interface]['encap_proto'] = str(results.group('encap'))
                    ciscodict['interfaces'][interface]['encap_vlan'] = str(results.group('vlan'))
                    ciscodict['interfaces'][interface]['encap_mode'] = str(results.group('mode'))
                    results = re.search(r'^duplex\s(.*)$', child)
                    ciscodict['interfaces'][interface]['bridge_id'] = str(results.group('bridgeid'))
                    ciscodict['interfaces'][interface]['bridge_args'].append(str(results.group('args')))
                    results = re.search(r'^switchport\smode\s(?P<mode>(trunk|access|auto))(?P<args>.*)$', child)
                    ciscodict['interfaces'][interface]['switch_mode'] = str(results.group('mode'))
                    ciscodict['interfaces'][interface]['switch_mode_args'].append(str(results.group('args')))
