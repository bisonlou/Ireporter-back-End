from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, data):
        # required_keys = ['createdOn', 'title', 'comment',
        #                  'location', 'status', 'type']

        # list_values = ['Images', 'Videos']
        # string_values = ['title', 'comment', 'createdOn', 'type']

        # for key in required_keys:
        #     if key not in data:
        #         return False

        if 'createdOn' not in data:
            return False
        if 'title' not in data:
            return False
        if 'comment' not in data:
            return False
        if 'location' not in data:
            return False
        if 'status' not in data:
            return False
        if 'type' not in data:
            return False

        # for value in string_values:
        #     if type(data[value]) is not str:
        #         return False

        if type(data['title']) is not str:
            return False
        if type(data['comment']) is not str:
            return False
        if type(data['createdOn']) is not str:
            return False
        if type(data['type']) is not str:
            return False

        # for value in list_values:
        #     if value in data:
        #         if type(data[value]) is not list:
        #             return False
        if 'Images' in data:
            if type(data['Images']) is not list:
                return False

        if 'Videos' in data:
            if type(data['Videos']) is not list:
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
