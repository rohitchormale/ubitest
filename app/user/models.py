from flask_login import UserMixin
from app import db


class User(UserMixin, db.Document):
    meta = {"collection": "ubi_user"}
    first_name = db.StringField(max_length=32, required=True)
    last_name = db.StringField(max_length=32)
    # email = db.StringField(max_length=32, required=True, unique=True)
    username = db.StringField(max_length=32, required=True, unique=True)
    password = db.StringField(required=True)
    admin = db.BooleanField(default=False)
    free_points = db.IntField(min_value=0)
    purchased_points = db.IntField(min_value=0)
    inventory_list = db.ListField(db.ReferenceField('Inventory'))

    def save(self, *args, **kwargs):
        if not self.free_points:
            self.free_points = 0
        if not self.purchased_points:
            self.purchased_points = 0
        return super(User, self).save(*args, **kwargs)