from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
from flask import Response
from flask import make_response
from flask import send_from_directory

import sys
import os
import socket
import io
import json
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_weasyprint import HTML, render_pdf

import dbconnector.dbconnector as dbcon
import tracert as tr
from plotter import Plotter
from evaluation import Evaluation
from subnet import Subnet

#init classes
#connect to db
datadb = dbcon.DBconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")

#create clas for traces
tracert = tr.Tracert(datadb)

#create subnet to get info about ip
sub = Subnet("/files/de.csv")

#create plotter to create images
plotter = Plotter(datadb, sub)

#create evaluetor to predic username
eval= Evaluation(datadb)

## Flask ##########################################################
#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'), static_folder=os.path.abspath('/static/'))

### robot.txt ####################
@app.route('/robots.txt')
def return_robots_txt():
    return app.send_static_file("robots.txt")

### humans.txt ####################
@app.route('/humans.txt')
def return_humans_txt():
    return app.send_static_file("humans.txt")


### humans.txt ####################
@app.route('/manifest.webmanifest')
def return_manifest_txt():
    return app.send_static_file("manifest.webmanifest")

### pdf ##########################
@app.route('/download/pdf/diagram/<from_date>/<to_date>/')
def create_pdf_for_diagram(from_date,to_date):
    available_images = plotter.get_diagram_json("Total", from_date,to_date)
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    html = render_template('diagram_pdf_template.html', available_images = available_images, actual_user = "Total", from_date=from_date, to_date=to_date)
    return render_pdf(HTML(string=html), download_filename="total_diagram_"+from_date+"-"+to_date+"_"+date+".pdf")

@app.route('/download/pdf/diagram/<username>/<from_date>/<to_date>/')
def create_pdf_for_diagram_for_user(username, from_date,to_date):
    available_images = plotter.get_diagram_json(username,from_date,to_date)
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    html = render_template('diagram_pdf_template.html', available_images = available_images, actual_user = username, from_date=from_date, to_date=to_date)
    return render_pdf(HTML(string=html), download_filename=username+"_diagram_"+from_date+"-"+to_date+"_"+date+".pdf")

#comapre total with total
@app.route('/download/pdf/compare/<from_date>/<to_date>/', methods=["GET"])
def create_pdf_for_compare(from_date,to_date):
    available_images = plotter.get_compare_json("Total", "Total",from_date,to_date)
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    html = render_template('compare_pdf_template.html', available_images = available_images, actual_user_1 = "Total", actual_user_2 = "Total", from_date=from_date, to_date=to_date)
    return render_pdf(HTML(string=html), download_filename="Total_Total_compare_"+from_date+"-"+to_date+"_"+date+".pdf")

@app.route("/download/pdf/compare/<from_date>/<to_date>/",  methods=["POST"])
#comapre user given in Post (user1 and user2)
def create_pdf_for_diagram_for_users(from_date,to_date):
    #get data form post request
    req = request.form

    #extract data
    ip = request.remote_addr
    user1 = req["user1"]
    user2  = req["user2"]

    available_images = plotter.get_compare_json(user1, user2,from_date,to_date)

    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    html = render_template('compare_pdf_template.html', available_images = available_images, actual_user_1 = user1, actual_user_2 = user2, from_date=from_date, to_date=to_date)
    return render_pdf(HTML(string=html), download_filename=user1+"_"+user2+"_compare_"+from_date+"-"+to_date+"_"+date+".pdf")
    

### download #####################
@app.route('/download/json/')
def return_total_as_json_file():
    data = datadb.read()
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    return Response(json.dumps(data, indent=2), mimetype='text/plain', headers={"Content-Disposition":"attachment;filename=total_data_ip_collector_"+date+".json"})

#return data in db as json file
@app.route('/download/json/<username>/', methods=["GET"])
def return_total_as_json_file_for_user(username):
    data = datadb.read(username)
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d-%H%M")
    return Response(json.dumps(data, indent=2), mimetype='text/plain', headers={"Content-Disposition":"attachment;filename="+username+"_data_ip_collector_"+date+".json"})

### image #########################
@app.route('/image/<image>')
def return_image(image):
    fig = plotter.create_image(image)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/white/image/<image>')
def return_image_white(image):
    fig = plotter.create_image(image,0)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

### diagram #######################
#returns diagrams for all user based on json from plotter class
@app.route('/diagram/', methods=["GET"])
def diagram():
    now = datetime.datetime.now()
    to_date = now.strftime("%Y-%m-%d")
    from_date = datadb.get_first_measurement()

    available_images = plotter.get_diagram_json("Total", from_date, to_date)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('diagram.html', available_images = available_images, person_data=person_data, running_Threads= running_Threads, actual_user = "Total", from_date=from_date, to_date=to_date)

