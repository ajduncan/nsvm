nsvm
====

# Network Simulation of Virtual Manets #

This experiment uses ns-2 to simulate a mobile ad-hoc network using AODV, 
then analyzes the trace file to generate a prediction of when a node in the
network will fall out of range from another.  The simulation runs once again
using the result of the prediction algorithm, then the results are compared
to generate a true positive and false positive rate.

## Setup Requirements ##

The actual steps to get the experiment working are documented fully under
the provision.sh script, which Vagrant uses to conduct an experiment.

This project was developed under Ubuntu 13.10 and can also run under Ubuntu 12.04.

Refer to [this guide](http://www.nsnam.com/2013/10/installing-network-simulator-2-ns-235.html "ubuntu install")

Ubuntu 13.10 with packages: ns2, tk, tk-dev, tcl, tcl-dev, xgraph.

ns-2.35 [source code](http://sourceforge.net/projects/nsnam/files/ns-2/2.35/ns-src-2.35.tar.gz/download "Source")

You also need to install python dependencies:

    $ sudo apt-get install python-virtualenv python-pip
    $ sudo apt-get build-dep python-numpy python-scipy
    $ cd simulation
    $ virtualenv -p python2 ~/nsvm_env2
    $ . ~/nsvm_env2/bin/activate
    (.env2)$ pip install numpy 
    (.env2)$ pip install scipy 
    (.env2)$ pip install pandas
    (.env2)$ pip install -r requirements.txt
    (.env2)$ python tran.py

## Running the Simulation ##

The best way to run the experiment is to use vagrant, simply execute the 
following from the project root:

    $ vagrant up

To run the experiment again while the vm is running:

    $ vagrant provision

To rebuild all dependencies and run the experiment again:

    $ vagrant halt
    $ vagrant destroy
    $ vagrant up

## Running the Simulation Manually ##

The network simulation is defined interactively (if desired) by running `ns simulation.tcl' in the simulation folder.

    $ vagrant ssh

    $ cd /vagrant/simulation
	$ ns simulation.tcl

## Results ##

The project stores results under the results folder, and includes the trace files and predict
files.  If you're using vagrant to run the experiment, this folder will be updated with data after
the experiment concludes.

## Report Generation ##

Statistics on dropped packets, protocols, etc can be gathered and reported by parsing the simulation.tr file, using
the tran.py utility.

    $ vagrant ssh

	$ cd /vagrant
	$ . /home/vagrant/env2/bin/activate
	(env2) $ pip install -r requirements.txt
	$ python simulation/tran.py results/simulation.tr results/predict.tcl results/predict.txt

## ns-2 Tutorials ##

The simulator of choice is currently ns-2.  Example TCL code is provided from
http://www.isi.edu/nsnam/ns/tutorial/ and used under tutorials/ns2 for reference.

Notes:

* example3.tcl: Don't forget to click the re-layout button to see the correct topology.
* VII - http://www.isi.edu/nsnam/ns/tutorial/nsnew.html references an old branch of the code.
In order to make this work, you must review the changes to packet.h, etc.
* VIII & IX - You also need the ns source and tcl/mobility.  

## ns-2 New Protocol Notes ##

See: http://www.isi.edu/nsnam/ns/tutorial/nsnew.html
See also: http://elmurod.net/en/index.php/archives/157
and: http://www.nsnam.com/2013/07/wsn-flooding-routing-protocol-wfrp-in.html

This is applicable when implementing a new or existing protocol from research to compare
results against experiments.

## ns-2 Examples ##

The Ad-Hoc On-Demand Distance Vector routing, which this project uses to simulate 
the operation of a MANET, is implemented as an example AODV tcl from revision 11 
of the ns-2.34-allinone project, provided under examples/aodv.tcl.

To run the example:

    $ cd examples
    $ ns aodv.tcl

