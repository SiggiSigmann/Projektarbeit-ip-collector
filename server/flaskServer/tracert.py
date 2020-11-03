from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys
import socket

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def run(self, ip, traceId):
        print("start trace", file=sys.stderr)
        trace = []
        for i in range(1, 28):
            print("dst="+str("www.google.de")+", ttl="+str(i), file=sys.stderr)
            pkt = IP(dst=str("www.google.de"), ttl=i) / UDP(dport=33434)
            print(pkt, file=sys.stderr)
            # Send the packet and get a reply
            reply = sr1(pkt, verbose=0)
            print(reply, file=sys.stderr)
            if reply is None:
                # No reply =(
                
                trace.append([i,"-"])
                print("--> " + str(i) + " -" , file=sys.stderr) 
            elif reply.type == 3:
                # We've reached our destination
                try:

                    trace.append([i,reply.src, socket.gethostbyaddr(reply.src)])
                    print("--> " + str(i) + " " + reply.src, file=sys.stderr) 

                except:
                    trace.append([i,reply.src, "-"])
                    print("--> " + str(i) + " " + reply.src, file=sys.stderr) 
                break
            else:
                try:

                    trace.append([i,reply.src, socket.gethostbyaddr(reply.src)])
                    print("--> " + str(i) + " " + reply.src, file=sys.stderr) 

                except:
                    trace.append([i,reply.src, "-"])
                    print("--> " + str(i) + " " + reply.src, file=sys.stderr) 
                break

        print(trace, file=sys.stderr)
        print("stop trace", file=sys.stderr)
        self.datadb.insertTrace(traceId, trace)

