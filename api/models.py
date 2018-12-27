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
        red_flag = [red_flag for red_flag in
                    db if red_flag.get_id() == flag_id]
        if len(red_flag) > 0:
            return red_flag
        else:
            return 404

    @staticmethod
    def put_red_flag(red_flag):
        current_red_flag = [flag for flag in
                            db if flag.get_id() == red_flag.get_id()]
        if len(current_red_flag) > 0:
            keys = ['title', 'location', 'image', 'video', 'date', 'comment']
            for key in keys:
                setattr(current_red_flag[0], key, getattr(red_flag, key))
        else:
            return 404

    @staticmethod
    def patch_red_flag(red_flag, key):
        current_red_flag = [flag for flag in
                            db if flag.get_id() == red_flag.get_id()]
        if len(current_red_flag) > 0:
            setattr(current_red_flag[0], key, getattr(red_flag, key))
        else:
            return 404

    @staticmethod
    def delete_red_flag(red_flag):
        current_red_flag = [flag for flag in
                            db if flag.get_id() == red_flag.get_id()]

        db.remove(current_red_flag[0])


class RedFlag():

    def __init__(self, flag_id, title, date, comment, location, user_id,
                 image=None, video=None):
        self.flag_id = flag_id
        self.title = title
        self.date = date
        self.location = location
        self.comment = comment
        self.user_id = user_id
        self.image = image
        self.video = video

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



    
