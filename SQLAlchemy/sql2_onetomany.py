from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onetomany.sqlite3' #/// : 현재 디렉토리 - //// : 절대 디렉토리
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

'''
    한 사람 당 여러 마리의 반려견을 키울 수 있음.
    one(Person) to Many(Pet) 모델 생성
'''

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pet', backref='owner') # 'Pet'은 관계가 있는 table 이름
                                                   # backref 옵션은 실제로는 존재하지 않지만 둘 사이를 이어주는 다리역할을 해줌
                                                   # 나중에 instance로 접근이 가능하다.(ex. 특정 pet의 onwer을 불러올 때 pet_name.owner_name 이런식으로 호출 가능) 
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id')) # ForeignKey는 one-to-many 관계가 있는 table과 연결시켜주는 고리
                                                                 # ForeignKey가 바라보는 primarykey를 지정해야함
                                                                 # 해당 table의 이름을 '소문자'로 하는 것이 특징

'''
    sqlite3 onetomany.sqlite3 실행 후

    justin = Person(name='Justin') / Person1 생성
    sakong = Person(name='Sakong') / Person2 생성

    pet1 = Pet(name='Pet1', owner=justin) / Pet1 생성 : backref옵션을 통해 owner를 사용할 수 있음. 이때 객체를 넣어줘야함('justin' 이거는 안 됨...)
                                                      : 이미 객체를 생성한 상태에서만 owner 활용 가능

    pet1 = Pet.query.filter_by(name='Pet1') / Pet1 객체 불러온 후에
    pet1.name                               / Pet1의 이름도 호출하고
    pet1.owner.name                         / Pet1의 owner의 이름도 호출 가능 졸라 신기
'''