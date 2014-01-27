nsvm
====

# Network Simulation of Virtual Manets #

This project contains work toward manet simulations.  The scope of the
project is to create a flexible system to run mobile ad-hoc network (MANET) 
simulations and then tweak the result of the simulation based on recent 
research.

## Setup Requirements ##

This project was developed under Ubuntu 13.10 and is untested in other 
versions of Ubuntu.

Refer to [this guide](http://www.nsnam.com/2013/10/installing-network-simulator-2-ns-235.html "ubuntu install")

Ubuntu 13.10 with packages: ns2, tk, tk-dev, tcl, tcl-dev, xgraph.

ns-2.35 [source code](http://sourceforge.net/projects/nsnam/files/ns-2/2.35/ns-src-2.35.tar.gz/download "Source")

You also need to install python dependencies:

    $ sudo apt-get install python-virtualenv python-pip
    $ sudo apt-get build-dep python-numpy python-scipy
    $ cd simulation
    $ virtualenv -p python2 .env2
    $ . .env2/bin/activate
    (.env2)$ pip install numpy 
    (.env2)$ pip install scipy 
    (.env2)$ pip install pandas
    (.env2)$ pip install -r requirements.txt
    $ python tran.py

## Running the Simulation ##

The manet simulation is defined interactively (if desired) by running `ns manet.tcl' in the simulation folder.

	$ cd simulation
	$ ns manet.tcl

## Report Generation ##

Statistics on dropped packets, protocols, etc can be gathered and reported by parsing the manet.tr file, using
the tran.py utility.

	$ cd simulation
	$ . env2/bin/activate
	(env2) $ pip install -r requirements.txt
	$ python tran.py manet.tr

## ns-2 Tutorials ##

The simulator of choice is currently ns-2.  Example TCL code is provided from
http://www.isi.edu/nsnam/ns/tutorial/ and used under tutorials/ns2 for reference.

Notes:

* example3.tcl: Don't forget to click the re-layout button to see the correct topology.
* VII - http://www.isi.edu/nsnam/ns/tutorial/nsnew.html references an old branch of the code.
In order to make this work, you must review the changes to packet.h, etc.
* VIII & IX - You also need the ns source and tcl/mobility.  

## ns-2 Examples ##

The Ad-Hoc On-Demand Distance Vector routing, which this project uses to simulate 
the operation of a MANET, is implemented as an example AODV tcl from revision 11 
of the ns-2.34-allinone project, provided under examples/aodv.tcl.

To run the example:

    $ cd examples
    $ ns aodv.tcl

