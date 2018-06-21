#!/bin/bash

#interface=enp0s8
#ip=192.168.11.254
#delay=2000ms

# Delete all existing qdiscs
tc qdisc del dev enp0s8 root
# tc qdisc add dev enp0s8 root handle 1: htb
# tc class add dev enp0s8 parent 1: classid 1:1 htb rate 1000mbit
# tc filter add dev enp0s8 parent 1: protocol ip prio 1 u32 flowid 1:1 match ip dst 192.168.12.0/24
# tc qdisc add dev enp0s8 parent 1:1 handle 10: netem delay 2500ms 500ms


# This line sets a HTB qdisc on the root of enp0s8, and it specifies that the class 1:30 is used by default. It sets the name of the root as 1:, for future references.
tc qdisc add dev enp0s8 root handle 1: htb default 30

# This creates a class called 1:1, which is direct descendant of root (the parent is 1:), this class gets assigned also an HTB qdisc, and then it sets a max rate of 6mbits, with a burst of 15k
tc class add dev enp0s8 parent 1: classid 1:1 htb rate 6mbit burst 15k

# The previous class has this branches:

# Class 1:10, which has a rate of 5mbit
tc class add dev enp0s8 parent 1:1 classid 1:10 htb rate 5mbit burst 15k

# Class 1:20, which has a rate of 3mbit
tc class add dev enp0s8 parent 1:1 classid 1:20 htb rate 3mbit ceil 6mbit burst 15k

# Class 1:30, which has a rate of 1kbit. This one is the default class.
tc class add dev enp0s8 parent 1:1 classid 1:30 htb rate 1kbit ceil 6mbit burst 15k

# tc qdisc add dev eth0 parent 1:10 handle 10: sfq perturb 10
tc qdisc add dev enp0s8 parent 1:10 handle 10: netem delay 2500ms 500ms

# tc qdisc add dev enp0s8 parent 1:20 handle 20: sfq perturb 10
tc qdisc add dev enp0s8 parent 1:20 handle 20: netem delay 4500ms 500ms

# This command adds a filter to the qdisc 1: of dev eth0, set the
# priority of the filter to 1, matches packets with a
# destination ip 192.168.12.0/24, and make the class 1:10 process the
# packets that match.
# tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip dst 192.168.11.0/24 flowid 1:10

# This command adds a filter to the qdisc 1: of dev eth0, set the
# priority of the filter to 1, matches packets with a
# destination ip 192.168.12.0/24, and make the class 1:10 process the
# packets that match.
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip dst 192.168.3.21/32 flowid 1:20
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip dst 192.168.3.22/32 flowid 1:20
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip dst 192.168.3.23/32 flowid 1:20
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip src 192.168.3.21/32 flowid 1:20
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip src 192.168.3.22/32 flowid 1:20
tc filter add dev enp0s8 protocol ip parent 1: prio 1 u32 match ip src 192.168.3.23/32 flowid 1:20




# # Martin Devera, author of HTB, then recommends SFQ for beneath these classes:
# tc qdisc add dev enp0s8 parent 1:10 handle 10: sfq perturb 10
# tc qdisc add dev enp0s8 parent 1:20 handle 20: sfq perturb 10
# tc qdisc add dev enp0s8 parent 1:30 handle 30: sfq perturb 10