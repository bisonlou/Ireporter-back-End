from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, data):
        required_keys = ['created_on', 'title', 'comment',
                         'location', 'status', 'type']

        list_values = ['images', 'videos']
        string_values = ['title', 'comment', 'created_on', 'type']

        for key in required_keys:
            if key not in data:
                return False

        for value in string_values:
            if type(data[value]) is not str:
                return False

        for value in list_values:
            if value in data:
                if type(data[value]) is not list:
                    return False

        return True

    def is_modifiable(self, incident):
        if not incident.status.upper() == 'PENDING':
            return False
        return True

    def is_owner(self, incident, user_id):
        if incident.created_by != user_id:
            return False
        return True
