import sqlite3
from pathlib import Path
from sqlite3 import Connection, OperationalError


class Database:
    db_path: Path = Path("data").absolute() / "fuhrpark.db"

    @classmethod
    def _db(cls):
        db: Connection = sqlite3.connect(database=cls.db_path)
        with db:
            return db

    @classmethod
    def _select(cls, query: str, params: tuple=()):
        cursor = cls._db().cursor()
        result = cursor.execute(query, params)
        return result

    @classmethod
    def brand(cls):
        result = cls._select("SELECT name FROM marke").fetchall()
        return sorted([row[0] for row in result])

    @classmethod
    def model(cls, brand: str):
        result = cls._select("SELECT name FROM modell_name WHERE marke_name = ?", (brand,)).fetchall()
        return sorted([row[0] for row in result])

    @classmethod
    def base_data(cls, model: str):
        result = cls._select("SELECT * FROM daten WHERE modell_name = ?", (model,)).fetchall()
        if result:
            return [row for row in result[0]]
        else:
            return []


    @classmethod
    def get_data(cls, name: str):
        try:
            result = cls._select(f"SELECT DISTINCT {name} FROM daten").fetchall()
            return sorted([row[0] for row in result])
        except OperationalError:
            return []

    @classmethod
    def get_id(cls, table: str, column: str, value: str):
        result = cls._select(f"SELECT id FROM {table} WHERE {column} = ?", (value,)).fetchone()
        if result:
            return result[0]
        else:
            return -1

    @classmethod
    def insert(cls, values):
        with cls._db():
            cursor = cls._db().cursor()
            cursor.execute("""
            INSERT INTO fahrzeug (
                getriebe, kraftstoff, nummernschild,
                marke_id, modell_id, status_id, typ_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (values,))
            cls._db().commit()