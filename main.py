from flask import Flask, jsonify, request, abort
import ujson
import user_utils
import os
import time

app = Flask(__name__)

@app.before_request
def before():
    global requestIP
    requestIP = request.remote_addr.replace('.','')
    requestIP = int(requestIP)
    
    
@app.route('/')
def welcome():
    response = ({'response':'Welcome to the SBAHA API'})
    return jsonify(response)

@app.route('/inventory/')
def inventory():
    response = user_utils.inventory()
    return jsonify(response)

@app.route('/data/')
def data_request():
    ip = request.args.get('ip')
    data = user_utils.data_request(ip)
    return jsonify(data)

@app.route('/reset/')
def reset_lc():
    ip = request.args.get('ip')
    data = user_utils.reset_lc(ip)
    return jsonify(data)

@app.route('/stats/')
def stats():
    data = user_utils.stats()
    return jsonify(data)    
    

if __name__ == '__main__':
    #app.run(host='89.40.11.37', port=443, ssl_context=('server.crt', 'server.key'))
    app.run(debug=True, port=5000)
