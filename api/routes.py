from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)

red_flags = []


def add_red_flag(red_flag):
    red_flags.append(red_flag)


def get_current_id():
    if len(red_flags) == 0:
        return 0        
    return red_flags[-1]['id']
    

def get_all_red_flags():
    return red_flags


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
            'id':  get_current_id() + 1,
            'date': request.json['date'],
            'offender': request.json['offender'],
            'location': request.json['location'],
            'description': request.json['description'],
            'image': request.json['image'],
            'video': request.json['video']
            }
            
    success_response = {
        'id': get_current_id() + 1,
        'message': 'Created red-flag record'
    }

    red_flags.append(red_flag)
    return jsonify({'status': 201, 'data': [success_response]})


@app.route('/api/v1/redflags', methods=['GET'])
def get_red_flags():

    return jsonify({'status': 200, 'data': [red_flags]})


@app.route('/api/v1/redflag/<int:flag_id>/<string:location>', methods=['PATCH'])
def update_red_flag(flag_id, location):

    if not int(flag_id):
        abort(400)
    if len(location) == 0:
        abort(400)

    red_flag = [red_flag for red_flag in red_flags if red_flag['id'] == flag_id]

    if len(red_flags[0]) == 0:
        abort(404)
    
    red_flag[0]['location'] = location

    success_response = {
        'id': red_flag[0]['id'],
        'message': 'Updated red-flag record’s location'
    }

    return jsonify({'status': 200, 'data': [success_response]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}, 404))


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400
