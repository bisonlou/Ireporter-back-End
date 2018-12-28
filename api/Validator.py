from flask import jsonify
from api.models import RedFlags


class ValidateRedFlags():

    def has_required_keys(red_flag_data):
        required_keys = ["date", "title", "comment", "location",
                         "user_id"]
        for key in required_keys:
            if key not in red_flag_data:
                raise KeyError

    def is_id_int(flag_id):
        if not int(flag_id) or flag_id == '':
            raise TypeError

