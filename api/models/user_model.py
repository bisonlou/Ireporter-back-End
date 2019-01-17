user_table = []


class User():

    def __init__(self, **kwags):
        self._id = kwags['id']
        self._user_name = kwags['user_name']
        self._email = kwags['email']
        self._password = kwags['password']
        self._phone_number = kwags['phone_number']
        self._date_registered = kwags['date_registered']
        self._first_name = kwags['first_name']
        self._last_name = kwags['last_name']
        self._other_names = kwags['other_names']
        self._is_admin = kwags['is_admin']

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def is_admin(self):
        return self._is_admin

    def to_dict(self):
        return dict(id=self._id,
                    user_name=self._user_name,
                    email=self._email,
                    password=self._password,
                    phone_number=self._phone_number,
                    date_registered=self._date_registered,
                    first_name=self._first_name,
                    last_name=self._last_name,
                    other_names=self._other_names,
                    is_admin=self._is_admin)


class UserServices():

    def add_user(self, user):
        user_table.append(user)

    def get_user_by_id(self, user_id):
        return self.get_user('id', user_id)

    def get_user_by_email(self, login_email):
        return self.get_user('email', login_email)

    def get_user(self, key, value):
        users = []
        if key == 'id':
            users = [user for user in user_table if user.id == value]
        elif key == 'email':
            users = [user for user in user_table if user.email == value]

        # only return if ther is a user found
        if len(users) > 0:
            return users[0]

    def get_all(self):
        return [user.to_dict() for user in user_table]

    # def delete_user(self, user_id):
    #     users = self.get_user(user_id)
    #     if len(users) > 0:
    #         user_table.remove(users[0])

    # def promote_user(self, user_id):
    #     users = self.get_user_by_id(user_id)
    #     if len(users) > 0:
    #         users[0].is_admin = True

    def count(self):
        return len(user_table)

    def remove_all(self):
        user_table.clear()
