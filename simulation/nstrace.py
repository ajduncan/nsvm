#!/usr/bin/env python

""" 
A library of functions for working with ns-2 data in nstrace format.

Trace file analysis of ns-2, as defined in:

http://nsnam.isi.edu/nsnam/index.php/Manual:_Trace_and_Monitoring_Support
http://nsnam.isi.edu/nsnam/index.php/NS-2_Trace_Formats#AODV_Trace_Formats
http://www.isi.edu/nsnam/ns/doc/node289.html
http://www.isi.edu/nsnam/ns/doc/node185.html

but using re.compile() and saving the resulting regular expression object for reuse is more efficient when the expression will be used several times in a single program.

"""


import re


re_node_register = re.compile("^M (\d+.\d+) (\d+)")
re_packet_event = re.compile("-It (\w+) -Il (\d+)")

# Note, the new format is inconsistent with isi.edu's current documentation.
# example drop event:
# d -t 70.017445296 -Hs 19 -Hd 0  -Ni 19 -Nx 334.11 -Ny 138.84 -Nz 0.00 -Ne -1.000000 -Nl RTR -Nw CBK -Ma 0 -Md 0  -Ms 13 -Mt 800 -Is 19.0 -Id 0.0  -It ack -Il 40   -If 0 -Ii 9955 -Iv 30 -Pn tcp -Ps 4973 -Pa 0 -Pf 0 -Po 0 
# d -t 10.289708693 -Hs 0  -Hd 19 -Ni 0  -Nx 49.61  -Ny 305.80 -Nz 0.00 -Ne -1.000000 -Nl IFQ -Nw --- -Ma 0 -Md 13 -Ms 0  -Mt 800 -Is 0.0  -Id 19.0 -It tcp -Il 1040 -If 0 -Ii 61   -Iv 30 -Pn tcp -Ps 38   -Pa 0 -Pf 0 -Po 0 
re_wireless_event = re.compile("-t (\d+.\d+) -Hs (\d+) -Hd (\d+) -Ni (\d+) -Nx (\d+.\d+) -Ny (\d+.\d+) -Nz (\d+.\d+) -Ne ([-]\d+.\d+) -Nl (\w+) -Nw ([---]{3}|\w+) -Ma ([0-9A-Fa-f]+) -Md ([0-9A-Fa-f]+) -Ms ([0-9A-Fa-f]+) -Mt ([0-9A-Fa-f]+)")
re_node_identifier = re.compile("-Ni (\d+)")
re_send_event = re.compile("^s")
re_receive_event = re.compile("^r")
re_drop_event = re.compile("^d")
re_forward_event = re.compile("^f")

# We only care about matching application layer presently?
re_predict_event = re.compile("-t (\d+.\d+) (.*) -Nl AGT (.*) -It tcp (.*)")

""" 
Return node register IDs provided lines from a trace file. 
"""
def get_nodes(lines):

    nodes = []
    for line in lines:
        found = re_node_register.search(line)

        if found:
            node_id = found.group(2)
            if not node_id in nodes:
                nodes.append(int(node_id))

    return nodes

"""
Provided lines, src and dst, build prediction event data for the predictor.
"""
def get_prediction_events(lines, src, dst):
    predict_data = {'0': '999'}

    for line in lines:
        # get predict events
        found = re_predict_event.search(line)
        if found:
            node_source = re_node_identifier.search(line)
            packet_event_found = re_packet_event.search(line)

            if node_source and packet_event_found:

                if node_source.group(1) == str(src):
                    predict_data[found.group(1)] = packet_event_found.group(2)

    return predict_data


""" 
Return packet statistics for a given node.
"""
def get_packet_statistics(lines, node):

    dropped_packets = [0,]
    dp_features = []
    received_packets = [0,]
    sent_packets = [0,]
    forwarded_packets = [0,]

    for line in lines:
        # get dropped packets.
        found = re_drop_event.search(line)
        if found:
            pe_found = re_packet_event.search(line)
            node_found = re_node_identifier.search(line)
            if node_found.group(1) == str(node) and pe_found:
                # extract wireless features for matching node.
                wireless_found = re_wireless_event.search(line)
                if wireless_found:
                    dp_features.append({'time': wireless_found.group(1), 'reason': wireless_found.group(10)})
                dropped_packets.append(int(pe_found.group(2)))

        # get received packets.
        found = re_receive_event.search(line)
        if found:
            pe_found = re_packet_event.search(line)
            node_found = re_node_identifier.search(line)
            if node_found.group(1) == str(node) and pe_found:
                received_packets.append(int(pe_found.group(2)))

    return (dropped_packets, received_packets, sent_packets, forwarded_packets, dp_features)


if __name__ == "__main__":

	print "Just a library."