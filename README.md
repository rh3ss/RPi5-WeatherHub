# RPi5-WeatherHub

RPi5-WeatherHub is a Raspberry Pi 5 weather dashboard showing live outdoor data from the OpenWeather API (https://openweathermap.org/) alongside indoor sensor measurements on a touch display.

Indoor temperature and humidity are measured using a DHT11 sensor, stored in a local SQLite database (`sensors.db`), and displayed as charts. If defined threshold values are exceeded, the user can be notified by email to ventilate the room.

Using on-screen navigation arrows, users can switch between the OpenWeather data view and the historical indoor sensor data view, providing a clear and interactive overview of both outdoor and indoor conditions.

<img width="560" height="336" alt="api" src="https://github.com/user-attachments/assets/62aa5be7-6b67-4803-b5ba-71f72b1bf4b6" />
<img width="560" height="336" alt="test" src="https://github.com/user-attachments/assets/90d113d8-e209-4996-bcfb-e3e811272017" />

## OpenWeather Forecast API
The OpenWeather Forecast API delivers detailed weather forecasts for the next 5 days with 3-hour time steps.  
It can be used to build weather applications, forecast visualizations, planning tools, or any feature that requires short-term weather predictions.

### Request:
```
https://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME},{COUNTRY_CODE}&appid={API_KEY}&units=metric&lang=de
```

### Response:
```json
{
    "cod": "200",
    "message": 0,
    "cnt": 40,
    "list": [
        {
            "dt": 1770630000,
            "main": {
                "temp": 3.2,
                "feels_like": -0.8,
                "temp_min": 2.9,
                "temp_max": 3.8,
                "pressure": 1009,
                "sea_level": 1009,
                "grnd_level": 996,
                "humidity": 86,
                "temp_kf": 0.0
            },
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "Überwiegend bewölkt",
                    "icon": "04d"
                }
            ],
            "clouds": {
                "all": 78
            },
            "wind": {
                "speed": 4.8,
                "deg": 310,
                "gust": 9.2
            },
            "visibility": 10000,
            "pop": 0.15,
            "rain": {
                "3h": 0.0
            },
            "sys": {
                "pod": "d"
            },
            "dt_txt": "2026-02-09 15:00:00"
        },
        [...]
    ],
    "city": {
        "id": 0,
        "name": "Bielefeld",
        "coord": {
            "lat": 52.0333,
            "lon": 8.5333
        },
        "country": "DE",
        "population": 331906,
        "timezone": 3600,
        "sunrise": 1770607200,
        "sunset": 1770643200
    }
}
```

## Configuration

Before running the application, fill in the file `secrets/secrets.yaml` with your credentials:

```yaml
weatherhub:
  api_key: [API_KEY]
  sender_email: [SENDER_EMAIL]
  sender_password: [SENDER_PASSWORD]
  recipient_email: [RECIPIENT_EMAIL]
```

## Installation

```
python3 -m venv .venv
source .venv/bin/activate
pip install flask
pip install pyyaml
pip install adafruit-blinka
pip install adafruit-circuitpython-dht
```

## Start Application
```
python3 app.py
```

## License
This project is intended for learning and personal use. Feel free to use and experiment.
