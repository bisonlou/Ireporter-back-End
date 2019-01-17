from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, data):
        '''
        Function to check if incident keys and key dat is present
        Also checks if data is in required format

        '''
        required_keys = ['created_on', 'title', 'comment', 'location', 'type']
        list_values = ['images', 'videos']
        string_values = ['title', 'comment', 'created_on', 'type']

        # get list of missing keys
        missing_keys = [key for key in required_keys if key not in data]
        if len(missing_keys) > 0:
            return False

        # get list of non-string values
        non_strings = [value for value in string_values
                       if type(data[value]) is not str]
        if len(non_strings) > 0:
            return False

        # get list of non-list values
        non_lists = [value for value in list_values
                     if value in data and type(data[value]) is not list]
        if len(non_lists) > 0:
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
