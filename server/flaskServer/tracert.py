from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys
import socket

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        print("Tracert: " + ip, file=sys.stdout)
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def run(self, ip, traceId):
        trace = []
        print("thread: " + ip, file=sys.stdout)

        for i in range(1, 28):
            print("thread: " + ip + " " + str(i), file=sys.stdout)
            pkt = IP(dst=ip, ttl=i) / UDP(dport=33434)
            # Send the packet and get a reply
            reply = sr1(pkt, verbose=0)
            if reply is None:
                # No reply =(

                trace.append([i,"-", "-"])
                print("thread: No reply " + ip , file=sys.stdout)
            elif reply.type == 3:
                # We've reached our destination
                hostname = ""
                try:
                    hostname = socket.gethostbyaddr(reply.src)[0]
                except:
                    hostname = "-"

                trace.append([i, reply.src, hostname])
                print("thread: done " + ip , file=sys.stdout)
                break
            else:
                hostname = ""
                try:
                    hostname = socket.gethostbyaddr(reply.src)[0]
                except:
                    hostname = "-"

                trace.append([i, reply.src, hostname])
                print("thread: witer " + ip , file=sys.stdout)

                
        print("done with trace: " + ip, file=sys.stdout)
        self.datadb.insertTrace(traceId, trace)
        print("stop: " + ip, file=sys.stdout)

