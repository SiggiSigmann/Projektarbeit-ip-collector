from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys
import socket

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        print("Tracert: " + ip, file=sys.stderr)
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def run(self, ip, traceId):
        trace = []
        print("thread: " + ip, file=sys.stderr)

        for i in range(1, 28):
            print("thread: " + ip + " " + str(i), file=sys.stderr)
            try:
                pkt = IP(dst=ip, ttl=i) / UDP(dport=33434)
                # Send the packet and get a reply
                reply = sr1(pkt, verbose=0)
                if reply is None:
                    # No reply =(
                    print("thread: No reply " + ip , file=sys.stderr)
                    trace.append([i,"-", "-"])
                    
                elif reply.type == 3:
                    # We've reached our destination
                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    print("thread: done " + ip , file=sys.stderr)
                    trace.append([i, reply.src, hostname])
                    
                    break
                else:
                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    trace.append([i, reply.src, hostname])
                    print("thread: weiter " + ip , file=sys.stderr)
            except:
                print("error " + ip , file=sys.stderr)

                
        print("done with trace: " + ip, file=sys.stderr)
        self.datadb.insertTrace(traceId, trace)
        print("stop: " + ip, file=sys.stderr)

