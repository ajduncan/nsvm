#!/usr/bin/env python

from datetime import datetime
import os
import random
import re
import subprocess

# Simple regex to extract the number of dropped packets in the tran.py analysis of ns-2 simulation.
re_droppedpacket_report = re.compile("^Dropped packet size for ")
re_node_identifier = re.compile("for (\d+):")
re_dropped = re.compile(": (\d+)")


def setup_experiment():
    """
    Ensure that certain conditions are met before running a simulation.
    """

    if not os.path.exists('/vagrant/results/without_prediction'):
        os.makedirs('/vagrant/results/without_prediction')

    if not os.path.exists('/vagrant/results/with_prediction'):
        os.makedirs('/vagrant/results/with_prediction')


def run_simulation(defaultrng=9999, predict=False):
    """
    Run an ns-2 simulation using the compiled version of ns-2.

    :param defaultrng:
        If provided, this is used to control the random seed ns-2 uses in a simulation.
    :param predict:
        If provided, this is used to specify if we are running ns-2 with the augmented
        rules which are derived from ``run_prediction``.
    """

    if predict:
        print "{0} : Running ns-2 simulation with prediction algorithm.".format(datetime.now())
        print "RNG is {0}".format(defaultrng)
        with open(os.devnull, 'w') as devnull:
            simulation_process = subprocess.Popen(
                [
                    '/home/vagrant/ns-allinone-2.35/bin/ns',
                    'simulation/simulation.tcl',
                    '--noinput',
                    '--defaultrng',
                    '{0}'.format(defaultrng),
                    '--results',
                    'with_prediction',
                    '--predict'
                ],
                stdout=devnull,
                stderr=devnull)
    else:
        print "{0} : Running ns-2 simulation without prediction algorithm.".format(datetime.now())
        print "RNG is {0}".format(defaultrng)
        with open(os.devnull, 'w') as devnull:
            simulation_process = subprocess.Popen(
                [
                    '/home/vagrant/ns-allinone-2.35/bin/ns',
                    'simulation/simulation.tcl',
                    '--noinput',
                    '--defaultrng',
                    '{0}'.format(defaultrng),
                    '--results',
                    'without_prediction'
                ],
                stdout=devnull,
                stderr=devnull)

    simulation_process.wait()
    print "{0} : ns-2 simulation complete.".format(datetime.now())


def run_prediction(virtualenv='~/.env2/'):
    """
    Analyze the results under results/without_prediction/simulation.tr, to create
    a predict.tcl file under results/with_prediction/predict.tcl and log a report in
    results/without_predict.txt

    :param virtualenv:
        If provided, this specifies the base virtual environment path to use.
    """

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
    predict_process.wait()
    print "{0} : Prediction generated.".format(datetime.now())


def generate_prediction_report(virtualenv='~/.env2/'):
    """
    Generate a report by analyzing the trace file in results/with_prediction/simulation.tr 
    to produce statistics under results/with_predict.txt.  If using tran.py, we also specify
    that the prediction made should be stored under results/new_predic.tcl.  This predict file
    is not used in the experiment.

    :param virtualenv:
        If provided, this specifies the base virtual environment path to use.
    """

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

def compare_reports(without_prediction, with_prediction, max_nodes):
    """
    Provided two reports and the maximum number of nodes to compare, return a dictionary
    of nodes with the dropped packets without preidction and with prediction.

    :param without_prediction:
        The path to the dropped packet report for the simulation run without the prediction.
    :param with_prediction:
        The path to the dropped packet report for the simulation run with the prediction.
    """

    result = {}

    print "{0} : Analyzing results.".format(datetime.now())

    without_fh = open(without_prediction, 'r')
    without_lines = without_fh.readlines()
    without_fh.close()

    with_fh = open(with_prediction, 'r')
    with_lines = with_fh.readlines()
    with_fh.close()

    for line in without_lines:
        found = re_droppedpacket_report.search(line)
        if found:
            node = re_node_identifier.search(line)
            dropped = re_dropped.search(line)

            if int(node.group(1)) <= max_nodes/2:
                result[int(node.group(1))] = {'without': dropped.group(1)}

    for line in with_lines:
        found = re_droppedpacket_report.search(line)
        if found:
            node = re_node_identifier.search(line)
            dropped = re_dropped.search(line)

            if int(node.group(1)) <= max_nodes/2:
                result[int(node.group(1))]['with'] = dropped.group(1)

    print "{0} : Finished analyzing results.".format(datetime.now())

    return result


def run_experiment(maxnodes, rng=9999, virtualenv='/home/vagrant/nsvm_env2/'):
    """
    Run an experimental set using ns-2 to facilitate a simulation, 
    analyze the simulation to produce a prediction, then use the
    prediction to re-run the same simulation.

    :param rng:
        Used to define a random number seed for ns-2.
    :param virtualenv:
        Used to define which virtual environment to use when calling subprocess.

    """

    # Run the simulation to generate trace file data, without sourcing in any 
    # modifications.  The results of the simulation should be saved under 
    # results/without_prediction
    run_simulation(defaultrng=rng, predict=False)

    # Analyze the tracefile and make a prediction.  The resulting predict.tcl and
    # report data should be saved under results/with_prediction.
    run_prediction(virtualenv=virtualenv)

    # Run the simulation again, but this time use the predict.tcl to augment the
    # behavior of the simulation.
    run_simulation(defaultrng=rng, predict=True)

    # Generate a report from the results of running the simulation with the prediction.
    generate_prediction_report(virtualenv=virtualenv)

    # Compare the results between the simulation without prediction and with.
    results = compare_reports('results/without_predict.txt', 'results/with_predict.txt', maxnodes)

    return results


if __name__ == "__main__":
    """
    1. Create an experiment routine which:
      a. Runs ns-2 with nodes sending data as normal and produces trace files.
      b. Runs predict to generate sets of predict data.
      c. Runs ns-2 with an augmented throughput/link at particular times based 
         on prediction that a link will fail.
    """

    runs = 3
    maxnodes = 20
    virtualenv = '/home/vagrant/nsvm_env2/'

    # set the experiment up.
    setup_experiment()

    # Conduct ``runs`` runs of experiments
    for i in range(0, runs):
        dp_with = 0
        dp_without = 0
        rng = random.randint(1, 9999)
        print "{0} : Conducting experiment set {1} of {2} using rng={3}.".format(datetime.now(), i+1, runs, rng)
        result = run_experiment(maxnodes, rng, virtualenv)
        print "{0} : Finished experiment set {1} of {2}.".format(datetime.now(), i+1, runs)

        print "NODE\t\tWITHOUT_PREDICTION\t\tWITH_PREDICTION\t\tDIFFERENCE"
        for n in result.keys():
            dp_without += int(result[n]['without'])
            dp_with += int(result[n]['with'])
            difference = int(result[n]['without']) - int(result[n]['with'])
            print "{0}\t\t{1}\t\t\t\t{2}\t\t\t{3}".format(n, result[n]['without'], result[n]['with'], difference)

        # clear that dict.
        result.clear()

        print ""
        print "TOTAL (without): {0}".format(dp_without)
        print "TOTAL (with): {0}".format(dp_with)
        print ""

    print "{0} : Finished running experiments.".format(datetime.now())
