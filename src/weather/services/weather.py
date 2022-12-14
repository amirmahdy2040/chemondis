import requests
import json
import pickle
from weather.models import OpenWeatherToken
from django.utils.translation import gettext as _
from django.core.cache import cache


class OpenWeather:

    def __init__(self) -> None:
        try:
            token = OpenWeatherToken.objects.first()
            self.TOKEN = token.token
            self.LIFE_CYCYLE = token.cache * 60
        except:
            raise Exception(_("Token is not found"))
        self.URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}&units=metric"

    # This function only calls the endpoint
    # TODO: Error handling should be added
    def raw_call(self, city):
        request_url = self.URL.format(city, self.TOKEN)
        response = requests.get(request_url)
        return response

    # This function returns the dict required for view
    # TODO: Error handling should be added
    def call(self, city):
        cached_val = cache.get(city)

        if cached_val is not None:
            return pickle.loads(cached_val)

        else:
            output = {}
            response = self.raw_call(city)
            response = json.loads(response.text)
            if self.validate("cod", response=response) == 200:
                output["name"] = self.validate("name", response=response)
                output["description"] = self.validate("weather", 0, "description", response=response)
                output["temperature"] = {
                    "min": self.validate("main", "temp_min", response=response),
                    "max": self.validate("main", "temp_max", response=response)}
                output["humidity"] = self.validate("main", "humidity", response=response)
                output["pressure"] = self.validate("main", "pressure", response=response)
                output["wind"] = {
                    "speed": self.validate("wind", "speed", response=response),
                    "direction": self.degree_to_direction(self.validate("wind", "deg", response=response))}

                cache.set(city, pickle.dumps(output), timeout=self.LIFE_CYCYLE)
                return output
            else:
                return {"Error": self.validate("message", response=response)}

    # This function retrieves the desired key by checking the type of response
    # It will return a message if the key is not found
    # If the message key is not present an error "Incomplete response from server" will be sent
    # Note: The input is in multi-dimensional format
    # TODO: Error handling should be added
    def validate(self, *key, response):
        val = response
        for ky in key:
            if type(val) == dict:
                val = val.get(ky, None)

            elif type(val) == list:
                val = val[ky] if len(val) >= ky else None

            if val is None:
                return response.get("message", "Incomplete response from server")

        return val

    # This function divides the input degree by the number of directions needed
    # The residual of the above number and the number of directions is the direction
    # The direction should be in clockwise format.
    # Sub directions can also be added incuding NE, NW, ...
    # TODO: Error handling should be added
    def degree_to_direction(self, degree):
        dirs = ['N', 'E', 'S', 'W']
        ix = int(round(degree / (360. / len(dirs))))
        return dirs[ix % len(dirs)]
