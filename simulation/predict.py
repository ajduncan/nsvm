#!/usr/bin/env python

"""
Link failure prediction analysis provided input file in nstrace format.
"""

from __future__ import print_function

# import namtrace as trace
import nstrace as trace


"""
Get tracefile data as lines from the file.
"""


def get_tracefile_data(filename):
    tracefile_fd = open(filename, 'r')
    tracefile_lines = tracefile_fd.readlines()
    return tracefile_lines


"""
Generate node statistics given trace file in nstrace format.
"""


def build_stats(tracefile_data):
    nodes = trace.get_nodes(tracefile_data)
    node_stats = {}
    for node in nodes:
        (d, r, s, f, dp_features) = trace.get_packet_statistics(
            tracefile_data, node)
        node_stats[node] = (sum(d), sum(r), sum(s), sum(f), dp_features)
    return node_stats


"""
Provided node stats, and node_id, generate a report.
"""


def ns_report(node_stats, stat_report_fh, node_id):
    print("Dropped packet size for {0}: {1}".format(
        node_id, node_stats[node_id][0]), file=stat_report_fh)
    print("Time sequenced reason for dropped packets: ", file=stat_report_fh)
    for feature in node_stats[node_id][4]:
        for k, v in feature.iteritems():
            print("{0}: {1}".format(k, v), file=stat_report_fh)

    print("Received packet size for {0}: {1}".format(
        node_id, node_stats[node_id][1]), file=stat_report_fh)
    print("Sent packet size for {0}: {1}".format(
        node_id, node_stats[node_id][2]), file=stat_report_fh)


"""
Provided tracefile data in nstrace format, predict if dst node will fall out of range from src.
"""


def build_prediction(tracefile_lines, src, dst):
    tcp_packet_size = 1000
    prediction = {}
    throughput_history = []
    avg_throughput_history = 0

    events = trace.get_prediction_events(tracefile_lines, src, dst)
    for time, packet_size in events.iteritems():
        # build a history
        throughput = (int(packet_size) * 8)/tcp_packet_size
        throughput_history.append(throughput)
        if len(throughput_history) > 1:
            avg_throughput_history = reduce(
                lambda x, y: x + y, throughput_history) / len(throughput_history)

            # make a prediction :\
        if throughput <= avg_throughput_history:
            prediction[time] = False
        else:
            prediction[time] = True

        # eventually, use past true positives if we haven't moved?

        return prediction


if __name__ == "__main__":

    print("Just a library.")
