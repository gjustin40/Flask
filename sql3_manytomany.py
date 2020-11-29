from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manytomany.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
    한 User가 여러개의 channel을 볼 수 있지만
    한 Channel을 여러 User들이 볼 수도 있으니 ManytoMany 관계
'''

# 밑에 있는 테이블은 ManytoMany의 관계를 만들 때 두 개의 연결고리를 위한 서브 테이블
# 실제로 이 테이블을 수정하는 일은 없지만, 두 테이블(user, channel)에 있는 데이터 중 관계가 되는 것들을
# 표시해놓는 테이블
user_channel = db.Table('user_channel',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('chaneel_id', db.Integer, db.ForeignKey('channel.channel_id'))
)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    channels = db.relationship('Channel', secondary=user_channel, backref='subscribers') # secondary를 통해 관계 정립
                                                                                         # backref은 앞에서도 봤듯이 연결고리, 어떤 객체로 불러올꺼냐

class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(50))