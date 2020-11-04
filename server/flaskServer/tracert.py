from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys
import socket
import time

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        print("TracertID: " + traceId, file=sys.stderr)
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def printThreads(self):
        print("running threads: ", file=sys.stderr)
        for thread in threading.enumerate(): 
            print("\t  "+ thread.name, file=sys.stderr)

    def run(self, ip, traceId):
        starttime = time.time()
        trace = []

        for i in range(1, 28):
            print("traceId: " + traceId + " " + str(i), file=sys.stderr)
            try:
                pkt = IP(dst=ip, ttl=i) / UDP(dport=33434)
                # Send the packet and get a reply
                reply = sr1(pkt, verbose=0, timeout=30)
                if reply is None:
                    # No reply =(
                    print("traceId: No reply " + traceId , file=sys.stderr)
                    trace.append([i,"-", "-"])
                    
                elif reply.type == 3:
                    # We've reached our destination
                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    print("traceId: done " + traceId , file=sys.stderr)
                    trace.append([i, reply.src, hostname])
                    
                    break
                else:
                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    trace.append([i, reply.src, hostname])
                    print("traceId: next " + traceId , file=sys.stderr)
            except:
                print("traceId " + traceId , file=sys.stderr)

                
        self.datadb.insertTrace(traceId, trace)
        print("stop: " + traceId + " " + str(time.time() - starttime), file=sys.stderr)

