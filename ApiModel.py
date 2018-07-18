from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app 
import requests 

db = SQLAlchemy(app)
api_address = "http://api.openweathermap.org/data/2.5/weather?appid=818eadb9974a00bfb849ddd5935c8144&q="

class Tourism(db.Model):
    __tablename__ = 'tourism'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(15))
    weather_temp = db.Column(db.Integer, nullable=False)
    weather_condition = db.Column(db.String(20), nullable=False)
    places_to_visit = db.Column(db.String(255))
    price = db.Column(db.Float) 

    def json(self):
        return{'city': self.city, 'places_to_visit': self.places_to_visit, 'weather_temp':self.weather_temp, 'weather_condition':self.weather_condition, 'price': self.price}
# get weather by city functions 
    def get_weather_condition(city):
        url = api_address+city
        json_data = requests.get(url).json()
        weather_condition = json_data["weather"][0]['description']
        return weather_condition 

    def get_weather_temp(city):
        url = api_address+city
        json_data = requests.get(url).json()
        rawtemp  = json_data["main"]['temp']
        rawtemp1 = int(rawtemp)
        weather_temp = int(rawtemp1-273.15)
        return weather_temp 

# this Function will add travel packages to the database and fetch temp data from weather Api 
    def add_travel_package(_city, _places_to_visit, _price):
        url = api_address+_city
        json_data = requests.get(url).json()
        _weather_condition = json_data["weather"][0]['description']
        _weather_temp = int((json_data["main"]['temp'])-273.15)
        new_book = Tourism(city=_city, weather_temp=_weather_temp, weather_condition=_weather_condition, places_to_visit=_places_to_visit, price=_price)
        db.session.add(new_book)
        db.session.commit()
        print(new_book) 
# get all the packages from database
    def get_all_travel_package():
        return [Tourism.json(tourism) for tourism in Tourism.query.all()]
# get all the packages by the city
    def get_package_by_city(_city):
        return [Tourism.json(Tourism.query.filter_by(city=_city).first())]
#delete entry from database
    def delete_package(_city):
        Tourism.query.filter_by(city=_city).delete()
        db.session.commit()
        
#update functions 
    def update_travel_price(_city, _price):
        price_to_update = Tourism.query.filter_by(city=_city).first()
        price_to_update.price = _price
        db.session.commit()

    def update_place_to_visit(_city, _places_to_visit):
        places_to_update = Tourism.query.filter_by(city=_city).first()
        places_to_update.places_to_visit = _places_to_visit
        db.session.commit()

    def replace_package(_city, _places_to_visit, _price):
        replacement_package = Tourism.query.filter_by(city=_city).first()
        replacement_package.places_to_visit = _places_to_visit
        replacement_package.price = _price
        db.session.commit()
 
    def __repr__(self):
        tourism_object = {
            'city': self.city,
            'places_to_visit': self.places_to_visit,
            'weather_temp': self.weather_temp,
            'weather_condition': self.weather_condition,
            'price': self.price
            }
        return json.dumps(tourism_object) 