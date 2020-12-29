from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
from flask import Response

import sys
import os
import socket
import io
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import dbconnector.dbconnector as dbcon
import tracert as tr
from plotter import Plotter

#from scapy.all import *
#import sys


#connect to db
datadb = dbcon.DBconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")

#create clas for traces
tracert = tr.Tracert(datadb)

#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'), static_folder=os.path.abspath('/static/'))

plotter = Plotter(datadb)

### image #########################
@app.route('/image/<image>')
def return_image(image):
    fig = plotter.create_image(image)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

### diagram #######################
@app.route('/diagram/', methods=["GET"])
def diagram():
    data = plotter.get_Json("total")
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('diagram.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = "Total")

@app.route('/diagram/<username>/', methods=["GET"])
def diagram_user(username):
    data = plotter.get_Json(username)
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('diagram.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = username)

### compare #########################
"""*@app.route('/compare/', methods=["GET"])
def comp():
    data = plotter.get_compare_json("total", "total")
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('compare.html', data = data, persondata=persondata, runningThreads= runningThreads, act1 = "Total", act2 = "Total")"""

@app.route("/compare/",  methods=["POST", "GET"])
def comp_user():
    if request.method == 'POST':
        #get data form post request
        req = request.form

        #extract data
        ip = request.remote_addr
        user1 = req["per1"]
        user2  = req["per2"]
        print(f"-->{user1} {user2}<--", file=sys.stderr)
        
        data = plotter.get_compare_json(user1, user2)
        persondata = datadb.getpersondata()
        runningThreads = tracert.getThreads()
        return render_template('compare.html', data = data,  persondata=persondata, runningThreads= runningThreads, act1 = user1, act2 = user2)
    else:

        data = plotter.get_compare_json("total", "total")
        persondata = datadb.getpersondata()
        runningThreads = tracert.getThreads()
        return render_template('compare.html', data = data, persondata=persondata, runningThreads= runningThreads, act1 = "Total", act2 = "Total")

### ip ##############################
#returns ip as json
@app.route("/ip/", methods=["GET"])
def return_ip_josn():
    return jsonify({'ip': request.remote_addr}), 200

### data #############################
#display data in db
@app.route('/data/', methods=["GET"])
def display_data():
    data = datadb.read()
    #print(data, file=sys.stderr)
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('data.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = "Total")

#display data in db
@app.route('/data/<username>/', methods=["GET"])
def display_data_by_name(username):
    data = datadb.read(username)
    persondata = datadb.getpersondata()
    runningThreads = tracert.getThreads()
    return render_template('data.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = username)

#return data in db as json
@app.route('/data/json/', methods=["GET"])
def return_data_json():
    data = datadb.read()
    persondata = datadb.getpersondata()
    return data

### main ################################
#main page
#handel insert in db
@app.route("/", methods=["GET", "POST"])
def ip_request():
    if request.method == 'POST':
        #get data form post request
        req = request.form

        #extract data
        ip = request.remote_addr
        username = req["username"]

        #insert ip in database and initiate trace
        traceId = datadb.insert(username, ip)
        tracert.execute(ip, traceId)

        return render_template('index.html', ip = ip, result=1)

    else:
        ip = request.remote_addr
        return render_template('index.html', ip = ip)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
