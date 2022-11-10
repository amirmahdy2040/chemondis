from django.test import TestCase


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

