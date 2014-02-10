#!/usr/bin/env python

""" 

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
re_node_identifier = re.compile("-Ni (\d+)")
re_send_event = re.compile("^s")
re_receive_event = re.compile("^r")
re_drop_event = re.compile("^d")
re_forward_event = re.compile("^f")


def get_nodes(lines):
    """ 
    Return node register IDs provided lines from a trace file. 
    """

    nodes = []
    for line in lines:
        found = re_node_register.search(line)

        if found:
            node_id = found.group(2)
            if not node_id in nodes:
                nodes.append(int(node_id))

    return nodes


def get_packet_statistics(lines, node):
    """ 
    Return packet statistics for a given node.
    """

    dropped_packets = [0,]
    received_packets = [0,]
    sent_packets = [0,]

    for line in lines:
        # get dropped packets.
        found = re_drop_event.search(line)
        if found:
            pe_found = re_packet_event.search(line)
            node_found = re_node_identifier.search(line)
            if node_found.group(1) == str(node):
                # print "Node ({0}) Dropped ({1}): {2} bytes.".format(node_found.group(1), pe_found.group(1), pe_found.group(2))
                dropped_packets.append(int(pe_found.group(2)))

        # get received packets.
        found = re_receive_event.search(line)
        if found:
            pe_found = re_packet_event.search(line)
            node_found = re_node_identifier.search(line)
            if node_found.group(1) == str(node):
                # print "Node ({0}) Received ({1}): {2} bytes.".format(node_found.group(1), pe_found.group(1), pe_found.group(2))
                received_packets.append(int(pe_found.group(2)))

    return (dropped_packets, received_packets, sent_packets)


if __name__ == "__main__":

	print "Just a library."