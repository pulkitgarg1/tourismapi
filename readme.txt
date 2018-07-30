Deployment Instructions for Tourism Web Api 

Python 3 environment is required to run the project 
Dependencies are listed in requirements.txt file and must be installed before running.
The Server can be started using Python app.py command on local machine. 

The api can be accessed by the following link: 

1) http://localhost:5000/tourism
It will return the available packages in JSON.
Sample Response 
{
  "tourism": [
    {
      "city": "dublin", 
      "package": "3 days 2 nights", 
      "price": 300.0, 
      "weather_condition": "broken clouds", 
      "weather_temp": 18
    }, {package 2}, {package 3}
]
}
 


2) To access the service a registered user will need a TOKEN

http://localhost:5000/login 
Method: POST with username and password in JSON.

Sample : {"username":'api',password:'password'}

It will return a token

3) The package details can be accessed the link

http://localhost:5000/tourism/<cityname>?token=(token)

It will return the result in one of the format below.  

If Weather is Suitable 
[
    [
        {
            "city": "cork",
            "package": "2 Days 2 Nights",
            "price": 150,
            "weather_condition": "scattered clouds",
            "weather_temp": 22
        }
    ],
    {
        "Trip Highlights ": [
            {
                "city": "Cork",
                "place_to_visit": [
                    "St. Anne's Church Shandon Bells",
                    "Cork Butter Museum",
                    "Cork City Goal",
                    "Elizabeth Fort, Barrack Street",
                    "Cork Vision Centre",
                    "Collins Barracks Cork Military Museum",
                    "University College Cork (UCC)"
                ]
            }
        ]
    }
]

If weather is not Suitable

[
    [
        {
            "city": "dublin",
            "package": "3 days 2 nights",
            "price": 300,
            "weather_condition": "broken clouds",
            "weather_temp": 18
        }
    ],
    {
        "Current_weather_temp": 20,
        "Warning": "weather not suitable for travels",
        "ideal_temp_to_visit": 18
    }
]

The user can interact with the api by using GET,POST,PUT,PATCH,DELETE Methods. 