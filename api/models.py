from flask import json

redflag_table = []
user_table = []


class RedFlag():

    def __init__(self, **kwags):
        self.flag_id = kwags['flag_id']
        self.title = kwags['title']
        self.date = kwags['date']
        self.comment = kwags['comment']
        self.user_id = kwags['user_id']
        self.location = kwags['location']
        self.status = kwags['status']
        if 'images' in kwags:
            self.images = kwags['images']
        if 'videos' in kwags:
            self.videos = kwags['videos']

    def get_id(self):
        return self.flag_id

    def to_string(self):
        return f"""{self.flag_id}, {self.title}, {self.comment}, {self.date},
        {self.location}, {self.status}"""

    def to_dict(self):
        return self.__dict__


class RedFlagServices():

    def __init__(self):
        pass

    def post_red_flag(self, red_flag):
        redflag_table.append(red_flag)

    def count(self):
        return len(redflag_table)

    def get_next_flag_id(self):
        return self.count() + 1

    def get_all(self, user_id):
        # check if user is admin
        user_services = UserServices()
        if user_services.user_is_admin(user_id):
            return [red_flag.__dict__ for red_flag in redflag_table]
        # covert flag items to dictionaties
        return [red_flag.__dict__ for red_flag in redflag_table
                if red_flag.user_id == user_id]

    def remove_all(self):
        redflag_table.clear()

    def get_red_flag(self, flag_id):
        # covert flag item to dictionaties
        existing_red_flag = [red_flag for red_flag in
                             redflag_table if red_flag.get_id() == flag_id]
        if len(existing_red_flag) == 0:
            raise ValueError
        return existing_red_flag

    def put_red_flag(self, existing_flag, updated_flag):
        keys = ['title', 'location', 'images', 'videos', 'date', 'comment',
                'status']
        for key in keys:
            if hasattr(updated_flag, key):
                setattr(existing_flag[0], key, getattr(updated_flag, key))

    def patch_red_flag(self, existing_red_flag, red_flag, key):
        setattr(existing_red_flag[0], key, getattr(red_flag, key))

    def delete_red_flag(self, red_flag):
        red_flag = self.get_red_flag(red_flag.get_id())
        redflag_table.remove(red_flag[0])



class User():

    def __init__(self, **kwags):
        self.id = kwags['id']
        self.username = kwags['username']
        self.password = kwags['password']
        self.phone = kwags['phone']
        self.admin = kwags['admin']


class UserServices():

    def add_user(self, user):
        user_table.append(user)

    def get_user_by_id(self, user_id):
        return [user for user in user_table if user.id == user_id]

    def get_user_by_username(self, username):
        return [user for user in user_table if user.username == username]

    def update_phone(self, user_id, new_phone_no):
        user = self.get_user(user_id)
        user[0].phone = new_phone_no

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        user_table.remove(user[0])

    def user_is_admin(self, user_id):
        user = self.get_user_by_id(user_id)
        return user[0].admin

    def promote_user(self, user_id):
        user = self.get_user_by_id(user_id)
        user[0].admin = True

    def count(self):
        return len(user_table)

    def remove_all(self):
        user_table.clear()
