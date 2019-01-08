import uuid
from api import app
from api.models.user_model import UserServices, User
from api.validators.user_validator import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort
from flask_jwt_extended import create_access_token

user_services = UserServices()
validator = UserValidator()


class UserController():

    def register(self, data):
        hashed_password = generate_password_hash(
                            data['password'], method='sha256')

        user_id = str(uuid.uuid4())
        data['id'] = user_id
        data['password'] = hashed_password
        data['is_admin'] = False

        new_user = User(**data)
        user_services.add_user(new_user)

        success_response = {'id': user_id, 'message': 'User created'}

        return jsonify({'status': 201, 'data': [success_response]}), 201

    def login(self, data):
        if not validator.has_required_fields(data):
            abort(401)
        user = user_services.get_user_by_username(data['username'])

        if not user:
            abort(401)

        if check_password_hash(user[0].password, data['password']):
            access_token = create_access_token(identity=user[0].id)
            return jsonify(access_token=access_token), 200

        abort(401)

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({'status': 401, 'error': 'Unauthorised'}), 401
