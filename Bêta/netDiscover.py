import os
import platform
import re
from datetime import datetime

def net_map(net, iface='wlan0'):
   net1 = net.split('.')
   a = '.'

   net2 = net1[0] + a + net1[1] + a + net1[2] + a
   st1 = 100
   en1 = 127
   en1 = en1 + 1
   oper = platform.system()

   hosts = []
   if oper == "Windows":
      ping1 = "ping -n 1 "
      arp_command = "arp -a"
      mac_pattern = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
      
      t1 = datetime.now()
      print("Scanning in Progress:")
      
      for ip in range(st1, en1):
         addr = net2 + str(ip)
         comm = ping1 + addr
         response = os.popen(comm)
         ans = ' '.join(response.readlines())
         
         if ("perte 0%" in ans):
               arp_response = os.popen(arp_command).read()
               mac_match = re.search(mac_pattern, arp_response)
               if mac_match:
                  mac_address = mac_match.group()
                  print(f"MAC Address: {mac_address}")
                  hosts.append({"IP": addr, "MAC": mac_address})
               else:
                  hosts.append({"IP": addr, "MAC": "Unknown"})
   
      t2 = datetime.now()
      total = t2 - t1
      print("Scanning completed in:", total)
        
   elif oper == "Linux":
      ping1 = "ping -c 1 "
      arp_command = "arping -c 1 -I {} {}"
      mac_pattern = r"([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})"
      
      t1 = datetime.now()
      print("Scanning in Progress:")
      
      for ip in range(st1, en1):
         addr = net2 + str(ip)
         comm = ping1 + addr
         response = os.popen(comm)
         ans = ' '.join(response.readlines())
         
         if "Destination Host Unreachable" not in ans:
               arp_response = os.popen(arp_command.format(iface, addr)).read()
               mac_match = re.search(mac_pattern, arp_response)
               if mac_match:
                  mac_address = mac_match.group()
                  hosts.append({"IP": addr, "MAC": mac_address})

               else:
                  hosts.append({"IP": addr, "MAC": "Unknown"})
   
      t2 = datetime.now()
      total = t2 - t1
      print("Scanning completed in:", total)
        
   else:
      print("Unsupported operating system.")
    
   return hosts
