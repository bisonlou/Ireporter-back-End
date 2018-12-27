from flask import Flask, request, json, jsonify
from api.models import RedFlag, RedFlags
import api.Validator

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'greeting': 'Welcome to iReporter',
                    'post flag': '/api/v1/redflag',
                    'get flags': '/api/v1/redflags',
                    'get flag': '/api/v1/redflag/flag_id',
                    'alter flag': '/api/v1/redflag/flag_id',
                    'update flag': '/api/v1/redflag/flag_id/key',
                    'delete flag': '/api/v1/redflag/flag_id'
                    })


@app.route('/api/v1/redflag', methods=['POST'])
def add_red_flag():
    data = request.get_json()   
    if api.Validator.validate_red_flag(data) == 400:
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    red_flags = RedFlags()
    flag_id = red_flags.get_next_flag_id()
    red_flag = RedFlag(flag_id, data['title'], data['date'], data['comment'],
                       data['location'], data['user_id'], data['image'],
                       data['video'])
    red_flags.post_red_flag(red_flag)

    success_response = {
        'id': flag_id,
        'message': 'Created red-flag record'
    }
    return jsonify({'status': 201, 'data': [success_response]}), 201


@app.route('/api/v1/redflags', methods=['GET'])
def get_red_flags():
    return jsonify({'status': 200, 'data':
                    RedFlags.get_all()})


@app.route('/api/v1/redflag/<int:flag_id>', methods=['GET'])
def get_red_flag(flag_id):
    if api.Validator.validate_id(flag_id) == 404:
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    response = RedFlags.get_red_flag(flag_id)
    if response == 404:
        return jsonify({'status': 404, 'error': 'Not Found'}), 404
    else:
        return jsonify({'status': 200, 'data': response[0].to_dict()}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['PUT'])
def alter_red_flag(flag_id):
    data = request.get_json()
    if api.Validator.validate_id(flag_id) == 400:
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    if api.Validator.validate_red_flag(data) == 400:
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    red_flag = RedFlag(flag_id, data['title'], data['date'], data['comment'],
                       data['location'], data['user_id'], data['image'],
                       data['video'])
    if RedFlags.put_red_flag(red_flag) == 404:
        return jsonify({'status': 404, 'error': 'Not Found'}), 404
    else:
        updated_red_flag = RedFlags.get_red_flag(red_flag.get_id())
        return jsonify({'status': 200, 'data':
                        [updated_red_flag[0].to_dict()]})


@app.route('/api/v1/redflag/<int:flag_id>/<string:query>', methods=['PATCH'])
def update_red_flag_location(flag_id, query):
    data = request.get_json()
    if api.Validator.validate_red_flag(data) == 400:
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    red_flag = RedFlag(flag_id, data['title'], data['date'], data['comment'],
                       data['location'], data['user_id'], data['image'],
                       data['video'])

    if RedFlags.patch_red_flag(red_flag, query) == 404:
        return jsonify({'status': 404, 'error': 'Not Found'}), 404
    else:
        success_response = {
            'id': flag_id,
            'message': f'Updated red-flag record’s {query}'
            }
    return jsonify({'status': 200, 'data': [success_response]}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['DELETE'])
def delete_red_flag(flag_id):

    red_flag = RedFlags.get_red_flag(flag_id)
    if red_flag != 404:
        RedFlags.delete_red_flag(red_flag[0])
    else:
        return jsonify({'status': 404, 'error': 'Not Found'}), 404

    success_response = {
        'id': flag_id,
        'message': 'red-flag record has been deleted'
    }
    return jsonify({'status': 200, 'data': [success_response]}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 404, 'error': 'Not Found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 400, 'error': 'Bad Request'}), 400
