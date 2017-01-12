#!/usr/bin/env python
import csv
import re


class pyassetcsv(object):
    def __init__(self):
        pass
    def loadcsv(self,file):
        if not type(file) is str:
            return
        if not re.match(r'^CSV\_(?:[0-9]{1,3}\.){3}[0-9]{1,3}_[0-9]{20}\.(csv|txt)$',file):
            return
        try:
            with open(file,'rb') as csvfile:
                csvobj = csv.DictReader(csvfile)
                csvfile.close()
            csvobj['scan'] = {'type':'csv'}
        except Exception as err:
            print("readcsv: Error: %s" % err)
        return  csvobj

    def writedict2csv(self,dictobj,file,fieldnames):
        if not type(dictobj) is dict:
            return
        if not re.match(r'^CSV\_([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])_[0-9]{20}\.csv',file):
            return
        try:
            if not type(fieldnames) is list or len(fieldnames) < 1:
                with open(file,'wb') as csvfile:
                    csv.DictWriter(csv)
                    csvfile.close()
            elif type(fieldnames) is list and len(fieldnames) > 0:
                with open(file,'wb') as csvfile:
                    csv.DictWriter(dictobj,fieldnames=fieldnames)
                    csvfile.close()
            else:
                print("writecsv2dict: Critical: Invalid input for fieldnames given!")
                return
        except Exception as err:
            print("readcsv: Error: %s" % err)
        return True

    def writelist2csv(self,listobj,file):
        # We are a expecting a list with tuples
        if not type(file) is list and type(file[0]) is tuple:
            return
        if not re.match(r'^CSV\_([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])_[0-9]{20}\.csv',file):
            return
        try:
            with open(file,'wb') as csvfile:
                for line in listobj:
                    csvfile.writelines(','.join(line))
                csvfile.close()

        except Exception as err:
            print("writelist2csv:Error: %s" % err)

