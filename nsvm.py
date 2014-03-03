#!/usr/bin/env python

import subprocess


def run_simulation(defaultrng=9999, predict=False):
	if predict:
		print "Running ns-2 simulation with prediction algorithm."
		manet_process = subprocess.Popen(
			[
		    	'ns',
		    	'simulation/manet.tcl',
		    	'--noinput',
		    	'--defaultrng {0}'.format(defaultrng),
		    	'--predict'
		    ],
		    stdout=open('/dev/null', 'w'),
		    stderr=open('/dev/null', 'w'))
	else:
		print "Running ns-2 simulation without prediction algorithm."
		manet_process = subprocess.Popen(
			[
		    	'ns',
		    	'simulation/manet.tcl',
		    	'--noinput',
		    	'--defaultrng {0}'.format(defaultrng)
		    ],
		    stdout=open('/dev/null', 'w'),
		    stderr=open('/dev/null', 'w'))

	manet_process.wait()
	print "ns-2 simulation complete."


def run_prediction():
    print "Running prediction."
    predict_process = subprocess.Popen(
        [
        	'simulation/.env2/bin/python',
        	'simulation/tran.py',
        	'simulation/manet.tr'
        ],
        stdout=open('/dev/null', 'w'),
        stderr=open('/dev/null', 'w'))
    predict_process.wait()
    print "Prediction generated."


if __name__ == "__main__":
	"""
	1. Create an experiment routine which: 
	  a. Runs ns-2 with nodes sending data as normal and produces trace files.
	  b. Runs predict to generate sets of predict data.
	  c. Runs ns-2 with an augmented throughput/link at particular times based on prediction that a link will fail with CBK
	"""

	run_simulation()
	run_prediction()
	run_simulation(predict=True)
