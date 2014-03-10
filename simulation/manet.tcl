# CPSC 5900
# MANET Simulator

# Lifted and expanded from:
# https://code.google.com/p/ns-allinone-2-34-imp-protocol/source/browse/trunk/src/ns-2.34/aodv/example.tcl?r=11

# ONGOING. Todo: Review documentation further: http://www.isi.edu/nsnam/ns/doc/ns_doc.pdf

# DONE. Todo: Allow command line processing of some setup parameters, including number of nodes.
# Todo: include seed and separate random numbers for topology and other variables.

proc setup {} {
	# Define default values for simulation:
	set val(chan)           Channel/WirelessChannel    ;# channel type
	set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
	set val(netif)          Phy/WirelessPhy            ;# network interface type
	set val(mac)            Mac/802_11                 ;# MAC type
	set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
	set val(ll)             LL                         ;# link layer type
	set val(ant)            Antenna/OmniAntenna        ;# antenna model
	set val(ifqlen)         15                         ;# max packet in ifq (default was 50)
	set val(nn)             20                         ;# number of mobilenodes
	set val(rp)             AODV                       ;# routing protocol
	set val(x)              500                        ;# X dimension of topography
	set val(y)              400                        ;# Y dimension of topography
	set val(stop)           100                        ;# time of simulation end
	set val(rqnp)			.5                         ;# percent of mobilenodes performing requests.

	global argc argv
	global defaultRNG
	$defaultRNG seed 99999
	set noinput 0
	# result folder for experiments
	set results ./results
	set val(tracefd_file)	"$results/manet.tr"
	set val(namtrace_file)	"$results/manet.nam"

	if {$argc > 0} {
		for {set i 0} {$i < $argc } { incr i } {
			if {[lindex $argv $i] == "--noinput"} {
				set noinput 1
			}

			if {[lindex $argv $i] == "--defaultrng"} {
				if {$argc > [expr $i + 1]} { 
					$defaultRNG seed [lindex $argv [expr $i + 1]]
					puts "defaultRNG is $defaultRNG"
				}
			}

		}
	}

	if {$noinput == 0} {
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
			puts "Enter max packet in ifq:"
			set val(ifqlen) [gets stdin]
			puts "Max packet in ifq is $val(ifqlen)."
			puts "Enter percent of mobilenodes performing requests (.01 to 1):"
			set val(rqnp) [gets stdin]
			puts "Percent mobilenodes performing requests is $val(rqnp)."
			puts "Enter duration of simulation (seconds): "
			set val(stop) [gets stdin]
			puts "Simulation will run for $val(stop) seconds."

			# finish our setup.
			set setup 0
		}
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
puts "defaultRNG is $defaultRNG"

set topology_ [new RandomVariable/Uniform]
$topology_ set min_ $val(x)
$topology_ set max_ $val(y)

puts [format "Got random topology value = %d" [expr round([$topology_ value])]]

set ns            [new Simulator]
set tracefd       [open $val(tracefd_file) w]
set namtrace      [open $val(namtrace_file) w]

# use the new trace format.
$ns use-newtrace
$ns trace-all $tracefd
$ns namtrace-all-wireless $namtrace $val(x) $val(y)

# set up topography object
set topo       [new Topography]

$topo load_flatgrid $val(x) $val(y)

create-god $val(nn)

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
-macTrace ON \
-movementTrace ON

# DONE: Todo: setup N nodes and their properties/connections?

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

# Todo: Allow simulation of *specific* movement across topology for N mobile nodes.
# for {set i 0} {$i < $val(nn) } { incr i } {
	# puts [format "$node_($i) at 10.0 setdest %d %d 10.0" [expr round([$topology_ value])] [expr round([$topology_ value])] ]
	# $ns at 10.0 [format "$node_($i) setdest 400.0 400.0 10.0" [expr $i]]
# }


# DONE: Todo: Allow ftp between j nodes instead of between 0 and N specifically.
# node 0 as tcp and node 1 as sink

for {set i 0} {$i < [expr int($val(nn) * $val(rqnp))] } { incr i} {
	# use nn - i and i e.g. nn = 100 and rqnp = 1, 1:100, 2:99, 3:98, ... 49:51

	set tcp_($i) [new Agent/TCP/Newreno]
	$ns attach-agent $node_($i) $tcp_($i)

	set sink_($i) [new Agent/TCPSink]
	$ns attach-agent $node_([expr $val(nn) - 1 - $i ]) $sink_($i)

	$ns connect $tcp_($i) $sink_($i)

	set ftp_($i) [new Application/FTP]
	$ftp_($i) attach-agent $tcp_($i)
	$ns at 10.0 "$ftp_($i) start"

}

if { [file exists "predict.tcl" ] } {
	# include result of predict in the form of:
	# $ns at <time> "<whatever>"
	source "predict.tcl"
}

# ending nam and the simulation
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"
$ns at 100.0 "puts \"end simulation\" ; $ns halt"

proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    close $tracefd
    close $namtrace
    # Execute nam on the trace file
    # exec nam manet.nam &
    exit 0
}

#Call the finish procedure after 5 seconds of simulation time
$ns run
