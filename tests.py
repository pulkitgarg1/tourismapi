import unittest
from ApiModel import * 
import requests
import json
import sys
from UserModel import *

expected_response  = [[{"city": "dublin", "package": "3 days 2 nights", "price": 300.0, "weather_condition": "broken clouds", "weather_temp": 18}], {"Current_weather_temp": 24, "Warning": "weather not suitable for travels", "ideal_temp_to_visit": 18}]


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_get_package_details(self):
        response = requests.get('http://localhost:5000/tourism/dublin')
        
        self.assertEqual(response.json(),expected_response)
 
class TestFlaskApiAuthentication(unittest.TestCase):   
    def username_password_match(self):
    	test = User.username_password_match('api','password')
    	self.assertEqual(True,test)


expected_response1 = [{'city': 'dublin', 'package': '3 days 2 nights', 'weather_temp': 18, 'weather_condition': 'broken clouds', 'price': 300.0}]

class TestFlaskApi(unittest.TestCase):
    '''
    def test_Api(self):
       	response = self.app.get('http://localhost:5000/tourism/dublin')
       	self.assertEqual(json.loads(response.get_data().decode(sys.getdefaultencoding())),dublinresponse)
'''
    def test_get_package_details(self):
    	result = Tourism.get_package_by_city("dublin")
    	self.assertEqual(expected_response1, result)


if __name__ == "__main__":
    unittest.main()