@app.route('/diagram/', methods=["POST"])
def diagram_time():
    req = request.form

    from_date = req["from_date"]
    to_date = req["to_date"]

    available_images = plotter.get_diagram_json("Total", from_date, to_date)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('diagram.html', available_images = available_images, person_data=person_data, running_Threads= running_Threads, actual_user = "Total", from_date=from_date, to_date=to_date)

@app.route('/diagram/<username>/', methods=["GET"])
#returns diagrams for given user (in <username>) based on json from plotter class
def diagram_user(username):
    now = datetime.datetime.now()
    to_date = now.strftime("%Y-%m-%d")
    from_date = datadb.get_first_measurement(username)

    available_images = plotter.get_diagram_json(username, from_date, to_date)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('diagram.html', available_images = available_images, person_data=person_data, running_Threads= running_Threads, actual_user = username, from_date=from_date, to_date=to_date)

@app.route('/diagram/<username>/', methods=["POST"])
#returns diagrams for given user (in <username>) based on json from plotter class
def diagram_user_date(username):
    req = request.form

    from_date = req["from_date"]
    to_date = req["to_date"]

    available_images = plotter.get_diagram_json(username, from_date, to_date)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('diagram.html', available_images = available_images, person_data=person_data, running_Threads= running_Threads, actual_user = username, from_date=from_date, to_date=to_date)

### compare #########################
#comapre total with total
@app.route('/compare/', methods=["GET"])
def comapre_user_with_most_entries():
    actual_user_1 = "Total"
    actual_user_2 = "Total"
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()

    if len(person_data['persons']) > 2:
        actual_user_1 = person_data['persons'][1]['name']
        actual_user_2 = person_data['persons'][2]['name']

    now = datetime.datetime.now()
    to_date = now.strftime("%Y-%m-%d")
    from_date_1 = datadb.get_first_measurement(actual_user_1)
    from_date_2 = datadb.get_first_measurement(actual_user_2)

    #get biggest time range
    if from_date_1>from_date_2:
        from_date = from_date_1
    else:
        from_date = from_date_2

    available_images = plotter.get_compare_json(actual_user_1, actual_user_2, from_date, to_date)
    return render_template('compare.html', available_images = available_images, person_data=person_data, running_Threads= running_Threads, actual_user_1 = actual_user_1, actual_user_2 = actual_user_2, from_date=from_date, to_date=to_date)

@app.route("/compare/",  methods=["POST"])
#comapre user given in Post (user1 and user2)
def comapre_user_in_post():
    #get data form post request
    req = request.form

    #extract data
    ip = request.remote_addr
    user1 = req["user1"]
    user2  = req["user2"]

    from_date = req["from_date"]
    to_date = req["to_date"]
    
    available_images = plotter.get_compare_json(user1, user2, from_date, to_date)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('compare.html', available_images = available_images,  person_data=person_data, running_Threads= running_Threads, actual_user_1 = user1, actual_user_2 = user2, from_date=from_date, to_date=to_date)

### data #############################
#display data in db
@app.route('/data/', methods=["GET"])
def display_data():
    data = datadb.read()
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('data.html', data = data, person_data=person_data, running_Threads= running_Threads, actual_user = "Total")

#display data in db
@app.route('/data/<username>/', methods=["GET"])
def display_data_by_name(username):
    data = datadb.read(username)
    person_data = datadb.get_persons()
    running_Threads = tracert.get_Threads()
    return render_template('data.html', data = data, person_data=person_data, running_Threads= running_Threads, actual_user = username)

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
@app.route("/", methods=["GET"])
def ip_request():
    #get most likely user
    ip = request.remote_addr
    got_proposal, proposal_user = eval.max_likely_user(ip)

    ip = request.remote_addr
    return render_template('index.html', ip = ip, proposal=got_proposal, username=proposal_user)

@app.route("/", methods=["POST"])
def ip_request_post():
    ip = request.remote_addr
    
    #get data form post request
    req = request.form
    print(req , file=sys.stderr)

    #extract data
    ip = request.remote_addr
    username = req["username"]
    username = username.replace(".", "")
    username = username.replace("_", "")
    if not username.isalpha():
        username = "error"

    ip_info = sub.get_ip_location(ip)

    #insert ip in database and initiate trace
    traceId = datadb.insert(username, ip, ip_info)
    tracert.execute(ip, traceId)

    #get most likely user
    got_proposal, proposal_user = eval.max_likely_user(ip)

    return render_template('index.html', ip = ip, result=1, proposal=got_proposal, username=proposal_user)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
