from flask import Flask, jsonify, request, Response, render_template
import json
from settings import *
from ApiModel import *
import jwt, datetime
from flask_restplus import Api, Resource

places_list = [
  {
    "city":"Dublin",
    "place_to_visit":[
      "Guinness Storehouse",
      "Temple Bar",
      "Dublin Castel",
      "Phoenix Park",
      "St Stephen’s Green",
      "Spire of Dublin",
      "Dublin Zoo",
      "Christ Church Cathedral"
    ],
    "package":"3day, 4night",
    "cost":"200"
  },
  {
    "city":"Galway",
    "place_to_visit":[
      "Connemara National Park",
      "The Fisheries Watchtower Museum",
      "Clifden Sky Road",
      "Kinvara",
      "Salthill Promenade",
      "Dunguaire Castle",
      "Galway City Museum",
      "Galway Cathedral"
    ],
    "package":"2 Days 3 Nights",
    "cost":"200"
  },
  {
    "city":"Cork",
    "place_to_visit":[
      "St. Anne's Church Shandon Bells",
      "Cork Butter Museum",
      "Cork City Goal",
      "Elizabeth Fort, Barrack Street",
      "Cork Vision Centre",
      "Collins Barracks Cork Military Museum",
      "University College Cork (UCC)"
    ],
    "package":"2 Days 3 Nights",
    "cost":"175"
  },
  {
    "city":"Waterford",
    "place_to_visit":[
      "Hook Lighthouse",
      "The Irish National Heritage Park",
      "Johnstown Castle & Gardens",
      "Kilmore Quay and the Saltee Islands"
    ],
    "package":"1 Day 2 Nights",
    "cost":"220"
  },
  {
    "city":"Kilkenny",
    "place_to_visit":[
      "St Canice's Cathedral",
      "Black Abbey",
      "Rothe House",
      "St. Mary’s Medieval Mile Museum"
    ],
    "package":"Day Trip",
    "cost":"90"
  },
  {
    "city":"Athlone",
    "place_to_visit":[
      "Athlone Castle",
      "Luan Gallery",
      "Moydrum Castle",
      "Ss. Peter & Pauls Church",
      "Lough Ree",
      "Athlone Equestrian Centre"
    ],
    "package":"Day Trip",
    "cost":"130"
  },
  {
    "city":"Westport",
    "place_to_visit":[
      "Knubble Bay",
      "Bonyun Preserve",
      "Porter Preserve",
      "Nickels-Sortwell House",
      "Fort Edgecomb",
      "Castle Tucker"
    ],
    "package":"Daytrip",
    "cost":"80"
  },
  {
    "city":"Limerick",
    "place_to_visit":[
      "King John's Castle",
      "Hunt Museum",
      "St Mary's Cathedral",
      "King's Island",
      "St John's Cathedral",
      "Frank McCourt Museum"
    ],
    "package":"1 Day 2 Nights",
    "cost":"210"
  },
  {
    "city":"Dingle",
    "place_to_visit":[
      "Dingle Oceanworld Aquarium",
      "Gallarus Oratory",
      "An Diseart",
      "St James' Church",
      "Dingle Peninsula",
      "St Mary's Catholic Church",
      "Eask Tower"
    ],
    "package":"2 Days 2 Nights",
    "cost":"180"
  },
  {
    "city":"Belfast",
    "place_to_visit":[
      "Belfast City Hall",
      "Titanic Quarter",
      "Waterfront Hall",
      "Belfast Castle",
      "Ulster Museum",
      "Victoria Square Shopping centre",
      "Stormont Parliament Buildings",
      "Odyssey Arena",
      "St. Georges Market",
      "Grand Opera House"
    ],
    "package":"3 Days 4 Nights",
    "cost":"300"
  }
]


app.config['SECRET_KEY'] = 'DontLo$eit'

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json ')

def validObject(Object):
    if("city" in Object and "places_to_visit" in Object and "price" in Object):
        return True
    else:
        return False
#get all the travel packages 
@app.route('/tourism')
def get_package():
    return jsonify({'tourism': Tourism.get_all_travel_package()})

#update/replace packages 
@app.route('/tourism/<city>', methods=['PUT'])
def update_package(city):
    request_data = request.get_json()
    Tourism.replace_package(city, request_data['places_to_visit'],request_data['price'])
    response = Response("", status=204)
    return response

#Working
@app.route('/home')
def main():
    return render_template('index.html')

#to patch the database 
@app.route('/tourism/<city>', methods=['PATCH'])
def patch_database(city):
    request_data = request.get_json()
    updated_db = {}
    if ("places_to_visit" in request_data):
        Tourism.update_place_to_visit(city, request_data['places_to_visit'])
    if ("price" in request_data):
        Tourism.update_travel_price(city, request_data['price'])
    
    response = Response("", status=204)
    response.headers['Location'] = "/tourism/" + str(city)
    return response 

#Delete the package
@app.route('/tourism/<city>', methods=['DELETE'])
def delete_entry(city):
    Tourism.delete_package(city)
    response = Response(json.dumps(), status=404, mimetype='application/json')
    return response

# route to add a new package 
@app.route('/tourism', methods=['POST'])
def add_package():
    request_data = request.get_json()
    if(validObject(request_data)):
        
        Tourism.add_travel_package(request_data['city'], request_data['places_to_visit'], request_data['price'])
        response = Response("", 201, mimetype='application/json ')
        response.headers['Location'] = "/tourism/"+ str(request_data['city'])
        return response
    else:
        invalidtourismObjectErrorMsg = {
            "error": "invalid response",
            "helpString": "send data in correct format stupid"
            }
        response = Response(json.dumps(invalidtourismObjectErrorMsg), status=400, mimetype='application/json')
        return jsonify(request.get_json())


#route to get packages from 
@app.route('/tourism/<city>', methods=['GET'])
def get_city_package(city):
    print(city)
    data = [place for place in places_list if place['city'].lower() == city.lower()]
    return_value = Tourism.get_package_by_city(city)+data
    
    return jsonify(return_value)

app.run(port=5000, debug=True)
