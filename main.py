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
                machine VARCHAR NOT NULL,
                weight REAL,
                rating INTEGER,
                description TEXT,
                PRIMARY KEY (date, machine)
            );
        ''')

    def add_workout(self, date: datetime.date, machine: str, weight: float = None, rating: int = None,
                    description: str = None):
        try:
            self._cursor.execute(f'''
                INSERT INTO {self.table_name} (date, machine, weight, rating, description)
                VALUES (?, ?, ?, ?, ?);
            ''', (date, machine, weight, rating, description))
        except sqlite3.IntegrityError:
            raise Exception(f'Workout with {machine} on {date} already exists')

    def commit(self):
        self._connection.commit()


db = Database('gym_tracker.db', 'workouts')
# db.drop_table()
# db.create_table()
# db.commit()
db.add_workout(str(datetime.today().date()), 'бицепс', 35)
db.add_workout(datetime(2025, 3, 1).date(), 'Bench Press', 60, 5)
db.add_workout(datetime(2025, 3, 2).date(), 'Bench Press', 62.5, 4)
db.add_workout(datetime(2025, 3, 3).date(), 'Bench Press', 65, 4)
db.add_workout(datetime(2025, 3, 4).date(), 'Bench Press', 70, 2)
db.commit()
print(type(datetime(2025, 3, 4).date()))
