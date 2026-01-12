from flask import Flask, jsonify, render_template, send_from_directory
import urllib.request
import json
import time
import threading
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.appconfig import AppConfig
from src.utils.secrets import Secret, SecretsHelper
from src.utils.dbclient import DBClient
from src.utils.dhtclient import DHTClient
from src.utils.emailclient import EmailClient

config = AppConfig("config.toml")
base_url = config.apiconfig.base_url
city_name = config.apiconfig.city_name
country_code = config.apiconfig.country_code
trigger = config.apiconfig.ventilation_trigger
refresh_timer = config.apiconfig.refresh_timer_in_minutes
db_writing_frequency = config.apiconfig.db_writing_frequency_in_minutes

secret_helper = SecretsHelper("secrets.yaml")
api_key = secret_helper.read_secret(Secret.API_KEY)

db_client = DBClient("sensors.db")
dht_client = DHTClient()
email_client = EmailClient()

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

def db_writer() -> None:
    while True:
        dht_client.save_dht_data_to_db()
        time.sleep(60 * db_writing_frequency)

@app.route("/api/weather")
def api_weather():
    url = f"{base_url}?q={city_name},{country_code}&appid={api_key}&units=metric&lang=de"
    data = json.loads(urllib.request.urlopen(url).read())
    now = int(time.time())

    hourly = []
    for hour in data["list"]:
        if now <= hour["dt"] <= now + 86400:
            hourly.append({
                "dt": hour["dt"],
                "temp": hour["main"]["temp"],
                "temp_min": hour["main"]["temp_min"],
                "temp_max": hour["main"]["temp_max"],
                "feels_like": hour["main"]["feels_like"],
                "humidity": hour["main"]["humidity"],
                "wind_speed_kmh": round(hour["wind"]["speed"] * 3.6, 1),
                "icon": hour["weather"][0]["icon"],
                "desc": hour["weather"][0]["description"],
                "pop": hour.get("pop", 0)
            })

    return jsonify({
        "hourly": hourly,
        "sunrise": data["city"]["sunrise"],
        "sunset": data["city"]["sunset"]
    })

@app.route("/db/data")
def api_dbdata():
    rows = db_client.pull_from_db(
        "SELECT temperature, humidity, ventilated, timestamp FROM sensordata ORDER BY id DESC LIMIT 60"
    )
    
    temps = [row[0] for row in rows]
    hums = [row[1] for row in rows]
    vents = [row[2] for row in rows]
    
    return jsonify({
        "labels": [row[3][11:16] for row in rows],
        "temperature": temps,
        "humidity": hums,
        "ventilated": vents,
        "avg_temp": round(sum(temps)/len(temps), 1) if temps else NaN,
        "avg_hum": round(sum(hums)/len(hums), 1) if hums else NaN
    })

@app.route("/")
def index():
    return render_template("index.html", city=city_name, refresh_time=refresh_timer)

def open_browser():
    time.sleep(1)
    webbrowser.open("http://0.0.0.0:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    threading.Thread(target=db_writer, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
