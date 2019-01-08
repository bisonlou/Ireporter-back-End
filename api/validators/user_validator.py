
class UserValidator():

    def has_required_fields(self, data):
        if not data or not data['username'] or not data['password']:
            return False
        return True
