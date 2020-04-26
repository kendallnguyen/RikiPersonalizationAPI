from flask_wtf import FlaskForm, validators, Form

from wtforms import StringField, BooleanField, SubmitField, TextField, Field, HiddenField, RadioField
from wtforms.validators import DataRequired, InputRequired, Optional, Length, ValidationError


class preferences(FlaskForm):
    method = RadioField('I want to: (must choose one)', choices=[('put', 'change all of my preferences'), ('patch', 'change some preferences'), ('post', 'create a new user')])
    name = StringField('Name', [InputRequired()])
    backgroundColor = StringField('BackgroundColor', [InputRequired()])
    textColor = StringField('TextColor', [InputRequired()])
    buttonColor = StringField('ButtonColor', [InputRequired()])
    font = StringField('Font', [InputRequired()])
    submit = SubmitField()
    delete = SubmitField('Yes, Delete Me')
    put = SubmitField('change all of my preferences')
    post = SubmitField('change some of my preferences')


