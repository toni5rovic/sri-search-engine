from flask import abort, Flask, jsonify
from flask import make_response
from flask import request
import os, sys

import services

app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def search():
    q = request.args.get('q', type=str)
    results = services.handle_query(q)
    return jsonify(results)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
