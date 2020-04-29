from flask import abort, Flask, jsonify
from flask import make_response
from flask import request
from flask_cors import CORS, cross_origin

import os, sys, json

import services

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/search', methods=['GET'])
@cross_origin()
def search():
    q = request.args.get('q', type=str)
    prf = request.args.get('prf', type=str)
    
    prfBool = False
    if prf == "true":
        prfBool = True

    results = services.handle_query(q, prfBool)
    return json.dumps([ob.__dict__ for ob in results])

@app.route('/api/file/<string:file_name>', methods=['GET'])
@cross_origin()
def file(file_name):
    result = services.get_file(file_name)
    return result

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
