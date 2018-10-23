from flask_wtf.form import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange


class AddInventoryForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=32)])
    points = IntegerField("Price in Points", validators=[InputRequired(), NumberRange(min=0, max=1000)])


class PurchaseItemForm(FlaskForm):
    name = StringField("Inventory Name", validators=[InputRequired(), Length(max=32)])


class PurchasePointsForm(FlaskForm):
    points = IntegerField("Purchase Points (Only for testing)", validators=[InputRequired(), NumberRange(min=0, max=50)])
