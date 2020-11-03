from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
import os
import dbconnector.dbconnector as dbcon
import socket

data = dbcon.dbconnector(socket.gethostbyname('db'),"networkdata", "root", "1234567")

data.insert()
data.select()



template_dir = os.path.abspath('/html/')
app = Flask(__name__, template_folder=template_dir)


@app.route("/return/ip", methods=["GET"])
def get_my_ip1():

    return jsonify({'ip': request.remote_addr}), 200
    #headers = request.headers
    #return "Request headers:\n" + str(headers)
    #return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route('/', methods=["GET"])
def indexfunc():
    ip = request.remote_addr
    return render_template('index.html', ip = ip)

@app.route("/", methods=["POST"])
def handel_ip():

    if request.method == "POST":

        req = request.form
        return jsonify(req), 200

    return jsonify({'ip': request.remote_addr}), 200

@app.route('/ip/<ip>')
def index_fake(ip):
    return render_template('index.html', ip = ip)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)