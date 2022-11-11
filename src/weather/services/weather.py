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

        return output

    def validate(self, *key, response):
        val = response
        for ky in key:
            if type(ky) == str:
                val = val.get(ky, None)

            elif type(ky) == int:
                val = val[ky] if len(val) >= ky else None

            if val is None:
                break

        if val is None and response["cod"] != 200:
            return response["message"]
        elif val is None and response["cod"] == 200:
            return "Incomplete response from server"
        else:
            return val
