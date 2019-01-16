from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, data):
        '''
        Function to check if incident keys and key dat is present
        Also checks if data is in required format

        '''
        required_keys = ['created_on', 'title', 'comment',
                         'location', 'type']

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
        '''
        Function to check if an incident is modifiable
        An incident is only modifiable if its status is pending
        Returns False if an incident is not modifiable

        '''
        if not incident.status == 0:
            return False
        return True

    def is_owner(self, incident, user_id):
        '''
        Function to check if an incident was created by a given user
        Returns False if the user is not the incident creator

        '''
        if incident.created_by != user_id:
            return False
        return True
