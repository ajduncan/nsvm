#!/usr/bin/env python

from __future__ import print_function
# from ggplot import *
import optparse

import predict


"""
Convert a prediction report for a given interaction of two nodes into ns-2 TCL commands.
"""


def predict_tcl(tracefile_lines, predict_file, max_nodes, src, dst):
    node_predictions = predict.build_prediction(tracefile_lines, src, dst)
    predict_fh = open(predict_file, 'a')
    if node_predictions:
        for time, prediction in node_predictions.iteritems():
            if prediction == True:
                # src here might be i = 1 .. n, but this corresponds to a tcp mapping of n/2
                # if i > n/2 then we should ignore because we're looking at dst nodes now.
                if not src > max_nodes/2:
                    print("$ns at {0} \"$tcp_({1}) set packetSize_ 1500\"".format(time, src), file=predict_fh)

"""
Print a prediction report for a given interaction of two nodes.
"""


def predict_report(tracefile_lines, stat_report_fh, src, dst):
    print(
        "################################################################################\n",
        file=stat_report_fh)
    print("Time series node predictions: {0}->{1}\n".format(
        src, dst), file=stat_report_fh)
    print(
        "################################################################################\n",
        file=stat_report_fh)
    node_predictions = predict.build_prediction(tracefile_lines, src, dst)
    if node_predictions:
        for time, prediction in node_predictions.iteritems():
            print("T: {0} P: {1}".format(
                time, prediction), file=stat_report_fh)
            print("\n\n", file=stat_report_fh)


"""
Print node statistics report for every node in the simulation,
with r = number of nodes.
"""


def stat_report(tracefile_lines, stat_report_file, r):
    stat_report_fh = open(stat_report_file, 'w')
    node_stats = predict.build_stats(tracefile_lines)

    for node in node_stats:
        print(
            "################################################################################\n",
            file=stat_report_fh)
        print("Node Stats for: {0}\n".format(node), file=stat_report_fh)
        print(
            "################################################################################\n",
            file=stat_report_fh)
        predict.ns_report(node_stats, stat_report_fh, node)

        dst = int(node) - r
        predict_report(tracefile_lines, stat_report_fh, int(node), dst)
        print("\n\n", file=stat_report_fh)


if __name__ == "__main__":

    parser = optparse.OptionParser(
        usage="%prog [options] file", version="%prog 0.1")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("incorrect number of arguments")

    tracefile_lines = predict.get_tracefile_data(args[0])
    predict_file = args[1]
    stat_report_file = args[2]

    stat_report(tracefile_lines, stat_report_file, 20)
    # clear the predict report
    predict_fh = open(predict_file, 'w')
    predict_fh.close()
    for i in range(0, 19):
        predict_tcl(tracefile_lines, predict_file, 19, i, 19 - i)

    # assuming we have r nodes, of which one half is futzing around with the other;
    # r = 20
    # for src in range(1, r/2):
    #     dst = r - src
    #     predict_report(tracefile_lines, src, dst)


"""
    p = ggplot(aes(x='date', y='beef'), data=meat) + \
        geom_point(color='lightblue') + \
        stat_smooth(span=.15, color='black', se=True) + \
        ggtitle("Beef: It's What's for Dinner") + \
        xlab("Date") + \
        ylab("Head of Cattle Slaughtered")
    ggsave(p, "beef.png")
    print p
"""
