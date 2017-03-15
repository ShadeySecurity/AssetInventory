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
apt-get update
apt-get install python-pip ansible -y
pip install pip --upgrade
pip install ansible --upgrade
mkdir -p /etc/ansible
cp -fu ../conf/hosts /etc/ansible
chmod 755 /etc/ansible/hosts
ansible-playbook local -c local install-pyAssetContext.yml

