#!/bin/sh

echo "
########################################################################
                      _     _             
 _ __  _ __ _____   _(_)___(_) ___  _ __  
| '_ \| '__/ _ \ \ / / / __| |/ _ \| '_ \ 
| |_) | | | (_) \ V /| \__ \ | (_) | | | |
| .__/|_|  \___/ \_/ |_|___/_|\___/|_| |_|
|_|                                       

Author: Andrew Duncan <ajduncan@gmail.com>, <Andrew-Duncan@utc.edu>
Project: nsvm
Experiment: Node out of range prediction

########################################################################
"


# Update and upgrade
echo "Updating system..."
apt-get update > /dev/null 2>&1
echo "Upgrading system packages..."
apt-get -y upgrade > /dev/null 2>&1

# Install system dependencies.
echo "Installing system dependencies: python-virtualenv, python-pip, tcl, tcl-dev, ns2..."
apt-get -y install python-virtualenv python-pip tcl tcl-dev ns2 > /dev/null 2>&1

echo "Installing ns-2 build dependencies: build-essential, autoconf, automake, libxmu-dev, dpkg-dev, libx11-dev..."
apt-get -y install build-essential autoconf automake libxmu-dev dpkg-dev libx11-dev > /dev/null 2>&1

# Build pip dependencies for numpy and scipy
echo "Building system dependencies for application dependencies: python-numpy, python-scipy."
apt-get -y build-dep python-numpy python-scipy > /dev/null 2>&1

# Build ns-2
if [ ! -d "/home/vagrant/ns-allinone-2.35" ];
then
	cd /home/vagrant/
	echo "Downloading ns-2.35 from sourceforge.net."
	wget "http://downloads.sourceforge.net/project/nsnam/allinone/ns-allinone-2.35/ns-allinone-2.35.tar.gz?r=&ts=1395619377&use_mirror=tcpdiag"
	mv ns-allinone*.tar.gz* ns-allinone-2.35.tar.gz
	echo "Uncompressing tarball."
	tar xzf ns-allinone-2.35.tar.gz
	echo "Adding environment variables to .bashrc..."
	cat /vagrant/bashrc_template.txt >> /home/vagrant/.bashrc
	echo "building ns-2..."
	cd /home/vagrant/ns-allinone-2.35
	/home/vagrant/ns-allinone-2.35/install
	chown -R vagrant:vagrant /home/vagrant/ns-allinone-2.35
fi

# Create a virtual environment for nsvm
if [ ! -d "/home/vagrant/nsvm_env2" ];
then
	echo "Creating application virtual environment."
	sudo -u vagrant virtualenv -p python2 /home/vagrant/nsvm_env2 > /dev/null 2>&1
fi

# Install all the dependencies in the order which satisfies requirements.
if [ -d /home/vagrant/nsvm_env2 ];
then
	echo "Installing appliction dependencies."
	echo "Installing numpy dependency..."
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install numpy > /dev/null 2>&1
	echo "Installing scipy dependency..."
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install scipy > /dev/null 2>&1
	echo "Installing pandas dependency..."
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install pandas > /dev/null 2>&1
	echo "Installing requirements for nsvm simulation..."
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install -r /vagrant/simulation/requirements.txt > /dev/null 2>&1
	echo "Done installing all application dependencies."
fi

# Remove previous timestamp-started file.
if [ -f /home/vagrant/started ];
then
	echo "Clearing previous started file."
	rm /home/vagrant/started
fi

# Create started file with timestamp.
touch /home/vagrant/started
echo "Timestamp file created under /home/vagrant/started"

if [ -d /home/vagrant/nsvm_env2 ] && [ -d /vagrant/simulation ] && [ -f /vagrant/nsvm.py ];
then
	echo "
########################################################################
Running experiment...
"

	cd /vagrant
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/python /vagrant/nsvm.py
	echo "

Experiment complete.
########################################################################
"

fi
