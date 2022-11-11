import requests
import json


class OpenWeather:

    def __init__(self) -> None:
        self.TOKEN = "TOKEN"
        self.URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}"

    # This function only calls the endpoint
    # TODO: Error handling should be added
    def raw_call(self, city):
        request_url = self.URL.format(city, self.TOKEN)
        response = requests.get(request_url)
        return response

    # This function returns the dict required for view
    # TODO: Error handling should be added
    def call(self, city):
        output = {}
        response = self.raw_call(city)
        response = json.loads(response.text)

        output["name"] = self.validate("name", response=response)
        output["description"] = self.validate("weather", 0, "description", response=response)
        output["temperature"] = {
            "min": self.validate("main", "temp_min", response=response),
            "max": self.validate("main", "temp_max", response=response)}
        output["humidity"] = self.validate("weather", "humidity", response=response)
        output["pressure"] = self.validate("weather", "pressure", response=response)
        output["wind"] = {
            "speed": self.validate("wind", "speed", response=response),
            "direction": self.degree_to_direction(self.validate("wind", "deg", response=response))}

        return output

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
