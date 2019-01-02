import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, json, jsonify, abort
from api.models import RedFlag, RedFlagServices, User, UserServices
from api.Validator import ValidateRedFlags
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'bison'

red_flag_services = RedFlagServices()
user_services = UserServices()


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'greeting': 'Welcome to iReporter',
        'post flag': '/api/v1/redflag',
        'get flags': '/api/v1/redflags',
        'get flag': '/api/v1/redflag/flag_id',
        'alter flag': '/api/v1/redflag/flag_id',
        'update flag': '/api/v1/redflag/flag_id/key',
        'delete flag': '/api/v1/redflag/flag_id'
    }), 200


@app.route('/api/v1/redflag', methods=['POST'])
@jwt_required
def add_red_flag():
    data = request.get_json()
    user_id = get_jwt_identity()

    flag_id = red_flag_services.get_next_flag_id()

    data['flag_id'] = flag_id
    data['user_id'] = user_id
    data['status'] = 'Pending'
    validate_keys(data)

    red_flag = RedFlag(**data)

    red_flag_services.post_red_flag(red_flag)
    success_response = {'id': flag_id, 'message': 'Created red-flag record'}
    return jsonify({'status': 201, 'data': [success_response]}), 201


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_red_flags():
    user_id = get_jwt_identity()

    return jsonify({'status': 200, 'data': red_flag_services.get_all(user_id)})


@app.route('/api/v1/redflag/<int:flag_id>', methods=['GET'])
@jwt_required
def get_red_flag(flag_id):
    red_flags = get_red_flag_by_Id(flag_id)
    return jsonify({'status': 200, 'data': red_flags[0].to_dict()}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['PUT'])
@jwt_required
def alter_red_flag(flag_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    data['user_id'] = user_id
    validate_keys(data)

    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, user_id)
    validate_is_modifiable(existing_flag)

    data['flag_id'] = flag_id
    update_flag = RedFlag(**data)

    red_flag_services.put_red_flag(existing_flag, update_flag)

    updated_red_flag = red_flag_services.get_red_flag(update_flag.get_id())
    return jsonify({'status': 200, 'data':
                    [updated_red_flag[0].to_dict()]})


@app.route('/api/v1/redflag/<int:flag_id>/<string:query>', methods=['PATCH'])
@jwt_required
def update_red_flag_location(flag_id, query):
    data = request.get_json()
    user_id = get_jwt_identity()

    data['user_id'] = user_id
    validate_keys(data)

    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, user_id)
    validate_is_modifiable(existing_flag)

    data['flag_id'] = flag_id
    red_flag = RedFlag(**data)

    red_flag_services.patch_red_flag(existing_flag, red_flag, query)
    success_response = {
        'id': flag_id,
        'message': f'Updated red-flag record’s {query}'
    }
    return jsonify({'status': 200, 'data': [success_response]}), 200


@app.route('/api/v1/redflag/<int:flag_id>', methods=['DELETE'])
@jwt_required
def delete_red_flag(flag_id):
    user_id = get_jwt_identity()

    existing_flag = get_red_flag_by_Id(flag_id)
    validate_is_owner(existing_flag, user_id)
    validate_is_modifiable(existing_flag)

    red_flag_services.delete_red_flag(existing_flag[0])

    success_response = {
        'id': flag_id,
        'message': 'red-flag record has been deleted'
    }
    return jsonify({'status': 200, 'data': [success_response]}), 200


@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    user_id = str(uuid.uuid4())
    data['id'] = user_id
    data['password'] = hashed_password
    data['admin'] = False

    new_user = User(**data)
    user_services.add_user(new_user)

    success_response = {'id': user_id, 'message': 'User created'}
    return jsonify({'status': 201, 'data': [success_response]}), 201


@app.route('/api/v1/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        abort(401)
    user = user_services.get_user_by_username(auth['username'])

    if not user:
        abort(401)

    if check_password_hash(user[0].password, auth['password']):
        access_token = create_access_token(identity=user[0].id)
        return jsonify(access_token=access_token), 200

    abort(401)


def get_red_flag_by_Id(flag_id):
    try:
        return red_flag_services.get_red_flag(flag_id)
    except ValueError:
        abort(404)


def validate_keys(data):
    try:
        ValidateRedFlags.has_required_keys(data)
    except KeyError or TypeError:
        abort(400)


def validate_is_owner(existing_red_flag, user_id):
    if existing_red_flag[0].user_id != user_id:
        abort(401)


def validate_is_modifiable(existing_flag):
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
