from datetime import datetime, timedelta
import sys
import json
from requests import get
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def get_data(city):
    data = get(api_url, params={'q': city, 'units': 'metric', 'appid': api_key})
    return data.json()


def get_weather(data):
    return {"name": data['name'], "temperature": int(data['main']['temp']), "state": data['weather'][0]['main']}


@app.route("/add", methods=['POST'])
def add_city():
    if request.method == 'POST':
        city = request.form['city_name']
        data = get_data(city)

        if data['cod'] == "404":
            flash(data['message'], 'Error')
            return redirect(url_for('index'))

        if any(db.session.query(City).filter(City.name == data['name'])):
            flash("City already displayed")
            redirect(url_for('index'))

        row = City(**get_weather(data), date=datetime.utcnow()+ timedelta(seconds=int(data['timezone'])))
        db.session.add(row)
        db.session.commit()
        return redirect(url_for('index'))


@app.route("/delete/<city_id>", methods=['POST', 'GET'])
def delete_city(city_id):
    if request.method == 'POST':
        row = db.session.query(City).filter(City.id == city_id).first()
        if row:
            db.session.delete(row)
            db.session.commit()
        else:
            flash("City not in a database.")
    return redirect(url_for('index'))


@app.route("/update/<city_id>", methods=['POST', 'GET'])
def update_state(city_id):
    if request.method == 'POST':
        row = db.session.query(City).filter(City.id == city_id).first()
        if row:
            data = get_data(row.name)
            weather = get_weather(data)
            row.temperature = weather['temperature']
            row.state = weather['state']
            row.date = datetime.utcnow() + timedelta(seconds=int(data['timezone']))
            db.session.commit()
        else:
            flash("City not in a database.")
    return redirect(url_for('index'))


@app.route("/", methods=['GET'])
def index():
    cities = db.session.query(City).all()
    return render_template('index.html', cities=cities)


if __name__ == '__main__':
    
    with open('./secrets/app_key.json', 'r') as app_key_f:
        app_key = json.load(app_key_f)['APP_KEY']

    app.secret_key = app_key

    api_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = ""
    with open('./secrets/api_key.json', 'r') as api_key_f:
        api_key = json.load(api_key_f)['API_SECRET_KEY']

    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/city.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class City(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), unique=True, nullable=False)
        temperature = db.Column(db.Integer, nullable=False)
        state = db.Column(db.String(40), nullable=False)
        date = db.Column(db.DateTime, nullable=False)

        def __repr__(self):
            return f"<City: {self.name}>"

    db.create_all()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
