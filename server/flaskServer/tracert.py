#from scapy.all import *
from scapy.all import *
import threading
import dbconnector.dbconnector as dbcon
import sys
import socket
import time

#create trace to ip in seperat thread
class Tracert():
    def __init__(self, db):
        self.datadb = db

    #start new thread
    def execute(self, ip, traceId):
        x = threading.Thread(target=self._run, args=(ip, traceId), name=str(traceId))
        x.start()

    #returns runnign threads
    def getThreads(self):
        runningThreads = []
        for thread in threading.enumerate():
            if thread.name.startswith("MainThread") or thread.name.startswith("Thread"):
                continue
            runningThreads.append(thread.name)
        return runningThreads

    #will be executed by a new thread
    #creates trace to ip
    #stores trace in db
    def _run(self, ip, traceId):
        print("Thread["+traceId+"]: start", file=sys.stderr)
        starttime = time.time()
        trace = []

        #execute max 28 steps to find way to ip
        for i in range(1, 28):
            try:
                pkt = IP(dst=ip, ttl=i) / UDP(dport=33434)
                # Send the packet and get a reply
                reply = sr1(pkt, verbose=0, timeout=30)

                # No reply
                if reply is None:
                    print("traceId: No reply " + traceId , file=sys.stderr)
                    trace.append([i,"-", "-"])

                #destination reached
                elif reply.type == 3:
                    #try to get hostname
                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    #add tracestep to list
                    trace.append([i, reply.src, hostname])
                    break
                
                #got a tracestep
                else:
                    #try to get hostname

                    hostname = ""
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        hostname = "-"

                    #add tracestep to list
                    trace.append([i, reply.src, hostname])
                    

            except:
                print("Thread["+traceId+"]: error", file=sys.stderr)

        #insert trace in db
        self.datadb.insertTrace(traceId, trace)
        print("Thread["+traceId+"]: stop => " + str(time.time() - starttime), file=sys.stderr)


