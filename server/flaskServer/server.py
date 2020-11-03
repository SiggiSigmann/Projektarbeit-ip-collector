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
    print(data, file=sys.stderr)
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
