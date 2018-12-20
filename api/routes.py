from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import api.models

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello world'})


@app.route('/api/v1/redflag', methods=['POST'])
def add_red_flag():

    if not request.json:
        abort(400)
    if 'date' not in request.json:
        abort(400)
    if 'offender' not in request.json:
        abort(400)
    if 'description' not in request.json:
        abort(400)  

    red_flag = {
            'id':  models.get_current_id() + 1,
            'date': request.json['date'],
            'offender': request.json['offender'],
            'description': request.json['description']
            }
    success_response = {
        'id': models.get_current_id() + 1,
        'message': 'Created red-flag record'
    }

    models.add_red_flag(red_flag)
    return jsonify({'status': 201, 'data': [success_response]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}, 404))


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400
