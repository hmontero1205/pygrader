#!/bin/bash

# install apt packages
sudo apt install -y $(cat apt-packages.txt)

# install bat via deb package as it isn't available in Debian 10
wget https://github.com/sharkdp/bat/releases/download/v0.15.4/bat_0.15.4_amd64.deb
sudo dpkg -i ./bat_0.15.4_amd64.deb
rm bat_0.15.4_amd64.deb

# install python dependencies
pip3 install -r requirements.txt
