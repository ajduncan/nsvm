nsvm
====

# Network Simulation of Virtual Manets #

This project contains work toward manet simulations.  The scope of the
project is to create a flexible system to run mobile ad-hoc network (MANET) 
simulations and then tweak the result of the simulation based on recent 
research.

## Setup requirements ##

Ubuntu 13.10 with packages: ns2, tk, tk-dev, tcl, tcl-dev, xgraph.

ns-2.35 [source code](http://sourceforge.net/projects/nsnam/files/ns-2/2.35/ns-src-2.35.tar.gz/download "Source")

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

