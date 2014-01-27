# CPSC 5900
# MANET Simulator

# Lifted and expanded from:
# https://code.google.com/p/ns-allinone-2-34-imp-protocol/source/browse/trunk/src/ns-2.34/aodv/example.tcl?r=11

# Todo: Review documentation further: http://www.isi.edu/nsnam/ns/doc/ns_doc.pdf

# Todo: Allow command line processing of some setup parameters, including number of nodes.

proc setup {} {
	# Define default values for simulation:
	set val(chan)           Channel/WirelessChannel    ;# channel type
	set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
	set val(netif)          Phy/WirelessPhy            ;# network interface type
	set val(mac)            Mac/802_11                 ;# MAC type
	set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
	set val(ll)             LL                         ;# link layer type
	set val(ant)            Antenna/OmniAntenna        ;# antenna model
	set val(ifqlen)         50                         ;# max packet in ifq
	set val(nn)             20                         ;# number of mobilenodes
	set val(rp)             AODV                       ;# routing protocol
	set val(x)              500                        ;# X dimension of topography
	set val(y)              400                        ;# Y dimension of topography
	set val(stop)           100                        ;# time of simulation end

	puts "Run interactive setup?"
	puts "1. Yes"
	puts "2. No"
	set setup [gets stdin]
	if {$setup == 1 } {
		puts "How many nodes should be used in the simulation?"
		set val(nn) [gets stdin]
		puts "Setting up simulation for $val(nn) mobile nodes."
		puts "Enter X dimension value of topography: "
		set val(x) [gets stdin]
		puts "Enter Y dimension value of topography: "
		set val(y) [gets stdin]
		puts "Topography is $val(x) by $val(y) meters."
		puts "Enter duration of simulation (seconds): "
		set val(stop) [gets stdin]
		puts "Simulation will run for $val(stop) seconds."

		# finish our setup.
		set setup 0
	}
	return [array get val]
}

array set val [setup]

puts "Setup values are: "
foreach key [array names val] {
    puts "${key}:\t$val($key)"
}

# Todo accept seed in setup.
global defaultRNG
$defaultRNG seed 99999

set topology_ [new RandomVariable/Uniform]
$topology_ set min_ $val(x)
$topology_ set max_ $val(y)

puts [format "Got random topology value = %d" [expr round([$topology_ value])]]

set ns            [new Simulator]
set tracefd       [open manet.tr w]
set windowVsTime2 [open win.tr w]
set namtrace      [open manet.nam w]

$ns trace-all $tracefd
$ns namtrace-all-wireless $namtrace $val(x) $val(y)

# set up topography object
set topo       [new Topography]

$topo load_flatgrid $val(x) $val(y)

create-god $val(nn)

#
#  Create nn mobilenodes [$val(nn)] and attach them to the channel.
#

# configure the nodes
$ns node-config -adhocRouting $val(rp) \
-llType $val(ll) \
-macType $val(mac) \
-ifqType $val(ifq) \
-ifqLen $val(ifqlen) \
-antType $val(ant) \
-propType $val(prop) \
-phyType $val(netif) \
-channelType $val(chan) \
-topoInstance $topo \
-agentTrace ON \
-routerTrace ON \
-macTrace OFF \
-movementTrace ON

for {set i 0} {$i < $val(nn) } { incr i } {
    set node_($i) [$ns node]
    # Create random movement for nodes
    $node_($i) random-motion 1

	# Provide initial location across topology for N mobile nodes.
	$node_($i) set X_ $topology_ value
	$node_($i) set Y_ $topology_ value
	$node_($i) set Z_ 0.0

	# Begin random movement from start distance at time zero.
	$ns at 1.0 "$node_($i) start"

}

# Todo: Simulate specific movement across topology for N mobile nodes.
# for {set i 0} {$i < $val(nn) } { incr i } {
	# puts [format "$node_($i) at 10.0 setdest %d %d 10.0" [expr round([$topology_ value])] [expr round([$topology_ value])] ]
	# $ns at 10.0 [format "$node_($i) setdest 400.0 400.0 10.0" [expr $i]]
# }


# configure node 0 and node 1
# node 0 as tcp and node 1 as sink
set tcp01 [new Agent/TCP/Newreno]
$ns attach-agent $node_(0) $tcp01

set sink01 [new Agent/TCPSink]
$ns attach-agent $node_([expr $val(nn) - 1 ]) $sink01

$ns connect $tcp01 $sink01

set ftp01 [new Application/FTP]
$ftp01 attach-agent $tcp01
$ns at 10.0 "$ftp01 start"

# Printing the window size

# ending nam and the simulation
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"
$ns at 100.0 "puts \"end simulation\" ; $ns halt"

proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    close $tracefd
    close $namtrace
    #Execute nam on the trace file
    exec nam manet.nam &
    exit 0
}

#Call the finish procedure after 5 seconds of simulation time
$ns run
