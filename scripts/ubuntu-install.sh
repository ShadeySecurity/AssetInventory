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
apt-get install python-pip wget unzip -yf
wget http://www.web2py.com/examples/static/web2py_src.zip --directory-prefix=/opt
unzip /opt/web2py_src.zip
mkdir -P /opt/web2py/applications/SimpleAssetInventory
cp -rfu ../* /opt/web2py/applications/SimpleAssetInventory
chown $USER:$USER /opt/web2py -R
pip install -r requirements.txt
cp -fu ./cronrun.py /etc/cron.d/
(crontab -l ; echo "*/1 * * * * /etc/cron.d/cronrun.py")  | uniq - | crontab -
