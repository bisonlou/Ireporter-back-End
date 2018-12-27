from flask import jsonify
from api.models import RedFlags


def validate_red_flag(red_flag_data):
    required_keys = ["date", "title", "comment", "location",
                     "user_id"]
    for key in required_keys:
        if key not in red_flag_data:
            return 400


def validate_id(flag_id):
    if not int(flag_id) or flag_id == '':
        return 400
