from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def run(self, ip, traceId):
        trace = []
        print("start trace", file=sys.stderr)
        
        for i in range(1, 28):
            print("dst="+str(ip)+", ttl="+str(i), file=sys.stderr)
            pkt = IP(dst=ip, ttl=i) / UDP(dport=33434)
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
                trace.append([i,reply.src])
                print("--> " + str(i) + " " + reply.src, file=sys.stderr) 
                break
            else:
            # We're in the middle somewhere
                trace.append([i,reply.src])
                print("--> " + str(i) + " " + reply.src, file=sys.stderr) 


        print("stop trace", file=sys.stderr)
        self.datadb.insertTrace(traceId, trace)

