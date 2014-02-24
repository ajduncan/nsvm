#!/usr/bin/env python

""" 
Link failure prediction analysis provided input file in nstrace format.
"""


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
        (d, r, s, f, dp_features) = trace.get_packet_statistics(tracefile_data, node)
        node_stats[node] = (sum(d), sum(r), sum(s), sum(f), dp_features)
    return node_stats


"""
Provided node stats, and node_id, generate a report.
"""
def ns_report(node_stats, node_id):
    print "Dropped packet size for {0}: {1}".format(node_id, node_stats[node_id][0])
    print "Time sequenced reason for dropped packets: "
    for feature in node_stats[node_id][4]:
        for k, v in feature.iteritems():
            print "{0}: {1}".format(k, v)

    print "Received packet size for {0}: {1}".format(node_id, node_stats[node_id][1])
    print "Sent packet size for {0}: {1}".format(node_id, node_stats[node_id][2])


"""
Provided tracefile data in nstrace format, predict if dst node will fall out of range from src.
"""
def build_prediction(tracefile_lines, src, dst):
    prediction = {}
    ttl_history = []
    avg_ttl_history = 0

    events = trace.get_prediction_events(tracefile_lines, src, dst)
    for time, ttl in events.iteritems():
    	# build a history :C
    	ttl_history.append(ttl)
    	if len(ttl_history) > 1:
	    	avg_ttl_history = reduce(lambda x, y: x + y, ttl_history) / len(ttl_history)

	    # make a prediction :\
    	if ttl <= avg_ttl_history:
    		prediction[time] = False
    	else:
    		prediction[time] = True

    	# eventually, use past true positives if we haven't moved?

	return prediction


if __name__ == "__main__":

	print "Just a library."
