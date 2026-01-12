import os
import sqlite3
from pathlib import Path
from typing import List, Tuple, Any, Optional

class DBClient:
    def __init__(self, file_path: str) -> None:
        self.db_file = Path(__file__).resolve().parent / "data" / file_path
        self.db_file.parent.mkdir(parents=True, exist_ok=True)

        expression = """
            CREATE TABLE IF NOT EXISTS sensordata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                humidity REAL,
                ventilated BOOLEAN,
                timestamp TEXT
            )
        """
        self.push_to_db(expression)

    def _execute(self, sql: str, params: tuple = (), fetch: bool = False, commit: bool = False) -> Optional[List[Tuple[Any, ...]]]:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if commit:
                conn.commit()
            if fetch:
                return cursor.fetchall()
        return None

    def push_to_db(self, sql: str, params: tuple = ()) -> None:
        self._execute(sql, params=params, commit=True)

    def pull_from_db(self, sql: str, params: tuple = ()) -> List[Tuple[Any, ...]]:
        rows = self._execute(sql, params=params, fetch=True)
        return rows[::-1] if rows else []
