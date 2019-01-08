from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, incident_data):
        required_keys = ["date", "title", "comment", "location", "status",
                         "user_id"]
        for key in required_keys:
            if key not in incident_data:
                return False
        return True

    def is_typeof_list(self, data, value):
        if value in data:
            if type(data[value]) is not list:
                return False
        return True

    def is_typeof_string(self, value):
        if type(value) is not str:
            return False
        return True

    def is_typeof_int(self, value):
        if type(value) is not int:
            return False
        return True

    def is_modifiable(self, incident):
        if not incident.status.upper() == "PENDING":
            return False
        return True

    def is_owner(self, incident, user_id):
        if incident.user_id != user_id:
            return False
        return True
