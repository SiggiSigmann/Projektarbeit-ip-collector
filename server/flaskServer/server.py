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

#connect to db
datadb = dbcon.dbconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")

#create clas for traces
tracert = tr.Tracert(datadb)

#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'))


#returns ip as json
@app.route("/ip", methods=["GET"])
def return_ip_josn():
    return jsonify({'ip': request.remote_addr}), 200

#display data in db
@app.route('/data', methods=["GET"])
def display_data():
    data = datadb.read()
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('data.html', data = data, persondata=persondata, runningThreads= runningThreads)

#return data in db as json
@app.route('/data/json', methods=["GET"])
def return_data_json():
    data = datadb.read()
    persondata = datadb.getpersondata()
    return data

#main page
@app.route('/', methods=["GET"])
def index_page():
    ip = request.remote_addr
    return render_template('index.html', ip = ip)

#handel insert in db
@app.route("/", methods=["POST"])
def ip_request():
    #get data form post request
    req = request.form

    #extract data
    ip = request.remote_addr
    username = req["username"]

    #insert ip in database and initiate trace
    traceId = datadb.insert(username, ip)
    tracert.execute(ip, traceId)

    return render_template('index.html', ip = ip, result=1)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
