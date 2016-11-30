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
mkdir -P /opt/web2py/applications/SimpleAssetInventory
if [ $1 == "offline"]; then
    # Use local cached version... may or may not work... not ideal
    unzip ./external/*.zip
    tar -xvzf ./External/*.tar.gz
    dpkg -i ./External/nmap_6.40-0.2ubuntu1_amd64.deb
    cp -fu ./External/web2py /opt/
    python ./External/python-libnmap-master/setup.py install
    python ./External/python-nmap-0.6.1/setup.py install
else
    # Pull the latest and greatest of everything directly from our friends online
    apt-get install python-pip wget unzip -yf
    wget http://www.web2py.com/examples/static/web2py_src.zip --directory-prefix=/opt 
    pip install -r requirements.txt
    unzip /opt/web2py_src.zip -d /opt/
fi
# Now to move in to a nice little setup home
cp -rfu ../* /opt/web2py/applications/SimpleAssetInventory
# TEll everyone we own this place
chown $USER:$USER /opt/web2py -R
# Put our main man at the head of the agency
cp -fu ./cronrun.py /etc/cron.d/
# Update cron to check on our main man every minutes... he has problems now
(crontab -l ; echo "*/1 * * * * /etc/cron.d/cronrun.py")  | uniq - | crontab -
