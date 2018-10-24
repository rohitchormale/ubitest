#!/usr/bin/env python3

"""
FreePoints Credit Service. This service credits user free points as per configuration. Configuration can be found at `config.py'.

Do NOT run this script directly. Instead use singleton script `bin/fpcservice.sh`

@author: Rohit Chormale
"""


import logging
import datetime
logging.basicConfig(level=logging.DEBUG, filename='/tmp/fpcservice.log', filemode='a')
from flask import Flask
from flask_mongoengine import MongoEngine
from app.inventory.models import Transaction, FPCredit
from app.helpers import generate_transaction_id

# app and components initialization
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = MongoEngine(app)


def main():
    timestamp = datetime.datetime.now() - datetime.timedelta(hours=app.config["FP_CREDIT_DURATION_HOURS"], minutes=app.config["FP_CREDIT_DURATION_MINS"])
    fp_credit_users = FPCredit.objects(timestamp__lte=timestamp)
    for fp in fp_credit_users:
        if fp.user.free_points >= int(app.config["FP_CREDIT_MAX_POINTS"]):
            app.logger.info("Skipping user. Free points already reached to threshold %s" %(fp.user.username))
            fp.delete()
            continue

        credit_points = app.config["FP_CREDIT_MAX_POINTS"] - fp.user.free_points
        if credit_points > app.config["FP_CREDIT_POINTS"]:
            credit_points = app.config["FP_CREDIT_POINTS"]
        fp.user.free_points = fp.user.free_points + credit_points
        try:
            fp.user.save()
            trans_timestamp = datetime.datetime.now()
            trans_fp = Transaction(user=fp.user, trans_type="FP", trans_id=generate_transaction_id(), points=credit_points, description="Free Points Credited", timestamp=trans_timestamp)
            trans_fp.save()
            if fp.user.free_points >= int(app.config["FP_CREDIT_MAX_POINTS"]):
                app.logger.debug("Deleting user %s from free credit queue as threshold reached %s" % fp.user.username)
                fp.delete()
            else:
                fp.timestamp = trans_timestamp
                fp.save()
        except Exception as e:
            app.logger.error("Error in FreeCredit Service")
        app.logger.info("%s Free Points credited to %s" %(credit_points, fp.user.username))
    app.logger.info("[*] Service finished !!!")


if __name__ == "__main__":
    app.logger.info("[*] Service started...")
    main()
