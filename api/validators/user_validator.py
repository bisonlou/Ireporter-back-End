import re


class UserValidator():

    def has_required_fields(self, data):

        keys = ['user_name', 'password', 'first_name',
                'last_name', 'email', 'phone_number',
                'date_registered', 'other_names']

        for key in keys:
            if key not in data:                
                return False

        required_keys = ['user_name', 'first_name', 'last_name',
                         'email', 'phone_number', 'date_registered']

        for key in required_keys:
            if not data[key]:
                return False

        return True

    def validate_password(self, data):
        password = data['password']
        errors = {}
        if len(password) < 6:
            errors['min-length'] = 'Password should be 6 or more characters'
        if len(password) > 12:
            errors['max-length'] = 'Password should be 12 or less characters'
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
        required_keys = ['email', 'password']

        for key in required_keys:
            if key not in data:
                return False

        for key in required_keys:
            if not data[key]:
                return False

        return True

    def user_is_admin(self, user):
        return user.is_admin
