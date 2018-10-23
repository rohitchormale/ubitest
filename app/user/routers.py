"""
Routes -

Configure blueprint and routes for different controllers in app
"""


from flask import Blueprint
from .controllers import *

user_blueprint = Blueprint('user', 'user', url_prefix='/user')
user_blueprint.add_url_rule('register', 'register', register, methods=["GET", "POST"])
user_blueprint.add_url_rule('login', 'login', login, methods=["GET", "POST"])
user_blueprint.add_url_rule('logout', 'logout', logout, methods=["POST",])



