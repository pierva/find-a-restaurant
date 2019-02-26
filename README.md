## Simple API mashup

This application makes use of google geocoding API and foursquare API to return a restaurant in a specific location based on the meal type specified by the user.
Also the application has all the CRUD functionality to interact with the underneath database (sqlite).

### Getting Started
Download the repository and in the root folder create a file called `config.py`
This file will contain your API keys for the geocoder and foursquare APIs.

In the `config.py` file include the following:

```
foursquare_client_id = "<YOUR-CLIENT-ID"
foursquare_secret = "YOUR-SECRET"
GEOCODER_API_KEY = "YOUR-KEY"
foursquare_v = 20180323 #Use the version you need
```

### findARestaurant
The chore logic of the third party API calls is located in the `findARestaurant.py` file.
One single method `findARestaurant(mealType, location)` will return an object with the following info:
  ```
  {
    'name': 'restaurant_name',
    'address': 'restaurant_address',
    'image': 'picture_link'
  }
  ```

  The location passed in the `findARestaurant` method is an address (or city, country). This address will then sent to google to get the coordinates for the specific location.


### The views.py file
All the user API endpoints are located in the `views.py` file.
The available routes are:
```
/ and /restaurants (GET, POST)
/restaurants/<int:id> (GET, PUT, DELETE)
```
