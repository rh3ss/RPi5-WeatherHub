import os
import tomllib 
from typing import Any, Dict, Optional
from pathlib import Path

class ConfigSection:
    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data
 
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._data.get(key, default)
 
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data})"

class ApiConfig(ConfigSection):
	@property
	def base_url(self) -> str:
		return self._data["base_url"]
		
	@property
	def city_name(self) -> str:
		return self._data["city_name"]
		
	@property
	def country_code(self) -> str:
		return self._data["country_code"]
	
	@property
	def ventilation_trigger(self) -> int:
		return self._data["ventilation_trigger"]
		
	@property
	def refresh_timer_in_minutes(self) -> int:
		return self._data["refresh_timer_in_minutes"]
		
	@property
	def db_writing_frequency_in_minutes(self) -> int:
		return self._data["db_writing_frequency_in_minutes"]

class AppConfig:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(os.path.join("configs", file_path))
        self._raw_config: Dict[str, Any] = {}

        self._load()

        self.apiconfig = ApiConfig(self._raw_config.get("apiconfig", {}))

    def _load(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.file_path}")

        with self.file_path.open("rb") as f:
            self._raw_config = tomllib.load(f)
