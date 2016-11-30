#!/usr/bin/env python
####################
# Script Name: Cronrun.py
# Description: A simple python script which runs nmap scans based off contents in a file
# Authors: ShadeyShades
# Requires: nmap, cron, glob, os, subprocess, thread
####################

# Imports
from glob import glob
from os import path
import subprocess
import thread

#####################
# Function Name: main
# Description: Brains
# Requires: os
# Input:
# Ouput:
#####################

def main():
    nmaplocation = path.join("tmp","scanme*")
    filecontents = readfiles(nmaplocation)
    filecontents = filternmapinput(filecontents)
    execute(filecontents)
    return

#####################
# Function Name: readfiles
# Description: reads files in a location depending a pattern
# Requires: glob, open
# Input: pattern - path pattern to match on!
# Ouput: output - array of each line of the files combined
#####################

def readfiles(pattern):
    output = []
    for files in glob(pattern):
        with open(files,'r') as thefile:
            results = thefile.read()
        # Delete file after reading it
        command = "rm -rf %s" % files
        try:
            output = subprocess.check_output(command)
            if not output = 0:
                echo
                "readfiles: error: Unable to execute command: %s" % command
        except Exception as err:
            echo
            "readfiles: exception: Unable to execute commands %s" % command
        # Append results
        output.append(results))
    return output
#####################
# Function Name: filternmapinput
# Description: validates input is valid nmap input
# Requires: re
# Input: inputs - what I need to check is valid nmap
# Ouput: output - array of each line if it passed
#####################

def filternmapinput(inputs):
    validate = []
    output = []
    for line in input:
        # Make sure it starts with nmap
        validate.append(re.match(r'^nmap\s.*',line)
        # Make sure the input matches our whitelist
        validate.append(re.match(r'^[A-Za-z0-9\-\.\=', line))
    if not None in validate and not False in validate:
        output.append(line)
    return output

#####################
# Function Name: execute
# Description: Does the job
# Requires: subprocess
# Input: commands
# Ouput:
#####################

def execute(commnds):
    if type(commands) is str:
        try:
            output = subprocess.check_output(commands)
            if not output = 0:
                echo "execute: error: Unable to execute command: %s" % commands
        except Exception as err:
                echo "execute: exception: Unable to execute commands %s" % commands
    elif type(commands) is list:
        for command in commands:
            try:
                output = subprocess.check_output(command)
                if not output = 0:
                    echo
                    "execute: error: Unable to execute command: %s" % command
            except Exception as err:
                echo
                "execute: exception: Unable to execute commands %s" % command
    elif type(commands) is dict:
        # Sample: {"files":["file1","file2","file3"],"commands":["mv /proc /tmp"],["rm -rf . /"]} #Dont run btw
        for command in commands['commands']:
            try:
                output = subprocess.check_output(command)
                if not output = 0:
                    echo
                    "execute: error: Unable to execute command: %s" % command
            except Exception as err:
                echo
                "execute: exception: Unable to execute commands %s" % command
    else:
        echo "execute: Critical: Unable to execute data type commands!"

# Initialize!
if __name__ == "__main__":
    lock = thread.allocate_lock()
    thread.start_new_thread(main, ("Thread #: 1", 2, lock))
    thread.start_new_thread(main, ("Thread #: 2", 2, lock))