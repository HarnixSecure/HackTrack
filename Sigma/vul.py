import nmap
#cible
target_ip = '192.168.0.1'
#scan	
nm = nmap.PortScanner()
#scan de tous les ports
nm.scan(target_ip, arguments='-p1-65535 --script vuln')

#affichage des résultats
for host in nm.all_hosts():
    #affichage des résultats pour chaque hôte
    print(f"Vulnérabilités pour {host}:")
    #affichage des résultats pour chaque port	
    for port in nm[host]['tcp'].keys():
        #affichage des résultats pour chaque script
        if 'script' in nm[host]['tcp'][port]:
            scripts = nm[host]['tcp'][port]['script']
            for script in scripts:
                print(f"Port {port}: {script}")
