#!/usr/bin/env python

""" 

Trace file analysis of ns-2, as defined in:

http://www.isi.edu/nsnam/ns/doc/node289.html

"""

# Lifted from http://ilab.cs.byu.edu/cs660/tools/parse.py
# Parse an ns-2 trace file for some basic statistics

import optparse
from ggplot import *

class Parser:
    def __init__(self):
        parser = optparse.OptionParser(usage = "%prog [options] file", version = "%prog 0.1")

        (self.options, self.args) = parser.parse_args()
        if len(self.args) != 1:
            parser.error("incorrect number of arguments")

    def parse(self):
        tcp = 0
        udp = 0
        tcp_bytes = 0
        udp_bytes = 0
        tcp_loss = 0
        udp_loss = 0
        f = open(self.args[0])

        for line in f.readlines():
            field = line.split()

            if field[0] == '+' and field[2] == '2' and field[3] == '3':
                if field[4] == 'tcp':
                    tcp += int(field[5])
                if field[4] == 'cbr':
                    udp += int(field[5])

            if field[0] == '-' and field[2] == '2' and field[3] == '3':
                if field[4] == 'tcp':
                    tcp_bytes += int(field[5])
                if field[4] == 'cbr':
                    udp_bytes += int(field[5])

            if field[0] == 'd' and field[2] == '2' and field[3] == '3':
                if field[4] == 'tcp':
                    tcp_loss += int(field[5])
                if field[4] == 'cbr':
                    udp_loss += int(field[5])
                    
        # temporarily handle division by zero errors   
        if tcp == 0:
        	tcp = 0.1
        if udp == 0:
        	udp = 0.1
        total = tcp + udp
        print "TCP", tcp_bytes, "UDP", udp_bytes, "Total", total, "TCP/Total", float(tcp_bytes)/total, "UDP/Total", float(udp_bytes)/total
        print "TCP loss",float(tcp_loss)/tcp,"UDP loss",float(udp_loss)/udp
                

if __name__ == "__main__":

    # p = Parser()
    # p.parse()

    p = ggplot(aes(x='date', y='beef'), data=meat) + \
        geom_point(color='lightblue') + \
        stat_smooth(span=.15, color='black', se=True) + \
        ggtitle("Beef: It's What's for Dinner") + \
        xlab("Date") + \
        ylab("Head of Cattle Slaughtered")
    ggsave(p, "beef.png")
    print p

