import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from .appconfig import AppConfig
from .secrets import Secret, SecretsHelper

class EmailClient:
    def __init__(self) -> None:
        self.config = AppConfig("config.toml")
        self.trigger = self.config.apiconfig.ventilation_trigger
        
        self.secret_helper = SecretsHelper("secrets.yaml")
        self.sender_email = self.secret_helper.read_secret(Secret.SENDER_EMAIL)
        self.sender_password = self.secret_helper.read_secret(Secret.SENDER_PASSWORD)
        self.recipient_email = self.secret_helper.read_secret(Secret.RECIPIENT_EMAIL)
        
        self.email_cooldown = timedelta(hours=1)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    def should_send_email(self, humidity: float, last_timestamp: datetime) -> bool:
        if humidity > self.trigger:
            return True

        if last_timestamp is not None and datetime.now() - last_timestamp >= self.email_cooldown:
            return True

        return False

    def send_email(self, temperatur_value: float, humidity_value: float, timestamp: datetime) -> None:
        subject = f"Luftfeuchtigkeit bei {humidity_value}%"
        body = (
            f"Lüftungsbenachrichtigung:\n\n"
            f"Uhrzeit: {timestamp}\n"
            f"Temperatur: {temperatur_value}°C\n"
            f"Luftfeuchtigkeit: {humidity_value}%\n"
        )

        msg = MIMEText(body)
        msg["To"] = self.recipient_email
        msg["Subject"] = subject

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
