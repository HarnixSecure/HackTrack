from scapy.all import *

def sniff_packets(interface, auth_hosts_file):
    with open(auth_hosts_file, 'r') as file:
        auth_hosts = [line.strip() for line in file]
    known_hosts = set(auth_hosts)

    least_recent_packets = []
    suspected_packets = [] 
    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            matched = 0
            if src_ip not in known_hosts:
                for recent_packet in least_recent_packets:
                    if match_request(packet, recent_packet):
                        matched+=1
                        break
                    
                if (matched==1):
                    print(f"Matching response found for {src_ip}!")

                elif (matched>3):
                    print(f"Potentially dangerous activity coming from {src_ip}!")
                    suspected_packets.append(packet)

                else:
                    print(f"Unauthenticated request coming from {src_ip}!")
                    suspected_packets.append(packet)



        least_recent_packets.append(packet)

        if len(least_recent_packets) > 20:
            least_recent_packets.pop(0)

    sniff(iface=interface, prn=packet_callback, store=0)
    

def match_request(packet, recent_packet):
    return (
        IP in packet and IP in recent_packet and
        packet[IP].src == recent_packet[IP].dst and
        packet[IP].dst == recent_packet[IP].src
    )

# Example usage
interface = 'wlan0'
auth_hosts_file = 'the_good_ones.txt'
sniff_packets(interface, auth_hosts_file)
