#!/usr/bin/env python3

#needed modules importation
import time
import sys
import os

#follow(file) acts like (>_tail -f file) under Linux
def follow(thefile):
    thefile.seek(0, os.SEEK_END)
    
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue

        yield line

if __name__ == '__main__':
    #introducing application capabilities to user
    print("""You'll be aware of : 
    		1 - Any remote SSH connection
    		2 - Every time sudo command is used
    		3 - Any user trying to connect or deconnect\n\n*******************Starting listener*******************""")
    
    #By the way, we've found the file /var/log/auth.log interesting for our log analysis. So all actions have been based on it
    logfile = open("/var/log/auth.log","r")
    loglines = follow(logfile)
    
    #here comes our controller. It receives each new line added to file and take a decision according to them
    for line in loglines:
        table = line.split()
        date = table[0].split('T')
        daydate = date[0].split('-')
        archiving = f"{daydate[-1]}/{daydate[-2]}/{daydate[0]} à {date[1].split('.')[0]}"
        if "password" in line :
            content = f"[alpha@logging]__Connection {table[-1]} from {table[-4]} via client port {table[-2]} as {table[-6]} "
            if table[3] == 'Failed' :
                content += "while typing a wrong password"
            else :
                content += "while typing a correct password"
            print(f"{content} at {archiving}")
        elif 'authentication failure' in line :
            content = f"[alpha@logging]__{table[-3].split('=')[1]} tried to connected as {table[-1].split('=')[1]} while typing a wrong password"
            print(f"{content} at {archiving}")
        elif "session opened" in line :
            ruser = table[-1].split('(')[0]
            meth = table[3].split('(')[-1].split(':')[0]
            if ruser :
                content = f"[alpha@logging]__{ruser} has been connected as {table[-3].split('(')[0]} via {meth}"
                print(f"{content} at {archiving}")
        elif "session closed" in line :
            print(f"[alpha@logging]__{table[-1]} deconnection at {archiving}")
