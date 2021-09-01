import argparse
import time
import random
from scapy.contrib.gtp import (
        GTP_U_Header,
        GTPPDUSessionContainer)
from scapy.all import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--sport', default=2152,
                        type=int, help="UDP Source port. If the random option (-r/--random) is active, the source UDP port will be randomized")
    parser.add_argument('-a', '--address', type=str, help="Destination IPv4 address")
    parser.add_argument('-t', '--teid', default=1,
                        type=int, help="GTP-U Tunnel Endpoint Identifier(TEID)")
    parser.add_argument('-q', '--qfi', default=1,
                        type=int, help="QoS Flow ID(QFI)")
    parser.add_argument('-r', '--random', action='store_true',
                        help="Randomize the source udp port")
    parser.add_argument('-u', '--duration', default=10,
                        type=int, help="Packet sending duration [sec]")
    parser.add_argument('-i', '--interval', default=100,
                        type=int, help="Packet sending interval [msec]")
    args = parser.parse_args()

    payload = "test "*20

    outerIp = IP(dst=args.address)
    outerUdp = UDP(sport=args.sport, dport=2152)
    gtpHeader = GTP_U_Header(teid=args.teid, next_ex=133)/GTPPDUSessionContainer(type=1, QFI=args.qfi)
    innerIp = IP(src="10.0.0.1", dst="10.0.0.2")/TCP(sport=10001,dport=443)/payload


    mint = args.interval/1000.0
    count = int(args.duration / mint)

    for i in range(count):
        time.sleep(mint)
        if (args.random):
            srcUdpPort = random.randrange(49152,65535,1)
            outerUdp = UDP(sport=srcUdpPort, dport=2152)
        sendingPacket = outerIp/outerUdp/gtpHeader/innerIp
        send(sendingPacket, verbose=True)