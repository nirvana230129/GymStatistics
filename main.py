import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


class Database:
    def __init__(self, db_file, table_name):
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()
        self.table_name = table_name

    def drop_table(self):
        self._cursor.execute(f'DROP TABLE IF EXISTS {self.table_name};')

    def create_table(self):
        self._cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                date DATE NOT NULL,
                machine TEXT NOT NULL,
                weight REAL,
                rating INTEGER,
                PRIMARY KEY (date, machine)
            );
        ''')

    def add_workout(self, date, machine, weight=None, rating=None):
        self._cursor.execute(f'''
            INSERT INTO {self.table_name} (date, machine, weight, rating)
            VALUES (?, ?, ?, ?)
        ''', (date, machine, weight, rating))

    def commit(self):
        self._connection.commit()

db = Database('gym_tracker.db', 'workouts')
db.drop_table()
db.create_table()
db.commit()
db.add_workout(str(datetime.today().date()), 'бицепс',35)
db.add_workout(datetime(2025, 3, 1).date(), 'Bench Press', 80, 4)
db.commit()
