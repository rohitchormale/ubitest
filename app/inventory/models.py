from app import db


class Inventory(db.Document):
    meta = {"collection": "ubi_inventory"}
    name = db.StringField(max_length=32, unique=True)
    points = db.IntField(min_value=0, default=0)


TRANS_TYPE = (
    ("FP", "free points"),
    ("PP", "purchased points"),
)


class Transaction(db.Document):
    meta = {"collection": "ubi_transaction"}
    user = db.ReferenceField("User", required=True)
    trans_type = db.StringField(max_length=3, choices=TRANS_TYPE, required=True)
    trans_id = db.StringField(required=True) # can be shared between 2 transactions
    points = db.IntField(required=True)
    description = db.StringField(max_length=32, required=False)
    timestamp = db.DateTimeField(required=True)


class FPCredit(db.Document):
    meta = {"collection": "ubi_fpcredit"}
    user = db.ReferenceField("User", required=True, unique=True)
    timestamp = db.DateTimeField(required=True)

