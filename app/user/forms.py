"""
This module implements various forms related with user registration and authentication

@author: Rohit Chormale
"""

from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=32)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=32)])
    # email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=32)])
    username = StringField("Username", validators=[InputRequired(), Length(max=32)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=5, max=32)])


class LoginForm(FlaskForm):
    # email = StringField("Email", validators=[InputRequired(), Email(), Length(max=32)])
    username = StringField("Username", validators=[InputRequired(), Length(max=32)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=5, max=32)])

