# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    backgroundColor = db.Column(db.String(80))
    textColor = db.Column(db.String(80))
    buttonColor = db.Column(db.String(80))
    font = db.Column(db.String(80))
    theme = db.Column(db.String(80))

    def json(self):
        return {'name': self.name, 'backgroundColor': self.backgroundColor,
                'textColor': self.textColor, 'buttonColor': self.buttonColor,
                'font': self.font, 'theme': self.theme}

    def add_user(_name, _backgroundColor, _textColor,
                 _buttonColor, _font, _theme):
        new_user = User(name=_name, backgroundColor=_backgroundColor,
                        textColor=_textColor, buttonColor=_buttonColor,
                        font=_font, theme=_theme)
        db.session.add(new_user)
        db.session.commit()

    def get_all_users():
        return [User.json(user) for user in User.query.all()]

    def get_user(_name):
        return [User.json(User.query.filter_by(name=_name).first())]

    def delete_user(_name):
        is_successful = User.query.filter_by(name=_name).delete()
        db.session.commit()
        return bool(is_successful)

    def update_user_name(_name, _newName):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update.name = _newName
        db.session.commit()

    def update_user_backgroundColor(_name, _backgroundColor):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update.backgroundColor = _backgroundColor
        db.session.commit()

    def update_user_textColor(_name, _textColor):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update.textColor = _textColor
        db.session.commit()

    def update_user_buttonColor(_name, _buttonColor):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update._buttonColor = _buttonColor
        db.session.commit()

    def update_user_font(_name, _font):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update.font = _font
        db.session.commit()

    def update_user_theme(_name, _theme):
        user_to_update = User.query.filter_by(name=_name).first()
        user_to_update.theme = _theme
        db.session.commit()

    def replace_user(_name, _backgroundColor, _textColor,
                     _buttonColor, _font, _theme):
        user_to_replace = User.query.filter_by(name=_name).first()
        user_to_replace.backgroundColor = _backgroundColor
        user_to_replace.textColor = _textColor
        user_to_replace.buttonColor = _buttonColor
        user_to_replace.font = _font
        user_to_replace.theme = _theme
        db.session.commit()

    def __repr__(self):
        user_object = {
            'name': self.name,
            'background-color': self.backgroundColor,
            'text-color': self.textColor,
            'button-color': self.buttonColor,
            'font': self.font,
            'theme': self.theme
        }
        return json.dumps(user_object)
