from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

from myblog.models import User, Post


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
            
class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired()])
    content = TextAreaField('Content',
                            validators=[InputRequired()])
    submit = SubmitField('Post')