# RPi5-WeatherHub

RPi5-WeatherHub is a Raspberry Pi 5–based weather dashboard that combines live outdoor weather data with indoor sensor measurements. Outdoor weather information is retrieved from the OpenWeather API (https://openweathermap.org/) for a configurable location and displayed on a connected touch display.

In addition to the external data, the system uses a DHT11 temperature and humidity sensor to collect indoor measurements. These values are stored locally in a SQLite database (`sensors.db`) and visualized as charts on the display.

Using on-screen navigation arrows, users can switch between the OpenWeather data view and the historical indoor sensor data view, providing a clear and interactive overview of both outdoor and indoor conditions.


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
