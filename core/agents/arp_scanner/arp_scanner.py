from scapy.all import ARP, Ether, srp

class ARPScanner:
    def scan_network(self, ip_range):
        arp_request = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        result = srp(packet, timeout=2, verbose=0)[0]
        return [{'ip': received.psrc, 'mac': received.hwsrc} for sent, received in result]
