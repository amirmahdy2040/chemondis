from unittest import TestCase


class TestWeather(TestCase):

    def setUp(self):
        pass

    def test_call_api(self):
        """
        This method checks the endpoint response to be valid for valid cities.
        """
        from weather.services.weather import OpenWeather
        ow = OpenWeather()
        cities = {"Berlin": 200, "Guangzhou": 200, "Notvalidcity": 404, "Munich": 200, "Tehran": 200}
        for city in cities:
            result = ow.raw_call(city=city)
            self.assertEqual(
                result.status_code, cities[city],
                msg=f"The response for {city} is not as expected {cities[city]}")

    def test_call(self):
        """
        This method checks if the reponse of the method is in dict format.
        """
        from weather.services.weather import OpenWeather
        ow = OpenWeather()
        cities = {"Berlin": "Berlin", "Guangzhou": "Guangzhou",
                  "Notvalidcity": "city not found", "Munich": "Munich", "Tehran": "Tehran"}
        for city in cities:
            result = ow.call(city=city)
            self.assertEqual(
                result["name"], cities[city],
                msg=f"The response for {city} is not as expected {cities[city]}")

    def test_validate_function(self):
        """
        This method check validate function inside class
        The response variable is an imaginary reponse from the Openweather
        """
        from weather.services.weather import OpenWeather
        ow = OpenWeather()
        response1 = {"weather": ["wind", "temperature", "humidity", {"description": "This is a desc"}]}
        response2 = {"weather": {"wind": "90", "temperature": "19", "humidity": "50", "description": "This is a desc"}}
        response3 = {"error": "Server error"}
        response4 = {"coord": {"lon": 13.4105, "lat": 52.5244},
                     "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                     "base": "stations",
                     "main":
                     {"temp": 284.98, "feels_like": 284.23, "temp_min": 283.7, "temp_max": 286.58, "pressure": 1020,
                      "humidity": 77},
                     "visibility": 10000, "wind": {"speed": 6.26, "deg": 226, "gust": 7.15},
                     "clouds": {"all": 0},
                     "dt": 1668162287,
                     "sys": {"type": 2, "id": 2011538, "country": "DE", "sunrise": 1668147639, "sunset": 1668180012},
                     "timezone": 3600, "id": 2950159, "name": "Berlin", "cod": 200}

        self.assertEqual(ow.validate("weather", 3, "description", response=response1), "This is a desc")
        self.assertEqual(ow.validate("weather", "description", response=response2), "This is a desc")
        self.assertEqual(
            ow.validate("weather", 3, "description", response=response3),
            "Incomplete response from server")
        self.assertEqual(ow.validate("weather", 0, "description", response=response4), "clear sky")
        self.assertEqual(ow.validate("main", "feels_like", response=response4), 284.23)
        self.assertEqual(ow.validate("clouds", "all", response=response4), 0)

    def test_degree_direction(self):
        """
        This method checks if the direction is correctly calculated
        """
        from weather.services.weather import OpenWeather
        ow = OpenWeather()

        degree = {30: "N", 0: "N", 44: "N", 46: "E", 360: "N", 480: "E"}
        for dg in degree:
            dir = ow.degree_to_direction(dg)
            self.assertEqual(dir, degree[dg])
