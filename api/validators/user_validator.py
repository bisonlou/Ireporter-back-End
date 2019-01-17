import re


class UserValidator():

    def has_required_fields(self, data):
        '''
        Function to check if user keys and key data is present
        Also checks if data is in required format
        Returns True on succes otherwise False

        '''
        keys = ['user_name', 'password', 'first_name',
                'last_name', 'email', 'phone_number',
                'date_registered', 'other_names']

        # get list of missing keys
        missing_keys = [key for key in keys if key not in data]
        if len(missing_keys) > 0:
            return False

        required_keys = ['user_name', 'first_name', 'last_name',
                         'email', 'phone_number', 'date_registered']

        # get list of keys with missing data
        missing_data = [key for key in required_keys if not data[key]]
        if len(missing_data):
            return False

        return True

    # TODO : validate email

    def validate_password(self, data):
        '''
        Function to check if the given password meets minimum requrements
        Returns a dictionary of errors

        '''
        password = data['password']
        errors = {}
        if len(password) < 6 or len(password) > 12:
            errors['length'] = 'Password should be between 6 and 12 characters'
        if not re.search("[a-z]", password):
            errors['lower-char'] = 'Password should contain atleast 1 lower case character'
        if not re.search("[0-9]", password):
            errors['numerical-char'] = 'Password should contain atleast 1 number'
        if not re.search("[A-Z]", password):
            errors['upper-char'] = 'Password should contain atleast 1 upper case character'
        if not re.search("[$#@]", password):
            errors['symbol-char'] = "Password should contain atleast 1 of '$','#','@'"

        return errors

    def has_login_required_fields(self, data):
        '''
        Function to check if the login data is present
        Returns True on success otherwise False

        '''
        required_keys = ['email', 'password']

        for key in required_keys:
            if key not in data or not data[key]:
                return False

        return True

    def user_is_admin(self, user):
        '''
        Function to check if the is an administrator
        Return True if the user is an administrator
        otherwise False

        '''
        return user.is_admin
