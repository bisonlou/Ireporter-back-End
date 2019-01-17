import uuid
from api import app
from api.models.user_model import UserServices, User
from api.validators.user_validator import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort, request
from flask_jwt_extended import create_access_token, get_jwt_identity

user_services = UserServices()
validator = UserValidator()


class UserController():
    '''
    Class to handle user related routes

    '''

    def register(self):
        '''
        Function to register a user

        '''
        data = request.get_json()
        hashed_password = generate_password_hash(
                            data['password'], method='sha256')
        user_id = str(uuid.uuid4())

        if not validator.has_required_fields(data):
            abort(400)

        errors = validator.validate_password(data)
        if len(errors) > 0:
            return jsonify({'status': 400, 'data': errors}), 400

        data['id'] = user_id
        data['password'] = hashed_password

        if user_services.count() == 0:
            data['is_admin'] = True
        else:
            data['is_admin'] = False

        new_user = User(**data)
        user_services.add_user(new_user)
        success_response = {'id': user_id, 'message': 'User created'}

        return jsonify({'status': 201, 'data': success_response}), 201

    def login(self):
        '''
        Function to login a user
        The user must be registered
        The function returns a jason web token

        '''
        data = request.get_json()
        if not validator.has_login_required_fields(data):
            abort(400)

        user = user_services.get_user_by_email(data['email'])
        if not user:
            abort(401)

        if check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        abort(401)

    def get_all(self):
        '''
        Function to return all users given a user id
        The user should be an administrator in order to get all the uses

        '''
        user_id = get_jwt_identity()
        user = user_services.get_user_by_id(user_id)
        if not validator.user_is_admin(user):
            abort(403)

        users = user_services.get_all()

        return jsonify({'status': 200, 'data': users}), 200
