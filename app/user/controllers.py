from flask import request, render_template, redirect, flash, session, url_for
from mongoengine.errors import NotUniqueError
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import current_user, login_user, login_required, logout_user
from .forms import *
from .models import *


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Handle unauthorized requests"""
    return redirect(url_for("user.login"))


def register():
    """Handle registration request"""
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        password = generate_password_hash(form.password.data, method="sha256")
        try:
            user = User.objects.create(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, password=password)
        except NotUniqueError as e:
            key = str(e).split("index: ")[-1].split("_")[0]
            flash("%s already exists" % key.title())
            return render_template("register.html", form=form)
        login_user(user)
        return redirect(url_for("inventory.dashboard"))
    return render_template("register.html", form=form)


def login():
    """Handle login requests"""
    if current_user.is_authenticated:
        return redirect(url_for("inventory.dashboard"))

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.objects(username=form.username.data).first()
        if user is None:
            flash("Invalid username/password")
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("inventory.dashboard"))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@login_required
def logout():
    """Handle logout request. Invalid user session"""
    logout_user()
    return redirect(url_for("user.login"))


