#!/usr/bin/env bash
####################
# Script Name: ubuntu_install.sh
# Description: A simple bash install script for ubuntu
# Authors: ShadeyShades
# Requires: apt-get pip
####################

# Make sure we are root / sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get install python-pip -yf
pip install -r requirements.txt
cp -fu ./cronrun.py /etc/cron.d/
(crontab -l ; echo "*/1 * * * * /etc/cron.d/cronrun.py")  | uniq - | crontab -
