nsvm
====

# Network Simulation of Vehicular Manets #

This project contains work toward vehicular manet simulations.  The scope of the
project is to create a flexible system to run vehicular mobile ad-hoc network
(MANET) simulations and then tweak the result of the simulation based on recent 
research.

A vehicular MANET has interesting properties, in that the z coordinate does not
typically change that much, and the typical physical paths of nodes in the 
network can be constrained to a road topology.  

## Setup requirements ##

Ubuntu 13.10 with packages: ns2, tk, tk-dev, tcl, tcl-dev, xgraph.

ns-2.35 [source code](http://sourceforge.net/projects/nsnam/files/ns-2/2.35/ns-src-2.35.tar.gz/download "Source")

## ns2 tutorials ##

The simulator of choice is currently ns2.  Example TCL code is provided from
http://www.isi.edu/nsnam/ns/tutorial/ and used under tutorials/ns2 for reference.

Notes:

* example3.tcl: Don't forget to click the re-layout button to see the correct topology.
* VII - http://www.isi.edu/nsnam/ns/tutorial/nsnew.html references an old branch of the code.
In order to make this work, you must review the changes to packet.h, etc.
* VIII & IX - You also need the ns source and tcl/mobility.  

