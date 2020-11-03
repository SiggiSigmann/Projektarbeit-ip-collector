from icmplib import ping, multiping, traceroute, Host, Hop
import threading
import dbconnector.dbconnector as dbcon

class Tracert():
    def __init__(self, db):
        self.datadb = db

    def execute(self, ip, traceId):
        x = threading.Thread(target=self.run, args=(ip, traceId))
        x.start()

    def run(self, ip, traceId):
        print("start trace", file=sys.stderr)
        trace = traceroute(ip)
        print("stop trace", file=sys.stderr)
        self.datadb.insertTrace(traceId, trace)

