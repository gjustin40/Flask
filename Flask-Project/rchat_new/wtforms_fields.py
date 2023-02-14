from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256

from models import *


def invalid_credentials(form, field):
    """ Username as Password checker """

    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError('Username or Password is incorret')
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError('Username or Password is incorret')


class RegistrationForm(FlaskForm):

    username = StringField(
        label='username',
        validators=[
            InputRequired(message='Username Required'),
            Length(min=4, max=25, message='Username must be between 4 to 25 characters')])
    password = PasswordField(
        label='password',
        validators=[
            InputRequired(message='password Required'),
            Length(min=4, max=25, message='password must be between 4 to 25 characters')])
    confirm_pswd = PasswordField(
        label='Confirm Password',
        validators=[
            InputRequired(message='confirm_pswd Required'),
            EqualTo('password', message='Password is incorrect')])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        print('aaaaaaaaaaaaaaaaaaaaaaaaa')
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(f"'{username.data}' is already exists. Select a different username.")


class LoginForm(FlaskForm):

    username = StringField(label='username',
                           validators=[InputRequired(message='Username required')])

    password = PasswordField(label='password',
                             validators=[InputRequired(message='Passowrd required'),invalid_credentials])

    submit_button = SubmitField('Login')
