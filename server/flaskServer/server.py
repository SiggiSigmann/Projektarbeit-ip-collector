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
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import dbconnector.dbconnector as dbcon
import tracert as tr
from plotter import Plotter
from evaluation import Evaluation

#connect to db
datadb = dbcon.DBconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")

#create clas for traces
tracert = tr.Tracert(datadb)

#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'), static_folder=os.path.abspath('/static/'))

#create plotter to create images
plotter = Plotter(datadb)

eval= Evaluation(datadb)

### download #####################
@app.route('/download/')
def return_total_file():
    data = datadb.read()
    x = datetime.datetime.now()
    date = x.strftime("%Y%m%d-%H%M")
    return Response(json.dumps(data, indent=2), mimetype='text/plain', headers={"Content-Disposition":"attachment;filename=total_data_ip_collector_"+date+".json"})

#return data in db as json file
@app.route('/download/<username>/', methods=["GET"])
def return_total_file_user(username):
    data = datadb.read(username)
    return Response(json.dumps(data, indent=2), mimetype='text/plain', headers={"Content-Disposition":"attachment;filename="+username+"_data_ip_collector_"+date+".json"})

### image #########################
@app.route('/image/<image>')
def return_image(image):
    fig = plotter.create_image(image)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

### diagram #######################
#returns diagrams for all user based on json from plotter class
@app.route('/diagram/', methods=["GET"])
def diagram():
    data = plotter.get_Json("Total")
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('diagram.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = "Total")

@app.route('/diagram/<username>/', methods=["GET"])
#returns diagrams for given user (in <username>) based on json from plotter class
def diagram_user(username):
    data = plotter.get_Json(username)
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('diagram.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = username)

### compare #########################
#comapre total with total
@app.route('/compare/', methods=["GET"])
def comp():
    data = plotter.get_compare_json("Total", "Total")
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('compare.html', data = data, persondata=persondata, runningThreads= runningThreads, act1 = "Total", act2 = "Total")

@app.route("/compare/",  methods=["POST"])
#comapre user given in Post (user1 and user2)
def comp_user():
    #get data form post request
    req = request.form

    #extract data
    ip = request.remote_addr
    user1 = req["user1"]
    user2  = req["user2"]
    
    data = plotter.get_compare_json(user1, user2)
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('compare.html', data = data,  persondata=persondata, runningThreads= runningThreads, act1 = user1, act2 = user2)

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
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('data.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = "Total")

#display data in db
@app.route('/data/<username>/', methods=["GET"])
def display_data_by_name(username):
    data = datadb.read(username)
    persondata = datadb.get_person_data()
    runningThreads = tracert.getThreads()
    return render_template('data.html', data = data, persondata=persondata, runningThreads= runningThreads, actual = username)

#return data in db as json
@app.route('/data/json/', methods=["GET"])
def return_data_json():
    data = datadb.read()
    return data

#return data in db as json
@app.route('/data/json/<username>/', methods=["GET"])
def return_data_json_username(username):
    data = datadb.read(username)
    return data

### main ################################
#main page
#handel insert in db
@app.route("/", methods=["GET", "POST"])
def ip_request():

    #get most likely user
    ip = request.remote_addr
    prob , uname = eval.max_likely_user(ip)

    if request.method == 'POST':
        #get data form post request
        req = request.form

        #extract data
        ip = request.remote_addr
        username = req["username"]

        #insert ip in database and initiate trace
        traceId = datadb.insert(username, ip)
        tracert.execute(ip, traceId)

        return render_template('index.html', ip = ip, result=1, proposal=prob, username=uname)

    else:
        ip = request.remote_addr
        return render_template('index.html', ip = ip, proposal=prob, username=uname)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
