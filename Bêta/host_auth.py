from netDiscover import net_map
from scapy.all import *

def auth_hosts(network, output_file='the_good_ones.txt'):
    auth_hosts = []
    host_list = net_map(network)

    for host in host_list:
        if 'MAC' in host and host['MAC'] != 'Unknown':
            auth_hosts.append(host)

    with open(output_file, 'w') as file:
        for host in auth_hosts:
            ip_address = host['IP']
            mac_address = host['MAC']
            hostname = get_hostname_from_ip(ip_address)
            file.write(f"IP: {ip_address}, MAC: {mac_address}, Hostname: {hostname}\n")

    return auth_hosts


def get_hostname_from_ip(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return "Unknown"

auth_hosts('192.168.8.0')