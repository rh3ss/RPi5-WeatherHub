import os
import yaml
from pathlib import Path
from enum import Enum
from typing import Any, Optional

class Secret(Enum):
    API_KEY = "api_key"
    SENDER_EMAIL = "sender_email"
    SENDER_PASSWORD = "sender_password"
    RECIPIENT_EMAIL = "recipient_email"

class SecretsHelper:
    def __init__(self, file_path: str) -> None:
        path = Path(os.path.join("secrets", file_path))
        with open(path, "r") as f:
            self.data = yaml.safe_load(f) or {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        weather = self.data.get("weatherhub", {})
        return weather.get(key, default)

    def read_secret(self, secret: Secret, default: Optional[Any] = None) -> Any:
        return self.get(secret.value, default)
