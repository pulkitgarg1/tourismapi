from flask import Flask, jsonify, request, Response, render_template
from settings import *
from ApiModel import *
import jwt, datetime, json
from UserModel import User
#from functools import wraps
from place import places_list


placeslist = places_list
travels = Tourism.get_all_travel_package()


#cache to limit database access 
def updatetravelCache():
  global travels
  travels = Tourism.get_all_travel_package()

app.config['SECRET_KEY'] = 'DontLo$eit'

# valid token generation for valid users 
@app.route('/login', methods=['POST'])
def get_token():
    request_data=request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    match = User.username_password_match(username, password)
    if match:
      expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
      token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
      return token
    else:
<<<<<<< HEAD

      #return Response('', 401, mimetype='application/json')
      invalidUser = {
            "error": "invalid Login Credentials ",
            "helpString": "Verify api username and password "
            }
      response = Response(json.dumps(invalidUser), status=401, mimetype='application/json')
      return response
# token Required function 
=======
      return Response('', 401, mimetype='application/json')
'''
>>>>>>> 5830c2198c627f5e292e6e271765a050192a8ba2
def token_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    token = str(request.args.get('token'))
    try:
      jwt.decode(token, app.config['SECRET_KEY'])
      return f(*args, **kwargs)
    except:
      return jsonify({'error': 'Need a valid token to view this page'})
  return wrapper
<<<<<<< HEAD

#check if the payload is valid or not
=======
'''

>>>>>>> 5830c2198c627f5e292e6e271765a050192a8ba2
def validObject(Object):
    if("city" in Object and "package" in Object and "price" in Object):
        return True
    else:
        return False
#get all the travel packages 
@app.route('/tourism')
def get_package():
    return jsonify({'tourism': Tourism.get_all_travel_package()})

#update/replace packages 
@app.route('/tourism/<city>', methods=['PUT'])
@token_required
def update_package(city):
    request_data = request.get_json()
    Tourism.replace_package(city, request_data['package'],request_data['price'])
    updatetravelCache()
    response = Response("", status=204)
    return response


#working
#to patch the database 
@app.route('/tourism/<city>', methods=['PATCH'])
@token_required
def patch_database(city):
    request_data = request.get_json()
    updated_db = {}
    if ("package" in request_data):
        Tourism.update_place_to_visit(city, request_data['package'])
        updatetravelCache()
    if ("price" in request_data):
        Tourism.update_travel_price(city, request_data['price'])
        updatetravelCache()
    
    response = Response("", status=204)
    response.headers['Location'] = "/tourism/" + str(city)
    return response 

#Delete the package
@app.route('/tourism/<city>', methods=['DELETE'])
@token_required
def delete_entry(city):
    Tourism.delete_package(city)
    updatetravelCache()
    #response = Response(json.dumps(), status=404, mimetype='application/json')
    return "Travel Package has been deleted"

# route to add a new package 
@app.route('/tourism', methods=['POST'])
@token_required
def add_package():
    request_data = request.get_json()
    if(validObject(request_data)):
        a = request_data['places_to_visit']
        Tourism.add_travel_package(request_data['city'], request_data['package'], request_data['price'], request_data['weather_temp'])
        updatetravelCache()
        response = Response("", 201, mimetype='application/json ')
        response.headers['Location'] = "/tourism/"+ str(request_data['city'])
        data = {"city":request_data['city'],
                "places_to_visit":a
                }
        places_list.append(data)
        return response
    else:
        invalidtourismObjectErrorMsg = {
            "error": "invalid response",
            "helpString": "send data in correct format"
            }
        response = Response(json.dumps(invalidtourismObjectErrorMsg), status=400, mimetype='application/json')
        return response


#route to get packages
@app.route('/tourism/<city>', methods=['GET'])
@token_required
def get_city_package(city):
    print(city)
    return_value1 = Tourism.get_package_by_city(city)
    ideal_temp = Tourism.get_temp_by_city(city)
    data = [place for place in placeslist if place['city'].lower() == city.lower()]
    #return_value1 = Tourism.get_package_by_city(city)+data
    return_value = []
    for travel in travels:
      travelweather = int(Tourism.get_weather_temp(city))
      if (travel["city"] == city ) :
        if travelweather < int(ideal_temp):
      #if (travel["city"] == city) :
          return_value = {
          'Trip Highlights ': data
          }
        else:
          return_value ={
          'Warning' : "weather not suitable for travels",
          'Current_weather_temp': travelweather,
          'ideal_temp_to_visit': ideal_temp
          }
    

    return jsonify(return_value1, return_value )

  if __name__ == '__main__':
  app.run()
