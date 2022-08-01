from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from mininet.log import setLogLevel, info 
import time
import os


if'__main__'==__name__:
	os.system('mn -c')
	os.system( 'clear' )
	setLogLevel( 'info' )
	net = Mininet(link=TCLink)
	
	#add host and router
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	#add links
	net.addLink(h1,r1,cls=TCLink, intfName1='h1-eth0', intfName2='r1-eth0',bw=1)
	net.addLink(h1,r2,cls=TCLink, intfName1='h1-eth1', intfName2='r2-eth0',bw=1)
	net.addLink(h2,r3,cls=TCLink, intfName1='h2-eth0', intfName2='r3-eth0',bw=1)
	net.addLink(h2,r4,cls=TCLink, intfName1='h2-eth1', intfName2='r4-eth0',bw=1)
	net.addLink(r1,r3,cls=TCLink, intfName1='r1-eth1', intfName2='r3-eth1',bw=0.5)
	net.addLink(r1,r4,cls=TCLink, intfName1='r1-eth2', intfName2='r4-eth1',bw=1)
	net.addLink(r2,r3,cls=TCLink, intfName1='r2-eth1', intfName2='r3-eth2',bw=1)
	net.addLink(r2,r4,cls=TCLink, intfName1='r2-eth2', intfName2='r4-eth2',bw=0.5)

	net.build()

	#config ip host
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h1.cmd("ifconfig h1-eth0 197.167.0.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 197.167.1.1 netmask 255.255.255.0")
	
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eth1 0")
	h2.cmd("ifconfig h2-eth0 197.167.2.1 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 197.167.3.1 netmask 255.255.255.0")
	
	#config ip router
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 197.167.0.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 197.167.4.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 197.167.6.1 netmask 255.255.255.0")
		
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 197.167.1.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 197.167.7.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 197.167.5.1 netmask 255.255.255.0")
		
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 197.167.2.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 197.167.4.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 197.167.7.2 netmask 255.255.255.0")
		
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 197.167.3.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 197.167.6.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 197.167.5.2 netmask 255.255.255.0")
		
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")


	#static routing host
	h1.cmd("ip rule add from 197.167.0.1 table 1")
	h1.cmd("ip rule add from 197.167.1.1 table 2")
	h1.cmd("ip route add 197.167.0.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 197.167.0.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 197.167.1.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 197.167.1.2 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 197.167.0.2 dev h1-eth0")
	
	h2.cmd("ip rule add from 197.167.2.1 table 1")
	h2.cmd("ip rule add from 197.167.3.1 table 2")
	h2.cmd("ip route add 197.167.2.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 197.167.2.2 dev h2-eth0 table 1")
	h2.cmd("ip route add 197.167.3.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 197.167.3.2 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 197.167.2.2 dev h2-eth0")

	#static routing router
	r1.cmd("route add -net 197.167.2.0/24 gw 197.167.4.2")
	r1.cmd("route add -net 197.167.7.0/24 gw 197.167.4.2")
	r1.cmd("route add -net 197.167.3.0/24 gw 197.167.6.2")
	r1.cmd("route add -net 197.167.5.0/24 gw 197.167.6.2")
	r1.cmd("route add -net 197.167.1.0/24 gw 197.167.6.2")
	
	r2.cmd("route add -net 197.167.2.0/24 gw 197.167.7.2")
	r2.cmd("route add -net 197.167.3.0/24 gw 197.167.5.2")
	r2.cmd("route add -net 197.167.4.0/24 gw 197.167.7.2")
	r2.cmd("route add -net 197.167.6.0/24 gw 197.167.5.2")
	r2.cmd("route add -net 197.167.0.0/24 gw 197.167.7.2")
	
	r3.cmd("route add -net 197.167.0.0/24 gw 197.167.4.1")
	r3.cmd("route add -net 197.167.1.0/24 gw 197.167.7.1")
	r3.cmd("route add -net 197.167.5.0/24 gw 197.167.7.1")
	r3.cmd("route add -net 197.167.6.0/24 gw 197.167.4.1")
	r3.cmd("route add -net 197.167.3.0/24 gw 197.167.7.1")
	
	r4.cmd("route add -net 197.167.0.0/24 gw 197.167.6.1")
	r4.cmd("route add -net 197.167.1.0/24 gw 197.167.5.1")
	r4.cmd("route add -net 197.167.4.0/24 gw 197.167.6.1")
	r4.cmd("route add -net 197.167.7.0/24 gw 197.167.5.1")
	r4.cmd("route add -net 197.167.2.0/24 gw 197.167.6.1")
	
	#tcp and buffer
	#r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	#r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 20ms")
	
	#r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	#r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 40ms")
	
	#r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	#r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 60ms")
	
	#r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	#r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 100ms")
	
	# time.sleep(2)
	h2.cmd("iperf -s &")
	# time.sleep(2)
	h1.cmd("iperf -c 197.167.2.1 -t 10 &") 
	
	CLI(net)
	
	net.stop()
