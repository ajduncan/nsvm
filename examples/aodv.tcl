# https://code.google.com/p/ns-allinone-2-34-imp-protocol/source/browse/trunk/src/ns-2.34/aodv/example.tcl?r=11
# wrls1.tcl
# A 3-node example for ad-hoc simulation with AODV

# Define options
set val(chan)           Channel/WirelessChannel    ;# channel type
set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
set val(netif)          Phy/WirelessPhy            ;# network interface type
set val(mac)            Mac/802_11                 ;# MAC type
set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
set val(ll)             LL                         ;# link layer type
set val(ant)            Antenna/OmniAntenna        ;# antenna model
set val(ifqlen)         50                         ;# max packet in ifq
set val(nn)             2                          ;# number of mobilenodes
set val(rp)             AODV                       ;# routing protocol
set val(x)              500                        ;# X dimension of topography
set val(y)              400                        ;# Y dimension of topography
set val(stop)           100                        ;# time of simulation end

set ns            [new Simulator]
set tracefd       [open simple.tr w]
set windowVsTime2 [open win.tr w]
set namtrace      [open simwrls.nam w]

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
}

# Provide initial location of mobilenodes
$node_(0) set X_ 5.0
$node_(0) set Y_ 5.0
$node_(0) set Z_ 0.0

$node_(1) set X_ 280
$node_(1) set Y_ 180.0
$node_(1) set Z_ 0.0

#$node_(2) set X_ 150.0
#$node_(2) set Y_ 240.0
#$node_(2) set Z_ 0.0

#$node_(3) set X_ 250.0
#$node_(3) set Y_ 240.0
#$node_(3) set Z_ 0.0

#$node_(4) set X_ 100.0
#$node_(4) set Y_ 70.0
#$node_(4) set Z_ 0.0

# Generation of movements
$ns at 10.0 "$node_(0) setdest 250.0 250.0 10.0"
$ns at 15.0 "$node_(1) setdest 200.0 300.0 10.0"
#$ns at 110.0 "$node_(0) setdest 480.0 300.0 10.0"
#$ns at 70.0 "$node_(3) setdest 300.0 320.0 10.0"
#$ns at 80.0 "$node_(4) setdest 180.0 280.0 10.0"
#$ns at 20.0 "$node_(2) setdest 10.0 280.0 10.0"

#---------------------- configure node 0 and node 1
#---------------------- node 0 as tcp and node 1 as sink
set tcp01 [new Agent/TCP/Newreno]
$ns attach-agent $node_(0) $tcp01

set sink01 [new Agent/TCPSink]
$ns attach-agent $node_(1) $sink01

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
    exec nam simwrls.nam &
    exit 0
}

#Call the finish procedure after 5 seconds of simulation time
$ns run 
