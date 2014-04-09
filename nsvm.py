#!/usr/bin/env python

from datetime import datetime
import subprocess


def run_simulation(defaultrng=9999, predict=False):
    if predict:
        print "{0} : Running ns-2 simulation with prediction algorithm.".format(datetime.now())
        print "RNG is {0}".format(defaultrng)
        simulation_process = subprocess.Popen(
            [
                '/home/vagrant/ns-allinone-2.35/bin/ns',
                'simulation/simulation.tcl',
                '--noinput',
                '--defaultrng {0}'.format(defaultrng),
                '--results with_prediction',
                '--predict'
            ],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
    else:
        print "{0} : Running ns-2 simulation without prediction algorithm.".format(datetime.now())
        print "RNG is {0}".format(defaultrng)
        simulation_process = subprocess.Popen(
            [
                '/home/vagrant/ns-allinone-2.35/bin/ns',
                'simulation/simulation.tcl',
                '--noinput',
                '--defaultrng {0}'.format(defaultrng),
                '--results without_prediction'
            ],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))

    simulation_process.wait()
    print "{0} : ns-2 simulation complete.".format(datetime.now())


def run_prediction(virtualenv='~/.env2/'):
    print "{0} : Running prediction.".format(datetime.now())
    python_interpreter = virtualenv + 'bin/python'
    predict_process = subprocess.Popen(
        [
            python_interpreter,
            'simulation/tran.py',
            'results/without_prediction/simulation.tr',
            'results/with_prediction/predict.tcl',
            'results/without_predict.txt'
        ])
    #,
    #    stdout=open('/dev/null', 'w'),
    #    stderr=open('/dev/null', 'w'))
    predict_process.wait()
    print "{0} : Prediction generated.".format(datetime.now())


def generate_report(virtualenv='~/.env2/'):
    print "{0} : Generating report.".format(datetime.now())
    python_interpreter = virtualenv + 'bin/python'
    report_process = subprocess.Popen(
        [
            python_interpreter,
            'simulation/tran.py',
            'results/with_prediction/simulation.tr',
            'results/new_predict.tcl',
            'results/with_predict.txt'
        ])
    report_process.wait()
    print "{0} : Report generated.".format(datetime.now())


if __name__ == "__main__":
    """
    1. Create an experiment routine which:
      a. Runs ns-2 with nodes sending data as normal and produces trace files.
      b. Runs predict to generate sets of predict data.
      c. Runs ns-2 with an augmented throughput/link at particular times based on prediction that a link will fail with CBK
    """

    # Consider making the following two settings arguments instead
    rng = 9999
    virtualenv = '/home/vagrant/nsvm_env2/'

    run_simulation(defaultrng=rng, predict=False)
    run_prediction(virtualenv=virtualenv)
    run_simulation(defaultrng=rng, predict=True)
    generate_report(virtualenv=virtualenv)
