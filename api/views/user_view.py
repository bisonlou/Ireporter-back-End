from api import app
from flask import request
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.get_json()
    return user_controller.register(data)


@app.route('/api/v1/login', methods=['POST'])
def login():
    auth = request.get_json()
    return user_controller.login(auth)
