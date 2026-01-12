import board
import adafruit_dht
from datetime import datetime
from src.utils.appconfig import AppConfig
from src.utils.dbclient import DBClient
from src.utils.emailclient import EmailClient

class DHTClient:
	def __init__(self) -> None:
		self.db_client = DBClient("sensors.db")
		self.email_client = EmailClient()
		self.config = AppConfig("config.toml")
		self.trigger = self.config.apiconfig.ventilation_trigger
		
		self.dht_sensor = adafruit_dht.DHT11(board.D14)
		self.last_email_tstmp = datetime.now()
		
	def get_dht_data(self) -> dict[str, float | str]:
		try:
			return {"temperature": round(self.dht_sensor.temperature, 1), "humidity": round(self.dht_sensor.humidity, 1)}
		except:
			return {"temperature": "N.A.", "humidity": "N.A."}

	def save_dht_data_to_db(self) -> None:
		data = self.get_dht_data()
		if data["temperature"] != "N.A.":
			temperature = data["temperature"]
			humidity = data["humidity"]
			timestamp = datetime.now().isoformat(timespec="seconds")
			
			self.db_client.push_to_db(
				"INSERT INTO sensordata (temperature, humidity, ventilated, timestamp) VALUES (?, ?, ?, ?)",
				(temperature, humidity, humidity > self.trigger, timestamp)
			)
			if self.email_client.should_send_email(humidity, self.last_email_tstmp):
				self.email_client.send_email(temperature, humidity, timestamp)
				self.last_email_tstmp = datetime.now()
