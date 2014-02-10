#!/usr/bin/env python

# from ggplot import *
import optparse

# import namtrace as trace
import nstrace as trace


if __name__ == "__main__":

    parser = optparse.OptionParser(usage = "%prog [options] file", version = "%prog 0.1")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    tracefile_fd = open(args[0], 'r')
    tracefile_lines = tracefile_fd.readlines()

    nodes = trace.get_nodes(tracefile_lines)
    node_stats = {}
    for node in nodes:
        (d, r, s, f, dp_features) = trace.get_packet_statistics(tracefile_lines, node)
        node_stats[node] = (sum(d), sum(r), sum(s), sum(f), dp_features)

    print "Dropped packet size for {0}: {1}".format(0, node_stats[0][0])
    print "Time sequenced reason for dropped packets: {}".format(node_stats[0][4])
    print "Received packet size for {0}: {1}".format(0, node_stats[0][1])
    print "Sent packet size for {0}: {1}".format(0, node_stats[0][2])

    print "Dropped packet size for {0}: {1}".format(19, node_stats[19][0])
    print "Time sequenced reason for dropped packets: {}".format(node_stats[19][4])
    print "Received packet size for {0}: {1}".format(19, node_stats[19][1])
    print "Sent packet size for {0}: {1}".format(19, node_stats[19][2])

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
