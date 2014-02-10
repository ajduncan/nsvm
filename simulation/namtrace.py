#!/usr/bin/env python

""" 

NAM:

http://nsnam.isi.edu/nsnam/index.php/NS-2_Trace_Formats#NAM_Trace_Formats
http://www.isi.edu/nsnam/ns/doc/node617.html

Regular expression parser:
http://docs.python.org/2/library/re.html

but using re.compile() and saving the resulting regular expression object for reuse is more efficient when the expression will be used several times in a single program.

"""


import re


re_node_register = re.compile("^n -t (\d+.\d+) -s (\d+) -x (\d+.\d+) -y (\d+.\d+) -U ([-]\d+.\d+) -V ([-]\d+.\d+) -T (\d+.\d+)")
re_send_event = re.compile("^s")
re_receive_event = re.compile("^r")
re_drop_event = re.compile("^d")
re_forward_event = re.compile("^f")


""" Return node register IDs provided lines from a trace file. """
def get_nodes(lines):
    nodes = []
    for line in lines:
        found = re_node_register.search(line)

        if found:
            node_id = found.group(2)
            if not node_id in nodes:
                nodes.append(node_id)

    return nodes

def get_received_packets(lines, node):
	packets = 0
	for line in lines:
		found = re_receive_event.search(line)

		if found:
			print "Got receive match: {}".format(found.group(0))

	return packets

if __name__ == "__main__":

	print "Just a library."