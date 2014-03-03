#!/usr/bin/env python

from datetime import datetime
import subprocess


def run_simulation(defaultrng=9999, predict=False):
	if predict:
		print "{0} : Running ns-2 simulation with prediction algorithm.".format(datetime.now())
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
		print "{0} : Running ns-2 simulation without prediction algorithm.".format(datetime.now())
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
	print "{0} : ns-2 simulation complete.".format(datetime.now())


def run_prediction():
    print "{0} : Running prediction.".format(datetime.now())
    predict_process = subprocess.Popen(
        [
        	'simulation/.env2/bin/python',
        	'simulation/tran.py',
        	'simulation/manet.tr'
        ],
        stdout=open('/dev/null', 'w'),
        stderr=open('/dev/null', 'w'))
    predict_process.wait()
    print "{0} : Prediction generated.".format(datetime.now())


if __name__ == "__main__":
	"""
	1. Create an experiment routine which: 
	  a. Runs ns-2 with nodes sending data as normal and produces trace files.
	  b. Runs predict to generate sets of predict data.
	  c. Runs ns-2 with an augmented throughput/link at particular times based on prediction that a link will fail with CBK
	"""

	rng = 9999
	run_simulation(defaultrng=rng, predict=False)
	run_prediction()
	run_simulation(predict=True)
