from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)

@app.route("/ip", methods=["GET"])
def get_my_ip1():
    return jsonify({'ip': request.remote_addr}), 200

print(__name__)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)