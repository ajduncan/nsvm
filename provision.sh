#!/bin/sh

# Update and upgrade
echo "Updating system."
apt-get update
echo "Upgrading system packages."
apt-get -y upgrade

# Install system dependencies.
echo "Installing system dependencies."
apt-get -y install python-virtualenv python-pip

# Build pip dependencies for numpy and scipy
echo "Building system dependencies for application dependencies."
apt-get -y build-dep python-numpy python-scipy

# Create a virtual environment for nsvm
echo "Creating application virtual environment."
sudo -u vagrant virtualenv -p python2 /home/vagrant/nsvm_env2

# Install all the dependencies in the order which satisfies requirements.
if [ -f /home/vagrant/nsvm_env2 ];
then
	echo "Installing appliction dependencies."
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install numpy
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install scipy
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install pandas
	sudo -u vagrant /home/vagrant/nsvm_env2/bin/pip install -r /vagrant/simulation/requirements.txt
fi

# Remove previous timestamp-started file.
if [ -f /home/vagrant/started ];
then
	rm /home/vagrant/started
fi

# Create started file with timestamp.
touch /home/vagrant/started
echo "Timestamp file created under /home/vagrant/started"