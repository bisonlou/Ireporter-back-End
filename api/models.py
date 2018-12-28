from flask import json

db = []


class RedFlags():
    def post_red_flag(self, red_flag):
        db.append(red_flag)

    @staticmethod
    def count():
        return len(db)

    def get_next_flag_id(self):
        return self.count() + 1

    @staticmethod
    def get_all():
        # covert flag items to dictionaties
        return [RedFlag.__dict__ for RedFlag in db]

    @staticmethod
    def remove_all():
        db.clear()

    @staticmethod
    def get_red_flag(flag_id):
        # covert flag item to dictionaties
        existing_red_flag = [red_flag for red_flag in
                             db if red_flag.get_id() == flag_id]
        if len(existing_red_flag) == 0:
            raise ValueError
        return existing_red_flag

    @staticmethod
    def put_red_flag(existing_flag, update_flag):        
        keys = ['title', 'location', 'image', 'video', 'date', 'comment']
        for key in keys:
            setattr(existing_flag[0], key, getattr(update_flag, key))

    @staticmethod
    def patch_red_flag(existing_red_flag, red_flag, key):
        setattr(existing_red_flag[0], key, getattr(red_flag, key))

    @staticmethod
    def delete_red_flag(red_flag):
        found_red_flag = RedFlags.get_red_flag(red_flag.get_id())
        if found_red_flag == 0:
            return 404
        db.remove(found_red_flag[0])


class RedFlag():

    def __init__(self, **kwags):
        self.flag_id = kwags['flag_id']
        self.title = kwags['title']
        self.date = kwags['date']
        self.comment = kwags['comment']
        self.user_id = kwags['user_id']
        self.location = kwags['location']     
        if 'image' in kwags:
            self.image = kwags['image']
        if 'video' in kwags:
            self.video = kwags['video']

    def get_id(self):
        return self.flag_id

    def title(self, new_title):
        self.title = new_title

    def comment(self, new_comment):
        self.comment = new_comment

    def date(self, new_date):
        self.date = new_date

    def location(self, new_location):
        self.location = new_location

    def image(self, new_image):
        self.image = new_image

    def video(self, new_video):
        self.video = new_video

    def to_string(self):
        return f'{self.flag_id}, {self.title}, {self.comment}, {self.date}, {self.location}'

    def to_dict(self):
        return self.__dict__
        # return {'flag_id': self.flag_id,
        #         'title': self.title,
        #         'date': self.date,
        #         'comment': self.comment,
        #         'location': self.location,
        #         'image': self.image,
        #         'video': self.video,
        #         'user_id': self.user_id
        #         }



    
