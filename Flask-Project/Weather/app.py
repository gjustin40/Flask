from flask import Flask, request, render_template, redirect, url_for, flash
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db' #users가 테이블이 될 것이다. Table
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 불필요한 warning을 없애줄것이다.
app.secret_key = 'weather'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=6805469813f27791b0a7c54dc5bb1468&lang=kr'
api_key = '6805469813f27791b0a7c54dc5bb1468'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['POST'])
def index_post():
    if request.method == 'POST':
        new_city_name = request.form.get('city')

        new_city_data = requests.get(url.format(new_city_name)).json()
        print(new_city_data)
        print('=========================')
        if new_city_data['cod'] != 200:
            flash('This is not in the world!', 'error')

        else:    
            if City.query.filter_by(name=new_city_name).first():
                flash('This is in the Database', 'error')

            else:
                new_city = City(name=new_city_name)
                db.session.add(new_city)
                db.session.commit()
                flash('Check the {} weather!'.format(new_city_name))

    return redirect(url_for('index'))

@app.route('/')
def index():
 
    weather_data_list = []
    cites = City.query.all()

    for city in reversed(cites):
        city_data = requests.get(url.format(city.name)).json()
        weather_data = {
            'weather_id' : city.id,
            'name' : city_data['name'],
            'temp' : city_data['main']['temp'],
            'weather' : city_data['weather'][0]['main'],
            'detail' : city_data['weather'][0]['description'],
            'icon' : city_data['weather'][0]['icon'],
            'wind' : city_data['wind']['speed']
        }
        weather_data_list.append(weather_data)
    return render_template('index.html', weather_data_list=weather_data_list)

@app.route('/delete/<int:weather_id>')
def index_delete(weather_id):
    
    city = City.query.get(weather_id)
    db.session.delete(city)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

