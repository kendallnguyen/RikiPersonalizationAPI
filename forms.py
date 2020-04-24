from flask_wtf import FlaskForm, validators
import wtforms
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Required


class preferences(FlaskForm):
    name = StringField('Name')
    backgroundColor = StringField('backgroundColor')
    textColor = StringField('textColor')
    buttonColor = StringField('buttonColor')
    font = StringField('font')
    theme = StringField('theme')
    submit = SubmitField('Submit')
