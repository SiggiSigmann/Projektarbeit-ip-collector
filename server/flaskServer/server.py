from flask import request
from flask import jsonify
from flask import Flask
from flask import render_template
import os


template_dir = os.path.abspath('/html/')
app = Flask(__name__, template_folder=template_dir)


@app.route("/ip", methods=["GET"])
def get_my_ip1():

    return jsonify({'ip': request.remote_addr}), 200
    #headers = request.headers
    #return "Request headers:\n" + str(headers)
    #return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route('/')
def index():
    ip = request.remote_addr
    return render_template('index.html', ip = ip)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)