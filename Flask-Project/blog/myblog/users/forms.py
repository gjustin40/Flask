from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from myblog.models import User


class RegistrationForm(FlaskForm):
    """ Registration """

    username = StringField('Username',
                           validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    confirm_pswd = PasswordField('Confirm Password',
                            validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(f"'{username.data}' is already taken. Please choose different Username.")
        
    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError(f"'{email.data}' is already taken. Please choose different Username.")
        


class LoginForm(FlaskForm):
    """ Login """
    
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    """ Updating Account """

    username = StringField('Username',
                           validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user_object = User.query.filter_by(username=username.data).first()
            if user_object:
                raise ValidationError(f"'{username.data}' is already taken. Please choose different Username.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user_object = User.query.filter_by(email=email.data).first()
            if user_object:
                raise ValidationError(f"'{email.data}' is already taken. Please choose different Username.")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    submit = SubmitField('Requset Password Reset')

    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object is None:
            raise ValidationError("There is no account with that email. You must register first.")
            

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[InputRequired()])
    confirm_pswd = PasswordField('Confirm Password',
                            validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')