from flask_wtf import FlaskForm, validators
import wtforms
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired



class render_field:
    pass


class preferences(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    backgroundColor = StringField('BackgroundColor')
    textColor = StringField()
    buttonColor = StringField()
    font = StringField()
    theme = StringField()
    submit = SubmitField()
