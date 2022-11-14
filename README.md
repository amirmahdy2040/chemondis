# Chemondis

This application is intended to capture data from Openweather api.

It uses django, template, websocket for updating data, translation in 3 languages.

### Install
In order to install the application execute the following command.
```bash
sudo make build
sudo make start
```
or 
```
sudo make restart
```

Settings can be modified in /admin endpoint. (user: admin, pass: 123456)

NOTE: This page should be opened in another browser, or in incognito mode.

NOTE: These credentials should be changed in a more serious environment. 

```http
  POST /weather/
```
This endpoint sends a request for getting weather details for a city.
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `city` | `string` | **Required**. City name |


### Tests
There are unit-tests written in weather/services/tests_weather location that can be executed using following command.

```bash
python manage.py test 
```

NOTE: For the sake of simplicity there is an active TOKEN in tests, which should not be included in code.

NOTE: For the sake of simplicity, an instance of the application is deployed at http://23.88.40.119:8002




