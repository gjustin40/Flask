import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from myblog import mail

# from pathlib import Path
def save_picture(form_picture):
    fname_hex = secrets.token_hex(8)
    _, ext_name = os.path.splitext(form_picture.filename)
    picture_fname = fname_hex + ext_name
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fname)
    
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fname


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Requset', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To Reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simpy ignore this email and no changes will be made.
'''
    mail.send(msg)