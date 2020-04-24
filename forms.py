from flask_wtf import FlaskForm, validators
import wtforms
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Required


class preferences(FlaskForm):
    name = StringField('')
    backgroundColor = StringField('')
    textColor = StringField('')
    buttonColor = StringField('')
    font = StringField('')
    theme = StringField('')
    submit = SubmitField('')
