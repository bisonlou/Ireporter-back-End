from flask import Flask, request, json, jsonify, abort
from api.models import RedFlag, RedFlags
from api.Validator import ValidateRedFlags

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
            'greeting': 'Welcome to iReporter',
            'post flag': 'https://bisonlou.herokuapp.com/api/v1/redflag',
            'get flags': 'https://bisonlou.herokuapp.com/api/v1/redflags',
            'get flag': 'https://bisonlou.herokuapp.com/api/v1/redflag/flag_id',
            'alter flag': 'https://bisonlou.herokuapp.com/api/v1/redflag/flag_id',
            'update flag': 'https://bisonlou.herokuapp.com/api/v1/redflag/flag_id/key',
            'delete flag': 'https://bisonlou.herokuapp.com/api/v1/redflag/flag_id'
            }), 200


@app.route('/api/v1/redflag', methods=['POST'])
def add_red_flag():
    data = request.get_json()
    validate_keys(data)

    red_flags = RedFlags()
    flag_id = red_flags.get_next_flag_id()

    data['flag_id'] = flag_id
    red_flag = RedFlag(**data)

    red_flags.post_red_flag(red_flag)
    success_response = {'id': flag_id, 'message': 'Created red-flag record'}
    return jsonify({'status': 201, 'data': [success_response]}), 201


@app.route('/api/v1/redflags', methods=['GET'])
def get_red_flags():    
    return jsonify({'status': 200, 'data': RedFlags.get_all()})


@app.route('/api/v1/redflag/<int:flag_id>', methods=['GET'])
def get_red_flag(flag_id):
    red_flags = get_red_flag_by_Id(flag_id)
    return jsonify({'status': 200, 'data': red_flags[0].to_dict()}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['PUT'])
def alter_red_flag(flag_id):
    data = request.get_json()
    validate_keys(data)

    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, data['user_id'])
    validate_is_modifiable(existing_flag)

    data['flag_id'] = flag_id
    update_flag = RedFlag(**data)

    RedFlags.put_red_flag(existing_flag, update_flag)

    updated_red_flag = RedFlags.get_red_flag(update_flag.get_id())
    return jsonify({'status': 200, 'data':
                    [updated_red_flag[0].to_dict()]})


@app.route('/api/v1/redflag/<int:flag_id>/<string:query>', methods=['PATCH'])
def update_red_flag_location(flag_id, query):
    data = request.get_json()
    validate_keys(data)
    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, data['user_id'])
    validate_is_modifiable(existing_flag)

    data['flag_id'] = flag_id
    red_flag = RedFlag(**data)

    RedFlags.patch_red_flag(existing_flag, red_flag, query)
    success_response = {
            'id': flag_id,
            'message': f'Updated red-flag record’s {query}'
            }
    return jsonify({'status': 200, 'data': [success_response]}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['DELETE'])
def delete_red_flag(flag_id):
    data = request.get_json()
    validate_keys(data)    

    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, data['user_id'])
    validate_is_modifiable(existing_flag)

    RedFlags.delete_red_flag(existing_flag[0])

    success_response = {
        'id': flag_id,
        'message': 'red-flag record has been deleted'
    }
    return jsonify({'status': 200, 'data': [success_response]}), 200


def get_red_flag_by_Id(flag_id):
    try:
        return RedFlags.get_red_flag(flag_id)
    except ValueError:
        abort(404)


def validate_keys(data):
    try:
        ValidateRedFlags.has_required_keys(data)
    except KeyError or TypeError:
        abort(400)


def validate_is_owner(existing_red_flag, flag_id):
    if existing_red_flag[0].flag_id is not flag_id:
        abort(401)


def validate_is_modifiable(existing_flag):
    print(existing_flag[0].status.upper())
    if existing_flag[0].status.upper() != "PENDING":
        abort(403)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 404, 'error': 'Not Found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 400, 'error': 'Bad Request'}), 400


@app.errorhandler(401)
def bad_request(error):
    return jsonify({'status': 401, 'error': 'Unauthorised'}), 401


@app.errorhandler(403)
def bad_request(error):
    return jsonify({'status': 403, 'error': 'Forbidden'}), 403
