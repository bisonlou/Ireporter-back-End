user_table = []


class User():

    def __init__(self, **kwags):
        self.id = kwags['id']
        self.user_name = kwags['user_name']
        self.email = kwags['email']
        self.password = kwags['password']
        self.phone = kwags['phone_number']
        self.date_registered = kwags['date_registered']
        self.first_name = kwags['first_name']
        self.last_name = kwags['last_name']
        self.other_names = kwags['other_names']
        self.is_admin = kwags['is_admin']


class UserServices():

    def add_user(self, user):
        user_table.append(user)

    def get_user_by_id(self, user_id):
        users = [user for user in user_table if user.id == user_id]
        if len(users) > 0:
            return users[0]

    def get_user_by_email(self, email):
        users = [user for user in user_table if user.email == email]
        if len(users) > 0:
            return users[0]

    def get_all(self):
        return [user.__dict__ for user in user_table]

    def delete_user(self, user_id):
        users = self.get_user(user_id)
        if len(users) > 0:
            user_table.remove(users[0])

    def promote_user(self, user_id):
        users = self.get_user_by_id(user_id)
        if len(users) > 0:
            users[0].is_admin = True

    def count(self):
        return len(user_table)

    def remove_all(self):
        user_table.clear()
