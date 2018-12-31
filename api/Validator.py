from flask import jsonify
from api.models import RedFlags


class ValidateRedFlags():

    def has_required_keys(red_flag_data):
        required_keys = ["date", "title", "comment", "location", "status",
                         "user_id"]
        for key in required_keys:
            if key not in red_flag_data:
                raise KeyError

        optional_keys = ["images", "videos"]   
        for key in optional_keys:
            if key in red_flag_data:
                if type(red_flag_data[key]) is not list:
                    raise TypeError
