#!/bin/bash
# run this file within the directory to create your virtual environment properly
#
$ ./setup_environment.sh
echo "Cloning the netbox-install repo"
git clone https://github.com/ntwauto/netbox-install.git
cd netbox-install/
echo "Creating a local virtual environment venv"
python3 -m venv venv
echo "Sourcing the virtual environment"
source venv/bin/activate
echo "Updating pip wheel and setuptools"
pip install -U pip wheel setuptools
echo "Installing required python packages"
pip install -r requirements.txt
echo "Copy environment variable env.example to .env"
cp env.example .env
