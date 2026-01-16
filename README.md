# RPi5-WeatherHub

RPi5-WeatherHub is a Raspberry Pi 5 weather dashboard showing live outdoor data from the OpenWeather API (https://openweathermap.org/) alongside indoor sensor measurements on a touch display.

Indoor temperature and humidity are measured using a DHT11 sensor, stored in a local SQLite database (`sensors.db`), and displayed as charts. If defined threshold values are exceeded, the user can be notified by email to ventilate the room.

Using on-screen navigation arrows, users can switch between the OpenWeather data view and the historical indoor sensor data view, providing a clear and interactive overview of both outdoor and indoor conditions.

<table>
  <tr>
    <td>
      <img width="800" height="480" alt="api" src="https://github.com/user-attachments/assets/62aa5be7-6b67-4803-b5ba-71f72b1bf4b6" />
    </td>
    <td>
      <img width="800" height="480" alt="test" src="https://github.com/user-attachments/assets/90d113d8-e209-4996-bcfb-e3e811272017" />
    </td>
  </tr>
</table>

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
