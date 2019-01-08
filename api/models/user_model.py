user_table = []


class User():

    def __init__(self, **kwags):
        self.id = kwags['id']
        self.username = kwags['username']
        self.password = kwags['password']
        self.phone = kwags['phone']
        self.is_admin = kwags['is_admin']


class UserServices():

    def add_user(self, user):
        user_table.append(user)

    def get_user_by_id(self, user_id):
        users = [user for user in user_table if user.id == user_id]
        return users[0]

    def get_user_by_username(self, username):
        return [user for user in user_table if user.username == username]

    def update_phone(self, user_id, new_phone_no):
        user = self.get_user(user_id)
        user[0].phone = new_phone_no

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        user_table.remove(user[0])

    def promote_user(self, user_id):
        user = self.get_user_by_id(user_id)
        user[0].admin = True

    def count(self):
        return len(user_table)

    def remove_all(self):
        user_table.clear()
