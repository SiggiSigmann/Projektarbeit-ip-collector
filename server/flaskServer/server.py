from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
import os
import dbconnector.dbconnector as dbcon
import socket
import tracert as tr
from scapy.all import *
import sys


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
        
        trace.append([i,"-", "notfound"])
        print("--> " + str(i) + " -" , file=sys.stderr) 
    elif reply.type == 3:
        # We've reached our destination
        trace.append([i,reply.src, socket.gethostbyaddr(reply.src)])
        print("--> " + str(i) + " " + reply.src, file=sys.stderr) 
        break
    else:
    # We're in the middle somewhere
        trace.append([i,reply.src, socket.gethostbyaddr(reply.src)])
        print("--> " + str(i) + " " + reply.src, file=sys.stderr) 

print(trace, file=sys.stderr)
print("stop trace", file=sys.stderr)


datadb = dbcon.dbconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")#
datadb.select()

tracert = tr.Tracert(datadb)

template_dir = os.path.abspath('/html/')
app = Flask(__name__, template_folder=template_dir)


@app.route("/return/ip", methods=["GET"])
def get_my_ip1():

    return jsonify({'ip': request.remote_addr}), 200
    #headers = request.headers
    #return "Request headers:\n" + str(headers)
    #return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


@app.route('/data', methods=["GET"])
def datapage():
    data = datadb.select()
    return render_template('data.html', data = data)

@app.route('/', methods=["GET"])
def indexfunc():
    ip = request.remote_addr
    return render_template('index.html', ip = ip)


@app.route("/", methods=["POST"])
def handel_ip():

    if request.method == "POST":

        req = request.form

        ip = request.remote_addr
        username = req["username"]

        traceId = datadb.insert(username, ip)

        tracert.execute(ip, traceId)

        return render_template('index.html', ip = "ok")

    return render_template('index.html', ip = "err")

@app.route('/ip/<ip>')
def index_fake(ip):
    return render_template('index.html', ip = ip)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)