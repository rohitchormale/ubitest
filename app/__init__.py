from flask import Flask, redirect, render_template
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .helpers import JSONEncoder


# app and components initialization
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.json_encoder = JSONEncoder
csrf = CSRFProtect(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "user.login"


# blueprint registrations
from app.user.routers import user_blueprint
app.register_blueprint(user_blueprint)

from app.inventory.routers import inventory_blueprint
app.register_blueprint(inventory_blueprint)


# abstract common routes which can be changed in future
@app.route("/")
def home():
    """Handle root resource request"""
    return redirect("/inventory/dashboard")


@app.errorhandler(404)
def page_not_found(e):
    """Handle error gracefully"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server error gracefully"""
    return render_template("500.html"), 500
